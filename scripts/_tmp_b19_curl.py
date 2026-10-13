# -*- coding: utf-8 -*-
import subprocess
urls = [
    'https://www.aitoolcrux.com/blog/clearscope-alternatives/',
    'https://www.aitoolcrux.com/blog/gemini_38_flash_review/',
    'https://www.aitoolcrux.com/blog/dify-vs-langchain-2026/',
]
for u in urls:
    for attempt in range(3):
        out = subprocess.run(['curl.exe', '-s', '-L', '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '-o', 'NUL', '-w', '%{http_code}', u],
                             capture_output=True, text=True, encoding='utf-8')
        code = out.stdout.strip()
        if code == '200':
            print(u, '->', code)
            break
        print(u, 'attempt', attempt + 1, '->', code)
