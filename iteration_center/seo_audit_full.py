"""
AIToolCrux 全站技术SEO审计（sitemap驱动版）
从 sitemap.xml 读取全部URL，10并发爬取，输出Markdown报告。
不提交GitHub，只出本地报告。
"""
import httpx
from bs4 import BeautifulSoup
import re
import sys
import time
from urllib.parse import urljoin, urlparse
from collections import defaultdict, Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import xml.etree.ElementTree as ET

BASE = "https://www.aitoolcrux.com"
SITEMAP = f"{BASE}/sitemap.xml"
UA = "Mozilla/5.0 (compatible; AIToolCrux-Audit/1.0)"
TIMEOUT = 20
WORKERS = 10
PER_REQUEST_DELAY = 0.1  # 每个请求后sleep
OUT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\seo_audit_full_20260917.md"

client = httpx.Client(http2=True, timeout=TIMEOUT, follow_redirects=True,
                       headers={"User-Agent": UA})

def fetch_urls_from_sitemap():
    """从sitemap.xml读所有URL"""
    print(f"[1/4] 读取sitemap: {SITEMAP}")
    r = client.get(SITEMAP)
    r.raise_for_status()
    root = ET.fromstring(r.text)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [loc.text.strip() for loc in root.findall(".//sm:url/sm:loc", ns)]
    # 也兼容无命名空间
    if not urls:
        urls = [loc.text.strip() for loc in root.iter("loc")]
    urls = [u for u in urls if u.startswith("http")]
    print(f"      共 {len(urls)} 个URL")
    return urls

def check_page(url):
    """检查单个页面，返回结果dict"""
    res = {
        "url": url, "status": None, "title": None, "title_len": 0,
        "meta": None, "meta_len": 0, "h1_count": 0,
        "canonical": None, "has_og": False, "has_schema": False,
        "size_kb": 0, "imgs": 0, "imgs_no_alt": 0,
        "img_urls": [], "ext_links": [], "issues": [],
    }
    try:
        time.sleep(PER_REQUEST_DELAY)
        r = client.get(url)
        res["status"] = r.status_code
        res["size_kb"] = round(len(r.content) / 1024, 1)

        if r.status_code != 200:
            res["issues"].append(("P0", f"HTTP {r.status_code}"))
            return res

        soup = BeautifulSoup(r.text, "lxml")

        # Title
        t = soup.find("title")
        if t:
            res["title"] = t.text.strip()
            res["title_len"] = len(res["title"])
            if res["title_len"] < 30:
                res["issues"].append(("P1", f"Title过短 {res['title_len']}字符"))
            elif res["title_len"] > 60:
                res["issues"].append(("P1", f"Title过长 {res['title_len']}字符"))
        else:
            res["issues"].append(("P1", "缺Title"))

        # Meta Description
        m = soup.find("meta", attrs={"name": "description"})
        if m and m.get("content"):
            res["meta"] = m["content"].strip()
            res["meta_len"] = len(res["meta"])
            if res["meta_len"] < 50:
                res["issues"].append(("P1", f"Meta Description过短 {res['meta_len']}字符"))
            elif res["meta_len"] > 160:
                res["issues"].append(("P1", f"Meta Description过长 {res['meta_len']}字符"))
        else:
            res["issues"].append(("P1", "缺Meta Description"))

        # H1
        h1s = soup.find_all("h1")
        res["h1_count"] = len(h1s)
        if res["h1_count"] == 0:
            res["issues"].append(("P1", "缺H1"))
        elif res["h1_count"] > 1:
            res["issues"].append(("P1", f"{res['h1_count']}个H1（应=1）"))

        # Canonical
        c = soup.find("link", attrs={"rel": "canonical"})
        res["canonical"] = c.get("href") if c else None
        if not res["canonical"]:
            res["issues"].append(("P1", "缺Canonical"))

        # OG
        res["has_og"] = soup.find("meta", attrs={"property": "og:title"}) is not None
        if not res["has_og"]:
            res["issues"].append(("P2", "缺Open Graph"))

        # JSON-LD
        res["has_schema"] = len(soup.find_all("script", attrs={"type": "application/ld+json"})) > 0
        if not res["has_schema"]:
            res["issues"].append(("P1", "缺JSON-LD结构化数据"))

        # 图片alt
        imgs = soup.find_all("img")
        res["imgs"] = len(imgs)
        res["imgs_no_alt"] = sum(1 for i in imgs if not i.get("alt"))
        if res["imgs"] > 0 and res["imgs_no_alt"] / res["imgs"] > 0.3:
            res["issues"].append(("P2", f"{res['imgs_no_alt']}/{res['imgs']}图缺alt"))

        # 页面大小
        if res["size_kb"] > 500:
            res["issues"].append(("P1", f"页面{res['size_kb']}KB >500KB"))

        # 收集图片URL（用于大图检测）
        for i in imgs[:15]:  # 限制每页最多15张
            src = i.get("src") or i.get("data-src")
            if src:
                res["img_urls"].append(urljoin(url, src))

        # 收集外链（前20个）
        for a in soup.find_all("a", href=True)[:30]:
            href = a["href"]
            if href.startswith("http") and BASE not in href:
                res["ext_links"].append(href)
        res["ext_links"] = list(dict.fromkeys(res["ext_links"]))[:20]

    except Exception as e:
        res["issues"].append(("P0", f"请求失败: {str(e)[:80]}"))
    return res

