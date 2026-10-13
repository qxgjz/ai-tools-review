import io, sys, os, re, json, html as H
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

posts = json.load(open('data/posts.json', encoding='utf-8'))
bad_h1 = []
checked = 0
for p in posts:
    slug = p.get('slug', '')
    f = os.path.join('out', 'blog', slug, 'index.html')
    if not os.path.exists(f):
        continue
    checked += 1
    c = open(f, encoding='utf-8', errors='ignore').read()
    n = len(re.findall(r'<h1\b', c))
    if n != 1:
        bad_h1.append((slug, n))
print('博客页检查:', checked, '| 非单H1:', len(bad_h1))
for b in bad_h1[:20]:
    print('  ', b)

bad_cat = []
catdir = os.path.join('out', 'blog', 'category')
total_cat = 0
if os.path.isdir(catdir):
    for d in os.listdir(catdir):
        f = os.path.join(catdir, d, 'index.html')
        if not os.path.exists(f):
            continue
        total_cat += 1
        c = open(f, encoding='utf-8', errors='ignore').read()
        t = re.search(r'<title>([\s\S]*?)</title>', c)
        m = re.search(r'name="description" content="([\s\S]*?)"', c)
        tl = len(H.unescape(t.group(1))) if t else 0
        ml = len(H.unescape(m.group(1))) if m else 0
        if tl > 60 or ml > 155:
            bad_cat.append((d, tl, ml))
print('category页:', total_cat, '| 超长:', len(bad_cat))
for b in bad_cat:
    print('  ', b)
