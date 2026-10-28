import type { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      // 通用爬虫规则
      {
        userAgent: '*',
        allow: '/',
        disallow: [
          '/api/',
          '/og/',
          '/cdn-cgi/',
          '/_next/',
          '/admin',
          '/dashboard',
          '/account',
          '/settings',
          '/private',
          // architect r68 (AUTO-REDIRECT-SPIKE-20261027): 屏蔽遗留 article-api 伪 URL 变体，
          // 防止 Google/Bing 继续发现并标记"自动重定向"（已由 _redirects 301 具体规则 + 410 兜底）
          '/blog/article-api-',
        ],
      },
      // Google 爬虫特殊配置
      {
        userAgent: 'Googlebot',
        allow: '/',
        disallow: ['/blog/article-api-'],
        crawlDelay: 1,
      },
      // Google 图片爬虫
      {
        userAgent: 'Googlebot-Image',
        allow: '/',
      },
      // Bing 爬虫
      {
        userAgent: 'Bingbot',
        allow: '/',
        disallow: ['/blog/article-api-'],
        crawlDelay: 1,
      },
      // 百度爬虫
      {
        userAgent: 'Baiduspider',
        allow: '/',
        crawlDelay: 1,
      },
      // Yandex 爬虫
      {
        userAgent: 'YandexBot',
        allow: '/',
        crawlDelay: 2,
      },
      // DuckDuckGo 爬虫
      {
        userAgent: 'DuckDuckBot',
        allow: '/',
      },
      // 搜狗爬虫
      {
        userAgent: 'Sogou Spider',
        allow: '/',
      },
      // 360爬虫
      {
        userAgent: '360Spider',
        allow: '/',
      },
      // AI 爬虫配置 - 允许主流AI爬虫访问内容（有助于AI搜索引用）
      {
        userAgent: 'GPTBot',
        allow: '/',
        disallow: ['/api/', '/og/', '/cdn-cgi/', '/admin', '/private'],
      },
      {
        userAgent: 'ClaudeBot',
        allow: '/',
        disallow: ['/api/', '/og/', '/cdn-cgi/', '/admin', '/private'],
      },
      {
        userAgent: 'Claude-Web',
        allow: '/',
        disallow: ['/api/', '/og/', '/cdn-cgi/', '/admin', '/private'],
      },
      {
        userAgent: 'PerplexityBot',
        allow: '/',
        disallow: ['/api/', '/og/', '/cdn-cgi/', '/admin', '/private'],
      },
      {
        userAgent: 'Bytespider',
        allow: '/',
        disallow: ['/api/', '/og/', '/cdn-cgi/', '/admin', '/private'],
      },
      // 更多AI爬虫配置（有助于AI搜索和引用）
      {
        userAgent: 'Google-Extended',
        allow: '/',
        disallow: ['/api/', '/og/', '/cdn-cgi/', '/admin', '/private'],
      },
      {
        userAgent: 'Applebot',
        allow: '/',
        disallow: ['/api/', '/og/', '/cdn-cgi/', '/admin', '/private'],
      },
      {
        userAgent: 'Amazonbot',
        allow: '/',
        disallow: ['/api/', '/og/', '/cdn-cgi/', '/admin', '/private'],
      },
      {
        userAgent: 'meta-externalagent',
        allow: '/',
        disallow: ['/api/', '/og/', '/cdn-cgi/', '/admin', '/private'],
      },
      // AI search/research crawlers added 2026-09-20 (GEO optimization)
      {
        userAgent: 'OAI-SearchBot',
        allow: '/',
        disallow: ['/api/', '/og/', '/cdn-cgi/', '/admin', '/private'],
      },
      {
        userAgent: 'ChatGPT-User',
        allow: '/',
        disallow: ['/api/', '/og/', '/cdn-cgi/', '/admin', '/private'],
      },
      {
        userAgent: 'Claude-SearchBot',
        allow: '/',
        disallow: ['/api/', '/og/', '/cdn-cgi/', '/admin', '/private'],
      },
      {
        userAgent: 'Claude-User',
        allow: '/',
        disallow: ['/api/', '/og/', '/cdn-cgi/', '/admin', '/private'],
      },
      {
        userAgent: 'Perplexity-User',
        allow: '/',
        disallow: ['/api/', '/og/', '/cdn-cgi/', '/admin', '/private'],
      },
      {
        userAgent: 'Applebot-Extended',
        allow: '/',
        disallow: ['/api/', '/og/', '/cdn-cgi/', '/admin', '/private'],
      },
      // 禁止恶意/资源消耗大的爬虫
      {
        userAgent: 'AhrefsBot',
        disallow: ['/api/', '/cdn-cgi/', '/_next/'],
        crawlDelay: 5,
      },
      {
        userAgent: 'SemrushBot',
        disallow: ['/api/', '/cdn-cgi/', '/_next/'],
        crawlDelay: 5,
      },
      {
        userAgent: 'MJ12bot',
        disallow: ['/api/', '/cdn-cgi/', '/_next/'],
        crawlDelay: 5,
      },
      // architect r28 (commander_cf_probe_2026-10-17): 高消耗采集/镜像爬虫限制
      // (保留全部 AI 搜索 bot 允许，GEO 不倒退)
      // architect r43 (analyst_20261021): CCBot 放行 llms 文件+博客目录——Common Crawl
      // 数据源影响 GPT 系训练语料可见性，博客内容为主 AI 引用来源；其余路径保持 Disallow
      // architect r74 (2026-10-29): GEO 审计发现 CCBot Disallow:/ 使全站除 llms/博客外不可见,
      // AI 可见性最大化 → 与其他 AI crawler 一致放开全站(allow:/ + 有限 disallow), 消除脚本 blocked 误报
      {
        userAgent: 'CCBot',
        allow: '/',
        disallow: ['/api/', '/og/', '/cdn-cgi/', '/admin', '/private'],
      },
      {
        userAgent: 'PetalBot', // 华为 Petal Search 采集
        disallow: ['/'],
      },
      {
        userAgent: 'SeznamBot', // Seznam 搜索引擎采集
        disallow: ['/'],
      },
      {
        userAgent: 'YisouSpider', // 神马/UC 采集
        disallow: ['/'],
      },
      {
        userAgent: 'facebookexternalhit', // FB 链接嗅探
        disallow: ['/'],
      },
      {
        userAgent: 'ia_archiver', // Internet Archive 镜像
        disallow: ['/'],
      },
      {
        userAgent: 'DotBot', // 邮件/爬虫探测
        disallow: ['/'],
      },
      {
        userAgent: 'MegaIndex.ru',
        disallow: ['/'],
      },
      {
        userAgent: 'Barkrowler', // 高消耗爬虫
        disallow: ['/'],
      },
    ],
    sitemap: ['https://www.aitoolcrux.com/sitemap.xml'],
    host: 'www.aitoolcrux.com',
    // NOTE: Google officially confirmed it does NOT use llms.txt (2026-08).
    // llms.txt remains available for non-Google AI crawlers (Claude, Perplexity, etc.)
    // but is no longer a priority for Google SEO. Do not invest further in llms.txt optimization.
    // https://www.aitoolcrux.com/llms.txt - Site overview for non-Google AI systems
    // https://www.aitoolcrux.com/llms-full.txt - Full content for LLM ingestion
  };
}
