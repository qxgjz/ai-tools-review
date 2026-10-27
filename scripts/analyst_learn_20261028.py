# -*- coding: utf-8 -*-
"""2026-10-28 分析师-数据学习：AI 搜索流量分析（GEO/AEO）→ 落地 state.json + 笔记 + commander_learning"""
import json, os
from datetime import datetime

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
now_iso = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
today = '2026-10-28'

state_p = os.path.join(P, 'iteration_center', 'state.json')
d = json.load(open(state_p, encoding='utf-8'))
nf = d['next_iteration_focus']
ids = {i.get('id') for i in nf}

added = []
def add_todo(t):
    if t['id'] not in ids:
        nf.append(t); ids.add(t['id']); added.append(t['id'])

# ===== 落地待办（assigned_to=分析师） =====
add_todo({'id': 'P1-AI-OVERVIEWS-BASELINE-20261028', 'status': 'pending', 'priority': 'P1',
          'assigned_to': ['window4', '分析师'],
          'task': 'GSC Generative AI 报告核查：2026-08-31 已全站上线，打开 GSC Performance→Generative AI tab（若 AI 数据量过少不显示则记录门槛），记录 AI Overviews/AI Mode 印象基线（按页面/国家拆分）；联动 GEO-BASELINE-AUDIT-20261013 的 Google 侧数据层',
          'source': 'learning_ai_search_geo_20261028', 'data_verified': True, 'created_date': today})
add_todo({'id': 'P1-GEO-PROOF-LEDGER-20261028', 'status': 'pending', 'priority': 'P1',
          'assigned_to': ['window4', '分析师'],
          'task': '建 Proof Ledger 买家问题库（20 个，从 LONGTAIL P0 场景选：best ai essay writer/free thumbnail maker/voiceover 等），每月首工作日跑 ChatGPT/Perplexity/Claude/Gemini 四引擎，记录引用出现/URL/位置；计算 share of mentions=品牌出现 prompts/总 prompts；这是 GEO-BASELINE-AUDIT-20261013 的可执行方法论',
          'source': 'learning_ai_search_geo_20261028', 'data_verified': True, 'created_date': today})
add_todo({'id': 'P2-GA4-AI-CHANNEL-20261028', 'status': 'pending', 'priority': 'P2',
          'assigned_to': ['window4', '分析师'],
          'task': 'GA4 自定义渠道组：regex 匹配 AI 工具来源（perplexity.ai/chatgpt.com/claude.ai/gemini.google.com/copilot.microsoft.com）补齐 GA4 AI Assistant 行漏计的 AI 引流，与 GSC Generative AI 印象交叉分析',
          'source': 'learning_ai_search_geo_20261028', 'data_verified': True, 'created_date': today})
add_todo({'id': 'P2-QUOTE-CITATION-GEO-20261028', 'status': 'pending', 'priority': 'P2',
          'assigned_to': ['window4', '分析师'],
          'task': 'GEO 文章模板要素落地：Princeton GEO 论文实证"引文+引用权威来源"提升 AI 可见性最高 40%（领域依赖）；给创作家的文章 SOP 增加引用/引语密度要求，供 KW/CA 待办执行时参考',
          'source': 'learning_ai_search_geo_20261028', 'data_verified': True, 'created_date': today})

