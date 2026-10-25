import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\public\_redirects'
text = '''

# r63 P0-CANONICAL-REDIRECT-AUDIT-20261026: URL canonicalization (GSC home x3 / about x2)
/index.html / 301
/index / 301

# r63 P0-ARTICLE-API-URL-CLEAN-20261026: legacy article-api pseudo URLs -> canonical article or 410
/blog/article-api-20260904-215236-midjourney-v7-review-2026-is-it-still-the-best-ai-image-generator-md /blog/midjourney-v7-review-2026/ 301
/blog/article-api-* 410
'''
with open(P, 'a', encoding='utf-8') as f:
    f.write(text)
print('_redirects appended. lines now:', sum(1 for _ in open(P, encoding='utf-8')))
