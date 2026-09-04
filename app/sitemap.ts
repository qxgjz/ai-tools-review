import type { MetadataRoute } from "next";
import tools from "@/data/tools.json";
import posts from "@/data/posts.json";

// 网站基础 URL（部署后替换为你的域名）
const BASE_URL = "https://www.aitoolcrux.com";

export default function sitemap(): MetadataRoute.Sitemap {
  // 静态页面
  const staticPages: MetadataRoute.Sitemap = [
    {
      url: `${BASE_URL}/`,
      lastModified: new Date(),
      changeFrequency: "daily",
      priority: 1,
    },
    {
      url: `${BASE_URL}/ranking`,
      lastModified: new Date(),
      changeFrequency: "daily",
      priority: 0.95,
    },
    {
      url: `${BASE_URL}/compare`,
      lastModified: new Date(),
      changeFrequency: "weekly",
      priority: 0.85,
    },
    {
      url: `${BASE_URL}/generator`,
      lastModified: new Date(),
      changeFrequency: "monthly",
      priority: 0.7,
    },
    {
      url: `${BASE_URL}/search`,
      lastModified: new Date(),
      changeFrequency: "monthly",
      priority: 0.6,
    },
    {
      url: `${BASE_URL}/blog`,
      lastModified: new Date(),
      changeFrequency: "daily",
      priority: 0.9,
    },
    {
      url: `${BASE_URL}/about`,
      lastModified: new Date(),
      changeFrequency: "monthly",
      priority: 0.5,
    },
    {
      url: `${BASE_URL}/contact`,
      lastModified: new Date(),
      changeFrequency: "monthly",
      priority: 0.4,
    },
    {
      url: `${BASE_URL}/disclosure`,
      lastModified: new Date(),
      changeFrequency: "yearly",
      priority: 0.3,
    },
    {
      url: `${BASE_URL}/privacy`,
      lastModified: new Date(),
      changeFrequency: "yearly",
      priority: 0.3,
    },
    {
      url: `${BASE_URL}/terms`,
      lastModified: new Date(),
      changeFrequency: "yearly",
      priority: 0.3,
    },
  ];

  // 工具详情页
  const toolPages: MetadataRoute.Sitemap = tools.map((tool) => ({
    url: `${BASE_URL}/tools/${tool.slug}`,
    lastModified: new Date(tool.lastUpdated),
    changeFrequency: "weekly",
    priority: 0.8,
  }));

  // 分类页（从工具数据中提取唯一分类）
  const categories = [...new Set(tools.map((t) => t.category))];
  const categoryPages: MetadataRoute.Sitemap = categories.map((cat) => ({
    url: `${BASE_URL}/category/${cat}`,
    lastModified: new Date(),
    changeFrequency: "daily",
    priority: 0.7,
  }));

  // 博客文章页（根据文章类型设置不同优先级）
  const blogPages: MetadataRoute.Sitemap = posts.map((post) => {
    // 高优先级：评测文章和对比文章
    const isReview = post.title.toLowerCase().includes("review") || post.category?.toLowerCase().includes("review");
    const isComparison = post.title.toLowerCase().includes("vs") || post.title.toLowerCase().includes("comparison");
    const isGuide = post.title.toLowerCase().includes("guide") || post.title.toLowerCase().includes("best");
    
    let priority = 0.7;
    let changeFrequency: "always" | "hourly" | "daily" | "weekly" | "monthly" | "yearly" | "never" = "monthly";
    
    if (isReview) {
      priority = 0.85;
      changeFrequency = "weekly";
    } else if (isComparison) {
      priority = 0.8;
      changeFrequency = "weekly";
    } else if (isGuide) {
      priority = 0.75;
      changeFrequency = "monthly";
    }
    
    return {
      url: `${BASE_URL}/blog/${post.slug}`,
      lastModified: new Date(post.publishedAt),
      changeFrequency,
      priority,
    };
  });

  // 博客分类页
  const blogCategories = [...new Set(posts.map((p) => p.categorySlug).filter(Boolean))];
  const blogCategoryPages: MetadataRoute.Sitemap = blogCategories.map((cat) => ({
    url: `${BASE_URL}/blog/category/${cat}`,
    lastModified: new Date(),
    changeFrequency: "daily",
    priority: 0.65,
  }));

  // 博客标签页
  const allTags = [...new Set(posts.flatMap((p) => p.tagSlugs || []))];
  const blogTagPages: MetadataRoute.Sitemap = allTags.slice(0, 50).map((tag) => ({
    url: `${BASE_URL}/blog/tag/${tag}`,
    lastModified: new Date(),
    changeFrequency: "weekly",
    priority: 0.5,
  }));

  return [...staticPages, ...toolPages, ...categoryPages, ...blogPages, ...blogCategoryPages, ...blogTagPages];
}
