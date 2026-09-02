import type { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: "*",
        allow: "/",
        disallow: ["/api/", "/_next/"],
      },
      // Google 爬虫特殊配置
      {
        userAgent: "Googlebot",
        allow: "/",
        crawlDelay: 1,
      },
      // 百度爬虫
      {
        userAgent: "Baiduspider",
        allow: "/",
      },
    ],
    sitemap: "https://www.aitoolcrux.com/sitemap.xml",
    // 搜索引擎验证（替换为你的验证代码）
    // host: "www.aitoolcrux.com",
  };
}
