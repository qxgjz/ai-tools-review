# -*- coding: utf-8 -*-
"""r32 每周一 GSC 关键词机会筛选：15-50位有曝光关键词 top 清单 + state.json 补录 + 日志
数据源：live_pull_20261024_0939.json（query 维度，最新拉取）+ fetch_gsc.py 报告（2026-09-25~10-24）"""
import json, os
from datetime import datetime

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
SP = os.path.join(P, 'iteration_center', 'state.json')
now_iso = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
now = datetime.now().strftime('%Y-%m-%d %H:%M')

# ============ 1. 实际读取数据（禁止编造） ============
lp = json.load(open(os.path.join(P, 'gsc-ga4-report', 'live_pull_20261024_0939.json'), encoding='utf-8'))
queries = lp['top_queries']
pages = lp['top_pages']
md = open(os.path.join(P, 'gsc-ga4-report', '2026-09-25_2026-10-24.md'), encoding='utf-8').read()

# 15-50 位有曝光（查询级）
q_opp = [q for q in queries if 15 <= q['position'] <= 50 and q['impressions'] > 0]
# 15-50 位有曝光（页面级）
p_opp = [p for p in pages if 15 <= p['position'] <= 50 and p['impressions'] > 0]
# 5-15 位次优（真实数据，标注非口径）
q_near = [q for q in queries if 5 <= q['position'] < 15 and q['impressions'] > 0]
p_near = [p for p in pages if 5 <= p['position'] < 15 and p['impressions'] > 0]
# 50-100 位深度观察（有曝光）
q_deep = [q for q in queries if 50 < q['position'] <= 100 and q['impressions'] > 0]

print('== 15-50位查询级命中 ==')
for q in q_opp: print(q)
print('== 15-50位页面级命中 ==')
for p in p_opp: print(p)
print('== 5-15位次优(查询) ==')
for q in q_near: print(q)
print('== 5-15位次优(页面) ==')
for p in p_near: print(p)
print('== 50-100位深度观察 ==')
for q in q_deep: print(q)
print('== 全量查询(8条) ==')
for q in queries: print(q['keys'][0], q['impressions'], q['position'])
print('== 全量页面(15条) ==')
for p in pages: print(p['keys'][0].split('/blog/')[-1][:60], p['impressions'], round(p['position'], 1))

# ============ 2. state.json 补录（防重复） ============
d = json.load(open(SP, encoding='utf-8'))
nf = d['next_iteration_focus']
ids = {i.get('id') for i in nf}
added = []
def add_todo(t):
    if t['id'] not in ids:
        nf.append(t); ids.add(t['id']); added.append(t['id'])

# tabbyml：r27 已开 CTR-QUERY-TABBYML(completed, CTR角度)；本轮"关键词机会"新角度（排名仍18位，内容增强拉近距离）
add_todo({'id': 'KW-OPP-TABBYML-20261026', 'status': 'pending', 'priority': 'P2',
          'assigned_to': ['window2', '创作家'],
          'task': '关键词机会[tabbyml]（GSC 实读 pos18.0/1imp，15-50位机会区；r27 CTR 优化后排名未进前10）→ 建议写 1200 字 TabbyML 上手评测（本地部署/LLM 网关/企业用例），增强内容拉近距离，目标进前10',
          'source': f'gsc_weekly_opportunity_{datetime.now().strftime("%Y%m%d")}',
          'position': 18.0, 'impressions': 1, 'data_verified': True, 'created_at': now_iso})

