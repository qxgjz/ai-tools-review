# -*- coding: utf-8 -*-
"""记录真实用户分析 - 2026-10-09"""
import json, os
from datetime import datetime

BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
TODAY = "2026-10-09"
NOW = datetime.now().isoformat(timespec="seconds")

# ========== 追加 audit_findings ==========
audit_path = os.path.join(BASE, "iteration_center", "audit_findings.md")
with open(audit_path, "a", encoding="utf-8") as f:
    f.write(f"""

---

## [P0] GA4 流量中 85% 为 Bot/自动化流量，真实用户仅 ~250

**发现时间**: {NOW}
**数据来源**: GA4 API 实时拉取（properties/556518278，28天 9/11-10/8）
**分析方法**: 多维度交叉验证（国家+设备+浏览器+时间+来源）

### 现象

| 指标 | 数值 | 正常范围 | 判断 |
|---|---|---|---|
| Total Sessions | 1,712 | - | - |
| 新加坡占比 | 85.5% (1,466) | <10% | 🔴 异常 |
| Chrome 占比 | 97.5% (1,670) | 65-75% | 🔴 异常 |
| UTC 6:00 单小时占比 | 46% (792) | <10% | 🔴 异常 |
| direct 流量占比 | 97.7% (1,680) | 30-50% | 🔴 异常 |
| Engagement Rate | 7.8% | 30-50% | 🔴 异常 |

### Bot 流量判定依据

1. **地理异常**: 英文 AI 工具评测站，85% 用户来自新加坡（AWS/GCP 云服务器集中地）
2. **浏览器异常**: 97.5% Chrome，无 Safari/Firefox/Edge 正常分布
3. **时间异常**: UTC 6:00（北京时间 14:00）单小时 792 sessions，其他时间 30-50
4. **来源异常**: 97.7% direct，无 referrer
5. **行为异常**: 平均停留 7.8 秒，engagement 仅 6%（桌面端）

### 真实用户估算

扣除新加坡 bot 流量后：

| 来源 | Sessions | Engagement | 质量评级 |
|---|---|---|---|
| 美国 | 110 | 30% | ✅ 真实 |
| 中国 | 56 | 32% | ✅ 真实 |
| ChatGPT (ai-assistant) | 28 | 68% | ✅✅ 最高质量 |
| 其他国家 | ~80 | - | ✅ 部分真实 |
| Bing organic | 3 | 100% | ✅ |
| **真实用户合计** | **~250-280** | - | - |

### 真实用户关键特征

| 维度 | 发现 |
|---|---|
| 设备 | Mobile engagement 46% vs Desktop 6%（移动端质量高 7 倍） |
| 来源 | ChatGPT 来的用户 68% engagement，全站最高质量渠道 |
| 页面 | /blog/suno-alternatives 57.5% engagement，唯一健康页 |
| 时间 | 真实用户活跃在 UTC 10-21 点（北京时间 18:00-次日 5:00） |
| 回访 | 仅 5 个回访用户（0.3%），内容留存力几乎为 0 |

### 附带发现：URL 重复 Bug

Top pages 同时出现：
- `/blog/suno-alternatives/`（40 pageviews）
- `/blog/suno-alternatives-2026/`（9 pageviews）

同一篇文章两个 URL，trailing slash 和 canonical 配置问题，分散 SEO 权重。

### 修复建议

**P0（工程师）**:
1. GA4 后台开启 Bot 过滤（Admin → Property Settings → Bot Filtering）
2. 服务端过滤新加坡云服务商 IP 段（AWS ap-southeast-1, GCP asia-southeast1）
3. 修 URL canonical：统一 trailing slash 策略，301 重定向重复 URL

**P1（增长黑客）**:
4. ChatGPT 带来 28 个高质量 session（68% engagement），研究如何让 ChatGPT 更多引用本站
5. 提交站点到 AI 搜索引擎（Perplexity、ChatGPT 插件目录等）

**P1（创作家）**:
6. suno-alternatives 57.5% engagement，复制内容模板到其他 alternatives 文章
7. 优化移动端体验（mobile 用户 engagement 是 desktop 的 7 倍）

**P1（分析师）**:
8. 后续报告区分 bot/真实用户，不要被总 sessions 数字误导
9. 建立"真实用户"基线：~250/28天，日均 ~9 个真实用户

### 验证方法

修复后观察 7 天：
- 新加坡流量占比应降到 < 15%
- Chrome 占比应降到 70-80%
- UTC 6:00 高峰应消失
- direct 流量应降到 50-70%
- engagement rate 应升到 20%+（因为过滤了 bot）

""")
print(f"[OK] audit_findings.md appended (bot traffic analysis)")

