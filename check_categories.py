import json
from collections import Counter

# Check tools
with open('data/tools.json', 'r', encoding='utf-8') as f:
    tools = json.load(f)

print(f'=== 工具总数: {len(tools)} ===')
print()

# Check all categories
categories = [tool.get('category', 'N/A') for tool in tools]
category_counts = Counter(categories)

print('=== 所有分类及工具数量 ===')
for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
    print(f'  {cat}: {count}个工具')

print()
print('=== 检查marketing分类 ===')
marketing_tools = [tool for tool in tools if tool.get('category') == 'marketing']
print(f'  marketing分类工具数: {len(marketing_tools)}')
if marketing_tools:
    print('  工具列表:')
    for tool in marketing_tools[:5]:
        print(f"    - {tool.get('name')} (slug: {tool.get('slug')})")

print()
print('=== 检查canva工具 ===')
canva_tools = [tool for tool in tools if 'canva' in str(tool.get('slug', '')).lower()]
print(f'  canva相关工具数: {len(canva_tools)}')
for tool in canva_tools:
    print(f"    - {tool.get('name')} (slug: {tool.get('slug')}, category: {tool.get('category')})")

print()
print('=== 检查分类页支持的分类 ===')
# Read category page to find supported categories
with open('app/category/[slug]/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Find category data
import re
# Look for category definitions
if 'categoryData' in content:
    print('  找到categoryData')
elif 'categories' in content:
    print('  找到categories')
    # Extract category slugs
    slugs = re.findall(r"slug:\s*['\"]([^'\"]+)['\"]", content)
    if slugs:
        print(f'  支持的分类slug: {len(slugs)}个')
        for slug in slugs:
            print(f'    - {slug}')

print()
print('=== 检查是否有404处理 ===')
if 'notFound' in content:
    print('  找到notFound处理')
elif '404' in content:
    print('  找到404处理')
else:
    print('  未找到明确的404处理')
