# -*- coding: utf-8 -*-
"""r38 收尾：闭环 AI-OVERVIEWS-BASELINE + CTR 待办 + audit/KW/competitor 追加 + 日志"""
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

# ===== ① 闭环 P1-AI-OVERVIEWS-BASELINE-20261028（CDP 实读证据） =====
closed = []
for t in nf:
    if t.get('id') == 'P1-AI-OVERVIEWS-BASELINE-20261028' and t.get('status') != 'completed':
        t['status'] = 'completed'
        t['completed_at'] = now_iso
        t['evidence'] = ('AdsPower CDP 实读 GSC Generative AI 报告（2026-08-31~10-25，URL=.../performance/search-analytics/ai）：'
                         'AI 总曝光 8 次；top 网页 suno-review-2026(3)/gemini_38_flash_review(2)/首页(1)/cursor-review-2026(1)/tools-knowledge(1)。'
                         'GEO/AEO 品牌可见性基线建立：8 次 AI 展示，suno 评测最高。另 UI 全量查询 281 行含真实点击 best voice changer 2026=1clk。')
        closed.append('P1-AI-OVERVIEWS-BASELINE-20261028')
# GEO-BASELINE/ELMO 保持 pending（真实阻塞：需 ChatGPT/Perplexity 账号登录态；需 Docker）
for t in nf:
    if t.get('id') in ('P1-GEO-BASELINE-AUDIT-20261013', 'P1-TOOL-ELMO-20261017'):
        t['blocker_note'] = 'r38 复核：AdsPower 无 ChatGPT/Perplexity 登录态，无法 GUI 跑四引擎；ELMO 需本机 Docker（不可用）。保持 pending。'

# ===== ② CTR 待办（最新 GSC 窗口 09-27~10-26，5-15 位 CTR<3%） =====
add_todo({'id': 'CTR-PAGE-MEETING-ASSISTANTS-20261028', 'status': 'pending', 'priority': 'P1',
          'assigned_to': ['window5', '打磨师'],
          'task': '页面 https://www.aitoolcrux.com/blog/best-ai-meeting-assistants-2026 排名 9.0 但 CTR 仅 0%（imp 1），优化 title/meta description 提升点击率',
          'source': f'ctr_optimization_{today}', 'data_verified': True, 'created_date': today})
add_todo({'id': 'CTR-PAGE-OBSERVABILITY-20261028', 'status': 'pending', 'priority': 'P1',
          'assigned_to': ['window5', '打磨师'],
          'task': '页面 https://www.aitoolcrux.com/blog/best-ai-observability-tools-2026 排名 9.5 但 CTR 仅 0%（imp 2），优化 title/meta description 提升点击率',
          'source': f'ctr_optimization_{today}', 'data_verified': True, 'created_date': today})
add_todo({'id': 'CTR-PAGE-PRODUCTIVITY-20261028', 'status': 'pending', 'priority': 'P1',
          'assigned_to': ['window5', '打磨师'],
          'task': '页面 https://www.aitoolcrux.com/blog/best-ai-productivity-tools-2026 排名 10.5 但 CTR 仅 0%（imp 2），优化 title/meta description 提升点击率',
          'source': f'ctr_optimization_{today}', 'data_verified': True, 'created_date': today})

# ===== ③ 新发现补录待办 =====
add_todo({'id': 'P0-EXPOSURE-CLIFF-20261028', 'status': 'pending', 'priority': 'P0',
          'assigned_to': ['window1', '架构师'],
          'task': 'GSC 曝光断崖核查：fetch_gsc 双窗口实拉 2008 imp(08-29~09-26) → 170 imp(09-27~10-26) 即 -91.5%；日均从 2008/30≈67 降至 170/30≈6。时间点与 article-api-* 时间戳 URL/auto_redirect 94 暴增（r33）吻合，疑似索引质量信号受损。核查 9 月下旬变更（批量 URL 上线/redirect 配置）并给出恢复方案。',
          'source': f'gsc_analysis_{today}', 'data_verified': True, 'created_date': today})
add_todo({'id': 'P1-MOBILE-EXPOSURE-20261028', 'status': 'pending', 'priority': 'P1',
          'assigned_to': ['window1', '架构师'],
          'task': '移动端曝光异常低：GSC 最新窗口 MOBILE 仅 4/170 imp（2.4%），DESKTOP 166。移动端收录/展示需核查（RWD 配置、viewport、Core Web Vitals 移动得分）。',
          'source': f'gsc_analysis_{today}', 'data_verified': True, 'created_date': today})

