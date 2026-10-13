#!/usr/bin/env python3
"""把zens-ink内容质量检查结果写入state.json待办"""
import json
from datetime import datetime

with open('iteration_center/state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

today = datetime.now().strftime('%Y-%m-%d')
existing_ids = {t['id'] for t in state.get('next_iteration_focus', [])}

new_todos = [
    {
        "id": "P0-CONTENT-BLUF-FIX-ALL-001",
        "priority": "P0",
        "title": "批量修复145篇文章BLUF开头结论缺失（AI搜索时代必须开头给答案）",
        "assigned_to": ["window5"],
        "status": "pending",
        "created": today,
        "description": "zens-ink检测100%文章缺少BLUF（Bottom Line Up Front）开头结论。每篇文章必须在第一段直接给出结论/答案，不要铺垫。参考格式：'Quick Answer: [直接结论]'。用zens-ink content_qc验证修复后分数>=70。"
    },
    {
        "id": "P0-CONTENT-OUTBOUND-LINKS-001",
        "priority": "P0",
        "title": "批量修复104篇文章外链不足（每篇至少2个权威来源引用）",
        "assigned_to": ["window5"],
        "status": "pending",
        "created": today,
        "description": "zens-ink检测71%文章外链不足2个。每篇文章必须引用至少2个权威来源（官方文档、研究报告、数据来源），用<a>标签链接到原始来源。重点修复对比类和评测类文章。"
    },
    {
        "id": "P0-CONTENT-REWRITE-BOTTOM10-001",
        "priority": "P0",
        "title": "重写最低分10篇文章（23-33分，字数严重不足）",
        "assigned_to": ["window3"],
        "status": "pending",
        "created": today,
        "description": "zens-ink检测最低分10篇：midjourney-v7-vs-flux-2026(23分)、chatgpt-vs-claude-2026-comparison(28)、claude-37-vs-gpt4o(28)、synthesia-vs-heygen(28)、motion-ai-alternatives(28)、quillbot-alternatives(28)、runway-alternatives(28)、writesonic-alternatives(28)、otter-ai-alternatives(33)、claude-opus-4-vs-gpt-5-2026(33)。全部重写，每篇>=2000词，包含BLUF开头、FAQ、外链、对比表格、真实截图。"
    },
    {
        "id": "P1-CONTENT-QUESTION-HEADINGS-001",
        "priority": "P1",
        "title": "批量修复97篇文章缺少问题格式标题（匹配用户真实搜索意图）",
        "assigned_to": ["window5"],
        "status": "pending",
        "created": today,
        "description": "zens-ink检测66%文章没有问题格式的H2/H3标题。每篇文章至少有1个H2/H3用用户真实问题格式（如'What is X?'、'How much does X cost?'、'X vs Y: which is better?'），用Google搜索建议和People Also Ask获取真实问题。"
    },
    {
        "id": "P1-CONTENT-H2-SECTIONS-001",
        "priority": "P1",
        "title": "批量修复68篇文章H2标题不足（至少3个H2分段）",
        "assigned_to": ["window5"],
        "status": "pending",
        "created": today,
        "description": "zens-ink检测46%文章H2标题少于3个。每篇文章至少有3个H2分段，结构清晰：1) 开头结论 2) 详细分析 3) 对比/评测 4) FAQ。AI搜索按分段提取答案，结构越清晰越容易被引用。"
    },
    {
        "id": "P1-CONTENT-FAQ-MISSING-001",
        "priority": "P1",
        "title": "批量修复38篇文章缺少FAQ区块（AI搜索最爱引用FAQ）",
        "assigned_to": ["window5"],
        "status": "pending",
        "created": today,
        "description": "zens-ink检测26%文章缺少FAQ。每篇文章末尾必须有FAQ区块，至少3个Q&A，问题来自Google People Also Ask和搜索建议，答案直接给出（50-100词），用FAQPage schema标记。"
    },
    {
        "id": "P1-CONTENT-REWRITE-BELOW50-001",
        "priority": "P1",
        "title": "重写69篇低分文章（<50分，占47%）",
        "assigned_to": ["window3"],
        "status": "pending",
        "created": today,
        "description": "zens-ink检测69篇文章低于50分（占47%）。按优先级分批重写：先重写有排名潜力的关键词文章，再重写工具评测类，最后重写对比类。每篇重写后用zens-ink验证>=70分，用llmevalkit检测无幻觉。"
    },
    {
        "id": "P1-CONTENT-INTERNAL-LINKS-001",
        "priority": "P1",
        "title": "批量修复24篇文章内链不足（每篇至少2个内部链接）",
        "assigned_to": ["window5"],
        "status": "pending",
        "created": today,
        "description": "zens-ink检测16%文章内链不足2个。每篇文章至少链接到2个相关文章/工具页，用关键词锚文本，帮助Google发现和索引更多页面，提升整体网站权重。"
    },
    {
        "id": "P2-CONTENT-LISTS-TABLES-001",
        "priority": "P2",
        "title": "批量修复21篇文章缺少列表/表格（结构化数据更容易被AI提取）",
        "assigned_to": ["window5"],
        "status": "pending",
        "created": today,
        "description": "zens-ink检测14%文章缺少列表或表格。对比类文章必须有对比表格，评测类必须有优缺点列表，清单类必须有编号列表。结构化数据比纯文字更容易被AI搜索提取和引用。"
    },
    {
        "id": "P0-CONTENT-QC-AUTOMATION-001",
        "priority": "P0",
        "title": "建立内容发布前QC自动化检查（zens-ink+llmevalkit双重验证）",
        "assigned_to": ["window5"],
        "status": "pending",
        "created": today,
        "description": "所有新文章发布前必须通过：1) zens-ink content_qc >=70分 2) llmevalkit幻觉检测通过 3) 字数>=2000词 4) 有FAQ 5) 有BLUF开头 6) 有至少2个外链。不通过不发布，从源头杜绝低质量内容。"
    }
]

added = 0
skipped = 0
for todo in new_todos:
    if todo['id'] in existing_ids:
        skipped += 1
        print(f"跳过（已存在）: {todo['id']}")
    else:
        state['next_iteration_focus'].append(todo)
        added += 1
        print(f"添加: {todo['priority']} - {todo['title'][:50]}")

with open('iteration_center/state.json', 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"\n{'='*50}")
print(f"完成！新增 {added} 条待办，跳过 {skipped} 条已存在")
print(f"当前总待办数: {len(state['next_iteration_focus'])}")

# 按优先级统计
p_count = {'P0': 0, 'P1': 0, 'P2': 0}
for t in state['next_iteration_focus']:
    p = t.get('priority', 'P2')
    p_count[p] = p_count.get(p, 0) + 1
print(f"P0: {p_count['P0']}条, P1: {p_count['P1']}条, P2: {p_count['P2']}条")
