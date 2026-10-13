const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const SRC = "C:\\Users\\通明街\\Doubao\\chats\\2026-08-28\\new-chat\\ai-tools-review\\content_drafts\\screenshots\\n8n";
const OUT = path.join(SRC, "webp");
fs.mkdirSync(OUT, { recursive: true });

const FILES = [
  ["real_ui\\github_2.png", "n8n-editor-ai-agent.webp"],          // 真实编辑器界面
  ["real_ui\\template-grid.png", "n8n-templates.webp"],           // 模板库
  ["pricing_chart.png", "n8n-pricing-chart.webp"],                // 价格对比图
  ["real_ui\\template-list_full.png", "n8n-workflows.webp"],      // 工作流模板库
];

(async () => {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  for (const [src, dst] of FILES) {
    try {
      const srcPath = path.join(SRC, src);
      await page.goto("file:///" + srcPath.replace(/\\/g, "/"), { waitUntil: "load", timeout: 20000 });
      await page.waitForTimeout(600);
      const fp = path.join(OUT, dst);
      // 按原图比例截取
      await page.screenshot({ path: fp, fullPage: true, type: "webp", quality: 82 });
      console.log(`OK ${dst} (${Math.round(fs.statSync(fp).size/1024)}KB)`);
    } catch (e) {
      console.log(`FAIL ${dst}: ${e.message}`);
    }
  }
  await browser.close();
  console.log("done");
})();
