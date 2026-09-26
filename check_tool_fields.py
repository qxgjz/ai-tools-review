import json

# 读取工具数据
with open('data/tools.json', 'r', encoding='utf-8') as f:
    tools = json.load(f)

print(f"总工具数: {len(tools)}")
print("\n" + "=" * 80)
print("TOP 20 工具字段完整性检查")
print("=" * 80)

# 按评分排序取Top20
def get_rating(tool):
    rating = tool.get('rating', 0)
    if isinstance(rating, dict):
        return rating.get('total', 0)
    return rating if isinstance(rating, (int, float)) else 0

sorted_tools = sorted(tools, key=get_rating, reverse=True)[:20]

# 检查字段
fields_to_check = ['name', 'slug', 'description', 'category', 'tags', 'features', 'pros', 'cons', 'pricing', 'useCases', 'faq', 'officialUrl', 'screenshots']

field_stats = {field: 0 for field in fields_to_check}

for i, tool in enumerate(sorted_tools, 1):
    rating = tool.get('rating', 'N/A')
    if isinstance(rating, dict):
        rating = rating.get('total', 'N/A')
    print(f"\n{i}. {tool.get('name', 'Unknown')} (评分: {rating})")
    print(f"   slug: {tool.get('slug', 'N/A')}")
    print(f"   category: {tool.get('category', 'N/A')}")
    
    missing_fields = []
    for field in fields_to_check:
        value = tool.get(field)
        if value and (not isinstance(value, list) or len(value) > 0):
            field_stats[field] += 1
            if isinstance(value, list):
                print(f"   ✅ {field}: {len(value)} 项")
            elif isinstance(value, str) and len(value) > 100:
                print(f"   ✅ {field}: {len(value)} 字符")
            else:
                print(f"   ✅ {field}: 有")
        else:
            missing_fields.append(field)
            print(f"   ❌ {field}: 缺失")
    
    if missing_fields:
        print(f"   ⚠️  缺失字段: {', '.join(missing_fields)}")

print("\n" + "=" * 80)
print("字段统计 (Top 20)")
print("=" * 80)
for field, count in field_stats.items():
    percentage = (count / 20) * 100
    status = "✅" if percentage >= 80 else "⚠️" if percentage >= 50 else "❌"
    print(f"{status} {field}: {count}/20 ({percentage:.0f}%)")

# 检查所有工具的字段统计
print("\n" + "=" * 80)
print("全部工具字段统计")
print("=" * 80)
all_field_stats = {field: 0 for field in fields_to_check}
for tool in tools:
    for field in fields_to_check:
        value = tool.get(field)
        if value and (not isinstance(value, list) or len(value) > 0):
            all_field_stats[field] += 1

for field, count in all_field_stats.items():
    percentage = (count / len(tools)) * 100
    status = "✅" if percentage >= 80 else "⚠️" if percentage >= 50 else "❌"
    print(f"{status} {field}: {count}/{len(tools)} ({percentage:.0f}%)")
