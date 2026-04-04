#!/usr/bin/env python3
"""Alpha TTS - Generates speech via Kokoro TTS (primary) or Edge TTS (fallback)."""
import sys
import subprocess
import os
import time
import requests

# Kokoro endpoint (via Cloudflare tunnel)
KOKORO_URL = "https://koko-tts.tacimpulse.net/v1/audio/speech"
KOKORO_MODEL = "kokoro"
KOKORO_VOICE = "af_v0nicole+af_v0bella"  # Alpha's signature voice (Nicole + Bella)

# Edge TTS fallback
EDGE_VOICE = "en-US-AriaNeural"

def generate_kokoro(text, voice=None, output_path=None):
    """Generate speech using Kokoro TTS."""
    voice = voice or KOKORO_VOICE
    
    resp = requests.post(
        KOKORO_URL,
        json={
            "model": KOKORO_MODEL,
            "voice": voice,
            "input": text
        },
        timeout=30
    )
    
    if resp.status_code == 200 and len(resp.content) > 0:
        if output_path:
            with open(output_path, 'wb') as f:
                f.write(resp.content)
            return output_path
        else:
            # Write to temp file
            workspace = os.environ.get("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace")
            out_dir = os.path.join(workspace, "tts-output")
            os.makedirs(out_dir, exist_ok=True)
            outfile = os.path.join(out_dir, f"voice-{int(time.time()*1000)}.mp3")
            with open(outfile, 'wb') as f:
                f.write(resp.content)
            return outfile
    else:
        raise Exception(f"Kokoro TTS failed: {resp.status_code} - {resp.text[:200]}")

def generate_edge(text, voice=None, output_path=None):
    """Generate speech using Edge TTS (fallback)."""
    voice = voice or EDGE_VOICE
    
    workspace = os.environ.get("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace")
    out_dir = os.path.join(workspace, "tts-output")
    os.makedirs(out_dir, exist_ok=True)
    
    outfile = output_path or os.path.join(out_dir, f"voice-{int(time.time()*1000)}.mp3")
    
    result = subprocess.run(
        ["edge-tts", "--voice", voice, "--text", text, "--write-media", outfile],
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        raise Exception(f"Edge TTS failed: {result.stderr}")
    
    return outfile

def main():
    if len(sys.argv) < 2:
        print("Usage: alpha-tts.py 'text to speak' [voice] [edge|kokoro]")
        sys.exit(1)
    
    text = sys.argv[1]
    voice = sys.argv[2] if len(sys.argv) > 2 else None
    provider = sys.argv[3] if len(sys.argv) > 3 else "kokoro"
    
    try:
        if provider == "kokoro":
            outfile = generate_kokoro(text, voice)
        else:
            outfile = generate_edge(text, voice)
        print(outfile)
    except Exception as e:
        # Fallback to Edge if Kokoro fails
        if provider == "kokoro":
            try:
                outfile = generate_edge(text, voice)
                print(outfile)
            except Exception as e2:
                print(f"Both TTS providers failed: {e2}", file=sys.stderr)
                sys.exit(1)
        else:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
