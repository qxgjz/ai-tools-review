import json, os
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
with open(os.path.join(base,'iteration_center','state.json'),'r',encoding='utf-8') as f:
    state = json.load(f)

# Recently completed tasks
done = [t for t in state['next_iteration_focus'] if t.get('status')=='completed' and 'window3' in t.get('assigned_to',[])]
done.sort(key=lambda x: x.get('completed_at', x.get('updated_at','')), reverse=True)
print(f'=== Recently completed window3 tasks ({len(done)} total) ===')
for t in done[:10]:
    print(f"  {t.get('completed_at','?')[:10]}: [{t.get('id','?')}] {t.get('task', t.get('title','?'))[:60]}")

# Check: notion-ai-vs-salesforce in state?
print('\n=== Search for notion-ai-vs-salesforce ===')
for t in state['next_iteration_focus']:
    if 'salesforce' in str(t.get('task','')).lower() or 'salesforce' in str(t.get('slug','')).lower():
        print(f"  [{t.get('status','?')}] id={t.get('id','?')} slug={t.get('slug','?')} task={t.get('task','?')[:60]}")

# Check: what slugs are in the 38 pending kw tasks
print('\n=== 38 pending kw_ tasks slugs ===')
pending_kw = [t for t in state['next_iteration_focus'] if t.get('id','').startswith('kw_') and t.get('status')=='pending']
for t in pending_kw:
    print(f"  {t.get('slug','?')}")
