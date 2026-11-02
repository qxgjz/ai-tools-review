# -*- coding: utf-8 -*-
"""r44 收尾：闭环 P0-REQ13-VERIFY（12/13 200，baml 404）+ 新开 CTR 首页 + 产出/日志"""
import json, os, shutil
from datetime import datetime

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
NOW = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

# ===== 1. state.json =====
sp = os.path.join(P, 'iteration_center', 'state.json')
with open(sp, encoding='utf-8') as f:
    d = json.load(f)
nf = d['next_iteration_focus']

REQ_EV = ('r44 正式验证（11-02 到期日，requests 走代理 7890 实抓）：13 个高价值页线上可抓性 12/13 全部 200 '
          '（exa/claude/suno/kagi/llama-cpp/vllm/lobe-chat/langchain/crewai/deepeval/pr-agent/promptfoo，final 均带斜杠）；'
          'baml /tools/baml/ **404 页面不存在**（本地 posts.json 283 篇 0 命中）。sitemap 收录层：952 URLs 中 12/13 在站、'
          'GSC discovered=950。验证结论：12/13 通过（可抓取+在 sitemap），baml 失败（从未上线）→ 需补页或名单剔除。'
          '限制：逐 URL indexed 状态受 URL Inspection API 403 限制（死路），以可抓取+sitemap+discovered 三重证据判定')
GSC_EV = ('r44 预查（11-02，窗口 10-02~10-31 已滚动）：10-31 曝光=1 **无回升**（10-26/27 峰 18/16 后 10-28/29/30/31=4/1/1/1 连续 4 天低位）；'
          '新窗口 154 imp/pos 15.75 较上窗口 155/15.66 曝光持平略降。11-03 正式复查结论倾向"未恢复"，'
          '建议架构师复查时重点看 11-01/11-02 两日是否仍 <5')

# 闭环 REQ13
for i in nf:
    if i.get('id') == 'P0-REQ13-VERIFY-20261102':
        i['status'] = 'completed'
        i['completed_at'] = NOW
        i['evidence'] = REQ_EV
        i['closed_by'] = 'analyst_r44'
    elif i.get('id') == 'P0-GSC-REVIEW-20261103':
        i['evidence'] = GSC_EV

# 新开 CTR（查重：12 张历史 pending 无首页）
ids = {i.get('id') for i in nf}
new_ctr = 'CTR-PAGE-HOMEPAGE-20261102'
if new_ctr not in ids:
    nf.append({'id': new_ctr, 'priority': 'P1',
               'title': '首页 CTR 优化：pos 5.2 全站最大曝光页 12 imp 0 点击',
               'task': '页面 https://www.aitoolcrux.com/ 排名 5.2 但 CTR 仅 0%（impr=12 clk=0，全站最大曝光页），优化 title/meta description 提升点击率',
               'assigned_to': ['window5', '打磨师'], 'priority_flag': 'P1',
               'status': 'pending', 'created_at': NOW.split('T')[0],
               'source': 'ctr_optimization_20261102'})

# 新开 baml 补页/剔除确认
new_baml = 'P1-REQ13-BAML-20261102'
if new_baml not in ids:
    nf.append({'id': new_baml, 'priority': 'P1',
               'title': 'REQ13 baml 页缺失：404 从未上线，需补页或从名单剔除',
               'task': 'REQ13 名单中 baml（BoundaryML）无 /tools/baml/ 页面（线上 404、posts.json 0 命中、sitemap 无）——若名单确含 baml 则创建工具页并提交 sitemap；若名单不含则忽略并更新 REQ13 记录',
               'assigned_to': ['window2', '创作家', 'window1', '架构师'], 'priority_flag': 'P1',
               'status': 'pending', 'created_at': NOW.split('T')[0],
               'source': 'req13_verification_20261102', 'data_verified': True})

