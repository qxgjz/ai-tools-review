import os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
txt=open('public/_redirects','r',encoding='utf-8').read()
checks={
 '/blog/article-api-20260903-171438-creatium-coach-review-2025-is-this-ai-content-coach-worth-your-time-md':'/blog/creatium-coach-review-2025/',
 '/blog/article-api-20260903-173022-creatium-coach-review-2025-a-handy-way-to-turn-documents-into-a-coach-but-not-a-md':'/blog/creatium-coach-review-2025/',
 '/blog/article-api-20260903-173210-elevenlabs-review-2026-is-it-still-the-most-human-like-ai-voice-generator-md':'/blog/elevenlabs-review-2026/',
}
for old,new in checks.items():
    hit=[l for l in txt.splitlines() if old in l and new in l]
    print('OK' if hit else 'MISS', old[:55], '->', new, '|', hit[0].strip() if hit else '')
