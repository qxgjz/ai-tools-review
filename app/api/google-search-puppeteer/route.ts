import { NextRequest, NextResponse } from 'next/server';
import puppeteer from 'puppeteer-core';
import chromium from '@sparticuz/chromium';

/**
 * Google搜索代理API - 使用Puppeteer无头浏览器渲染JavaScript页面
 * 解决Google搜索需要JavaScript渲染的问题
 * 
 * 使用方法：
 * POST /api/google-search-puppeteer
 * Body: { "query": "site:https://www.aitoolcrux.com", "type": "indexing" | "ranking" }
 * Headers: Authorization: Bearer aitoolcrux-google-proxy-2026
 */

// API密钥（防止滥用）
const API_KEY = 'aitoolcrux-google-proxy-2026';

// 浏览器实例缓存（避免每次请求都启动新浏览器）
let browserInstance: any = null;
let browserLastUsed = 0;
const BROWSER_CACHE_TIME = 5 * 60 * 1000; // 5分钟缓存

export const maxDuration = 60; // Vercel函数最大执行时间60秒

export async function POST(request: NextRequest) {
  try {
    // 验证API密钥
    const authHeader = request.headers.get('authorization');
    if (!authHeader || authHeader !== `Bearer ${API_KEY}`) {
      return NextResponse.json(
        { error: 'Unauthorized', message: 'Invalid API key' },
        { status: 401 }
      );
    }

    // 解析请求体
    const body = await request.json();
    const { query, type = 'indexing', num = 20 } = body;

    if (!query) {
      return NextResponse.json(
        { error: 'Missing query parameter' },
        { status: 400 }
      );
    }

    console.log(`[Google Search Puppeteer] Query: ${query}, Type: ${type}`);

    // 获取或创建浏览器实例
    const browser = await getBrowser();
    if (!browser) {
      return NextResponse.json(
        {
          error: 'Failed to launch browser',
          details: 'Check server logs for details. This may be due to Vercel Serverless memory limits or Chromium binary issues.',
          suggestion: 'Consider using Google Custom Search JSON API or Bing search as alternative.',
        },
        { status: 500 }
      );
    }

    // 创建新页面
    const page = await browser.newPage();

    try {
      // 设置User-Agent和视口
      await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
      await page.setViewport({ width: 1920, height: 1080 });

      // 构建Google搜索URL
      const searchUrl = `https://www.google.com/search?q=${encodeURIComponent(query)}&num=${num}&hl=en`;

      console.log(`[Google Search Puppeteer] Navigating to: ${searchUrl}`);

      // 访问Google搜索
      await page.goto(searchUrl, {
        waitUntil: 'domcontentloaded',
        timeout: 30000,
      });

      // 等待搜索结果加载
      await page.waitForTimeout(3000);

      // 检查是否遇到验证码
      const pageTitle = await page.title();
      const pageContent = await page.content();
      const isCaptcha = pageContent.includes('captcha') || 
                        pageContent.includes('unusual traffic') ||
                        pageTitle.includes('sorry');

      if (isCaptcha) {
        console.log('[Google Search Puppeteer] Captcha detected, waiting...');
        await page.waitForTimeout(5000);
      }

      // 解析搜索结果
      const results = await page.evaluate((searchType: string) => {
        const results: any[] = [];

        if (searchType === 'indexing') {
          // 收录检查模式：检查是否有结果
          const resultElements = document.querySelectorAll('div.g, div.MjjYud, div[data-hveid]');
          const foundUrls: string[] = [];

          resultElements.forEach((el) => {
            const link = el.querySelector('a[href]');
            if (link) {
              const href = link.getAttribute('href');
              if (href && href.startsWith('http') && !href.includes('google.com')) {
                foundUrls.push(href);
              }
            }
          });

          // 检查是否有"没有结果"的提示
          const noResults = document.body.innerText.includes('did not match any documents') ||
                           document.body.innerText.includes('No results found for');

          results.push({
            type: 'indexing_check',
            isIndexed: !noResults && foundUrls.length > 0,
            resultCount: foundUrls.length,
            foundUrls: foundUrls.slice(0, 10),
            hasNoResultsIndicator: noResults,
          });

        } else {
          // 排名检查模式：提取搜索结果
          const resultElements = document.querySelectorAll('div.g, div.MjjYud');

          resultElements.forEach((el, index) => {
            if (index >= 20) return;

            const titleEl = el.querySelector('h3');
            const linkEl = el.querySelector('a[href]');
            const descEl = el.querySelector('div.VwiC3b, div.yXK7lf, div.IsZvec, div.MUxGbd');

            const title = titleEl ? titleEl.textContent?.trim() : '';
            const url = linkEl ? linkEl.getAttribute('href') : '';
            const description = descEl ? descEl.textContent?.trim() : '';

            if (title && url && url.startsWith('http') && !url.includes('google.com')) {
              results.push({
                rank: index + 1,
                title,
                url,
                description: description || '',
              });
            }
          });

          // 如果标准选择器没找到结果，尝试备用方法
          if (results.length === 0) {
            const allH3 = document.querySelectorAll('h3');
            const allLinks = document.querySelectorAll('a[href]');
            const filteredLinks = Array.from(allLinks)
              .map(a => a.getAttribute('href'))
              .filter(href => href && href.startsWith('http') && !href.includes('google.com') && !href.includes('gstatic.com'));

            allH3.forEach((h3, index) => {
              if (index >= 20) return;
              const title = h3.textContent?.trim();
              if (title && filteredLinks[index]) {
                results.push({
                  rank: index + 1,
                  title,
                  url: filteredLinks[index],
                  description: '',
                });
              }
            });
          }
        }

        return results;
      }, type);

      console.log(`[Google Search Puppeteer] Found ${results.length} results`);

      return NextResponse.json({
        success: true,
        query,
        type,
        resultCount: results.length,
        results,
        debug: {
          pageTitle,
          isCaptcha,
          contentLength: pageContent.length,
        },
      });

    } finally {
      // 关闭页面（但保留浏览器实例供下次使用）
      await page.close().catch(() => {});
      browserLastUsed = Date.now();
    }

  } catch (error: any) {
    console.error('[Google Search Puppeteer] Error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: error.message },
      { status: 500 }
    );
  }
}

