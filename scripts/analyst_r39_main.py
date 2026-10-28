# -*- coding: utf-8 -*-
"""r39 收尾：CTR x3 + CA x3（教程型缺口）+ 产出追加 + 日志"""
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

# ===== CTR 待办（最新 GSC 09-27~10-26：188 imp，5-15 位 CTR<3%） =====
add_todo({'id': 'CTR-PAGE-GUIDE-20261028', 'status': 'pending', 'priority': 'P1',
          'assigned_to': ['window5', '打磨师'],
          'task': '页面 https://www.aitoolcrux.com/blog/ai-tools-review-guide-2026/ 排名 10.0 但 CTR 仅 0%（imp 1），优化 title/meta description 提升点击率',
          'source': f'ctr_optimization_{today}', 'data_verified': True, 'created_date': today})
add_todo({'id': 'CTR-PAGE-COMPARISON-TOOLS-20261028', 'status': 'pending', 'priority': 'P1',
          'assigned_to': ['window5', '打磨师'],
          'task': '页面 https://www.aitoolcrux.com/blog/best-ai-comparison-tools-2026/ 排名 18.0 但 CTR 仅 0%（imp 1，5-20 扩大范围），优化 title/meta description 提升点击率',
          'source': f'ctr_optimization_{today}', 'data_verified': True, 'created_date': today})
add_todo({'id': 'CTR-PAGE-CODING-TOOLS-20261028', 'status': 'pending', 'priority': 'P1',
          'assigned_to': ['window5', '打磨师'],
          'task': '页面 https://www.aitoolcrux.com/blog/best-ai-coding-tools-2026 排名 4.1 但 CTR 仅 0%（imp 12=全站最大曝光页，首页边缘位，扩展依据），优化 title/meta description 提升点击率',
          'source': f'ctr_optimization_{today}', 'data_verified': True, 'created_date': today})

# ===== 职责A：CA 待办（竞品实抓 77 分类/531 courses + SERP 验证） =====
add_todo({'id': 'CA-TOOLS-TUTORIAL-20261028', 'status': 'pending', 'priority': 'P1',
          'assigned_to': ['window2', '创作家'],
          'task': '竞品 futurepedia 在做 AI 教程型内容（courses 531 URLs/learning-paths 3，我们 0 个分类），建议写 "AI Tools Tutorial for Beginners: 10 Free Tools You Can Master Today" 文章（slug: ai-tools-tutorial-beginners），SERP竞争度=Medium（general_search 实搜已验证：前 10 含 ai4everyone.ai 独立站）',
          'source': f'competitor_analysis_{today}', 'data_verified': True, 'created_date': today})
add_todo({'id': 'CA-FREE-AI-COURSES-20261028', 'status': 'pending', 'priority': 'P1',
          'assigned_to': ['window2', '创作家'],
          'task': '竞品 futurepedia 在卖 AI 课程（courses 531 URLs，变现=课程主导），我们 0 个课程类内容，建议写 "Best Free AI Courses in 2026: 15 Certified Resources" 文章（slug: best-free-ai-courses-2026，切入=独立测评+资源地图差异化），SERP竞争度=High（前 10 被 DataCamp/MIT/Coursera 垄断）',
          'source': f'competitor_analysis_{today}', 'data_verified': True, 'created_date': today})
add_todo({'id': 'CA-PRODUCTIVITY-CATEGORY-20261028', 'status': 'pending', 'priority': 'P1',
          'assigned_to': ['window2', '创作家'],
          'task': '竞品 futurepedia 有 ai-tools/productivity 分类页（我们只有单篇 best-ai-productivity-tools-2026，无分类聚合页），建议写 productivity AI 工具分类聚合页（slug: ai-tools/productivity），SERP竞争度=Medium（前 10 含 max-productive.ai/vucense.ai 两 niche 站）',
          'source': f'competitor_analysis_{today}', 'data_verified': True, 'created_date': today})

