"""
断链审计脚本（云端执行）
扫描网站所有页面的外链，检测404/500/超时
输出：broken_links_report.md + broken_links.json
"""
import json
import os
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.join(BASE, "iteration_center")
SITEMAP_URL = "https://aitoolcrux.com/sitemap.xml"
SITE_DOMAIN = "aitoolcrux.com"

# 忽略的域名（已知可能不稳定但不影响）
IGNORE_DOMAINS = [
    "twitter.com", "x.com",  # Twitter经常403
    "facebook.com",
    "instagram.com",
    "linkedin.com",
]

def get_all_urls_from_sitemap():
    """从sitemap获取所有页面URL"""
    try:
        r = requests.get(SITEMAP_URL, timeout=15)
        if r.status_code == 200:
            import re
            urls = re.findall(r'<loc>(.*?)</loc>', r.text)
            return urls
    except Exception as e:
        print(f"  ⚠️ Sitemap获取失败: {e}")
    return []

def extract_external_links(page_url):
    """从页面提取所有外链"""
    try:
        r = requests.get(page_url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return []
        import re
        # 提取所有href
        links = re.findall(r'href=["\'](https?://[^"\']+)["\']', r.text)
        # 过滤外链（非本站域名）
        external = [l for l in links if SITE_DOMAIN not in l]
        return list(set(external))
    except Exception as e:
        return []

def check_link(url):
    """检查单个链接状态"""
    try:
        r = requests.head(url, timeout=10, allow_redirects=True, 
                          headers={"User-Agent": "Mozilla/5.0"})
        return {"url": url, "status": r.status_code, "ok": r.status_code < 400}
    except requests.Timeout:
        return {"url": url, "status": "timeout", "ok": False}
    except requests.ConnectionError:
        return {"url": url, "status": "connection_error", "ok": False}
    except Exception as e:
        return {"url": url, "status": f"error: {str(e)[:50]}", "ok": False}

def should_ignore(url):
    """是否应该忽略该链接"""
    return any(d in url for d in IGNORE_DOMAINS)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("🔗 开始断链审计")
    
    # 1. 获取所有页面
    print("\n📄 获取页面列表...")
    page_urls = get_all_urls_from_sitemap()
    print(f"  共 {len(page_urls)} 个页面")
    
    if not page_urls:
        print("  ⚠️ 无法获取页面列表，使用默认页面")
        page_urls = ["https://aitoolcrux.com/", "https://aitoolcrux.com/blog/"]
    
    # 2. 提取所有外链
    print("\n🔍 提取外链...")
    all_external_links = set()
    page_links_map = {}
    
    for i, page_url in enumerate(page_urls[:50]):  # 先检查前50页，避免超时
        print(f"  [{i+1}/{min(len(page_urls), 50)}] {page_url[:60]}...")
        links = extract_external_links(page_url)
        page_links_map[page_url] = links
        for link in links:
            if not should_ignore(link):
                all_external_links.add(link)
    
    print(f"\n  共提取 {len(all_external_links)} 个唯一外链（已忽略社交媒体）")
    
    # 3. 并发检查链接
    print("\n⚡ 检查链接状态（并发10个）...")
    broken_links = []
    checked = 0
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_link, url): url for url in all_external_links}
        for future in as_completed(futures):
            result = future.result()
            checked += 1
            if not result["ok"]:
                broken_links.append(result)
            if checked % 20 == 0:
                print(f"  已检查 {checked}/{len(all_external_links)}，发现 {len(broken_links)} 个断链")
    
    # 4. 找出每个断链出现在哪些页面
    print("\n📊 分析断链出现位置...")
    for broken in broken_links:
        pages_with_link = []
        for page_url, links in page_links_map.items():
            if broken["url"] in links:
                pages_with_link.append(page_url)
        broken["found_in_pages"] = pages_with_link
    
    # 5. 保存结果
    output = {
        "audit_time": datetime.utcnow().isoformat() + "Z",
        "pages_checked": min(len(page_urls), 50),
        "total_external_links": len(all_external_links),
        "broken_links_count": len(broken_links),
        "broken_links": broken_links
    }
    
    json_path = os.path.join(OUTPUT_DIR, "broken_links.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    # 6. 生成Markdown报告
    md_path = os.path.join(OUTPUT_DIR, "broken_links_report.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("# 断链审计报告\n\n")
        f.write(f"审计时间: {output['audit_time']}\n\n")
        f.write(f"## 统计\n\n")
        f.write(f"| 指标 | 数值 |\n|---|---|\n")
        f.write(f"| 检查页面数 | {output['pages_checked']} |\n")
        f.write(f"| 外链总数 | {output['total_external_links']} |\n")
        f.write(f"| 断链数 | {output['broken_links_count']} |\n")
        f.write(f"| 断链率 | {output['broken_links_count']/max(output['total_external_links'],1)*100:.1f}% |\n\n")
        
        if broken_links:
            f.write(f"## 断链详情（{len(broken_links)}个）\n\n")
            f.write("| 状态 | URL | 出现页面 |\n|---|---|---|\n")
            for b in broken_links[:30]:
                pages = ", ".join([p.split("/")[-1][:30] for p in b.get("found_in_pages", [])[:3]])
                f.write(f"| {b['status']} | {b['url'][:80]} | {pages} |\n")
        else:
            f.write("✅ 未发现断链！\n")
    
    print(f"\n✅ 完成！")
    print(f"  检查页面: {output['pages_checked']}")
    print(f"  外链总数: {output['total_external_links']}")
    print(f"  断链数: {output['broken_links_count']}")
    print(f"  断链率: {output['broken_links_count']/max(output['total_external_links'],1)*100:.1f}%")
    print(f"  JSON结果: {json_path}")
    print(f"  Markdown报告: {md_path}")

if __name__ == '__main__':
    main()
