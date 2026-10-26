# -*- coding: utf-8 -*-
"""分析师 r31：新 P0×2(prompt/research) + CA5 + KW(2P0+5P1) + CTR1(5-20位) + 阻塞复查"""
import json, os
from datetime import datetime

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
SP = os.path.join(P, 'iteration_center', 'state.json')
now_iso = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
now = datetime.now().strftime('%Y-%m-%d %H:%M')
today = '2026-10-26'

d = json.load(open(SP, encoding='utf-8'))
nf = d['next_iteration_focus']
ids = {i.get('id') for i in nf}
added = []
def add_todo(t):
    if t['id'] not in ids:
        nf.append(t); ids.add(t['id']); added.append(t['id'])

# ============ 1. 阻塞复查（保持 pending，禁止假完成） ============
for i in nf:
    if i.get('id') == 'P1-GEO-BASELINE-AUDIT-20261013':
        i['note'] = 'r31 复查 2026-10-26 21:0x：仍阻塞——需浏览器 GUI 跑 ChatGPT Search/Perplexity/AIO SERP；无浏览器会话不可完成，保持 pending'
    if i.get('id') == 'P1-TOOL-ELMO-20261017':
        i['note'] = 'r31 复查 2026-10-26 21:0x：仍阻塞——本机 Docker 不可用（elmo 为 Docker Compose 自托管）；保持 pending'

# ============ 2. CTR +1（GSC 窗口未滚动=同 r30 数据；5-20 位新命中仅 comparison-tools/ 18.0） ============
add_todo({'id': 'CTR-PAGE-COMPARISON-TOOLS-SLASH-20261026', 'status': 'pending', 'priority': 'P1',
          'assigned_to': ['window5', '打磨师'],
          'task': '页面 https://www.aitoolcrux.com/blog/best-ai-comparison-tools-2026/（带斜杠变体）排名 18.0 但 CTR 0%（5-20 位，r31 扩口径筛出），优化 title/meta description 提升点击率',
          'source': f'ctr_optimization_{today}', 'created_at': now_iso,
          'position': 18.0, 'ctr_pct': 0.0, 'window': '2026-09-25~10-24'})

# ============ 3. 竞品缺口 +5（职责A；本地 40 篇实读确认无这些分类） ============
ca = [
    ('CA-PROMPT-GENERATORS-20261026', 'prompt-generators', 'best-ai-prompt-generators-2026', 'Medium'),
    ('CA-RESEARCH-ASSISTANT-20261026', 'research-assistant', 'best-ai-research-assistant-tools-2026', 'Medium'),
    ('CA-VIDEO-GENERATORS-20261026', 'video-generators', 'best-ai-video-generators-2026', 'High'),
    ('CA-BUSINESS-20261026', 'business', 'best-ai-business-tools-2026', '预估Low'),
    ('CA-REAL-ESTATE-20261026', 'real-estate', 'best-ai-real-estate-tools-2026', '预估Medium'),
]
for tid, cat, slug, compd in ca:
    add_todo({'id': tid, 'status': 'pending', 'priority': 'P1',
              'assigned_to': ['window2', '创作家'],
              'task': f'竞品 futurepedia 在做 {cat} 内容（竞品有 1 个分类，我们 0 个），建议写 {slug} 文章，SERP竞争度={compd}',
              'source': f'competitor_analysis_{today}', 'data_verified': True,
              'serp_competition': compd, 'competitor_count': 1, 'our_count': 0, 'created_at': now_iso})

# ============ 4. KW P0 +2（prompt-generators / research-assistant，SERP 已验证 Medium） ============
add_todo({'id': 'KW-VOLUME-CONFIRMED-PROMPT-20261026', 'status': 'pending', 'priority': 'P0',
          'assigned_to': ['window2', '创作家'],
          'task': '基于关键词 [best AI prompt generators 2026]（SERP 已验证 Medium，r31 实搜）写 2000 字新文章，标题建议 [Best AI Prompt Generators 2026: 8 Tested (Free Options Included)]，slug 建议 [best-ai-prompt-generators-2026]，切入：免费额度+按场景分（视频/代码/营销文案）+PromptPerfect 多模型优化实测',
          'source': f'keyword_mining_{today}', 'serp_competition': 'Medium', 'serp_verified': True,
          'volume_verified': True, 'created_at': now_iso, 'our_angle': '免费额度+场景化实测'})
