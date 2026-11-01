# -*- coding: utf-8 -*-
"""r42 收尾：state 更新（CTR 新开单 2 + SNAPSHOT evidence）+ 产出追加 + 双日志（2026-11-01）"""
import json, os, re
from datetime import datetime

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
NOW = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

# ===== 1. state.json =====
sp = os.path.join(P, 'iteration_center', 'state.json')
with open(sp, encoding='utf-8') as f:
    d = json.load(f)
nf = d['next_iteration_focus']

# P0-GSC-SNAPSHOT-RETRY evidence（保持 pending，indexed 环比不可得）
for i in nf:
    if i.get('id') == 'P0-GSC-SNAPSHOT-RETRY-20261029':
        i['evidence'] = (
            'r42 2026-11-01 AdsPower CDP 实抓：sitemaps 页 submitted=950、已发现网页=950、状态成功、上次读取 2026-11-01 '
            '（10-28 时 931 → 环比 +19，10-18 提交批次被 Google 读取）；indexing 端点 /search-console/indexing 404 再确认'
            '（GSC 改版死路）——indexed/not_indexed 完整环比待 GSC 恢复；sitemaps discovered 950 作为周度替代跟踪指标'
        )

# CTR 新开单 2 条（查重后确认 NEW）
existing_sources = set()
for i in nf:
    if 'ctr_optimization' in str(i.get('source', '')):
        existing_sources.add(str(i.get('id')))
new_ctr = [
    {
        'id': 'CTR-PAGE-MARKETING-TOOLS-20261101',
        'priority': 'P1',
        'status': 'pending',
        'assigned_to': ['window5', '打磨师'],
        'task': '页面 https://www.aitoolcrux.com/blog/best-ai-marketing-tools-2026 排名 8.0 但 CTR 仅 0%（imp 1，新窗口 10-01~10-30 新进 5-15 区间），优化 title/meta description 提升点击率',
        'source': 'ctr_optimization_2026-11-01',
        'created_at': NOW,
    },
    {
        'id': 'CTR-QUERY-TABBYML-20261101',
        'priority': 'P1',
        'status': 'pending',
        'assigned_to': ['window5', '打磨师'],
        'task': '查询 [tabbyml] 排名 18.0 但 CTR 仅 0%（imp 1，5-20 扩大范围），优化匹配页 title/meta 提升点击率',
        'source': 'ctr_optimization_2026-11-01',
        'created_at': NOW,
    },
]
added = 0
for c in new_ctr:
    if c['id'] not in existing_sources:
        nf.append(c)
        added += 1
