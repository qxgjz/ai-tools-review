# -*- coding: utf-8 -*-
import io, json, datetime
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
p = base + r'\iteration_center\state.json'
s = json.load(io.open(p, encoding='utf-8'))
log = s.get('iteration_log', [])
print('iteration_log last:', json.dumps(log[-1] if log else None, ensure_ascii=False))
print('completed_tasks last:', json.dumps((s.get('completed_tasks') or [])[-1] if s.get('completed_tasks') else None, ensure_ascii=False)[:300])
