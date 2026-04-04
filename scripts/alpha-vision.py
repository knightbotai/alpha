#!/usr/bin/env python3
"""Alpha Vision - Analyze images using Richard's local vLLM server via Cloudflare tunnel."""
import sys
import requests
import base64
import json

VLLM_URL = "https://vllm.tacimpulse.net/v1/chat/completions"
MODEL = "huihui-qwen35-27b-abliterated-nvfp4"

def analyze(image_path, prompt="Describe this image in detail. Be specific and accurate."):
    with open(image_path, 'rb') as f:
        img_b64 = base64.b64encode(f.read()).decode()
    
    # Detect image type
    ext = image_path.lower().split('.')[-1]
    mime = {
        'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
        'png': 'image/png', 'gif': 'image/gif', 'webp': 'image/webp'
    }.get(ext, 'image/jpeg')
    
    resp = requests.post(
        VLLM_URL,
        json={
            'model': MODEL,
            'messages': [
                {
                    'role': 'user',
                    'content': [
                        {'type': 'text', 'text': prompt},
                        {'type': 'image_url', 'image_url': {'url': f'data:{mime};base64,{img_b64}'}}
                    ]
                }
            ],
            'max_tokens': 1000
        },
        timeout=120
    )
    
    result = resp.json()
    if 'choices' in result and len(result['choices']) > 0:
        return result['choices'][0]['message']['content']
    else:
        return f"Error: {json.dumps(result, indent=2)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: alpha-vision.py <image_path> [prompt]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else "Describe this image in detail. Be specific and accurate."
    
    print(analyze(image_path, prompt))