def check_big_images(results):
    """检测大图：页面引用的单张图片>200KB"""
    print("[3/4] 检测大图（>200KB）...")
    all_imgs = set()
    for r in results:
        all_imgs.update(r["img_urls"])
    print(f"      去重后图片URL: {len(all_imgs)}")

    big = []
    def head_img(u):
        try:
            time.sleep(PER_REQUEST_DELAY)
            h = client.head(u, follow_redirects=True)
            cl = h.headers.get("content-length")
            if cl and int(cl) > 200 * 1024:
                return (u, round(int(cl)/1024, 1))
        except: pass
        return None

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for res in ex.map(head_img, list(all_imgs)[:800]):  # 限制最多800个
            if res:
                big.append(res)
    print(f"      大图: {len(big)}")
    return big

def check_broken_links(results):
    """检测broken外链：每页前20个外链，非200"""
    print("[4/4] 检测broken外链...")
    # 去重所有外链
    all_ext = set()
    for r in results:
        all_ext.update(r["ext_links"])
    print(f"      去重后外链: {len(all_ext)}")

    broken = {}
    def head_link(u):
        try:
            time.sleep(PER_REQUEST_DELAY)
            h = client.head(u, follow_redirects=True)
            return (u, h.status_code)
        except Exception as e:
            return (u, f"ERR:{str(e)[:40]}")

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for u, code in ex.map(head_link, list(all_ext)[:500]):  # 限制500个
            if code != 200:
                broken[u] = code
    print(f"      broken外链: {len(broken)}")
    return broken

