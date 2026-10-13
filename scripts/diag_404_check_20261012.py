# -*- coding: utf-8 -*-
"""检查 GSC 报 404 的 URL 在本地数据中是否存在，并核对线上 HTTP 状态"""
import json, os, sys, urllib.request

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
tools = json.load(open(base + r'\data\tools-index.json', encoding='utf-8'))
tl = tools if isinstance(tools, list) else tools.get('tools', [])

targets = ['gpt-4','gemini','midjourney','elevenlabs','notion-ai','github-copilot','cursor','sora']
print('== 本地 data/tools-index.json 检查 ==')
for slug in targets:
    hit = [t for t in tl if t.get('slug') == slug]
    if hit:
        print(slug, '=> 存在 | category =', hit[0].get('category'))
    else:
        print(slug, '=> 不存在(本地无此工具)')

print()
print('== 全部 categories ==')
cats = sorted(set(t.get('category') for t in tl))
print(cats)

# 线上 URL 状态检查
urls = [
    'https://www.aitoolcrux.com/tools/gpt-4',
    'https://www.aitoolcrux.com/category/chatbots',
    'https://www.aitoolcrux.com/category/image-generation',
    'https://www.aitoolcrux.com/category/marketing',
    'https://www.aitoolcrux.com/tools/gemini',
]
print()
print('== 线上 HTTP 状态（curl 风格）==')
for u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'})
        r = urllib.request.urlopen(req, timeout=20)
        print(u, '=>', r.getcode())
    except urllib.error.HTTPError as e:
        print(u, '=>', e.code)
    except Exception as e:
        print(u, '=> ERR', type(e).__name__)
