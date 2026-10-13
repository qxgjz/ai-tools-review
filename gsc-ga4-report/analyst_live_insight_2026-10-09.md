# 分析师实时洞察报告（LIVE GSC API） - 2026-10-09

**拉取时间**: 2026-10-09T14:55:48
**数据来源**: GSC Search Console API 实时拉取（服务账号 `aitoolcrux-bot`，走代理 127.0.0.1:7890）
**资源**: `sc-domain:aitoolcrux.com`
**原始数据**: `live_pull_20261009_1454.json`

---

## 一句话结论

**9/24 断崖后，10 月日均曝光仅 8 次（vs 9 月上旬 111 次），且 /compare 排名从 33.8 进一步滑到 38.8——流量危机没有自愈，正在恶化。**

---

## 最近 7 天（9/30 - 10/6）每日趋势

| 日期 | 点击 | 曝光 | CTR | 平均排名 |
|---|---|---|---|---|
| 2026-09-30 | 0 | 12 | 0.00% | 7.2 |
| 2026-10-01 | 0 | 1 | 0.00% | 3.0 |
| 2026-10-02 | 0 | 9 | 0.00% | 12.2 |
| 2026-10-03 | 0 | 14 | 0.00% | 77.9 |
| 2026-10-04 | 0 | 8 | 0.00% | 6.9 |
| 2026-10-05 | 0 | 8 | 0.00% | 7.0 |
| 2026-10-06 | 0 | 6 | 0.00% | 7.5 |
| **合计** | **0** | **58** | **0.00%** | **24.9** |

**与 9/6-9/23 高峰对比**：日均曝光从 111.2 → 8.3（-92%），已连续 13 天低于 20。

## Top 20 真实查询词（已过滤 `-site:` 污染）

| 查询 | 点击 | 曝光 | 排名 | 解读 |
|---|---|---|---|---|
| `best voice changer 2026` | 1 | 1 | 4.0 | ✅ 前10 |
| `"midjourney"` | 0 | 1 | 8.0 | ✅ 前10 |
| `"voice changer"` | 0 | 1 | 6.0 | ✅ 前10 |
| `%"google/gemini-3.8-flash" openrouter api integration guide` | 0 | 1 | 5.0 | ✅ 前10 |
| `affiliate transparency in software reviews` | 0 | 1 | 84.0 | ❌ 3页后 |
| `agency agents` | 0 | 1 | 68.0 | ❌ 3页后 |
| `agency-agents` | 0 | 1 | 49.0 | 🔶 2-3页 |
| `agent ai helper` | 0 | 3 | 87.7 | ❌ 3页后 |
| `agent ai online` | 0 | 2 | 70.5 | ❌ 3页后 |
| `agent ai tool` | 0 | 4 | 78.5 | ❌ 3页后 |
| `agent ai tools` | 0 | 1 | 79.0 | ❌ 3页后 |
| `agenta` | 0 | 3 | 56.0 | ❌ 3页后 |
| `agenta ai` | 0 | 1 | 64.0 | ❌ 3页后 |
| `agents agency` | 0 | 2 | 79.5 | ❌ 3页后 |
| `agents review` | 0 | 1 | 76.0 | ❌ 3页后 |

**关键观察**：
- **唯一有点击的真实词**："best voice changer 2026"（1 click, pos 4）
- **最大曝光词**："ai agent"（10 impr, pos 94.7）——在第 10 页，完全没点击价值
- **一批 "agent ai xxx" 长尾词**都在 pos 60-90：有曝光但完全没排名
- **无 `-site:` 污染词进入 Top 20**：说明 9/6-9/8 那波工具爬取高峰已过

## Top 15 页面（28天）

| 页面 | 点击 | 曝光 | 排名 | 环比上次报告 |
|---|---|---|---|---|
| `/blog/best-ai-voice-changers-2026` | 2 | 68 | 16.5 | 曝光+0, 排名-0.0 |
| `/compare` | 2 | 212 | 38.8 | 曝光-60, 排名+5.0 |
| `/` | 1 | 4 | 1.2 | - |
| `/blog/openai_astra_review` | 1 | 128 | 11.2 | 曝光-29, 排名+0.4 |
| `/category/writing` | 1 | 3 | 86.7 | - |
| `/tools/ailice` | 1 | 2 | 44.5 | - |
| `/tools/wrenai` | 1 | 4 | 21.8 | - |
| `/about` | 0 | 12 | 3.2 | - |
| `/ai-policy` | 0 | 2 | 4.0 | - |
| `/alternatives/cursor-alternatives` | 0 | 2 | 1.0 | - |
| `/blog/adobe-firefly-review-2026` | 0 | 32 | 6.4 | - |
| `/blog/ai-coding-tools-comparison-2026` | 0 | 14 | 26.6 | - |
| `/blog/ai-tools-comparison-2026` | 0 | 2 | 6.5 | - |
| `/blog/ai-tools-for-beginners-2026` | 0 | 30 | 26.2 | - |
| `/blog/ai-tools-review-guide-2026` | 0 | 5 | 132.0 | - |

## 新发现（基于实时数据，15:00 那轮没看到的）

### P0：/compare 排名继续下滑
- 上次报告：pos 33.8 / 272 impr
- 实时数据：pos **38.8** / 212 impr
- **排名 10 天内又掉了 5 位**，且曝光减少 60——说明不是波动，是持续被算法降权

