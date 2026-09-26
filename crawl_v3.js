
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const EDGE_PATH = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe";
const OUTPUT_DIR = "C:\\Users\\通明街\\Doubao\\chats\\2026-09-02\\new-chat\\top20_screenshots_v3";

const TOOLS = [{"name": "Grammarly", "slug": "grammarly", "url": "https://www.grammarly.com/", "rating": 9.2, "expected_title": "Grammarly"}, {"name": "Claude", "slug": "claude", "url": "https://www.anthropic.com/claude", "rating": 9.1, "expected_title": "Claude"}, {"name": "GitHub Copilot", "slug": "github-copilot", "url": "https://github.com/features/copilot", "rating": 9.1, "expected_title": "Copilot"}, {"name": "Cursor", "slug": "cursor", "url": "https://www.cursor.com/", "rating": 9.0, "expected_title": "Cursor"}, {"name": "ElevenLabs", "slug": "elevenlabs", "url": "https://elevenlabs.io/", "rating": 9.0, "expected_title": "ElevenLabs"}, {"name": "DALL-E 3", "slug": "dall-e-3", "url": "https://openai.com/dall-e-3", "rating": 8.9, "expected_title": "DALL"}, {"name": "Notion AI", "slug": "notion-ai", "url": "https://www.notion.so/product/ai", "rating": 8.9, "expected_title": "Notion"}, {"name": "Canva Magic", "slug": "canva-magic", "url": "https://www.canva.com/magic/", "rating": 8.9, "expected_title": "Canva"}, {"name": "Windsurf", "slug": "windsurf", "url": "https://windsurf.com/", "rating": 8.8, "expected_title": "Windsurf"}, {"name": "Perplexity", "slug": "perplexity", "url": "https://www.perplexity.ai/", "rating": 8.8, "expected_title": "Perplexity"}, {"name": "ChatGPT", "slug": "chatgpt", "url": "https://openai.com/chatgpt", "rating": 8.7, "expected_title": "ChatGPT"}, {"name": "Figma AI", "slug": "figma-ai", "url": "https://www.figma.com/ai/", "rating": 8.7, "expected_title": "Figma"}, {"name": "Suno", "slug": "suno", "url": "https://suno.com/", "rating": 8.7, "expected_title": "Suno"}, {"name": "Runway", "slug": "runway", "url": "https://runwayml.com/", "rating": 8.6, "expected_title": "Runway"}, {"name": "Midjourney", "slug": "midjourney", "url": "https://docs.midjourney.com/", "rating": 8.5, "expected_title": "Midjourney"}, {"name": "Sora", "slug": "sora", "url": "https://openai.com/sora", "rating": 8.5, "expected_title": "Sora"}, {"name": "Jasper", "slug": "jasper", "url": "https://www.jasper.ai/", "rating": 8.4, "expected_title": "Jasper"}, {"name": "Gemini", "slug": "gemini", "url": "https://gemini.google.com/", "rating": 8.3, "expected_title": "Gemini"}, {"name": "Copy.ai", "slug": "copy-ai", "url": "https://www.copy.ai/", "rating": 8.3, "expected_title": "Copy"}, {"name": "Stable Diffusion", "slug": "stable-diffusion", "url": "https://stability.ai/", "rating": 8.2, "expected_title": "Stability"}];

const HIDE_COOKIE_CSS = `
/* Cookie banners & consent */
[class*="cookie-banner"], [class*="cookieBanner"], [class*="cookie_notice"],
[class*="cookie-consent"], [class*="cookieConsent"], [class*="cookie-modal"],
[class*="gdpr"], [class*="GDPR"], [class*="consent-banner"], [class*="consentBanner"],
[class*="onetrust"], [id*="onetrust"], [class*="cookiebot"], [id*="CybotCookiebot"],
[class*="cc-window"], [class*="cc-banner"], [class*="osano"], [class*="iubenda"],
[class*="trustarc"], [class*="termly"], [class*="cookie-law"], [class*="cookiebar"],
[class*="cookie-bar"], [class*="cookie-popup"], [class*="cookie-overlay"],
[class*="privacy-banner"], [class*="privacy-consent"], [class*="accept-cookies"],
[class*="consent-modal"], [class*="consent-overlay"], [id*="cookie"],
[class*="CookieBanner"], [class*="CookieConsent"], [class*="ConsentBanner"],
/* Chat widgets */
[class*="chat-widget"], [class*="chatWidget"], [class*="intercom"],
[class*="crisp"], [class*="tawk"], [class*="zendesk"], [class*="hubspot-messages"],
[class*="chatbot"], [class*="chat-bubble"], [id*="chat-widget"],
/* Ads */
[class*="advertisement"], [class*="ad-banner"], [class*="ad-slot"],
[id*="google_ads"], [class*="adsbygoogle"], [class*="ad-container"],
/* Popups & overlays */
[class*="popup-overlay"], [class*="modal-backdrop"], [class*="newsletter-popup"],
[class*="exit-intent"], [class*="lead-popup"], [class*="signup-modal"],
[class*="login-modal"], [class*="overlay-backdrop"],
/* Annoying floating elements */
[class*="floating-button"], [class*="floating-widget"], [class*="sticky-banner"]
{ display: none !important; opacity: 0 !important; visibility: hidden !important; pointer-events: none !important; z-index: -9999 !important; }
`;

