import json, io, sys, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# 备份
shutil.copy(r'data/posts.json', r'data/posts.json.bak_r27')
posts = json.load(open(r'data/posts.json', encoding='utf-8'))
# 规范映射：单数 -> 复数（仅明确的近义合并）
mapping = {'comparison': 'comparisons', 'guide': 'guides'}
changed = []
for p in posts:
    old = p.get('categorySlug')
    if old in mapping:
        new = mapping[old]
        p['categorySlug'] = new
        p['category'] = p.get('category', '')  # 保留category字段不动
        changed.append((p.get('slug', ''), old, new))
json.dump(posts, open(r'data/posts.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('规范化完成，改动篇数:', len(changed))
for s, o, n in changed[:15]:
    print(' ', s, ':', o, '->', n)
