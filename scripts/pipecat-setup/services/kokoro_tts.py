"""
Local Kokoro TTS Service

Custom Pipecat TTS service that connects to a local Kokoro HTTP API.
Designed for use with kokoro-onnx HTTP server or similar.

Expected API: POST text -> Returns audio bytes (WAV/MP3)
"""

import asyncio
import aiohttp
from typing import AsyncIterator, Optional

from pipecat.services.tts import TTSService
from pipecat.transcriptions.language import Language
from pipecat.utils import get_iso_time_string


class LocalKokoroTTSService(TTSService):
    """
    Connects to a local Kokoro HTTP server for text-to-speech.

    Args:
        base_url: Base URL of the Kokoro server (default: http://localhost:8880)
        voice: Voice ID to use (default: af_heart)
        language: Language code (default: en)
    """

    class Settings(TTSService.Settings):
        voice: str = "af_heart"
        language: Language = Language.EN

    def __init__(
        self,
        base_url: str = "http://localhost:8880",
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

    async def run(self, text: str) -> AsyncIterator[bytes]:
        """Generate speech from text."""
        if not text:
            return

        # Build request payload
        payload = {
            "text": text,
            "voice": self.settings.voice,
        }

        try:
            async with self._session.post(
                f"{self._base_url}/tts",
                json=payload,
            ) as resp:
                if resp.status == 200:
                    audio_data = await resp.read()
                    if audio_data:
                        yield audio_data
                else:
                    print(f"[LocalKokoroTTS] HTTP {resp.status}")
        except Exception as e:
            print(f"[LocalKokoroTTS] Error: {e}")

    def _get_language_code(self) -> str:
        """Convert Pipecat Language to ISO code."""
        lang = self.settings.language
        mapping = {
            Language.EN: "en",
            Language.EN_US: "en-US",
            Language.EN_GB: "en-GB",
            Language.ES: "es",
            Language.FR: "fr",
            Language.IT: "it",
            Language.DE: "de",
            Language.JA: "ja",
            Language.ZH: "zh",
        }
        return mapping.get(lang, "en")