# -*- coding: utf-8 -*-
import subprocess, re, io, json
urls = [
    ('claude-vs-gemini-2026-comparison', 'https://www.aitoolcrux.com/blog/claude-vs-gemini-2026-comparison/', 'Claude vs Gemini 2026'),
    ('gemini-vs-chatgpt-2026', 'https://www.aitoolcrux.com/blog/gemini-vs-chatgpt-2026/', 'Gemini vs ChatGPT 2026'),
    ('elevenlabs-v2-review-2026', 'https://www.aitoolcrux.com/blog/elevenlabs-v2-review-2026/', 'ElevenLabs v2 Review 2026'),
]
for slug, u, expect in urls:
    out = subprocess.run(['curl.exe', '-s', '-L', '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', u], capture_output=True, text=True).stdout
    h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', out, re.S)
    has_expect = expect in out
    has_img = '/screenshots/real/webp/gemini-pricing.webp' in out or '/screenshots/real/webp/elevenlabs-voice-changer.webp' in out
    print(slug, '| H1:', (h1s[0][:70] if h1s else 'NONE'), '| expect-in-page:', has_expect, '| webp-img:', has_img)