/**
 * 获取或创建浏览器实例
 */
async function getBrowser() {
  try {
    // 检查缓存的浏览器实例是否仍然可用
    if (browserInstance && Date.now() - browserLastUsed < BROWSER_CACHE_TIME) {
      try {
        // 测试浏览器是否仍然连接
        const pages = await browserInstance.pages();
        if (pages) {
          console.log('[Google Search Puppeteer] Reusing cached browser instance');
          return browserInstance;
        }
      } catch (e) {
        console.log('[Google Search Puppeteer] Cached browser disconnected, creating new one');
        browserInstance = null;
      }
    }

    console.log('[Google Search Puppeteer] Launching new browser instance...');

    try {
      // 获取Chromium可执行文件路径
      const executablePath = await chromium.executablePath();
      console.log('[Google Search Puppeteer] Chromium executable path:', executablePath);
      console.log('[Google Search Puppeteer] Chromium args:', JSON.stringify(chromium.args));

      // 启动Chromium（使用@sparticuz/chromium，专为Serverless优化）
      browserInstance = await puppeteer.launch({
        args: [
          ...chromium.args,
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage',
          '--disable-gpu',
          '--no-first-run',
          '--no-zygote',
          '--single-process',
        ],
        defaultViewport: { width: 1920, height: 1080 },
        executablePath,
        headless: true,
      });

      browserLastUsed = Date.now();
      console.log('[Google Search Puppeteer] Browser launched successfully');

      return browserInstance;

    } catch (launchError: any) {
      console.error('[Google Search Puppeteer] Browser launch error details:', {
        message: launchError.message,
        stack: launchError.stack,
        name: launchError.name,
      });
      throw launchError;
    }

  } catch (error: any) {
    console.error('[Google Search Puppeteer] Failed to launch browser:', error);
    return null;
  }
}

// 支持GET请求（简单测试用）
export async function GET(request: NextRequest) {
  return NextResponse.json({
    service: 'Google Search Proxy (Puppeteer)',
    status: 'running',
    usage: 'POST with { "query": "search terms", "type": "indexing" | "ranking" }',
    auth: 'Bearer aitoolcrux-google-proxy-2026',
    note: 'Uses headless Chromium to render JavaScript-heavy Google search results',
  });
}
