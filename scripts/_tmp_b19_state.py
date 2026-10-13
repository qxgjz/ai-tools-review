# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
st = json.load(io.open(base + r'\iteration_center\state.json', encoding='utf-8'))
print('total:', st.get('total_articles_generated'))
print('latest_commit:', st.get('latest_commit'))
print('iteration_log entries:', len(st.get('iteration_log', [])))
print('last log keys:', list(st['iteration_log'][-1].keys()) if st.get('iteration_log') else None)
