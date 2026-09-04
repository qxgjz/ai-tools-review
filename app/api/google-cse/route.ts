import { NextRequest, NextResponse } from 'next/server';

/**
 * Google Custom Search API代理
 * 使用Google官方Custom Search JSON API获取搜索结果
 * 
 * 配置方法：
 * 1. 在Google Cloud Console启用Custom Search API
 * 2. 创建可编程搜索引擎 (https://programmablesearchengine.google.com/)
 * 3. 获取API密钥和搜索引擎ID (CX)
 * 4. 在Vercel环境变量中配置:
 *    - GOOGLE_CSE_API_KEY
 *    - GOOGLE_CSE_CX
 * 
 * 使用方法：
 * POST /api/google-cse
 * Body: { "query": "site:https://www.aitoolcrux.com", "type": "indexing" | "ranking" }
 * Headers: Authorization: Bearer aitoolcrux-google-proxy-2026
 */

// API密钥（防止滥用）
const PROXY_API_KEY = 'aitoolcrux-google-proxy-2026';

// Google CSE配置（从环境变量读取）
const GOOGLE_CSE_API_KEY = process.env.GOOGLE_CSE_API_KEY || '';
const GOOGLE_CSE_CX = process.env.GOOGLE_CSE_CX || '';

export const maxDuration = 30;

export async function POST(request: NextRequest) {
  try {
    // 验证代理API密钥
    const authHeader = request.headers.get('authorization');
    if (!authHeader || authHeader !== `Bearer ${PROXY_API_KEY}`) {
      return NextResponse.json(
        { error: 'Unauthorized', message: 'Invalid API key' },
        { status: 401 }
      );
    }

    // 检查Google CSE配置
    if (!GOOGLE_CSE_API_KEY || !GOOGLE_CSE_CX) {
      return NextResponse.json(
        {
          error: 'Google CSE not configured',
          message: 'Please configure GOOGLE_CSE_API_KEY and GOOGLE_CSE_CX environment variables',
          setupGuide: {
            step1: 'Go to Google Cloud Console → APIs & Services → Enable Custom Search JSON API',
            step2: 'Go to https://programmablesearchengine.google.com/ → Create a new search engine',
            step3: 'Get API key from Google Cloud Console → Credentials',
            step4: 'Get Search engine ID (CX) from Programmable Search Engine settings',
            step5: 'Add to Vercel environment variables: GOOGLE_CSE_API_KEY and GOOGLE_CSE_CX',
          },
        },
        { status: 503 }
      );
    }

    // 解析请求体
    const body = await request.json();
    const { query, type = 'indexing', num = 10 } = body;

    if (!query) {
      return NextResponse.json(
        { error: 'Missing query parameter' },
        { status: 400 }
      );
    }

    console.log(`[Google CSE] Query: ${query}, Type: ${type}`);

    // 调用Google Custom Search API
    const cseUrl = `https://www.googleapis.com/customsearch/v1?key=${GOOGLE_CSE_API_KEY}&cx=${GOOGLE_CSE_CX}&q=${encodeURIComponent(query)}&num=${num}`;

    const response = await fetch(cseUrl, {
      headers: {
        'Accept': 'application/json',
      },
      signal: AbortSignal.timeout(20000),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`[Google CSE] API error: ${response.status}`, errorText);
      return NextResponse.json(
        { error: `Google CSE API error: ${response.status}`, details: errorText },
        { status: 502 }
      );
    }

    const data = await response.json();

    // 解析搜索结果
    const items = data.items || [];
    const searchInformation = data.searchInformation || {};

    console.log(`[Google CSE] Found ${items.length} results, totalResults: ${searchInformation.totalResults}`);

    // 根据类型格式化结果
    let results: any[] = [];

    if (type === 'indexing') {
      // 收录检查模式
      const foundUrls = items.map((item: any) => item.link).filter(Boolean);
      const totalResults = parseInt(searchInformation.totalResults || '0', 10);

      results.push({
        type: 'indexing_check',
        query,
        isIndexed: totalResults > 0 || foundUrls.length > 0,
        resultCount: foundUrls.length,
        totalResults,
        foundUrls: foundUrls.slice(0, 10),
        searchTime: searchInformation.searchTime,
      });

    } else {
      // 排名检查模式
      results = items.map((item: any, index: number) => ({
        rank: index + 1,
        title: item.title || '',
        url: item.link || '',
        description: item.snippet || '',
        displayLink: item.displayLink || '',
        htmlFormattedUrl: item.htmlFormattedUrl || '',
        pagemap: item.pagemap || {},
      }));
    }

    return NextResponse.json({
      success: true,
      query,
      type,
      resultCount: results.length,
      results,
      searchInformation: {
        totalResults: searchInformation.totalResults,
        searchTime: searchInformation.searchTime,
        formattedTotalResults: searchInformation.formattedTotalResults,
        formattedSearchTime: searchInformation.formattedSearchTime,
      },
    });

  } catch (error: any) {
    console.error('[Google CSE] Error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: error.message },
      { status: 500 }
    );
  }
}

// 支持GET请求（简单测试用）
export async function GET(request: NextRequest) {
  return NextResponse.json({
    service: 'Google Custom Search API Proxy',
    status: GOOGLE_CSE_API_KEY && GOOGLE_CSE_CX ? 'configured' : 'not_configured',
    usage: 'POST with { "query": "search terms", "type": "indexing" | "ranking" }',
    auth: 'Bearer aitoolcrux-google-proxy-2026',
    setupRequired: !GOOGLE_CSE_API_KEY || !GOOGLE_CSE_CX,
  });
}
