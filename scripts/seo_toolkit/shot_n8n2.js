const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const OUT = "C:\\Users\\通明街\\Doubao\\chats\\2026-08-28\\new-chat\\ai-tools-review\\content_drafts\\screenshots\\n8n";
fs.mkdirSync(OUT, { recursive: true });

// 优先真实产品界面：docs教程页(内嵌真实编辑器截图)、templates库(真实工作流画布)
const URLS = [
  ["n8n-editor-tutorial", "https://docs.n8n.io/advanced-ai/intro-tutorial/", 5000],
  ["n8n-workflow-template", "https://n8n.io/workflows/", 5000],
  ["n8n-ai-agent-docs", "https://docs.n8n.io/advanced-ai/ai-agents/build-ai-agent/", 5000],
  ["n8n-build-first-workflow", "https://docs.n8n.io/advanced-ai/intro-tutorial/", 4000],
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
      for (const sel of ["button:has-text('Accept all')", "button:has-text('Accept')", "#CybotCookiebotDialogBodyButtonAccept", "button:has-text('DECLINE ALL')"]) {
        try { await page.click(sel, { timeout: 1500 }); await page.waitForTimeout(400); } catch (e) {}
      }
      // 滚动到内容主体区域
      await page.evaluate(() => window.scrollTo(0, 350));
      await page.waitForTimeout(1200);
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
