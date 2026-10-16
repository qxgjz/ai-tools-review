import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
p = r'iteration_center/state.json'
d = json.load(open(p, encoding='utf-8'))
items = d['next_iteration_focus']
# 去重防重复添加
ids = {i.get('id') for i in items}
if 'GEO-SLUG-NORM-R27' not in ids:
    items.append({
        "id": "GEO-SLUG-NORM-R27",
        "task": "GEO技术修复-分类slug规范化部署",
        "title": "blog category slug 单复数规范化部署（comparison→comparisons、guide→guides，6篇）+ _redirects 301；本地已修复且 tsc+build 门控通过、产物验证通过；待 push 部署+线上验证（github.com 网络阻塞）",
        "priority": "P1",
        "status": "pending",
        "assigned_to": ["window1", "架构师"],
        "source": "geo_audit_2026-10-17",
        "created_at": "2026-10-17T00:15:00",
        "completion_note": "push 阻塞于 github.com:443 不可达（5次重试+HTTP/1.1；ssh.github.com:443 可达但无SSH key）；commit 已本地就绪"
    })
    print('新增待办 GEO-SLUG-NORM-R27')
else:
    print('已存在，跳过')
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
# 复核
d2 = json.load(open(p, encoding='utf-8'))
arch = [i for i in d2['next_iteration_focus'] if '架构师' in i.get('assigned_to', [])]
pend = [i for i in arch if i.get('status') == 'pending']
print('架构师 pending 总数:', len(pend))
for i in pend:
    print('-', i.get('priority'), i.get('id'), '|', i.get('title', '')[:50])