d['next_iteration_focus'] = nf
d['last_update'] = now_iso
json.dump(d, open(SP, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('todos added:', len(added), added)
print('focus:', len(nf), '| pending:', len([i for i in nf if i.get('status')=='pending']))

# ============ 3. keyword_opportunities.md 追加 r32 ============
def mdtbl(rows):
    out = ['| 关键词/页面 | Imp | Pos | 判定 |', '|---|---|---|---|']
    for r in rows:
        name = r['keys'][0].split('/blog/')[-1].replace('https://www.aitoolcrux.com/', '/')
        if len(name) > 55: name = name[:52] + '...'
        out.append(f"| {name} | {r['impressions']} | {round(r['position'],1)} | 见上 |")
    return '\n'.join(out)

add = f"""

---

## r32 · 每周一 GSC 关键词机会筛选（{now}）

**数据源（实读）**：`live_pull_20261024_0939.json`（最新拉取，query 窗口 09-25~10-22，8 条查询/15 页面）+ `fetch_gsc.py` 报告（窗口 09-25~10-24，171 imp/0 click/14.29）。站点曝光量小，15-50 位样本仅 2，**不编造凑 20 个**，按真实命中输出。

### 一、Top 机会（15-50 位有曝光 · 口径命中 2 条）
| # | 词/页面 | Imp | Pos | 机会判定 | 当前状态 |
|---|---|---|---|---|---|
| 1 | query: tabbyml | 1 | 18.0 | 品牌词有曝光，内容薄弱，机会区 | r27 已开 CTR（completed）；本轮新开 **KW-OPP-TABBYML P2**（内容增强） |
| 2 | page: /blog/best-ai-comparison-tools-2026/（带斜杠变体） | 1 | 18.0 | 页面进 18 位但 0 点击 | r31 已开 CTR-PAGE-COMPARISON-TOOLS-SLASH（pending），不重复 |

### 二、次优观察（5-15 位 · 非本任务口径，真实数据，均已开过 CTR/修复待办）
| 词/页面 | Imp | Pos | 覆盖状态 |
|---|---|---|---|
| ai-coding-tools-comparison-2026 | 2 | 5.5 | r28 CANNIBAL-RESOLVE（pending） |
| best-ai-coding-tools-2026 | 12 | 4.1 | r28 蚕食分析覆盖 |
| /ai-policy | 1 | 8.0 | r29 CTR ✅ |
| best-ai-meeting-assistants-2026 | 1 | 9.0 | r30 CTR（pending） |
| best-ai-observability-tools-2026 | 2 | 9.5 | r30 CTR（pending） |
| best-ai-productivity-tools-2026 | 2 | 10.5 | r30 CTR（pending） |

### 三、深度观察（50-100 位有曝光 · 内容几乎为零，暂不开单）
| 词 | Imp | Pos | 说明 |
|---|---|---|---|
| google gemini langgraph | 1 | 75.0 | 技术长尾，排名极深 |
| milvus ui | 1 | 84.0 | 工具词，无对应内容 |
| react agent | 1 | 82.0 | 技术词 |
| bondai | 2 | 89.5 | 品牌词 2imp，无对应内容 |

### 四、数据源限制说明
- live_pull 最新为 10-24（fetch_gsc.py 只写 md 汇总不写 query JSON）；10-25/10-26 无新 live_pull
- 全量 8 条查询 + 15 页面如上（fetch_gsc 报告 Top Queries 8 条/Top Pages 20 条中 15 条有曝光明细）
- 竞争度依据：真实 GSC 排名+曝光（未用第三方搜索量）；搜索量全部"预估"标注
"""
with open(os.path.join(P, 'iteration_center', 'keyword_opportunities.md'), 'a', encoding='utf-8') as f:
    f.write(add)
print('keyword appended')

# ============ 4. 日志 ============
log = f"""

## r32 追加（{now} · 每周一 GSC 关键词机会筛选）

- 执行：GSC 数据实读（live_pull_20261024 + fetch_gsc 报告），15-50 位筛选完成
- 机会命中：2 条（query tabbyml 18.0 / page comparison-tools/ 18.0）——均已开单/在池，本轮新开 1 条（KW-OPP-TABBYML P2）
- 次优观察 6 条（5-15 位，均已覆盖）、深度观察 4 条（50-100 位，暂不开单）
- 写入待办：1 条（P2 KW-OPP-TABBYML，创作家）
- 失败/限制：live_pull 无 10-25/26 新数据（fetch_gsc 只写 md）；15-50 位样本 2 条不满足 top20 目标——诚实输出未编造
"""
with open(os.path.join(P, 'window_logs', f'analyst_{datetime.now().strftime("%Y-%m-%d")}.md'), 'a', encoding='utf-8') as f:
    f.write(log)
print('logs appended')
