import io

f = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\knowledge_monetization.md"
with io.open(f, "r", encoding="utf-8") as fh:
    old = fh.read()

entry = """
## 2026-09-19 高频学习 - Recurring Affiliate 经济学 & SEO工具联盟选择框架

### 15个知识点
1. **Recurring vs 一次性佣金的盈亏平衡点在第8-10个月**：一次性$200（Semrush）vs recurring 20%×$129/月（Ahrefs），客户活到第10个月后recurring永久反超。SEO工具行业客户平均LTV 24个月，recurring终身价值是一次性的2-3倍。
2. **客户留存率 > 佣金百分比**：95%月留存×30%佣金 跑赢 85%月留存×50%佣金。选联盟时第一眼看churn，第二眼看rate。
3. **SEO工具购买决策周期2-6周、3-7次接触**：cookie必须≥60天才够覆盖；30天cookie要求落地页直接转化，90-120天cookie可以养邮件序列再转化。
4. **Last-click归因下，"比较/替代方案/vs"类文章价值最高**：用户最后一次点的链接拿佣金，所以"X vs Y""X alternatives"这类站在决策末端的页面转化率是单纯评测页的2-3倍。
5. **In-house program > 第三方网络**：in-house无网络抽成，佣金更高、cookie更长、能直接对接affiliate manager；缺点是要分别申请、分别看dashboard。
6. **自动批准 vs 手动审核**：Mangools/Surfer/InVideo(Pictory)注册即开；Ahrefs/Semrush/Kajabi要求1000+月UV或已有流量证明。新站先打自动批准的，攒案例再申请手动审核的。
7. **起付金额$50-$150**：$50起付更早拿到第一笔钱建立正反馈；$150门槛意味着前2-3个月收入积压。Mangools $150、Surfer $100、Semrush $50。
8. **佣金率会下调，要选3年没降过的**：Semrush历史上从40% recurring砍到$200一次性；Jasper/Copy.ai直接关停联盟。签约前查Wayback Machine上该联盟条款页的历史版本。
9. **Tiered佣金设计：冲到下一档值得做90天专项**：Mangools 25%/30%/35%，101单/月跳到35%等于收入+16.7%（不是33%，因为基数变了）；算清当前月单数，差几单到下一tier就加一把火。
10. **谈判窗口：月销50+可以找AM谈**：要求涨5-10%佣金、降低起付、延长cookie。Merchant愿意为稳定销量让5个百分点。
11. **成功affiliate组合 = 1个一次性 + 1-2个recurring**：一次性提供现金流（前3个月有钱到账），recurring堆长期被动收入。单一模式抗风险差。
12. **转化率benchmark**：评测站CTA→affiliate点击3-5%合格，6-8%优秀，9%+ exceptional。如果自己站点<2%，先改CTA位置/文案，不要急着加新联盟。
13. **反churn推荐纪律**：推荐前自己用满2周。推荐客户第1个月就取消的产品，recurring等于零。
14. **FirstPromoter/PartnerStack/Impact 是SaaS联盟主战场**：AI工具站90%的recurring program在这三个平台上，直接注册一个账号就能批量申请，不用挨个官网找。
15. **AI工具站变现结构三层**：顶层（direct affiliate recurring）= 主收入；中层（display ads/Ezoic）= 兜底；底层（email list/digital product）= 长期复利。不要在月UV<500时急着接广告，会拖慢LCP、伤SEO。

### 新发现联盟
| 工具 | 佣金 | Cookie | 起付 | 平台 | 申请链接 |
|---|---|---|---|---|---|
| Mangools（KWFinder/SERPWatcher/LinkMiner） | 25-35% lifetime recurring（tiered：<30单25%，31-100单30%，101+单35%） | 30天 | $150 PayPal | In-house，即时批准，无需审核 | https://mangools.com/affiliates |
| SE Ranking（备选） | 30% lifetime recurring | 120天 | 未公开 | In-house | https://www.se-ranking.com/affiliates/ |
| SpyFu（备选） | 40% | 365天 | $100 | In-house | 申请后自动开通 |

**Mangools为什么值得申请**：
- 即时批准，新站就能上（不卡UV门槛）
- $49/月入门价，比Semrush/Ahrefs便宜，转化率更高
- 67%的新用户注册后24小时内决定订阅（高转化信号）
- lifetime recurring，SEO工具行业低churn，长期复利
- 我们网站已经有500+工具页，只要在"best SEO tools""keyword research tools"类文章里插入Mangools推荐位即可

### 可落地建议（给窗口1）
- 在Top工具页里加一个"SEO Tools"板块（如果还没有），把Mangools affiliate链接放进去
- 写一篇"Mangools vs Semrush vs Ahrefs: Which SEO Tool Is Worth It in 2026?"文章，吃比较关键词的高转化流量
- CTA文案沿用现有"Try Mangools Free" + "No credit card required"模式，不用新加组件
- 用户侧动作：注册一个免费Mangools账号，自动拿到affiliate ID，把链接发回窗口5入库

---
"""

# Insert after the first line (title) and the blank line
lines = old.split("\n", 2)
if len(lines) >= 3:
    new = lines[0] + "\n" + lines[1] + entry + lines[2]
else:
    new = old + entry

with io.open(f, "w", encoding="utf-8") as fh:
    fh.write(new)
print("OK, entry inserted")
