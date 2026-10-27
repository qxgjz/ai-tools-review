# -*- coding: utf-8 -*-
"""r33 P0-INDEX-SNAPSHOT-RERUN 收尾：写入结构化快照 + 更新 gsc_indexed_baseline + audit_findings + state.json 闭环"""
import json, os
from datetime import datetime

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
now_iso = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
now = datetime.now().strftime('%Y-%m-%d %H:%M')

snap = {
    "source": "adspower_cdp_gsc_page", "pulled_at": now_iso, "report_date": "2026/10/25",
    "indexed": 640, "not_indexed": 744, "total_known": 1384,
    "reasons": {
        "auto_redirect": 94, "noindex": 33,
        "duplicate_without_canonical": 9, "redirect_error": 5,
        "not_found_404": 4, "discovered_not_indexed": 589,
        "duplicate_google_chosen": 8, "crawled_not_indexed": 2
    }
}
sp = os.path.join(P, 'gsc-ga4-report', 'indexing_snapshot_20261027.json')
old = json.load(open(os.path.join(P, 'gsc-ga4-report', 'indexing_snapshot_20261012.json'), encoding='utf-8')) if os.path.exists(os.path.join(P, 'gsc-ga4-report', 'indexing_snapshot_20261012.json')) else {}
snap['prev'] = {"indexed": old.get('indexed'), "not_indexed": old.get('not_indexed'), "total_known": old.get('total_known')}
json.dump(snap, open(sp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('snapshot written:', snap['indexed'], snap['not_indexed'], snap['total_known'])

# 更新 gsc_indexed_baseline
bp = os.path.join(P, 'gsc-ga4-report', 'gsc_indexed_baseline_20261025.md')
bs = open(bp, encoding='utf-8').read()
add = f"""

## 二、W2 更新（{now} · AdsPower CDP 实抓 GSC 索引覆盖率页）

| 周次 | 报告日 | indexed | not_indexed | 收录率 | 数据源 |
|---|---|---|---|---|---|
| W1 | 2026-10-09 | 477 | 428 | 52.8% | indexing_snapshot_20261012 |
| **W2** | **2026-10-25** | **640** | **744** | **46.2%** | **indexing_snapshot_20261027（本次实抓）** |

### 环比变化（W1→W2）
| 指标 | W1 | W2 | 变化 |
|---|---|---|---|
| 已知 URL 总数 | 905 | 1384 | +479（+52.9%，sitemap 10/23 更新） |
| 已编入（indexed） | 477 | 640 | +163（绝对收录增长） |
| 未编入（not_indexed） | 428 | 744 | +316 |
| 收录率 | 52.8% | **46.2%** | **-6.6pp（相对下降）** |

### 未收录原因变化（重点）
| 原因 | W1 | W2 | 变化 | 判定 |
|---|---|---|---|---|
| **discovered_not_indexed（已发现未编入）** | 400 | **589** | +189 | P0：Google 已发现但未入索引，内容质量/需求相关，最大杠杆 |
| **auto_redirect（自动重定向）** | 9 | **94** | **+85 暴增** | P0：新增页面重定向链异常，疑似 article-api-* 时间戳 URL / 新分类页 301 配置 |
| **noindex** | 5 | **33** | +28 | P1：检查是否误设 noindex |
| duplicate_without_canonical | 9 | 9 | 0 | 维持（架构师 CANONICAL 待办） |
| redirect_error | 1 | 5 | +4 | P1：重定向链修复（已有架构师待办） |
| not_found_404 | 2 | 4 | +2 | P1：404 清理 |
| duplicate_google_chosen | (未单列) | 8 | 新增 | P1：规范页与用户指定不同 |
| crawled_not_indexed | 2 | 2 | 0 | 维持 |

### 结论（纠偏）
1. 绝对收录 **477→640（+34%）**——内容扩充持续有效
2. 但收录率 **52.8%→46.2%**（-6.6pp）：新增 479 URL 中 316 未收录，Google 对新增长尾页的收录意愿低
3. **auto_redirect 9→94 暴增是新的 P0 异常**：与 r28 发现的 article-api-* 时间戳 URL（.md 后缀）污染索引高度相关，需架构师优先排查重定向链
4. discovered_not_indexed 589（79.2% 未编入）仍是第一杠杆：内容质量提升 + 内链
"""
open(bp, 'w', encoding='utf-8').write(bs + add)
print('baseline updated')

# audit_findings 追加
afp = os.path.join(P, 'iteration_center', 'audit_findings.md')
af = open(afp, encoding='utf-8').read()
afadd = f"""

## W2 索引监控发现（{now} · AdsPower CDP 实抓 GSC 索引覆盖率页）

### [P0] 异常：auto_redirect 9→94 暴增（+85）
- 现象：GSC 索引报告"网页会自动重定向"10-12 为 9，10-27 实抓为 **94**
- 推断：与 r28 已发现的 article-api-* 时间戳 URL（`.md` 后缀、异常 URL 污染索引）及新增页面 301 链相关
- 建议：架构师 P0 排查新增 94 个重定向 URL，优先清理 article-api-* 时间戳页面（ARTICLE-API-URL-CLEAN 待办加速）

### [P0] 异常：收录率 52.8%→46.2%（-6.6pp）
- 现象：已知 URL 905→1384（+479，sitemap 10/23 更新），indexed 477→640（+163），未编入 428→744（+316）
- 影响：内容量扩充但收录意愿下降，Google 对新长尾页"已发现未编入"589 条
- 建议：discovered_not_indexed 仍是第一杠杆（内容质量+内链+IndexNow 提交高价值页）

### [P1] 观察：noindex 5→33（+28）
- 现象：noindex 页面从 5 增至 33
- 建议：检查是否误设 noindex（如新模板默认）

### [P1] 观察：duplicate_google_chosen 新增 8 条
- 现象：Google 选择规范页与用户指定不同 8 条
- 建议：纳入 CANONICAL-REDIRECT-AUDIT 待办一并修复
"""
open(afp, 'a', encoding='utf-8').write(afadd)
print('audit appended')

# state.json 闭环 P0-INDEX-SNAPSHOT-RERUN + GSC-QUOTA-RERUN
d = json.load(open(os.path.join(P, 'iteration_center', 'state.json'), encoding='utf-8'))
nf = d['next_iteration_focus']
closed = []
for t in nf:
    if t.get('id') in ('P0-INDEX-SNAPSHOT-RERUN-20261026', 'GSC-QUOTA-RERUN-20261012'):
        if t.get('status') != 'completed':
            t['status'] = 'completed'
            t['completed_at'] = now_iso
            t['evidence'] = 'indexing_snapshot_20261027.json: indexed=640/not_indexed=744/total=1384; 环比收录率52.8%->46.2%; auto_redirect 9->94 P0发现'
            closed.append(t['id'])
d['next_iteration_focus'] = nf
d['last_update'] = now_iso
json.dump(d, open(os.path.join(P, 'iteration_center', 'state.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('closed:', closed)
