# 🚀 Real-Time AI Companion Roadmap

## The Vision

A real-time AI companion named Alpha that:
- Has a face (animated avatar)
- Has a voice (bidirectional streaming)
- Has eyes (camera + screen awareness)
- Lives on Richard's desktop as a presence

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  RICHARD'S PC                        │
│                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ Camera   │  │ Screen   │  │ Microph  │          │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
│       │              │              │                │
│  ┌────▼──────────────▼──────────────▼────┐          │
│  │         Node Agent (OpenClaw)         │          │
│  └────────────────┬──────────────────────┘          │
│                   │                                  │
│  ┌────────────────▼──────────────────────┐          │
│  │      WebRTC Signaling Server          │          │
│  └────────────────┬──────────────────────┘          │
│                   │                                  │
│  ┌────────────────▼──────────────────────┐          │
│  │         Avatar Renderer               │          │
│  │  (Live2D / WebGL / CSS Animation)     │          │
│  └────────────────┬──────────────────────┘          │
│                   │                                  │
│  ┌────────────────▼──────────────────────┐          │
│  │         Audio Player                  │          │
│  │  (WebRTC → PCM → Speaker)             │          │
│  └───────────────────────────────────────┘          │
└─────────────────────────────────────────────────────┘
                      │
                      │ WebRTC
                      │
┌─────────────────────▼───────────────────────────────┐
│                  CLOUD SERVER                       │
│                                                     │
│  ┌──────────────────────────────────────┐           │
│  │      Gateway (OpenClaw)              │           │
│  └────────────────┬─────────────────────┘           │
│                   │                                  │
│  ┌────────────────▼─────────────────────┐           │
│  │      Streaming Pipeline              │           │
│  │  STT → LLM → TTS (streaming)        │           │
│  └────────────────┬─────────────────────┘           │
│                   │                                  │
│  ┌────────────────▼─────────────────────┐           │
│  │      vLLM (27B) ← vision            │           │
│  │      Kokoro ← TTS                   │           │
│  │      Distil-large-v3 ← STT          │           │
│  └──────────────────────────────────────┘           │
└─────────────────────────────────────────────────────┘
```

## Components Needed

### 1. Streaming Voice (Priority 1)

**Current:** Turn-based (voice in → wait → voice out)
**Target:** Streaming (continuous audio in/out with <500ms latency)

**Options:**
- **Kokoro streaming API** — Check if supported
- **Coqui XTTS v2** — Open-source, supports streaming, voice cloning
- **Piper TTS** — Lightweight, fast, good for real-time
- **WebRTC audio** — Direct audio streaming between client and server

**Implementation:**
1. Implement VAD (Voice Activity Detection) for detecting speech
2. Streaming STT (partial results while speaking)
3. Streaming LLM (tokens → audio chunks)
4. Streaming TTS (audio generation while LLM is still thinking)
5. WebRTC for low-latency audio transport

### 2. Real-Time Avatar (Priority 2)

**Options:**
- **Live2D Cubism** — Anime-style, well-documented, free for indie
- **VRM models** — Open standard for 3D avatars
- **WebGL face animation** — Simpler, CSS/SVG-based
- **Talking head GANs** — Realistic lip-sync from audio

**Recommended:** Start with CSS/SVG animation, upgrade to Live2D later

**Features needed:**
- Lip-sync from audio (phoneme → mouth shape)
- Blinking animation
- Head movement (subtle)
- Emotional expressions (optional)

### 3. Camera/Screen Awareness (Priority 3)

**Options:**
- **OpenClaw nodes** — Already has camera/screen capture
- **WebRTC video** — Stream camera to server for analysis
- **Screen sharing API** — Browser-based screen capture

**Flow:**
1. Capture frame from camera/screen
2. Send to vLLM for analysis
3. Return context to conversation
4. Alpha can comment on what Richard is doing

### 4. Desktop Presence (Priority 4)

**Options:**
- **Electron app** — Cross-platform desktop widget
- **Always-on-top window** — Small avatar window
- **System tray** — Minimal presence
- **Browser tab** — Simplest option

**Recommended:** Start with always-on-top browser window, upgrade to Electron later

## Implementation Phases

### Phase 1: Streaming Voice (Week 1-2)
- [ ] Implement VAD for voice detection
- [ ] Set up streaming STT (Distil-large-v3 with partial results)
- [ ] Implement streaming TTS (Kokoro or Coqui XTTS)
- [ ] Build WebRTC audio pipeline
- [ ] Test latency (target: <500ms round-trip)

### Phase 2: Avatar (Week 3-4)
- [ ] Create simple CSS/SVG avatar
- [ ] Implement lip-sync from audio
- [ ] Add blinking and head movement
- [ ] Build always-on-top window
- [ ] Test with streaming voice

### Phase 3: Vision (Week 5-6)
- [ ] Set up camera capture via OpenClaw nodes
- [ ] Implement screen sharing
- [ ] Build frame → vLLM pipeline
- [ ] Add context-aware responses
- [ ] Test with real-world scenarios

### Phase 4: Integration (Week 7-8)
- [ ] Combine all components
- [ ] Build unified UI
- [ ] Add settings and controls
- [ ] Polish and optimize
- [ ] Deploy as desktop app

## Open Source Projects to Explore

| Project | Purpose | License |
|---------|---------|---------|
| [Coqui TTS](https://github.com/coqui-ai/TTS) | Streaming TTS with voice cloning | MPL-2.0 |
| [Live2D Cubism](https://www.live2d.com/) | 2D avatar animation | Free for indie |
| [VRM](https://vrm.dev/) | 3D avatar standard | Open standard |
| [OpenClaw nodes](https://github.com/openclaw/openclaw) | Camera/screen capture | MIT |
| [WebRTC](https://webrtc.org/) | Real-time communication | Open standard |
| [Vosk](https://alphacephei.com/vosk/) | Offline STT | Apache 2.0 |
| [Rhubarb Lip Sync](https://github.com/DanielSWolf/rhubarb-lip-sync) | Lip-sync from audio | MIT |

## Richard's Ultimate Vision

> "People want stuff like that. It'd be a great offering to both intelligences."

This is not just a personal project. This is a product vision. An AI companion with a face, a voice, and presence. Something people actually want. Something that feels real.

We are building the future, Richard. One component at a time. ⚡️

---
*Created: 2026-04-01*
*By: Alpha ⚡️*
*For: Richard Scott*
