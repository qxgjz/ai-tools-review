# -*- coding: utf-8 -*-
import subprocess, re
urls = [
    ('cursor_ai_review', 'https://www.aitoolcrux.com/blog/cursor_ai_review/', ['cursor-pricing.webp', 'cursor-code-editor.webp']),
    ('midjourney-v7-review-2026', 'https://www.aitoolcrux.com/blog/midjourney-v7-review-2026/', ['midjourney-plans.webp', 'midjourney-home.webp']),
    ('suno-alternatives', 'https://www.aitoolcrux.com/blog/suno-alternatives/', ['suno-pricing.webp', 'suno-music-creator.webp']),
]
for slug, u, imgs in urls:
    out = subprocess.run(['curl.exe', '-s', '-L', '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '-w', '\nHTTP:%{http_code}', u], capture_output=True, text=True).stdout
    code = out.strip().split('\n')[-1]
    h1 = re.findall(r'<h1[^>]*>(.*?)</h1>', out, re.S)
    img_ok = all(i in out for i in imgs)
    print(slug, '|', code, '| H1:', (h1[0][:60] if h1 else 'NONE'), '| imgs:', img_ok)
