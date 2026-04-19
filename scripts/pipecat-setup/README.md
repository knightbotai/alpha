# Alpha Pipecat Bot

A local voice bot for Alpha using Pipecat framework with local services.

## Architecture

```
┌─────────────┐
│   User     │
│  (WebRTC)  │
└─────┬───────┘
      │ audio
      ▼
┌─────────────────────────────────────────────────────────┐
│                    Pipecat Pipeline                     │
├─────────┬─────────┬─────────────────────────────────────┤
│   STT   │   LLM  │                TTS                  │
│         │        │                                     │
│ Whisper │  vLLM  │             Kokoro                 │
│ :8001   │ :8000  │              :8880                 │
└─────────┴────────┴─────────────────────────────────────┘
```

## Local Services Required

1. **vLLM** (port 8000): OpenAI-compatible API for LLM inference
2. **Whisper STT** (port 8001): HTTP API for speech-to-text
3. **Kokoro TTS** (port 8880): HTTP API for text-to-speech

## Quick Start

### 1. Setup

```powershell
# Run the setup script
.\setup.ps1
```

### 2. Configure Environment

Edit `.env` with your Daily.co room settings:
```
DAILY_URL=https://your-room.daily.co/room-name
DAILY_TOKEN=your-room-token
```

### 3. Start Local Services

Start your local services on the specified ports:
- vLLM on `localhost:8000`
- Whisper (faster-whisper-server or similar) on `localhost:8001`
- Kokoro TTS on `localhost:8880`

### 4. Run the Bot

```powershell
python bot.py
```

## Features

### Mode Switching (Code-Enforced)

The bot supports two modes enforced in code (not prompts):
- **CONCISE**: Brief, direct responses
- **STORY**: Narrative, descriptive responses

Mode is automatically detected from user input:
- Story triggers: "tell me a story", "what happens next", "continue", etc.
- Concise triggers: "what is", "when did", "quick", etc.

### Echo Prevention

The `EchoPrevention` class tracks recent responses and detects loops:
- Suppresses response if detected repeated 2+ times
- Prevents infinite conversation loops

### Local Services Only

All processing happens locally:
- No external API calls for STT/LLM/TTS
- Data never leaves your machine

## File Structure

```
alpha-pipecat/
├── bot.py              # Main bot code
├── state.py           # Mode state machine
├── requirements.txt  # Python dependencies
├── setup.ps1        # Windows setup script
└── services/
    ├── __init__.py
    ├── whisper_stt.py  # Local Whisper adapter
    └── kokoro_tts.py  # Local Kokoro adapter
```

## Troubleshooting

### Port Already in Use

If you get "Address already in use", check what's using the port:
```powershell
netstat -ano | findstr "8000"
```

### Connection Refused

Make sure your local services are running:
- vLLM: `curl http://localhost:8000/v1/models`
- Whisper: `curl http://localhost:8001/health`
- Kokoro: `curl http://localhost:8880/health`

### Audio Issues

Ensure correct sample rates in PipelineParams:
- Input: 16000 Hz
- Output: 24000 Hz

## Dependencies

- Python 3.10+
- pipecat-ai >= 0.0.100
- aiohttp >= 3.9.0
- silero-vad >= 0.0.3