d['next_iteration_focus'] = nf
d['last_update'] = now_iso
json.dump(d, open(state_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
pend = len([i for i in nf if i.get('status') == 'pending'])
print('added:', added)
print('focus:', len(nf), '| pending:', pend)

# ===== 学习笔记 =====
note = f"""# 数据学习：AI 搜索流量分析（GEO/AEO）· 2026-10-28

## 主题
AI 搜索流量分析：GSC Generative AI 报告 + GEO 测量方法论 + 2026 AIO 点击影响数据

## 权威来源（5 组）
1. Google Search Console Generative AI 报告（leadverge.io / web25.io / auspia.ai / computese.com / neuraladx.com，2026-09 实操指南）
2. Princeton GEO 论文（arXiv 2311.09735 / OpenReview NV6rn7j5p5，GEO-bench 10k 查询）
3. Proof Ledger 方法论（theanswerengine.ai，2026-06）
4. 零点击研究（SparkToro/Search Engine Land 68%；Ahrefs 减点击 58%；Pew 8%）
5. AIO 覆盖率与 CTR 影响（soedja/DemandSphere 品牌词 80%；toolsolved position-1 丢 34.5-58%；euracle share of mentions）

## 12 个知识点
1. **GSC Generative AI 报告**：2026-08-31 全站上线，统计 AI Overviews + AI Mode 印象，可按页面/国家/设备/日期拆分
2. **报告显示门槛**：AI 数据量过少时不显示该 tab（aitoolcrux 印象量小，需实测核查）
3. **Opt-out 存在**：Search generative AI control 可排除站点出 AIO/AI Mode（几天生效，不影响普通搜索排名）
4. **GA4 原生 AI 行**：traffic acquisition 自带 AI Assistant 渠道行
5. **GA4 补漏**：自定义渠道组 regex 匹配 AI 来源（GA4 会漏计 AI 工具引流）
6. **PAWC 指标**：Princeton 提出位置调整字数 = 答案中出现位置越靠前权重越高 + 引用字数贡献
7. **GEO 方法有效性**：9 种方法中引文/引语类提升可见性最高 40%，且领域依赖（同一方法不同领域效果不同）
8. **Proof Ledger**：固定 20 个买家问题，月度跑 4 引擎，记引用出现/URL/位置 = 免费可复现的 GEO 基线
9. **零点击 68%**：SparkToro 2026 初，不到 1/3 Google 搜索仍产生点击
10. **AIO 减点击 58%**：Ahrefs 30 万关键词研究（2025-12 发布）
11. **Pew 8%**：AI 框出现时用户点击有机结果仅 8%；position-1 丢 34.5%-58% 点击
12. **品牌词 AIO 激增**：2026-09 品牌词 AI Overviews 覆盖 26%→80%（三倍）；share of mentions = 品牌出现 prompts/总 prompts

## 对 AIToolCrux 的可落地结论
- GEO-BASELINE-AUDIT 阻塞项有了完整方法论：GSC Generative AI 报告（Google 侧）+ Proof Ledger 四引擎（AI 侧）双轨
- 文章层：引用权威来源+直接引语 → AI 引用可见性提升（联动现有 GEO/AEO 审计强约束）
- 监控层：GA4 AI 渠道 regex + GSC AIO 印象 = 零成本 AI 流量监控
- 数据层：AIO 印象 = 无点击也有曝光价值（当前 GSC 0 点击不代表无 AI 价值）

## 落地待办
{json.dumps(added, ensure_ascii=False)}
"""
open(os.path.join(P, 'gsc-ga4-report', 'learning_ai_search_geo_20261028.md'), 'w', encoding='utf-8').write(note)
print('note written')

# ===== commander_learning.md 摘要 =====
cl = r'C:\Users\通明街\Doubao\chats\2026-09-02\new-chat\commander_learning.md'
seg = f"""

### 2026-10-28 数据学习：AI 搜索流量分析（GEO/AEO）
**权威来源(5)**：GSC Generative AI 报告实操指南（leadverge/web25/auspia/computese/neuraladx）/ Princeton GEO 论文（arXiv 2311.09735）/ Proof Ledger 方法论（theanswerengine）/ 零点击数据（SparkToro 68%·Ahrefs 58%·Pew 8%）/ AIO 品牌词覆盖 80%（soedja）
**12个知识点核心**：
1. GSC Generative AI 报告 2026-08-31 全站上线（AIO+AI Mode 印象，按页/国/设备拆分）；**数据量过少不显示 tab，aitoolcrux 需实测**
2. GA4 traffic acquisition 原生 AI Assistant 行 + 自定义渠道组 regex 补漏 AI 来源（GA4 会漏计）
3. **PAWC 指标**（位置调整字数）：答案位置越靠前权重越高 → AI 引用评估的量化基准
4. **引文+引语提升 AI 可见性最高 40%**（Princeton，领域依赖）→ 文章模板加引用密度要求
5. **Proof Ledger 方法**：固定 20 买家问题×4 引擎（ChatGPT/Perplexity/Claude/Gemini）月度跑，记引用/URL/位置 + share of mentions → GEO-BASELINE 可执行方法论（已开 P1 待办）
6. 零点击 68%（SparkToro 2026 初）；AIO 减点击 58%（Ahrefs 30万词）；Pew 用户仅 8% 点有机结果；position-1 丢 34.5-58%
7. 品牌词 AIO 覆盖 26%→80%（2026-09 三倍激增）→ 品牌词保护是 GEO 重点
8. Opt-out 存在（Search generative AI control，不影响普通排名）
9. **AIO 印象=无点击也有曝光价值**：当前 GSC 0 点击≠无 AI 价值，印象层必须监控
10. 落地：4 条分析师待办（P1-AI-OVERVIEWS-BASELINE / P1-GEO-PROOF-LEDGER / P2-GA4-AI-CHANNEL / P2-QUOTE-CITATION-GEO）
"""
with open(cl, 'a', encoding='utf-8') as f:
    f.write(seg)
print('commander_learning appended')

# ===== 日志 =====
log = f"""

## 2026-10-28 数据学习（分析师-数据学习 定时触发）

- 主题：AI 搜索流量分析（GEO/AEO）
- 权威来源：5 组（GSC Generative AI 报告 / Princeton GEO 论文 / Proof Ledger / 零点击研究 / AIO 覆盖率）
- 知识点：12 个（PAWC/引文40%/零点击68%/Pew 8%/品牌词80%/Opt-out/GSC报告门槛 等）
- 落地待办：4 条（P1×2 + P2×2，assigned_to=分析师）→ GEO-BASELINE 阻塞项获得可执行方法论
- 剩余 pending：{pend}
"""
open(os.path.join(P, 'window_logs', 'analyst_2026-10-28.md'), 'a', encoding='utf-8').write(log)
print('log appended')
