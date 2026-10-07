"""
截图机器人 - Playwright批量截图
调用: python scripts/seo_toolkit/screenshot_bot.py --url https://chat.openai.com --tool chatgpt
输出: public/screenshots/{tool}/ 下3张WebP截图

整合工具:
- Playwright (浏览器自动化)
- Python PIL (图片优化)
"""
import sys, os, argparse, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import *

def take_screenshots(url, tool_name, pages=None):
    """批量截图：首页/仪表盘、核心功能、定价页"""
    from playwright.sync_api import sync_playwright
    if pages is None:
        pages = [
            {"name": "homepage", "url": url, "wait": 3000},
            {"name": "pricing", "url": url.rstrip("/") + "/pricing", "wait": 3000},
            {"name": "features", "url": url.rstrip("/") + "/features", "wait": 3000},
        ]

    output_dir = os.path.join(SCREENSHOTS_DIR, tool_name)
    os.makedirs(output_dir, exist_ok=True)
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = context.new_page()

        for pg in pages:
            try:
                print(f"  截图: {pg['name']} -> {pg['url']}")
                page.goto(pg["url"], wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(pg["wait"])
                # 关闭可能的弹窗
                try:
                    page.click("button:has-text('Accept')", timeout=2000)
                except:
                    pass
                try:
                    page.click("button:has-text('Got it')", timeout=2000)
                except:
                    pass
                # 截图
                filepath = os.path.join(output_dir, f"{pg['name']}.webp")
                page.screenshot(path=filepath, full_page=False, type="webp", quality=80)
                size = os.path.getsize(filepath)
                results.append({"name": pg["name"], "path": filepath, "size": size, "ok": size < 300000})
                print(f"    ✅ {filepath} ({size//1024}KB)")
            except Exception as e:
                print(f"    ❌ {pg['name']} 失败: {e}")
                results.append({"name": pg["name"], "path": "", "size": 0, "ok": False, "error": str(e)})

        browser.close()
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="工具官网URL")
    parser.add_argument("--tool", required=True, help="工具名（用于目录名）")
    parser.add_argument("--pages", nargs="+", help="自定义页面URL列表")
    args = parser.parse_args()

    print(f"=== 截图机器人 ===")
    print(f"工具: {args.tool}")
    print(f"URL: {args.url}")

    pages = None
    if args.pages:
        pages = [{"name": f"page_{i}", "url": u, "wait": 3000} for i, u in enumerate(args.pages)]

    results = take_screenshots(args.url, args.tool, pages)
    ok_count = sum(1 for r in results if r["ok"])
    print(f"\n=== 完成 ===")
    print(f"成功: {ok_count}/{len(results)}")
    print(f"输出目录: {os.path.join(SCREENSHOTS_DIR, args.tool)}")
    if ok_count < 2:
        print("⚠️  成功截图不足2张，可能需要手动补充")
        sys.exit(1)

if __name__ == "__main__":
    main()
