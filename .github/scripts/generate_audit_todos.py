"""
从质量审计和SEO审计结果中自动生成state.json待办
云端执行：每次审计后自动把P0/P1问题写入next_iteration_focus
"""
import json
import os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATE_PATH = os.path.join(BASE, "iteration_center", "state.json")
QUALITY_REPORT = os.path.join(BASE, "iteration_center", "quality_audit_report.md")
SEO_RESULTS = os.path.join(BASE, "iteration_center", "full_audit_results.json")

def load_state():
    with open(STATE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_state(state):
    with open(STATE_PATH, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def todo_exists(state, todo_id):
    return any(t.get('id') == todo_id for t in state.get('next_iteration_focus', []))

def add_todo(state, todo_id, task, assigned_to, priority, source):
    if todo_exists(state, todo_id):
        return False
    state['next_iteration_focus'].append({
        'id': todo_id,
        'task': task,
        'assigned_to': [assigned_to],
        'priority': priority,
        'status': 'pending',
        'source': source,
        'created_at': datetime.utcnow().isoformat() + 'Z'
    })
    return True

def main():
    state = load_state()
    added = 0
    
    # 1. 从质量审计报告中提取F级文章
    if os.path.exists(QUALITY_REPORT):
        with open(QUALITY_REPORT, 'r', encoding='utf-8') as f:
            content = f.read()
        # 简单解析F级文章（实际脚本可能有JSON格式）
        import re
        f_articles = re.findall(r'\*\*F级\*\*.*?slug[:\s]+([\w-]+)', content)
        for slug in f_articles:
            tid = f"P0-QUALITY-F-{slug}"
            if add_todo(state, tid, f"重写F级文章：{slug}（0图0链接，质量<60分）", "window5", "P0", "quality_audit_cloud"):
                added += 1
                print(f"  + 新增待办: {tid}")
    
    # 2. 从SEO审计结果中提取critical问题
    if os.path.exists(SEO_RESULTS):
        try:
            with open(SEO_RESULTS, 'r', encoding='utf-8') as f:
                seo = json.load(f)
            issues = seo.get('critical_issues', []) + seo.get('high_issues', [])
            for i, issue in enumerate(issues[:10]):
                tid = f"P0-SEO-{issue.get('type','issue')}-{i}"
                desc = issue.get('description', str(issue))[:100]
                if add_todo(state, tid, f"SEO问题修复：{desc}", "window1", "P0", "seo_audit_cloud"):
                    added += 1
                    print(f"  + 新增待办: {tid}")
        except Exception as e:
            print(f"  ⚠️ SEO结果解析失败: {e}")
    
    save_state(state)
    print(f"\n✅ 完成：新增 {added} 条待办")
    print(f"当前总待办数: {len(state.get('next_iteration_focus', []))}")

if __name__ == '__main__':
    main()
