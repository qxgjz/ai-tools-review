# -*- coding: utf-8 -*-
# 用zens-ink复查3篇整改文章
import os, sys, json

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
os.chdir(base)
sys.path.insert(0, base)

from zens_ink import content_qc

posts = os.path.join(base, 'data', 'posts.json')
with open(posts, encoding='utf-8') as f:
    pdata = json.load(f)
if isinstance(pdata, dict):
    items = pdata.get('posts', pdata)
else:
    items = pdata

slugs = ['claude-opus-4-vs-gpt-5-2026', 'perplexity-vs-chatgpt-2026', 'midjourney-v7-vs-dall-e-3-2026']
for s in slugs:
    found = None
    if isinstance(items, list):
        found = next((x for x in items if s in str(x.get('slug', ''))), None)
    else:
        found = items.get(s)
    if not found:
        print('{}: 未找到'.format(s))
        continue
    content = found.get('content', '') or ''
    title = found.get('title', '') or ''
    try:
        result = content_qc.check_draft(title=title, content=content)
        # 兼容不同返回结构
        if isinstance(result, dict):
            score = result.get('score') or result.get('total_score') or result.get('quality_score') or 'N/A'
            print('{}: score={}'.format(s, score))
            for k in ['missing', 'issues', 'warnings']:
                if k in result:
                    print('  {}: {}'.format(k, str(result[k])[:200]))
        else:
            print('{}: 返回={}'.format(s, str(result)[:200]))
    except Exception as e:
        print('{}: ❌ 评分失败: {}'.format(s, str(e)[:150]))
