# -*- coding: utf-8 -*-
import urllib.request, time
opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler())
opener.addheaders = [('User-Agent','Mozilla/5.0'), ('Accept','text/html')]
targets = ['https://www.aitoolcrux.com/blog/cursor-vs-windsurf-2026/',
           'https://www.aitoolcrux.com/screenshots/real/webp/windsurf-pricing.webp']
for u in targets:
    ok = False
    for i in range(3):
        try:
            with opener.open(u, timeout=120) as r:
                body = r.read().decode('utf-8', errors='ignore')
                code = r.getcode()
            if '/blog/' in u:
                print(u.split('/blog/')[1].rstrip('/'), '| HTTP', code, '| selfcheck:', 'Verification (batch15' in body, '| zensink:', 'zens-ink' in body, '| FAQ:', 'Frequently Asked Questions' in body, '| len:', len(body))
            else:
                print('windsurf-pricing.webp ->', code)
            ok = True
            break
        except Exception as e:
            print(u.split('/blog/')[-1].split('/screenshots/')[-1], '| attempt', i+1, 'ERR', str(e)[:60])
            time.sleep(8)
    if not ok:
        print(u, '| FAILED after retries')
