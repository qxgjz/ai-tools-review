# -*- coding: utf-8 -*-
"""分析师 r27（21:00 档）：CTR 待办 + 竞品分析追加 + 关键词挖掘追加 + 待办写入"""
import json, os
from datetime import datetime

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
SP = os.path.join(P, 'iteration_center', 'state.json')
now = datetime.now().strftime('%Y-%m-%d %H:%M')
now_iso = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
d = json.load(open(SP, encoding='utf-8'))
nf = d['next_iteration_focus']
idx = {i.get('id'): i for i in nf}
added = []

# ============ 1. CTR 待办（基于新报告实读，3 条新） ============
ctr_items = [
    ('https://www.aitoolcrux.com/blog/best-ai-coding-tools-2026', '4.1', '0', '全站最高曝光 12 imp，排名第 4 仍 0 点击'),
    ('https://www.aitoolcrux.com/blog/best-ai-comparison-tools-2026/', '18.0', '0', '5-20 扩选范围'),
    ('QUERY: github copilot windsurf amazon q tabnine jetbrains ai pricing changes', '5.0', '0', '查询级，5 位 0 点击，长尾组合词'),
]
for url, pos, ctr, note in ctr_items:
    if url.startswith('QUERY:'):
        tid = 'CTR-QUERY-COPILOT-PRICING-20261025'
        task = f'查询 [{url.replace("QUERY: ","")}] 排名 {pos} 但 CTR 仅 {ctr}%，优化对应落地页 title/meta description 提升点击率'
    else:
        slug = url.rstrip('/').split('/')[-1][:36]
        tid = 'CTR-PAGE-' + slug.upper() + '-20261025'
        task = f'页面 {url} 排名 {pos} 但 CTR 仅 {ctr}%，优化 title/meta description 提升点击率'
    if tid not in idx:
        nf.append({'id': tid, 'status': 'pending', 'priority': 'P1',
                   'assigned_to': ['window5', '打磨师'], 'task': task,
                   'source': 'ctr_optimization_2026-10-25', 'created_at': now_iso,
                   'position': float(pos), 'ctr_pct': float(ctr), 'note': note})
        idx[tid] = nf[-1]; added.append(tid)

# ============ 2. 竞品分析追加（r27 段，保留 r26） ============
ca_add = f"""
---

## r27 追加（{now} · 21:00 档）

**数据源**：futurepedia 75 分类缓存（同 r26）+ 本地 40 篇 published 文章 + 5 词 SERP 实搜

### 本轮新缺口（5 个，避开 r26 已开单）
| 缺口分类 | futurepedia | 我们 | 建议选题 | 竞争度 | 前 10 竞品 |
|---|---|---|---|---|---|
| portrait-generators | 1 | 0 | best-ai-portrait-generators-2026 | High | DEV/Sozee/Slashdot/Habr |
| text-to-image | 1 | 0 | best-ai-text-to-image-generators-2026 | High | scored.tools/Pixo/TechSifted/AIRated/Dreamina/ToolChase |
| project-management | 1 | 0 | best-ai-project-management-tools-2026 | High | ClickUp/DigitalPM/TechRepublic/Productive/Slack |
| code-assistant | 1 | 0 | best-ai-coding-assistant-2026 | High | CodeTalentHub/DEV/DigitalTrends/Xataka |
| gift-ideas | 1 | 0 | best-ai-gift-idea-generators-2026 | Medium | ToolWorthy/GiftX/topai.tools/AIToolsGuidebook/Foundr |

### 可借鉴选题（5 个）
1. **Best AI Portrait Generators 2026**（best-ai-portrait-generators-2026）— High — 切入：免费额度矩阵（ProfileLoom 1张/Pixelbin 3张/Bing 15张）+ 商用安全（Firefly）
2. **Best AI Text-to-Image Generators 2026**（best-ai-text-to-image-generators-2026）— High — 切入：按需求分（文字渲染=Ideogram/艺术=Midjourney/商用=Firefly/开源=FLUX）+ 评分制
3. **Best AI Project Management Tools 2026**（best-ai-project-management-tools-2026）— High — 切入：按团队类型分（PMO=Monday/软件团队=Jira/预算=Productive/个人=Motion）+ 定价表
4. **Best AI Coding Assistant 2026**（best-ai-coding-assistant-2026）— High — 切入：按工作流分（IDE=Cursor/Copilot/终端=Claude Code/开源=OpenCode）+ 实测对比
5. **Best AI Gift Idea Generators 2026**（best-ai-gift-idea-generators-2026）— Medium — 切入：按流程分（发现=GiftX/会话=GiftList Genie/Amazon=SmartGiftAI/免账号=Giftruly）

### SERP 验证
- 5 词全部实搜，High×4 / Medium×1；权威域：ClickUp/TechRepublic/DigitalTrends
"""
ca_path = os.path.join(P, 'iteration_center', 'competitor_analysis_2026-10-25.md')
with open(ca_path, 'a', encoding='utf-8') as f:
    f.write(ca_add)
