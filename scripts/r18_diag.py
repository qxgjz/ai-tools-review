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
for slug in ['midjourney-review-2026','kling-review-2026','leonardo-ai-review-2026']:
    p=next(x for x in posts if x['slug']==slug)
    c=p['content']; fmt='HTML' if '<' in c[:300] else 'MD'
    if fmt=='HTML': c=html_to_md(c)
    exc=p.get('excerpt','')[:160]
    md=f"---\ntitle: \"{p['title']}\"\ndescription: \"{exc}\"\ndate: 2026-10-18\n---\n\n{c}\n"
    tmp=Path(tempfile.mkdtemp())/f'{slug}.md'; tmp.write_text(md,encoding='utf-8')
    r=content_qc.check_draft(tmp)
    print(f"=== {slug} [{fmt}] score={r['score']} excerpt={len(p.get('excerpt',''))}c title={len(p['title'])}c ===")
    for ch in r['checks']:
        if not ch['pass']: print(f"  FAIL {ch['check']}: {ch.get('note','')[:110]}")
    print()
