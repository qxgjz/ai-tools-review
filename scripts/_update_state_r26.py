import json, io, sys, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
p = r'iteration_center/state.json'
data = json.load(open(p, encoding='utf-8'))
now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
ids = {
 'P0-TOOL-FIX-001': '工具链11/11真实import验证通过：本轮实测环境仅3/11可用，pip补装8个缺失工具(opengtm/trafilatura/courlan/textstat/nltk/rank-bm25/chromadb/openserp)后重验11/11全OK；无代码改动',
 'P0-URL-MD-SUFFIX-20261016': '已复现确认-md垃圾URL不在当前站点：out/无-md产物、sitemap/_redirects/posts.json均无、线上web_fetch返回404死链；垃圾URL已清除，GSC曝光归零待Google重新爬取自然移除，无代码可改',
 'P1-PERF-COMPARE-20261016': '/compare首屏优化完成：RadarChart/MultiRadarChart改dynamicImport(ssr:false)于4个页面+tools-index数据改客户端fetch(public/data/tools-index.json)；首屏传输1803KB->879KB(-51%)，642KB共享chunk从首屏移除；tsc+build过；commit c183beb/97e9af0/d4b48e5已push',
 'ux_p1_ttfb_recovered_but_total_timeout_2026-10-16_17h': '服务器端web_fetch验证/compare/完整渲染（QuickAnswer/Top10表格/FAQ/选择器全在），判定疑误报（UX本机网络不可达模式，同r23-r25连续多轮）',
}
items = data.get('next_iteration_focus', [])
upd = 0
for it in items:
    iid = it.get('id', '')
    if iid in ids and it.get('status') != 'completed':
        it['status'] = 'completed'
        it['completed_at'] = now
        it['completion_note'] = ids[iid]
        upd += 1
        print('updated:', iid)
json.dump(data, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('updated count:', upd)
