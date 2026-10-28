# -*- coding: utf-8 -*-
"""r39 竞品缺口分析：futurepedia 实抓 77 分类 vs 本地 243 md vs 已开单"""
import requests, re, os, json
from collections import Counter
import urllib.parse

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
proxies = {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}
ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}

r = requests.get('https://futurepedia.io/sitemap.xml', headers=ua, proxies=proxies, timeout=30)
urls = re.findall(r'<loc>(.*?)</loc>', r.text)
cats = Counter()
for u in urls:
    p = urllib.parse.urlparse(u).path
    seg = [s for s in p.strip('/').split('/') if s]
    if seg and seg[0] == 'ai-tools' and len(seg) >= 2:
        cats[seg[1]] += 1
print('total ai-tools categories:', len(cats), '| total urls:', len(urls))

# 本地内容
local = set()
for root, dirs, files in os.walk(os.path.join(P, 'content_drafts')):
    for f in files:
        if f.endswith('.md'):
            local.add(os.path.splitext(f)[0].lower())
print('local md:', len(local))

# 已开单分类（state 全量 task 文本）
d = json.load(open(os.path.join(P, 'iteration_center', 'state.json'), encoding='utf-8'))
alltasks = [i.get('task', '') for i in d['next_iteration_focus']] + [i.get('task', '') for i in d.get('archived_todos', [])]
opened = set()
for t in alltasks:
    for x in re.findall(r'竞品[^\s（(]*', t):
        opened.add(x.replace('竞品', '').strip())
    for x in re.findall(r'\[([a-z][a-z0-9-]+)\]', t.lower()):
        pass

gaps = []
for c, n in sorted(cats.items(), key=lambda x: -x[1]):
    toks = set(re.split(r'[-_\s]+', c))
    hit_local = any(toks & set(re.split(r'[-_\s]+', os.path.splitext(lf)[0])) for lf in local)
    hit_open = any(toks & set(re.split(r'[-_\s]+', o)) for o in opened if o)
    tag = 'LOCAL' if hit_local else ('OPENED' if hit_open else 'GAP')
    if tag == 'GAP':
        gaps.append((c, n))
    print(tag, '|', c, n)

print('\n=== GAP count:', len(gaps), '===')
for c, n in gaps:
    print(c, n)