with open(sp, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
pend = len([i for i in nf if i.get('status') == 'pending'])
print('state: focus=%d pending=%d' % (len(nf), pend))

# ===== 2. latest_report.md 更新 =====
src = os.path.join(P, 'gsc-ga4-report', '2026-10-02_2026-10-31.md')
dst = os.path.join(P, 'gsc-ga4-report', 'latest_report.md')
shutil.copyfile(src, dst)
print('latest_report.md 已更新为 10-02~10-31 窗口')

# ===== 3. audit_findings.md r44 段 =====
open(os.path.join(P, 'iteration_center', 'audit_findings.md'), 'a', encoding='utf-8').write("""

## r44（2026-11-02 · 分析师-数据洞察 SOP 触发）

### P0 REQ13 正式验证（到期日闭环）
| URL（/tools/） | 线上响应 | sitemap 在站 | 判定 |
|---|---|---|---|
| exa/claude/suno/kagi/llama-cpp/vllm/lobe-chat/langchain/crewai/deepeval/pr-agent/promptfoo | 12/12 全 200 | ✅（952 URLs） | ✅ 通过 |
| baml | **404** | ❌（无此页） | ❌ 失败 |

结论：12/13 通过（可抓取+sitemap+discovered 950 三重证据）；**baml 从未上线** → 新开 P1-REQ13-BAML-20261102（补页或剔除）。限制：逐 URL indexed 受 API 403 限制，以三重证据判定。

### P0 GSC 断崖 48h 预查（正式复查 11-03）
- 窗口 10-02~10-31 = **154 imp / 0 clk / pos 15.75**（上窗口 155/15.66，曝光持平略降）
- **10-31=1 曝光，连续 4 天 4/1/1/1 低位，无回升迹象** → 11-03 正式复查结论倾向"未恢复"；建议架构师查 11-01/11-02 是否仍 <5

### P1 CTR 待办积压发现（本轮新开仅 1 张的原因）
- 历史 CTR pending **12 张**（10-27/10-28/11-01 批次）全部未执行，本轮新窗口候选 observability 9.5/productivity 10.5/meeting 9.0/marketing 8.0/guide 10.0/comparison 18.0/about 全部已被覆盖
- 唯一新候选：**首页 pos 5.2（12 imp 全站最大曝光页）** → 新开 CTR-PAGE-HOMEPAGE-20261102
- 发现：CTR 待办积压导致重复开单空间耗尽，需打磨师批量执行 12 张历史单
""")

# ===== 4. keyword_opportunities.md r44 段 =====
open(os.path.join(P, 'iteration_center', 'keyword_opportunities.md'), 'a', encoding='utf-8').write("""

## r44（2026-11-02 · 复核轮）

- Easy Wins：aizolo reviews pos 22（imp 1）不足 5 个跳过；tabbyml pos 18 已开 CTR 单
- 竞品缺口 0 新（GAP 10 条全历史覆盖）；无新 P0 关键词（不硬凑）
- REQ13 验证：12/13 在站可抓取，baml 404 缺失
- Total keywords analyzed：6 查询 + 77 竞品分类
""")

# ===== 5. competitor_analysis_2026-11-02.md =====
open(os.path.join(P, 'iteration_center', 'competitor_analysis_2026-11-02.md'), 'w', encoding='utf-8').write("""# 竞品分析 r44（2026-11-02）

## 复抓结果（futurepedia 77 分类，requests+proxy 7890）
- GAP 10 条（chatbots/productivity/workflows/religion/marketing/automations/human-resources/presentations/legal/teachers/transcriber 等）——逐条对照历史 CA/KW 记录**全部已覆盖** → **0 新缺口**
- 结构性缺口不变：课程/教程类内容我们 0（CA 3 条已开）

## SERP 验证
无（0 新缺口词，禁止编造）
""")

# ===== 6. 双日志 append r44 段 =====
open(os.path.join(P, 'window_logs', 'analyst_2026-11-02.md'), 'a', encoding='utf-8').write("""

## r44 段（11-02 触发）
- 执行待办：**1 条闭环**（P0-REQ13-VERIFY-20261102：12/13 在站 200、baml 404 → 新开补页单）+ GSC-REVIEW 预查（10-31=1 无回升）
- 新发现：**2 条**（①REQ13 验证结果+baml 缺失；②CTR 12 张历史单积压导致重复耗尽，本轮仅 1 张新开）
- CTR 新开单：**1 张**（CTR-PAGE-HOMEPAGE-20261102 pos5.2/0%/12imp）
- 挖词 0；竞品缺口 0 新；SERP 0；Easy Wins 跳过
- 剩余 pending：%d（脚本复核）
- 环境：GSC 窗口滚动 10-02~10-31（154/15.75）；代理正常；ego-browser 不可用（requests 实抓替代）
""" % pend)

open(os.path.join(P, 'window_logs', 'analyst_keyword_2026-11-02.md'), 'a', encoding='utf-8').write("""

## r44 段（复核轮）
1. 竞品挖词：✅ 77 分类复抓，GAP 10 全历史覆盖 → 0 新
2. Easy Wins：✅ aizolo pos22 imp1 不足 5 跳过
3. 扩展/分级/SERP：无新候选，跳过
4. 输出：✅ keyword_opportunities.md r44 段；挖词 0 条写入
""")
print('r44 files written')
