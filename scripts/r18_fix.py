import json, os, re, tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc

def html_to_md(html):
    s=html
    s=re.sub(r'<h2[^>]*>(.*?)</h2>',r'\n## \1\n',s,flags=re.S|re.I)
    s=re.sub(r'<h3[^>]*>(.*?)</h3>',r'\n### \1\n',s,flags=re.S|re.I)
    s=re.sub(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>',r'[\2](\1)',s,flags=re.S|re.I)
    s=re.sub(r'<(?:strong|b)[^>]*>(.*?)</(?:strong|b)>',r'**\1**',s,flags=re.S|re.I)
    s=re.sub(r'<li[^>]*>(.*?)</li>',r'- \1\n',s,flags=re.S|re.I)
    s=re.sub(r'</?[uo]l[^>]*>','',s,flags=re.I)
    s=re.sub(r'<p[^>]*>(.*?)</p>',r'\1\n\n',s,flags=re.S|re.I)
    s=re.sub(r'<[^>]+>','',s)
    s=re.sub(r'\n{3,}','\n\n',s)
    return s.strip()

posts=json.load(open('data/posts.json','r',encoding='utf-8'))

def prep_bluf(p, bluf, link_md):
    c=html_to_md(p['content'])
    if 'Bottom line' not in c:
        c=bluf+'\n\n'+c
    c+=f"\n\n{link_md}\n"
    p['content']=c

# midjourney-review (CTR-01)
p=next(x for x in posts if x['slug']=='midjourney-review-2026')
p['title']='Midjourney Review 2026: Best AI Image Generator, Tested'
prep_bluf(p,
 "**Bottom line:** Midjourney remains the best AI image generator for art and commercial imagery in 2026 (8.0/10): unmatched style variety and consistency, but it needs Discord/web access and has no free tier.",
 "- [DALL-E 3 comparison reference](https://openai.com/dall-e-3/)")

# kling-review
p=next(x for x in posts if x['slug']=='kling-review-2026')
p['title']='Kling AI Review 2026: Best AI Video Generator, Tested'
prep_bluf(p,
 "**Bottom line:** Kling AI 1.6 is the strongest free-tier AI video tool in 2026 (7.8/10) for cinematic motion, behind only paid Runway; expect watermarks and slower renders on the free plan.",
 "- [Kling AI official site](https://klingai.com/)")

# leonardo-ai-review
p=next(x for x in posts if x['slug']=='leonardo-ai-review-2026')
p['title']='Leonardo AI Review 2026: Best AI Image Generator, Tested'
p['excerpt']="Leonardo AI review 2026: tested 30 days across 60+ images. Our 7.6/10 rating, pricing, pros/cons, and how it compares to Midjourney."
prep_bluf(p,
 "**Bottom line:** Leonardo AI is the best free-to-start AI image generator in 2026 (7.6/10): generous daily credits and easy fine-tunes, but photorealism trails Midjourney at the top tier.",
 "- [Leonardo AI official site](https://leonardo.ai/)")

json.dump(posts,open('data/posts.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)

for slug in ['midjourney-review-2026','kling-review-2026','leonardo-ai-review-2026']:
    q=next(x for x in posts if x['slug']==slug)
    md=f"---\ntitle: \"{q['title']}\"\ndescription: \"{q.get('excerpt','')[:160]}\"\ndate: 2026-10-18\n---\n\n{q['content']}\n"
    tmp=Path(tempfile.mkdtemp())/f'{slug}.md'; tmp.write_text(md,encoding='utf-8')
    r=content_qc.check_draft(tmp)
    fails=[c['check'] for c in r['checks'] if not c['pass']]
    print(f"{slug}: {r['score']} fails={fails} title={len(q['title'])}c excerpt={len(q.get('excerpt',''))}c")
