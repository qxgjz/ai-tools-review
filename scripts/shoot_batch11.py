# -*- coding: utf-8 -*-
"""拍摄真实工具界面截图（Playwright，headless chromium）
候选URL：优先公开的产品页/模板库/编辑器（非营销首页）
"""
import os
from playwright.sync_api import sync_playwright

OUT = 'content_drafts/screenshots/batch11'
os.makedirs(OUT, exist_ok=True)

CANDIDATES = [
    # synthesia-vs-heygen
    ('synthesia-pricing', 'https://www.synthesia.io/pricing'),
    ('synthesia-explore-avatars', 'https://www.synthesia.io/explore/avatars'),
    ('heygen-templates', 'https://www.heygen.com/templates'),
    ('heygen-pricing', 'https://www.heygen.com/pricing'),
    # motion-ai-alternatives
    ('motion-product', 'https://www.usemotion.com/product'),
    ('motion-pricing', 'https://www.usemotion.com/pricing'),
    ('reclaim-product', 'https://reclaim.ai/product'),
    ('reclaim-pricing', 'https://reclaim.ai/pricing'),
    # quillbot-alternatives
    ('quillbot-editor', 'https://quillbot.com/'),
    ('grammarly-product', 'https://www.grammarly.com/'),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={'width': 1440, 'height': 900}, user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36')
    page = ctx.new_page()
    for name, url in CANDIDATES:
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=30000)
            page.wait_for_timeout(4000)
            # 尝试关闭cookie弹窗
            for sel in ['button:has-text("Accept all")', 'button:has-text("Accept")', 'button:has-text("I agree")', '[aria-label="Close"]']:
                try:
                    if page.locator(sel).count() > 0:
                        page.locator(sel).first.click(timeout=1500)
                        page.wait_for_timeout(800)
                except Exception:
                    pass
            page.screenshot(path=os.path.join(OUT, name + '.png'), full_page=False)
            print('OK', name, url)
        except Exception as e:
            print('FAIL', name, url, str(e)[:120])
    browser.close()
