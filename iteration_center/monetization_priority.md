# 变现优先级报告

> 生成时间：2026-09-16
> 角色：变现运营专员
> 依据：knowledge_monetization.md + 本轮新调研 + 线上FTC披露检查

---

## 一、本轮新调研发现

### 🆕 新发现的高佣金计划

| 工具 | 佣金 | Cookie | 平台 | 亮点 |
|------|------|--------|------|------|
| **Scalenut** | **30-50% lifetime recurring** | 60天 | FirstPromoter | 终身佣金！50个活跃客户后升到40%，$50起付，PayPal月结 |
| **Descript** | $25一次性（已从15% recurring改版） | 30天 | PartnerStack | ⚠️ 2026年已改成flat $25，不再是recurring，降级 |
| **Jasper AI** | 约45% recurring（老数据） | - | - | 状态存疑，需官网确认是否重新开放 |

### 重要更新
- **Scalenut** 应升为 **Tier 1**：终身recurring非常稀有，SEO工具类，和我们网站受众（内容创作者）高度匹配
- **Descript** 从推荐列表降级：已不是recurring
- **Jasper** 之前记录"已关闭"，但多个2026年来源仍提及其联盟，建议重新查官网确认

---

## 二、FTC合规检查结果

| 检查项 | 状态 | 证据 |
|--------|------|------|
| 工具页有affiliate disclosure | ✅ | ElevenLabs页29处提及 |
| disclosure在CTA附近 | ✅ | 紧跟按钮下方 |
| rel="sponsored"标签 | ✅ | 代码中已加 |
| 专门/disclosure页面 | 待确认 | 需检查/disclosure路由是否存在 |
| 文章页disclosure | 待检查 | 需抽样blog文章 |

---

## 三、推荐申请优先级（更新版）

### 🔥 立即申请（本周）

| 优先级 | 工具 | 为什么 | 平台 |
|--------|------|--------|------|
| P0 | **Scalenut** | 30-50%终身recurring，SEO工具，受众精准 | FirstPromoter |
| P0 | **ElevenLabs** | ✅ 已接入 | PartnerStack |
| P1 | **InVideo** | 50%首单，视频创作者刚需 | Impact |
| P1 | **Pictory** | 30% recurring，视频创作者 | 官网直申 |
| P1 | **Writesonic** | 30% lifetime，写作工具 | 官网直申 |
| P2 | **HeyGen/Synthesia/Anyword/Speechify** | 视频/写作类recurring | Rewardful |

### ⚠️ 暂缓

| 工具 | 原因 |
|------|------|
| Descript | 已改$25一次性，不是recurring |
| Grammarly | CJ注册受阻（地区限制） |
| Jasper | 状态不明，需官网确认 |
| Amazon Associates | 按用户要求不优先 |

---

## 四、CTA优化建议（基于现状）

### 已完成 ✅
- [x] 有affiliateUrl的工具显示"Try {name} Free"（commit f67ce44）
- [x] 无affiliateUrl的保持"Visit Official Website"
- [x] CTA下方有FTC disclosure

### 待优化 📋

1. **对比页（/compare）加CTA**：对比页已占16%曝光，但CompareAffiliateButton还是"Visit"，应改成"Try Free →"
2. **文章页CTA**：blog文章目前没有affiliate CTA，应在相关工具文章末尾加
3. **信任背书**：CTA旁加"✅ Tested & Reviewed"标签，提高点击率
4. **对比页"Our Pick"模块**：在/compare底部加月度推荐模块

---

## 五、变现瓶颈分析

| 瓶颈 | 影响 | 解决方案 |
|------|------|---------|
| 533个工具只有1个有affiliateUrl | 99.8%流量没有变现入口 | 用户注册Impact/Rewardful后批量填链接 |
| 月UV低（GSC曝光908，点击4） | 联盟平台审核难通过 | 先做SEO流量（窗口1/3在做） |
| 没有Revenue Tracking | 不知道哪个工具页转化好 | 接入后从PartnerStack/Impact后台看 |
| 对比页CTA弱 | 高转化页面浪费 | 改"Visit"→"Try Free" |

---

## 六、30天变现路线图

### Week 1（本周）
- [ ] 用户注册FirstPromoter，申请Scalenut
- [ ] 用户注册Impact，申请InVideo
- [ ] 用户注册Rewardful，申请HeyGen/Synthesia
- [ ] 改/compare页CTA文案

### Week 2
- [ ] 把拿到的链接批量填进tools.json
- [ ] 检查/disclosure页面是否存在
- [ ] 文章页加affiliate CTA模块

### Week 3
- [ ] 申请Pictory/Writesonic官网直申
- [ ] 加"Tested & Reviewed"信任标签
- [ ] 对比页加"Our Pick"模块

### Week 4
- [ ] 接入Surfer SEO（PartnerStack，已有账号）
- [ ] 月度变现数据复盘
- [ ] 申请Semrush（Impact，需流量证明）

---

## 七、需要用户手动完成的事（阻塞项）

| # | 任务 | 为什么我不能做 |
|---|------|--------------|
| 1 | 注册FirstPromoter申请Scalenut | 需邮箱验证+税务信息 |
| 2 | 注册Impact申请InVideo/Semrush/Canva | 需填网站资料+审核 |
| 3 | 注册Rewardful申请HeyGen/Synthesia/Anyword/Speechify | 需邮箱验证 |
| 4 | 完成Dub Partners域名TXT验证 | 需登录DNS后台 |

---

*报告人：变现运营专员*
*下次执行：自动触发时继续更新此文件*
