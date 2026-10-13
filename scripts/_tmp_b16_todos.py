# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
st = json.load(io.open(base + r'\iteration_center\state.json', encoding='utf-8'))
for t in st.get('current_todo', []):
    print(t.get('id'), '|', t.get('priority'), '|', t.get('status'), '|', t.get('assignee'), '|', t.get('title'))
    print('   desc:', str(t.get('description'))[:180])
