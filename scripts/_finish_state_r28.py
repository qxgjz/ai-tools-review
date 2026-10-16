import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
p = r'iteration_center/state.json'
d = json.load(open(p, encoding='utf-8'))
items = d['next_iteration_focus']

notes = {
    'CF-20261017-001': '完成可落地部分：CF GraphQL httpRequests1dGroups 拉取 10/3-10/10 每日请求/页面/唯一数，bot_traffic_pct=92.6（GA4 engaged 反向；CF 非页面请求占比 70.5%），分析报告 iteration_center/cf_bot_analysis_2026-10-17.md。UA点名部分阻塞：现有 CF token 无 httpRequestsAdaptiveGroups（UA/路径维度）与 Logpush 权限（403）→ 需指挥官提供 Zone Analytics 全权限 token 或 dashboard 开启 Logpush（见报告行动项）',
    'CF-20261017-002': 'app/robots.ts 新增 8 个高消耗采集爬虫限制（CCBot/PetalBot/SeznamBot/YisouSpider/facebookexternalhit/ia_archiver/DotBot/MegaIndex.ru/Barkrowler），保留全部 AI 搜索 bot 允许（GEO 不倒退）；Bot Fight Mode 需 CF dashboard 手动开启（API token 无权限），已在日志记录行动项',
    'GA4-20261017-003': '根因：layout gtag config send_page_view:false + GA4PageTracker 首屏 useEffect 早于 gtag.js(afterInteractive) 就绪 → 首屏 page_view 丢失 → landing (not set)。修复：GA4PageTracker 首屏轮询等待 gtag 就绪（10×200ms）后发送 page_view（带 page_location/page_path/page_title/page_type）。tsc+build 通过',
}
for i in items:
    if i.get('id') in notes:
        i['status'] = 'completed'
        i['completed_at'] = '2026-10-17T02:00:00'
        i['completion_note'] = notes[i['id']]
        print('completed:', i['id'])

# bot_traffic_pct 字段
d['bot_traffic_pct'] = 92.6
d['bot_traffic_pct_note'] = '2026-10-17 architect r28: GA4 engaged 反向口径（100-7.4）；CF 非页面请求占比 70.5%；cf_bot_analysis_2026-10-17.md 含多口径'
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('bot_traffic_pct = 92.6 written')

# 复核
d2 = json.load(open(p, encoding='utf-8'))
arch = [i for i in d2['next_iteration_focus'] if '架构师' in i.get('assigned_to', [])]
pend = [i for i in arch if i.get('status') == 'pending']
print('架构师 pending 剩余:', len(pend))
