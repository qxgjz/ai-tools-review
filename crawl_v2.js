
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const EDGE_PATH = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe";
const OUTPUT_DIR = "C:\\Users\\通明街\\Doubao\\chats\\2026-09-02\\new-chat\\top20_screenshots_v2";

const TOOLS = [{"name": "Grammarly", "slug": "grammarly", "url": "https://www.grammarly.com/", "rating": 9.2}, {"name": "Claude", "slug": "claude", "url": "https://claude.ai/", "rating": 9.1}, {"name": "GitHub Copilot", "slug": "github-copilot", "url": "https://github.com/features/copilot", "rating": 9.1}, {"name": "Cursor", "slug": "cursor", "url": "https://www.cursor.com/", "rating": 9.0}, {"name": "ElevenLabs", "slug": "elevenlabs", "url": "https://elevenlabs.io/", "rating": 9.0}, {"name": "DALL-E 3", "slug": "dall-e-3", "url": "https://openai.com/dall-e-3", "rating": 8.9}, {"name": "Notion AI", "slug": "notion-ai", "url": "https://www.notion.so/product/ai", "rating": 8.9}, {"name": "Canva Magic", "slug": "canva-magic", "url": "https://www.canva.com/magic/", "rating": 8.9}, {"name": "Windsurf", "slug": "windsurf", "url": "https://windsurf.com/", "rating": 8.8}, {"name": "Perplexity", "slug": "perplexity", "url": "https://www.perplexity.ai/", "rating": 8.8}, {"name": "ChatGPT", "slug": "chatgpt", "url": "https://openai.com/chatgpt", "rating": 8.7}, {"name": "Figma AI", "slug": "figma-ai", "url": "https://www.figma.com/ai/", "rating": 8.7}, {"name": "Suno", "slug": "suno", "url": "https://suno.com/", "rating": 8.7}, {"name": "Runway", "slug": "runway", "url": "https://runwayml.com/", "rating": 8.6}, {"name": "Midjourney", "slug": "midjourney", "url": "https://www.midjourney.com/", "rating": 8.5}, {"name": "Sora", "slug": "sora", "url": "https://openai.com/sora", "rating": 8.5}, {"name": "Jasper", "slug": "jasper", "url": "https://www.jasper.ai/", "rating": 8.4}, {"name": "Gemini", "slug": "gemini", "url": "https://gemini.google.com/", "rating": 8.3}, {"name": "Copy.ai", "slug": "copy-ai", "url": "https://www.copy.ai/", "rating": 8.3}, {"name": "Stable Diffusion", "slug": "stable-diffusion", "url": "https://stability.ai/", "rating": 8.2}];

const HIDE_COOKIE_CSS = `
/* Cookie banners */
[class*="cookie-banner"], [class*="cookieBanner"], [class*="cookie_notice"],
[class*="cookie-consent"], [class*="cookieConsent"], [class*="cookie-modal"],
[class*="gdpr"], [class*="GDPR"], [class*="consent-banner"], [class*="consentBanner"],
[class*="onetrust"], [id*="onetrust"], [class*="cookiebot"], [id*="CybotCookiebot"],
[class*="cc-window"], [class*="cc-banner"], [class*="osano"], [class*="iubenda"],
[class*="trustarc"], [class*="termly"], [class*="cookie-law"], [class*="cookiebar"],
[class*="cookie-bar"], [class*="cookie-popup"], [class*="cookie-overlay"],
[class*="privacy-banner"], [class*="privacy-consent"], [class*="accept-cookies"],
/* Chat widgets */
[class*="chat-widget"], [class*="chatWidget"], [class*="intercom"],
[class*="crisp"], [class*="tawk"], [class*="zendesk"], [class*="hubspot-messages"],
/* Ads */
[class*="advertisement"], [class*="ad-banner"], [class*="ad-slot"],
[id*="google_ads"], [class*="adsbygoogle"],
/* Popups */
[class*="popup-overlay"], [class*="modal-backdrop"], [class*="newsletter-popup"],
[class*="exit-intent"], [class*="lead-popup"]
{ display: none !important; opacity: 0 !important; visibility: hidden !important; pointer-events: none !important; z-index: -9999 !important; }
`;

