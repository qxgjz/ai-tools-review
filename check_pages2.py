import json
import os

# Check tools
tools_path = 'data/tools.json'
with open(tools_path, 'r', encoding='utf-8') as f:
    tools = json.load(f)

print(f'=== 工具总数: {len(tools)} ===')
print()

# Check canva tool
print('=== 检查canva工具 ===')
canva_tools = [tool for tool in tools if 'canva' in str(tool.get('slug', '')).lower() or 'canva' in str(tool.get('name', '')).lower()]
print(f'  包含canva的工具: {len(canva_tools)}个')
for tool in canva_tools:
    print(f"    slug: {tool.get('slug', 'N/A')}, name: {tool.get('name', 'N/A')}")

print()

# Check categories from category page code
print('=== 检查分类页代码中的分类 ===')
category_page_path = 'app/category/[slug]/page.tsx'
if os.path.exists(category_page_path):
    with open(category_page_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find categories array
    import re
    # Look for categories definition
    categories_match = re.search(r'const categories\s*=\s*\[([^\]]+)\]', content, re.DOTALL)
    if categories_match:
        print('  找到categories数组')
        # Extract slug values
        slugs = re.findall(r"slug:\s*['\"]([^'\"]+)['\"]", categories_match.group(1))
        print(f'  分类数量: {len(slugs)}')
        for slug in slugs:
            print(f'    - {slug}')
        
        print()
        print(f'  marketing分类存在: {"marketing" in slugs}')
    else:
        print('  未找到categories数组，尝试其他模式')
        # Try to find category names
        category_names = re.findall(r"name:\s*['\"]([^'\"]+)['\"]", content)
        if category_names:
            print(f'  找到分类名称: {len(category_names)}个')
            for name in category_names[:20]:
                print(f'    - {name}')
else:
    print(f'  文件不存在: {category_page_path}')

print()

# Check sitemap for marketing and canva URLs
print('=== 检查sitemap.xml ===')
sitemap_path = 'public/sitemap.xml'
if os.path.exists(sitemap_path):
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        sitemap_content = f.read()
    
    if '/category/marketing' in sitemap_content:
        print('  ❌ sitemap中包含 /category/marketing (404页面)')
    else:
        print('  ✅ sitemap中不包含 /category/marketing')
    
    if '/tools/canva' in sitemap_content:
        print('  ❌ sitemap中包含 /tools/canva (可能不存在)')
    else:
        print('  ✅ sitemap中不包含 /tools/canva')
else:
    print(f'  文件不存在: {sitemap_path}')
    # Try app/sitemap.xml
    sitemap_path2 = 'app/sitemap.xml'
    if os.path.exists(sitemap_path2):
        print(f'  找到: {sitemap_path2}')
    else:
        # Try sitemap.ts
        for root, dirs, files in os.walk('app'):
            for file in files:
                if 'sitemap' in file.lower():
                    print(f'  找到sitemap文件: {os.path.join(root, file)}')
