#!/usr/bin/env python3
"""
AIToolCrux Content Quality Audit Script
Runs deterministic quality checks on all articles in data/posts.json.
Usage: python scripts/quality_audit.py [--fix] [--min-score 85]
"""

import json
import re
import sys
import os
import html
from collections import defaultdict

POSTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'posts.json')

def count_words(html_str):
    text = re.sub(r'<[^>]+>', ' ', html_str)
    text = html.unescape(text)
    return len(text.split())

def count_internal_links(content):
    html_links = len(re.findall(r'href="/(blog|category|tools|alternatives|comparisons|compare|ranking|best-for)/', content))
    md_links = len(re.findall(r'\]\(/(blog|category|tools|alternatives|comparisons|compare|ranking|best-for)/', content))
    return html_links + md_links

def has_section(content, patterns):
    for p in patterns:
        if re.search(p, content, re.I):
            return True
    return False

def count_images(content):
    return len(re.findall(r'<img\s', content, re.I))

def get_first_paragraph(content):
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
    for p in paragraphs:
        text = re.sub(r'<[^>]+>', '', p).strip()
        if len(text) > 20:
            return text
    return ''

def flesch_reading_ease(text):
    """Simplified Flesch Reading Ease calculation."""
    sentences = max(1, len(re.findall(r'[.!?]+', text)))
    words = max(1, len(text.split()))
    syllables = 0
    for word in text.split():
        word = word.lower()
        vowels = 'aeiouy'
        count = 0
        prev_vowel = False
        for c in word:
            is_vowel = c in vowels
            if is_vowel and not prev_vowel:
                count += 1
            prev_vowel = is_vowel
        if word.endswith('e') and count > 1:
            count -= 1
        syllables += max(1, count)
    return 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)

def count_qa_pairs(content):
    """Count Q&A pairs (questions followed by answers)."""
    questions = len(re.findall(r'<(?:strong|b|h4|p)[^>]*>\s*(?:Q[:\.]?|Question[:\.]?|How|What|Why|When|Where|Can|Is|Are|Do|Does|Should|Which|Who)\b', content, re.I))
    return questions

def audit_post(post):
    """Audit a single post, return dict of checks."""
    content = post.get('content', '')
    slug = post.get('slug', 'unknown')
    title = post.get('title', '')
    
    checks = {}
    
    # 1. Word count
    wc = count_words(content)
    checks['word_count'] = wc
    checks['word_count_pass'] = wc >= 2000
    
    # 2. Quick Answer
    checks['has_quick_answer'] = has_section(content, [
        r'<h[23][^>]*>\s*Quick Answer',
        r'<h[23][^>]*>\s*TL;DR',
        r'<h[23][^>]*>\s*The Short Version',
        r'<h[23][^>]*>\s*Bottom Line',
    ])
    
    # 3. First paragraph length (AEO: ≤320 chars)
    first_p = get_first_paragraph(content)
    checks['first_para_length'] = len(first_p)
    checks['first_para_pass'] = len(first_p) <= 320
    
    # 4. Key Takeaways
    checks['has_key_takeaways'] = has_section(content, [
        r'<h[23][^>]*>\s*Key Takeaways',
        r'<h[23][^>]*>\s*Key Takeaway',
    ])
    
    # 5. FAQ
    checks['has_faq'] = has_section(content, [
        r'<h[23][^>]*>\s*FAQ',
        r'<h[23][^>]*>\s*Frequently Asked',
    ])
    
    # 6. How We Tested
    checks['has_how_we_tested'] = has_section(content, [
        r'<h[23][^>]*>\s*How We Tested',
        r'<h[23][^>]*>\s*Our Testing',
        r'<h[23][^>]*>\s*Testing Methodology',
    ])
    
    # 7. Internal links
    il = count_internal_links(content)
    checks['internal_links'] = il
    checks['internal_links_pass'] = il >= 3
    
    # 8. Images
    img_count = count_images(content)
    checks['image_count'] = img_count
    checks['has_images'] = img_count >= 1
    
    # 9. Real screenshots flag
    checks['has_real_screenshots'] = post.get('hasRealScreenshots', False)
    
    # 10. Readability
    plain_text = re.sub(r'<[^>]+>', ' ', content)
    plain_text = html.unescape(plain_text)
    fre = flesch_reading_ease(plain_text[:5000])
    checks['flesch_reading_ease'] = round(fre, 1)
    checks['readability_pass'] = fre >= 40  # "fairly easy" or better
    
    # 11. Q&A density
    qa_count = count_qa_pairs(content)
    checks['qa_count'] = qa_count
    checks['qa_density_pass'] = qa_count >= 3
    
    # 12. Title contains keywords
    checks['title_length'] = len(title)
    checks['title_pass'] = 30 <= len(title) <= 70
    
    # 13. Comparison content (A vs B)
    checks['has_comparison'] = bool(re.search(r'\bvs\.?\b|compared to|versus', content, re.I))
    
    # 14. External citations
    ext_links = len(re.findall(r'href="https?://(?!www\.aitoolcrux\.com)', content))
    checks['external_links'] = ext_links
    checks['external_links_pass'] = ext_links >= 1
    
    # Calculate score
    score = 0
    total = 0
    weight_map = {
        'word_count_pass': 10,
        'has_quick_answer': 8,
        'first_para_pass': 5,
        'has_key_takeaways': 5,
        'has_faq': 8,
        'has_how_we_tested': 8,
        'internal_links_pass': 8,
        'has_images': 5,
        'has_real_screenshots': 5,
        'readability_pass': 8,
        'qa_density_pass': 5,
        'title_pass': 5,
        'has_comparison': 5,
        'external_links_pass': 5,
    }
    for check, weight in weight_map.items():
        total += weight
        if checks.get(check, False):
            score += weight
    
    checks['quality_score'] = round(score / total * 100, 1)
    checks['grade'] = 'A' if score/total >= 0.9 else 'B' if score/total >= 0.8 else 'C' if score/total >= 0.7 else 'D' if score/total >= 0.6 else 'F'
    
    return checks

