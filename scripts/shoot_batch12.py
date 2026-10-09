# -*- coding: utf-8 -*-
"""batch12 截图：runway/writesonic/otter 三篇的替代工具真实界面候选
优先拍 pricing/product/工具操作页，避开营销首页；必要时多拍候选供淘汰
"""
import os
from playwright.sync_api import sync_playwright

OUT = 'content_drafts/screenshots/batch12'
os.makedirs(OUT, exist_ok=True)

CANDIDATES = [
    # runway-alternatives 篇
    ('runway-pricing', 'https://runwayml.com/pricing'),
    ('runway-product', 'https://runwayml.com/product'),
    ('pika-pricing', 'https://pika.art/pricing'),
    ('kling-pricing', 'https://app.klingai.com/global/global-video/create?enter_from=nav_video'),
    ('luma-pricing', 'https://lumalabs.ai/dream-machine'),
    # writesonic-alternatives 篇
    ('writesonic-pricing', 'https://writesonic.com/pricing'),
    ('jasper-pricing', 'https://www.jasper.ai/pricing'),
    ('jasper-product', 'https://www.jasper.ai/product'),
    ('copyai-product', 'https://copy.ai/'),
    # otter-ai-alternatives 篇
    ('otter-pricing', 'https://otter.ai/pricing'),
    ('fireflies-pricing', 'https://fireflies.ai/pricing'),
    ('fireflies-product', 'https://fireflies.ai/product'),
    ('granola-product', 'https://www.granola.ai/'),
    ('notebooklm-product', 'https://notebooklm.google.com/'),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(
        viewport={'width': 1440, 'height': 900},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36'
    )
    page = ctx.new_page()
    for name, url in CANDIDATES:
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=35000)
            page.wait_for_timeout(6000)
            # 关 cookie 弹窗
            for sel in ['button:has-text("Accept all")', 'button:has-text("Accept")',
                        'button:has-text("I agree")', 'button:has-text("Got it")',
                        '[aria-label="Close"]', 'button:has-text("Dismiss")']:
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
