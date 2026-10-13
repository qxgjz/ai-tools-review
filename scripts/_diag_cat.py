import re, os, json

p = 'out/category/agent/index.html'
size = os.path.getsize(p)
html = open(p, encoding='utf-8').read()
print('category/agent HTML:', round(size/1024, 1), 'KB')
pushes = re.findall(r'self\.__next_f\.push\(\[1,\s*"(.*?)"\]\)', html, re.S)
print('RSC payload:', round(sum(len(x) for x in pushes)/1024, 1), 'KB')

posts = json.load(open('data/posts.json', encoding='utf-8'))
tools = json.load(open('data/tools.json', encoding='utf-8'))
print('posts slug 出现:', len([p2 for p2 in posts if p2['slug'] in html]), '/', len(posts))
print('tools slug 出现:', len([t for t in tools if t.get('slug') in html]), '/', len(tools))

# 大文本是否进 payload：搜正文长文片段
long_marker = 'Quick Answer' if 'Quick Answer' in html else None
print('有 Quick Answer:', 'Quick Answer' in html)
