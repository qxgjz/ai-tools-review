import json, os, glob
from datetime import datetime

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'

# 1. Check posts.json last modified
posts_path = os.path.join(base, 'data', 'posts.json')
mtime = datetime.fromtimestamp(os.path.getmtime(posts_path))
with open(posts_path,'r',encoding='utf-8') as f:
    posts = json.load(f)
print(f'posts.json: {len(posts)} articles, last modified: {mtime}')

# 2. Check content_drafts recent files
drafts = glob.glob(os.path.join(base, 'content_drafts', '*_READY.md'))
drafts.sort(key=os.path.getmtime, reverse=True)
print(f'\ncontent_drafts/*_READY.md: {len(drafts)} files')
for d in drafts[:5]:
    mt = datetime.fromtimestamp(os.path.getmtime(d))
    print(f'  {mt}: {os.path.basename(d)}')

# 3. Check content_briefs count
briefs = glob.glob(os.path.join(base, 'iteration_center', 'content_briefs', '*_input.md'))
print(f'\ncontent_briefs: {len(briefs)} briefs')

# 4. Check which kw_ tasks exist but have NO corresponding post
with open(os.path.join(base,'iteration_center','state.json'),'r',encoding='utf-8') as f:
    state = json.load(f)
kw_tasks = [t for t in state['next_iteration_focus'] if t.get('id','').startswith('kw_') and t.get('status')=='pending']
print(f'\nPending kw_ tasks: {len(kw_tasks)}')
slugs_in_posts = {p.get('slug','') for p in posts}
missing = []
for t in kw_tasks:
    slug = t.get('slug','')
    if slug not in slugs_in_posts:
        missing.append(slug)
print(f'  No post yet: {len(missing)}')
print(f'  Already posted: {len(kw_tasks)-len(missing)}')

# 5. Check recent posts
recent = sorted(posts, key=lambda x: x.get('publishedAt',''), reverse=True)[:5]
print(f'\n5 most recent posts:')
for p in recent:
    print(f"  {p.get('publishedAt','?')}: {p.get('slug','?')}")
