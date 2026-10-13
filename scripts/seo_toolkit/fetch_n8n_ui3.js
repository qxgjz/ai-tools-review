const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const OUT = "C:\\Users\\通明街\\Doubao\\chats\\2026-08-28\\new-chat\\ai-tools-review\\content_drafts\\screenshots\\n8n\\real_ui";
fs.mkdirSync(OUT, { recursive: true });

const TASKS = [
  // GitHub README 真实编辑器截图（截图直接来自产品）
  { name: "github-readme", url: "https://github.com/n8n-io/n8n", type: "github" },
  // n8n官网workflows有效模板
  { name: "template-list", url: "https://n8n.io/workflows/", type: "list" },
  // docs 教程（滚动截整页）
  { name: "docs-ai-agents", url: "https://docs.n8n.io/advanced-ai/ai-agents/", type: "docs" },
  { name: "docs-build-first", url: "https://docs.n8n.io/advanced-ai/intro-tutorial/", type: "docs" },
];

(async () => {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
  const ctx = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
  });
  const page = await ctx.newPage();
  for (const t of TASKS) {
    try {
      console.log(`[*] ${t.name} -> ${t.url}`);
      await page.goto(t.url, { waitUntil: "domcontentloaded", timeout: 45000 });
      await page.waitForTimeout(5000);
      for (const sel of ["button:has-text('Accept all')", "button:has-text('Accept')", "#CybotCookiebotDialogBodyButtonAccept"]) {
        try { await page.click(sel, { timeout: 1500 }); await page.waitForTimeout(400); } catch (e) {}
      }
      // 等待懒加载：滚动到底再回顶部
      await page.evaluate(async () => {
        const h = document.body.scrollHeight;
        for (let y = 0; y < h; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 250)); }
        window.scrollTo(0, 0);
      });
      await page.waitForTimeout(1500);

      if (t.type === "github") {
        // 下载 README 中较大的产品截图
        const imgs = await page.evaluate(() => Array.from(document.querySelectorAll('article img'))
          .map(i => ({ src: i.src, w: i.naturalWidth, h: i.naturalHeight }))
          .filter(i => i.w >= 300 && i.h >= 150));
        console.log(`    github imgs: ${imgs.length}`);
        let n = 0;
        for (const img of imgs.slice(0, 10)) {
          n++;
          const ext = img.src.includes('.png') ? 'png' : (img.src.includes('.webp') ? 'webp' : 'jpg');
          const fp = path.join(OUT, `github_${n}.${ext}`);
          try {
            const resp = await page.request.get(img.src, { timeout: 25000 });
            if (resp.ok()) {
              const buf = await resp.body();
              if (buf.length > 25000) { fs.writeFileSync(fp, buf); console.log(`    saved ${path.basename(fp)} (${Math.round(buf.length/1024)}KB)`); }
              else console.log(`    skip ${Math.round(buf.length/1024)}KB`);
            }
          } catch (e) { console.log(`    fail ${e.message.slice(0,50)}`); }
        }
      } else if (t.type === "docs") {
        // 截取正文区域
        const shots = await page.evaluate(() => {
          const el = document.querySelector('main, article, .doc-content, [class*="content"]');
          const r = el ? el.getBoundingClientRect() : null;
          return r ? { x: r.x, y: r.y, w: r.width, h: r.height } : null;
        });
        // 全页截图（长图）
        const fp = path.join(OUT, `${t.name}_full.png`);
        await page.screenshot({ path: fp, fullPage: true, type: "png" });
        console.log(`    full page OK (${Math.round(fs.statSync(fp).size/1024)}KB)`);
      } else {
        const fp = path.join(OUT, `${t.name}_full.png`);
        await page.screenshot({ path: fp, fullPage: true, type: "png" });
        console.log(`    full page OK (${Math.round(fs.statSync(fp).size/1024)}KB)`);
      }
    } catch (e) {
      console.log(`    FAIL ${t.name}: ${e.message}`);
    }
  }
  await browser.close();
  console.log("done");
})();
