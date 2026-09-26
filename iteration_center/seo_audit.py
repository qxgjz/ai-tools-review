"""
AIToolCrux 全站技术SEO审计脚本
替代Screaming Frog，用Python爬取关键页面并检查SEO问题
"""
import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urljoin, urlparse
from collections import defaultdict

BASE_URL = "https://www.aitoolcrux.com"
TIMEOUT = 15

# 要审计的关键页面列表
PAGES_TO_CHECK = [
    "/",
    "/compare",
    "/category/agent",
    "/category/code",
    "/category/writing",
    "/blog/openai_astra_review",
    "/blog/stable-diffusion-review-2026",
    "/blog/dify_ai_review",
    "/blog/cursor_ai_review",
    "/blog/gemini_38_flash_review",
    "/blog/suno-review-2026",
    "/blog/midjourney-v7-review-2026-is-it-still-the-best-ai-image-generator-md",
]

def check_page(path):
    """检查单个页面的SEO元素"""
    url = urljoin(BASE_URL, path)
    result = {
        "url": url,
        "path": path,
        "status": None,
        "title": None,
        "title_length": 0,
        "meta_desc": None,
        "meta_desc_length": 0,
        "h1": [],
        "h2_count": 0,
        "canonical": None,
        "has_og": False,
        "has_schema": False,
        "page_size_kb": 0,
        "issues": [],
    }
    
    try:
        resp = requests.get(url, timeout=TIMEOUT, headers={
            "User-Agent": "Mozilla/5.0 (compatible; SEO-Audit/1.0)"
        })
        result["status"] = resp.status_code
        result["page_size_kb"] = round(len(resp.content) / 1024, 1)
        
        if resp.status_code != 200:
            result["issues"].append(f"HTTP {resp.status_code}")
            return result
        
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Title
        title_tag = soup.find("title")
        if title_tag:
            result["title"] = title_tag.text.strip()
            result["title_length"] = len(result["title"])
            if result["title_length"] < 30:
                result["issues"].append("Title太短 (<30字符)")
            elif result["title_length"] > 60:
                result["issues"].append("Title太长 (>60字符)")
        else:
            result["issues"].append("缺少Title标签")
        
        # Meta Description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            result["meta_desc"] = meta_desc["content"].strip()
            result["meta_desc_length"] = len(result["meta_desc"])
            if result["meta_desc_length"] < 50:
                result["issues"].append("Meta Description太短 (<50字符)")
            elif result["meta_desc_length"] > 160:
                result["issues"].append("Meta Description太长 (>160字符)")
        else:
            result["issues"].append("缺少Meta Description")
        
        # H1标签
        h1_tags = soup.find_all("h1")
        result["h1"] = [h.text.strip() for h in h1_tags]
        if len(h1_tags) == 0:
            result["issues"].append("缺少H1标签")
        elif len(h1_tags) > 1:
            result["issues"].append(f"有{len(h1_tags)}个H1标签（应该只有1个）")
        
        # H2数量
        result["h2_count"] = len(soup.find_all("h2"))
        
        # Canonical
        canonical = soup.find("link", attrs={"rel": "canonical"})
        if canonical:
            result["canonical"] = canonical.get("href")
        else:
            result["issues"].append("缺少Canonical标签")
        
        # Open Graph
        og_title = soup.find("meta", attrs={"property": "og:title"})
        result["has_og"] = og_title is not None
        if not result["has_og"]:
            result["issues"].append("缺少Open Graph标签")
        
        # 结构化数据
        scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
        result["has_schema"] = len(scripts) > 0
        if not result["has_schema"]:
            result["issues"].append("缺少JSON-LD结构化数据")
        
        # 图片alt检查（抽样）
        imgs = soup.find_all("img")
        no_alt = sum(1 for img in imgs if not img.get("alt"))
        if len(imgs) > 0 and no_alt / len(imgs) > 0.3:
            result["issues"].append(f"{no_alt}/{len(imgs)}张图片缺少alt标签")
        
    except Exception as e:
        result["issues"].append(f"请求失败: {str(e)[:100]}")
    
    return result


def main():
    print("=== AIToolCrux 技术SEO审计 ===")
    print(f"共检查 {len(PAGES_TO_CHECK)} 个关键页面\n")
    
    results = []
    for path in PAGES_TO_CHECK:
        print(f"检查: {path}")
        result = check_page(path)
        results.append(result)
    
    # 统计问题
    all_issues = defaultdict(list)
    for r in results:
        for issue in r["issues"]:
            all_issues[issue].append(r["path"])
    
    # 输出报告
    print("\n" + "="*60)
    print("=== 审计结果汇总 ===")
    print("="*60)
    
    # 问题统计
    print(f"\n总页面数: {len(results)}")
    print(f"有问题的页面数: {sum(1 for r in results if r['issues'])}")
    print(f"总问题数: {sum(len(r['issues']) for r in results)}")
    
    # 问题分类统计
    print("\n--- 问题分类统计 ---")
    for issue, pages in sorted(all_issues.items(), key=lambda x: -len(x[1])):
        print(f"  {issue}: {len(pages)}个页面")
    
    # 详细页面报告
    print("\n--- 详细页面报告 ---")
    for r in results:
        status_icon = "✅" if not r["issues"] else "⚠️"
        print(f"\n{status_icon} {r['path']}")
        print(f"   状态: {r['status']} | 大小: {r['page_size_kb']}KB")
        if r["title"]:
            print(f"   Title: {r['title'][:60]}... ({r['title_length']}字符)")
        if r["meta_desc"]:
            print(f"   Meta: {r['meta_desc'][:60]}... ({r['meta_desc_length']}字符)")
        print(f"   H1: {len(r['h1'])}个 | H2: {r['h2_count']}个")
        if r["issues"]:
            print(f"   问题:")
            for issue in r["issues"]:
                print(f"     - {issue}")
    
    # 保存JSON结果
    output_path = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\seo_audit_result.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n结果已保存到: {output_path}")
    return results


if __name__ == "__main__":
    main()
