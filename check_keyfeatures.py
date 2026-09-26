import json

with open('data/tools.json', 'r', encoding='utf-8') as f:
    tools = json.load(f)

# 检查keyFeatures字段
has_keyfeatures = sum(1 for t in tools if t.get('keyFeatures') and len(t.get('keyFeatures', [])) > 0)
print(f'keyFeatures字段: {has_keyfeatures}/{len(tools)} ({has_keyfeatures/len(tools)*100:.0f}%)')

# 检查Top20的keyFeatures
def get_rating(tool):
    rating = tool.get('rating', 0)
    if isinstance(rating, dict):
        return rating.get('total', 0)
    return rating if isinstance(rating, (int, float)) else 0

sorted_tools = sorted(tools, key=get_rating, reverse=True)[:20]
print('\nTop20工具keyFeatures:')
for i, tool in enumerate(sorted_tools, 1):
    kf = tool.get('keyFeatures', [])
    name = tool.get('name', 'Unknown')
    if kf and len(kf) > 0:
        print(f'  {i}. {name}: OK {len(kf)} items')
    else:
        print(f'  {i}. {name}: MISSING')
