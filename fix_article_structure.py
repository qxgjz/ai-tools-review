import json
import re

with open('data/posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

print(f"Total posts: {len(posts)}")
print("\n=== Checking Article Structure Issues ===")

fixes_applied = 0

for i, post in enumerate(posts):
    title = post.get('title', '')
    content = post.get('content', '')
    original_content = content
    issues = []

    # 1. 修复"competing tools"模板变量
    if 'competing tools' in content.lower():
        # 查找具体的上下文
        matches = re.findall(r'.{0,50}competing tools.{0,50}', content, re.IGNORECASE)
        for match in matches:
            issues.append(f"competing tools: ...{match}...")
        # 替换为更自然的表达
        content = re.sub(r'\d+\s*competing\s+tools', 'alternative tools', content, flags=re.IGNORECASE)
        content = re.sub(r'competing tools', 'alternative tools', content, flags=re.IGNORECASE)

    # 2. 修复重复总结（同时有Final Words和Final Verdict）
    has_final_words = 'Final Words' in content or 'final words' in content.lower()
    has_final_verdict = 'Final Verdict' in content or 'final verdict' in content.lower()

    if has_final_words and has_final_verdict:
        issues.append("Has both Final Words and Final Verdict")
        # 保留Final Verdict，移除Final Words部分（如果Final Words较短）
        # 找到Final Words部分并移除
        content = re.sub(r'##\s*Final Words.*?(?=##\s*Final Verdict)', '', content, flags=re.DOTALL | re.IGNORECASE)

    # 3. 修复Introduction在Final之后的问题
    intro_pos = content.lower().find('introduction')
    final_pos = content.lower().find('final ')

    if intro_pos > 0 and final_pos > 0 and intro_pos > final_pos:
        issues.append(f"Introduction (pos {intro_pos}) after Final (pos {final_pos})")
        # 这种情况比较复杂，通常是因为文章结构混乱
        # 我们标记但不自动修复，因为需要人工判断

    # 4. 修复"My Hands-On Experience with Best"模板问题
    if 'Hands-On Experience with Best' in content:
        issues.append("'Hands-On Experience with Best' template issue")
        content = content.replace('Hands-On Experience with Best', 'Hands-On Experience')

    # 5. 检查空的模板变量
    empty_vars = re.findall(r'\{[a-zA-Z_]+\}', content)
    if empty_vars:
        issues.append(f"Empty template variables: {empty_vars[:5]}")
        for var in set(empty_vars):
            content = content.replace(var, '')

    # 6. 修复AI味的典型表达
    ai_phrases = [
        (r'In conclusion,', 'Ultimately,'),
        (r'It is important to note that', 'Notably,'),
        (r'As mentioned above,', ''),
        (r'First and foremost,', 'First,'),
        (r'Last but not least,', 'Finally,'),
        (r'In today\'s digital age,', ''),
        (r'With the rapid advancement of technology,', ''),
    ]
    for pattern, replacement in ai_phrases:
        if re.search(pattern, content, re.IGNORECASE):
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

    if issues:
        print(f"\nPost {i}: {title[:50]}")
        for issue in issues:
            print(f"  - {issue}")

    if content != original_content:
        post['content'] = content
        fixes_applied += 1
        print(f"  ✓ Fixed ({len(issues)} issues)")

print(f"\n=== Fixes Applied: {fixes_applied} posts ===")

# 保存修复后的文章
with open('data/posts.json', 'w', encoding='utf-8') as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)

print("Saved updated posts.json")

# 统计文章质量
print("\n=== Article Quality Summary ===")
total_words = 0
short_articles = 0
for post in posts:
    content = post.get('content', '')
    word_count = len(content.split())
    total_words += word_count
    if word_count < 500:
        short_articles += 1

print(f"Total articles: {len(posts)}")
print(f"Average word count: {total_words // len(posts)}")
print(f"Short articles (<500 words): {short_articles}")
print(f"Articles with FAQ: {sum(1 for p in posts if p.get('faqs') and len(p['faqs']) > 0)}")
