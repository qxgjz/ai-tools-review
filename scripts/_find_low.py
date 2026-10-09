import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
d = json.load(open('iteration_center/zensink_content_quality_report.json', 'r', encoding='utf-8'))
rows = sorted(d['all_results'], key=lambda r: r['score'])
already = {'midjourney-v7-vs-flux-2026','chatgpt-vs-claude-2026-comparison','claude-37-vs-gpt4o'}
print('=== Lowest 20 (excluding already-optimized) ===')
n = 0
for r in rows:
    if r['slug'] in already: continue
    print(f"  score={r['score']:>3}  words={r.get('word_count',0):>5}  slug={r['slug']}")
    n += 1
    if n >= 20: break
