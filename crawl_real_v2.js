
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const EDGE_PATH = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe";
const OUTPUT_DIR = "C:\\Users\\通明街\\Doubao\\chats\\2026-09-02\\new-chat\\top20_real_screenshots";
const TOOLS = [{"name": "Grammarly", "slug": "grammarly", "rating": 9.2, "sources": [["docs", "https://support.grammarly.com/"], ["blog", "https://www.grammarly.com/blog/grammar/"], ["app", "https://app.grammarly.com/"]]}, {"name": "Claude", "slug": "claude", "rating": 9.1, "sources": [["docs", "https://docs.anthropic.com/en/docs/overview"], ["app", "https://claude.ai/"], ["blog", "https://www.anthropic.com/news"]]}, {"name": "GitHub Copilot", "slug": "github-copilot", "rating": 9.1, "sources": [["docs", "https://docs.github.com/en/copilot"], ["blog", "https://github.blog/changelog/label/copilot/"]]}, {"name": "Cursor", "slug": "cursor", "rating": 9.0, "sources": [["docs", "https://docs.cursor.com/get-started"], ["blog", "https://www.cursor.com/blog"]]}, {"name": "ElevenLabs", "slug": "elevenlabs", "rating": 9.0, "sources": [["docs", "https://elevenlabs.io/docs/introduction"], ["app", "https://elevenlabs.io/app/text-to-speech"], ["blog", "https://elevenlabs.io/blog"]]}, {"name": "DALL-E 3", "slug": "dall-e-3", "rating": 8.9, "sources": [["blog", "https://openai.com/blog/dall-e-3/"], ["docs", "https://platform.openai.com/docs/guides/images"]]}, {"name": "Notion AI", "slug": "notion-ai", "rating": 8.9, "sources": [["docs", "https://www.notion.so/help/notion-ai"], ["app", "https://www.notion.so/"]]}, {"name": "Canva Magic", "slug": "canva-magic", "rating": 8.9, "sources": [["docs", "https://www.canva.com/help/magic-design/"], ["blog", "https://www.canva.com/blog/category/design/"]]}, {"name": "Windsurf", "slug": "windsurf", "rating": 8.8, "sources": [["docs", "https://docs.codeium.com/"], ["blog", "https://codeium.com/blog"]]}, {"name": "Perplexity", "slug": "perplexity", "rating": 8.8, "sources": [["app", "https://www.perplexity.ai/"], ["docs", "https://docs.perplexity.ai/"], ["blog", "https://blog.perplexity.ai/"]]}, {"name": "ChatGPT", "slug": "chatgpt", "rating": 8.7, "sources": [["app", "https://chatgpt.com/"], ["blog", "https://openai.com/blog/chatgpt/"], ["docs", "https://platform.openai.com/docs/overview"]]}, {"name": "Figma AI", "slug": "figma-ai", "rating": 8.7, "sources": [["docs", "https://help.figma.com/hc/en-us/categories/126080102114-Magic"], ["blog", "https://www.figma.com/blog/"]]}, {"name": "Suno", "slug": "suno", "rating": 8.7, "sources": [["app", "https://suno.com/create"], ["docs", "https://docs.suno.com/"]]}, {"name": "Runway", "slug": "runway", "rating": 8.6, "sources": [["docs", "https://help.runwayml.com/hc/en-us"], ["blog", "https://runwayml.com/blog/"], ["app", "https://runwayml.com/"]]}, {"name": "Midjourney", "slug": "midjourney", "rating": 8.5, "sources": [["docs", "https://docs.midjourney.com/docs/quick-start"], ["app", "https://www.midjourney.com/app/"]]}, {"name": "Sora", "slug": "sora", "rating": 8.5, "sources": [["blog", "https://openai.com/blog/sora/"], ["docs", "https://platform.openai.com/docs/guides/video"]]}, {"name": "Jasper", "slug": "jasper", "rating": 8.4, "sources": [["docs", "https://www.jasper.ai/docs"], ["blog", "https://www.jasper.ai/blog"]]}, {"name": "Gemini", "slug": "gemini", "rating": 8.3, "sources": [["app", "https://gemini.google.com/"], ["docs", "https://ai.google.dev/gemini-api/docs"], ["blog", "https://blog.google/technology/ai/"]]}, {"name": "Copy.ai", "slug": "copy-ai", "rating": 8.3, "sources": [["docs", "https://www.copy.ai/docs"], ["blog", "https://www.copy.ai/blog"]]}, {"name": "Stable Diffusion", "slug": "stable-diffusion", "rating": 8.2, "sources": [["github", "https://github.com/Stability-AI/stablediffusion"], ["docs", "https://platform.stability.ai/docs/getting-started"], ["blog", "https://stability.ai/news"]]}];
const HIDE_COOKIE_CSS = `
[class*="cookie"], [class*="Cookie"], [id*="cookie"], [id*="Cookie"],
[class*="consent"], [class*="Consent"], [class*="gdpr"], [class*="GDPR"],
[class*="onetrust"], [id*="onetrust"], [class*="cookiebot"], [class*="cc-"],
[class*="chat-widget"], [class*="chatWidget"], [class*="intercom"], [class*="crisp"],
[class*="popup"], [class*="modal-backdrop"], [class*="newsletter-popup"],
[class*="floating-button"], [class*="floating-widget"], [class*="banner"],
[class*="announcement"], [class*="promo-banner"], [class*="sticky-banner"],
[class*="signup"], [class*="login-prompt"], [class*="cta-banner"],
[class*="auth-wall"], [class*="paywall"]
{ display: none !important; opacity: 0 !important; visibility: hidden !important; pointer-events: none !important; z-index: -9999 !important; }
`;

