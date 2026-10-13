# -*- coding: utf-8 -*-
import subprocess, time, io, os
tmp = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\scripts\_page_cur.html'
targets = [('page', 'https://www.aitoolcrux.com/blog/cursor-vs-windsurf-2026/'),
           ('img', 'https://www.aitoolcrux.com/screenshots/real/webp/windsurf-pricing.webp')]
for kind, u in targets:
    ok = False
    for i in range(3):
        try:
            if kind == 'page':
                r = subprocess.run(['curl.exe','-sL','--max-time','150','-A','Mozilla/5.0','-o',tmp,u], capture_output=True, text=True, timeout=170)
                if os.path.exists(tmp):
                    body = io.open(tmp, encoding='utf-8', errors='ignore').read()
                    print('cursor-vs-windsurf-2026 | selfcheck:', 'Verification (batch15' in body, '| zensink:', 'zens-ink' in body, '| FAQ:', 'Frequently Asked Questions' in body, '| len:', len(body))
                    ok = True
                    break
            else:
                code = subprocess.run(['curl.exe','-sL','--max-time','90','-A','Mozilla/5.0','-o','NUL','-w','%{http_code}',u], capture_output=True, text=True, timeout=110).stdout.strip()
                print('windsurf-pricing.webp ->', code)
                ok = (code == '200')
                break
        except Exception as e:
            print(kind, '| attempt', i+1, 'ERR', str(e)[:80])
        time.sleep(10)
    if not ok and kind == 'page':
        print('cursor page FAILED after retries')