print('competitor_analysis appended:', len(ca_add.encode('utf-8')), 'bytes')

# ============ 3. 关键词挖掘追加（r27 段） ============
kw_add = f"""

---

## {now} 关键词挖掘 r27（21:00 档 · 与竞品分析同轮）

**Total keywords analyzed: 8**（P0×3 + P1×5）

### P0（SERP 已验证）
| 词 | 竞争度 | 建议标题 | slug |
|---|---|---|---|
| best AI portrait generators 2026 | High | Best AI Portrait Generators 2026: 9 Free & Paid Tested (ProfileLoom vs Pixelbin vs Firefly) | best-ai-portrait-generators-2026 |
| best AI project management tools 2026 | High | Best AI Project Management Tools 2026: 10 Tested (ClickUp vs Monday vs Asana) | best-ai-project-management-tools-2026 |
| best AI coding assistant 2026 | High | Best AI Coding Assistant 2026: 7 Tested (Cursor vs Copilot vs Claude Code vs OpenCode) | best-ai-coding-assistant-2026 |

### P1
| 词 | 竞争度(估) | 建议标题 | slug |
|---|---|---|---|
| best AI text-to-image generators 2026 | High | Best AI Text-to-Image Generators 2026: 8 Tested (Ideogram vs Midjourney vs FLUX) | best-ai-text-to-image-generators-2026 |
| best AI gift idea generators 2026 | Medium | Best AI Gift Idea Generators 2026: 7 Tested (GiftX vs Giftruly vs SmartGiftAI) | best-ai-gift-idea-generators-2026 |
| best AI 3D generator tools 2026 | Medium | Best AI 3D Generator Tools 2026: 7 Tested | best-ai-3d-generator-tools-2026 |
| best AI churn prediction tools 2026 | Medium | Best AI Churn Prediction Tools 2026: 6 Tested | best-ai-churn-prediction-tools-2026 |
| best AI fun tools 2026 | Low | Best AI Fun Tools 2026: 12 Tested | best-ai-fun-tools-2026 |

### 搜索量标注（"预估"）
| 词 | 搜索量 | 依据 |
|---|---|---|
| portrait / project-mgmt / coding-assistant | 预估高 | SERP 5-6 站竞争 High（ClickUp/TechRepublic/DigitalTrends 权威域） |
| text-to-image / gift | 预估中-高 | SERP 验证 High/Medium |
| 3D / churn / fun | 预估中 | futurepedia 分类缺口依据，未实搜 |
"""
kw_path = os.path.join(P, 'iteration_center', 'keyword_opportunities.md')
with open(kw_path, 'a', encoding='utf-8') as f:
    f.write(kw_add)
print('keyword_opportunities appended:', len(kw_add.encode('utf-8')), 'bytes')

