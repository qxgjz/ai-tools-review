import json
from pathlib import Path

STATE_FILE = Path(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json")

with open(STATE_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

todos = data['next_iteration_focus']

# 标记已完成的P0
for t in todos:
    title = t.get('title', '')
    if 'Vercel切到Cloudflare' in title or 'Vercel免费额度超300%' in title:
        t['status'] = 'completed'
        t['completed_at'] = '2026-10-02'
        print(f'✅ 标记完成: {title[:50]}')
    if 'GA4服务账号认证失败' in title:
        t['status'] = 'completed'
        t['completed_at'] = '2026-09-29'
        print(f'✅ 标记完成: {title[:50]}')

# 只保留未完成的
active = [t for t in todos if t.get('status') not in ('completed', 'archived')]

p0 = [t for t in active if t.get('priority') == 'P0']
p1 = [t for t in active if t.get('priority') == 'P1']

print(f'\n📊 最终待办: {len(active)}条')
print(f'  P0: {len(p0)}条')
print(f'  P1: {len(p1)}条')
print(f'\nP0任务:')
for t in p0:
    print(f'  - [{t.get("status")}] {t.get("title", "")[:60]}')

data['next_iteration_focus'] = active

with open(STATE_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('\n✅ 已保存')
