import io, os, sys, re, html
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

html_files = []
for root, dirs, files in os.walk('out'):
    for f in files:
        if f == 'index.html':
            html_files.append(os.path.join(root, f))
print('HTML总数:', len(html_files))

issues = {'title_short': [], 'title_long': [], 'no_meta': [], 'meta_short': [], 'meta_long': [], 'h1_not1': [], 'no_schema': [], 'no_alt_imgs': [], 'big_pages': []}
for hf in html_files:
    c = open(hf, encoding='utf-8', errors='ignore').read()
    url = hf.replace(os.sep, '/').replace('out', 'https://www.aitoolcrux.com', 1).replace('/index.html', '/')
    m = re.search(r'<title[^>]*>(.*?)</title>', c, re.S)
    tl = len(html.unescape(m.group(1).strip())) if m else 0
    if not m:
        issues['title_short'].append(url)
    elif tl < 30:
        issues['title_short'].append((url, tl))
    elif tl > 60:
        issues['title_long'].append((url, tl))
    md = re.search(r'<meta name="description" content="(.*?)"', c)
    if not md:
        issues['no_meta'].append(url)
    elif len(html.unescape(md.group(1))) < 50:
        issues['meta_short'].append((url, len(html.unescape(md.group(1)))))
    elif len(html.unescape(md.group(1))) > 160:
        issues['meta_long'].append((url, len(html.unescape(md.group(1)))))
    h1 = len(re.findall(r'<h1[ >]', c))
    if h1 != 1:
        issues['h1_not1'].append((url, h1))
    if 'application/ld+json' not in c:
        issues['no_schema'].append(url)
    imgs = re.findall(r'<img[^>]*>', c)
    noalt = [i for i in imgs if 'alt=' not in i]
    if noalt:
        issues['no_alt_imgs'].append((url, len(noalt)))
    kb = len(c) / 1024
    if kb > 600:
        issues['big_pages'].append((url, round(kb, 1)))

print('== 问题统计 ==')
for k, v in issues.items():
    print(k, len(v))
for k in ['title_short', 'title_long', 'no_meta', 'meta_short', 'meta_long', 'h1_not1', 'no_schema', 'no_alt_imgs', 'big_pages']:
    for item in issues[k][:8]:
        print(' ', k, item)
