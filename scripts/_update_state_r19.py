import json, io, sys
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
p = 'iteration_center/state.json'
d = json.load(open(p, encoding='utf-8'))
now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
items = d['next_iteration_focus']

def has_id(iid):
    return any(x.get('id') == iid for x in items)

# --- 技术类（架构师已自修完成，留痕为 completed）---
if not has_id('SEO-AUDIT-20261014-DUAL-H1'):
    items.append({
        'id': 'SEO-AUDIT-20261014-DUAL-H1',
        'task': '全站双H1根因修复：lib/markdown.ts h1->h2 正则漏转无属性<h1>，产生<h1>...</h2>畸形对，审计计为第二H1',
        'priority': 'P1', 'status': 'completed', 'assigned_to': ['window1', '架构师'],
        'source': 'seo_audit_20261014', 'created_at': now, 'completed_at': now,
        'completion_note': '根因=正则/<h1(\s+[^>]*?)>/g不匹配无属性<h1>，闭合</h1>却已转</h2>→畸形标签。改/<h1([^>]*)>/g后162篇博客全部单H1（本地产物验证0非单H1）。commit 414bd45 Deploy success，线上/blog/runway-vs-pika-2026/渲染正常。'
    })
if not has_id('SEO-AUDIT-20261014-CATEGORY-META'):
    items.append({
        'id': 'SEO-AUDIT-20261014-CATEGORY-META',
        'task': '博客分类页Title/Meta过长（8页，title 63-95字符/meta 170字符）：categoryName用分类并集拼接导致',
        'priority': 'P1', 'status': 'completed', 'assigned_to': ['window1', '架构师'],
        'source': 'seo_audit_20261014', 'created_at': now, 'completed_at': now,
        'completion_note': 'generateMetadata加长度截断（title≤60、desc≤155保留关键词）。37个category页全部合规（本地产物验证0超长）。commit 414bd45 Deploy success，线上/blog/category/ai-tools/ title已截断渲染。'
    })
# --- 内容类（派 window2/创作家）---
if not has_id('SEO-AUDIT-20261014-BROKEN-LINKS'):
    items.append({
        'id': 'SEO-AUDIT-20261014-BROKEN-LINKS',
        'task': '全站broken外链188条待核（812 URL审计）：403反爬类(ProductHunt/G2/Midjourney等实际活链)、404死链(bing.com/images/create等)、timeout类(jina.ai/mistral等)需人工核实替换或移除',
        'priority': 'P1', 'status': 'pending', 'assigned_to': ['window2', '创作家'],
        'source': 'seo_audit_20261014', 'created_at': now,
        'completion_note': '详细清单见iteration_center/seo_audit_full_20260917.md Broken外链节；403类勿当死链删除（反爬拒绝bot），仅处理确认404/timed out目标失效的链接。'
    })

json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
from collections import Counter
c = Counter(x.get('priority') for x in items if x.get('status') == 'pending')
mine = [x for x in items if x.get('status') == 'pending' and ('window1' in x.get('assigned_to', []) or '架构师' in x.get('assigned_to', []))]
print('新增3条。架构师pending:', len(mine), '| 全局pending:', sum(c.values()), dict(c))
