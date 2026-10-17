import json, os, re
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')

# ---------- 1) add 301s for CTR-03/04/05 (extract exact old path from task text) ----------
s = json.load(open('iteration_center/state.json','r',encoding='utf-8'))
red_path = 'public/_redirects'
red = open(red_path,'r',encoding='utf-8').read()
adds = []
target = {
 'CTR-20261017-03':'/blog/creatium-coach-review-2025/',
 'CTR-20261017-04':'/blog/creatium-coach-review-2025/',
 'CTR-20261017-05':'/blog/elevenlabs-review-2026/',
}
for t in s['next_iteration_focus']:
    tid = t.get('id','')
    if tid in target:
        m = re.search(r'(/blog/article-api-[^\s]+?md)', t['task'])
        if m:
            old = m.group(1)
            line = f"{old} {target[tid]} 301"
            if old not in red:
                adds.append(line)
if adds:
    block = "\n# Legacy article-api URLs (R16 2026-10-17)\n" + "\n".join(adds) + "\n"
    if not red.endswith('\n'): red += '\n'
    red += block
    open(red_path,'w',encoding='utf-8').write(red)
print("ADDED 301s:")
for a in adds: print("  ", a)

# ---------- 2) CTR-06 optimize title/excerpt ----------
posts = json.load(open('data/posts.json','r',encoding='utf-8'))
p = next(x for x in posts if x['slug']=='best-ai-voice-changers-2026')
new_title = "Best AI Voice Changers 2026: Real-Time Tools for Discord & Podcasts"
new_ex = ("Find the best AI voice changer in 2026: we tested 7 over 10 days for streaming, podcasts, "
          "and gaming. Compare voice quality, pricing, and pick yours today.")
print(f"\nCTR-06 title {len(new_title)}c, excerpt {len(new_ex)}c")
p['title'] = new_title
p['excerpt'] = new_ex
json.dump(posts, open('data/posts.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)

# ---------- 3) evidence for 01/02 ----------
for slug in ['adobe-firefly-review-2026','ai-tools-comparison-2026']:
    q = next(x for x in posts if x['slug']==slug)
    ok_t = 50<=len(q['title'])<=60
    ok_e = 120<=len(q.get('excerpt',''))<=155
    print(f"{slug}: title {len(q['title'])}c({'OK' if ok_t else 'XX'}) excerpt {len(q.get('excerpt',''))}c({'OK' if ok_e else 'XX'})")
