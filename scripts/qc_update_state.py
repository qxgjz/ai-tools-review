"""把 P0/P1 写进 state.json.next_iteration_focus"""
import os, json
from datetime import datetime

ROOT = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
os.chdir(ROOT)

s = json.load(open('iteration_center/state.json', 'r', encoding='utf-8'))

todos = [
    {
        "id": "P1-CONTENT-KWD-DENSITY-001",
        "priority": "P1",
        "title": "4篇草稿关键词密度0.0-0.13% < 0.5%",
        "description": "midjourney/chatgpt-vs-claude/claude-37/n8n 四篇发布稿里主关键词出现次数不足。窗口3发布前在正文自然多提2-3次主关键词，不要堆砌。",
        "assigned_to": ["内容生产窗口"],
        "source": "hallucination_audit_report",
        "created_at": "2026-10-09T15:00:00+09:00",
        "status": "pending"
    },
    {
        "id": "P1-CONTENT-CAUSAL-CLAIMS-001",
        "priority": "P1",
        "title": "3处因果断言缺来源（causal detector标记）",
        "description": "claude-37篇'Claude leads on nuanced translation'、midjourney篇'each generation takes 40-60 min'、chatgpt篇'thinking parameter allocates...'——补一句官方benchmark或文档链接。",
        "assigned_to": ["内容生产窗口"],
        "source": "hallucination_audit_report",
        "created_at": "2026-10-09T15:00:00+09:00",
        "status": "pending"
    },
    {
        "id": "P1-TOOL-CONTRADICTION-FP-001",
        "priority": "P1",
        "title": "ContradictionDetector纯规则模式误报率100%",
        "description": "全文自对照(answer=context=全文)时，表格vs正文重复陈述被误判为negation_flip/antonym，23/23全误报。建议llmevalkit_toolkit加后处理：if context==answer skip contradiction。",
        "assigned_to": ["指挥官"],
        "source": "hallucination_audit_report",
        "created_at": "2026-10-09T15:00:00+09:00",
        "status": "pending"
    },
]

if 'next_iteration_focus' not in s:
    s['next_iteration_focus'] = []
existing = {t.get('id') for t in s['next_iteration_focus'] if isinstance(t, dict)}
for t in todos:
    if t['id'] not in existing:
        s['next_iteration_focus'].insert(0, t)

# 标记4篇草稿可发布
s['drafts_ready_to_publish'] = [
    "2026-10-09-midjourney-v7-vs-flux-2026_REWRITE.md",
    "2026-10-09-chatgpt-vs-claude-2026-comparison_REWRITE.md",
    "2026-10-09-claude-37-vs-gpt4o_REWRITE.md",
    "2026-10-09-n8n-review-2026_DRAFT.md",
]
s['last_updated'] = "2026-10-09T15:00:00+09:00"

json.dump(s, open('iteration_center/state.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f"state.json updated. next_iteration_focus: {len(s['next_iteration_focus'])} items")
print(f"drafts_ready_to_publish: {len(s['drafts_ready_to_publish'])}")
