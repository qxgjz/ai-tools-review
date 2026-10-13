# -*- coding: utf-8 -*-
# 用zens-ink content_qc.check_draft(path) 复查3篇整改文章
import os, sys, json

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
os.chdir(base)
sys.path.insert(0, base)

from zens_ink import content_qc
from pathlib import Path

# 文章文件在 content_drafts/ 或 blog 目录下，先找
posts = os.path.join(base, 'data', 'posts.json')
with open(posts, encoding='utf-8') as f:
    pdata = json.load(f)
if isinstance(pdata, dict):
    items = pdata.get('posts', pdata)
else:
    items = pdata

slugs = ['claude-opus-4-vs-gpt-5-2026', 'perplexity-vs-chatgpt-2026', 'midjourney-v7-vs-dall-e-3-2026']

# 查找文章文件路径
def find_slug_file(slug):
    candidates = []
    for root_dir in ['content_drafts', 'public', 'data', 'blog', 'src']:
        d = os.path.join(base, root_dir)
        if not os.path.isdir(d):
            continue
        for dp, dn, fn in os.walk(d):
            for f in fn:
                if slug in f and f.endswith(('.md', '.json', '.txt')):
                    candidates.append(os.path.join(dp, f))
    return candidates

for s in slugs:
    files = find_slug_file(s)
    print('=== {} ==='.format(s))
    for fp in files[:3]:
        print('  文件: {} ({}字节)'.format(fp, os.path.getsize(fp)))
        try:
            result = content_qc.check_draft(Path(fp))
            if isinstance(result, dict):
                score = result.get('score') or result.get('total_score') or result.get('quality_score')
                print('  score={}'.format(score))
            else:
                print('  返回: {}'.format(str(result)[:200]))
        except Exception as e:
            print('  ❌ {}'.format(str(e)[:150]))
    if not files:
        # 从posts.json内容生成临时md文件再评分
        found = None
        if isinstance(items, list):
            found = next((x for x in items if s in str(x.get('slug', ''))), None)
        else:
            found = items.get(s)
        if found:
            tmp = os.path.join(base, 'scripts', 'tmp_{}.md'.format(s))
            with open(tmp, 'w', encoding='utf-8') as f:
                f.write('# {}\n\n{}'.format(found.get('title', s), found.get('content', '')))
            print('  临时md生成: {}'.format(tmp))
            try:
                result = content_qc.check_draft(Path(tmp))
                if isinstance(result, dict):
                    score = result.get('score') or result.get('total_score') or result.get('quality_score')
                    print('  score={}'.format(score))
                else:
                    print('  返回: {}'.format(str(result)[:200]))
            except Exception as e:
                print('  ❌ {}'.format(str(e)[:150]))
