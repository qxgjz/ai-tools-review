import json

data = json.load(open('data/tools.json', 'r', encoding='utf-8'))

# 找出描述过短的工具
short_desc_tools = [t for t in data if len(t.get('description', '')) < 30]

print(f'描述过短的工具数: {len(short_desc_tools)}')
print('\n=== 描述过短的工具列表 ===')
for i, t in enumerate(short_desc_tools, 1):
    print(f'{i}. [{t["category"]}] {t["name"]} ({t.get("vendor", "unknown")})')
    print(f'   slug: {t["slug"]}')
    print(f'   描述: "{t.get("description", "")}"')
    print(f'   描述长度: {len(t.get("description", ""))}')
    print()
