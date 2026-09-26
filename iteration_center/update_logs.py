import json
from datetime import datetime

# Update state.json
with open('iteration_center/state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

state['current_iteration'] = state.get('current_iteration', 71) + 1
state['last_run'] = datetime.now().isoformat()

# Mark completed tasks
completed_ids = ['P1-005', 'P1-006', 'P1-007']
for task in state.get('todo', []):
    if task.get('id') in completed_ids:
        task['status'] = 'completed'
        task['completed_at'] = datetime.now().isoformat()

with open('iteration_center/state.json', 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

cur = state['current_iteration']
print(f"[OK] state.json updated to iteration {cur}")

# Update iteration_log.json
with open('iteration_center/iteration_log.json', 'r', encoding='utf-8') as f:
    log = json.load(f)

new_entry = {
    'iteration': cur,
    'date': datetime.now().isoformat(),
    'tasks_completed': ['P1-005', 'P1-006', 'P1-007'],
    'files_changed': ['next.config.mjs', 'app/tools/[slug]/page.tsx'],
    'commit': '6ad5d592 + 37fe6a02',
    'summary': 'Fixed blog category redirects (tools->ai-tools, added coding/chat/search), tightened tool title truncation to 24 chars (<=60 total), added word-boundary meta description truncation at 155 chars',
    'verification': 'Homepage 200, tool page 200, blog page 200, all 4 redirects return 308, title 47 chars, meta 153 chars'
}

if isinstance(log, list):
    log.insert(0, new_entry)
    log = log[:20]
elif isinstance(log, dict):
    if 'iterations' not in log:
        log['iterations'] = []
    log['iterations'].insert(0, new_entry)

with open('iteration_center/iteration_log.json', 'w', encoding='utf-8') as f:
    json.dump(log, f, indent=2, ensure_ascii=False)
print("[OK] iteration_log.json updated")
