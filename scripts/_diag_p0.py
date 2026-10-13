import json, re
posts = json.load(open('data/posts.json', encoding='utf-8'))
upd = [p for p in posts if p.get('updatedAt') or p.get('lastUpdated')]
p = upd[0]
print('验证文章:', p['slug'], '| updatedAt:', p.get('updatedAt') or p.get('lastUpdated'))
html = open('out/blog/%s/index.html' % p['slug'], encoding='utf-8').read()
m = re.search(r'Last updated:</strong>\s*([^<]+)', html)
print('页面 Last updated 渲染:', m.group(1).strip() if m else '未找到')

print('--- robots.txt AI bots ---')
txt = open('out/robots.txt', encoding='utf-8').read()
for ua in ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'PerplexityBot', 'ClaudeBot', 'Google-Extended', 'Bingbot']:
    print(ua, ':', '在' if ua in txt else '缺失')
