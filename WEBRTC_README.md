# Alpha WebRTC - Quick Start Guide

## What This Does

Real-time voice conversation with Alpha through your browser! No phone calls, no latency wait — just speak and hear responses.

## Prerequisites

1. **Python 3.10+** on your Windows machine
2. **Cloudflare tunnels** running for:
   - `fastwhisp-dist-v3.tacimpulse.net` (Whisper STT)
   - `vllm.tacimpulse.net` (vLLM reasoning)
   - `koko-tts.tacimpulse.net` (Kokoro TTS)

## Setup

### 1. Install FastRTC

Open PowerShell or Command Prompt and run:

```powershell
pip install "fastrtc[vad, tts]" numpy requests
```

### 2. Get the Code

Clone the repo or just download `alpha-webrtc.py` from:
https://github.com/knightbotai/alpha/blob/master/scripts/alpha-webrtc.py

### 3. Run It!

```powershell
python alpha-webrtc.py
```

You'll see a URL like `http://localhost:7860` — open that in Chrome or Edge.

## Usage

1. Click "Start" to enable your microphone
2. Speak naturally — the system detects when you pause
3. Alpha processes your speech and responds through your speakers
4. Chat history is maintained for context

## Troubleshooting

### "Module not found" error
Run the pip install command again — make sure you're using the quotes:
`pip install "fastrtc[vad, tts]" numpy requests`

### Can't connect to services
Check your Cloudflare tunnels are running:
```powershell
curl https://fastwhisp-dist-v3.tacimpulse.net/health
curl https://vllm.tacimpulse.net/health
curl https://koko-tts.tacimpulse.net/health
```

### Audio issues
- Make sure your microphone is not muted
- Check Windows sound settings
- Try using headphones to avoid echo

## Current Version

This is a **prototype** — simple but functional. It:
- ✅ Handles voice activity detection
- ✅ Connects to your existing Whisper/vLLM/Kokoro services
- ✅ Maintains chat history for context

Future upgrades planned:
- Avatar lip-sync
- Camera/screen awareness
- Lower latency