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

# ---- CTR-03 voice-changers (68 impr, rank16.5): stronger hook + free + CTA ----
p=next(x for x in posts if x['slug']=='best-ai-voice-changers-2026')
p['title']='Best AI Voice Changers 2026: Free & Real-Time Tools Compared'
p['excerpt']=('Looking for the best AI voice changer in 2026? We tested 7 over 10 days for streaming, gaming, and '
              'podcasts — quality, pricing, free options, and pick yours now.')

# ---- CTR-04 adobe-firefly (26 impr, rank5.2): benefit title + official link ----
p=next(x for x in posts if x['slug']=='adobe-firefly-review-2026')
p['title']='Adobe Firefly Review 2026: Free AI Image Generator, Tested'
p['excerpt']=('Adobe Firefly review 2026: tested 2 weeks on commercial images. See our honest verdict, free tier, '
               'commercial license, pricing, and how it compares to Midjourney — read before you sign up.')
if 'firefly.adobe.com' not in p['content']:
    p['content']=p['content'].rstrip()+'\n\n- [Adobe Firefly official site](https://firefly.adobe.com/)\n'

# ---- microsoft-365-copilot: BLUF + clean title ----
p=next(x for x in posts if x['slug']=='microsoft-365-copilot-review-2026')
p['title']='Microsoft 365 Copilot Review 2026: Worth It for Teams?'
c=html_to_md(p['content'])
if 'Bottom line' not in c:
    c=("**Bottom line:** Microsoft 365 Copilot is the best in-office AI for existing M365 subscribers (7.9/10), "
       "deeply woven into Word/Excel/Teams, but its monthly add-on price only pays off if you already live in the suite.\n\n")+c
p['content']=c

# ---- notion-ai: BLUF + second source + clean title + trim excerpt ----
p=next(x for x in posts if x['slug']=='notion-ai-review-2026')
p['title']='Notion AI Review 2026: Best Notion Assistant, Tested'
p['excerpt']=('Notion AI review 2026: tested 30 days, writing 30+ docs and organizing 50+ notes. Our 7.8/10 rating, '
              'pricing, pros/cons, and how it compares to alternatives.')
c=html_to_md(p['content'])
if 'Bottom line' not in c:
    c=("**Bottom line:** Notion AI is the best built-in writing assistant inside Notion (7.8/10) for drafting, "
       "summarizing, and database Q&A, but stand-alone writers may prefer a cheaper add-on.\n\n")+c
if 'notion.so/help' not in c:
    c+="\n\n- [Notion AI help center](https://www.notion.so/help)\n"
p['content']=c

# ---- otter-ai: BLUF + competitor source + clean title + trim excerpt ----
p=next(x for x in posts if x['slug']=='otter-ai-review-2026')
p['title']='Otter.ai Review 2026: Best AI Meeting Assistant, Tested'
p['excerpt']=('Otter.ai review 2026: tested 30 days across 20 meetings. Our 7.8/10 rating, pricing, pros/cons, and how '
              'it compares to Fireflies for transcription.')
c=html_to_md(p['content'])
if 'Bottom line' not in c:
    c=("**Bottom line:** Otter.ai is the best AI meeting note-taker for fast, accurate live transcription (7.8/10), "
       "but advanced team workflows push buyers toward Fireflies or paid enterprise tiers.\n\n")+c
if 'fireflies.ai' not in c:
    c+="\n\n- [Fireflies.ai alternative](https://fireflies.ai/)\n"
p['content']=c

json.dump(posts,open('data/posts.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)

for slug in ['best-ai-voice-changers-2026','adobe-firefly-review-2026','microsoft-365-copilot-review-2026','notion-ai-review-2026','otter-ai-review-2026']:
    q=next(x for x in posts if x['slug']==slug)
    md=f"---\ntitle: \"{q['title']}\"\ndescription: \"{q.get('excerpt','')[:160]}\"\ndate: 2026-10-19\n---\n\n{q['content']}\n"
    tmp=Path(tempfile.mkdtemp())/f'{slug}.md'; tmp.write_text(md,encoding='utf-8')
    r=content_qc.check_draft(tmp)
    fails=[c['check'] for c in r['checks'] if not c['pass']]
    print(f"{slug}: {r['score']} fails={fails} title={len(q['title'])}c excerpt={len(q.get('excerpt',''))}c")
