#!/usr/bin/env python3
"""
Alpha WebRTC Prototype - Real-time Voice Chat
Uses FastRTC to connect STT -> LLM -> TTS via WebRTC

Requirements:
    pip install "fastrtc[vad, tts]" numpy requests

Usage:
    python alpha-webrtc.py
    # Then open the URL shown in terminal
"""

import os
import requests
import numpy as np
from fastrtc import Stream, ReplyOnPause, audio_to_bytes, aggregate_bytes_to_16bit

# === Configuration ===
# LOCAL addresses (faster!) - use these if services are on same machine
WHISPER_URL = os.getenv("WHISPER_URL", "http://localhost:8001/v1/audio/transcriptions")
VLLM_URL = os.getenv("VLLM_URL", "http://localhost:8000/v1/chat/completions")
VLLM_MODEL = os.getenv("VLLM_MODEL", "huihui-qwen35-27b-abliterated-nvfp4")
KOKORO_URL = os.getenv("KOKORO_URL", "http://localhost:8880/v1/audio/speech")
KOKORO_VOICE = os.getenv("KOKORO_VOICE", "af_v0nicole+af_v0bella")

# Cloudflare fallback (for remote access - slower!)
# WHISPER_URL = "https://fastwhisp-dist-v3.tacimpulse.net/v1/audio/transcriptions"
# VLLM_URL = "https://vllm.tacimpulse.net/v1/chat/completions"
# KOKORO_URL = "https://koko-tts.tacimpulse.net/v1/audio/speech"

# Chat history
chat_history = []
is_processing = False  # Flag to prevent generator conflicts


def transcribe(audio_tuple):
    """Send audio to Whisper and get text."""
    sample_rate, audio_data = audio_tuple
    
    # Convert numpy array to bytes
    audio_bytes = audio_to_bytes((sample_rate, audio_data))
    
    # Send to Whisper
    files = {'file': ('audio.wav', audio_bytes, 'audio/wav')}
    data = {'model': 'distil-large-v3', 'language': 'en'}
    
    try:
        resp = requests.post(WHISPER_URL, files=files, data=data, timeout=30)
        if resp.status_code == 200:
            result = resp.json()
            return result.get('text', '')
        else:
            print(f"Whisper error: {resp.status_code} - {resp.text}")
            return ""
    except Exception as e:
        print(f"Whisper error: {e}")
        return ""


def generate_response(text):
    """Send text to vLLM and get response."""
    if not text.strip():
        return ""
    
    # Add user message to history
    chat_history.append({"role": "user", "content": text})
    
    # Keep history manageable (last 10 messages)
    messages = chat_history[-10:]
    
    payload = {
        "model": VLLM_MODEL,
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    try:
        resp = requests.post(VLLM_URL, json=payload, timeout=60)
        if resp.status_code == 200:
            result = resp.json()
            response = result['choices'][0]['message']['content']
            chat_history.append({"role": "assistant", "content": response})
            return response
        else:
            print(f"vLLM error: {resp.status_code} - {resp.text}")
            return "Sorry, I had trouble thinking just now."
    except Exception as e:
        print(f"vLLM error: {e}")
        return "Sorry, I'm having trouble connecting right now."


def text_to_speech(text):
    """Send text to Kokoro and get audio."""
    if not text.strip():
        return None
    
    payload = {
        "input": text,
        "voice": KOKORO_VOICE
    }
    
    try:
        resp = requests.post(KOKORO_URL, json=payload, timeout=30)
        print(f"Kokoro response status: {resp.status_code}")
        if resp.status_code == 200:
            # Kokoro returns raw audio (MP3), need to decode properly
            audio_data = resp.content
            print(f"Kokoro audio size: {len(audio_data)} bytes")
            
            # Try using scipy to convert MP3 to raw PCM
            try:
                from scipy.io import wavfile
                import io
                # Use soundfile instead for better MP3 support
                import soundfile as sf
                # Read MP3 data
                audio_array, sample_rate = sf.read(io.BytesIO(audio_data), dtype='int16')
                print(f"Decoded: {sample_rate}Hz, {len(audio_array)} samples")
                yield (sample_rate, audio_array.T)  # Transpose for FastRTC format
            except ImportError:
                # Fallback: if no scipy/soundfile, yield raw and let FastRTC handle it
                print("scipy/soundfile not available, trying direct yield")
                audio_array = np.frombuffer(audio_data, dtype=np.uint8)
                yield (24000, audio_array.reshape(1, -1))
        else:
            print(f"Kokoro error: {resp.status_code} - {resp.text[:200]}")
    except Exception as e:
        print(f"Kokoro exception: {e}")


def handler(audio):
    """Main handler - STT -> LLM -> TTS"""
    global is_processing
    
    # Skip if already processing (prevents generator conflicts)
    if is_processing:
        print("Already processing, skipping input")
        return
    
    # Step 1: Transcribe
    text = transcribe(audio)
    if not text or len(text.strip()) < 2:
        print("Empty or too short, skipping")
        return
    
    # Check for echo/loop
    if chat_history and chat_history[-1].get("role") == "assistant":
        last_response = chat_history[-1].get("content", "").lower()
        if text.lower().strip() == last_response.strip():
            print("Same as last response, adding variation")
            text = text + " (continuing)"
    
    print(f"You: {text}")
    
    # Set flag to prevent concurrent processing
    is_processing = True
    
    try:
        # Step 2: Generate response
        response = generate_response(text)
        if not response:
            print("No response generated")
            return
        
        print(f"Alpha: {response}")
        
        # Step 3: Synthesize speech
        for audio_chunk in text_to_speech(response):
            yield audio_chunk
    finally:
        is_processing = False


# Create the stream with VAD tuning
# Mode options: "noise", "standard", "sensitive" - default is "standard"
stream = Stream(
    handler=ReplyOnPause(handler),
    modality="audio",
    mode="send-receive"
)

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🎙️  Alpha WebRTC - Real-time Voice")
    print("="*50)
    print("\nUsing LOCAL services (fast!):")
    print(f"  - Whisper: {WHISPER_URL}")
    print(f"  - vLLM: {VLLM_URL}")
    print(f"  - Kokoro: {KOKORO_URL}")
    print("\nOpen http://localhost:7860 in Chrome/Edge")
    print("Click Start, then speak!\n")
    
    # Launch the UI
    stream.ui.launch()