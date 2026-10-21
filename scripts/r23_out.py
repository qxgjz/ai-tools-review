# -*- coding: utf-8 -*-
import io,re,os,glob
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
targets={'dify_ai_review':None,'stable-diffusion-review-2026':None,'cursor_ai_review':None,'gemini_38_flash_review':None,
'adobe-firefly-review-2026':None,'ai-coding-tools-comparison-2026':None,'best-ai-voice-changers-2026':None}
# locate index.html / index.txt under out/blog
for slug in targets:
    hits=glob.glob(os.path.join('out','blog',slug,'**','index.*'),recursive=True)+glob.glob(os.path.join('out','blog',slug,'index.*'))
    targets[slug]=hits
for slug,hits in targets.items():
    print('\n###',slug,'files=',hits)
    for f in hits[:1]:
        raw=io.open(f,encoding='utf-8',errors='replace').read()
        tm=re.search(r'<title>(.*?)</title>',raw,re.S|re.I)
        dm=re.search(r'<meta\s+name="description"\s+content="([^"]*)"',raw,re.I)
        print(' title:',tm.group(1).strip() if tm else 'NONE','(',len(tm.group(1).strip()) if tm else 0,')')
        print(' desc :',(dm.group(1)[:160] if dm else 'NONE'))
