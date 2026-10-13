# -*- coding: utf-8 -*-
# 检查GA4异常流量/not set P0是否录入 + zens-ink可用性 + 3篇文章文件存在性
import json, os

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
sp = os.path.join(base, 'iteration_center', 'state.json')
with open(sp, encoding='utf-8') as f:
    data = json.load(f)
focus = data.get('next_iteration_focus', [])
tasks_text = [str(t.get('task', '')) for t in focus]

print('=== 1. GA4异常流量P0是否录入 ===')
hit = [t for t in focus if '893' in str(t.get('task')) or '异常流量' in str(t.get('task')) or '20261003' in str(t.get('task'))]
print('命中:', len(hit))
for t in hit:
    print('[{}|{}] {}'.format(t.get('status'), t.get('priority'), str(t.get('task'))[:120]))

print()
print('=== 2. GA4 (not set)落地页P0是否录入 ===')
hit2 = [t for t in focus if '(not set)' in str(t.get('task'))]
print('命中:', len(hit2))
for t in hit2:
    print('[{}|{}] {}'.format(t.get('status'), t.get('priority'), str(t.get('task'))[:120]))

print()
print('=== 3. 性能故障(36小时持续)是否录入 ===')
hit3 = [t for t in focus if '故障' in str(t.get('task')) and ('首页' in str(t.get('task')) or 'TTFB' in str(t.get('task')) or '超时' in str(t.get('task')) or '不可达' in str(t.get('task')))]
print('命中:', len(hit3))
for t in hit3:
    print('[{}|{}|{}] {}'.format(t.get('status'), t.get('priority'), t.get('assigned_to'), str(t.get('task'))[:120]))

print()
print('=== 4. 3篇整改文章文件存在性 ===')
posts = os.path.join(base, 'data', 'posts.json')
if os.path.exists(posts):
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
        if found:
            content = found.get('content', '') or ''
            print('{}: 存在, content长度={}'.format(s, len(content)))
        else:
            print('{}: ❌ 未找到'.format(s))
else:
    print('posts.json 不存在:', posts)

print()
print('=== 5. zens-ink 可用性 ===')
import importlib
for mod in ['zens_ink', 'scripts.zensink_toolkit']:
    try:
        importlib.import_module(mod)
        print('{}: ✅ 可导入'.format(mod))
    except Exception as e:
        print('{}: ❌ {}'.format(mod, str(e)[:100]))