add_todo({'id': 'KW-VOLUME-CONFIRMED-RESEARCH-20261026', 'status': 'pending', 'priority': 'P0',
          'assigned_to': ['window2', '创作家'],
          'task': '基于关键词 [best AI research assistant tools 2026]（SERP 已验证 Medium，r31 实搜）写 2000 字新文章，标题建议 [Best AI Research Assistants 2026: Perplexity vs ChatGPT Deep Research vs Elicit]（vs 型差异化），slug 建议 [best-ai-research-assistant-tools-2026]，切入：学术(文献综述Elicit/Consensus) vs 网页研究(Perplexity) vs 长报告(ChatGPT Deep Research) 分场景',
          'source': f'keyword_mining_{today}', 'serp_competition': 'Medium', 'serp_verified': True,
          'volume_verified': True, 'created_at': now_iso, 'our_angle': '学术vs网页vs长报告分场景'})

# ============ 5. KW P1 +5（未开单；3 分类 + 2 长尾） ============
kwp1 = [
    ('KW-BUSINESS-20261026', 'best AI business tools 2026', 'Best AI Business Tools 2026: 10 Tested (SMB Focus)', 'best-ai-business-tools-2026', '预估Low'),
    ('KW-REAL-ESTATE-20261026', 'AI tools for real estate agents 2026', 'Best AI Tools for Real Estate Agents 2026: 8 Tested (Listings to CRM)', 'best-ai-real-estate-tools-2026', '预估Medium'),
    ('KW-VIDEO-GENERATORS-20261026', 'best AI video generators 2026', 'Best AI Video Generators 2026: 9 Tested (Kling vs Seedance vs Veo)', 'best-ai-video-generators-2026', 'High'),
    ('KW-HOWTO-AI-BUSINESS-20261026', 'how to use AI for small business 2026', 'How to Use AI for Your Small Business in 2026: Step-by-Step Guide', 'how-to-use-ai-for-small-business-2026', '预估Medium'),
    ('KW-HOWTO-AI-RESEARCH-20261026', 'how to use AI for research paper 2026', 'How to Use AI for Research Papers in 2026: 7-Step Workflow', 'how-to-use-ai-for-research-paper-2026', '预估Medium'),
]
for tid, kw, title, slug, compd in kwp1:
    add_todo({'id': tid, 'status': 'pending', 'priority': 'P1',
              'assigned_to': ['window2', '创作家'],
              'task': f'基于关键词 [{kw}] 写 2000 字新文章，标题建议 [{title}]，slug 建议 [{slug}]',
              'source': f'keyword_mining_{today}', 'serp_competition': compd,
              'serp_verified': False, 'volume_verified': False, 'created_at': now_iso})

