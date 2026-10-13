const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const OUT = "C:\\Users\\通明街\\Doubao\\chats\\2026-08-28\\new-chat\\ai-tools-review\\content_drafts\\screenshots\\n8n";
fs.mkdirSync(OUT, { recursive: true });

const URLS = [
  ["n8n-home", "https://n8n.io/", 4000],
  ["n8n-ai-page", "https://n8n.io/ai/", 4000],
  ["n8n-docs-ai-agents", "https://docs.n8n.io/advanced-ai/ai-agents/", 4000],
  ["n8n-pricing", "https://n8n.io/pricing/", 4000],
];

(async () => {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
  const ctx = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
  });
  const page = await ctx.newPage();
  for (const [name, url, wait] of URLS) {
    try {
      console.log(`[*] ${name} -> ${url}`);
      await page.goto(url, { waitUntil: "domcontentloaded", timeout: 45000 });
      await page.waitForTimeout(wait);
      for (const sel of ["button:has-text('Accept all')", "button:has-text('Accept')", "#CybotCookiebotDialogBodyButtonAccept"]) {
        try { await page.click(sel, { timeout: 1500 }); await page.waitForTimeout(500); } catch (e) {}
      }
      for (let i = 0; i < 2; i++) { await page.mouse.wheel(0, 800); await page.waitForTimeout(600); }
      const fp = path.join(OUT, `${name}.png`);
      await page.screenshot({ path: fp, fullPage: false, type: "png" });
      console.log(`    OK ${fp} (${Math.round(fs.statSync(fp).size / 1024)}KB)`);
    } catch (e) {
      console.log(`    FAIL ${name}: ${e.message}`);
    }
  }
  await browser.close();
  console.log("done");
})();
