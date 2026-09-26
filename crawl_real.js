
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const EDGE_PATH = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe";
const OUTPUT_DIR = "C:\\Users\\通明街\\Doubao\\chats\\2026-09-02\\new-chat\\top20_real_screenshots";
const TOOLS = [{"name": "Grammarly", "slug": "grammarly", "rating": 9.2, "sources": ["https://www.g2.com/products/grammarly/screenshots", "https://www.capterra.com/p/142594/Grammarly/", "https://www.grammarly.com/blog/"]}, {"name": "Claude", "slug": "claude", "rating": 9.1, "sources": ["https://www.g2.com/products/claude/screenshots", "https://www.capterra.com/p/265486/Claude/", "https://docs.anthropic.com/en/docs/overview"]}, {"name": "GitHub Copilot", "slug": "github-copilot", "rating": 9.1, "sources": ["https://www.g2.com/products/github-copilot/screenshots", "https://www.capterra.com/p/252078/GitHub-Copilot/", "https://github.blog/changelog/"]}, {"name": "Cursor", "slug": "cursor", "rating": 9.0, "sources": ["https://www.g2.com/products/cursor/screenshots", "https://www.capterra.com/p/269580/Cursor/", "https://docs.cursor.com/"]}, {"name": "ElevenLabs", "slug": "elevenlabs", "rating": 9.0, "sources": ["https://www.g2.com/products/elevenlabs/screenshots", "https://www.capterra.com/p/256877/ElevenLabs/", "https://elevenlabs.io/blog"]}, {"name": "DALL-E 3", "slug": "dall-e-3", "rating": 8.9, "sources": ["https://www.g2.com/products/dall-e-3/screenshots", "https://www.capterra.com/p/248803/DALL-E-3/", "https://openai.com/blog"]}, {"name": "Notion AI", "slug": "notion-ai", "rating": 8.9, "sources": ["https://www.g2.com/products/notion-ai/screenshots", "https://www.capterra.com/p/247558/Notion-AI/", "https://www.notion.so/help"]}, {"name": "Canva Magic", "slug": "canva-magic", "rating": 8.9, "sources": ["https://www.g2.com/products/canva/screenshots", "https://www.capterra.com/p/118401/Canva/", "https://www.canva.com/designschool/"]}, {"name": "Windsurf", "slug": "windsurf", "rating": 8.8, "sources": ["https://www.g2.com/products/windsurf/screenshots", "https://www.capterra.com/p/271234/Windsurf/"]}, {"name": "Perplexity", "slug": "perplexity", "rating": 8.8, "sources": ["https://www.g2.com/products/perplexity-ai/screenshots", "https://www.capterra.com/p/262783/Perplexity-AI/", "https://blog.perplexity.ai/"]}, {"name": "ChatGPT", "slug": "chatgpt", "rating": 8.7, "sources": ["https://www.g2.com/products/chatgpt/screenshots", "https://www.capterra.com/p/252078/ChatGPT/", "https://openai.com/blog"]}, {"name": "Figma AI", "slug": "figma-ai", "rating": 8.7, "sources": ["https://www.g2.com/products/figma/screenshots", "https://www.capterra.com/p/147608/Figma/", "https://help.figma.com/"]}, {"name": "Suno", "slug": "suno", "rating": 8.7, "sources": ["https://www.g2.com/products/suno/screenshots", "https://www.capterra.com/p/270123/Suno/"]}, {"name": "Runway", "slug": "runway", "rating": 8.6, "sources": ["https://www.g2.com/products/runway/screenshots", "https://www.capterra.com/p/191234/Runway/", "https://runwayml.com/blog"]}, {"name": "Midjourney", "slug": "midjourney", "rating": 8.5, "sources": ["https://www.g2.com/products/midjourney/screenshots", "https://www.capterra.com/p/247890/Midjourney/", "https://docs.midjourney.com/"]}, {"name": "Sora", "slug": "sora", "rating": 8.5, "sources": ["https://www.g2.com/products/sora/screenshots", "https://www.capterra.com/p/271567/Sora/"]}, {"name": "Jasper", "slug": "jasper", "rating": 8.4, "sources": ["https://www.g2.com/products/jasper/screenshots", "https://www.capterra.com/p/185456/Jasper/", "https://www.jasper.ai/blog"]}, {"name": "Gemini", "slug": "gemini", "rating": 8.3, "sources": ["https://www.g2.com/products/google-gemini/screenshots", "https://www.capterra.com/p/265432/Google-Gemini/", "https://blog.google/technology/ai/"]}, {"name": "Copy.ai", "slug": "copy-ai", "rating": 8.3, "sources": ["https://www.g2.com/products/copy-ai/screenshots", "https://www.capterra.com/p/185678/Copy-ai/", "https://www.copy.ai/blog"]}, {"name": "Stable Diffusion", "slug": "stable-diffusion", "rating": 8.2, "sources": ["https://www.g2.com/products/stable-diffusion/screenshots", "https://www.capterra.com/p/247654/Stable-Diffusion/", "https://github.com/Stability-AI/stablediffusion"]}];
const HIDE_COOKIE_CSS = `
[class*="cookie"], [class*="Cookie"], [id*="cookie"], [id*="Cookie"],
[class*="consent"], [class*="Consent"], [class*="gdpr"], [class*="GDPR"],
[class*="onetrust"], [id*="onetrust"], [class*="cookiebot"], [class*="cc-"],
[class*="chat-widget"], [class*="chatWidget"], [class*="intercom"], [class*="crisp"],
[class*="popup"], [class*="modal-backdrop"], [class*="newsletter-popup"],
[class*="floating-button"], [class*="floating-widget"], [class*="banner"],
[class*="announcement"], [class*="promo-banner"], [class*="sticky-banner"],
[class*="signup"], [class*="login-prompt"], [class*="cta-banner"]
{ display: none !important; opacity: 0 !important; visibility: hidden !important; pointer-events: none !important; z-index: -9999 !important; }
`;

