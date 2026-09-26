import json
import os
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
data = json.load(open(os.path.join(base, 'data', 'tools.json'), 'r', encoding='utf-8'))
sorted_tools = sorted(data, key=lambda x: x.get('overallScore', 0), reverse=True)
print(f"Total tools: {len(data)}")
print(f"With realExperience: {sum(1 for t in data if t.get('realExperience'))}")
print()
print("Top 50 status:")
for i, t in enumerate(sorted_tools[:50]):
    rank = i + 1
    has = 'Y' if t.get('realExperience') else 'N'
    print(f"  {rank:2d}. [{has}] {t['name']:25s} ({t.get('category','?')})")
