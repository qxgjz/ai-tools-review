# -*- coding: utf-8 -*-
import subprocess, time
urls = [
    ('best-ai-tools-for-beginners-2026', 'Best AI Tools for Beginners 2026'),
    ('agenta-ai-review-2026', 'Agenta AI Review 2026'),
    ('cursor-vs-windsurf-2026', 'Cursor vs Windsurf 2026'),
]
for slug, title in urls:
    u = 'https://www.aitoolcrux.com/blog/' + slug + '/'
    ok = False
    for attempt in range(2):
        try:
            r = subprocess.run(['curl.exe', '-sL', '-A', 'Mozilla/5.0', '-o', 'NUL', '-w', '%{http_code}', u],
                               capture_output=True, text=True, timeout=60)
            code = r.stdout.strip()
            if code == '200':
                # fetch body and check title
                b = subprocess.run(['curl.exe', '-sL', '-A', 'Mozilla/5.0', u], capture_output=True, text=True, timeout=60)
                body = b.stdout
                has_title = title in body
                print(slug, '| HTTP', code, '| title match:', has_title, '| len:', len(body))
                ok = True
                break
            else:
                print(slug, '| attempt', attempt+1, 'HTTP', code)
        except Exception as e:
            print(slug, '| attempt', attempt+1, 'err', str(e)[:80])
        time.sleep(5)
    if not ok:
        print(slug, '| FAILED')
