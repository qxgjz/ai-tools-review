# -*- coding: utf-8 -*-
"""r45 收尾：闭环 P0-GSC-REVIEW-20261103（10-31 回填 2 仍低位）+ 竞品 0 新（teachers 被 batch74 覆盖）+ CTR 0 新"""
import json, os, shutil
from datetime import datetime

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
NOW = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

# ===== 1. state.json =====
sp = os.path.join(P, 'iteration_center', 'state.json')
with open(sp, encoding='utf-8') as f:
    d = json.load(f)
nf = d['next_iteration_focus']

GSC_EV = ('r45 正式复查（11-02 预执行，GSC 重跑 10-02~10-31 窗口，数据回填）：10-31 曝光回填 1→2 仍低位；'
          '峰后 10-28/29/30/31=4/1/1/2 **连续 4 天 <5 无回升**；窗口总量 156 imp / pos 15.56 较 r44（154/15.75）'
          '曝光 +2、位置 +0.19，持平略升但无实质恢复。结论：**曝光断崖未恢复**（r73 auto_redirect 修复生效但索引/排名恢复滞后）；'
          '11-03 后若窗口滚动至 10-04~11-02 可复查 11-01/11-02 两日是否仍 <5，建议架构师保持监测')

for i in nf:
    if i.get('id') == 'P0-GSC-REVIEW-20261103':
        i['status'] = 'completed'
        i['completed_at'] = NOW
        i['evidence'] = GSC_EV
        i['closed_by'] = 'analyst_r45'
        break

with open(sp, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
pend = len([i for i in nf if i.get('status') == 'pending'])
print('state: focus=%d pending=%d' % (len(nf), pend))

# ===== 2. latest_report.md 更新（同窗口重跑已更新数据）=====
shutil.copyfile(os.path.join(P, 'gsc-ga4-report', '2026-10-02_2026-10-31.md'),
                os.path.join(P, 'gsc-ga4-report', 'latest_report.md'))
print('latest_report.md 已同步（156 imp / pos 15.56）')

# ===== 3. audit_findings.md r45 段 =====
open(os.path.join(P, 'iteration_center', 'audit_findings.md'), 'a', encoding='utf-8').write("""

## r45（2026-11-02 晚档 · 分析师-数据洞察 SOP 触发）

### P0 GSC-REVIEW-20261103 正式复查（闭环）
- GSC 重跑窗口 10-02~10-31（数据回填）：**10-31 曝光 1→2 仍低位**，峰后 10-28/29/30/31=4/1/1/2 连续 4 天 <5
- 窗口 156 imp / pos 15.56（r44 154/15.75：曝光 +2、位置 +0.19）——持平略升，**无实质恢复**
- 结论：**曝光断崖未恢复**（r73 修复生效但索引/排名层恢复滞后）；11-03 后窗口滚动可复查 11-01/11-02

### P2 竞品差距收窄（batch74 覆盖）
- 竞品 GAP 10→9：**teachers 缺口已被 batch74 的 best-ai-tools-for-teachers 覆盖**；结构性缺口（课程/教程）也已由 best-free-ai-courses 补上

### P1 CTR 候选池耗尽（0 新开）
- 新窗口 8 个 rank 4-20 候选（首页 5.2/ai-policy 8.0/guide 10.0/comparison 18.0/marketing 8.0/meeting 9.0/observability 9.5/productivity 10.5）**全部已被历史 13 张 pending 覆盖**
- 需打磨师批量执行后才能释放新候选；积压本身是风险项
""")

# ===== 4. keyword_opportunities.md r45 段 =====
open(os.path.join(P, 'iteration_center', 'keyword_opportunities.md'), 'a', encoding='utf-8').write("""

## r45（2026-11-02 晚档 · 复核轮）

- GSC Easy Wins：aizolo reviews pos 22（imp 1）不足 5 跳过；tabbyml pos 18 已开 CTR 单
- 竞品缺口 0 新（GAP 9 全历史覆盖；teachers 已被 batch74 覆盖，缺口池收窄）
- CTR 候选 0 新（13 张历史单未执行，候选池耗尽）
- Total keywords analyzed：6 查询 + 77 竞品分类
""")

# ===== 5. competitor_analysis_2026-11-02.md r45 段（append，同日期）=====
open(os.path.join(P, 'iteration_center', 'competitor_analysis_2026-11-02.md'), 'a', encoding='utf-8').write("""

## r45 段（11-02 晚档复抓）
- GAP 9 条（chatbots2/productivity/workflows/religion/marketing/automations/human-resources/presentations/transcriber）——全历史覆盖 → **0 新**
- 变化：teachers 缺口消失（batch74 已发布 best-ai-tools-for-teachers）；结构性课程缺口已由 best-free-ai-courses 覆盖 → 竞品差距收窄
- SERP 验证：无（0 新缺口词）
""")

# ===== 6. 双日志 append r45 段 =====
open(os.path.join(P, 'window_logs', 'analyst_2026-11-02.md'), 'a', encoding='utf-8').write("""

## r45 段（11-02 晚档触发）
- 执行待办：**1 条闭环**（P0-GSC-REVIEW-20261103：10-31 回填 2 仍低位、连续 4 天 <5、窗口 156/15.56 无回升 → 断崖未恢复）
- 阻塞未变：P1-GEO-BASELINE-AUDIT（需登录态）、P1-TOOL-ELMO（需 Docker）、P1-REQ13-BAML（等创作家/架构师）
- 新发现：**1 条**（竞品差距收窄：teachers 缺口被 batch74 覆盖，GAP 10→9）
- CTR 新开单：**0 张**（候选池 8 项全被历史 13 张覆盖，需打磨师批量执行）
- 挖词 0；竞品缺口 0 新；SERP 0；Easy Wins 跳过
- 剩余 pending：PENDING_N（脚本复核）
- 环境：GSC 窗口未滚动（10-02~10-31）但数据回填；代理正常；ego-browser 不可用（requests 实抓替代）
""".replace('PENDING_N', str(pend)))

open(os.path.join(P, 'window_logs', 'analyst_keyword_2026-11-02.md'), 'a', encoding='utf-8').write("""

## r45 段（复核轮）
1. 竞品挖词：OK 77 分类复抓，GAP 9 全历史覆盖 → 0 新（teachers 已由 batch74 覆盖）
2. Easy Wins：OK aizolo pos22 imp1 不足 5 跳过
3. 扩展/分级/SERP：无新候选，跳过
4. 输出：OK keyword_opportunities.md r45 段
""")
print('r45 files written')
