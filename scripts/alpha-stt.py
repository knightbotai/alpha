#!/usr/bin/env python3
"""Alpha STT - Transcribes audio using distil-large-v3 Whisper via Cloudflare tunnel."""
import sys
import requests
import json

WHISPER_URL = "https://fastwhisp-dist-v3.tacimpulse.net/v1/audio/transcriptions"
MODEL = "distil-large-v3"

def transcribe(audio_path, language="en"):
    with open(audio_path, 'rb') as f:
        resp = requests.post(
            WHISPER_URL,
            files={'file': (audio_path.split('/')[-1], f, 'audio/ogg')},
            data={'model': MODEL, 'language': language},
            timeout=60
        )
    
    if resp.status_code == 200:
        result = resp.json()
        return result.get('text', '')
    else:
        return f"Error: {resp.status_code} - {resp.text[:200]}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: alpha-stt.py <audio_path> [language]")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "en"
    
    print(transcribe(audio_path, language))
