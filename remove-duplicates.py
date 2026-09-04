import json

data = json.load(open('data/tools.json', 'r', encoding='utf-8'))
print(f'原始工具数: {len(data)}')

# 需要删除的重复工具slug（旧名称）
slugs_to_remove = [
    'opendevin',      # OpenHands旧名
    'gpt-index',       # llama_index旧名
    'embedchain',      # mem0旧名
    'memgpt',          # letta旧名
    'privategpt',      # private-gpt重复（保留带连字符的）
    'agent-llm',       # AGiXT旧名
    'quiver',          # quivr旧名
]

# 删除重复工具
removed = []
unique_data = []
for t in data:
    if t['slug'] in slugs_to_remove:
        removed.append(t)
    else:
        unique_data.append(t)

print(f'\n已删除重复工具: {len(removed)}')
for t in removed:
    print(f'  - {t["name"]} (slug: {t["slug"]})')

# 保存去重后的数据
json.dump(unique_data, open('data/tools.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print(f'\n═══════════════════════════════════════')
print(f'✅ 重复工具清理完成')
print(f'═══════════════════════════════════════')
print(f'删除工具数: {len(removed)}')
print(f'剩余工具数: {len(unique_data)}')

# 重新统计分类
from collections import Counter
cats = Counter(t.get('category', 'unknown') for t in unique_data)
print(f'\n=== 清理后各分类工具数量 ===')
for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
    print(f'  {cat}: {count}')

# 验证没有重复
slugs = [t['slug'] for t in unique_data]
duplicate_slugs = [s for s in set(slugs) if slugs.count(s) > 1]
print(f'\n重复slug数: {len(duplicate_slugs)}')
if duplicate_slugs:
    print(f'重复的slug: {duplicate_slugs}')
else:
    print('✅ 没有重复slug')
