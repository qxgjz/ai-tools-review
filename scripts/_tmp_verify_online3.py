# -*- coding: utf-8 -*-
import urllib.request, io, time
urls = ['https://www.aitoolcrux.com/blog/best-ai-tools-for-beginners-2026/',
        'https://www.aitoolcrux.com/blog/agenta-ai-review-2026/',
        'https://www.aitoolcrux.com/blog/cursor-vs-windsurf-2026/']
opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler())
opener.addheaders = [('User-Agent','Mozilla/5.0'), ('Accept','text/html')]
for u in urls:
    try:
        with opener.open(u, timeout=90) as r:
            body = r.read().decode('utf-8', errors='ignore')
            code = r.getcode()
        slug = u.split('/blog/')[1].rstrip('/')
        print(slug, '| HTTP', code, '| selfcheck:', 'Verification (batch15' in body, '| zensink:', 'zens-ink' in body, '| FAQ:', 'Frequently Asked Questions' in body, '| len:', len(body))
    except Exception as e:
        print(u, 'ERR', str(e)[:100])
    time.sleep(2)
imgs = ['/screenshots/real/webp/agenta-home.webp','/screenshots/real/webp/agenta-pricing.webp',
        '/screenshots/real/webp/chatgpt-pricing.webp','/screenshots/real/webp/claude-pricing.webp',
        '/screenshots/real/webp/windsurf-pricing.webp','/screenshots/real/webp/cursor-pricing.webp']
for i in imgs:
    try:
        with opener.open('https://www.aitoolcrux.com' + i, timeout=60) as r:
            code = r.getcode()
        print(i, '->', code)
    except Exception as e:
        print(i, '-> ERR', str(e)[:80])
