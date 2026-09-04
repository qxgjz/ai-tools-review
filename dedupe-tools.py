import json

data = json.load(open('data/tools.json', 'r', encoding='utf-8'))
print(f'原始工具数: {len(data)}')

# 检查重复（按slug）
slugs = {}
duplicates = []
for t in data:
    slug = t['slug']
    if slug in slugs:
        duplicates.append(slug)
    else:
        slugs[slug] = t

print(f'重复slug数: {len(duplicates)}')
if duplicates:
    print(f'重复的slug: {duplicates[:10]}')

# 检查重复（按name+vendor）
names = {}
name_duplicates = []
for t in data:
    key = f'{t["name"].lower()}_{t.get("vendor","").lower()}'
    if key in names:
        name_duplicates.append(t['name'])
    else:
        names[key] = t

print(f'重复name+vendor数: {len(name_duplicates)}')
if name_duplicates:
    print(f'重复的name: {name_duplicates[:10]}')

# 去重（保留第一个）
seen_slugs = set()
unique_data = []
for t in data:
    if t['slug'] not in seen_slugs:
        seen_slugs.add(t['slug'])
        unique_data.append(t)

print(f'\n去重后工具数: {len(unique_data)}')
print(f'删除了 {len(data) - len(unique_data)} 个重复工具')

# 保存去重后的数据
json.dump(unique_data, open('data/tools.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('已保存去重后的数据')

# 重新统计分类
from collections import Counter
cats = Counter(t.get('category', 'unknown') for t in unique_data)
print('\n=== 去重后各分类工具数量 ===')
for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
    print(f'  {cat}: {count}')
