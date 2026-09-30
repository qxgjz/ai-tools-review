"""
竞品分析流水线 - 全自动
调用: python scripts/seo_toolkit/competitor_pipeline.py --keyword "best AI tools"
输出: iteration_center/competitor_templates.md + competitor_analysis/

整合工具:
- Serper API (找竞品)
- Playwright (批量抓取页面结构)
- Python requests+BS4 (解析)
"""
import sys, os, json, argparse, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import *

def find_competitors(keyword, count=5):
    """用Serper API找竞品"""
    import requests
    resp = requests.post(SERPER_API_URL,
        headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
        data=json.dumps({"q": keyword, "num": 15}), timeout=15)
    data = resp.json()
    competitors = []
    skip_domains = ["google.com", "youtube.com", "wikipedia.org", "reddit.com", "amazon.com"]
    for r in data.get("organic", []):
        url = r.get("link", "")
        domain = url.split("/")[2] if "://" in url else url.split("/")[0]
        if any(s in domain for s in skip_domains):
            continue
        competitors.append({"title": r.get("title",""), "url": url, "domain": domain,
                            "snippet": r.get("snippet","")})
        if len(competitors) >= count:
            break
    return competitors

def analyze_page_structure(url):
    """用Playwright抓取页面结构"""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1440, "height": 900})
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3000)
            # 提取结构
            structure = page.evaluate("""() => {
                const h1s = [...document.querySelectorAll('h1')].map(e => e.innerText.trim());
                const h2s = [...document.querySelectorAll('h2')].map(e => e.innerText.trim());
                const h3s = [...document.querySelectorAll('h3')].map(e => e.innerText.trim());
                const tables = [...document.querySelectorAll('table')].map(t => ({
                    rows: t.querySelectorAll('tr').length,
                    headers: [...t.querySelectorAll('th')].map(e => e.innerText.trim())
                }));
                const faqs = [...document.querySelectorAll('details, .faq, [class*="faq"]')].length;
                const ctas = [...document.querySelectorAll('a[href*="affiliate"], a[href*="ref"]')].length;
                const wordCount = document.body.innerText.split(/\\s+/).length;
                return {h1s, h2s: h2s.slice(0,15), h3s: h3s.slice(0,10), tables, faqs, ctas, wordCount};
            }""")
            structure["url"] = url
            browser.close()
            return structure
    except Exception as e:
        print(f"[WARN] Playwright failed for {url}: {e}")
        # fallback: requests+BS4
        try:
            import requests
            from bs4 import BeautifulSoup
            resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(resp.text, "html.parser")
            return {
                "url": url,
                "h1s": [h.get_text(strip=True) for h in soup.find_all("h1")],
                "h2s": [h.get_text(strip=True) for h in soup.find_all("h2")[:15]],
                "h3s": [h.get_text(strip=True) for h in soup.find_all("h3")[:10]],
                "tables": [{"rows": len(t.find_all("tr")), "headers": [th.get_text(strip=True) for th in t.find_all("th")]} for t in soup.find_all("table")],
                "faqs": len(soup.find_all(["details"], class_=lambda c: c and "faq" in c.lower())),
                "ctas": 0,
                "wordCount": len(soup.get_text().split())
            }
        except Exception as e2:
            print(f"[ERROR] BS4 fallback also failed: {e2}")
            return {"url": url, "error": str(e2)}

def extract_template(structures):
    """从多个竞品结构中提取共性模板"""
    # 统计H2出现频率
    from collections import Counter
    all_h2s = []
    for s in structures:
        all_h2s.extend(s.get("h2s", []))
    common_h2s = Counter(all_h2s).most_common(10)

    # 统计表格列
    all_headers = []
    for s in structures:
        for t in s.get("tables", []):
            all_headers.extend(t.get("headers", []))
    common_headers = Counter(all_headers).most_common(8)

    return {
        "common_h2s": common_h2s,
        "common_table_headers": common_headers,
        "avg_word_count": sum(s.get("wordCount",0) for s in structures) // max(len(structures),1),
        "avg_faqs": sum(s.get("faqs",0) for s in structures) // max(len(structures),1),
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", required=True, help="搜索词找竞品")
    parser.add_argument("--count", type=int, default=3, help="分析竞品数量")
    args = parser.parse_args()

    print(f"=== 竞品分析流水线 ===")
    print(f"搜索词: {args.keyword}")

    # Step 1: 找竞品
    print("\n[1/3] 搜索竞品...")
    competitors = find_competitors(args.keyword, args.count)
    print(f"  找到 {len(competitors)} 个竞品:")
    for c in competitors:
        print(f"    - {c['domain']}: {c['title'][:60]}")

    # Step 2: 逐个分析结构
    print("\n[2/3] 批量抓取页面结构...")
    structures = []
    for i, c in enumerate(competitors):
        print(f"  [{i+1}/{len(competitors)}] {c['domain']}...", end=" ")
        s = analyze_page_structure(c["url"])
        s["title"] = c["title"]
        s["domain"] = c["domain"]
        structures.append(s)
        print(f"H2={len(s.get('h2s',[]))} 表格={len(s.get('tables',[]))} 字数={s.get('wordCount','?')}")
        time.sleep(2)

    # Step 3: 提取模板+输出
    print("\n[3/3] 提取共性模板...")
    template = extract_template(structures)

    os.makedirs(os.path.join(ITERATION_DIR, "competitor_analysis"), exist_ok=True)
    # 保存每个竞品的详细分析
    for s in structures:
        domain = s["domain"].replace(".", "_")
        with open(os.path.join(ITERATION_DIR, "competitor_analysis", f"{domain}.json"), "w", encoding="utf-8") as f:
            json.dump(s, f, ensure_ascii=False, indent=2)

    # 输出模板
    with open(COMPETITOR_TEMPLATES, "w", encoding="utf-8") as f:
        f.write(f"# 竞品分析模板 - 搜索词: {args.keyword}\n\n")
        f.write(f"生成时间: {time.strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"## 分析的竞品\n")
        for c in competitors:
            f.write(f"- {c['domain']}: {c['url']}\n")
        f.write(f"\n## 共性数据\n")
        f.write(f"- 平均字数: {template['avg_word_count']}\n")
        f.write(f"- 平均FAQ数: {template['avg_faqs']}\n")
        f.write(f"\n## 高频H2标题\n")
        for h2, count in template["common_h2s"]:
            f.write(f"- [{count}次] {h2}\n")
        f.write(f"\n## 高频对比表列名\n")
        for h, count in template["common_table_headers"]:
            f.write(f"- [{count}次] {h}\n")
        f.write(f"\n## 推荐文章结构（综合竞品）\n")
        f.write("1. H1: {关键词} 2026: {明确价值主张}\n")
        f.write("2. Quick Answer（280-320字符直接给结论）\n")
        f.write("3. Key Takeaways（3-5条）\n")
        f.write("4. 对比表（含高频列名）\n")
        for h2, _ in template["common_h2s"][:8]:
            f.write(f"5. {h2}\n")
        f.write(f"6. FAQ（{template['avg_faqs']}个，来自PAA）\n")
        f.write("7. Final Verdict + 联盟链接\n")

    print(f"\n=== 完成 ===")
    print(f"分析竞品: {len(structures)} 个")
    print(f"平均字数: {template['avg_word_count']}")
    print(f"输出: {COMPETITOR_TEMPLATES}")
    print(f"详细数据: iteration_center/competitor_analysis/")

if __name__ == "__main__":
    main()
