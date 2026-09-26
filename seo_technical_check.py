import requests
import re
from urllib.parse import urljoin

SITE_URL = "https://www.aitoolcrux.com"

# 要检查的关键页面
pages_to_check = [
    ("/", "Homepage"),
    ("/ranking", "Ranking Page"),
    ("/category/chat", "Category Page"),
    ("/tools/chatgpt", "Tool Detail Page"),
    ("/blog", "Blog List Page"),
    ("/blog/perplexity-ai-review-2026-best-ai-search-engine", "New Article Page"),
    ("/methodology", "Methodology Page"),
    ("/about", "About Page"),
]

def check_page(url, name):
    """检查单个页面的SEO元素"""
    result = {
        'name': name,
        'url': url,
        'status': None,
        'title': None,
        'title_length': 0,
        'meta_description': None,
        'meta_description_length': 0,
        'h1_count': 0,
        'h1_text': None,
        'canonical': None,
        'meta_robots': None,
        'og_title': None,
        'og_description': None,
        'json_ld_count': 0,
        'json_ld_types': [],
        'lang': None,
        'errors': [],
        'warnings': [],
    }

    try:
        response = requests.get(url, timeout=20, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; SEO-Checker/1.0)'
        })
        result['status'] = response.status_code

        if response.status_code != 200:
            result['errors'].append(f"HTTP Status: {response.status_code}")
            return result

        html = response.text

        # Title
        title_match = re.search(r'<title>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
        if title_match:
            result['title'] = title_match.group(1).strip()
            result['title_length'] = len(result['title'])
            if result['title_length'] < 30:
                result['warnings'].append(f"Title too short: {result['title_length']} chars (min 30)")
            elif result['title_length'] > 70:
                result['warnings'].append(f"Title too long: {result['title_length']} chars (max 70)")
        else:
            result['errors'].append("Missing <title> tag")

        # Meta Description
        desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
        if desc_match:
            result['meta_description'] = desc_match.group(1).strip()
            result['meta_description_length'] = len(result['meta_description'])
            if result['meta_description_length'] < 50:
                result['warnings'].append(f"Meta description too short: {result['meta_description_length']} chars (min 50)")
            elif result['meta_description_length'] > 160:
                result['warnings'].append(f"Meta description too long: {result['meta_description_length']} chars (max 160)")
        else:
            result['warnings'].append("Missing meta description")

        # H1
        h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL | re.IGNORECASE)
        result['h1_count'] = len(h1_matches)
        if h1_matches:
            result['h1_text'] = re.sub(r'<[^>]+>', '', h1_matches[0]).strip()
        if result['h1_count'] == 0:
            result['errors'].append("Missing H1 tag")
        elif result['h1_count'] > 1:
            result['warnings'].append(f"Multiple H1 tags: {result['h1_count']} (should be 1)")

        # Canonical
        canonical_match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', html, re.IGNORECASE)
        if canonical_match:
            result['canonical'] = canonical_match.group(1)
        else:
            result['warnings'].append("Missing canonical link")

        # Meta Robots
        robots_match = re.search(r'<meta\s+name=["\']robots["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
        if robots_match:
            result['meta_robots'] = robots_match.group(1)
            if 'noindex' in result['meta_robots'].lower():
                result['errors'].append("Page has noindex - will not be indexed!")
        else:
            result['warnings'].append("Missing meta robots tag (default: index, follow)")

        # OG Tags
        og_title_match = re.search(r'<meta\s+property=["\']og:title["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
        if og_title_match:
            result['og_title'] = og_title_match.group(1)

        og_desc_match = re.search(r'<meta\s+property=["\']og:description["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
        if og_desc_match:
            result['og_description'] = og_desc_match.group(1)

        # JSON-LD
        json_ld_matches = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.DOTALL | re.IGNORECASE)
        result['json_ld_count'] = len(json_ld_matches)
        for match in json_ld_matches:
            type_match = re.search(r'"@type"\s*:\s*"([^"]+)"', match)
            if type_match:
                result['json_ld_types'].append(type_match.group(1))

        # HTML lang
        lang_match = re.search(r'<html[^>]*lang=["\']([^"\']+)["\']', html, re.IGNORECASE)
        if lang_match:
            result['lang'] = lang_match.group(1)

    except Exception as e:
        result['errors'].append(f"Request error: {str(e)}")

    return result

def check_robots_txt():
    """检查robots.txt"""
    print("\n" + "="*60)
    print("ROBOTS.TXT CHECK")
    print("="*60)
    try:
        response = requests.get(f"{SITE_URL}/robots.txt", timeout=10)
        if response.status_code == 200:
            print("✅ robots.txt found (200 OK)")
            print("\nContent:")
            print(response.text[:500])
            if 'Sitemap:' in response.text:
                print("\n✅ Sitemap declared in robots.txt")
            else:
                print("\n⚠️  Sitemap NOT declared in robots.txt")
        else:
            print(f"❌ robots.txt returned status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking robots.txt: {e}")

def check_sitemap():
    """检查sitemap.xml"""
    print("\n" + "="*60)
    print("SITEMAP.XML CHECK")
    print("="*60)
    try:
        response = requests.get(f"{SITE_URL}/sitemap.xml", timeout=15)
        if response.status_code == 200:
            print("✅ sitemap.xml found (200 OK)")
            # 统计URL数量
            url_count = response.text.count('<url>')
            print(f"   URLs in sitemap: {url_count}")
            # 检查最后修改
            if '<lastmod>' in response.text:
                print("   ✅ Lastmod dates present")
            else:
                print("   ⚠️  No lastmod dates")
        else:
            print(f"❌ sitemap.xml returned status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking sitemap: {e}")

def check_404_page():
    """检查404页面"""
    print("\n" + "="*60)
    print("404 PAGE CHECK")
    print("="*60)
    try:
        response = requests.get(f"{SITE_URL}/this-page-does-not-exist-12345", timeout=10)
        print(f"Status code: {response.status_code}")
        if response.status_code == 404:
            print("✅ Correct 404 status code")
        else:
            print(f"⚠️  Expected 404, got {response.status_code}")
        if '404' in response.text or 'Not Found' in response.text or 'not found' in response.text:
            print("✅ 404 message present on page")
        else:
            print("⚠️  No clear 404 message on page")
    except Exception as e:
        print(f"❌ Error checking 404: {e}")

# 主程序
print("="*60)
print("SEO TECHNICAL CHECK - aitoolcrux.com")
print("="*60)

# 检查关键页面
all_results = []
for path, name in pages_to_check:
    url = urljoin(SITE_URL, path)
    print(f"\nChecking: {name} ({url})")
    result = check_page(url, name)
    all_results.append(result)

    print(f"  Status: {result['status']}")
    print(f"  Title: {result['title'][:60] if result['title'] else 'MISSING'}... ({result['title_length']} chars)")
    print(f"  Meta Desc: {'Present' if result['meta_description'] else 'MISSING'} ({result['meta_description_length']} chars)")
    print(f"  H1: {result['h1_count']} - {result['h1_text'][:50] if result['h1_text'] else 'N/A'}")
    print(f"  Canonical: {'Present' if result['canonical'] else 'MISSING'}")
    print(f"  Meta Robots: {result['meta_robots'] or 'default (index, follow)'}")
    print(f"  JSON-LD: {result['json_ld_count']} scripts - Types: {', '.join(result['json_ld_types'][:3])}")
    print(f"  Lang: {result['lang'] or 'MISSING'}")

    if result['errors']:
        print(f"  ❌ ERRORS: {'; '.join(result['errors'])}")
    if result['warnings']:
        print(f"  ⚠️  WARNINGS: {'; '.join(result['warnings'][:2])}")

# 检查robots.txt, sitemap, 404
check_robots_txt()
check_sitemap()
check_404_page()

# 总结
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
total_errors = sum(len(r['errors']) for r in all_results)
total_warnings = sum(len(r['warnings']) for r in all_results)
print(f"Pages checked: {len(all_results)}")
print(f"Total errors: {total_errors}")
print(f"Total warnings: {total_warnings}")

if total_errors == 0:
    print("\n✅ No critical SEO errors found!")
else:
    print(f"\n❌ {total_errors} critical errors need attention")

if total_warnings > 0:
    print(f"⚠️  {total_warnings} warnings should be reviewed")
