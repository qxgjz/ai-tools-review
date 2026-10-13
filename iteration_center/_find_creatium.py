# -*- coding: utf-8 -*-
"""查Creatium重复文章 + noindex逻辑"""
import json, os, glob

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'

# 1) 找Creatium相关文章
print('===== Creatium 相关文章 =====')
for posts_file in glob.glob(os.path.join(base, 'data', '*.json')):
    if 'post' not in os.path.basename(posts_file).lower():
        continue
    try:
        data = json.load(open(posts_file, encoding='utf-8'))
        items = data if isinstance(data, list) else data.get('posts', data.get('items', []))
        if isinstance(data, dict) and 'posts' in data:
            items = data['posts']
        if not isinstance(items, list):
            items = []
        for p in items:
            if not isinstance(p, dict):
                continue
            blob = json.dumps(p, ensure_ascii=False).lower()
            if 'creatium' in blob:
                print(' file=%s' % os.path.basename(posts_file))
                print('  slug=%s title=%s' % (p.get('slug',''), str(p.get('title',''))[:60]))
                print('  url=%s' % p.get('url', p.get('permalink','')))
                print('  date=%s' % p.get('date', p.get('publishedAt','')))
    except Exception as e:
        pass

# 2) 查noindex逻辑
print()
print('===== noindex逻辑（app目录） =====')
for f in glob.glob(os.path.join(base, 'app', '**', '*.ts'), recursive=True) + glob.glob(os.path.join(base, 'app', '**', '*.tsx'), recursive=True):
    try:
        content = open(f, encoding='utf-8').read()
        if 'noindex' in content.lower():
            # 只打印包含noindex的行
            for i, line in enumerate(content.splitlines(), 1):
                if 'noindex' in line.lower():
                    print(' %s:%d: %s' % (os.path.relpath(f, base), i, line.strip()[:100]))
    except Exception:
        pass
