import os, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = r'out/authors/aitoolcrux-editorial-team'
for sub in ['', 'page/2', 'page/3']:
    p = os.path.join(base, sub, 'index.html')
    if os.path.exists(p):
        c = open(p, encoding='utf-8').read()
        links = re.findall(r'href="/blog/', c)
        sz = round(os.path.getsize(p) / 1024, 1)
        name = sub if sub else 'page1'
        print(name, 'KB:', sz, 'links:', len(links))
    else:
        name = sub if sub else 'page1'
        print(name, 'MISSING')
