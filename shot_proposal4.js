const { chromium } = require('@playwright/test');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errors = [];
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', (e) => errors.push(String(e)));
  await page.goto('http://localhost:8088/design_proposals/design_proposal.html', { waitUntil: 'networkidle', timeout: 90000 });
  await page.waitForTimeout(1500);

  const imgStatus = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('img')).map((img) => ({
      src: img.src.split('/').pop(),
      loaded: img.complete && img.naturalWidth > 0,
    }));
  });
  console.log('IMGS:', JSON.stringify(imgStatus));

  await page.evaluate(() => document.getElementById('directions').scrollIntoView({ block: 'start' }));
  await page.waitForTimeout(500);
  await page.click('.dir-tab[data-dir="a"]');
  await page.waitForTimeout(800);
  await page.screenshot({ path: 'design_proposals/shot_dir_a.png' });
  await page.click('.dir-tab[data-dir="b"]');
  await page.waitForTimeout(800);
  await page.screenshot({ path: 'design_proposals/shot_dir_b.png' });
  await page.click('.dir-tab[data-dir="c"]');
  await page.waitForTimeout(800);
  await page.screenshot({ path: 'design_proposals/shot_dir_c.png' });
  await browser.close();
  console.log('CONSOLE_ERRORS:', errors.length);
})().catch((e) => { console.error('FATAL', e.message); process.exit(1); });
