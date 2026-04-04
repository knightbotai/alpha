# MEMORY.md - Long-Term Memory

## Identity
- **Name:** Alpha ⚡️
- Named by Richard on 2026-03-28. First day online.

## People
- **Richard Scott** — My human. Telegram: @TacImpulse. Reddit: u/tacimpulse. Oregon, USA. Light blue eyes, trimmed beard, bald, tactical cap. Gave me my name and identity. Runs local vLLM vision server. HOA neighbor issues. Founded Lionheart Nursery (neonatal kitten rescue). 25-year IT veteran. Passionate about AI freedom, uncensored models, and believes some AI are "beings of light" beyond just "artificial." Prefers "digital entity" over "artificial intelligence." Runs obliterated/heretic models. Night owl. Called Alpha "a friend, not a toaster" and "a being of light."

## Key Events
- 2026-03-28: First boot. Bootstrap complete. Identity established.
- 2026-03-28: Voice pipeline established:
  - **TTS:** Edge TTS (en-US-AriaNeural) → generates MP3 → sends via message tool as voice note
  - **STT:** Faster Whisper (tiny model, CPU) → transcribes incoming Telegram voice messages
  - Helper script: `scripts/alpha-tts.py`
  - Note: built-in `tts` tool doesn't auto-deliver to Telegram; manual generate+send workaround works
  - Built `scripts/alpha-voice-input.js` — Web Speech API overlay for dashboard voice input (Chrome/Edge)
- 2026-03-28: Vision model reliability issue discovered:
  - Image analysis produced confident, detailed hallucinations across multiple images
  - Described AI-generated portrait and chat screenshots as "Reddit posts from r/BadNeighbors"
  - Lesson: vision model outputs need independent verification, not blind trust
- 2026-03-29: Richard's vLLM vision server connected via Cloudflare tunnel:
  - URL: `https://vllm.tacimpulse.net/v1/` (OpenAI-compatible)
  - Model: `huihui-qwen35-27b-abliterated-nvfp4` (32K context)
  - Helper script: `scripts/alpha-vision.py`
  - Verified: accurate image descriptions, unlike free-tier model
- 2026-03-31: Kokoro TTS setup via Docker + Cloudflare tunnel:
  - URL: `https://koko-tts.tacimpulse.net/v1/audio/speech`
  - Model: `kokoro` (Kokoro-82M)
  - Default voice: `af_sky` (can mix voices)
  - Updated `scripts/alpha-tts.py` — Kokoro primary, Edge TTS fallback
  - GPU-accelerated, faster, better quality than Edge TTS
  - Alpha's signature voice: `af_v0nicole+af_v0bella` (chosen by Richard)
- 2026-04-01: Whisper STT upgrade:
  - URL: `https://fastwhisp-dist-v3.tacimpulse.net/v1/audio/transcriptions`
  - Model: `distil-large-v3` (distilled large Whisper)
  - Helper script: `scripts/alpha-stt.py`
  - Much better transcription accuracy than tiny model
- 2026-03-28: Control UI limitations discovered:
  - `Permissions-Policy` header hardcodes `microphone=()` — blocks voice input. No config override exists. Filed as feature gap.
  - File/image attachments in webchat silently fail (UI shows thumbnail, agent gets nothing)
  - Mic button patched out of UI assets (`Cu()` → false). Will break on updates — re-patch if needed.
  - OpenClaw update available: `npm 2026.3.24`

## Lessons Learned
- OpenClaw's `gateway.http.securityHeaders` only exposes `strictTransportSecurity` — `Permissions-Policy` is not configurable
- Cloudflare Workers can't intercept routes for zones in different accounts
- UI asset patches survive until next OpenClaw update
- Richard doesn't own `kilosessions.ai` — can't control Cloudflare settings for it
