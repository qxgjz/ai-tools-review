# -*- coding: utf-8 -*-
import subprocess
urls = ['https://www.aitoolcrux.com/blog/best-ai-tools-for-beginners-2026/',
        'https://www.aitoolcrux.com/blog/agenta-ai-review-2026/',
        'https://www.aitoolcrux.com/blog/cursor-vs-windsurf-2026/']
for u in urls:
    b = subprocess.run(['curl.exe','-sL','-A','Mozilla/5.0',u], capture_output=True, text=True, timeout=60).stdout
    print(u.split('/blog/')[1].rstrip('/'), '| selfcheck block visible:', 'Verification (batch15' in b, '| zensink mention:', 'zens-ink' in b, '| FAQ:', 'Frequently Asked Questions' in b)
imgs = ['/screenshots/real/webp/agenta-home.webp','/screenshots/real/webp/agenta-pricing.webp',
        '/screenshots/real/webp/chatgpt-pricing.webp','/screenshots/real/webp/claude-pricing.webp',
        '/screenshots/real/webp/windsurf-pricing.webp','/screenshots/real/webp/cursor-pricing.webp']
for i in imgs:
    u = 'https://www.aitoolcrux.com' + i
    code = subprocess.run(['curl.exe','-sL','-A','Mozilla/5.0','-o','NUL','-w','%{http_code}',u], capture_output=True, text=True, timeout=60).stdout.strip()
    print(i, '->', code)
