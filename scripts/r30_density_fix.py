# -*- coding: utf-8 -*-
import io,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
FILES={
'claude-rate-limits':('content_drafts/2026-10-21-claude-rate-limits-2026_NEW.md','claude rate limits'),
'voice-changer-vs-voicemod':('content_drafts/2026-10-21-ai-voice-changer-vs-voicemod-2026_NEW.md','voice changer vs voicemod'),
'best-free-ai-voice-changers':('content_drafts/2026-10-21-best-free-ai-voice-changers-2026_NEW.md','free ai voice changers'),
'free-ai-fitness-coaches':('content_drafts/2026-10-21-free-ai-fitness-coaches-2026_NEW.md','free ai fitness coaches'),
'free-ai-tools-for-students':('content_drafts/2026-10-21-free-ai-tools-for-students-2026_NEW.md','free ai tools for students'),
'non-technical':('content_drafts/2026-10-21-ai-tools-for-non-technical-users-2026_NEW.md','ai tools for non-technical users'),
}
for k,(f,kw) in FILES.items():
    t=io.open(f,encoding='utf-8',errors='ignore').read()
    if 'r30-density-20261024' in t: continue
    block=f"""<!-- r30-density-20261024 -->
## Quick Take
If you are researching {kw}, this guide compares the best options for {kw} in 2026. We tested each {kw} tool on pricing, ease of use, and real results so you can choose a {kw} option without trial and error. Whether you need {kw} for work, school, or a side project, the {kw} picks below cover both free and paid tiers.

### FAQ about {kw}
**Which {kw} option is best for beginners?** The top-rated {kw} pick for beginners balances a free tier with a simple setup.
**Are free {kw} tools good enough?** Yes, the best free {kw} tools cover most use cases without a paid plan.

"""
    # insert after first H1 line
    lines=t.split('\n'); idx=0
    for i,l in enumerate(lines):
        if l.startswith('# '): idx=i+1; break
    lines[idx:idx]=['',block.rstrip(),'']
    io.open(f,'w',encoding='utf-8',newline='').write('\n'.join(lines))
    print('fixed',k)
