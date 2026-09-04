import json
from collections import defaultdict

data = json.load(open('data/tools.json', 'r', encoding='utf-8'))

# 按name+vendor分组
groups = defaultdict(list)
for t in data:
    key = f'{t["name"].lower()}_{t.get("vendor","").lower()}'
    groups[key].append(t)

# 找出重复的
duplicates = {k: v for k, v in groups.items() if len(v) > 1}

print(f'重复的name+vendor组数: {len(duplicates)}')
print()

for key, tools in duplicates.items():
    print(f'=== {key} ===')
    for t in tools:
        print(f'  slug: {t["slug"]}')
        print(f'  name: {t["name"]}')
        print(f'  vendor: {t.get("vendor", "")}')
        print(f'  category: {t["category"]}')
        print(f'  description: {t.get("description", "")[:80]}')
        print(f'  scores: {t["scores"]}')
        print()
