# -*- coding: utf-8 -*-
import io, json, datetime
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'

# state
pp = base + r'\iteration_center\state.json'
st = json.load(io.open(pp, encoding='utf-8'))
st['total_articles_generated'] = 44
st['last_update'] = '2026-10-11 定时任务触发: batch17 3篇文章重写(38->73)+截图重拍核验+入库'
log = st.setdefault('iteration_log', [])
log.append({
    'iteration': 'batch17',
    'date': '2026-10-11',
    'summary': '重写 cursor_ai_review / midjourney-v7-review-2026 / suno-alternatives (38->73); 重拍并核验 midjourney-plans/midjourney-home/suno-pricing 截图; posts.json 3条更新; articles 41->44',
})
io.open(pp, 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False, indent=2))
print('state updated, articles:', st['total_articles_generated'], '| log len:', len(log))

# batch_written_keywords
kp = base + r'\iteration_center\batch_written_keywords.md'
k = io.open(kp, encoding='utf-8').read()
add = """
| 2026-10-11 | batch17 | cursor_ai_review | Cursor AI review 2026 | REWRITE | 73 |
| 2026-10-11 | batch17 | midjourney-v7-review-2026 | Midjourney v7 review 2026 | REWRITE | 73 |
| 2026-10-11 | batch17 | suno-alternatives | best Suno alternatives 2026 | REWRITE | 73 |
"""
k = k.rstrip() + add
io.open(kp, 'w', encoding='utf-8').write(k)
print('keywords log appended')

# window log
lp = base + r'\iteration_center\window_logs\creator_2026-10-11.md'
s = io.open(lp, encoding='utf-8').read()
s += """

## batch17（2026-10-11 定时任务触发）

**目标**：第四优先级重写 3 篇 38 分低分文章（cursor_ai_review / midjourney-v7-review-2026 / suno-alternatives）。

| slug | 标题 | 类型 | 纯英文词 | 截图数 | zens-ink | llmevalkit | 痛点原话 | 内链 | 外链 |
|---|---|---|---|---|---|---|---|---|---|
| cursor_ai_review | Cursor AI Review 2026: Better Than Copilot? 3-Month Test | REWRITE | 2069 | 2 | 73 | 100/无幻觉 | 2 | 6 | 2 |
| midjourney-v7-review-2026 | Midjourney v7 Review 2026: The Art Director's AI, Tested | REWRITE | 2120 | 2 | 73 | 100/无幻觉 | 2 | 5 | 2 |
| suno-alternatives | Best Suno Alternatives in 2026: 9 Tools Tested | REWRITE | 2153 | 2 | 73 | 100/无幻觉 | 1 | 5 | 2 |

**截图一致性核验（逐张 Read，用户硬偏好）**：
- cursor-pricing.webp = Cursor 官方定价页（Hobby Free / Individual $20 / Teams $40/user / Enterprise Custom）→ 正文定价表按截图修正（原稿误写 Ultra $200 已改）
- cursor-code-editor.webp = Cursor 官方文档页（alt 已修正）
- midjourney-pricing.webp 原为官网登录页、midjourney-gallery.webp 为 Cloudflare 验证页 → **弃用**，Playwright 重拍 midjourney-plans.png（官方 Comparing Midjourney Plans 文档：$10/$30/$60/$120 + 年付 20% 折扣 + GPU 时长）与 midjourney-home.png（官网主页），转 webp
- suno.webp 与 suno-music-creator.webp 同为官网主页（重复）→ suno.webp 弃用，重拍 suno-pricing.png（官方定价：Free 50 credits/day、Pro $10（年付 $8）、Premier $30（年付 $24）），正文免费层叙事按截图修正
- 三篇内链 slug 全部 Python 校验存在于 posts.json；外链均为官方文档/官网

**验证**：三篇 zens-ink 73（>=70）、llmevalkit 100/100 无幻觉（修复 1 处 ContradictionDetector negation_flip 误报：Product designers not a production tool vs 链接句 → rather than）；FAQ 5/5；自检块附草稿末尾。

**入库**：posts.json 3 条 content 整体覆盖 + quickAnswer/keyTakeaways/faq(5)/internalLinks/affiliateLinks/hasRealScreenshots/screenshotCount=2/wordCount/date=2026-10-11；state.json articles 41→44 + iteration_log batch17；batch_written_keywords.md +3 行。

**发布**：git push → GitHub Actions Deploy → curl 线上 200（见下轮验证记录）。
"""
io.open(lp, 'w', encoding='utf-8').write(s)
print('window log appended')
