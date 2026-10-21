# -*- coding: utf-8 -*-
import io,json,subprocess,sys,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))

BLOCKS={
'best-ai-image-generators-2026':"""**Bottom line:** In 2026, Midjourney v7 produces the most polished commercial images, DALL-E 3 handles precise text and prompts, and Stable Diffusion wins for free local control; pick by use case, not hype.

## Quick Verdict
- Best polished art: [Midjourney](https://www.midjourney.com/)
- Best text-in-image: [DALL-E 3](https://openai.com/dall-e-3)
- Best free local option: Stable Diffusion

## Which AI image generator is easiest for beginners?
DALL-E 3 is easiest for beginners because plain English prompts work well; Midjourney needs Discord and prompt craft; Stable Diffusion needs setup.

## Frequently Asked Questions

**Are free AI image generators good enough in 2026?**
Free tiers are fine for drafts and social graphics; commercial print or client work usually needs a paid plan.

**Can I sell images I generate?**
Check each tool's commercial license; paid Midjourney and DALL-E 3 plans generally allow commercial use.

**Which tool has the best photo realism?**
Midjourney v7 leads on photorealism and lighting; DALL-E 3 wins on exact instruction following.

""",
'midjourney-v7-vs-dall-e-3-ecommerce':"""**Bottom line:** For e-commerce product photos in 2026, Midjourney v7 wins on lighting and realism for mockups, while DALL-E 3 wins when you need exact text, labels, and prompt accuracy on the product.

## Quick Verdict
- Realistic mockups: [Midjourney v7](https://www.midjourney.com/)
- Exact text & labels: [DALL-E 3](https://openai.com/dall-e-3)

## Frequently Asked Questions

**Which costs less per product photo?**
DALL-E 3 via ChatGPT Plus often costs less per batch; Midjourney Pro gives faster, higher-volume generation.

**Which handles product text better?**
DALL-E 3 renders readable labels and packaging text; Midjourney still garbles small text.

**Can I use the photos commercially?**
Yes on paid plans; review each license and keep a record of generations for your listings.

""",
'notion-ai-vs-obsidian-ai':"""**Bottom line:** Pick Notion AI for databases, docs, and team collaboration; pick Obsidian AI for local-first, private notes and a permanent knowledge graph you own.

## Quick Verdict
- Team docs & databases: [Notion AI](https://www.notion.so/product/ai)
- Private local notes: [Obsidian](https://obsidian.md/)

## Frequently Asked Questions

**Is Notion AI or Obsidian AI better for students?**
Notion AI suits shared projects and databases; Obsidian AI suits private study notes that stay offline.

**Which works offline?**
Obsidian stores files locally and works offline; Notion AI requires an internet connection.

**Which is cheaper?**
Obsidian is a local app with optional paid AI; Notion AI adds a per-seat AI subscription on top.

""",
}
by={p['slug']:p for p in posts}
for slug,block in BLOCKS.items():
    c=by[slug]['content']
    if 'Bottom line' not in c[:400]:
        by[slug]['content']=block+c.lstrip()
json.dump(posts,io.open('data/posts.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)

for slug in BLOCKS:
    c=by[slug]['content']
    tmp=base+r'\scripts\_tmp_r24f_'+slug+'.md'
    io.open(tmp,'w',encoding='utf-8').write(c[:30000])
    out=subprocess.run([sys.executable,'-m','zens_ink.content_qc',tmp,'--format','json'],capture_output=True,text=True,encoding='utf-8')
    res=json.loads(out.stdout); r=res[0] if isinstance(res,list) else res
    fails=[(x['weight'],x['check']) for x in r['checks'] if not x['pass']]
    print(slug,'score=',r['score'],'fails=',fails)
    assert r['score']>=70, slug+' <70'