# ============ 4. 待办写入（CA 5 + KW 8） ============
comp_todos = [
    {'id': 'CA-PORTRAIT-GENERATORS-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P1',
     'task': '竞品 futurepedia 在做 portrait-generators 内容（竞品有 1 个分类，我们 0 个），建议写 best-ai-portrait-generators-2026 文章（ProfileLoom/Pixelbin/Firefly 对比），SERP竞争度=High',
     'source': 'competitor_analysis_2026-10-25', 'serp_competition': 'High', 'data_verified': True, 'competitor_count': 1, 'our_count': 0},
    {'id': 'CA-TEXT-TO-IMAGE-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P1',
     'task': '竞品 futurepedia 在做 text-to-image 内容（竞品有 1 个分类，我们 0 个），建议写 best-ai-text-to-image-generators-2026 文章（Ideogram/Midjourney/FLUX 对比），SERP竞争度=High',
     'source': 'competitor_analysis_2026-10-25', 'serp_competition': 'High', 'data_verified': True, 'competitor_count': 1, 'our_count': 0},
    {'id': 'CA-PROJECT-MANAGEMENT-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P1',
     'task': '竞品 futurepedia 在做 project-management 内容（竞品有 1 个分类，我们 0 个），建议写 best-ai-project-management-tools-2026 文章（ClickUp/Monday/Asana 对比），SERP竞争度=High',
     'source': 'competitor_analysis_2026-10-25', 'serp_competition': 'High', 'data_verified': True, 'competitor_count': 1, 'our_count': 0},
    {'id': 'CA-CODE-ASSISTANT-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P1',
     'task': '竞品 futurepedia 在做 code-assistant 内容（竞品有 1 个分类，我们 0 个），建议写 best-ai-coding-assistant-2026 文章（Cursor/Copilot/Claude Code 对比），SERP竞争度=High',
     'source': 'competitor_analysis_2026-10-25', 'serp_competition': 'High', 'data_verified': True, 'competitor_count': 1, 'our_count': 0},
    {'id': 'CA-GIFT-IDEAS-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P1',
     'task': '竞品 futurepedia 在做 gift-ideas 内容（竞品有 1 个分类，我们 0 个），建议写 best-ai-gift-idea-generators-2026 文章（GiftX/Giftruly/SmartGiftAI 对比），SERP竞争度=Medium',
     'source': 'competitor_analysis_2026-10-25', 'serp_competition': 'Medium', 'data_verified': True, 'competitor_count': 1, 'our_count': 0},
]
kw_todos = [
    {'id': 'KW-PORTRAIT-GENERATORS-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P0',
     'task': '基于关键词 [best AI portrait generators 2026] 写 2000 字新文章，标题建议 [Best AI Portrait Generators 2026: 9 Free & Paid Tested]，slug 建议 [best-ai-portrait-generators-2026]',
     'source': 'keyword_mining_2026-10-25', 'serp_competition': 'High', 'serp_verified': True,
     'our_angle': '免费额度矩阵（ProfileLoom 1张/Pixelbin 3张/Bing 15张）+ 商用安全（Firefly）'},
    {'id': 'KW-PROJECT-MANAGEMENT-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P0',
     'task': '基于关键词 [best AI project management tools 2026] 写 2000 字新文章，标题建议 [Best AI Project Management Tools 2026: 10 Tested]，slug 建议 [best-ai-project-management-tools-2026]',
     'source': 'keyword_mining_2026-10-25', 'serp_competition': 'High', 'serp_verified': True,
     'our_angle': '按团队类型分（PMO=Monday/软件=Jira/预算=Productive/个人=Motion）+ 定价表'},
    {'id': 'KW-CODING-ASSISTANT-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P0',
     'task': '基于关键词 [best AI coding assistant 2026] 写 2000 字新文章，标题建议 [Best AI Coding Assistant 2026: 7 Tested]，slug 建议 [best-ai-coding-assistant-2026]',
     'source': 'keyword_mining_2026-10-25', 'serp_competition': 'High', 'serp_verified': True,
     'our_angle': '按工作流分（IDE=Cursor/Copilot/终端=Claude Code/开源=OpenCode）+ 实测对比'},
    {'id': 'KW-TEXT-TO-IMAGE-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P1',
     'task': '基于关键词 [best AI text-to-image generators 2026] 写 2000 字新文章，标题建议 [Best AI Text-to-Image Generators 2026: 8 Tested]，slug 建议 [best-ai-text-to-image-generators-2026]',
     'source': 'keyword_mining_2026-10-25', 'serp_competition': 'High'},
    {'id': 'KW-GIFT-IDEAS-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P1',
     'task': '基于关键词 [best AI gift idea generators 2026] 写 2000 字新文章，标题建议 [Best AI Gift Idea Generators 2026: 7 Tested]，slug 建议 [best-ai-gift-idea-generators-2026]',
     'source': 'keyword_mining_2026-10-25', 'serp_competition': 'Medium'},
    {'id': 'KW-3D-GENERATOR-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P1',
     'task': '基于关键词 [best AI 3D generator tools 2026] 写 2000 字新文章，标题建议 [Best AI 3D Generator Tools 2026: 7 Tested]，slug 建议 [best-ai-3d-generator-tools-2026]',
     'source': 'keyword_mining_2026-10-25', 'serp_competition': 'Medium'},
    {'id': 'KW-CHURN-PREDICTION-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P1',
     'task': '基于关键词 [best AI churn prediction tools 2026] 写 2000 字新文章，标题建议 [Best AI Churn Prediction Tools 2026: 6 Tested]，slug 建议 [best-ai-churn-prediction-tools-2026]',
     'source': 'keyword_mining_2026-10-25', 'serp_competition': 'Medium'},
    {'id': 'KW-FUN-TOOLS-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P1',
     'task': '基于关键词 [best AI fun tools 2026] 写 2000 字新文章，标题建议 [Best AI Fun Tools 2026: 12 Tested]，slug 建议 [best-ai-fun-tools-2026]',
     'source': 'keyword_mining_2026-10-25', 'serp_competition': 'Low'},
]
for t in comp_todos + kw_todos:
    if t['id'] not in idx:
        t.update({'status': 'pending', 'created_at': now_iso})
        nf.append(t); idx[t['id']] = t; added.append(t['id'])

d['next_iteration_focus'] = nf
d['last_update'] = now_iso
json.dump(d, open(SP, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('added todos:', added)
print('focus:', len(nf))
