# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
d = json.load(io.open(base + r'\iteration_center\zensink_content_quality_report.json', encoding='utf-8'))
print('total:', d.get('total'), '| avg:', d.get('average_score'), '| fail_count:', d.get('fail_count'))
for it in d.get('low_quality_articles', []):
    print(it.get('slug') or it.get('file') or it.get('title'), '| score:', it.get('score') or it.get('zens_ink_score'))
print('--- all_results sample ---')
ar = d.get('all_results', [])
print('all_results count:', len(ar) if isinstance(ar, list) else '?')
if isinstance(ar, list):
    # sort by score ascending, print bottom 30
    def sc(x):
        return x.get('score') or x.get('zens_ink_score') or 999
    for it in sorted(ar, key=sc)[:35]:
        print(' ', it.get('slug') or it.get('file') or it.get('title'), '|', sc(it))
