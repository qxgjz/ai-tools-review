# -*- coding: utf-8 -*-
"""r43 收尾：闭环 P0-GSC-DROP-REINVESTIGATE + P0-SOURCE-VALIDATION（分析师部分）+ 产出/日志追加"""
import json, os
from datetime import datetime

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
NOW = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

# ===== 1. state.json =====
sp = os.path.join(P, 'iteration_center', 'state.json')
with open(sp, encoding='utf-8') as f:
    d = json.load(f)
nf = d['next_iteration_focus']

GSC_EV = ('r43 分析师排查完成（11-01）：①sitemap 拉取正常——GSC sitemaps 页 submitted=950/已发现网页=950、'
          '状态成功、上次读取 2026-11-01（AdsPower CDP 实抓）；②核心服务响应全 200——线上 sitemap.xml 952 URLs 200 XML、'
          '首页/3 个博客页 200、无尾斜杠 301→带斜杠 200；③public/_redirects Cloudflare 规则齐全（/tools、Blog 301、Category）；'
          '结论：断崖非 sitemap/响应/重定向三层问题，指向 auto_redirect 事件后排名/索引层影响，修复已生效但曝光恢复滞后。'
          '48h 复查点：2026-11-03 再看 10-31~11-02 三日曝光是否回升。根因报告见 audit_findings r43 段')
SRC_EV = ('r43 源头校验落地（11-01）：scripts/analyst_source_validator.py 实跑——生成源待办 91 条（keyword_mining/'
          'competitor_analysis/ctr_optimization）缺 title 91/91（100%，task 全有）；建议 slug 与 posts.json 283 篇冲突 0；'
          '全库缺 title 或 desc/task 共 409 条。结论：源头只写 task 不写 title 是规范缺口主因，slug 合规。'
          '历史单补齐为创作家职责（window2/创作家），校验器可复用于未来生成')

for i in nf:
    if i.get('id') == 'P0-GSC-DROP-REINVESTIGATE-20261101':
        i['status'] = 'completed'
        i['completed_at'] = NOW
        i['evidence'] = GSC_EV
        i['closed_by'] = 'analyst_r43(分析师部分；架构师 48h 复查 11-03)'
    elif i.get('id') == 'P0-SOURCE-VALIDATION-20261101':
        i['status'] = 'completed'
        i['completed_at'] = NOW
        i['evidence'] = SRC_EV
        i['closed_by'] = 'analyst_r43(校验器+实测；创作家补齐历史单)'

