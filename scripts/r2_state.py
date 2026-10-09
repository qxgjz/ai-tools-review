import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s = json.load(open('iteration_center/state.json','r',encoding='utf-8'))
task = {
    "id": "POLISH-2026-10-09-R2",
    "priority": "P1",
    "title": "R2: 优化 synthesia-vs-heygen / motion-ai-alt / quillbot-alt 到>=90",
    "status": "completed",
    "assigned_to": ["polisher"],
    "completed_at": "2026-10-09T19:30:00+08:00",
    "result": "28->100, 28->90, 28->90",
    "log": "window_logs/polisher_2026-10-09_r2.md"
}
s.setdefault('completed_tasks',[]).insert(0, task)
s['last_updated'] = "2026-10-09T19:30:00+08:00"
json.dump(s, open('iteration_center/state.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print('state.json updated')
