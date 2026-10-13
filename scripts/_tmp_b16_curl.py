# -*- coding: utf-8 -*-
import subprocess
urls = [
    ('claude-vs-gemini-2026-comparison', 'https://www.aitoolcrux.com/blog/claude-vs-gemini-2026-comparison/'),
    ('gemini-vs-chatgpt-2026', 'https://www.aitoolcrux.com/blog/gemini-vs-chatgpt-2026/'),
    ('elevenlabs-v2-review-2026', 'https://www.aitoolcrux.com/blog/elevenlabs-v2-review-2026/'),
]
for slug, u in urls:
    for attempt in range(3):
        r = subprocess.run(['curl.exe', '-s', '-L', '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '-o', 'NUL', '-w', '%{http_code}', u], capture_output=True, text=True)
        code = r.stdout.strip()
        if code == '200':
            print(slug, 'HTTP', code, 'OK')
            break
        print(slug, 'attempt', attempt, 'HTTP', code)
