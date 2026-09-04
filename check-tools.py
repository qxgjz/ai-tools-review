import json
from collections import Counter

data = json.load(open('data/tools.json', 'r', encoding='utf-8'))
cats = Counter(t.get('category', 'unknown') for t in data)

print('=== 各分类工具数量 ===')
for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
    print(f'  {cat}: {count}')
print(f'\n总计: {len(data)} 个工具')

# 检查agent分类的工具质量
agent_tools = [t for t in data if t.get('category') == 'agent']
print(f'\n=== agent分类工具样本（前15个）===')
for t in agent_tools[:15]:
    avg_score = sum(t['scores'].values()) / len(t['scores'])
    print(f'  - {t["name"]} ({t.get("vendor", "unknown")}) | 评分: {avg_score:.1f}')
    print(f'    描述: {t.get("description", "")[:100]}')

# 检查低质量工具（描述过短或评分异常）
print(f'\n=== 低质量工具检查 ===')
short_desc = [t for t in data if len(t.get('description', '')) < 30]
print(f'描述过短(<30字符): {len(short_desc)} 个')

zero_scores = [t for t in data if any(v == 0 for v in t['scores'].values())]
print(f'有0分维度: {len(zero_scores)} 个')

no_pricing = [t for t in data if not t.get('pricing') or len(t['pricing']) == 0]
print(f'无定价信息: {len(no_pricing)} 个')

no_pros = [t for t in data if not t.get('pros') or len(t['pros']) == 0]
print(f'无优势信息: {len(no_pros)} 个')

no_cons = [t for t in data if not t.get('cons') or len(t['cons']) == 0]
print(f'无不足信息: {len(no_cons)} 个')
