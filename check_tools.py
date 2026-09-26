import json

data = json.load(open('data/tools.json', 'r', encoding='utf-8'))
print(f'Total tools: {len(data)}')

sorted_tools = sorted(data, key=lambda x: x.get('overallScore', 0), reverse=True)
print('\nTop 20 tools:')
for i, t in enumerate(sorted_tools[:20]):
    print(f'  {i+1}. {t["name"]} - {t.get("overallScore", 0)}/10 - {t.get("category", "N/A")}')

# Check testing fields for top 5
print('\n--- Testing fields for Top 5 tools ---')
for i, t in enumerate(sorted_tools[:5]):
    print(f'\n{i+1}. {t["name"]}:')
    print(f'   testingPeriod: {t.get("testingPeriod", "N/A")}')
    print(f'   testingDetails: {str(t.get("testingDetails", "N/A"))[:200]}')
    print(f'   bestFor: {t.get("bestFor", "N/A")}')
    print(f'   verdict: {str(t.get("verdict", "N/A"))[:100]}')

# Check how many tools have testingDetails
has_testing = sum(1 for t in data if t.get('testingDetails') and len(str(t.get('testingDetails', ''))) > 50)
print(f'\nTools with testingDetails (>50 chars): {has_testing}/{len(data)}')
