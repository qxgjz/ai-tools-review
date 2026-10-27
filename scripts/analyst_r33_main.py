# -*- coding: utf-8 -*-
"""r33 主脚本：竞品分析产出+关键词挖词+CTR待办+GAP复核闭环+日志"""
import json, os
from datetime import datetime

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
now_iso = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
now = datetime.now().strftime('%Y-%m-%d %H:%M')
today = datetime.now().strftime('%Y-%m-%d')

# ============ 1. state.json 补录（去重） ============
d = json.load(open(os.path.join(P, 'iteration_center', 'state.json'), encoding='utf-8'))
nf = d['next_iteration_focus']
ids = {i.get('id') for i in nf}
added = []
def add_todo(t):
    if t['id'] not in ids:
        nf.append(t); ids.add(t['id']); added.append(t['id'])

# CTR 待办（新窗口 5-15 位，真实数据；不足2则扩5-20）
add_todo({'id': 'CTR-PAGE-ABOUT-20261027', 'status': 'pending', 'priority': 'P1',
          'assigned_to': ['window5', '打磨师'],
          'task': '页面 /about 排名 3.3 但 CTR 仅 0%（impr=7 clk=0，双变体 3.3+1.3），优化 title/meta description 提升点击率',
          'source': f'ctr_optimization_{today}', 'position': 3.3, 'ctr': 0.0, 'data_verified': True, 'created_at': now_iso})
add_todo({'id': 'CTR-QUERY-GH-COPILOT-PRICING-20261027', 'status': 'pending', 'priority': 'P1',
          'assigned_to': ['window5', '打磨师'],
          'task': '查询 [github copilot windsurf amazon q tabnine jetbrains ai pricing changes] 排名 5.0 但 CTR 仅 0%（impr=1 clk=0），低价值导航长尾观察，优化匹配页 title 或放弃',
          'source': f'ctr_optimization_{today}', 'position': 5.0, 'ctr': 0.0, 'data_verified': True, 'created_at': now_iso})

# 竞品缺口 CA 待办（5个，SERP 全 High）
serp = {
    'email-assistant': ('best AI email assistant tools 2026', 'Best AI Email Assistants 2026: 12 Tools Compared for Gmail & Outlook', 'best-ai-email-assistants-2026', 'High'),
    'music-generator': ('best AI music generator 2026', 'Best AI Music Generators 2026: Suno, Udio & 10 More Tested', 'best-ai-music-generators-2026', 'High'),
    'text-to-video': ('best AI text to video generator 2026', 'Best AI Text-to-Video Generators 2026: 10 Tools Ranked by Output Quality', 'best-ai-text-to-video-generators-2026', 'High'),
    'social-media': ('best AI social media tools 2026', 'Best AI Social Media Tools 2026: 15 Tested for Scheduling & Content', 'best-ai-social-media-tools-2026', 'High'),
    'website-builders': ('best AI website builder 2026', 'Best AI Website Builders 2026: 12 Compared for Speed & Cost', 'best-ai-website-builders-2026', 'High'),
}
for cat, (kw, title, slug, comp) in serp.items():
    cid = f'CA-{cat.upper().replace("-","_")}-20261027'
    add_todo({'id': cid, 'status': 'pending', 'priority': 'P1',
              'assigned_to': ['window2', '创作家'],
              'task': f'竞品 futurepedia 在做 {cat} 内容（竞品有 1 个分类，我们 0 个），建议写 {title} 文章，SERP竞争度={comp}',
              'source': f'competitor_analysis_{today}', 'data_verified': True, 'created_at': now_iso})
    # KW 待办：3 个 P0（email/music/text-to-video）+ 2 个 P1（social/website）
    pr = 'P0' if cat in ('email-assistant', 'music-generator', 'text-to-video') else 'P1'
    kid = f'KW-{cat.upper().replace("-","_")}-20261027'
    add_todo({'id': kid, 'status': 'pending', 'priority': pr,
              'assigned_to': ['window2', '创作家'],
              'task': f'基于关键词 [{kw}] 写 2000 字新文章，标题建议 [{title}]，slug 建议 [{slug}]',
              'source': f'keyword_mining_{today}', 'serp_competition': comp, 'serp_verified': True,
              'our_angle': '免费额度对比+独立实测结论', 'created_at': now_iso})

