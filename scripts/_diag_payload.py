import re, json, os

for slug in ['microsoft-365-copilot-review-2026', 'ai-coding-tools-comparison-2026']:
    p = f'out/blog/{slug}/index.html'
    size = os.path.getsize(p)
    html = open(p, encoding='utf-8').read()
    pushes = re.findall(r'self\.__next_f\.push\(\[1,\s*"(.*?)"\]\)', html, re.S)
    pl = sum(len(x) for x in pushes)
    print(f'{slug}: HTML={round(size/1024,1)}KB payload={round(pl/1024,1)}KB')

html = open('out/blog/microsoft-365-copilot-review-2026/index.html', encoding='utf-8').read()
print('total HTML:', len(html), 'KB:', round(len(html)/1024, 1))

pushes = re.findall(r'self\.__next_f\.push\(\[1,\s*"(.*?)"\]\)', html, re.S)
payload_len = sum(len(p) for p in pushes)
print('RSC payload chars:', payload_len, 'KB:', round(payload_len/1024, 1))

h2s = re.findall(r'<h2[^>]*id="([^"]+)"[^>]*>', html)
h3s = re.findall(r'<h3[^>]*id="([^"]+)"[^>]*>', html)
print('h2 with id:', len(h2s), '| h3 with id:', len(h3s))
print('sample h2 ids:', h2s[:3])
print('TOC rendered:', 'On this page' in html)

posts = json.load(open('data/posts.json', encoding='utf-8'))
titles_in = [p['slug'] for p in posts if p['slug'] in html]
print('posts slug 出现条数:', len(titles_in), '/', len(posts))

content_markers = [p['slug'] for p in posts if len(p.get('content', '')) > 50000 and p['content'][:80] in html]
print('全content注入条数:', len(content_markers))

tools = json.load(open('data/tools.json', encoding='utf-8'))
t_slugs = [t['slug'] for t in tools if t.get('slug') in html]
print('tools slug 出现条数:', len(t_slugs), '/', len(tools))

# 看 payload 前 300 字符判断内容形态
print('--- payload 采样 ---')
print(pushes[0][:300] if pushes else 'no payload')
