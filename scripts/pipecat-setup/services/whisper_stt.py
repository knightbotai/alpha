"""
Local Whisper STT Service

Custom Pipecat STT service that connects to a local Whisper HTTP API.
Designed for use with faster-whisper-server or similar local Whisper servers.

Expected API: POST audio bytes ->Returns JSON with "text" field
"""

import asyncio
import aiohttp
from typing import AsyncIterator, Optional

from pipecat.audio.aivoice_output_frame import AIVoiceOutputFrame
from pipecat.services.stt import STTService
from pipecat.transcriptions.language import Language
from pipecat.utils import get_iso_time_string


class LocalWhisperSTTService(STTService):
    """
    Connects to a local Whisper HTTP server for speech-to-text.

    Args:
        base_url: Base URL of the Whisper server (default: http://localhost:8001)
        language: Language code for transcription (default: en)
        prompt: Optional prompt to guide transcription
    """

    class Settings(STTService.Settings):
        language: Language = Language.EN
        prompt: Optional[str] = None

    def __init__(
        self,
        base_url: str = "http://localhost:8001",
        settings: Optional[Settings] = None,
        **kwargs,
    ):
        super().__init__(settings=settings, **kwargs)
        self._base_url = base_url.rstrip("/")
        self._session: Optional[aiohttp.ClientSession] = None

    async def start(self):
        await super().start()
        self._session = aiohttp.ClientSession()

    async def stop(self):
        await super().stop()
        if self._session:
            await self._session.close()
            self._session = None

    async def run(self, frames: AsyncIterator) -> AsyncIterator[str]:
        """Process audio frames and yield transcriptions."""
        audio_data = b""
        async for frame in frames:
            if isinstance(frame, AIVoiceOutputFrame):
                audio_data += frame.data

        if not audio_data:
            return

        # Send to local Whisper server
        try:
            async with self._session.post(
                f"{self._base_url}/transcribe",
                data=audio_data,
                headers={"Content-Type": "audio/wav"},
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    text = result.get("text", "").strip()
                    if text:
                        yield text
                else:
                    # Try alternative endpoint path
                    pass
        except Exception as e:
            print(f"[LocalWhisperSTT] Error: {e}")

    def _get_language_code(self) -> str:
        """Convert Pipecat Language to ISO code."""
        lang = self.settings.language
        if lang == Language.EN:
            return "en"
        elif lang == Language.EN_US:
            return "en"
        elif lang == Language.EN_GB:
            return "en"
        # Add other languages as needed
        return "en"