# 新 P0 发现：auto_redirect 暴增
add_todo({'id': 'AUTO-REDIRECT-SPIKE-20261027', 'status': 'pending', 'priority': 'P0',
          'assigned_to': ['window1', '架构师'],
          'task': 'GSC 索引报告实抓（10-27）：auto_redirect 9→94 暴增（+85，noindex 5→33），疑似 article-api-* 时间戳 URL/.md 后缀及新页面 301 链；排查并清理重定向链（与 ARTICLE-API-URL-CLEAN 联动）',
          'source': f'index_snapshot_{today}', 'data_verified': True, 'created_at': now_iso})

d['next_iteration_focus'] = nf
d['last_update'] = now_iso
json.dump(d, open(os.path.join(P, 'iteration_center', 'state.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('todos added:', len(added), added)
print('focus:', len(nf), '| pending:', len([i for i in nf if i.get('status')=='pending']))

# ============ 2. GAP 复核闭环（P1-REPORT-GAP-RECHECK） ============
gap_summary = """### P1-REPORT-GAP-RECHECK 复核结论（{now}）
| GAP ID | 状态 | 结论 |
|---|---|---|
| P0-TRAFFIC-CLIFF-20260924（流量悬崖） | focus/archived_todos 均无记录 | 已丢失（历史清理覆盖），git 历史可溯源；行为影响已由 r30-r33 持续监控替代 |
| P1-OPENSER（openserp 排名核对） | archived_todos 内 P1-TOOL-OPENSERP-001 **completed** | 已闭环归档 ✅ |
| GSC-QUOTA-RERUN-20261012（配额重跑） | 本轮随 P0-INDEX-SNAPSHOT-RERUN **completed** | 已闭环（indexing_snapshot_20261027 实抓）✅ |
"""
open(os.path.join(P, 'iteration_center', 'audit_findings.md'), 'a', encoding='utf-8').write('\n\n---\n\n## GAP ID 复核（%s）\n%s' % (now, gap_summary))
print('gap recheck appended')

# 闭环 P1-REPORT-GAP-RECHECK + P1-GSC-SCRIPT-PATH-CONFIRM
d = json.load(open(os.path.join(P, 'iteration_center', 'state.json'), encoding='utf-8'))
nf = d['next_iteration_focus']
for t in nf:
    if t.get('id') == 'P1-REPORT-GAP-RECHECK-20261027' and t.get('status') != 'completed':
        t['status'] = 'completed'; t['completed_at'] = now_iso
        t['evidence'] = 'TRAFFIC-CLIFF无记录/OPENSERP已completed归档/QUOTA-RERUN随P0闭环'
    if t.get('id') == 'P1-GSC-SCRIPT-PATH-CONFIRM-20261027' and t.get('status') != 'completed':
        t['status'] = 'completed'; t['completed_at'] = now_iso
        t['evidence'] = '确认fetch_gsc.py在.github/scripts/；-site:/site:过滤已补强并验证（site:worldmonitor.app移出报告）'
d['next_iteration_focus'] = nf
d['last_update'] = now_iso
json.dump(d, open(os.path.join(P, 'iteration_center', 'state.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('P1s closed')

# ============ 3. competitor_analysis_2026-10-27.md ============
ca = f"""
# 竞品内容缺口分析 · {now}

## 一、数据源（实抓，非凭记忆）
- futurepedia sitemap 实抓成功（competitor_sitemap_cache.json 更新于 10-27 08:07，75 分类）
- topai.tools sitemap 仍 404（HTTP Error，连续多轮）
- 本地文章目录 268 个 md（content_drafts 全量）+ 历史 CA/KW 待办去重

## 二、竞品内容矩阵（截取与缺口相关）
| 竞品分类 | futurepedia | aitoolcrux 本地 | 缺口 |
|---|---|---|---|
| email-assistant | 1 分类 | 0 | **是** |
| music-generator | 1 分类 | 0（有 elevenlabs-vs 但非 best-list） | **是** |
| text-to-video | 1 分类 | 0 | **是** |
| social-media | 1 分类 | 0 | **是** |
| website-builders | 1 分类 | 0 | **是** |
| ai-agents/chatbots/logo-generator/customer-support 等 | 1 | 已有文章 | 否 |

## 三、内容缺口清单 + 5 个可借鉴选题（SERP 验证）
| # | 缺口分类 | 建议标题 | slug | SERP 竞争度 | 前10竞品 |
|---|---|---|---|---|---|
| 1 | email-assistant | Best AI Email Assistants 2026: 12 Tools Compared for Gmail & Outlook | best-ai-email-assistants-2026 | High | Carly/Inbox Zero/Lindy/alfred_/Hiver/Superhuman/Gemini |
| 2 | music-generator | Best AI Music Generators 2026: Suno, Udio & 10 More Tested | best-ai-music-generators-2026 | High | Suno/Udio/ElevenLabs/Evasong/Kenerate/Enkio |
| 3 | text-to-video | Best AI Text-to-Video Generators 2026: 10 Tools Ranked by Output Quality | best-ai-text-to-video-generators-2026 | High | PixVerse/Fliki/Synthesia/Zapier/Shopify/Veo |
| 4 | social-media | Best AI Social Media Tools 2026: 15 Tested for Scheduling & Content | best-ai-social-media-tools-2026 | High | Hootsuite/Sprout/Buffer/Zapier/TechSifted/SocialPilot |
| 5 | website-builders | Best AI Website Builders 2026: 12 Compared for Speed & Cost | best-ai-website-builders-2026 | High | Elementor/Wix/Replit/Framer/B12/Blink |

## 四、SERP 验证章节（general_search 实搜 2026-10-27 09:14-09:15）
- 5 词全 High：email-assistant（工具官方自推密集）/music-generator（Suno-Udio 生态+工具站）/text-to-video（大厂官方 SEO 页）/social-media（SaaS 官方+测评站）/website-builders（平台官方+测评站）
- 切入角度（统一）：**免费额度对比 + 独立实测结论 + 工具适用场景矩阵**（区别于竞品官方自推）
- 搜索量标注：全部"预估"，依据=竞品分类存在（futurepedia 有分类）+ SERP 竞争度
"""
open(os.path.join(P, 'iteration_center', f'competitor_analysis_{today}.md'), 'w', encoding='utf-8').write(ca)
print('competitor_analysis written')

# ============ 4. keyword_opportunities.md 追加 ============
ko = f"""

---

## r33 · 关键词挖掘（{now} · 竞品 sitemap 实抓成功）

**Total keywords analyzed: 5**（全部 SERP 实搜验证）

| # | 关键词 | 分级 | 竞争度 | 建议标题 | slug | 依据 |
|---|---|---|---|---|---|---|
| 1 | best AI email assistant tools 2026 | **P0** | High | Best AI Email Assistants 2026: 12 Tools Compared for Gmail & Outlook | best-ai-email-assistants-2026 | futurepedia 有分类我们无；SERP 实搜验证 |
| 2 | best AI music generator 2026 | **P0** | High | Best AI Music Generators 2026: Suno, Udio & 10 More Tested | best-ai-music-generators-2026 | 同上 |
| 3 | best AI text to video generator 2026 | **P0** | High | Best AI Text-to-Video Generators 2026: 10 Tools Ranked by Output Quality | best-ai-text-to-video-generators-2026 | 同上 |
| 4 | best AI social media tools 2026 | P1 | High | Best AI Social Media Tools 2026: 15 Tested for Scheduling & Content | best-ai-social-media-tools-2026 | 同上 |
| 5 | best AI website builder 2026 | P1 | High | Best AI Website Builders 2026: 12 Compared for Speed & Cost | best-ai-website-builders-2026 | 同上 |

### SERP 验证（5 词全部实搜）
- 搜索量：全部"预估"，无第三方数据；依据=竞品分类存在+SERP 前10 竞品密度
- 竞争度判定：email-assistant High（工具官方自推密集）/music-generator High/text-to-video High/social-media High/website-builders High
- 切入角度：免费额度对比+独立实测+场景矩阵（竞品多为官方自推）
"""
open(os.path.join(P, 'iteration_center', 'keyword_opportunities.md'), 'a', encoding='utf-8').write(ko)
print('keyword appended')

# ============ 5. GSC 报告 latest_report ============
lr = f"""
# GSC 最新报告快照 · {now}

## 汇总（窗口 2026-09-26~2026-10-25，fetch_gsc.py 实拉）
| 指标 | 数值 |
|---|---|
| Clicks | 0 |
| Impressions | 166 |
| CTR | 0.00% |
| Avg Position | 14.61 |
| 有曝光 URL 数（searchAnalytics） | **199** |

## 索引快照（AdsPower CDP 实抓 GSC 索引覆盖率页，10-27）
| 指标 | W1(10-09) | W2(10-25) | 变化 |
|---|---|---|---|
| 已知 URL | 905 | **1384** | +479 |
| 已编入 | 477 | **640** | +163 |
| 未编入 | 428 | **744** | +316 |
| 收录率 | 52.8% | **46.2%** | -6.6pp |

## 未收录原因（W2）
discovered_not_indexed **589**（P0）· auto_redirect **94**（P0 暴增 9→94）· noindex **33**（P1）· duplicate_without_canonical 9 · duplicate_google_chosen 8 · redirect_error 5 · not_found_404 4 · crawled_not_indexed 2

## Top 查询（-site:/site: 过滤后）
ai-native ide adoption metrics cursor replit latest(1.0) / github copilot...pricing(5.0) / tabbyml(18.0) / bondai(89.5) / milvus ui(84.0) / react agent(82.0) / google gemini langgraph(75.0)
"""
open(os.path.join(P, 'gsc-ga4-report', f'latest_report_{today}.md'), 'w', encoding='utf-8').write(lr)
print('latest_report written')

# ============ 6. 日志 ============
log = f"""

## r33（{now} · 分析师-数据洞察 SOP 触发）

- 执行待办：4 条闭环（P0-INDEX-SNAPSHOT-RERUN ✅ / GSC-QUOTA-RERUN ✅ / P1-REPORT-GAP-RECHECK ✅ / P1-GSC-SCRIPT-PATH-CONFIRM ✅）；2 条阻塞复查（GEO-BASELINE/ELMO）
- 新发现：**auto_redirect 9→94 暴增（P0）**、收录率 52.8%→46.2%（P0）、noindex 5→33（P1）、duplicate_google_chosen 8（P1）
- 挖词：5 个（P0×3：email-assistant/music-generator/text-to-video；P1×2：social-media/website-builders）——全部 SERP 实搜验证
- 竞品缺口：5 个（futurepedia 75 分类实抓 vs 本地 268 md 去重后筛出，全 High）
- SERP 验证：5 个（general_search 实搜 09:14-09:15）
- CTR 待办：2 条（CTR-PAGE-ABOUT / CTR-QUERY-GH-COPILOT-PRICING）
- 写入待办：13 条（2 CTR + 5 CA + 5 KW + 1 AUTO-REDIRECT-SPIKE P0）
- 剩余 pending：{len([i for i in nf if i.get('status')=='pending'])}（含分析师阻塞 2 条）
- 成功：competitor_gap 实抓 ✅（缓存更新 75 分类）、fetch_gsc 新窗口 ✅（166/0/14.61）、site: 过滤修复 ✅
- 失败/降级：topai sitemap 404（连续多轮）；sitemaps API 对 sc-domain 404/www 403（权限限制，改用 CDP 通道）
"""
open(os.path.join(P, 'window_logs', f'analyst_{today}.md'), 'a', encoding='utf-8').write(log)
print('logs appended')
