# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
s = json.load(io.open(base + r'\iteration_center\state.json', encoding='utf-8'))
print('articles:', s.get('total_articles_generated'))
print('last_update:', s.get('last_update'))
print('latest_commit:', s.get('latest_commit'))
print('--- current_todo ---')
for t in s.get('current_todo', []):
    print(json.dumps({k: t.get(k) for k in ['id','priority','title','status','assigned_to','source']}, ensure_ascii=False))
print('--- completed_todo last 5 ---')
for t in (s.get('completed_todo') or [])[-5:]:
    print(json.dumps(t, ensure_ascii=False)[:200])
