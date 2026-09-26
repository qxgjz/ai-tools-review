import json

with open('data/tools.json', 'r', encoding='utf-8') as f:
    tools = json.load(f)

sorted_tools = sorted(tools, key=lambda x: x.get('overallScore', 0), reverse=True)

print(f"Total tools: {len(tools)}")
print(f"Tools with realExperience: {sum(1 for t in tools if t.get('realExperience'))}")
print()

print("Top 50 tools status:")
print("=" * 80)
for i, t in enumerate(sorted_tools[:50]):
    rank = i + 1
    has_exp = bool(t.get('realExperience'))
    status = '✓' if has_exp else '✗'
    print(f"  {rank:2d}. {status} {t['name']:25s} ({t.get('category', '?'):15s}) - {t.get('overallScore', 0)}/10")

print()
print("Tools 21-50 missing realExperience:")
missing = [t for t in sorted_tools[20:50] if not t.get('realExperience')]
print(f"  Count: {len(missing)}/30")
for t in missing:
    print(f"    - {t['name']} ({t.get('category')})")