async function tryUrl(browser, tool, url, sourceType, attempt) {
  const page = await browser.newPage();
  try {
    await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
    await page.setExtraHTTPHeaders({ 'Accept-Language': 'en-US,en;q=0.9' });
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
    
    console.log(`  [${sourceType} ${attempt}] ${url}`);
    
    // 更短的超时，避免卡住
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 25000 });
    await new Promise(r => setTimeout(r, 3000));
    
    await page.addStyleTag({ content: HIDE_COOKIE_CSS });
    await new Promise(r => setTimeout(r, 500));
    
    // 滚动触发懒加载（限制滚动距离）
    await page.evaluate(async () => {
      await new Promise((resolve) => {
        let totalHeight = 0;
        const distance = 400;
        const timer = setInterval(() => {
          window.scrollBy(0, distance);
          totalHeight += distance;
          if (totalHeight >= 2500 || totalHeight >= document.body.scrollHeight) {
            clearInterval(timer);
            window.scrollTo(0, 0);
            resolve();
          }
        }, 120);
      });
    });
    await new Promise(r => setTimeout(r, 1500));
    await page.addStyleTag({ content: HIDE_COOKIE_CSS });
    await new Promise(r => setTimeout(r, 300));
    
    const title = await page.title();
    const currentUrl = page.url();
    const titleLower = title.toLowerCase();
    
    // 检查是否是登录墙或错误页
    const isLoginWall = titleLower.includes('sign in') || titleLower.includes('log in') || 
                        titleLower.includes('login') || titleLower.includes('sign up') ||
                        titleLower.includes('register') || currentUrl.includes('/login') || 
                        currentUrl.includes('/signin') || currentUrl.includes('/auth');
    const isError = titleLower.includes('404') || titleLower.includes('not found') || 
                     titleLower.includes('error') || titleLower.includes('page not found');
    
    // 保存截图
    const toolDir = path.join(OUTPUT_DIR, tool.slug);
    if (!fs.existsSync(toolDir)) fs.mkdirSync(toolDir, { recursive: true });
    const viewportPath = path.join(toolDir, `${sourceType}_viewport.png`);
    await page.screenshot({ path: viewportPath, fullPage: false });
    
    await page.close();
    
    const fileSize = fs.existsSync(viewportPath) ? fs.statSync(viewportPath).size : 0;
    const isGood = !isLoginWall && !isError && fileSize > 15000;
    
    return { success: isGood, isLoginWall, isError, title, url: currentUrl, source: sourceType, viewportPath, fileSize };
    
  } catch (error) {
    await page.close().catch(() => {});
    return { success: false, error: error.message.substring(0, 80), source: sourceType };
  }
}

async function main() {
  console.log('=== Real Product UI Screenshot Crawler v2 ===');
  console.log('Sources: Docs, Blogs, Web Apps, GitHub (no G2/Capterra)');
  console.log(`Output: ${OUTPUT_DIR}`);
  console.log(`Tools: ${TOOLS.length}`);
  console.log('');
  
  if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  
  const browser = await puppeteer.launch({
    executablePath: EDGE_PATH,
    headless: 'new',
    args: [
      '--no-sandbox', '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--disable-dev-shm-usage', '--disable-gpu',
      '--window-size=1440,900', '--lang=en-US'
    ]
  });
  
  const results = [];
  for (const tool of TOOLS) {
    console.log(`--- ${tool.name} (${tool.rating}/10) ---`);
    const toolResults = [];
    
    for (let i = 0; i < tool.sources.length; i++) {
      const [sourceType, url] = tool.sources[i];
      const result = await tryUrl(browser, tool, url, sourceType, i + 1);
      toolResults.push(result);
      if (result.success) {
        console.log(`  ✅ ${sourceType}: ${result.title.slice(0,50)} (${(result.fileSize/1024).toFixed(0)}KB)`);
      } else if (result.isLoginWall) {
        console.log(`  ⚠️ ${sourceType}: Login wall, skipping`);
      } else if (result.isError) {
        console.log(`  ⚠️ ${sourceType}: Error page`);
      } else {
        console.log(`  ❌ ${sourceType}: ${result.error || 'failed'}`);
      }
    }
    
    results.push({ ...tool, sources: toolResults });
    await new Promise(r => setTimeout(r, 1500));
    console.log('');
  }
  
  await browser.close();
  
  const resultsPath = path.join(OUTPUT_DIR, 'results.json');
  fs.writeFileSync(resultsPath, JSON.stringify(results, null, 2));
  
  const totalSuccess = results.reduce((acc, r) => acc + r.sources.filter(s => s.success).length, 0);
  const toolsWithScreenshot = results.filter(r => r.sources.some(s => s.success)).length;
  console.log(`=== Complete: ${totalSuccess} real screenshots, ${toolsWithScreenshot}/${TOOLS.length} tools have good screenshots ===`);
  console.log(`Results: ${resultsPath}`);
}

main().catch(e => { console.error('Fatal:', e.message); process.exit(1); });
