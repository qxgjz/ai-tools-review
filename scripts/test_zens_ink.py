"""测试zens-ink各模块是否可用"""
import os
os.environ['SERPER_API_KEY'] = 'db3bbe31d1470d3d4358896851c04030d2e76a6e'

from zens_ink import kd, search_intent, competitor_gap, reddit_blueocean

# 测试1: fetch_serp
print('=== 测试 kd.fetch_serp ===')
serp = kd.fetch_serp('Claude vs ChatGPT', gl='us', hl='en', num=5)
if serp:
    organic = serp.get('organic', [])
    print(f'获取到 {len(organic)} 个结果')
    for r in organic[:3]:
        title = r.get('title', '')[:60]
        print(f'  - {title}')
else:
    print('失败')

print()
# 测试2: calculate_kd
print('=== 测试 kd.calculate_kd ===')
kd_score = kd.calculate_kd(serp, 'Claude vs ChatGPT')
print(f'KD分数: {kd_score}')

print()
# 测试3: search_intent
print('=== 测试 search_intent.classify ===')
for kw in ['Claude vs ChatGPT', 'best AI tools 2026', 'how to use Claude', 'Claude pricing']:
    result = search_intent.classify(kw)
    print(f'  {kw}: {result}')

print()
# 测试4: competitor_gap
print('=== 测试 competitor_gap.fetch_sitemap ===')
try:
    urls = competitor_gap.fetch_sitemap('https://www.futurepedia.io/sitemap.xml')
    print(f'获取到 {len(urls)} 个URL')
    print(f'前3个: {urls[:3]}')
except Exception as e:
    print(f'失败: {e}')

print()
# 测试5: reddit_blueocean
print('=== 测试 reddit_blueocean.search_reddit ===')
try:
    posts = reddit_blueocean.search_reddit('AI tools recommendations', limit=5)
    print(f'获取到 {len(posts)} 个帖子')
except Exception as e:
    print(f'失败: {e}')

print()
# 测试6: kd.format_report
print('=== 测试 kd.format_report ===')
try:
    report = kd.format_report(serp, 'Claude vs ChatGPT')
    print(report[:500])
except Exception as e:
    print(f'失败: {e}')
