# -*- coding: utf-8 -*-
"""更新关键词报告 - 加入 SERP 验证和竞品对比 - 2026-10-09"""
import json, os
from datetime import datetime

BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
TODAY = "2026-10-09"
NOW = datetime.now().isoformat(timespec="seconds")

# SERP 竞争分析结果（基于 general_search 实际搜索）
serp_analysis = {
    "best ai agents 2026": {
        "serp_competitors": ["Manus (manus.im)", "FluxGrowth", "DataCamp", "Taskade", "Product Hunt", "DEV Community"],
        "competition_level": "High",
        "content_gap": "大部分是 2026 年 9 月才发布的新文章，内容还比较浅。缺少独立第三方的深度实测对比。",
        "our_angle": "做 6 维度实测评分（我们的方法论），对比 Manus/Claude Cowork/ChatGPT Agent/Devin 等实际产品",
        "serp_date": "2026-10-09",
    },
    "ai agent vs chatbot": {
        "serp_competitors": ["TechTarget", "Kayako", "Adobe", "DevRev", "agent-hq.io", "cloudybot.ai"],
        "competition_level": "Medium",
        "content_gap": "大部分是 B2B 企业视角，缺少面向普通用户的通俗解释和实例对比。",
        "our_angle": "用具体例子（ChatGPT vs Manus）说明区别，加决策树'你该用哪个'",
        "serp_date": "2026-10-09",
    },
    "how to build an ai agent": {
        "serp_competitors": ["Google Codelabs", "Microsoft Copilot Studio", "Bubble", "Dust.tt", "Dualite", "fleeceai.app"],
        "competition_level": "Medium-Low",
        "content_gap": "大部分是官方文档或单一平台教程，缺少多平台横向对比和选择指南。",
        "our_angle": "对比 5 个 no-code 平台（Zapier Agents/Make/Dust/Bubble/Taskade），给出选择矩阵",
        "serp_date": "2026-10-09",
    },
    "best ai comparison tools": {
        "serp_competitors": ["comparethe.ai", "zerotwo.ai", "toolchase.com", "aizolo.com (模型对比)"],
        "competition_level": "Low",
        "content_gap": "SERP 里没有专门的'best ai comparison tools'文章，都是 AI 工具对比本身。这是蓝海词。",
        "our_angle": "评测 5 个 AI 工具对比平台（comparethe.ai/toolchase/topai.tools/ours），告诉用户哪个最准",
        "serp_date": "2026-10-09",
    },
    "best ai voice changer for content creators": {
        "serp_competitors": ["TechTimes", "Dubbing AI (多语言 SEO 轰炸)", "CapCut", "Nerdynav", "GenMediaLab"],
        "competition_level": "Medium",
        "content_gap": "Dubbing AI 在做 SEO 轰炸但内容自卖自夸，缺少客观第三方实测。",
        "our_angle": "实测 8 个 voice changer 的延迟/音质/价格，加音频样本对比",
        "serp_date": "2026-10-09",
    },
    "suno alternatives 2026": {
        "serp_competitors": ["HitPaw", "AIUnpacker", "olud.ai", "DEV Community", "theairankings.com", "yuzec.com"],
        "competition_level": "High",
        "content_gap": "竞争激烈，但我们已有文章且 GA4 互动率 57.5%。需要更新 2026 年最新工具（Google Lyria 3/ACE-Step/HeartMuLa）。",
        "our_angle": "更新现有文章，加 2026 Q3 新工具，保持互动率优势",
        "serp_date": "2026-10-09",
    },
}

# 竞品对比
competitor_analysis = {
    "futurepedia.io": {
        "categories_count": "30+",
        "has_ai_agents_category": False,
        "has_voice_changer_category": False,
        "has_music_generator": True,
        "has_no_code": True,
        "content_types": ["工具目录", "课程教程"],
        "our_gaps": ["AI Agents 专门分类", "Voice Changer 专门分类", "深度评测文章"],
    },
    "topai.tools": {
        "tools_count": "23,522+",
        "categories_count": "120+",
        "has_ai_agents_category": False,
        "has_voice_changer_category": False,
        "content_types": ["工具目录", "Tool Playbooks (分步指南)", "Top 100 排名", "Trending Models"],
        "our_gaps": ["Tool Playbooks 分步指南", "AI Agents 专门内容", "Top Growing 工具追踪"],
    },
    "theresanaiforthat.com": {
        "status": "抓取被安全策略拦截，待补充",
        "our_gaps": ["待补充"],
    },
}

# 读现有报告
report_path = os.path.join(BASE, "iteration_center", "keyword_opportunities.md")
with open(report_path, "r", encoding="utf-8") as f:
    existing = f.read()

# 在报告末尾追加 SERP 验证和竞品对比
appendix = f"""

---

## 七、SERP 竞争验证（2026-10-09 实际搜索）

> 以下数据来自 general_search 实际搜索每个 P0 关键词的 Google SERP 前 10 结果。

| 关键词 | 竞争度 | 主要竞品 | 内容缺口 | 我们的切入角度 |
|---|---|---|---|---|
"""
for kw, data in serp_analysis.items():
    comps = ", ".join(data["serp_competitors"][:4])
    appendix += f"| `{kw}` | {data['competition_level']} | {comps} | {data['content_gap']} | {data['our_angle']} |\n"

