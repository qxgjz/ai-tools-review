
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const EDGE_PATH = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe";
const OUTPUT_DIR = "C:\\Users\\通明街\\Doubao\\chats\\2026-09-02\\new-chat\\top20_screenshots_v4";

const TOOLS = [{"name": "Grammarly", "slug": "grammarly", "rating": 9.2, "expected": "grammarly", "urls": ["https://www.grammarly.com/", "https://www.grammarly.com/grammar-check"]}, {"name": "Claude", "slug": "claude", "rating": 9.1, "expected": "claude", "urls": ["https://www.anthropic.com/claude", "https://www.anthropic.com/", "https://claude.ai/"]}, {"name": "GitHub Copilot", "slug": "github-copilot", "rating": 9.1, "expected": "copilot", "urls": ["https://github.com/features/copilot", "https://github.com/features/copilot/plans"]}, {"name": "Cursor", "slug": "cursor", "rating": 9.0, "expected": "cursor", "urls": ["https://www.cursor.com/", "https://cursor.com/"]}, {"name": "ElevenLabs", "slug": "elevenlabs", "rating": 9.0, "expected": "elevenlabs", "urls": ["https://elevenlabs.io/", "https://elevenlabs.io/text-to-speech"]}, {"name": "DALL-E 3", "slug": "dall-e-3", "rating": 8.9, "expected": "dall", "urls": ["https://openai.com/dall-e-3", "https://openai.com/index/dall-e-3/"]}, {"name": "Notion AI", "slug": "notion-ai", "rating": 8.9, "expected": "notion", "urls": ["https://www.notion.so/product/ai", "https://www.notion.com/product/ai"]}, {"name": "Canva Magic", "slug": "canva-magic", "rating": 8.9, "expected": "canva", "urls": ["https://www.canva.com/magic/", "https://www.canva.com/canva-ai/"]}, {"name": "Windsurf", "slug": "windsurf", "rating": 8.8, "expected": "windsurf", "urls": ["https://windsurf.com/", "https://codeium.com/windsurf"]}, {"name": "Perplexity", "slug": "perplexity", "rating": 8.8, "expected": "perplexity", "urls": ["https://www.perplexity.ai/", "https://www.perplexity.ai/"]}, {"name": "ChatGPT", "slug": "chatgpt", "rating": 8.7, "expected": "chatgpt", "urls": ["https://openai.com/chatgpt", "https://chatgpt.com/"]}, {"name": "Figma AI", "slug": "figma-ai", "rating": 8.7, "expected": "figma", "urls": ["https://www.figma.com/ai/", "https://www.figma.com/"]}, {"name": "Suno", "slug": "suno", "rating": 8.7, "expected": "suno", "urls": ["https://suno.com/", "https://suno.com/create"]}, {"name": "Runway", "slug": "runway", "rating": 8.6, "expected": "runway", "urls": ["https://runwayml.com/", "https://runway.com/"]}, {"name": "Midjourney", "slug": "midjourney", "rating": 8.5, "expected": "midjourney", "urls": ["https://docs.midjourney.com/", "https://www.midjourney.com/"]}, {"name": "Sora", "slug": "sora", "rating": 8.5, "expected": "sora", "urls": ["https://openai.com/sora", "https://openai.com/index/sora/"]}, {"name": "Jasper", "slug": "jasper", "rating": 8.4, "expected": "jasper", "urls": ["https://www.jasper.ai/", "https://www.jasper.ai/products"]}, {"name": "Gemini", "slug": "gemini", "rating": 8.3, "expected": "gemini", "urls": ["https://gemini.google.com/", "https://deepmind.google/technologies/gemini/"]}, {"name": "Copy.ai", "slug": "copy-ai", "rating": 8.3, "expected": "copy", "urls": ["https://www.copy.ai/", "https://www.copy.ai/platform"]}, {"name": "Stable Diffusion", "slug": "stable-diffusion", "rating": 8.2, "expected": "stability", "urls": ["https://stability.ai/", "https://stability.ai/news"]}];
const HIDE_COOKIE_CSS = `
[class*="cookie"], [class*="Cookie"], [id*="cookie"], [id*="Cookie"],
[class*="consent"], [class*="Consent"], [class*="gdpr"], [class*="GDPR"],
[class*="onetrust"], [id*="onetrust"], [class*="cookiebot"], [class*="cc-"],
[class*="chat-widget"], [class*="chatWidget"], [class*="intercom"], [class*="crisp"],
[class*="popup"], [class*="modal-backdrop"], [class*="newsletter-popup"],
[class*="floating-button"], [class*="floating-widget"], [class*="banner"],
[class*="announcement"], [class*="promo-banner"], [class*="sticky-banner"]
{ display: none !important; opacity: 0 !important; visibility: hidden !important; pointer-events: none !important; z-index: -9999 !important; }
`;

