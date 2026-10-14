import json, io, sys
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
p = 'iteration_center/state.json'
d = json.load(open(p, encoding='utf-8'))
now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
items = d['next_iteration_focus']

notes = {
    'LEARN-20261014-05': '实证完成：Next.js output:\'export\' 全站 SSG 静态预渲染，162 篇博客 HTML 全部含完整正文（out/ 中位 284KB/页，非JS壳）。线上 web_fetch 直接返回正文即服务器端可抓取证据。ChatGPT browse 可完整读取，无需改动。',
    'LEARN-20261014-02': '9 篇无 faq 字段文章补 FAQPage schema 兜底：defaultFAQs 抽到纯数据模块 components/content/faqData.ts（原在 use client 组件，server 侧 dot 访问报错），博客页统一 faqItems 数据源。修复后 164/164 博客页含 FAQPage JSON-LD（本地产物验证 0 缺失）。commit c149d16 Deploy success，线上 n8n-review-2026/what-is-an-ai-agent FAQ 区块渲染正常。',
    'UX-PERF-RECHECK-20261014': '11:00 巡检通过：服务器端 web_fetch 首页 200（完整渲染）、/404 200（404 页正常）、/blog/chatgpt-vs-claude-2026/ 200。无 code=000/超时，全站响应正常，标记稳定归档。',
}

done = 0
for x in items:
    iid = x.get('id', '')
    for k, n in notes.items():
        if iid.startswith(k) and x.get('status') == 'pending':
            x['status'] = 'completed'
            x['completed_at'] = now
            x['completion_note'] = n
            done += 1
            print('completed:', iid)

json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

from collections import Counter
c = Counter(x.get('priority') for x in items if x.get('status') == 'pending')
mine = [x for x in items if x.get('status') == 'pending' and ('window1' in x.get('assigned_to', []) or '架构师' in x.get('assigned_to', []))]
print('本轮完成:', done, '| 架构师pending:', len(mine), '| 全局pending:', sum(c.values()), dict(c))
