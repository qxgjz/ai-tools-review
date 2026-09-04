import type { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      // 通用爬虫规则
      {
        userAgent: "*",
        allow: "/",
        disallow: [
          "/api/",
          "/_next/",
          "/admin",
          "/dashboard",
          "/account",
          "/settings",
          "/private",
        ],
      },
      // Google 爬虫特殊配置
      {
        userAgent: "Googlebot",
        allow: "/",
        crawlDelay: 1,
      },
      // Google 图片爬虫
      {
        userAgent: "Googlebot-Image",
        allow: "/",
      },
      // Bing 爬虫
      {
        userAgent: "Bingbot",
        allow: "/",
        crawlDelay: 1,
      },
      // 百度爬虫
      {
        userAgent: "Baiduspider",
        allow: "/",
        crawlDelay: 1,
      },
      // Yandex 爬虫
      {
        userAgent: "YandexBot",
        allow: "/",
        crawlDelay: 2,
      },
      // DuckDuckGo 爬虫
      {
        userAgent: "DuckDuckBot",
        allow: "/",
      },
      // 搜狗爬虫
      {
        userAgent: "Sogou Spider",
        allow: "/",
      },
      // 360爬虫
      {
        userAgent: "360Spider",
        allow: "/",
      },
      // AI 爬虫配置 - 允许主流AI爬虫访问内容（有助于AI搜索引用）
      {
        userAgent: "GPTBot",
        allow: "/",
        disallow: ["/api/", "/admin", "/private"],
      },
      {
        userAgent: "ClaudeBot",
        allow: "/",
        disallow: ["/api/", "/admin", "/private"],
      },
      {
        userAgent: "Claude-Web",
        allow: "/",
        disallow: ["/api/", "/admin", "/private"],
      },
      {
        userAgent: "PerplexityBot",
        allow: "/",
        disallow: ["/api/", "/admin", "/private"],
      },
      {
        userAgent: "Bytespider",
        allow: "/",
        disallow: ["/api/", "/admin", "/private"],
      },
      // 更多AI爬虫配置（有助于AI搜索和引用）
      {
        userAgent: "Google-Extended",
        allow: "/",
        disallow: ["/api/", "/admin", "/private"],
      },
      {
        userAgent: "Applebot",
        allow: "/",
        disallow: ["/api/", "/admin", "/private"],
      },
      {
        userAgent: "Amazonbot",
        allow: "/",
        disallow: ["/api/", "/admin", "/private"],
      },
      {
        userAgent: "meta-externalagent",
        allow: "/",
        disallow: ["/api/", "/admin", "/private"],
      },
      // 禁止恶意/资源消耗大的爬虫
      {
        userAgent: "AhrefsBot",
        disallow: ["/api/", "/_next/"],
        crawlDelay: 5,
      },
      {
        userAgent: "SemrushBot",
        disallow: ["/api/", "/_next/"],
        crawlDelay: 5,
      },
      {
        userAgent: "MJ12bot",
        disallow: ["/api/", "/_next/"],
        crawlDelay: 5,
      },
    ],
    sitemap: [
      "https://www.aitoolcrux.com/sitemap.xml",
    ],
    host: "www.aitoolcrux.com",
  };
}
