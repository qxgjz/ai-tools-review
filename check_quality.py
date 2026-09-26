import json

posts = json.load(open('data/posts.json', 'r', encoding='utf-8'))
today = [p for p in posts if p.get('date', '').startswith('2026-09-16')]

print(f'今天发布的 {len(today)} 篇文章质量检查：')
print('=' * 60)

total_words = 0
has_qa = 0
has_kt = 0
has_faq = 0
has_screenshot = 0

for p in today:
    slug = p['slug']
    word_count = p.get('wordCount', 0)
    content = p.get('content', '')
    total_words += word_count
    
    if 'Quick Answer' in content:
        has_qa += 1
    if 'Key Takeaways' in content:
        has_kt += 1
    if 'FAQ' in content or 'faq' in content.lower():
        has_faq += 1
    if '/screenshots/' in content:
        has_screenshot += 1
    
    print(f'{slug}:')
    print(f'  字数: {word_count}')
    print(f'  Quick Answer: {"✅" if "Quick Answer" in content else "❌"}')
    print(f'  Key Takeaways: {"✅" if "Key Takeaways" in content else "❌"}')
    print(f'  FAQ: {"✅" if "FAQ" in content or "faq" in content.lower() else "❌"}')
    print(f'  有截图: {"✅" if "/screenshots/" in content else "❌"}')
    print()

print('=' * 60)
print(f'汇总：')
print(f'  平均字数: {total_words // len(today)}')
print(f'  有Quick Answer: {has_qa}/{len(today)}')
print(f'  有Key Takeaways: {has_kt}/{len(today)}')
print(f'  有FAQ: {has_faq}/{len(today)}')
print(f'  有截图: {has_screenshot}/{len(today)}')