async function tryUrl(browser, tool, url, attempt) {
  const page = await browser.newPage();
  try {
    await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
    await page.setExtraHTTPHeaders({ 'Accept-Language': 'en-US,en;q=0.9' });
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
    
    console.log(`  [尝试${attempt}] ${url}`);
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 40000 });
    await new Promise(r => setTimeout(r, 4000));
    
    // 注入CSS隐藏cookie横幅
    await page.addStyleTag({ content: HIDE_COOKIE_CSS });
    await new Promise(r => setTimeout(r, 800));
    
    // 智能点击cookie接受按钮（只点击明显在cookie横幅内的按钮）
    try {
      const acceptButtons = await page.$$('button:has-text("Accept"), button:has-text("Accept All"), button:has-text("I Agree"), button:has-text("Got it"), button:has-text("Allow all"), [id*="accept"]');
      for (const btn of acceptButtons.slice(0, 2)) {
        const box = await btn.boundingBox();
        if (box && box.y > 500) { // 只点击页面下方的按钮（通常是cookie横幅）
          await btn.click({ timeout: 2000 }).catch(() => {});
          await new Promise(r => setTimeout(r, 1000));
          break;
        }
      }
    } catch (e) {}
    
    // 再次注入CSS
    await page.addStyleTag({ content: HIDE_COOKIE_CSS });
    
    // 滚动触发懒加载
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
        }, 200);
      });
    });
    await new Promise(r => setTimeout(r, 2500));
    await page.addStyleTag({ content: HIDE_COOKIE_CSS });
    await new Promise(r => setTimeout(r, 500));
    
    // 验证页面标题
    const title = await page.title();
    const currentUrl = page.url();
    const titleLower = title.toLowerCase();
    const expectedLower = tool.expected.toLowerCase();
    const isCorrect = titleLower.includes(expectedLower) || currentUrl.includes(tool.expected.toLowerCase());
    
    if (!isCorrect) {
      console.log(`  ⚠️ 标题不匹配: "${title}" (预期包含"${tool.expected}")`);
    }
    
    // 保存截图
    const toolDir = path.join(OUTPUT_DIR, tool.slug);
    if (!fs.existsSync(toolDir)) fs.mkdirSync(toolDir, { recursive: true });
    const viewportPath = path.join(toolDir, 'viewport.png');
    await page.screenshot({ path: viewportPath, fullPage: false });
    
    await page.close();
    return { success: true, isCorrect, title, url: currentUrl, viewportPath };
    
  } catch (error) {
    await page.close().catch(() => {});
    return { success: false, error: error.message };
  }
}

async function main() {
  console.log('=== Puppeteer (90.3k stars, Google官方) Screenshot Crawler v4 ===');
  console.log('Features: Multi-URL fallback, smart cookie handling, page verification');
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
    let finalResult = null;
    
    for (let i = 0; i < tool.urls.length; i++) {
      const result = await tryUrl(browser, tool, tool.urls[i], i + 1);
      if (result.success) {
        finalResult = { ...tool, ...result };
        if (result.isCorrect) {
          console.log(`  ✅ 成功 (URL ${i + 1})`);
          break;
        } else {
          console.log(`  ⚠️ 成功但标题不匹配，尝试下一个URL...`);
        }
      }
    }
    
    if (!finalResult) {
      finalResult = { ...tool, success: false, error: 'All URLs failed', isCorrect: false };
      console.log(`  ❌ 所有URL均失败`);
    }
    
    results.push(finalResult);
    await new Promise(r => setTimeout(r, 2000));
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
