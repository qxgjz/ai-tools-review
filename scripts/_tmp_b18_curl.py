# -*- coding: utf-8 -*-
import subprocess, re
base_url = 'https://www.aitoolcrux.com'
slugs = ['lovable-vs-boltnew', 'beautiful-ai-alternatives', 'sudowrite-alternatives']
for slug in slugs:
    url = base_url + '/blog/' + slug + '/'
    r = subprocess.run(['curl.exe', '-s', '-L', '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0.0.0 Safari/537.36', '-o', 'NUL', '-w', '%{http_code}', url], capture_output=True, text=True)
    code = r.stdout.strip()
    body = subprocess.run(['curl.exe', '-s', '-L', '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0.0.0 Safari/537.36', url], capture_output=True, text=True).stdout
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', body, re.S)
    webp = re.findall(r'/screenshots/real/webp/[a-z0-9-]+\.webp', body)
    print(slug, '| http:', code, '| h1:', (h1.group(1).strip()[:60] if h1 else 'NONE'), '| webp refs:', len(set(webp)))
