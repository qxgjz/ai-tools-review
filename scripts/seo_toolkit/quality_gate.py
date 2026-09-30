"""
质量门检查 - 15项逐项检查
调用: python scripts/seo_toolkit/quality_gate.py --slug {文章slug}
输出: 检查结果，不达标项列出具体问题

整合工具:
- Python JSON解析
- 正则检查
- zens-ink content_qc (如果可用)
"""
import sys, os, json, argparse, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import *

def load_post(slug):
    with open(POSTS_JSON, "r", encoding="utf-8") as f:
        posts = json.load(f)
    for p in posts:
        if p.get("slug") == slug:
            return p
    return None

def check_post(post):
    """15项质量门检查"""
    results = []
    content = post.get("content", "") or ""
    title = post.get("title", "") or ""

    # 1. 字数
    word_count = len(content.split())
    results.append({
        "id": 1, "name": "字数2500-4000",
        "pass": QUALITY_STANDARDS["min_words"] <= word_count <= QUALITY_STANDARDS["max_words"],
        "value": word_count,
        "fix": f"当前{word_count}词，需{'扩写' if word_count < 2500 else '精简'}到2500-4000"
    })

    # 2. Quick Answer长度
    qa = post.get("quickAnswer", "") or ""
    results.append({
        "id": 2, "name": "Quick Answer 280-320字符",
        "pass": QUALITY_STANDARDS["quick_answer_min"] <= len(qa) <= QUALITY_STANDARDS["quick_answer_max"],
        "value": len(qa),
        "fix": f"当前{len(qa)}字符，需调整到280-320"
    })

    # 3. Key Takeaways数量
    kt = post.get("keyTakeaways", []) or []
    results.append({
        "id": 3, "name": "Key Takeaways≥3",
        "pass": len(kt) >= QUALITY_STANDARDS["min_key_takeaways"],
        "value": len(kt),
        "fix": f"当前{len(kt)}条，需补充到≥3条"
    })

    # 4. 有对比表
    has_table = "<table" in content or bool(re.search(r'\|.+\|.+\|', content))
    results.append({
        "id": 4, "name": "有对比表/数据表格",
        "pass": has_table,
        "value": "有" if has_table else "无",
        "fix": "添加对比表格（价格/功能/评分等）"
    })

    # 5. 有分场景推荐
    has_scenario = any(p in content.lower() for p in ["for students", "for beginners", "for developers", "for small business", "best for", "who should use"])
    results.append({
        "id": 5, "name": "有分场景推荐",
        "pass": has_scenario,
        "value": "有" if has_scenario else "无",
        "fix": "添加'Who Should Use What'分场景推荐章节"
    })

    # 6. 有Who Should Look Elsewhere
    has_elsewhere = any(p in content.lower() for p in ["look elsewhere", "who should not", "avoid if", "not for"])
    results.append({
        "id": 6, "name": "有Who Should Look Elsewhere",
        "pass": has_elsewhere,
        "value": "有" if has_elsewhere else "无",
        "fix": "添加'Who Should Look Elsewhere'诚实说明谁不该用"
    })

    # 7. 有How We Tested
    has_tested = any(p in content.lower() for p in ["how we tested", "how we evaluate", "our testing", "methodology"])
    results.append({
        "id": 7, "name": "有How We Tested",
        "pass": has_tested,
        "value": "有" if has_tested else "无",
        "fix": "添加'How We Tested'章节，含测试时长/设备/具体数字"
    })

    # 8. FAQ数量
    faq_count = len(re.findall(r'faq|question|q:', content.lower())) // 2
    faq_count = max(faq_count, content.count("?") // 8)
    results.append({
        "id": 8, "name": "FAQ≥5个",
        "pass": faq_count >= QUALITY_STANDARDS["min_faq"],
        "value": faq_count,
        "fix": f"当前约{faq_count}个FAQ，需补充到≥5个（用PAA问题）"
    })

    # 9. 定价有真实计算
    has_pricing_calc = bool(re.search(r'\$\d+', content)) and any(p in content.lower() for p in ["month", "year", "per month", "annual"])
    results.append({
        "id": 9, "name": "定价有真实成本计算",
        "pass": has_pricing_calc,
        "value": "有" if has_pricing_calc else "无",
        "fix": "添加具体价格和年成本计算（月费×12）"
    })

    # 10. 诚实说缺点
    has_cons = any(p in content.lower() for p in ["cons", "disadvantage", "downside", "drawback", "weakness", "limitation"])
    results.append({
        "id": 10, "name": "诚实说缺点",
        "pass": has_cons,
        "value": "有" if has_cons else "无",
        "fix": "每个推荐工具至少列2个缺点"
    })

    # 11. Last updated
    has_updated = "last updated" in content.lower() or "updated:" in content.lower()
    results.append({
        "id": 11, "name": "有Last updated",
        "pass": has_updated,
        "value": "有" if has_updated else "无",
        "fix": "末尾添加'Last updated: September 2026'"
    })

    # 12. 内链数量
    il = post.get("internalLinks", []) or []
    il_in_content = len(re.findall(r'href="/[^"]+"', content))
    total_il = max(len(il), il_in_content)
    results.append({
        "id": 12, "name": "内链≥3个",
        "pass": total_il >= QUALITY_STANDARDS["min_internal_links"],
        "value": total_il,
        "fix": f"当前{total_il}个内链，需补充到≥3个（用Python搜posts.json找相关文章）"
    })

    # 13. 联盟链接
    al = post.get("affiliateLinks", []) or []
    al_in_content = content.count('rel="sponsored"') + content.count("affiliate")
    total_al = max(len(al), al_in_content)
    results.append({
        "id": 13, "name": "联盟链接≥2处",
        "pass": total_al >= QUALITY_STANDARDS["min_affiliate_links"],
        "value": total_al,
        "fix": f"当前{total_al}处联盟链接，需在对比表+Final Verdict各放1个"
    })

    # 14. 真实截图
    has_screenshots = post.get("hasRealScreenshots", False) or len(re.findall(r'screenshots/[^"]+\.(webp|png|jpg)', content)) >= 3
    results.append({
        "id": 14, "name": "真实截图≥3张",
        "pass": has_screenshots,
        "value": "有" if has_screenshots else "无",
        "fix": "用Playwright截3张真实工具界面图（仪表盘/核心功能/定价页）"
    })

    # 15. 100%英文
    has_chinese = bool(re.search(r'[\u4e00-\u9fff]', content + title + qa))
    results.append({
        "id": 15, "name": "100%英文（无中文）",
        "pass": not has_chinese,
        "value": "纯英文" if not has_chinese else "含中文",
        "fix": "移除所有中文字符"
    })

    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", required=True, help="文章slug")
    parser.add_argument("--fix", action="store_true", help="自动修复可修复项")
    args = parser.parse_args()

    print(f"=== 质量门检查 ===")
    print(f"文章: {args.slug}")

    post = load_post(args.slug)
    if not post:
        print(f"[ERROR] 未找到文章: {args.slug}")
        sys.exit(1)

    print(f"标题: {post.get('title','')}")
    print(f"字数: {len(post.get('content','').split())}")

    results = check_post(post)
    passed = sum(1 for r in results if r["pass"])
    failed = [r for r in results if not r["pass"]]

    print(f"\n{'='*50}")
    print(f"检查结果: {passed}/15 通过")
    print(f"{'='*50}\n")

    for r in results:
        status = "✅" if r["pass"] else "❌"
        print(f"{status} [{r['id']:2d}] {r['name']}: {r['value']}")
        if not r["pass"]:
            print(f"   → 修复: {r['fix']}")

    if failed:
        print(f"\n❌ 未通过 {len(failed)} 项，不允许提交")
        print(f"需修复项: {', '.join(str(r['id']) for r in failed)}")
        sys.exit(1)
    else:
        print(f"\n✅ 全部15项通过，可以提交发布")
        sys.exit(0)

if __name__ == "__main__":
    main()
