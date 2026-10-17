import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')

# verified old paths from GSC reports (2026-09)
redirects = [
 ("/blog/article-api-20260903-171438-creatium-coach-review-2025-is-this-ai-content-coach-worth-your-time-md",
  "/blog/creatium-coach-review-2025/"),
 ("/blog/article-api-20260903-173022-creatium-coach-review-2025-a-handy-way-to-turn-documents-into-a-coach-but-not-a-md",
  "/blog/creatium-coach-review-2025/"),
 ("/blog/article-api-20260903-173210-elevenlabs-review-2026-is-it-still-the-most-human-like-ai-voice-generator-md",
  "/blog/elevenlabs-review-2026/"),
]
rp = 'public/_redirects'
red = open(rp,'r',encoding='utf-8').read()
added=[]
for old,new in redirects:
    if old not in red:
        added.append(f"{old} {new} 301")
if added:
    if not red.endswith('\n'): red+='\n'
    red += "\n# Legacy article-api orphan URLs (R16, verified against GSC 2026-09)\n" + "\n".join(added) + "\n"
    open(rp,'w',encoding='utf-8').write(red)
print("301 added:", len(added))
for a in added: print("  ",a)

# CTR-06 title fix (59c), excerpt 155c kept
posts = json.load(open('data/posts.json','r',encoding='utf-8'))
p = next(x for x in posts if x['slug']=='best-ai-voice-changers-2026')
p['title'] = "Best AI Voice Changers 2026: Real-Time Voice Tools Compared"
p['excerpt'] = ("Find the best AI voice changer in 2026: we tested 7 over 10 days for streaming, podcasts, "
                "and gaming. Compare voice quality, pricing, and pick yours today.")
json.dump(posts, open('data/posts.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print(f"\nCTR-06 title {len(p['title'])}c, excerpt {len(p['excerpt'])}c")
