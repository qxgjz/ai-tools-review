# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
st = json.load(io.open(base + r'\iteration_center\state.json', encoding='utf-8'))
print('iteration_log type:', type(st.get('iteration_log')))
il = st.get('iteration_log')
if isinstance(il, list):
    print('len:', len(il))
    if il:
        print(json.dumps(il[-1], ensure_ascii=False, indent=1)[:800])
elif isinstance(il, dict):
    print(json.dumps(il, ensure_ascii=False, indent=1)[:800])
print('last_action:', st.get('last_action'))
print('last_update:', st.get('last_update'))
print('last_iteration_date:', st.get('last_iteration_date'))
print('last_round:', st.get('current_round'))
print('last_published_article:', json.dumps(st.get('last_published_article'), ensure_ascii=False)[:200])
print('publication_stats:', json.dumps(st.get('publication_stats'), ensure_ascii=False)[:300])
print('total_posts:', st.get('total_posts'))
