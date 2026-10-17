import os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
red = open('public/_redirects','r',encoding='utf-8').read().splitlines()
for ln in red:
    if 'article-api' in ln:
        print(ln)
