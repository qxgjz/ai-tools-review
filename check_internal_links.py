import json

with open('data/tools.json', 'r', encoding='utf-8') as f:
    tools = json.load(f)

# Check specific tools
target_tools = ['midjourney', 'cursor', 'elevenlabs', 'notion-ai']
print('=== Target Tools Status ===')
for slug in target_tools:
    tool = next((t for t in tools if t['slug'] == slug), None)
    if tool:
        total = sum(tool['scores'].values()) / len(tool['scores'])
        print(f'{slug}: FOUND - {tool["name"]} - category: {tool["category"]} - score: {total:.1f}')
    else:
        print(f'{slug}: NOT FOUND in tools.json')

# Get top 10 tools by score
print()
print('=== Top 10 Tools by Score ===')
scored_tools = []
for tool in tools:
    if 'scores' in tool and tool['scores']:
        total = sum(tool['scores'].values()) / len(tool['scores'])
        scored_tools.append((tool['slug'], tool['name'], total, tool['category']))

scored_tools.sort(key=lambda x: x[2], reverse=True)
for i, (slug, name, score, category) in enumerate(scored_tools[:10]):
    print(f'{i+1}. {name} ({slug}) - {score:.1f} - {category}')

# Check if target tools are in top 20
print()
print('=== Target Tools in Top 20? ===')
top20_slugs = [t[0] for t in scored_tools[:20]]
for slug in target_tools:
    if slug in top20_slugs:
        rank = top20_slugs.index(slug) + 1
        print(f'{slug}: YES - rank #{rank}')
    else:
        print(f'{slug}: NO - not in top 20')
