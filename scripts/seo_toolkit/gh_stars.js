const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
  const page = await (await browser.newContext({ userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0" })).newPage();
  try {
    await page.goto("https://github.com/n8n-io/n8n", { waitUntil: "domcontentloaded", timeout: 45000 });
    await page.waitForTimeout(4000);
    const info = await page.evaluate(() => {
      const el = document.querySelector('a[href="/n8n-io/n8n/stargazers"], #repo-stars-counter-star, span#repo-stars-counter-star');
      const star = el ? el.textContent.trim() : null;
      // meta og
      const og = document.querySelector('meta[property="og:description"]');
      return { star, og: og ? og.content : null };
    });
    console.log(JSON.stringify(info, null, 2));
  } catch (e) { console.log("FAIL: " + e.message); }
  await browser.close();
})();
