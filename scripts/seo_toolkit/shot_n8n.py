"""n8n真实界面截图 - Playwright访问n8n产品页面"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright

OUT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\screenshots\n8n"
os.makedirs(OUT, exist_ok=True)

URLS = [
    ("n8n-home", "https://n8n.io/", 4000),
    ("n8n-ai-page", "https://n8n.io/ai/", 4000),
    ("n8n-docs-ai-agents", "https://docs.n8n.io/advanced-ai/ai-agents/", 4000),
    ("n8n-pricing", "https://n8n.io/pricing/", 4000),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1440, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")
    page = ctx.new_page()
    for name, url, wait in URLS:
        try:
            print(f"[*] {name} -> {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(wait)
            for sel in ["button:has-text('Accept all')", "button:has-text('Accept')", "#CybotCookiebotDialogBodyButtonAccept"]:
                try:
                    page.click(sel, timeout=1500); page.wait_for_timeout(500)
                except Exception:
                    pass
            # 滚动获取更多内容
            for _ in range(2):
                page.mouse.wheel(0, 800)
                page.wait_for_timeout(600)
            fp = os.path.join(OUT, f"{name}.png")
            page.screenshot(path=fp, full_page=False, type="png")
            print(f"    OK {fp} ({os.path.getsize(fp)//1024}KB)")
        except Exception as e:
            print(f"    FAIL {name}: {e}")
    browser.close()
print("done")
