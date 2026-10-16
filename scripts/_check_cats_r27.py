import json, io, sys
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
posts = json.load(open(r'data/posts.json', encoding='utf-8'))
cats = [p.get('categorySlug', '') for p in posts if p.get('categorySlug')]
c = Counter(cats)
print('blog categorySlug 总数:', len(cats), '唯一值:', len(c))
for slug, n in c.most_common(40):
    print(f'  {slug}: {n}篇')
# 找近义重复对
import re
norm = {}
for slug in c:
    key = re.sub(r's$', '', slug).lower()
    norm.setdefault(key, []).append(slug)
print('--- 近义分组(复数/单数):')
for key, group in norm.items():
    if len(group) > 1:
        print(' ', group)
