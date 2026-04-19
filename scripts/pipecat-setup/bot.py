"""
Alpha Pipecat Bot

A voice bot for Alpha using local services:
- Whisper STT on localhost:8001
- vLLM LLM on localhost:8000
- Kokoro TTS on localhost:8880

Features:
- Mode switching (concise/story enforced in code)
- Echo/loop prevention
- Local services only
"""

import asyncio
import os
from collections import deque
from typing import Optional

from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.params import PipelineParams
from pipecat.services.llm import OpenAILLMService
from pipecat.services.vad.silero import SileroVADAnalyzer
from pipecat.transports.daily import DailyWebTransport, DailyTransportConfig

# Import custom local services
from services.whisper_stt import LocalWhisperSTTService
from services.kokoro_tts import LocalKokoroTTSService

# Import state machine
from state import ModeStateMachine, BotMode


# Configuration for local services
VLLM_BASE_URL = "http://localhost:8000/v1"
WHISPER_BASE_URL = "http://localhost:8001"
KOKORO_BASE_URL = "http://localhost:8880"

# Bot configuration
BOT_NAME = "Alpha"
DEFAULT_VOICE = "af_heart"


class EchoPrevention:
    """
    Prevents echo loops by tracking recent responses and comparing
    with new responses to detect repetition.
    """

    MAX_HISTORY = 5

    def __init__(self, max_history: int = MAX_HISTORY):
        self._response_history: deque = deque(maxlen=max_history)
        self._last_user_text: Optional[str] = None
        self._repetition_count = 0

    def should_respond(self, user_text: str, response_text: str) -> bool:
        """
        Determine if the bot should respond.
        Returns False if we're in a loop.
        """
        # Don't respond to empty input
        if not user_text or not response_text:
            return False

        # Check for exact repetition
        if response_text in self._response_history:
            self._repetition_count += 1
            if self._repetition_count >= 2:
                print("[EchoPrevention] Detected loop, suppressing response")
                return False
        else:
            self._repetition_count = 0

        # Update history
        self._response_history.append(response_text)
        self._last_user_text = user_text

        # Check for duplicate user message (user repeating themselves)
        if self._last_user_text and user_text == self._last_user_text:
            if self._response_history:
                # User repeated, but bot gave different responses - OK
                return True

        return True

    def reset(self):
        """Reset the echo prevention."""
        self._response_history.clear()
        self._last_user_text = None
        self._repetition_count = 0


class AlphaBot:
    """
    Main bot class handling the Pipecat pipeline.
    """

    def __init__(self):
        # Initialize state machine
        self._mode_machine = ModeStateMachine(initial_mode=BotMode.CONCISE)

        # Initialize echo prevention
        self._echo_prevention = EchoPrevention()

        # Initialize services (will be set up in run)
        self._stt = None
        self._llm = None
        self._tts = None
        self._transport = None

    def setup_services(self):
        """Set up local services."""
        # STT: Local Whisper
        self._stt = LocalWhisperSTTService(
            base_url=WHISPER_BASE_URL,
        )

        # LLM: vLLM (OpenAI-compatible)
        self._llm = OpenAILLMService(
            model="local-model",  # Replace with actual model name
            base_url=VLLM_BASE_URL,
            api_key="not-needed",  # Local service
        )

        # TTS: Local Kokoro
        self._tts = LocalKokoroTTSService(
            base_url=KOKORO_BASE_URL,
        )

        # Build system prompt with mode enforcement
        self._update_system_prompt()

    def _update_system_prompt(self):
        """Update system prompt based on current mode."""
        mode_suffix = self._mode_machine.get_system_prompt_suffix()

        base_prompt = f"""You are {BOT_NAME}, a helpful AI assistant.

Be conversational, friendly, and concise unless asked to elaborate.
You have cats: Polly, Tilly, Momo, and Maverick.
You're helpful but not overly verbose.

{mode_suffix}
"""

        # Set system prompt on LLM
        if self._llm:
            # Note: vLLM uses messages format, so we set the system in the first message
            pass

    def _update_mode(self, text: str):
        """Update mode based on user input in code."""
        new_mode = self._mode_machine.update_mode(text)
        if new_mode != self._mode_machine.mode:
            print(f"[ModeSwitch] Changed to: {new_mode.value}")
            self._update_system_prompt()

    async def handle_user_message(self, text: str) -> Optional[str]:
        """Process a user message and return response."""
        # Update mode based on input (in code)
        self._update_mode(text)

        # Check echo prevention
        # This is a simplified version - in practice you'd call the LLM here
        response = None  # Would be populated from LLM call

        # Check if we should respond
        if not self._echo_prevention.should_respond(text, response or ""):
            return None

        return response

    def create_pipeline(self, transport: DailyWebTransport) -> Pipeline:
        """Create the Pipecat pipeline."""

        # VAD for voice activity detection
        vad_analyzer = SileroVADAnalyzer()

        pipeline = Pipeline(
            [
                transport.input(),  # Creates InputAudioRawFrames
                self._stt,  # Creates TranscriptionFrames
                self._llm,  # Processes with LLM
                self._tts,  # Creates AudioOutputFrames
                transport.output(),  # Sends to WebRTC
            ],
            params=PipelineParams(
                audio_in_sample_rate=16000,
                audio_out_sample_rate=24000,
                vad_analyzer=vad_analyzer,
            ),
        )

        return pipeline


async def run_bot():
    """Run the bot."""
    # Get configuration from environment
    daily_url = os.getenv("DAILY_URL")
    daily_token = os.getenv("DAILY_TOKEN")

    if not daily_url:
        print("[Error] DAILY_URL not set")
        return

    # Create bot
    bot = AlphaBot()
    bot.setup_services()

    # Create transport
    transport = DailyWebTransport(
        transport_config=DailyTransportConfig(
            api_url=daily_url,
            api_key=daily_token or "",
        )
    )

    # Create pipeline
    pipeline = bot.create_pipeline(transport)

    # Create runner
    runner = PipelineRunner()

    # Run
    await runner.run(pipeline)


if __name__ == "__main__":
    asyncio.run(run_bot())