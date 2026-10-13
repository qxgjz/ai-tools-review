# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
print('posts total:', len(posts))
# show a batch14-style entry (find newest slugs)
for p in posts:
    if p.get('slug') in ('what-is-an-ai-agent','best-ai-agents-2026','ai-agent-vs-chatbot-2026','how-to-build-an-ai-agent'):
        print('SLUG:', p.get('slug'))
        print('  keys:', list(p.keys()))
        print('  id:', p.get('id'), '| title:', p.get('title'))
        print('  excerpt:', (p.get('excerpt') or '')[:100])
        print('  date:', p.get('date'), '| category:', p.get('category'), '| catSlug:', p.get('categorySlug'))
        print('  author:', p.get('author'), '| rt:', p.get('readingTime'), '| wc:', p.get('wordCount'), '| tags:', p.get('tags'))
        print('  hsr:', p.get('hasRealScreenshots'), '| sc:', p.get('screenshotCount'))
        print('  content head:', (p.get('content') or '')[:120].replace(chr(10),' | '))
        print('  qa:', (p.get('quickAnswer') or '')[:90])
        print('  kt:', (p.get('keyTakeaways') or '')[:90])
        print('  faq type:', type(p.get('faq')))
        print()
# find cursor-vs-windsurf entry
for p in posts:
    if p.get('slug') == 'cursor-vs-windsurf-2026':
        print('FOUND cursor-vs-windsurf-2026 | keys:', list(p.keys()))
        print('  title:', p.get('title'), '| wc:', p.get('wordCount'), '| content head:', (p.get('content') or '')[:150])
        break