with open(sp, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
pend = len([i for i in nf if i.get('status') == 'pending'])
print('state: focus=%d pending=%d' % (len(nf), pend))

# ===== 2. audit_findings.md r43 段 =====
open(os.path.join(P, 'iteration_center', 'audit_findings.md'), 'a', encoding='utf-8').write("""

## r43（2026-11-01 15:3x · 分析师-数据洞察 SOP 触发）

### P0-1 GSC 断崖根因再排查（联合任务·分析师部分完成）
| 排查层 | 实测结果 | 判定 |
|---|---|---|
| sitemap 拉取 | GSC sitemaps submitted=950/已发现 950，状态成功，上次读取 2026-11-01（CDP 实抓） | ✅ 正常 |
| 线上 sitemap | 952 URLs，200 XML（requests 走代理 7890） | ✅ 正常 |
| 核心服务响应 | 首页/3 博客页 200，无尾斜杠 301→带斜杠 | ✅ 正常 |
| _redirects | public/_redirects Cloudflare 规则齐全（/tools、Blog 301、Category slugs） | ✅ 正常 |

**结论**：断崖非 sitemap/响应/重定向三层问题，指向 auto_redirect 9 月下旬暴增事件后排名/索引层影响——r73 修复已生效但曝光恢复滞后（10-26/27 峰 18/16 后 10-28~30 骤降 4/1/1）。**48h 复查点：2026-11-03** 看 10-31~11-02 三日曝光。

### P0-2 REQ13 预检（11-02 正式验证前一天）
- 线上 sitemap 952 URLs 中：exa/claude/suno/kagi/llama-cpp/vllm/lobe-chat/langchain/crewai/deepeval/pr-agent/promptfoo **12/12 全部在站**（含 /tools/ 页）
- **⚠ baml 页 MISSING**：本地 posts.json 283 篇 0 命中、线上 sitemap 无 /tools/baml/——若 REQ13 名单含 baml 需先补页，正式验证将失败

### P0-3 源头规范缺口确证（P0-SOURCE-VALIDATION 分析师部分）
- scripts/analyst_source_validator.py 实跑：生成源待办 91 条 **缺 title 91/91（100%）**、task 全有、slug 冲突 0、全库缺 title/desc 409 条
- 根因：keyword_mining/competitor_analysis 生成路径只写 task 不写 title → 校验器已落地可复用

### 数据口径
- GSC 窗口未滚动（10-01~10-30 同 r42）：155 imp / 0 clk / pos 15.66，重跑确认无回填变化；CTR 新候选 0（r42 已开 marketing-tools/tabbyml）
- 竞品复抓：77 分类 GAP 11 全历史覆盖 → 0 新
""")

# ===== 3. keyword_opportunities.md r43 段 =====
open(os.path.join(P, 'iteration_center', 'keyword_opportunities.md'), 'a', encoding='utf-8').write("""

## r43（2026-11-01 · 复核轮）

- GSC 窗口未滚动（155 imp/pos 15.66 同 r42），Easy Wins 候选仍仅 aizolo reviews(pos22)，不足 5 个跳过
- 竞品缺口 0 新；无新 P0 关键词（不硬凑，符合禁止假完成）
- REQ13 预检：12 核心工具页在 sitemap，baml 待确认
- Total keywords analyzed：6 查询 + 77 竞品分类
""")

# ===== 4. competitor_analysis_2026-11-01.md =====
open(os.path.join(P, 'iteration_center', 'competitor_analysis_2026-11-01.md'), 'w', encoding='utf-8').write("""# 竞品分析 r43（2026-11-01）

## 竞品内容矩阵（futurepedia 复抓，requests+proxy 7890）
| 维度 | futurepedia | aitoolcrux |
|---|---|---|
| sitemap 总 URL | 635（2026-10-28 结构，courses=531 83.6%） | 952 |
| /ai-tools/ 分类 | 77 | 本地 243 md 对应 |
| 主题结构 | 课程主导（变现=课程） | blog 评测主导 |
| 内容类型 | best/alternatives/vs + 课程/教程 | best/alternatives/vs 评测 |

## 内容缺口
- GAP 11 条（chatbots 2、productivity/workflows/religion/marketing/automations/human-resources/presentations/legal/teachers/transcriber 各 1）——逐条核实**全部已被历史 CA/KW 覆盖** → **0 新缺口**
- 结构性缺口（非分类）：课程/教程类内容我们 0（CA 3 条已开：tool-tutorial/free-courses/productivity 聚合页）

## SERP 验证
无（0 新缺口词，不编造）
""")

# ===== 5. 日志 append r43 段 =====
open(os.path.join(P, 'window_logs', 'analyst_2026-11-01.md'), 'a', encoding='utf-8').write("""

## r43 段（同日第二次触发，15:3x）
- 执行待办：**2 条闭环**（P0-GSC-DROP-REINVESTIGATE-20261101：三层排查全健康+根因报告；P0-SOURCE-VALIDATION-20261101：校验器落地 91/91 缺 title）+ REQ13 预检（12/13 在站，baml MISSING 预警）
- 新发现：**2 条 P0**（①断崖非 sitemap/响应/重定向层，48h 复查 11-03；②baml 页缺失）
- CTR 新开单 0（窗口未滚动，r42 已开 2 条）；挖词 0；竞品缺口 0 新；SERP 0
- 剩余 pending：%d（脚本复核）
- 环境：GSC 同窗口 155/15.66（重跑确认）；AdsPower/代理正常；ego-browser 不可用
""" % pend)

open(os.path.join(P, 'window_logs', 'analyst_keyword_2026-11-01.md'), 'a', encoding='utf-8').write("""

## r43 段（复核轮）
1. 竞品挖词：✅ 77 分类复抓，0 新
2. Easy Wins：✅ 窗口未滚动，aizolo pos22 不足 5 跳过
3. 扩展/分级/SERP：无新候选，跳过
4. 输出：✅ keyword_opportunities.md r43 段；挖词 0 条写入
""")
print('r43 files written')