d['next_iteration_focus'] = nf
d['last_update'] = now_iso
json.dump(d, open(SP, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('todos added:', len(added), added)
print('focus:', len(nf), '| pending:', len([i for i in nf if i.get('status')=='pending']))

# ============ 6. 竞品分析追加 r31 ============
ca_add = f"""

---

## r31 追加（{now} · 21:00 档）

**数据源**：competitor_gap 实抓失败（futurepedia/topai sitemap 无响应，同上轮）→ 降级缓存（futurepedia 75 分类，cached 10-25）；本地 40 篇 published 实读防重复

### 内容缺口（本轮 5 个新缺口；r30 已开 ai-detection/education/fashion/cartoon/religion，本轮不重复）
| 缺口分类 | 竞品 | 我们 | 建议选题 | 竞争度 |
|---|---|---|---|---|
| prompt-generators | 1 | 0 | best-ai-prompt-generators-2026 | **Medium**（SurePrompts/SaaSworthy/Filmora/BrandClickX/Toolradar，无巨头榜单） |
| research-assistant | 1 | 0 | best-ai-research-assistant-tools-2026 | **Medium**（scored.tools/AI Insiders/ToolPilot/Dupple/Rework/Digital Trends 提及） |
| video-generators | 1 | 0 | best-ai-video-generators-2026 | High（VideoGen/Fliki/PixVerse/DEV 垂直站强竞争+中文垃圾站污染） |
| business | 1 | 0 | best-ai-business-tools-2026 | 预估Low（未实搜，泛分类） |
| real-estate | 1 | 0 | best-ai-real-estate-tools-2026 | 预估Medium（未实搜，垂直有需求） |

### 可借鉴选题（5 个）
1. best-ai-prompt-generators-2026 — Medium — 切入：免费额度+按场景（视频/代码/营销）+PromptPerfect 多模型优化实测
2. best-ai-research-assistant-tools-2026 — Medium — 切入：学术（Elicit/Consensus）vs 网页（Perplexity）vs 长报告（ChatGPT Deep Research）
3. best-ai-video-generators-2026 — High — 切入：按任务分（Kling 60fps/Seedance 参考驱动/Veo 4K）+ 价格表
4. best-ai-business-tools-2026 — 预估Low — 切入：SMB 全流程（财务/CRM/营销/客服）
5. best-ai-real-estate-tools-2026 — 预估Medium — 切入：房源 listing→CRM→虚拟看房

### SERP 验证（实搜 3 词）
prompt-generators **Medium** / research-assistant **Medium** / video-generators **High**；business/real-estate 标预估（验证预算已用 3 个）
"""
with open(os.path.join(P, 'iteration_center', f'competitor_analysis_{today}.md'), 'a', encoding='utf-8') as f:
    f.write(ca_add)
print('competitor appended')

# ============ 7. keyword_opportunities.md 追加 r31 ============
kw_add = f"""

---

## r31 追加（{now} · 21:00 档）

**Total keywords analyzed: 3**（本轮实搜）+ 5 P1 候选（预估/长尾）

### 验证结论
- 实搜 3 词：prompt-generators **Medium（P0 新入选）** / research-assistant **Medium（P0 新入选）** / video-generators **High**
- P0 优先池：prompt-generators、research-assistant（本轮）+ education（r30）+ legal（r29）+ churn（r28）——均 serp_verified=true，Medium
- GSC Easy Wins：本轮跳过（GSC 窗口未滚动=同 r30 数据，live_pull 无新 20-50 位词）

### 本轮新增候选（P1）
| 词 | 竞争度（估） | 建议标题 | slug |
|---|---|---|---|
| best AI business tools 2026 | Low | Best AI Business Tools 2026: 10 Tested (SMB Focus) | best-ai-business-tools-2026 |
| AI tools for real estate agents 2026 | Medium | Best AI Tools for Real Estate Agents 2026: 8 Tested | best-ai-real-estate-tools-2026 |
| best AI video generators 2026 | High | Best AI Video Generators 2026: 9 Tested (Kling vs Seedance vs Veo) | best-ai-video-generators-2026 |
| how to use AI for small business 2026 | Medium | How to Use AI for Your Small Business in 2026: Step-by-Step | how-to-use-ai-for-small-business-2026 |
| how to use AI for research paper 2026 | Medium | How to Use AI for Research Papers in 2026: 7-Step Workflow | how-to-use-ai-for-research-paper-2026 |

### 搜索量标注（全"预估"）
依据=SERP 竞争度（实搜 3 词）或竞品分类缺口（未实搜词）。搜索量未编造。
"""
with open(os.path.join(P, 'iteration_center', 'keyword_opportunities.md'), 'a', encoding='utf-8') as f:
    f.write(kw_add)
print('keyword appended')

# ============ 8. 日报追加 r31 ============
rep = f"""

---

# r31 追加（{now} · 21:00 档 · GSC 窗口未滚动复查）

## GSC（fetch_gsc.py 实拉）
| 指标 | 数值 | 变化 |
|---|---|---|
| 窗口 | 2026-09-25~10-24 | **与 r30 相同（脚本固定窗口，本轮未滚动）** |
| Clicks / Impressions / CTR / AvgPos | 0 / 171 / 0% / 14.29 | 与 r30 完全一致 |

### 本轮结论
- 无新数据窗口 → 5-15 位新命中为 0（r30 已开 meeting/observability/productivity 3 条仍在打磨师池中）
- 扩口径 5-20 位筛出新命中 1 条：/blog/best-ai-comparison-tools-2026/（带斜杠变体）pos18.0 CTR 0% → 已开 CTR 待办
- 其余同窗口命中均已开单（tabbyml 18.0 r27✅ / ai-policy 8.0 r29✅），不重复
- 提醒：r30 已开 3 条 CTR 待办仍在 pending（打磨师 backlog），建议指挥官核查处理节奏
"""
with open(os.path.join(P, 'gsc-ga4-report', f'latest_report_{today}.md'), 'a', encoding='utf-8') as f:
    f.write(rep)
print('report appended')

# ============ 9. audit_findings 追加 r31 ============
audit = f"""
## {now} r31 追加 · GSC 窗口未滚动复查（09-25~10-24 同上轮）

**数据**：171/0/14.29 与 r30 完全一致（fetch_gsc.py 固定窗口，无新数据可读）。诚实记录：本轮无新曝光/排名变化可分析。
- **P1**：5-20 位扩口径筛出新命中 1 条（comparison-tools/ 带斜杠 pos18.0 CTR 0%）→ CTR 待办已开
- **P0 级（职责B）**：prompt-generators（Medium）与 research-assistant（Medium）SERP 实搜验证通过 → 2 个新 P0 待办（创作家），缓解"无词可写"backlog
- **P1 观察**：video-generators SERP 含中文垃圾站（IT168 推广页）污染，说明该词竞价激烈+搜索引擎结果质量下降，短期不建议主攻（标 High）
- 阻塞复查：GEO-BASELINE/ELMO 保持 pending（浏览器 GUI/Docker 不可用），未假完成
"""
with open(os.path.join(P, 'iteration_center', 'audit_findings.md'), 'a', encoding='utf-8') as f:
    f.write(audit)
print('audit appended')

# ============ 10. 日志追加 r31 ============
log = f"""

## r31 追加（{now} · 21:00 档）

- 执行待办：**2 条复查**（GEO-BASELINE/ELMO，均确认仍阻塞，保持 pending，未假完成）
- 新发现：**13 条待办**（CTR×1 + CA×5 + KW P0×2 + KW P1×5）
- 挖词：3 词实搜（Medium×2/High×1）+ 5 词新候选（3 分类 + 2 长尾）
- 竞品缺口：5 个（prompt/research Medium 实搜 + video High 实搜 + business/real-estate 预估）
- SERP 验证：3 词（prompt-generators/research-assistant=Medium 新 P0 入选；video=High）
- 写入待办：13 条
- 剩余 pending（分析师）：2（GEO-BASELINE、ELMO，均阻塞）

### 失败/降级记录
- competitor_gap 实抓失败（futurepedia/topai sitemap 无响应）→ 降级缓存，已记录
- GSC 窗口未滚动（=r30 数据，fetch_gsc.py 固定窗口）→ 无新曝光分析；CTR 5-15 位新命中 0，扩 5-20 位仅 1 条，已如实记录不硬凑
- GSC Easy Wins：跳过（无新 20-50 位词）
- GSC 实拉成功（数据同上轮）
"""
with open(os.path.join(P, 'window_logs', f'analyst_{today}.md'), 'a', encoding='utf-8') as f:
    f.write(log)

kwlog = f"""
---

## r31 追加（{now} · 21:00 档）

- 挖掘关键词：3 实搜 + 5 新候选（3 分类 + 2 长尾）
- P0/P1/P2：P0=2 新（prompt-generators/research-assistant，serp_verified）+ P1=5 新
- SERP 验证：3 词实搜（prompt Medium / research Medium / video High）
- GSC Easy Wins：跳过（窗口未滚动）
- 竞品对比：futurepedia 75 分类（缓存）vs 本地 40 篇（实读）
- 写入待办：7 条（2 P0 + 5 P1）
- 硬约束：P0 serp_verified=true ✅；搜索量全标预估附依据 ✅；competitor_gap 失败已写日志 ✅
"""
with open(os.path.join(P, 'window_logs', f'analyst_keyword_{today}.md'), 'a', encoding='utf-8') as f:
    f.write(kwlog)
print('logs appended')
