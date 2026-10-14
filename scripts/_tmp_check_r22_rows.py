import json, io, sys, re, html as _h
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
posts = json.load(open('data/posts.json', encoding='utf-8'))
matched = [p for p in posts if (p.get('author') or '').startswith('AIToolCrux')]
print('matched posts:', len(matched))
# count article rows per page by counting rows with the divide-y list structure
for sub in ['', 'page/2', 'page/3']:
    p = 'out/authors/aitoolcrux-editorial-team/' + sub + '/index.html'
    c = open(p, encoding='utf-8').read()
    # article rows: Link with href /blog/... and title span - count hover classes
    rows = len(re.findall(r'class="flex items-center justify-between gap-4 px-4 py-3', c))
    name = sub if sub else 'page1'
    print(name, 'article rows:', rows)