def build_report(results, big_imgs, broken_links):
    """生成Markdown报告"""
    print("\n生成报告...")
    # 重复title/meta
    title_counts = Counter(r["title"] for r in results if r["title"])
    dup_titles = {t: c for t, c in title_counts.items() if c > 1}
    meta_counts = Counter(r["meta"] for r in results if r["meta"])
    dup_metas = {m: c for m, c in meta_counts.items() if c > 1}

    # 按严重程度分组问题
    p0, p1, p2 = [], [], []
    issue_counter = Counter()
    for r in results:
        for sev, msg in r["issues"]:
            issue_counter[msg] += 1
            entry = f"{r['url']} — {msg}"
            if sev == "P0": p0.append(entry)
            elif sev == "P1": p1.append(entry)
            else: p2.append(entry)

    # 重复title的URL
    for t, c in dup_titles.items():
        urls = [r["url"] for r in results if r["title"] == t]
        p1.append(f"重复Title（{c}页）: \"{t[:70]}\" — " + ", ".join(urls[:5]))
    for m, c in dup_metas.items():
        urls = [r["url"] for r in results if r["meta"] == m]
        p2.append(f"重复Meta Description（{c}页）: \"{m[:70]}\" — " + ", ".join(urls[:5]))

    total = len(results)
    with_issue = sum(1 for r in results if r["issues"])
    total_issues = len(p0) + len(p1) + len(p2)

    lines = []
    lines.append("# AIToolCrux 全站技术SEO审计报告")
    lines.append(f"\n**生成时间**: 2026-09-17  ")
    lines.append(f"**审计工具**: sitemap驱动版（httpx + BeautifulSoup，10并发）  ")
    lines.append(f"**数据源**: {SITEMAP}\n")
    lines.append("## 汇总\n")
    lines.append(f"| 指标 | 数值 |")
    lines.append(f"|---|---|")
    lines.append(f"| 总URL数 | {total} |")
    lines.append(f"| 有问题的页面 | {with_issue} |")
    lines.append(f"| 总问题数（含重复title/meta/大图/broken link） | {total_issues + len(big_imgs) + len(broken_links)} |")
    lines.append(f"| P0（影响索引） | {len(p0)} |")
    lines.append(f"| P1（影响排名） | {len(p1)} |")
    lines.append(f"| P2（小问题） | {len(p2)} |")
    lines.append(f"| 大图（>200KB） | {len(big_imgs)} |")
    lines.append(f"| broken外链 | {len(broken_links)} |")
    lines.append(f"| 重复Title组 | {len(dup_titles)} |")
    lines.append(f"| 重复Meta组 | {len(dup_metas)} |")

    lines.append("\n## 问题分类计数\n")
    lines.append("| 问题 | 页面数 |")
    lines.append("|---|---|")
    for msg, c in issue_counter.most_common():
        lines.append(f"| {msg} | {c} |")

    lines.append("\n## P0：影响索引\n")
    if p0:
        for x in p0[:50]:
            lines.append(f"- {x}")
        if len(p0) > 50: lines.append(f"- ... 还有{len(p0)-50}条")
    else:
        lines.append("无 ✅")

    lines.append("\n## P1：影响排名\n")
    if p1:
        for x in p1[:100]:
            lines.append(f"- {x}")
        if len(p1) > 100: lines.append(f"- ... 还有{len(p1)-100}条")
    else:
        lines.append("无 ✅")

    lines.append("\n## P2：小问题\n")
    if p2:
        for x in p2[:80]:
            lines.append(f"- {x}")
        if len(p2) > 80: lines.append(f"- ... 还有{len(p2)-80}条")
    else:
        lines.append("无 ✅")

    lines.append("\n## 大图（>200KB）\n")
    if big_imgs:
        for u, kb in big_imgs[:30]:
            lines.append(f"- {kb}KB — {u}")
    else:
        lines.append("无 ✅")

    lines.append("\n## Broken外链（非200）\n")
    if broken_links:
        for u, code in list(broken_links.items())[:30]:
            lines.append(f"- {code} — {u}")
    else:
        lines.append("无 ✅")

    report = "\n".join(lines)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n报告已写入: {OUT}")
    return total, total_issues + len(big_imgs) + len(broken_links), len(p0), len(p1), len(p2)

def main():
    urls = fetch_urls_from_sitemap()
    if not urls:
        print("ERROR: sitemap无URL"); sys.exit(1)

    print(f"\n[2/4] 并发爬取 {len(urls)} 个页面（{WORKERS} workers）...")
    results = []
    done = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(check_page, u): u for u in urls}
        for fut in as_completed(futs):
            r = fut.result()
            results.append(r)
            done += 1
            if done % 50 == 0:
                print(f"      进度: {done}/{len(urls)}")

    big = check_big_images(results)
    broken = check_broken_links(results)
    total, total_iss, p0c, p1c, p2c = build_report(results, big, broken)
    print(f"\n=== 完成 ===")
    print(f"总页面: {total}")
    print(f"总问题: {total_iss}")
    print(f"P0={p0c} P1={p1c} P2={p2c}")
    client.close()

if __name__ == "__main__":
    main()
