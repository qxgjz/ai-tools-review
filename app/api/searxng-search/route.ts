import { NextRequest, NextResponse } from 'next/server';

/**
 * SearXNG 搜索代理 API
 * 通过多个公共 SearXNG 实例获取搜索结果，支持故障转移
 * 
 * 使用方法：
 * POST /api/searxng-search
 * Body: { "query": "site:https://www.aitoolcrux.com", "type": "indexing" | "ranking", "engines": "google" }
 * Headers: Authorization: Bearer aitoolcrux-searxng-proxy-2026
 */

// API密钥（防止滥用）
const PROXY_API_KEY = 'aitoolcrux-searxng-proxy-2026';

// 公共 SearXNG 实例列表（按优先级排序）
// 这些实例启用了 JSON 格式输出
const SEARXNG_INSTANCES = [
  'https://searx.be',
  'https://search.sapti.me',
  'https://searx.tiekoetter.com',
  'https://searx.work',
  'https://searx.ninja',
  'https://search.kael.ink',
  'https://baresearch.org',
  'https://searxng.site',
  'https://searx.fmac.xyz',
  'https://search.bus-hit.me',
];

// 实例健康状态缓存
const instanceHealth = new Map<string, { healthy: boolean; lastCheck: number; failCount: number }>();

// 健康检查间隔（5分钟）
const HEALTH_CHECK_INTERVAL = 5 * 60 * 1000;

// 最大失败次数（超过后暂时禁用该实例）
const MAX_FAIL_COUNT = 3;

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

    // 解析请求体
    const body = await request.json();
    const { query, type = 'ranking', engines = 'google', limit = 20, language = 'en' } = body;

    if (!query) {
      return NextResponse.json(
        { error: 'Missing query parameter' },
        { status: 400 }
      );
    }

    console.log(`[SearXNG] Query: ${query}, Type: ${type}, Engines: ${engines}`);

    // 获取健康的实例列表
    const healthyInstances = getHealthyInstances();
    console.log(`[SearXNG] Healthy instances: ${healthyInstances.length}/${SEARXNG_INSTANCES.length}`);

    if (healthyInstances.length === 0) {
      return NextResponse.json(
        { error: 'No healthy SearXNG instances available' },
        { status: 503 }
      );
    }

    // 尝试多个实例（故障转移）
    let results: any[] = [];
    let usedInstance = '';
    let errors: string[] = [];

    for (const instance of healthyInstances) {
      try {
        console.log(`[SearXNG] Trying instance: ${instance}`);
        
        const searchUrl = `${instance}/search?q=${encodeURIComponent(query)}&format=json&engines=${engines}&language=${language}`;
        
        const response = await fetch(searchUrl, {
          headers: {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
          },
          signal: AbortSignal.timeout(15000),
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        results = data.results || [];

        if (results.length > 0) {
          usedInstance = instance;
          markInstanceHealthy(instance);
          console.log(`[SearXNG] Success with ${instance}, got ${results.length} results`);
          break;
        } else {
          console.log(`[SearXNG] ${instance} returned empty results, trying next...`);
        }

      } catch (error: any) {
        const errorMsg = `${instance}: ${error.message}`;
        errors.push(errorMsg);
        console.log(`[SearXNG] Failed: ${errorMsg}`);
        markInstanceFailed(instance);
      }
    }

    if (results.length === 0) {
      return NextResponse.json(
        {
          error: 'All instances failed',
          errors,
          healthyInstances: healthyInstances.length,
        },
        { status: 502 }
      );
    }

    // 根据类型格式化结果
    let formattedResults: any[] = [];

    if (type === 'indexing') {
      // 收录检查模式
      const foundUrls = results
        .map((r: any) => r.url)
        .filter((url: string) => url && url.startsWith('http'));
      
      const totalResults = results.length;

      formattedResults.push({
        type: 'indexing_check',
        query,
        isIndexed: totalResults > 0,
        resultCount: foundUrls.length,
        totalResults,
        foundUrls: foundUrls.slice(0, 10),
        engines,
      });

    } else {
      // 排名检查模式
      formattedResults = results.map((item: any, index: number) => ({
        rank: index + 1,
        title: item.title || '',
        url: item.url || '',
        description: item.content || item.snippet || '',
        engine: item.engine || engines,
        score: item.score || 0,
        category: item.category || '',
      }));
    }

    return NextResponse.json({
      success: true,
      query,
      type,
      engines,
      resultCount: formattedResults.length,
      results: formattedResults,
      usedInstance,
      instanceCount: healthyInstances.length,
      errors: errors.slice(0, 3),
    });

  } catch (error: any) {
    console.error('[SearXNG] Error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: error.message },
      { status: 500 }
    );
  }
}

/**
 * 获取健康的实例列表
 */
function getHealthyInstances(): string[] {
  const now = Date.now();
  
  return SEARXNG_INSTANCES.filter(instance => {
    const health = instanceHealth.get(instance);
    
    if (!health) {
      return true; // 未检查过，默认健康
    }
    
    // 如果超过健康检查间隔，重置状态
    if (now - health.lastCheck > HEALTH_CHECK_INTERVAL) {
      return true;
    }
    
    // 如果失败次数超过最大值，暂时禁用
    if (health.failCount >= MAX_FAIL_COUNT) {
      return false;
    }
    
    return true;
  });
}

/**
 * 标记实例健康
 */
function markInstanceHealthy(instance: string) {
  instanceHealth.set(instance, {
    healthy: true,
    lastCheck: Date.now(),
    failCount: 0,
  });
}

/**
 * 标记实例失败
 */
function markInstanceFailed(instance: string) {
  const health = instanceHealth.get(instance) || {
    healthy: false,
    lastCheck: Date.now(),
    failCount: 0,
  };
  
  health.failCount += 1;
  health.lastCheck = Date.now();
  health.healthy = false;
  
  instanceHealth.set(instance, health);
}

// 支持GET请求（简单测试用）
export async function GET(request: NextRequest) {
  const healthyInstances = getHealthyInstances();
  
  return NextResponse.json({
    service: 'SearXNG Search Proxy',
    status: 'running',
    usage: 'POST with { "query": "search terms", "type": "indexing" | "ranking", "engines": "google" }',
    auth: 'Bearer aitoolcrux-searxng-proxy-2026',
    instances: {
      total: SEARXNG_INSTANCES.length,
      healthy: healthyInstances.length,
      list: SEARXNG_INSTANCES,
    },
  });
}
