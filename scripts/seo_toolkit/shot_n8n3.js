const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const OUT = "C:\\Users\\通明街\\Doubao\\chats\\2026-08-28\\new-chat\\ai-tools-review\\content_drafts\\screenshots\\n8n\\real_ui";

(async () => {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
  const ctx = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
  });
  const page = await ctx.newPage();
  try {
    await page.goto("https://n8n.io/workflows/", { waitUntil: "domcontentloaded", timeout: 45000 });
    await page.waitForTimeout(5000);
    for (const sel of ["button:has-text('Accept all')", "button:has-text('Accept')", "#CybotCookiebotDialogBodyButtonAccept"]) {
      try { await page.click(sel, { timeout: 1500 }); await page.waitForTimeout(400); } catch (e) {}
    }
    // 滚动到模板网格区域（找真实工作流卡片）
    await page.evaluate(() => window.scrollTo(0, 400));
    await page.waitForTimeout(1500);
    const fp = path.join(OUT, "template-grid.png");
    await page.screenshot({ path: fp, fullPage: false, type: "png" });
    console.log(`template-grid OK (${Math.round(fs.statSync(fp).size/1024)}KB)`);
    // 再截一个AI相关模板详情页
  } catch (e) { console.log("FAIL: " + e.message); }
  await browser.close();
  console.log("done");
})();