d['next_iteration_focus'] = nf
d['last_update'] = now_iso
json.dump(d, open(state_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
pend = len([i for i in nf if i.get('status') == 'pending'])
print('closed:', closed)
print('added:', added)
print('focus:', len(nf), '| pending:', pend)

# ===== ④ competitor_analysis 追加（实抓复核） =====
ca_file = os.path.join(P, 'iteration_center', f'competitor_analysis_{today}.md')
open(ca_file, 'a', encoding='utf-8').write("""

## r38 复核（09:3x · 代理恢复后实抓）
- **实抓成功**：requests+浏览器 UA+7890 直抓 futurepedia sitemap（200/635 URLs）→ **72 分类**（10-25 缓存为 75，差异 3 个=分类下线或 slug 变更，已按实抓更新缓存，source=live_fetch_20261028_requests_ua）
- **缺口复核**：72 分类 vs 本地 237 md → 23 个缺口，与 r37 清单一致；copywriting-assistant 与 text-generators 工具重叠不重复开；video-editing 与本地视频类内容疑似覆盖不重复开
- **结论**：r37 已开 5 个 CA（ecommerce/text-generators/chatbot-builders/design-generators/ticketing）在池未动，本轮无新缺口待办（避免待办池膨胀）
- topai.tools sitemap 持续 404（第 N 次确认，死路）
""")
print('competitor_analysis appended')

# ===== ⑤ keyword_opportunities 追加 =====
ko = os.path.join(P, 'iteration_center', 'keyword_opportunities.md')
open(ko, 'a', encoding='utf-8').write("""

## r38（2026-10-28 09:3x · GSC 全量查询 + Generative AI 基线档）

> 数据来源：AdsPower CDP 实读 GSC Performance UI（8/31~10/25 全量 281 查询）+ fetch_gsc 双窗口实拉。

### 曝光断崖（P0 信号）
| 窗口 | Impressions | 日均 |
|---|---|---|
| 08-29 ~ 09-26（prev） | 2008 | ~67 |
| 09-27 ~ 10-26（cur） | 170 | ~6 |
| 变化 | **-91.5%** | — |

### 正向信号
| 查询 | Clicks | Impressions | 意义 |
|---|---|---|---|
| best voice changer 2026 | **1** | 1 | 全站唯一真实点击（8/31~10/25 窗口），评测类长尾开始出结果 |
| ai observability tools | 0 | 17 | 已有曝光，pos 9.5，需 CTR 优化 |
| ai tool comparison / ai comparison tools / ai tool compare | 0 | 31+13+10 | 对比类需求合计 54 曝光 |

### Generative AI 基线（GEO/AEO 首建，2026-08-31~10-25）
AI 功能总曝光 **8 次**：suno-review-2026(3) / gemini_38_flash_review(2) / 首页(1) / cursor-review-2026(1) / tools-knowledge(1)。
→ GEO 策略验证点：suno/gemini/cursor 评测文已被 AI 引用，与 Proof Ledger 词库（音乐/语音/对比类）方向一致。

### 结论
Total keywords analyzed: 本轮新增 0 个 P0/P1 候选（Easy Wins=0：排名 20-50 有曝光词 0 个，诚实跳过）；累计 SERP 验证词 70+。
""")
print('keyword_opportunities appended')

# ===== ⑥ audit_findings 追加 =====
af = os.path.join(P, 'iteration_center', 'audit_findings.md')
open(af, 'a', encoding='utf-8').write(f"""

## r38（2026-10-28 09:3x · 代理恢复后 GSC 实拉 + Generative AI 基线）

### P0: 曝光断崖 -91.5%（2008 → 170 imp）
- 双窗口实拉（fetch_gsc.py）：prev 08-29~09-26=2008 imp，cur 09-27~10-26=170 imp
- 与 r33 auto_redirect 9→94 暴增时间吻合（9 月下旬），联动 P0-EXPOSURE-CLIFF-20261028（架构师）
- 10 月日均 1-7 imp，低位持续 30 天

### P1: 移动端曝光 2.4%（4/170 imp）
- 移动端几乎无展示，桌面 166。需核查 RWD/viewport/CWV 移动指标（P1-MOBILE-EXPOSURE-20261028）

### P1: article-api-* 污染 URL 持续
- 最新窗口 article-api-20260903(4 imp, pos3.2) + article-api-20260904(1 imp, pos6.0) 仍在 GSC 页面列表
- 持续消耗抓取配额，关联 AUTO-REDIRECT-SPIKE-20261027（r33，架构师 P0 在池）

### 新低 CTR 页面（3 条已开打磨师单）
- best-ai-meeting-assistants-2026 pos9.0 / observability pos9.5 / productivity pos10.5，全 0%

### 已闭环: AI-OVERVIEWS-BASELINE（Generative AI 基线 8 曝光）
- CDP 实读（见 state.json evidence）：suno(3)/gemini(2)/首页(1)/cursor(1)/tools-knowledge(1)
""")
print('audit_findings appended')

# ===== ⑦ 日志 =====
log1 = f"""

## r38（{today} 09:3x · 分析师-数据洞察 SOP 触发·代理恢复档）

- 执行待办：**1 条闭环**（P1-AI-OVERVIEWS-BASELINE-20261028，CDP 实读 Generative AI 报告，基线 8 曝光）；阻塞保持 2（GEO-BASELINE 需 ChatGPT/Perplexity 登录态、ELMO 需 Docker）——analyst pending 仅 3 条，无虚构凑数
- 新发现：4 条（**P0 曝光断崖 2008→170 -91.5%**、P1 移动端 2.4%、P1 article-api 污染持续、Generative AI 基线 8 曝光）
- 挖词：0 个新 P0/P1（Easy Wins=0 诚实跳过）；GSC UI 全量 281 查询实读，正向信号 best voice changer 2026=1clk
- 竞品缺口：23 个复核（实抓 72 分类/635 URLs 更新缓存），无新缺口
- SERP 验证：0（本轮无新候选词）
- CTR 待办：3 条（meeting pos9.0 / observability pos9.5 / productivity pos10.5）
- 写入待办：5 条（CTR×3 + P0-EXPOSURE-CLIFF + P1-MOBILE-EXPOSURE）
- 剩余 pending：{pend}
- 成功记录：GSC 实拉 ✅（170 imp 新窗口）、competitor 实抓 ✅（requests UA）、AI-OVERVIEWS-BASELINE ✅（CDP）
"""
open(os.path.join(P, 'window_logs', f'analyst_{today}.md'), 'a', encoding='utf-8').write(log1)
print('logs appended')
print('DONE')