d['next_iteration_focus'] = nf
d['last_update'] = now_iso
json.dump(d, open(state_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
pend = len([i for i in nf if i.get('status') == 'pending'])
print('added:', added)
print('focus:', len(nf), '| pending:', pend)

# ===== competitor_analysis 追加 =====
open(os.path.join(P, 'iteration_center', f'competitor_analysis_{today}.md'), 'a', encoding='utf-8').write("""

## r39 复核（21:2x · 代理正常实抓档）
- **futurepedia sitemap 结构重大变化**：635 URLs 中 **courses=531（83.6%）**、ai-tools 分类页 77、resources=7、learning-paths=3、tutorials=1。**变现模式=课程主导**（此前为工具目录+联盟）。
- ai-tools 分类 77 个 vs 本地 243 md：12 个名义 GAP（chatbots/productivity/workflows/religion/marketing/project-management/automations/human-resources/presentations/legal/teachers/transcriber）**逐条核对全部已被历史 CA 开单覆盖或本地已有**（HR/presentation/legal/teachers/religion/marketing/project-mgmt/automations 在 r25 大事记，chatbots 在 r37）→ 分类缺口 0 新。
- **真结构性缺口 = 内容类型**：竞品课程/教程类内容 531+3+7 URLs，我们 0。开 3 条 CA（教程型×2 + productivity 分类聚合×1，全部 SERP 实搜验证）。
- topai.tools sitemap 404 死路（持续）。
""")
print('competitor_analysis appended')

# ===== keyword_opportunities 追加 =====
open(os.path.join(P, 'iteration_center', 'keyword_opportunities.md'), 'a', encoding='utf-8').write("""

## r39（2026-10-28 21:2x · GSC 实拉修正 + courses 结构变化档）

### GSC 实拉（fetch_gsc 重跑修正）
| 指标 | 本期 09-27~10-26 | 上期 08-29~09-26 |
|---|---|---|
| Impressions | **188**（修正 +10.6%，r38 为 170） | 2008（断崖 -90.6%） |
| Clicks | 0 | 9 |
| Avg Position | 13.86（改善，r38 为 14.84） | — |
| MOBILE | 4 imp（2.1%） | — |
- 10-26 单日回升 18 imp（9 月底以来峰值），观察是否持续
- Easy Wins（pos 20-50 有曝光）：0 个（诚实跳过，与 r38 一致）

### SERP 验证（general_search 实搜 2026-10-28）
| 关键词 | 竞争度 | 前 10 竞品 | 切入角度 |
|---|---|---|---|
| ai tools tutorial for beginners | **Medium** | ai4everyone.ai(独立站)/Udemy/Digital for Life/Adobe | 零代码工具上手教程列表 |
| best free ai courses 2026 | **High** | DataCamp/MIT Learn/Coursera/Dataquest/DEV | 独立测评+资源地图差异化 |
| best ai productivity tools 2026 | **Medium** | max-productive.ai/vucense.ai(niche)/Digital Trends/Slack | 本地已有 pos10.5 基础，做分类聚合 |

### 关键词分级
- P0：0 个（无新分类缺口 + Easy Wins=0，诚实记录）
- P1：3 个 CA 词（见 competitor_analysis r39 段，均含 slug）
- P2：0 个新

Total keywords analyzed: 累计 70+（r29 起 SERP 验证口径），本轮 SERP 实搜 3 词。
""")
print('keyword_opportunities appended')

# ===== audit_findings 追加 =====
open(os.path.join(P, 'iteration_center', 'audit_findings.md'), 'a', encoding='utf-8').write("""

## r39（2026-10-28 21:2x · GSC 数据修正 + 竞品结构变化）

### GSC 数据修正（fetch_gsc 重跑）
- 188 imp / 0 clk / pos 13.86（r38 为 170/14.84，GSC 延迟修正 +10.6%/-0.98 位）；断崖仍 -90.6%（vs 2008）
- **10-26 单日 18 imp** 为 30 天峰值，观察是否走出低位（P0-EXPOSURE-CLIFF 在池待架构师）

### P1: MOBILE 2.1%（4/188 imp）持续（P1-MOBILE-EXPOSURE 在池未动）

### P1: 竞品变现模式重大变化
- futurepedia sitemap 531/635 URLs 为 courses（课程变现），工具目录降权。若课程联盟模式验证有效，aitoolcrux 可跟进教程型内容（本轮已开 CA×2）

### P1: 最大曝光页 0 CTR
- best-ai-coding-tools-2026 pos4.1 imp12（全站曝光 6.4%）0% CTR，已开打磨师单（扩展范围依据）
""")
print('audit_findings appended')

# ===== 日志 =====
open(os.path.join(P, 'window_logs', f'analyst_{today}.md'), 'a', encoding='utf-8').write(f"""

## r39（{today} 21:2x · 分析师-数据洞察 SOP 触发·代理正常档）

- 执行待办：0 条闭环（analyst pending 仅 2 条真阻塞：GEO-BASELINE 需 ChatGPT/Perplexity 登录态、ELMO 需 Docker，均已复核确认；**不凑数不编造**）
- 新发现：3 条（GSC 数据修正 170→188、10-26 单日 18 imp 回升信号、竞品 courses 531 变现结构变化）
- 挖词：0 个 P0 + 3 个 P1（CA 教程型，SERP 验证 3 词：tutorial=Medium/courses=High/productivity=Medium）
- 竞品缺口：分类缺口 0 新（12 名义 GAP 全覆盖核对）；**内容类型缺口 3**（courses 531/learning-paths 3/resources 7 vs 我们 0）
- SERP 验证：3 个（general_search 实搜记录前 10 竞品）
- CTR 待办：3 条（ai-tools-review-guide pos10.0 / best-ai-comparison-tools pos18.0 / best-ai-coding-tools pos4.1 imp12 最大曝光）
- 写入待办：6 条（CTR×3 + CA×3）
- 剩余 pending：{pend}
- 环境记录：ego-browser 不可用（skill 未安装，npx skills add 需重启 Agent），浏览器通道回退 AdsPower CDP（本轮未需用）；docker 不可用（ELMO 确认阻塞）
""")
open(os.path.join(P, 'window_logs', f'analyst_keyword_{today}.md'), 'a', encoding='utf-8').write(f"""

## r39 关键词挖掘（{today} 21:2x）

1. 竞品 sitemap 挖词：✅ futurepedia 实抓 77 ai-tools 分类 + 531 courses（结构变化已记录）；12 名义 GAP 全覆盖核对，0 新
2. GSC Easy Wins：✅ live_pull_20261024 解析，pos 20-50 有曝光词=0，跳过
3. 关键词扩展：✅ 基于 courses 结构缺口扩展 3 词（tutorial/courses/productivity）
4. 分级：P0=0（无新分类缺口，诚实）；P1=3（CA 词）；P2=0
5. SERP 验证：✅ 3 个（general_search 实搜，High×1/Medium×2）
6. 输出：✅ keyword_opportunities.md r39 段
7. state.json：✅ 写入 6 条（CTR×3 + CA×3，非 P0 无需 serp_verified 字段但均附 SERP 数据）
8. 目标产出：P0 0/3（客观无新 P0 不硬凑）、P1 3/5（写为 CA 单合并）
""")
print('logs appended')
print('DONE')
