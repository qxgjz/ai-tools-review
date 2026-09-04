import json

with open('data/tools.json', 'r', encoding='utf-8') as f:
    tools = json.load(f)

# 统计各分类工具数量
categories = {}
for tool in tools:
    cat = tool.get('category', 'unknown')
    categories[cat] = categories.get(cat, 0) + 1

print('当前分类统计:')
for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
    print(f'  {cat}: {count}')

# 列出agent分类中的前30个工具
agent_tools = [t for t in tools if t.get('category') == 'agent']
print(f'\nagent分类共 {len(agent_tools)} 个工具')
print('前30个agent工具:')
for i, tool in enumerate(agent_tools[:30]):
    name = tool.get('name', 'unknown')
    desc = tool.get('description', '')[:60]
    print(f'  {i+1}. {name} - {desc}')
