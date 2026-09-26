import requests
import time
from datetime import datetime

SITE_URL = "https://www.aitoolcrux.com"

# 要监控的页面
pages_to_monitor = [
    ("/", "Homepage"),
    ("/ranking", "Ranking Page"),
    ("/category/chat", "Category Page"),
    ("/tools/chatgpt", "Tool Detail Page"),
    ("/tools/cursor", "Tool Detail Page (Cursor)"),
    ("/blog", "Blog List Page"),
    ("/blog/cursor-ai-review-2026-best-ai-code-editor", "Blog Article Page"),
]

def measure_page(url, name):
    """测量单个页面的性能指标"""
    result = {
        'name': name,
        'url': url,
        'status': None,
        'ttfb': None,
        'total_time': None,
        'content_size': None,
        'content_size_kb': None,
        'headers': {},
        'errors': [],
    }

    try:
        # 开始计时
        start_time = time.time()

        # 发送请求，允许重定向
        response = requests.get(
            url,
            timeout=30,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            allow_redirects=True
        )

        # 计算时间
        end_time = time.time()
        total_time = (end_time - start_time) * 1000  # 转换为毫秒

        result['status'] = response.status_code
        result['total_time'] = total_time
        result['content_size'] = len(response.content)
        result['content_size_kb'] = result['content_size'] / 1024

        # 获取响应头
        result['headers'] = dict(response.headers)

        # 检查状态码
        if response.status_code != 200:
            result['errors'].append(f"HTTP Status: {response.status_code}")

        # 检查内容大小
        if result['content_size_kb'] > 2000:
            result['errors'].append(f"Content too large: {result['content_size_kb']:.0f}KB (>2000KB)")

        # 检查加载时间
        if total_time > 5000:
            result['errors'].append(f"Load time too slow: {total_time:.0f}ms (>5000ms)")

        # 检查压缩
        content_encoding = response.headers.get('Content-Encoding', 'none')
        if content_encoding == 'none' and result['content_size_kb'] > 100:
            result['errors'].append("No compression detected (gzip/brotli)")

        # 检查缓存
        cache_control = response.headers.get('Cache-Control', 'none')
        if cache_control == 'none':
            result['errors'].append("No Cache-Control header")

        # 检查HTTPS
        if not url.startswith('https://'):
            result['errors'].append("Not using HTTPS")

    except requests.exceptions.Timeout:
        result['errors'].append("Request timed out (>30s)")
    except requests.exceptions.ConnectionError:
        result['errors'].append("Connection error")
    except Exception as e:
        result['errors'].append(f"Error: {str(e)}")

    return result

# 主程序
print("="*70)
print("PERFORMANCE MONITOR - aitoolcrux.com")
print(f"Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*70)

all_results = []
for path, name in pages_to_monitor:
    url = SITE_URL + path
    print(f"\nMeasuring: {name}")
    print(f"  URL: {url}")

    result = measure_page(url, name)
    all_results.append(result)

    # 显示结果
    status_icon = "✅" if result['status'] == 200 else "❌"
    print(f"  Status: {status_icon} {result['status']}")
    print(f"  Load time: {result['total_time']:.0f}ms" if result['total_time'] else "  Load time: N/A")
    print(f"  Content size: {result['content_size_kb']:.1f}KB" if result['content_size_kb'] else "  Content size: N/A")

    # 显示响应头关键信息
    if result['headers']:
        print(f"  Content-Encoding: {result['headers'].get('Content-Encoding', 'none')}")
        print(f"  Cache-Control: {result['headers'].get('Cache-Control', 'none')[:50]}")
        print(f"  Server: {result['headers'].get('Server', 'unknown')}")

    if result['errors']:
        print(f"  ⚠️  Issues: {'; '.join(result['errors'])}")

# 性能评分
print(f"\n{'='*70}")
print("PERFORMANCE SUMMARY")
print("="*70)

# 计算平均指标
valid_results = [r for r in all_results if r['total_time'] is not None]
if valid_results:
    avg_load_time = sum(r['total_time'] for r in valid_results) / len(valid_results)
    avg_content_size = sum(r['content_size_kb'] for r in valid_results) / len(valid_results)
    max_load_time = max(r['total_time'] for r in valid_results)
    min_load_time = min(r['total_time'] for r in valid_results)

    print(f"Pages measured: {len(valid_results)}")
    print(f"Average load time: {avg_load_time:.0f}ms")
    print(f"Fastest page: {min_load_time:.0f}ms")
    print(f"Slowest page: {max_load_time:.0f}ms")
    print(f"Average content size: {avg_content_size:.1f}KB")

    # 性能评分
    score = 100
    if avg_load_time > 2000:
        score -= 20
    elif avg_load_time > 1000:
        score -= 10
    if avg_content_size > 1000:
        score -= 15
    elif avg_content_size > 500:
        score -= 5

    total_errors = sum(len(r['errors']) for r in all_results)
    score -= total_errors * 5

    score = max(0, min(100, score))

    print(f"\nPerformance Score: {score}/100")

    if score >= 90:
        print("✅ Excellent performance!")
    elif score >= 70:
        print("⚠️  Good performance, some improvements possible")
    elif score >= 50:
        print("⚠️  Fair performance, significant improvements needed")
    else:
        print("❌ Poor performance, urgent optimization required")

# 页面性能排名
print(f"\n{'='*70}")
print("PAGE PERFORMANCE RANKING (Fastest first)")
print("="*70)

sorted_results = sorted(valid_results, key=lambda x: x['total_time'])
for i, result in enumerate(sorted_results, 1):
    speed_icon = "⚡" if result['total_time'] < 1000 else "🐢" if result['total_time'] > 3000 else "✅"
    print(f"{i:2d}. {speed_icon} {result['name']:30s} - {result['total_time']:6.0f}ms - {result['content_size_kb']:7.1f}KB")

# 优化建议
print(f"\n{'='*70}")
print("OPTIMIZATION RECOMMENDATIONS")
print("="*70)

if max_load_time > 3000:
    slow_pages = [r for r in valid_results if r['total_time'] > 3000]
    print(f"⚠️  Slow pages (>3s): {len(slow_pages)}")
    for r in slow_pages:
        print(f"   - {r['name']}: {r['total_time']:.0f}ms, {r['content_size_kb']:.0f}KB")
    print("   Recommendation: Enable caching, optimize images, reduce JavaScript")

if avg_content_size > 500:
    print(f"\n⚠️  Large content size: {avg_content_size:.0f}KB average")
    print("   Recommendation: Enable Brotli compression, optimize images, lazy load below-fold content")

# 检查是否有页面没有压缩
uncompressed = [r for r in all_results if r['headers'] and r['headers'].get('Content-Encoding', 'none') == 'none' and r['content_size_kb'] and r['content_size_kb'] > 100]
if uncompressed:
    print(f"\n⚠️  Uncompressed pages: {len(uncompressed)}")
    for r in uncompressed:
        print(f"   - {r['name']}")
    print("   Recommendation: Enable gzip/Brotli compression on server")

print("\n✅ Performance monitoring complete!")
