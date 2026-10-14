import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
p = r'out/authors/aitoolcrux-editorial-team/index.html'
c = open(p, encoding='utf-8').read()
rsc = re.findall(r'self\.__next_f\.push\(\[1,"(.+?)"\]\)', c)
rsc_size = sum(len(x) for x in rsc)
print('total HTML KB:', round(len(c)/1024, 1))
print('RSC payload KB:', round(rsc_size/1024, 1))
print('non-RSC KB:', round((len(c)-rsc_size)/1024, 1))
links = re.findall(r'href="/blog/', c)
print('blog links:', len(links))
# sitemap title
sp = r'out/sitemap/index.html'
sc = open(sp, encoding='utf-8').read()
m = re.search(r'<title>(.*?)</title>', sc, re.S)
if m:
    import html as _h
    t = _h.unescape(m.group(1)).strip()
    print('sitemap title:', repr(t), 'len:', len(t))
