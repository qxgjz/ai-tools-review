const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const OUT = "C:\\Users\\通明街\\Doubao\\chats\\2026-08-28\\new-chat\\ai-tools-review\\content_drafts\\screenshots\\n8n\\real_ui";
fs.mkdirSync(OUT, { recursive: true });

const PAGES = [
  ["https://docs.n8n.io/advanced-ai/ai-agents/build-ai-agent/", "ai-agent"],
  ["https://docs.n8n.io/advanced-ai/intro-tutorial/", "intro-tutorial"],
  ["https://docs.n8n.io/build/workflows/", "workflows"],
  ["https://docs.n8n.io/advanced-ai/ai-chains/", "ai-chains"],
];

(async () => {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
  const ctx = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
  });
  const page = await ctx.newPage();
  let idx = 0;
  for (const [url, tag] of PAGES) {
    try {
      console.log(`[*] ${url}`);
      await page.goto(url, { waitUntil: "domcontentloaded", timeout: 45000 });
      await page.waitForTimeout(4000);
      for (const sel of ["button:has-text('Accept all')", "button:has-text('Accept')", "#CybotCookiebotDialogBodyButtonAccept"]) {
        try { await page.click(sel, { timeout: 1500 }); await page.waitForTimeout(400); } catch (e) {}
      }
      // 收集页面内所有图片URL
      const imgs = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('img')).map(i => i.src).filter(s => s && s.length > 20);
      });
      console.log(`    found ${imgs.length} images`);
      for (const src of imgs.slice(0, 12)) {
        // 只看截图类大图（避免logo/图标）
        if (/logo|icon|avatar|favicon/i.test(src)) continue;
        idx++;
        const ext = src.includes('.png') ? 'png' : 'jpg';
        const fp = path.join(OUT, `${tag}_${idx}.${ext}`);
        try {
          const resp = await page.request.get(src, { timeout: 20000 });
          if (resp.ok()) {
            const buf = await resp.body();
            if (buf.length > 15000) {  // 只保留大图
              fs.writeFileSync(fp, buf);
              console.log(`    saved ${fp} (${Math.round(buf.length/1024)}KB)`);
            } else {
              console.log(`    skip small ${Math.round(buf.length/1024)}KB: ${src.slice(0,80)}`);
            }
          }
        } catch (e) {
          console.log(`    fetch fail: ${e.message.slice(0,60)}`);
        }
      }
    } catch (e) {
      console.log(`    FAIL page: ${e.message}`);
    }
  }
  await browser.close();
  console.log("done");
})();
