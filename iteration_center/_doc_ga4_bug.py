# -*- coding: utf-8 -*-
"""记录 GA4 追踪 bug 根因 - 2026-10-09"""
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

## [P0] GA4 追踪配置 Bug：22-33% landing page 丢失 + 96% 流量误归 direct

**发现时间**: {NOW}
**数据来源**: GA4 API 实时拉取（properties/556518278）+ 代码审查

### 现象

| 指标 | 今天(10/9) | 昨天(10/8) | 28天均值 |
|---|---|---|---|
| landing page = (not set) | 26.5% | 33.3% | 22.6% |
| traffic source = direct | 96% | 99% | ~90% |
| engagement rate | 6.1% | 6.5% | 7.9% |

### 根因（代码级）

**Bug 1: `ga4-init` 脚本加载时序错误**
- 文件: `app/layout.tsx` 第 168 行
- 现状: `<Script id="ga4-init" strategy="afterInteractive">`
- 问题: `afterInteractive` 意味着页面可交互后才执行，此时才定义 `window.gtag`
- 后果: `GA4PageTracker` 第一次 `useEffect` 执行时 `window.gtag` 不存在，直接 return，第一个 page_view 丢失

**Bug 2: `send_page_view: false` 放大了 Bug 1**
- 文件: `app/layout.tsx` 第 173 行
- 现状: `gtag('config', 'G-7XYFQR3ETF', {{ send_page_view: false }})`
- 问题: 自动 page_view 被关闭，完全依赖 GA4PageTracker 手动发
- 后果: 手动发的第一次就丢了，双重保险变成双重漏发

**Bug 3: referrer 丢失导致 96% direct**
- gtag 加载延迟 → referrer 在 gtag 就绪前丢失
- AI 聊天工具（ChatGPT）点击流量 referrer 策略为 no-referrer
- 数据证实: 有 1 个 session 明确来自 chatgpt.com/ai-assistant，但大部分被吞

### 修复方案

**P0 修复（必须）**:
1. `ga4-init` 内联脚本改为 `strategy="beforeInteractive"`，确保 window.gtag 在 React 渲染前存在
2. `GA4PageTracker` 加重试机制: window.gtag 不存在时 setTimeout 100ms 重试，最多 5 次

**P1 修复（建议）**:
3. 或将 `send_page_view` 改回 `true`，让 gtag 自动发第一个 page_view，GA4PageTracker 只处理后续客户端路由
4. 所有外链加 UTM 参数，避免被归为 direct

### 影响评估

- 22-33% 的 session 没有正确的 landing page → 页面级流量分析不可信
- 96% direct → 渠道归因完全失效，无法判断流量从哪来
- engagement rate 7.9% 可能被低估（因为丢失的 page_view 可能是高互动页）

### 验证方法

修复后观察 24 小时:
- landing page = (not set) 应降到 < 5%
- direct 流量应降到 < 60%（新站正常范围）
- total sessions 应增加 10-20%（之前丢失的 page_view 被补回）

""")
print(f"[OK] audit_findings.md appended")

# ========== 更新 state.json ==========
state_path = os.path.join(BASE, "iteration_center", "state.json")
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

# 更新已有 P0-GA4-NOTSET-001 的详情
for item in state.get("next_iteration_focus", []):
    if isinstance(item, dict) and item.get("id") == "P0-GA4-NOTSET-001":
        item["detail"] = "根因已定位: app/layout.tsx ga4-init 用 afterInteractive 导致 window.gtag 加载延迟，GA4PageTracker 第一次 useEffect 因 !window.gtag return，第一个 page_view 丢失。叠加 send_page_view:false 放大问题。修复: 改 beforeInteractive + 加重试。详见 audit_findings.md。"
        item["root_cause_found"] = True
        print(f"[OK] updated {item['id']} with root cause")

state["last_updated"] = NOW
with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f"[OK] state.json updated")

# ========== 追加日志 ==========
log_path = os.path.join(BASE, "window_logs", f"analyst_{TODAY}.md")
with open(log_path, "a", encoding="utf-8") as f:
    f.write(f"""

---

## GA4 Bug 根因定位 - {NOW}

**用户提问**: "为什么会漏页面"
**代码审查**: app/layout.tsx + components/analytics/GA4PageTracker.tsx

**根因**:
1. ga4-init 用 afterInteractive → window.gtag 加载晚
2. GA4PageTracker 第一次 useEffect 时 !window.gtag → return → 第一个 page_view 丢
3. send_page_view:false → 没有自动 page_view 兜底
4. 结果: 22-33% landing page = (not set), 96% 流量 = direct

**产出**:
- audit_findings.md: P0 级 bug 记录 + 修复方案 + 验证方法
- state.json: P0-GA4-NOTSET-001 补充根因
""")
print(f"[OK] log appended")
print("\n=== ROOT CAUSE DOCUMENTED ===")
