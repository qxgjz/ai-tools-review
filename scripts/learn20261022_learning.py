# -*- coding: utf-8 -*-
import io,os
p=r'C:\Users\通明街\Doubao\chats\2026-09-02\new-chat\commander_learning.md'
block="""

---

## 打磨师学习｜2026-10-22 可读性优化 + 可扫描性 + LLM可提取（Readability / Scannability / GEO extraction）

> 主题：AI写作质量-可读性优化。来源5个权威：Google Search Central、Nielsen Norman Group(F-pattern/Be Succinct)、Yoast Readability、ClaritySEO/Front-End Checklist(Flesch)、HumansWithAI/Promptive(LLM提取)。已落地为3条打磨师P1待办（state.json）。

| # | 知识点 | 对aitoolcrux的落地 |
|---|---|---|
| 1 | Google官方：文字要easy-to-read且well-organized，长内容拆成段落+小节+标题帮助导航，无拼写语法错误（SEO Starter Guide） | 所有博客必须有层级H2/H3，不写大段无标题文字 |
| 2 | Flesch Reading Ease网页目标60-70；电商/工具类65-75、grade6-7；SOP硬线先保>50 | 批次打磨先过Flesch>50，理想冲60-70 |
| 3 | 平均句长15-20词；>25-30词理解度非线性下降；Yoast: >20词句子占比>25%即标红 | 逐句拆长句，25词以上必拆2-3句 |
| 4 | 网页段落2-4句/<100词；Yoast绿<150词、红>200词；移动端长块高跳出；单句段可用于强调 | 把超长段切成2-4句小块 |
| 5 | 一段只讲一个意思(one idea per paragraph)，额外观点用户会跳过 | 段内不混第二个论点 |
| 6 | NN/g F-pattern：用户扫读而非逐字读；要2-3级有意义标题（不用花俏标题），左缘前2-3词承载信息 | 标题用信息词，段首直接给要点 |
| 7 | 关键短语少量加粗（越少越突出）；锚文本用信息词，禁用click here/more（也利于屏幕阅读器/AI） | 对比页内链写具体工具名 |
| 8 | 列表/编号用于步骤与清单；对比、价格、功能不要埋进散文，用表格 | 工具对比改markdown表/bullet |
| 9 | 过渡词连接句子（however/for example/after that）；Yoast阈值约30%；避免连续同结构句 | 补过渡词，句式长短交替 |
| 10 | 主动语态>90%，被动>10%标红；用常见日常词，生僻术语只定义一次 | 把被动句改主动 |
| 11 | 删掉无信息的凑字开头(filler intro)，它比什么都拖慢扫描 | 砍掉"This article will discuss..."类空话 |
| 12 | LLM/Perplexity提取：首100词内给直接答案(BLUF)，含命名实体+具体数字+货币+日期，被逐字引用概率最高 | 首屏BLUF块带真实数字 |
| 13 | 每个问句H2下给40-60词自包含直答块（不依赖前文指代，匹配RAG~512-token分块） | Answer-First块量化为40-60词 |
| 14 | FAQ用用户真实搜索问句；事实带年份/更新日期，避免悬空代词 | FAQ句式对齐搜索词，标日期 |
| 15 | 每300-400词必须出现小标题；配图/图卡打断文字墙 | 长段落插H3或表/图 |

落地待办（已写入 iteration_center/state.json，assigned_to=打磨师）：
- P1-READABILITY-SENTENCE-PARA-20261022：句长/段落/被动/过渡词批次，Flesch>50冲60-70，一次≥5篇
- P1-SCAN-FORMAT-20261022：对比/价格转表格bullet、少量加粗、信息锚文本、删filler
- P1-LLM-ANSWER-BLOCK-20261022：首100词BLUF+实体/数字/日期，H2下40-60词自包含直答块

来源URL：
- https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/
- https://www.nngroup.com/articles/be-succinct-writing-for-the-web/
- https://yoast.com/features/readability-analysis/
- https://getclarityseo.com/guides/how-to-improve-your-websites-readability-score
- https://www.eyesift.com/blog/readability-checker/
- https://humanswith.ai/blog/how-to-optimize-content-for-llm-retrieval/
- https://getpromptive.ai/blog-how-to-structure-an-article-so-perplexity-quotes-it-word-for-word
"""
with io.open(p,'a',encoding='utf-8',newline='') as f:
    f.write(block)
print('appended bytes',len(block))
