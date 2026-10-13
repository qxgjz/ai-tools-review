# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
st = json.load(io.open(base + r'\iteration_center\state.json', encoding='utf-8'))
print('total:', st.get('total_articles_generated'))
print('latest_commit:', st.get('latest_commit'))
print('last batch in log:', st['iteration_log'][-1].get('batch') if st.get('iteration_log') else None)
# todos assigned to window2/creator
todos = st.get('current_todo', [])
if not isinstance(todos, list):
    print('current_todo type:', type(todos))
    for k, v in (todos.items() if isinstance(todos, dict) else []):
        print(k, '->', json.dumps(v, ensure_ascii=False)[:200])
else:
    print('todo count:', len(todos))
    for t in todos:
        print(json.dumps(t, ensure_ascii=False)[:300])