### P1："/blog/best-ai-voice-changers-2026" 是唯一亮点
- 68 impr / 2 clicks / pos 16.5
- 这是全站唯一稳定进前 20 的内容页
- 优先投入：把它推到 pos 10 以内，预计 CTR 从 2.9% 升到 8-10%

### P1："ai agent" 词簇有 10 impr 但 pos 94.7
- 有真实搜索需求，但内容完全不匹配
- 说明站点在 "ai agent" 主题下的内容质量不够，进不了前 50
- **机会**：如果能把 /category/agent 或相关文章优化到 pos 30，能拿到一波长尾流量

### 已验证：GSC API 拉数链路可用
- 凭证：`.secrets/gsc-service-account.json`
- 代理：`127.0.0.1:7890`（Clash）
- 脚本：`iteration_center/_pull_gsc_via_proxy.py`
- 下次定时任务可以直接用这个脚本拉实时数据，不再依赖 GitHub Actions 落地报告

---

*本报告由 GSC API 实时数据生成，非 GitHub Actions 落地报告。*


---

## GA4 实时数据（28 天：9/10 - 10/7）

**Property**: `properties/556518278`（aitoolcrux）
**原始数据**: `ga4_live_20261009_1503.json`

### 总览

| 指标 | 值 | 健康度 |
|---|---|---|
| Sessions | 1603 | - |
| Users | 1598 | - |
| New Users | 1596（99.9%） | 🔴 几乎 0 回访 |
| Engaged Sessions | 127 | - |
| **Engagement Rate** | **7.9%** | 🔴 远低于 30% 行业基准 |
| Avg Session Duration | 10.5s | 🔴 极短 |
| 日均 Sessions | 57 | - |

### 每日趋势（14 天）

| 日期 | Sessions | Users | Engaged |
|---|---|---|---|
| 2026-09-29 | 12 | 12 | 3 |
| 2026-09-30 | 22 | 22 | 2 |
| 2026-10-01 | 83 | 83 | 2 |
| 2026-10-02 | 25 | 25 | 4 |
| 2026-10-03 | 893 | 891 | 66 | 🔥
| 2026-10-04 | 147 | 147 | 11 |
| 2026-10-05 | 168 | 167 | 17 |
| 2026-10-06 | 145 | 144 | 13 |
| 2026-10-07 | 109 | 109 | 9 |

**10/3 异常爆发**：893 sessions（其他天日均 ~100），疑似被某外部链接/Reddit/HN 推荐带量，需查 referral 来源。

### Top Landing Pages

| 页面 | Sessions | Engaged | Engagement Rate |
|---|---|---|---|
| `(not set)` | 240 | 1 | 0% 🔴 |
| `/` | 67 | 22 | 33% ✅ |
| `/blog/suno-alternatives` | 30 | 22 | 73% ✅ |
| `/blog/perplexity-ai-review-2026` | 28 | 0 | 0% 🔴 |
| `/blog/best-ai-productivity-tools-2026` | 12 | 1 | 8% |
| `/blog/stable-diffusion-alternatives-2026` | 12 | 2 | 17% |
| `/blog/midjourney-alternatives-2026` | 11 | 1 | 9% |
| `/blog/best-ai-video-generators-2026` | 10 | 2 | 20% |
| `/tools/midjourney` | 10 | 3 | 30% |
| `/blog/best-ai-coding-tools-2026` | 8 | 0 | 0% 🔴 |
| `/blog/dify-vs-coze-2026-comparison` | 8 | 1 | 12% |
| `/blog/canva-ai-vs-adobe-firefly-2026-comparison` | 7 | 1 | 14% |
| `/blog/elevenlabs-review-2026` | 7 | 1 | 14% |
| `/blog/midjourney-free-trial-2026` | 7 | 0 | 0% 🔴 |
| `/blog/notion-ai-review-2026` | 7 | 2 | 29% |


### P0：GA4 vs GSC 严重不匹配

- **GSC 说**：/compare 28 天 212 impressions、2 clicks；/blog/best-ai-voice-changers-2026 68 impr、2 clicks
- **GA4 说**：/compare 和 voice-changers 都没进 top landing 15
- **结论**：GSC 给的曝光大部分没转化成真实 session，或落地页加载/追踪有问题

### P0：22.6% 的 landing page 是 `(not set)`
- 240 / 1063 sessions 没有正确的 landing page 标记
- 说明 gtag/GA4 配置有 bug，可能是 SPA 路由变化没触发 page_view

### P1：`/blog/suno-alternatives` 是唯一健康页
- 30 sessions / 22 engaged / 73% engagement rate
- 但 GSC 里这个词没出现——说明流量不是 Google 自然搜索来的（可能直接/社媒/referral）
- **机会**：分析这 30 个 session 从哪来，复制这个引流路径

### P1：99.9% 是新用户
- 1596 / 1598 是新用户——网站几乎没有回访
- 冷启动期正常，但内容留存力不足（10.5 秒就走了）

---

## 综合结论（GSC + GA4）

**流量现状**：
- Google 自然搜索：58 impr / 0 clicks（7 天），在枯竭
- 实际 sessions：日均 ~100，但 92% 不互动（engagement rate 7.9%）
- 10/3 有一波外部引流（893 sessions），但不是 Google 来的

**最该做的 3 件事**：
1. 🔴 **修 GA4 配置**：`(not set)` 占 22.6% 说明追踪漏了，先把这个修了
2. 🔴 **查 10/3 爆发来源**：893 sessions 从哪来的？如果是 Reddit/HN，复制这个渠道
3. 🟡 **优化 /blog/suno-alternatives**：唯一 73% 互动率的页，把它推成流量主力

