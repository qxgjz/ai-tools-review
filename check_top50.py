import json

data = json.load(open('data/tools.json', 'r', encoding='utf-8'))
sorted_tools = sorted(data, key=lambda x: x.get('overallScore', 0), reverse=True)

print('Top 21-50 tools (to be enhanced in Iteration 5):')
print('=' * 70)
for i, t in enumerate(sorted_tools[20:50]):
    rank = i + 21
    has_experience = bool(t.get('realExperience'))
    status = '✓ HAS' if has_experience else '✗ MISSING'
    print(f'  {rank:2d}. {t["name"]:25s} ({t["slug"]:30s}) - {t.get("overallScore", 0)}/10 - {status}')

print()
print(f'Total tools with realExperience: {sum(1 for t in data if t.get("realExperience"))}/{len(data)}')
print(f'Tools 21-50 with realExperience: {sum(1 for t in sorted_tools[20:50] if t.get("realExperience"))}/30')
