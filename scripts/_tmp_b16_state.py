# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
p = base + r'\iteration_center\state.json'
s = json.load(io.open(p, encoding='utf-8'))
print(json.dumps({k: (v if not isinstance(v, (list, dict)) else '<%s len=%s>' % (type(v).__name__, len(v))) for k, v in s.items()}, ensure_ascii=False, indent=1))
# show current_todo
todos = s.get('current_todo', s.get('todos', []))
if isinstance(todos, list):
    for t in todos[:8]:
        print('TODO:', json.dumps(t, ensure_ascii=False)[:300])