appendix += f"""
### SERP 验证结论

1. **best ai comparison tools 是蓝海**：SERP 前 10 没有专门文章，竞争最低
2. **ai agent vs chatbot / how to build an ai agent 竞争中等**：有内容但角度单一，我们可以做差异化
3. **best ai agents 2026 / suno alternatives 竞争高**：需要做深度实测才能突围
4. **voice changer 有 Dubbing AI SEO 轰炸**：但内容自卖自夸，客观实测有机会

---

## 八、竞品内容覆盖对比（2026-10-09 实际抓取）

| 维度 | futurepedia.io | topai.tools | AIToolCrux (我们) |
|---|---|---|---|
| 工具数量 | 数千 | 23,522+ | ~500 |
| 分类数 | 30+ | 120+ | ~15 |
| AI Agents 专门分类 | ❌ 无 | ❌ 无（只有 Chatbot builder） | ❌ 无 |
| Voice Changer 专门分类 | ❌ 无 | ❌ 无 | ❌ 无 |
| Music Generator | ✅ | ✅ | ✅ |
| 深度评测文章 | ❌ 主要是目录 | ❌ 主要是目录 | ✅ 我们的核心 |
| Tool Playbooks（分步指南） | ❌ | ✅ 有 | ❌ 无 |
| Top Growing 追踪 | ❌ | ✅ 有 | ❌ 无 |

### 竞品对比发现的内容缺口

1. **AI Agents 是三方共同缺口**：futurepedia 和 topai.tools 都没有专门分类，我们可以抢占
2. **Voice Changer 是三方共同缺口**：没有竞品做专门分类页
3. **Tool Playbooks 是内容类型缺口**：topai.tools 有但我们没有，可以做"如何用 XX 工具完成 YY"系列
4. **深度评测是我们的差异化优势**：竞品主要是目录，我们的 6 维度评测是护城河

---

## 九、调研验证总结

| 验证项 | 状态 | 说明 |
|---|---|---|
| GSC 实时数据 | ✅ 已验证 | 20 queries + 15 pages，28天 |
| GA4 页面表现 | ✅ 已验证 | engagement rate 交叉验证 |
| SERP 竞争分析 | ✅ 已验证 | 6 个 P0 词全部实际搜索 |
| 竞品内容覆盖 | ✅ 已验证 | futurepedia + topai.tools 实际抓取 |
| 真实搜索量 | ⚠️ 预估 | 无第三方 API，基于 GSC 曝光+SERP 竞争度推断 |
| theresanaiforthat | ⚠️ 未抓取 | 被安全策略拦截，下次用 browser-use |

**报告更新时间**: {NOW}
"""

with open(report_path, "w", encoding="utf-8") as f:
    f.write(existing + appendix)
print(f"[OK] keyword_opportunities.md updated with SERP + competitor analysis")

# ========== 更新 state.json 里的 P0 待办，加入 SERP 验证信息 ==========
state_path = os.path.join(BASE, "iteration_center", "state.json")
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

updated = 0
for item in state.get("next_iteration_focus", []):
    if isinstance(item, dict) and item.get("source") == f"keyword_mining_{TODAY}" and item.get("priority") == "P0":
        kw = item.get("keyword", "")
        if kw in serp_analysis:
            item["serp_competition"] = serp_analysis[kw]["competition_level"]
            item["serp_verified"] = True
            item["serp_date"] = "2026-10-09"
            item["our_angle"] = serp_analysis[kw]["our_angle"]
            updated += 1

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f"[OK] {updated} P0 todos updated with SERP verification data")

# ========== 追加日志 ==========
log_path = os.path.join(BASE, "window_logs", f"analyst_keyword_{TODAY}.md")
with open(log_path, "a", encoding="utf-8") as f:
    f.write(f"""

---

## 补充调研验证 - {NOW}

**用户要求**: 关键词挖掘需要经过大量调研和验证

**补充完成**:
1. SERP 竞争分析：6 个 P0 词全部用 general_search 实际搜索，记录前 10 竞品
2. 竞品抓取：futurepedia.io（sitemap 30+分类）+ topai.tools（23522工具/120分类）
3. theresanaiforthat.com 被安全策略拦截，未抓取

**关键发现**:
- best ai comparison tools 是蓝海（SERP 无专门文章）
- AI Agents 是 futurepedia + topai.tools 共同缺口
- Tool Playbooks 是 topai.tools 有但我们没有的内容类型
- 深度评测是我们的差异化优势

**更新**:
- keyword_opportunities.md 新增第七、八、九章（SERP验证+竞品对比+调研总结）
- state.json 6 条 P0 待办补充 serp_competition / serp_verified / our_angle
""")

print(f"[OK] log appended")
print("\n=== RESEARCH VALIDATION COMPLETE ===")
