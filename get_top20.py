import json

with open('data/tools.json', 'r', encoding='utf-8') as f:
    tools = json.load(f)

sorted_tools = sorted(tools, key=lambda x: x.get('rating', 0), reverse=True)
print('Top 20 tools:')
for i, t in enumerate(sorted_tools[:20], 1):
    print(f'{i}. {t["name"]} - {t.get("officialUrl", "N/A")}')
