# -*- coding: utf-8 -*-
"""补拍 quillbot 文章替代工具真实界面（非营销首页）"""
import os
from playwright.sync_api import sync_playwright

OUT = 'content_drafts/screenshots/batch11'
os.makedirs(OUT, exist_ok=True)

CANDIDATES = [
    ('wordtune-product', 'https://www.wordtune.com/product'),
    ('wordtune-pricing', 'https://www.wordtune.com/pricing'),
    ('paraphraser-io', 'https://www.paraphraser.io/'),
    ('undetectable-ai', 'https://undetectable.ai/'),
    ('quillbot-paraphraser', 'https://quillbot.com/paraphrasing-tool'),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={'width': 1440, 'height': 900}, user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36')
    page = ctx.new_page()
    for name, url in CANDIDATES:
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=30000)
            page.wait_for_timeout(5000)
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