with open(sp, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
pend_after = len([i for i in nf if i.get('status') == 'pending'])
print('state: focus=%d pending=%d ctr_added=%d' % (len(nf), pend_after, added))

# ===== 2. audit_findings.md r42 段 =====
open(os.path.join(P, 'iteration_center', 'audit_findings.md'), 'a', encoding='utf-8').write("""

## r42（2026-11-01 15:0x · 分析师-数据洞察 SOP 触发）

### P0: 新窗口 GSC 实拉 10-01~10-30：155 imp / 0 clk / pos 15.66（fetch_gsc 自动窗口 UTC-2d）
| 指标 | 本轮(10-01~30) | r41(09-28~10-27) | 口径 |
|---|---|---|---|
| Impressions | 155 | 197 | 窗口错 3 天（少 9 月末 3 天/多 10-28~30 尾部），不可直接环比 |
| Avg Position | 15.66 | 13.22 | 同上口径 |
| MOBILE | 5 (pos 9.60) | 5 (pos 9.60→10-27口径) | 移动位次显著优于桌面(15.87) |

- **关键 P0 观察：回升未延续**。Daily trend：10-26=18、10-27=16 峰值后，**10-28=4 → 10-29=1 → 10-30=1 骤降**，确认曝光断崖（auto_redirect 9→94 暴增后 ~170-200 区间）仍未修复，P0-EXPOSURE-CLIFF 继续有效
- sitemaps 通道：**submitted=950 / 已发现网页=950**（10-28 931 → +19，10-18 提交批次 11-01 被 Google 读取成功）——P0-GSC-SNAPSHOT-RETRY 降级指标可用
- indexing 端点 /search-console/indexing 404 再确认（死路，indexed 环比待 GSC 恢复）
- 新页面 best-ai-marketing-tools-2026 pos 8.0（5-15 区间新候选 → CTR 开单）；新查询 bondai(89)/milvus ui(84)/react agent(82)/google gemini langgraph(75) 均深尾无效曝光
- 已闭环：P0-ANALYST-LOG-DISCIPLINE-20261029（日志核实存在，UTF-8 有效，乱码系 PowerShell 显示问题）
""")

# ===== 3. keyword_opportunities.md r42 段 =====
open(os.path.join(P, 'iteration_center', 'keyword_opportunities.md'), 'a', encoding='utf-8').write("""

## r42（2026-11-01 · Easy Wins 复核）

- GSC 新窗口 155 imp / pos 15.66；top queries 6 条：aizolo reviews(22) / tabbyml(18) / bondai(89.3) / google gemini langgraph(75) / milvus ui(84) / react agent(82)
- **Easy Wins（pos 20-50）：1 个候选（aizolo reviews pos22），不足 5 个跳过**（SOP 阈值）
- 竞品缺口：0 新（复抓 77 分类，11 个名义 GAP 全历史覆盖，与 r41 一致）
- CTR 新开单 2 条：marketing-tools(pos8.0) + tabbyml(pos18)
- Total keywords analyzed：6 查询（实读）+ 77 分类（竞品实抓）
""")

# ===== 4. latest_report.md 更新 =====
lr = os.path.join(P, 'gsc-ga4-report', 'latest_report.md')
with open(os.path.join(P, 'gsc-ga4-report', '2026-10-01_2026-10-30.md'), encoding='utf-8') as f:
    new_report = f.read()
with open(lr, 'w', encoding='utf-8') as f:
    f.write('# Latest GSC Report (analyst r42 更新 2026-11-01)\n\n' + new_report)
print('latest_report.md updated')

# ===== 5. 双日志 =====
lg = os.path.join(P, 'window_logs', 'analyst_2026-11-01.md')
open(lg, 'w', encoding='utf-8').write("""# analyst r42 日志（2026-11-01）

## 执行摘要
- 执行待办：**1 条闭环**（P0-ANALYST-LOG-DISCIPLINE-20261029：日志已存在 UTF-8 有效，Slug-GUARD 记录齐全）+ P0-GSC-SNAPSHOT-RETRY 降级实抓（sitemaps 950/950 环比 +19，indexing 404 死路保持 pending）+ 阻塞确认（REQ13 11-02 未到期；GEO-BASELINE/ELMO 需登录态/Docker）
- 新发现：**2 条 P0 级**（①10-26/27 峰值后 10-28~30 骤降 4→1→1，曝光回升未延续；②sitemaps discovered 950 环比 +19）+ 1 条页面级（marketing-tools pos8.0 新进 5-15）
- CTR：新开单 2 条（CTR-PAGE-MARKETING-TOOLS-20261101 / CTR-QUERY-TABBYML-20261101）
- 挖词：0（aizolo pos22 单词不足 5 跳过）；竞品缺口 0 新；SERP 0
- 写入待办：2 条（CTR）；剩余 pending：%d（以脚本复核为准）
- 环境：AdsPower 在线（k1hfuvv6:63325，GSC/GA4/OpenSEO 已登录多 tab）；GSC API 实拉成功（155/15.66）；indexing 端点 404 死路再确认；ego-browser 不可用

## 数据来源
- fetch_gsc.py 实拉 2026-10-01_2026-10-30.md（155 imp / 0 clk / pos 15.66，Daily trend 全 30 天）
- AdsPower CDP 实抓 sitemaps 页（950/950）与 indexing 端点（404）
- competitor_gap 复抓（77 分类，GAP 11 全历史覆盖）
""" % pend_after)

open(os.path.join(P, 'window_logs', 'analyst_keyword_2026-11-01.md'), 'w', encoding='utf-8').write("""# analyst keyword r42 日志（2026-11-01）

1. 竞品 sitemap 挖词：✅ 复抓 futurepedia 77 分类，11 名义 GAP 全历史覆盖，0 新
2. GSC Easy Wins：✅ 新窗口 6 查询解析；aizolo reviews pos22 唯一候选，不足 5 个跳过
3. 关键词扩展：无新核心词（缺口 0 + Easy Wins 不足），跳过
4. 分级：P0=0 / P1=0 / P2=0
5. SERP 验证：0（无 P0 候选，不编造）
6. 输出：✅ keyword_opportunities.md r42 段
7. state.json：CTR 2 条（非挖词类）；挖词 0 条新写入
8. 目标产出：P0 0/3、P1 0/5（客观无新词不硬凑，符合"禁止假完成"约束）
""")
print('logs written')
