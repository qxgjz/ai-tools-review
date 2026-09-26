import json

with open('data/tools.json', 'r', encoding='utf-8') as f:
    tools = json.load(f)

print(f'Total tools: {len(tools)}')
t = tools[0]
print(f'Fields: {list(t.keys())}')

has_bestFor = sum(1 for x in tools if x.get('bestFor'))
has_notIdeal = sum(1 for x in tools if x.get('notIdealFor'))
has_freeAlt = sum(1 for x in tools if x.get('freeAlternative'))
print(f'Has bestFor: {has_bestFor}')
print(f'Has notIdealFor: {has_notIdeal}')
print(f'Has freeAlternative: {has_freeAlt}')

if has_bestFor:
    for x in tools:
        if x.get('bestFor'):
            name = x['name']
            bf = x['bestFor']
            print(f'Sample bestFor ({name}): {bf}')
            break

cats = {}
for x in tools:
    c = x.get('category', 'unknown')
    cats[c] = cats.get(c, 0) + 1
print(f'Categories: {len(cats)}')
for c, n in sorted(cats.items(), key=lambda x: -x[1])[:10]:
    print(f'  {c}: {n}')
