import json
import os

# Check categories
categories_path = 'app/data/categories.json'
if os.path.exists(categories_path):
    with open(categories_path, 'r', encoding='utf-8') as f:
        categories = json.load(f)
    
    print('=== 所有分类 ===')
    for cat in categories:
        print(f"  slug: {cat.get('slug', 'N/A')}, name: {cat.get('name', 'N/A')}")
    
    print()
    print('=== 检查marketing分类 ===')
    marketing_exists = any(cat.get('slug') == 'marketing' for cat in categories)
    print(f'  marketing分类存在: {marketing_exists}')
else:
    print(f'文件不存在: {categories_path}')
    # Try to find categories file
    for root, dirs, files in os.walk('app'):
        for file in files:
            if 'categor' in file.lower():
                print(f'  找到分类文件: {os.path.join(root, file)}')

print()

# Check tools
tools_path = 'app/data/tools.json'
if os.path.exists(tools_path):
    with open(tools_path, 'r', encoding='utf-8') as f:
        tools = json.load(f)
    
    print(f'=== 工具总数: {len(tools)} ===')
    print()
    print('=== 检查canva工具 ===')
    canva_tools = [tool for tool in tools if 'canva' in str(tool.get('slug', '')).lower() or 'canva' in str(tool.get('name', '')).lower()]
    print(f'  包含canva的工具: {len(canva_tools)}个')
    for tool in canva_tools:
        print(f"    slug: {tool.get('slug', 'N/A')}, name: {tool.get('name', 'N/A')}")
else:
    print(f'文件不存在: {tools_path}')
    # Try to find tools file
    for root, dirs, files in os.walk('app'):
        for file in files:
            if 'tool' in file.lower() and file.endswith('.json'):
                print(f'  找到工具文件: {os.path.join(root, file)}')
