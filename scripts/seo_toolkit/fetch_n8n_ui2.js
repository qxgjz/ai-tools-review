const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const OUT = "C:\\Users\\通明街\\Doubao\\chats\\2026-08-28\\new-chat\\ai-tools-review\\content_drafts\\screenshots\\n8n\\real_ui";
fs.mkdirSync(OUT, { recursive: true });

// 文档页正文内含真实编辑器截图，逐段滚动整页截图
const PAGES = [
  ["https://docs.n8n.io/advanced-ai/ai-agents/", "ai-agents-overview"],
  ["https://docs.n8n.io/build/workflows/", "workflows-overview"],
  ["https://docs.n8n.io/advanced-ai/intro-tutorial/", "intro-tutorial"],
  ["https://n8n.io/workflows/1958-custom-gpt-actions-in-n8n-with-your-own-schema/", "template-gpt"],
];

(async () => {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
  const ctx = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
  });
  const page = await ctx.newPage();
  for (const [url, tag] of PAGES) {
    try {
      console.log(`[*] ${tag} -> ${url}`);
      await page.goto(url, { waitUntil: "domcontentloaded", timeout: 45000 });
      await page.waitForTimeout(4500);
      for (const sel of ["button:has-text('Accept all')", "button:has-text('Accept')", "#CybotCookiebotDialogBodyButtonAccept"]) {
        try { await page.click(sel, { timeout: 1500 }); await page.waitForTimeout(400); } catch (e) {}
      }
      // 获取正文区域的图片和文档主体
      const info = await page.evaluate(() => {
        const main = document.querySelector('main, article, .doc-content, [class*="content"]');
        const imgs = Array.from(document.querySelectorAll('main img, article img, .doc-content img, [class*="content"] img'))
          .map(i => ({ src: i.src, w: i.naturalWidth, h: i.naturalHeight }))
          .filter(i => i.w >= 400 && i.h >= 200);
        return { imgs, bodyText: (main ? main.innerText : document.body.innerText).slice(0, 200) };
      });
      console.log(`    content imgs: ${info.imgs.length}; body: ${info.bodyText.replace(/\n/g,' ').slice(0,100)}`);
      // 下载正文内嵌大图
      let n = 0;
      for (const img of info.imgs.slice(0, 8)) {
        n++;
        const ext = img.src.includes('.png') ? 'png' : (img.src.includes('.webp') ? 'webp' : 'jpg');
        const fp = path.join(OUT, `${tag}_content_${n}.${ext}`);
        try {
          const resp = await page.request.get(img.src, { timeout: 20000 });
          if (resp.ok()) {
            const buf = await resp.body();
            if (buf.length > 20000) { fs.writeFileSync(fp, buf); console.log(`    saved ${path.basename(fp)} (${Math.round(buf.length/1024)}KB) ${img.w}x${img.h}`); }
            else console.log(`    skip small ${Math.round(buf.length/1024)}KB`);
          }
        } catch (e) { console.log(`    fetch fail: ${e.message.slice(0,50)}`); }
      }
      // 整页截图（滚动到正文中部）
      await page.evaluate(() => window.scrollTo(0, 500));
      await page.waitForTimeout(1000);
      const fp2 = path.join(OUT, `${tag}_page.png`);
      await page.screenshot({ path: fp2, fullPage: false, type: "png" });
      console.log(`    page shot OK (${Math.round(fs.statSync(fp2).size/1024)}KB)`);
    } catch (e) {
      console.log(`    FAIL ${tag}: ${e.message}`);
    }
  }
  await browser.close();
  console.log("done");
})();
