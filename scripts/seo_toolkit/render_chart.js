const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const htmlPath = "C:\\Users\\通明街\\Doubao\\chats\\2026-08-28\\new-chat\\ai-tools-review\\content_drafts\\screenshots\\n8n\\pricing_chart.html";
const OUT = "C:\\Users\\通明街\\Doubao\\chats\\2026-08-28\\new-chat\\ai-tools-review\\content_drafts\\screenshots\\n8n";

(async () => {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
  const page = await browser.newPage({ viewport: { width: 1200, height: 900 } });
  await page.goto("file:///" + htmlPath.replace(/\\/g, "/"), { waitUntil: "networkidle", timeout: 30000 });
  await page.waitForTimeout(2500);
  const fp = path.join(OUT, "pricing_chart.png");
  await page.screenshot({ path: fp, fullPage: true, type: "png" });
  console.log(`saved ${fp} (${Math.round(fs.statSync(fp).size/1024)}KB)`);
  await browser.close();
})();
