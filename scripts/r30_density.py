# -*- coding: utf-8 -*-
import io,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
FILES={
'claude-rate-limits':'content_drafts/2026-10-21-claude-rate-limits-2026_NEW.md',
'voice-changer-vs-voicemod':'content_drafts/2026-10-21-ai-voice-changer-vs-voicemod-2026_NEW.md',
'best-free-ai-voice-changers':'content_drafts/2026-10-21-best-free-ai-voice-changers-2026_NEW.md',
'free-ai-fitness-coaches':'content_drafts/2026-10-21-free-ai-fitness-coaches-2026_NEW.md',
'free-ai-tools-for-students':'content_drafts/2026-10-21-free-ai-tools-for-students-2026_NEW.md',
'non-technical':'content_drafts/2026-10-21-ai-tools-for-non-technical-users-2026_NEW.md',
}
KW={
'claude-rate-limits':'claude rate limits',
'voice-changer-vs-voicemod':'voice changer vs voicemod',
'best-free-ai-voice-changers':'free ai voice changers',
'free-ai-fitness-coaches':'free ai fitness coaches',
'free-ai-tools-for-students':'free ai tools for students',
'non-technical':'ai tools for non-technical users',
}
for k,f in FILES.items():
    t=io.open(f,encoding='utf-8',errors='ignore').read()
    t=re.sub(r'!\[[^\]]*\]\([^)]*\)','',t); t=re.sub(r'```.*?```','',t,flags=re.S)
    words=re.findall(r"[A-Za-z']+",t.lower())
    kw=KW[k]; n=len(words); occ=len(re.findall(re.escape(kw),t.lower()))
    dens=occ/n*100 if n else 0
    print(f'{k:32s} words={n:5d} occ={occ:2d} density={dens:.2f}% {"PASS" if dens>=0.5 else "FAIL"}')