# ========== 更新 state.json ==========
state_path = os.path.join(BASE, "iteration_center", "state.json")
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

# 新增待办
new_todos = [
    {
        "id": "P0-BOT-FILTER-001",
        "assigned_to": "工程师",
        "title": "GA4 开启 Bot 过滤 + 服务端过滤新加坡云 IP",
        "detail": "85% 流量来自新加坡（1466/1712），97.5% Chrome，UTC 6:00 单小时 46%，判定为 bot。GA4 后台开 Bot Filtering，服务端过滤 AWS ap-southeast-1 / GCP asia-southeast1 IP 段。",
        "status": "open",
        "created": TODAY,
        "evidence": "GA4 28d data: Singapore 1466, Chrome 1670, UTC6 792 sessions",
    },
    {
        "id": "P0-URL-CANONICAL-001",
        "assigned_to": "工程师",
        "title": "修复 URL 重复：suno-alternatives 有两个 URL",
        "detail": "/blog/suno-alternatives/ (40pv) 和 /blog/suno-alternatives-2026/ (9pv) 同时存在。统一 trailing slash 策略，301 重定向。检查全站是否有其他重复 URL。",
        "status": "open",
        "created": TODAY,
    },
    {
        "id": "P1-CHATGPT-REFERRAL-001",
        "assigned_to": "增长黑客",
        "title": "研究 ChatGPT 引用机制，扩大 AI 搜索流量",
        "detail": "ChatGPT 带来 28 个 session，68% engagement（全站最高）。研究：1) 哪些页面被 ChatGPT 引用 2) 如何让更多页面被引用 3) 提交到 Perplexity/ChatGPT 插件目录",
        "status": "open",
        "created": TODAY,
    },
    {
        "id": "P1-MOBILE-OPTIMIZE-001",
        "assigned_to": "工程师",
        "title": "优化移动端体验（mobile engagement 是 desktop 的 7 倍）",
        "detail": "Mobile engagement 46% vs Desktop 6%，avg duration 55s vs 8s。移动端用户质量远高，但只占 4.8% 流量。优化移动端 LCP/CLS，可能带来更多 mobile 流量。",
        "status": "open",
        "created": TODAY,
    },
]
state.setdefault("next_iteration_focus", []).extend(new_todos)
print(f"[OK] added {len(new_todos)} new todos")

# 更新关键指标
state["real_users_28d"] = "~250-280 (excluding ~1466 Singapore bot traffic)"
state["bot_traffic_pct"] = "85.5%"
state["highest_quality_channel"] = "ChatGPT (ai-assistant): 28 sessions, 68% engagement"
state["last_updated"] = NOW

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f"[OK] state.json updated")

# ========== 追加日志 ==========
log_path = os.path.join(BASE, "window_logs", f"analyst_{TODAY}.md")
with open(log_path, "a", encoding="utf-8") as f:
    f.write(f"""

---

## 真实用户深度分析 - {NOW}

**用户提问**: "真实用户情况怎么样"
**分析维度**: 设备/国家/来源/浏览器/时间/页面 6 维交叉

**重大发现**:
- 85.5% 流量是 bot（新加坡 1466 + Chrome 97.5% + UTC6 爆发 46% + direct 97.7%）
- 真实用户仅 ~250-280/28天，日均 ~9 人
- ChatGPT 来源 68% engagement（全站最高）
- Mobile engagement 46% vs Desktop 6%
- suno-alternatives 57.5% engagement（唯一健康页）
- 发现 URL 重复 bug（suno-alternatives 两个 URL）

**新增待办**:
- P0-BOT-FILTER-001: GA4 bot 过滤 + 新加坡云 IP 过滤
- P0-URL-CANONICAL-001: 修 URL 重复
- P1-CHATGPT-REFERRAL-001: 扩大 AI 搜索流量
- P1-MOBILE-OPTIMIZE-001: 优化移动端

**产出**:
- audit_findings.md: P0 bot 流量分析
- state.json: 4 条新待办 + 真实用户基线
""")
print(f"[OK] log appended")
print("\n=== REAL USER ANALYSIS DOCUMENTED ===")
