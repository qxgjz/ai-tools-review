# -*- coding: utf-8 -*-
"""找出 gpt-4/chatbots/image-generation/marketing 对应的真实 URL"""
import json, urllib.request

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
tools = json.load(open(base + r'\data\tools-index.json', encoding='utf-8'))
tl = tools if isinstance(tools, list) else tools.get('tools', [])

# 1) 含 gpt 的 slug
gpt_like = sorted(set(t.get('slug') for t in tl if 'gpt' in str(t.get('slug','')).lower() or 'chatgpt' in str(t.get('slug','')).lower()))
print('含gpt/chatgpt的slug:', gpt_like)

# 2) category=chat 的工具有多少，真实分类页
for c in ['chat','image','video','marketing']:
    n = len([t for t in tl if t.get('category') == c])
    print('category =', c, '=>', n, '个工具')

# 3) posts.json 里有没有 gpt-4 / marketing 相关文章
posts = json.load(open(base + r'\data\posts.json', encoding='utf-8'))
pl = posts if isinstance(posts, list) else posts.get('posts', [])
print('posts 总数:', len(pl))
gpt_posts = [p.get('slug') for p in pl if 'gpt' in str(p.get('slug','')).lower() or 'gpt' in str(p.get('title','')).lower()]
print('含gpt的文章slug:', gpt_posts[:15])

# 4) 线上验证真实 URL
def check(u):
    try:
        req = urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'})
        return urllib.request.urlopen(req, timeout=20).getcode()
    except Exception as e:
        code = getattr(e, 'code', None)
        return code if code else 'ERR'

candidates = [
    'https://www.aitoolcrux.com/category/chat',
    'https://www.aitoolcrux.com/category/image',
    'https://www.aitoolcrux.com/category/video',
]
for c in ['chatgpt','gpt4','gpt-4o','gpt-4']:
    candidates.append('https://www.aitoolcrux.com/tools/' + c)
print()
print('== 线上候选 URL ==')
for u in candidates:
    print(u, '=>', check(u))
