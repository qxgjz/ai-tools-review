import json

with open('data/posts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f'文章总数: {len(data)}')
print(f'\n第一篇文章字段:')
for key in data[0].keys():
    value = data[0][key]
    if isinstance(value, str):
        print(f'  {key}: {value[:80]}...' if len(value) > 80 else f'  {key}: {value}')
    elif isinstance(value, list):
        print(f'  {key}: [list, {len(value)} items]')
    elif isinstance(value, dict):
        print(f'  {key}: [dict, {len(value)} keys]')
    else:
        print(f'  {key}: {value}')

print(f'\n最近5篇文章:')
for post in data[:5]:
    print(f'  - {post.get("title", "无标题")[:70]}')
    print(f'    slug: {post.get("slug", "无")}')
    print(f'    日期: {post.get("publishedAt", post.get("date", "无"))}')
    print(f'    分类: {post.get("category", "无")}')
