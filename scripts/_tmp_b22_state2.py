# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
st = json.load(io.open(base + r'\iteration_center\state.json', encoding='utf-8'))
st['latest_commit'] = '32c70c9'
for entry in st['iteration_log']:
    if entry.get('batch') == 'batch22':
        entry['git'] = '32c70c9 pushed'
        entry['online_200'] = 'ai-video-generator-credits-burn-fast-2026/ai-tools-not-worth-the-money-2026/runway-vs-pika-2026 all 200'
        entry['deploy'] = 'success'
io.open(base + r'\iteration_center\state.json', 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False, indent=2))
print('state finalized, latest_commit =', st['latest_commit'], '| total =', st['total_articles_generated'])