def main():
    fix_mode = '--fix' in sys.argv
    min_score = 85
    if '--min-score' in sys.argv:
        idx = sys.argv.index('--min-score')
        if idx + 1 < len(sys.argv):
            min_score = int(sys.argv[idx + 1])
    
    with open(POSTS_PATH, 'r', encoding='utf-8') as f:
        posts = json.load(f)
    
    results = []
    failed = []
    
    for post in posts:
        checks = audit_post(post)
        results.append({'slug': post['slug'], 'title': post.get('title', ''), **checks})
        if checks['quality_score'] < min_score:
            failed.append((post['slug'], checks['quality_score'], checks['grade']))
    
    # Summary
    avg_score = sum(r['quality_score'] for r in results) / len(results)
    grades = defaultdict(int)
    for r in results:
        grades[r['grade']] += 1
    
    print(f"\n{'='*60}")
    print(f"AIToolCrux Content Quality Audit")
    print(f"{'='*60}")
    print(f"Total articles: {len(results)}")
    print(f"Average quality score: {avg_score:.1f}/100")
    print(f"Grade distribution: A={grades['A']}, B={grades['B']}, C={grades['C']}, D={grades['D']}, F={grades['F']}")
    print(f"Articles below {min_score}: {len(failed)}")
    print(f"{'='*60}\n")
    
    # Category pass rates
    categories = ['word_count_pass', 'has_quick_answer', 'first_para_pass', 'has_key_takeaways',
                  'has_faq', 'has_how_we_tested', 'internal_links_pass', 'has_images',
                  'has_real_screenshots', 'readability_pass', 'qa_density_pass', 'title_pass',
                  'has_comparison', 'external_links_pass']
    print("Category pass rates:")
    for cat in categories:
        passed = sum(1 for r in results if r.get(cat, False))
        pct = passed / len(results) * 100
        status = '✓' if pct >= 90 else '⚠' if pct >= 70 else '✗'
        print(f"  {status} {cat}: {passed}/{len(results)} ({pct:.0f}%)")
    
    if failed:
        print(f"\nArticles below {min_score} (need attention):")
        for slug, score, grade in sorted(failed, key=lambda x: x[1]):
            print(f"  {grade} {score:.0f}: {slug}")
    
    # Write report
    report_path = os.path.join(os.path.dirname(__file__), '..', 'iteration_center', 'quality_audit_report.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# AIToolCrux Content Quality Audit Report\n\n")
        f.write(f"**Date:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"## Summary\n\n")
        f.write(f"- Total articles: {len(results)}\n")
        f.write(f"- Average quality score: {avg_score:.1f}/100\n")
        f.write(f"- Grade distribution: A={grades['A']}, B={grades['B']}, C={grades['C']}, D={grades['D']}, F={grades['F']}\n")
        f.write(f"- Articles below {min_score}: {len(failed)}\n\n")
        f.write(f"## Category Pass Rates\n\n")
        f.write(f"| Category | Pass | Total | Rate |\n")
        f.write(f"|----------|------|-------|------|\n")
        for cat in categories:
            passed = sum(1 for r in results if r.get(cat, False))
            pct = passed / len(results) * 100
            f.write(f"| {cat} | {passed} | {len(results)} | {pct:.0f}% |\n")
        f.write(f"\n## Per-Article Scores\n\n")
        f.write(f"| Slug | Score | Grade | Words | Links | Images | Flesch |\n")
        f.write(f"|------|-------|-------|-------|-------|--------|--------|\n")
        for r in sorted(results, key=lambda x: x['quality_score']):
            f.write(f"| {r['slug'][:40]} | {r['quality_score']:.0f} | {r['grade']} | {r['word_count']} | {r['internal_links']} | {r['image_count']} | {r['flesch_reading_ease']} |\n")
    
    print(f"\nReport written to: {report_path}")
    
    return 0 if not failed else 1

if __name__ == '__main__':
    sys.exit(main())
