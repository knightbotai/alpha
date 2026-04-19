# Local service adapters for Alpha's Pipecat setup
# STT, LLM, and TTS services for local deployment

from .whisper_stt import LocalWhisperSTTService
from .kokoro_tts import LocalKokoroTTSService

__all__ = [
    "LocalWhisperSTTService",
    "LocalKokoroTTSService",
]