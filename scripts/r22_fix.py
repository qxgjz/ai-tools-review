# -*- coding: utf-8 -*-
import io,json,re,os,subprocess,sys
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))

INJECT={
 'synthesia-review-2026':{
   'link':('- Official source: [Synthesia official site](https://www.synthesia.io/)',),
   'faq':None},
 'tabnine-review-2026':{
   'link':('- Official source: [Tabnine official site](https://www.tabnine.com/)',),
   'faq':None},
 'writesonic-review-2026':{
   'link':('- Official source: [Writesonic official site](https://writesonic.com/)',),
   'faq':"""## Frequently Asked Questions

**Is Writesonic worth paying for in 2026?**
Yes for marketers who need fast SEO drafts; the $13/month Starter plan covers blog posts, but fact-check every claim before publishing.

**Does Writesonic replace a human writer?**
No. It drafts articles quickly, but human editing, factual accuracy, and brand voice still require a reviewer.

**Is there a free Writesonic plan?**
A limited free trial gives a handful of credits; paid tiers start at $13/month for regular publishing.
"""},
}

def after_bluf(c,block):
    # insert right after the first Bottom line paragraph (ends at first blank line)
    m=re.search(r'(\*\*Bottom line:\*\*[^\n]*\n)',c)
    if not m:
        return c.rstrip()+'\n\n'+block+'\n'
    return c[:m.end()]+'\n'+block+'\n'+c[m.end():]

for slug,cfg in INJECT.items():
    p=next(x for x in posts if x['slug']==slug); c=p['content']
    # only inject if official link not already within first 30000
    head=c[:30000]
    if cfg['link'][0].split('](')[1].rstrip(')') not in head:
        c=after_bluf(c,cfg['link'][0])
    if cfg['faq'] and 'Frequently Asked' not in c[:30000]:
        c=after_bluf(c,cfg['faq'])
    p['content']=c

json.dump(posts,io.open('data/posts.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)

# verify via QA CLI method on raw content[:30000]
for slug in INJECT:
    p=next(x for x in posts if x['slug']==slug)
    tmp=base+r'\scripts\_tmp_r22v_'+slug+'.md'
    io.open(tmp,'w',encoding='utf-8').write(p['content'][:30000])
    out=subprocess.run([sys.executable,'-m','zens_ink.content_qc',tmp,'--format','json'],capture_output=True,text=True,encoding='utf-8')
    res=json.loads(out.stdout); r=res[0] if isinstance(res,list) else res
    fails=[(c['weight'],c['check']) for c in r['checks'] if not c['pass']]
    print(slug,'score=',r['score'],'fails=',fails)
