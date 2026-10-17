import os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
red = open('public/_redirects','r',encoding='utf-8').read()
print('len',len(red),'has171438', '171438' in red, 'has article-api', 'article-api' in red)
print('--- tail 400 ---')
print(red[-400:])
