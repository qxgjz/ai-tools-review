import json

data = json.load(open('data/tools.json', 'r', encoding='utf-8'))
sorted_tools = sorted(data, key=lambda x: x.get('overallScore', 0), reverse=True)

# Check top 3 tools full testingDetails
for i, t in enumerate(sorted_tools[:3]):
    print(f'\n{"="*60}')
    print(f'{i+1}. {t["name"]} (Score: {t.get("overallScore", 0)}/10)')
    print(f'{"="*60}')
    print(f'testingPeriod: {t.get("testingPeriod", "N/A")}')
    print(f'\ntestingDetails (full):')
    print(t.get('testingDetails', 'N/A'))
    print(f'\nlongDescription length: {len(str(t.get("longDescription", "")))} chars')
    print(f'review field: {str(t.get("review", "N/A"))[:200]}')

# Check if any tool has realExperience or testMetrics
has_real = sum(1 for t in data if t.get('realExperience') or t.get('testMetrics') or t.get('performanceData'))
print(f'\n\nTools with realExperience/testMetrics: {has_real}/{len(data)}')
