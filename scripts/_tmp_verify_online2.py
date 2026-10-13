# -*- coding: utf-8 -*-
import subprocess, os, io
tmp = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\scripts\_page.html'
urls = ['https://www.aitoolcrux.com/blog/best-ai-tools-for-beginners-2026/',
        'https://www.aitoolcrux.com/blog/agenta-ai-review-2026/',
        'https://www.aitoolcrux.com/blog/cursor-vs-windsurf-2026/']
for u in urls:
    r = subprocess.run(['curl.exe','-sL','--max-time','120','-A','Mozilla/5.0','-o',tmp,u], capture_output=True, text=True, timeout=150)
    body = io.open(tmp, encoding='utf-8', errors='ignore').read()
    slug = u.split('/blog/')[1].rstrip('/')
    print(slug, '| selfcheck:', 'Verification (batch15' in body, '| zensink:', 'zens-ink' in body, '| FAQ:', 'Frequently Asked Questions' in body, '| len:', len(body))
imgs = ['/screenshots/real/webp/agenta-home.webp','/screenshots/real/webp/agenta-pricing.webp',
        '/screenshots/real/webp/chatgpt-pricing.webp','/screenshots/real/webp/claude-pricing.webp',
        '/screenshots/real/webp/windsurf-pricing.webp','/screenshots/real/webp/cursor-pricing.webp']
for i in imgs:
    u = 'https://www.aitoolcrux.com' + i
    code = subprocess.run(['curl.exe','-sL','--max-time','60','-A','Mozilla/5.0','-o','NUL','-w','%{http_code}',u], capture_output=True, text=True, timeout=80).stdout.strip()
    print(i, '->', code)
