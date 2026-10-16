import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
p = r'iteration_center/state.json'
d = json.load(open(p, encoding='utf-8'))
items = d['next_iteration_focus']
for i in items:
    if i.get('id') == 'GEO-SLUG-NORM-R27':
        i['status'] = 'completed'
        i['completed_at'] = '2026-10-17T00:30:00'
        i['completion_note'] = '分类slug规范化已上线：push 506cb48 → Deploy to Cloudflare Pages success；线上 /blog/category/comparisons/ 与 /blog/category/guides/ 200（11/4篇文章），旧 URL /blog/category/comparison 与 /guide 301 跟随成功；sitemap 去重（out 无单数分类）'
        print('GEO-SLUG-NORM-R27 -> completed')
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
# 复核
d2 = json.load(open(p, encoding='utf-8'))
arch = [i for i in d2['next_iteration_focus'] if '架构师' in i.get('assigned_to', [])]
pend = [i for i in arch if i.get('status') == 'pending']
print('架构师 pending 剩余:', len(pend))
for i in pend:
    print('-', i.get('priority'), i.get('id'))