async function tryUrl(browser, tool, url, sourceName, attempt) {
  const page = await browser.newPage();
  try {
    await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
    await page.setExtraHTTPHeaders({ 'Accept-Language': 'en-US,en;q=0.9' });
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
    
    console.log(`  [${sourceName} ${attempt}] ${url}`);
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 35000 });
    await new Promise(r => setTimeout(r, 4000));
    
    await page.addStyleTag({ content: HIDE_COOKIE_CSS });
    await new Promise(r => setTimeout(r, 800));
    
    // 滚动触发懒加载
    await page.evaluate(async () => {
      await new Promise((resolve) => {
        let totalHeight = 0;
        const distance = 400;
        const timer = setInterval(() => {
          window.scrollBy(0, distance);
          totalHeight += distance;
          if (totalHeight >= document.body.scrollHeight || totalHeight > 3000) {
            clearInterval(timer);
            window.scrollTo(0, 0);
            resolve();
          }
        }, 150);
      });
    });
    await new Promise(r => setTimeout(r, 2000));
    await page.addStyleTag({ content: HIDE_COOKIE_CSS });
    await new Promise(r => setTimeout(r, 500));
    
    const title = await page.title();
    const currentUrl = page.url();
    
    // 检查是否是404或错误页
    const isError = titleLower.includes('404') || titleLower.includes('not found') || titleLower.includes('error') || titleLower.includes('page not found');
    const titleLower = title.toLowerCase();
    
    // 保存截图
    const toolDir = path.join(OUTPUT_DIR, tool.slug);
    if (!fs.existsSync(toolDir)) fs.mkdirSync(toolDir, { recursive: true });
    const safeSource = sourceName.replace(/[^a-z0-9]/gi, '_').toLowerCase();
    const viewportPath = path.join(toolDir, `${safeSource}_viewport.png`);
    await page.screenshot({ path: viewportPath, fullPage: false });
    
    // 也保存全页截图
    const fullPath = path.join(toolDir, `${safeSource}_full.png`);
    try {
      await page.screenshot({ path: fullPath, fullPage: true });
    } catch(e) {}
    
    await page.close();
    
    const fileSize = fs.existsSync(viewportPath) ? fs.statSync(viewportPath).size : 0;
    return { success: !isError, isError, title, url: currentUrl, source: sourceName, viewportPath, fullPath, fileSize };
    
  } catch (error) {
    await page.close().catch(() => {});
    return { success: false, error: error.message, source: sourceName };
  }
}

async function main() {
  console.log('=== Real Product UI Screenshot Crawler ===');
  console.log('Sources: G2.com, Capterra.com, Docs, Blogs');
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
      const url = tool.sources[i];
      const sourceName = url.includes('g2.com') ? 'G2' : 
                         url.includes('capterra') ? 'Capterra' :
                         url.includes('docs') ? 'Docs' :
                         url.includes('blog') ? 'Blog' :
                         url.includes('github') ? 'GitHub' : 'Other';
      const result = await tryUrl(browser, tool, url, sourceName, i + 1);
      toolResults.push(result);
      if (result.success && result.fileSize > 10000) {
        console.log(`  ✅ ${sourceName}: ${result.title.slice(0,50)} (${(result.fileSize/1024).toFixed(0)}KB)`);
      } else if (result.success) {
        console.log(`  ⚠️ ${sourceName}: small file (${(result.fileSize/1024).toFixed(0)}KB)`);
      } else {
        console.log(`  ❌ ${sourceName}: ${result.error || 'error page'}`);
      }
    }
    
    results.push({ ...tool, sources: toolResults });
    await new Promise(r => setTimeout(r, 2000));
    console.log('');
  }
  
  await browser.close();
  
  const resultsPath = path.join(OUTPUT_DIR, 'results.json');
  fs.writeFileSync(resultsPath, JSON.stringify(results, null, 2));
  
  const totalSuccess = results.reduce((acc, r) => acc + r.sources.filter(s => s.success && s.fileSize > 10000).length, 0);
  console.log(`=== Complete: ${totalSuccess} real screenshots captured ===`);
  console.log(`Results: ${resultsPath}`);
}

main().catch(console.error);
