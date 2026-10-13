import json

# 看state.json里已完成的内容相关任务
with open('iteration_center/state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

print("=== 已完成任务中与内容质量相关的 ===")
content_related = []
for t in state.get('completed_tasks', []):
    title = t.get('title', '').lower()
    desc = t.get('description', '').lower()
    if any(k in title or k in desc for k in ['内容', '文章', 'content', '质量', 'qc', '重写', '优化', 'bluf', 'faq', '外链']):
        content_related.append(t)

print(f"共 {len(content_related)} 条内容相关已完成任务")
for t in content_related[:20]:
    print(f"  - [{t.get('priority','?')}] {t.get('title','')[:60]}")

print("\n=== completed_todo 中的内容相关任务 ===")
for t in state.get('completed_todo', [])[:20]:
    if isinstance(t, dict):
        print(f"  - {t.get('title', str(t))[:60]}")
    else:
        print(f"  - {str(t)[:60]}")

print("\n=== 当前待办中已有的内容质量任务（新增之前） ===")
existing_content = []
for t in state.get('next_iteration_focus', []):
    title = t.get('title', '').lower()
    if any(k in title for k in ['内容', '文章', 'content', '质量', '重写', 'bluf', 'faq', '外链']):
        if 'CONTENT-' not in t.get('id', ''):  # 排除刚才新增的
            existing_content.append(t)

print(f"共 {len(existing_content)} 条")
for t in existing_content:
    print(f"  - [{t.get('priority','?')}] {t.get('id','')}: {t.get('title','')[:60]}")
    print(f"    状态: {t.get('status','?')}")
