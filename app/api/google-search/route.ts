import { NextRequest, NextResponse } from 'next/server';

/**
 * Google搜索代理API
 * 解决中国大陆无法直接访问Google搜索的问题
 * 通过Vercel服务器代理访问Google搜索，返回结构化结果
 * 
 * 使用方法：
 * POST /api/google-search
 * Body: { "query": "site:https://www.aitoolcrux.com", "type": "indexing" | "ranking" }
 * Headers: Authorization: Bearer aitoolcrux-google-proxy-2026
 */

// API密钥（防止滥用）
const API_KEY = 'aitoolcrux-google-proxy-2026';

// Google搜索User-Agent
const GOOGLE_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';

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

    console.log(`[Google Search Proxy] Query: ${query}, Type: ${type}`);

    // 构建Google搜索URL - 使用移动版搜索（返回更简单的HTML）
    const searchUrl = `https://www.google.com/m/search?q=${encodeURIComponent(query)}&num=${num}&hl=en`;

    // 在Vercel服务器端访问Google搜索
    const response = await fetch(searchUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
      },
      redirect: 'follow',
      signal: AbortSignal.timeout(30000),
    });

    if (!response.ok) {
      console.error(`[Google Search Proxy] Google returned status: ${response.status}`);
      return NextResponse.json(
        { error: `Google search failed: ${response.status}` },
        { status: 502 }
      );
    }

    // 获取HTML内容
    const html = await response.text();

    // 调试：检查是否是验证码页面
    const isCaptcha = html.includes('captcha') || html.includes('Captcha') || 
                      html.includes('unusual traffic') || html.includes('sorry/index') ||
                      html.includes('Our systems have detected');

    console.log(`[Google Search Proxy] HTML length: ${html.length}, Is captcha: ${isCaptcha}`);

    // 解析搜索结果
    const results = parseGoogleResults(html, type, query);

    console.log(`[Google Search Proxy] Found ${results.length} results`);

    return NextResponse.json({
      success: true,
      query,
      type,
      resultCount: results.length,
      results,
      debug: {
        htmlLength: html.length,
        isCaptcha,
        htmlPreview: html.substring(0, 500),
        hasH3: html.includes('<h3'),
        hasResultDiv: html.includes('class="g"') || html.includes('MjjYud'),
      }
    });

  } catch (error: any) {
    console.error('[Google Search Proxy] Error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: error.message },
      { status: 500 }
    );
  }
}

/**
 * 解析Google搜索结果HTML
 */
function parseGoogleResults(html: string, type: string, query: string): any[] {
  const results: any[] = [];

  try {
    if (type === 'indexing') {
      // 收录检查模式：判断搜索结果中是否包含目标网站
      // 提取搜索结果中的所有链接
      const linkRegex = /<a[^>]+href="(https?:\/\/[^"]+)"[^>]*>/gi;
      let match;
      const links: string[] = [];

      while ((match = linkRegex.exec(html)) !== null) {
        const url = match[1];
        // 过滤掉Google自身的链接
        if (!url.includes('google.com') && !url.includes('gstatic.com') && !url.startsWith('https://www.google.')) {
          links.push(url);
        }
      }

      // 去重
      const uniqueLinks = [...new Set(links)];

      // 检查是否有"没有结果"的提示
      const noResultsIndicators = [
        'did not match any documents',
        'no results found',
        'No results found for',
        'Your search -',
        'did not match any search results',
      ];

      const hasNoResults = noResultsIndicators.some(indicator => 
        html.toLowerCase().includes(indicator.toLowerCase())
      );

      // 返回收录检查结果
      results.push({
        type: 'indexing_check',
        query,
        isIndexed: !hasNoResults && uniqueLinks.length > 0,
        resultCount: uniqueLinks.length,
        foundUrls: uniqueLinks.slice(0, 10),
        hasNoResultsIndicator: hasNoResults,
      });

    } else {
      // 排名检查模式：提取搜索结果的标题、链接、描述
      // Google搜索结果通常在 <div class="g"> 或 <div class="MjjYud"> 中
      // 使用更通用的正则表达式提取结果

      // 提取所有结果块
      const resultBlocks = html.match(/<div[^>]*class="[^"]*(?:g|MjjYud|hlcw0c)[^"]*"[^>]*>[\s\S]*?<\/div>\s*<\/div>/gi) || [];

      // 如果没找到标准结果块，使用备用方法提取链接和标题
      if (resultBlocks.length === 0) {
        // 提取所有h3标题（搜索结果标题通常是h3）
        const h3Regex = /<h3[^>]*>([\s\S]*?)<\/h3>/gi;
        const linkRegex = /<a[^>]+href="(https?:\/\/[^"]+)"[^>]*>/gi;

        let h3Match;
        let linkMatch;
        const titles: string[] = [];
        const links: string[] = [];

        while ((h3Match = h3Regex.exec(html)) !== null) {
          const title = h3Match[1].replace(/<[^>]*>/g, '').trim();
          if (title) titles.push(title);
        }

        while ((linkMatch = linkRegex.exec(html)) !== null) {
          const url = linkMatch[1];
          if (!url.includes('google.com') && !url.includes('gstatic.com') && !url.startsWith('https://www.google.')) {
            links.push(url);
          }
        }

        // 组合标题和链接
        const count = Math.min(titles.length, links.length, 20);
        for (let i = 0; i < count; i++) {
          results.push({
            rank: i + 1,
            title: titles[i],
            url: links[i],
            description: '',
          });
        }
      } else {
        // 解析标准结果块
        resultBlocks.forEach((block, index) => {
          if (index >= 20) return;

          // 提取标题
          const titleMatch = block.match(/<h3[^>]*>([\s\S]*?)<\/h3>/i);
          const title = titleMatch ? titleMatch[1].replace(/<[^>]*>/g, '').trim() : '';

          // 提取链接
          const linkMatch = block.match(/<a[^>]+href="(https?:\/\/[^"]+)"[^>]*>/i);
          const url = linkMatch ? linkMatch[1] : '';

          // 提取描述
          const descMatch = block.match(/<div[^>]*class="[^"]*(?:VwiC3b|yXK7lf|IsZvec)[^"]*"[^>]*>([\s\S]*?)<\/div>/i);
          const description = descMatch ? descMatch[1].replace(/<[^>]*>/g, '').trim() : '';

          if (title && url) {
            results.push({
              rank: index + 1,
              title,
              url,
              description,
            });
          }
        });
      }
    }

  } catch (parseError) {
    console.error('[Google Search Proxy] Parse error:', parseError);
  }

  return results;
}

// 支持GET请求（简单测试用）
export async function GET(request: NextRequest) {
  return NextResponse.json({
    service: 'Google Search Proxy',
    status: 'running',
    usage: 'POST with { "query": "search terms", "type": "indexing" | "ranking" }',
    auth: 'Bearer aitoolcrux-google-proxy-2026',
  });
}