const CLICK_ACCEPT_JS = () => {
  const acceptTexts = [
    'accept', 'accept all', 'accept all cookies', 'accept cookies',
    'i agree', 'agree', 'agree to all', 'got it', 'got it!',
    'ok', 'okay', 'allow all', 'allow', 'allow cookies',
    'confirm', 'continue', 'yes, accept', 'no thanks', 'dismiss',
    '关闭', '接受', '同意', '我同意', '知道了', '确认'
  ];
  const buttons = document.querySelectorAll('button, a, [role="button"], input[type="button"], input[type="submit"]');
  for (const btn of buttons) {
    const text = (btn.textContent || btn.value || '').trim().toLowerCase();
    if (text && acceptTexts.some(t => text === t || text.includes(t))) {
      const rect = btn.getBoundingClientRect();
      if (rect.width > 0 && rect.height > 0) {
        btn.click();
        return 'clicked: ' + text;
      }
    }
  }
  return 'no accept button found';
};

async function takeScreenshot(browser, tool) {
  const page = await browser.newPage();
  const toolDir = path.join(OUTPUT_DIR, tool.slug);
  if (!fs.existsSync(toolDir)) fs.mkdirSync(toolDir, { recursive: true });
  
  try {
    await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
    
    // 设置User-Agent
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
    
    console.log(`[${tool.name}] Navigating to ${tool.url}...`);
    await page.goto(tool.url, { waitUntil: 'networkidle2', timeout: 30000 });
    
    // 等待额外时间让动态内容加载
    await new Promise(r => setTimeout(r, 3000));
    
    // 注入CSS隐藏cookie横幅
    await page.addStyleTag({ content: HIDE_COOKIE_CSS });
    
    // 尝试点击接受按钮
    try {
      const result = await page.evaluate(CLICK_ACCEPT_JS);
      console.log(`[${tool.name}] Cookie button: ${result}`);
    } catch(e) {
      console.log(`[${tool.name}] Cookie click error: ${e.message}`);
    }
    
    // 再等待一下
    await new Promise(r => setTimeout(r, 1500));
    
    // 滚动页面触发懒加载
    await page.evaluate(async () => {
      await new Promise((resolve) => {
        let totalHeight = 0;
        const distance = 400;
        const timer = setInterval(() => {
          window.scrollBy(0, distance);
          totalHeight += distance;
          if (totalHeight >= document.body.scrollHeight) {
            clearInterval(timer);
            window.scrollTo(0, 0);
            resolve();
          }
        }, 200);
      });
    });
    
    // 等待滚动后内容加载
    await new Promise(r => setTimeout(r, 2000));
    
    // 再次注入CSS（滚动后可能有新的弹窗）
    await page.addStyleTag({ content: HIDE_COOKIE_CSS });
    
    // 截取视口截图
    const viewportPath = path.join(toolDir, 'viewport.png');
    await page.screenshot({ path: viewportPath, fullPage: false });
    console.log(`[${tool.name}] Viewport screenshot saved`);
    
    // 截取全页面截图
    const fullPath = path.join(toolDir, 'fullpage.png');
    await page.screenshot({ path: fullPath, fullPage: true });
    console.log(`[${tool.name}] Full page screenshot saved`);
    
    // 获取页面标题和URL用于验证
    const title = await page.title();
    const currentUrl = page.url();
    console.log(`[${tool.name}] Title: ${title}`);
    console.log(`[${tool.name}] URL: ${currentUrl}`);
    
    await page.close();
    return { success: true, title, url: currentUrl, viewportPath, fullPath };
    
  } catch (error) {
    console.log(`[${tool.name}] ERROR: ${error.message}`);
    await page.close().catch(() => {});
    return { success: false, error: error.message };
  }
}

async function main() {
  console.log('Starting improved screenshot crawler...');
  console.log(`Output directory: ${OUTPUT_DIR}`);
  console.log(`Tools to crawl: ${TOOLS.length}`);
  
  if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  
  const browser = await puppeteer.launch({
    executablePath: EDGE_PATH,
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--disable-dev-shm-usage',
      '--disable-gpu',
      '--window-size=1440,900'
    ]
  });
  
  const results = [];
  for (const tool of TOOLS) {
    console.log(`\n--- Processing: ${tool.name} (${tool.rating}/10) ---`);
    const result = await takeScreenshot(browser, tool);
    results.push({ ...tool, ...result });
    
    // 工具间延迟，避免被封
    await new Promise(r => setTimeout(r, 2000));
  }
  
  await browser.close();
  
  // 保存结果
  const resultsPath = path.join(OUTPUT_DIR, 'results.json');
  fs.writeFileSync(resultsPath, JSON.stringify(results, null, 2));
  
  const successCount = results.filter(r => r.success).length;
  console.log(`\n=== Complete: ${successCount}/${TOOLS.length} successful ===`);
  console.log(`Results saved to: ${resultsPath}`);
}

main().catch(console.error);
