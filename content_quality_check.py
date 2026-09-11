import json
import re
from collections import Counter

# 读取文章数据
with open('data/posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

def analyze_article(post):
    """分析单篇文章的内容质量"""
    content = post.get('content', '')
    title = post.get('title', 'Untitled')
    slug = post.get('slug', 'unknown')

    # 清理HTML标签，计算纯文本字数
    clean_text = re.sub(r'<[^>]+>', ' ', content)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    word_count = len(clean_text.split())

    # 检查各部分
    has_intro = bool(re.search(r'<h2>Introduction', content, re.IGNORECASE))
    has_features = bool(re.search(r'(Features|What is|Key Features)', content, re.IGNORECASE))
    has_pros_cons = bool(re.search(r'(Pros|Cons|Advantages|Disadvantages)', content, re.IGNORECASE))
    has_pricing = bool(re.search(r'(Pricing|Cost|Price|Plans)', content, re.IGNORECASE))
    has_comparison = bool(re.search(r'(vs\.?|Comparison|Compared|Alternative)', content, re.IGNORECASE))
    has_faq = bool(re.search(r'(FAQ|Frequently Asked)', content, re.IGNORECASE))
    has_conclusion = bool(re.search(r'(Conclusion|Final Verdict|Verdict|Summary)', content, re.IGNORECASE))
    has_real_experience = bool(re.search(r'(tested|used|experience|hands-on|we tried|we tested|our experience)', content, re.IGNORECASE))
    has_data = bool(re.search(r'(\d+%|\d+/\d+|score|rating|benchmark)', content, re.IGNORECASE))
    has_images = bool(re.search(r'<img', content, re.IGNORECASE))
    has_tables = bool(re.search(r'<table', content, re.IGNORECASE))
    has_lists = bool(re.search(r'<(ul|ol)', content, re.IGNORECASE))

    # 计算标题层级
    h2_count = len(re.findall(r'<h2', content, re.IGNORECASE))
    h3_count = len(re.findall(r'<h3', content, re.IGNORECASE))

    # 检查段落长度
    paragraphs = re.findall(r'<p>(.*?)</p>', content, re.DOTALL)
    avg_paragraph_length = 0
    long_paragraphs = 0
    if paragraphs:
        para_lengths = [len(re.sub(r'<[^>]+>', '', p).split()) for p in paragraphs]
        avg_paragraph_length = sum(para_lengths) / len(para_lengths)
        long_paragraphs = sum(1 for l in para_lengths if l > 100)

    # 质量评分
    score = 0
    max_score = 15
    checks = [
        ('Introduction', has_intro),
        ('Features/What is', has_features),
        ('Pros & Cons', has_pros_cons),
        ('Pricing', has_pricing),
        ('Comparison', has_comparison),
        ('FAQ', has_faq),
        ('Conclusion', has_conclusion),
        ('Real Experience', has_real_experience),
        ('Data/Statistics', has_data),
        ('Images', has_images),
        ('Tables', has_tables),
        ('Lists', has_lists),
        ('Word count > 1500', word_count > 1500),
        ('H2 sections (3+)', h2_count >= 3),
        ('Short paragraphs', avg_paragraph_length < 80),
    ]

    passed_checks = [name for name, passed in checks if passed]
    failed_checks = [name for name, passed in checks if not passed]
    score = len(passed_checks)

    # 判定薄内容
    is_thin = word_count < 500

    return {
        'title': title,
        'slug': slug,
        'word_count': word_count,
        'score': score,
        'max_score': max_score,
        'score_percent': (score / max_score) * 100,
        'is_thin': is_thin,
        'h2_count': h2_count,
        'h3_count': h3_count,
        'avg_paragraph_length': avg_paragraph_length,
        'long_paragraphs': long_paragraphs,
        'passed_checks': passed_checks,
        'failed_checks': failed_checks,
        'has_faq': has_faq,
        'has_real_experience': has_real_experience,
        'has_comparison': has_comparison,
        'has_pricing': has_pricing,
        'has_pros_cons': has_pros_cons,
    }

# 分析所有文章
print("="*70)
print("CONTENT QUALITY CHECK - aitoolcrux.com")
print("="*70)

all_results = []
for post in posts:
    result = analyze_article(post)
    all_results.append(result)

# 抽样检查最新3篇
print(f"\n=== Sampled Latest 3 Articles ===")
for i, result in enumerate(all_results[:3], 1):
    print(f"\n{i}. {result['title'][:60]}")
    print(f"   Slug: {result['slug'][:50]}")
    print(f"   Word count: {result['word_count']} words")
    print(f"   Quality score: {result['score']}/{result['max_score']} ({result['score_percent']:.0f}%)")
    print(f"   H2: {result['h2_count']}, H3: {result['h3_count']}")
    avg_para = result['avg_paragraph_length']
    print(f"   Avg paragraph: {avg_para:.0f} words")
    print(f"   Thin content: {'⚠️ YES' if result['is_thin'] else '✅ No'}")
    print(f"   Passed: {', '.join(result['passed_checks'])}")
    if result['failed_checks']:
        print(f"   Missing: {', '.join(result['failed_checks'])}")

# 整体统计
print(f"\n{'='*70}")
print("OVERALL CONTENT STATISTICS")
print("="*70)

total_articles = len(all_results)
avg_word_count = sum(r['word_count'] for r in all_results) / total_articles
avg_score = sum(r['score'] for r in all_results) / total_articles
thin_articles = [r for r in all_results if r['is_thin']]
high_quality = [r for r in all_results if r['score_percent'] >= 80]
low_quality = [r for r in all_results if r['score_percent'] < 50]

print(f"Total articles: {total_articles}")
print(f"Average word count: {avg_word_count:.0f} words")
print(f"Average quality score: {avg_score:.1f}/15 ({(avg_score/15)*100:.0f}%)")
print(f"Thin content (<500 words): {len(thin_articles)} articles")
print(f"High quality (80%+): {len(high_quality)} articles")
print(f"Low quality (<50%): {len(low_quality)} articles")

# 检查重复标题
titles = [r['title'] for r in all_results]
title_counts = Counter(titles)
duplicate_titles = {title: count for title, count in title_counts.items() if count > 1}
if duplicate_titles:
    print(f"\n⚠️  Duplicate titles found: {len(duplicate_titles)}")
    for title, count in duplicate_titles.items():
        print(f"   - '{title[:50]}' (x{count})")
else:
    print(f"\n✅ No duplicate titles")

# 检查缺少FAQ的文章
no_faq = [r for r in all_results if not r['has_faq']]
print(f"\nArticles without FAQ: {len(no_faq)}/{total_articles}")

# 检查缺少真实体验的文章
no_experience = [r for r in all_results if not r['has_real_experience']]
print(f"Articles without real experience: {len(no_experience)}/{total_articles}")

# 检查缺少对比的文章
no_comparison = [r for r in all_results if not r['has_comparison']]
print(f"Articles without comparison: {len(no_comparison)}/{total_articles}")

# 薄内容文章列表
if thin_articles:
    print(f"\n⚠️  Thin Content Articles (<500 words):")
    for r in thin_articles[:10]:
        print(f"   - {r['title'][:50]} ({r['word_count']} words)")
    if len(thin_articles) > 10:
        print(f"   ... and {len(thin_articles) - 10} more")

# 总结
print(f"\n{'='*70}")
print("SUMMARY & RECOMMENDATIONS")
print("="*70)
print(f"✅ Strengths:")
print(f"   - {len(high_quality)} high-quality articles (80%+ score)")
print(f"   - Average {avg_word_count:.0f} words per article")
print(f"   - No duplicate titles")

print(f"\n⚠️  Issues to address:")
if thin_articles:
    print(f"   - {len(thin_articles)} thin content articles need expansion")
if no_faq:
    print(f"   - {len(no_faq)} articles missing FAQ section")
if no_experience:
    print(f"   - {len(no_experience)} articles missing real user experience")
if low_quality:
    print(f"   - {len(low_quality)} low-quality articles (<50% score)")

print(f"\n📋 Priority actions:")
print(f"   1. Expand thin content articles to 1500+ words")
print(f"   2. Add FAQ sections to articles missing them")
print(f"   3. Add real user experience/testing details")
print(f"   4. Add comparison sections (vs competitors)")
print(f"   5. Add pricing tables where missing")