async function takeScreenshot(browser, tool) {
  const page = await browser.newPage();
  const toolDir = path.join(OUTPUT_DIR, tool.slug);
  if (!fs.existsSync(toolDir)) fs.mkdirSync(toolDir, { recursive: true });
  
  try {
    await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
    
    // 设置英文语言，避免中文重定向
    await page.setExtraHTTPHeaders({
      'Accept-Language': 'en-US,en;q=0.9'
    });
    
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
    
    console.log(`[${tool.name}] Navigating to ${tool.url}...`);
    await page.goto(tool.url, { waitUntil: 'networkidle2', timeout: 45000 });
    
    // 等待动态内容加载
    await new Promise(r => setTimeout(r, 4000));
    
    // 注入CSS隐藏cookie横幅/广告/弹窗（不点击任何按钮）
    await page.addStyleTag({ content: HIDE_COOKIE_CSS });
    
    // 再等待一下让CSS生效
    await new Promise(r => setTimeout(r, 1000));
    
    // 滚动页面触发懒加载图片
    await page.evaluate(async () => {
      await new Promise((resolve) => {
        let totalHeight = 0;
        const distance = 500;
        const timer = setInterval(() => {
          window.scrollBy(0, distance);
          totalHeight += distance;
          if (totalHeight >= document.body.scrollHeight) {
            clearInterval(timer);
            window.scrollTo(0, 0);
            resolve();
          }
        }, 250);
      });
    });
    
    // 等待滚动后内容加载
    await new Promise(r => setTimeout(r, 2500));
    
    // 再次注入CSS（滚动后可能有新弹窗）
    await page.addStyleTag({ content: HIDE_COOKIE_CSS });
    await new Promise(r => setTimeout(r, 500));
    
    // 截取视口截图
    const viewportPath = path.join(toolDir, 'viewport.png');
    await page.screenshot({ path: viewportPath, fullPage: false });
    console.log(`[${tool.name}] Viewport screenshot saved`);
    
    // 获取页面标题和URL用于验证
    const title = await page.title();
    const currentUrl = page.url();
    console.log(`[${tool.name}] Title: ${title}`);
    console.log(`[${tool.name}] URL: ${currentUrl}`);
    
    // 验证页面是否正确（标题是否包含预期关键词）
    const titleLower = title.toLowerCase();
    const expectedLower = (tool.expected_title || '').toLowerCase();
    const isCorrect = expectedLower === '' || titleLower.includes(expectedLower);
    if (!isCorrect) {
      console.log(`[${tool.name}] WARNING: Page may be wrong! Expected "${tool.expected_title}" in title`);
    }
    
    await page.close();
    return { success: true, title, url: currentUrl, viewportPath, isCorrect };
    
  } catch (error) {
    console.log(`[${tool.name}] ERROR: ${error.message}`);
    await page.close().catch(() => {});
    return { success: false, error: error.message };
  }
}

async function main() {
  console.log('=== Fixed Screenshot Crawler v3 ===');
  console.log('Strategy: CSS injection only (no auto-clicking)');
  console.log(`Output: ${OUTPUT_DIR}`);
  console.log(`Tools: ${TOOLS.length}`);
  console.log('');
  
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
      '--window-size=1440,900',
      '--lang=en-US'
    ]
  });
  
  const results = [];
  for (const tool of TOOLS) {
    console.log(`--- ${tool.name} (${tool.rating}/10) ---`);
    const result = await takeScreenshot(browser, tool);
    results.push({ ...tool, ...result });
    await new Promise(r => setTimeout(r, 2500));
    console.log('');
  }
  
  await browser.close();
  
  const resultsPath = path.join(OUTPUT_DIR, 'results.json');
  fs.writeFileSync(resultsPath, JSON.stringify(results, null, 2));
  
  const successCount = results.filter(r => r.success).length;
  const correctCount = results.filter(r => r.success && r.isCorrect).length;
  console.log(`=== Complete: ${successCount}/${TOOLS.length} successful, ${correctCount} verified correct ===`);
  console.log(`Results: ${resultsPath}`);
}

main().catch(console.error);
