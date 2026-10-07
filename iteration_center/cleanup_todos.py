"""
清理state.json待办：327条→50条以内
规则：
1. 备份原文件
2. backlog状态全部归档
3. 标题为空或"[待补标题]"的关键词任务归档（没有具体内容无法执行）
4. 去重（按title+assigned_to）
5. P0重新评估：只保留网站故障/数据归零/排名暴跌/部署失败等真正紧急的
6. P1保留和30天目标直接相关的
7. P2全部归档为backlog
"""
import json
import shutil
from datetime import datetime
from pathlib import Path

PROJECT = Path(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")
STATE_FILE = PROJECT / "iteration_center" / "state.json"

# 1. 备份
backup_name = f"state.json.backup_cleanup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
shutil.copy2(STATE_FILE, PROJECT / "iteration_center" / backup_name)
print(f"✅ 已备份: {backup_name}")

# 2. 读取
with open(STATE_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

todos = data.get('next_iteration_focus', [])
archived = data.get('archived_todos', [])
print(f"原始待办: {len(todos)}条, 已归档: {len(archived)}条")

# 3. 真正紧急的P0关键词（包含这些词的保留为P0）
URGENT_KEYWORDS = [
    '503', '404', '网站打不开', '部署失败', 'build fail',
    '流量归零', '排名暴跌', 'crash', '宕机', 'offline',
    'GSC认证失败', 'GA4认证失败', '服务账号',
    'Vercel暂停', 'Cloudflare', 'DNS',
]

# 4. 和30天目标直接相关的P1关键词
GOAL_KEYWORDS = [
    '曝光', '流量', 'UV', '点击', 'CTR', '排名', '索引', '收录',
    '关键词', '长尾', '内容', '文章', '外链', '联盟', '变现',
    '断链', 'H2', 'FAQ', 'GEO', 'schema', '内链',
    'screenshot', '截图', '原创', '质量',
]

def is_urgent(todo):
    """判断是否真正紧急"""
    title = (todo.get('title') or '').lower()
    return any(kw.lower() in title for kw in URGENT_KEYWORDS)

def is_goal_related(todo):
    """判断是否和30天目标相关"""
    title = (todo.get('title') or '').lower()
    return any(kw.lower() in title for kw in GOAL_KEYWORDS)

def is_empty_todo(todo):
    """判断是否是空壳任务"""
    title = (todo.get('title') or '').strip()
    if not title:
        return True
    if title.startswith('[待补标题]'):
        return True
    if title.startswith('kw_') and len(title) < 20:
        return True
    return False

# 5. 分类处理
keep = []
archive_now = []
seen = set()

for todo in todos:
    title = (todo.get('title') or '').strip()
    status = todo.get('status', 'pending')
    priority = todo.get('priority', 'P2')
    assignee = todo.get('assigned_to', '')
    if isinstance(assignee, list):
        assignee = ','.join(assignee)
    
    # 去重key
    dedup_key = f"{title}|{assignee}|{priority}"
    
    # 规则1: backlog状态全部归档
    if status == 'backlog':
        archive_now.append(todo)
        continue
    
    # 规则2: 空壳任务归档
    if is_empty_todo(todo):
        archive_now.append(todo)
        continue
    
    # 规则3: 去重
    if dedup_key in seen:
        archive_now.append(todo)
        continue
    seen.add(dedup_key)
    
    # 规则4: P0重新评估
    if priority == 'P0':
        if is_urgent(todo):
            todo['priority'] = 'P0'
            keep.append(todo)
        elif is_goal_related(todo):
            todo['priority'] = 'P1'  # 降级为P1
            keep.append(todo)
        else:
            todo['priority'] = 'P2'
            archive_now.append(todo)
        continue
    
    # 规则5: P1只保留和目标相关的
    if priority == 'P1':
        if is_goal_related(todo):
            keep.append(todo)
        else:
            todo['priority'] = 'P2'
            archive_now.append(todo)
        continue
    
    # 规则6: P2全部归档
    if priority == 'P2':
        archive_now.append(todo)
        continue
    
    # 其他状态保留
    keep.append(todo)

# 6. 如果保留的超过50条，按优先级截断
if len(keep) > 50:
    p0 = [t for t in keep if t.get('priority') == 'P0']
    p1 = [t for t in keep if t.get('priority') == 'P1']
    other = [t for t in keep if t.get('priority') not in ('P0', 'P1')]
    
    # P0全留，P1按顺序留，凑够50
    keep = p0 + p1[:50 - len(p0)]
    archive_now.extend(p1[50 - len(p0):])
    archive_now.extend(other)

# 7. 写入
data['next_iteration_focus'] = keep
data['archived_todos'] = archived + archive_now
data['last_cleanup'] = datetime.now().isoformat()
data['cleanup_summary'] = {
    'original': len(todos),
    'kept': len(keep),
    'archived': len(archive_now),
    'p0_count': len([t for t in keep if t.get('priority') == 'P0']),
    'p1_count': len([t for t in keep if t.get('priority') == 'P1']),
}

with open(STATE_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n📊 清理完成:")
print(f"  原始: {len(todos)}条")
print(f"  保留: {len(keep)}条")
print(f"  归档: {len(archive_now)}条")
print(f"  P0: {len([t for t in keep if t.get('priority')=='P0'])}条")
print(f"  P1: {len([t for t in keep if t.get('priority')=='P1'])}条")
print(f"\n保留的P0任务:")
for t in keep:
    if t.get('priority') == 'P0':
        print(f"  - {t.get('title','')[:70]}")
