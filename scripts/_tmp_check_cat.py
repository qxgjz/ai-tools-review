import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
for slug in ['ai-tools', 'ai-writing', 'agent']:
    p = 'out/blog/category/' + slug + '/index.html'
    c = open(p, encoding='utf-8', errors='ignore').read()
    m = re.search(r'<title[^>]*>(.*?)</title>', c, re.S)
    print(slug, '|', (m.group(1).strip() if m else 'NONE'))
    md = re.search(r'<meta name="description" content="(.*?)"', c)
    print('  desc len:', (len(md.group(1)) if md else 'NONE'))
