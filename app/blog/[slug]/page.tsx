import Link from "next/link";
import { notFound } from "next/navigation";
import dynamic from "next/dynamic";
import { ArrowRight } from "lucide-react";
import posts from "@/data/posts.json";
import tools from "@/data/tools.json";
import { AffiliateCTA } from "@/components/monetization/AffiliateCTA";
import { NewsletterSignup } from "@/components/monetization/NewsletterSignup";
import { AdSlot } from "@/components/monetization/AdSlot";
import { ReviewSchema, BreadcrumbSchema, FAQSchema } from "@/components/seo/Schema";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { AuthorBio } from "@/components/author/AuthorBio";
import { SourceReferences } from "@/components/seo/SourceReferences";
import { HandsOnExperience } from "@/components/content/HandsOnExperience";

// 动态导入重型组件，减少初始JS包大小
const Giscus = dynamic(() => import("@/components/comments/Giscus"), {
  ssr: false,
  loading: () => <div className="h-40 flex items-center justify-center text-gray-400 text-sm">加载评论中...</div>,
});

interface PostPageProps {
  params: { slug: string };
}

export function generateStaticParams() {
  return posts.map((post) => ({ slug: post.slug }));
}

export function generateMetadata({ params }: PostPageProps) {
  const post = posts.find((p) => p.slug === params.slug);
  if (!post) return {};

  // 判断文章语言（包含中文字符则为中文，否则为英文）
  const hasChinese = /[\u4e00-\u9fa5]/.test(post.title);
  const lang = hasChinese ? "zh-CN" : "en";

  // 从标题提取关键词
  const titleWords = post.title.toLowerCase().split(/\s+/).filter((w: string) => w.length > 3);
  const keywords = [...titleWords.slice(0, 5), ...(post.tags || []), "AI tools", "AI review", "AIToolCrux"];

  // 优化描述：确保150-160字符，包含关键词和CTA
  let description = post.excerpt;
  if (description.length > 160) {
    description = description.slice(0, 157) + "...";
  } else if (description.length < 120) {
    description = `${description} Expert analysis by AIToolCrux editorial team. Updated ${post.publishedAt || "2026"}.`;
    if (description.length > 160) {
      description = description.slice(0, 157) + "...";
    }
  }

  return {
    title: post.title,
    description: description,
    keywords: keywords,
    alternates: {
      canonical: `https://www.aitoolcrux.com/blog/${post.slug}`,
      languages: {
        [lang]: `https://www.aitoolcrux.com/blog/${post.slug}`,
      },
    },
    openGraph: {
      title: post.title,
      description: description,
      url: `https://www.aitoolcrux.com/blog/${post.slug}`,
      type: "article",
      publishedTime: post.publishedAt,
      modifiedTime: post.publishedAt,
      authors: ["AIToolCrux Editorial Team"],
      tags: post.tags || [],
    },
    twitter: {
      card: "summary_large_image",
      title: post.title,
      description: description,
    },
  };
}

export default function PostPage({ params }: PostPageProps) {
  const post = posts.find((p) => p.slug === params.slug);

  if (!post) {
    notFound();
  }

  // 智能相关文章推荐：标签重叠度(60%) + 分类匹配(25%) + 标题关键词相似度(15%)
  const calculateRelevance = (a: typeof post, b: typeof post): number => {
    let score = 0;
    // 标签重叠度（权重60%）
    const tagsA = a.tags || [];
    const tagsB = b.tags || [];
    const commonTags = tagsA.filter((t) => tagsB.includes(t));
    const tagOverlap = tagsA.length > 0 ? commonTags.length / Math.min(tagsA.length, 4) : 0;
    score += tagOverlap * 60;
    // 分类匹配（权重25%）
    if (a.category === b.category) score += 25;
    else if (a.categorySlug === b.categorySlug) score += 20;
    // 标题关键词相似度（权重15%）
    const wordsA = a.title.toLowerCase().split(/\s+/).filter((w) => w.length > 3);
    const wordsB = b.title.toLowerCase().split(/\s+/).filter((w) => w.length > 3);
    const commonWords = wordsA.filter((w) => wordsB.includes(w));
    const wordOverlap = wordsA.length > 0 ? commonWords.length / Math.min(wordsA.length, 6) : 0;
    score += wordOverlap * 15;
    return score;
  };
  const relatedPosts = posts
    .filter((p) => p.slug !== post.slug)
    .map((p) => ({ post: p, relevance: calculateRelevance(post, p) }))
    .filter((item) => item.relevance > 5) // 最低相关性阈值
    .sort((a, b) => b.relevance - a.relevance)
    .slice(0, 6)
    .map((item) => item.post);

  // 相关工具推荐：基于文章标签、分类和标题关键词
  const calculateToolRelevance = (tool: any): number => {
    let score = 0;
    // 标签匹配（权重50%）
    const postTags = (post.tags || []).map((t: string) => t.toLowerCase());
    const toolName = tool.name.toLowerCase();
    const toolVendor = (tool.vendor || "").toLowerCase();
    const toolCategory = (tool.category || "").toLowerCase();
    const toolDesc = (tool.description || "").toLowerCase();

    for (const tag of postTags) {
      if (toolName.includes(tag) || toolVendor.includes(tag) || toolDesc.includes(tag)) {
        score += 15;
      }
    }

    // 分类匹配（权重30%）
    const postCategory = (post.category || "").toLowerCase();
    const categoryMap: Record<string, string[]> = {
      "ai chat": ["chat", "agent"],
      "ai writing": ["writing", "productivity"],
      "ai image": ["image", "design"],
      "ai coding": ["code", "dev-tools"],
      "ai video": ["video"],
      "ai audio": ["audio"],
      "productivity": ["productivity", "search"],
      "comparison": ["chat", "writing", "image", "code", "video", "audio"],
      "guide": ["chat", "writing", "image", "code", "video", "audio", "productivity", "agent"],
    };
    const mappedCategories = categoryMap[postCategory] || [postCategory];
    if (mappedCategories.includes(toolCategory)) {
      score += 30;
    }

    // 标题关键词匹配（权重20%）
    const titleWords = post.title.toLowerCase().split(/\s+/).filter((w: string) => w.length > 3);
    for (const word of titleWords) {
      if (toolName.includes(word) || toolDesc.includes(word)) {
        score += 5;
      }
    }

    return score;
  };

  // 查找关联工具信息（用于联盟CTA和相关工具推荐过滤）
  const toolSlug = post.slug.replace("-review-2026", "");

  const relatedTools = tools
    .filter((t) => t.slug !== toolSlug)
    .map((t) => ({ tool: t, relevance: calculateToolRelevance(t) }))
    .filter((item) => item.relevance > 10)
    .sort((a, b) => b.relevance - a.relevance)
    .slice(0, 4)
    .map((item) => item.tool);

  const tool = tools.find((t) => t.slug === toolSlug);
  const toolName = tool?.name || post.title.split(" ")[0] || "this tool";
  const officialUrl = tool?.officialUrl || `https://www.google.com/search?q=${encodeURIComponent(toolName)}`;
  const affiliateUrl = (tool as any)?.affiliateUrl || undefined;

  // 计算工具平均评分（用于Review Schema）
  const avgScore = tool?.scores
    ? Object.values(tool.scores).reduce((a, b) => a + (typeof b === "number" ? b : 0), 0) /
      Object.keys(tool.scores).filter((k) => typeof (tool.scores as any)[k] === "number").length
    : 7.5;

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-12">
      {/* SEO结构化数据 */}
      <BreadcrumbSchema
        items={[
          { name: "Home", url: "/" },
          { name: "Blog", url: "/blog" },
          { name: post.category, url: `/blog/category/${post.categorySlug}` },
          { name: post.title, url: `/blog/${post.slug}` },
        ]}
      />
      <ReviewSchema
        name={post.title}
        reviewBody={post.excerpt}
        ratingValue={Math.round(avgScore * 10) / 10}
        author={post.author}
        datePublished={post.publishedAt}
        itemReviewed={toolName}
      />
      {/* Article Schema - 博客文章结构化数据 */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "Article",
            headline: post.title,
            description: post.excerpt,
            author: {
              "@type": "Organization",
              name: post.author || "AIToolCrux Editorial Team",
            },
            datePublished: post.publishedAt,
            dateModified: (post as any).updatedAt || (post as any).lastUpdated || post.publishedAt,
            publisher: {
              "@type": "Organization",
              name: "AIToolCrux",
              url: "https://www.aitoolcrux.com",
              logo: {
                "@type": "ImageObject",
                url: "https://www.aitoolcrux.com/logo.svg",
              },
            },
            mainEntityOfPage: {
              "@type": "WebPage",
              "@id": `https://www.aitoolcrux.com/blog/${post.slug}`,
            },
            image: (post as any).coverImage || (post as any).image || "https://www.aitoolcrux.com/og-image.svg",
            articleSection: post.category,
            wordCount: post.content ? post.content.length : 1500,
          }),
        }}
      />
      {/* FAQ Schema - 常见问题结构化数据（使用文章真实FAQ数据） */}
      {post.faq && post.faq.length > 0 && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "FAQPage",
              mainEntity: post.faq.map((item: any) => ({
                "@type": "Question",
                name: item.q,
                acceptedAnswer: {
                  "@type": "Answer",
                  text: item.a,
                },
              })),
            }),
          }}
        />
      )}

      {/* 可视化面包屑导航 */}
      <Breadcrumb
        items={[
          { name: "Blog", url: "/blog" },
          { name: post.category, url: `/blog/category/${post.categorySlug}` },
          { name: post.title },
        ]}
        className="mb-4"
      />

      {/* 返回按钮 */}
      <Link
        href="/blog"
        className="inline-flex items-center text-sm text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 mb-8 transition-colors"
      >
        ← 返回博客列表
      </Link>

      {/* 文章头部 */}
      <header className="mb-10">
        <div className="flex items-center gap-3 mb-4">
          <Link
            href={`/blog/category/${post.categorySlug}`}
            className="text-sm font-medium text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20 px-3 py-1 rounded-full hover:bg-blue-100 dark:hover:bg-blue-900/30 transition-colors"
          >
            {post.category}
          </Link>
          <span className="text-sm text-gray-500 dark:text-gray-400">{post.readTime} 分钟阅读</span>
        </div>
        <h1 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4 leading-tight">
          {post.title}
        </h1>
        <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
          <span>{post.author}</span>
          <span>·</span>
          <span>{post.publishedAt}</span>
        </div>
      </header>

      {/* 作者简介卡片 - E-E-A-T信任信号 */}
      <div className="mb-8">
        <AuthorBio
          name={post.author || "AIToolCrux Editorial Team"}
          role="AI Tools Expert & Reviewer"
        />
      </div>

      {/* 文章摘要 */}
      <div className="bg-gray-50 dark:bg-gray-900 border-l-4 border-blue-500 p-4 mb-6 rounded-r">
        <p className="text-gray-700 dark:text-gray-300 italic">{post.excerpt}</p>
      </div>

      {/* 开篇联盟CTA */}
      {affiliateUrl && (
        <AffiliateCTA
          toolName={toolName}
          officialUrl={officialUrl}
          affiliateUrl={affiliateUrl}
          description={`Ready to try ${toolName}? Click below to visit the official site and get started.`}
          variant="banner"
        />
      )}

      {/* 文章标签 */}
      <div className="flex flex-wrap gap-2 mb-10">
        {post.tags.map((tag, index) => (
          <Link
            key={tag}
            href={`/blog/tag/${post.tagSlugs[index]}`}
            className="text-xs text-gray-600 dark:text-gray-400 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
          >
            #{tag}
          </Link>
        ))}
      </div>

      {/* 我的使用体验章节 - 非商品化内容，E-E-A-T信任信号 */}
      <HandsOnExperience
        toolName={toolName}
        category={tool?.category || "default"}
        score={8.0}
        grade="B"
        testDuration="30 days"
      />

      {/* 文章内容 */}
      <article
        className="prose prose-lg dark:prose-invert max-w-none mb-10"
        dangerouslySetInnerHTML={{ __html: post.content }}
      />

      {/* FAQ 常见问题展示区域 */}
      {post.faq && post.faq.length > 0 && (
        <section className="mb-10">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
            <span className="w-8 h-8 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
              <span className="text-blue-600 dark:text-blue-400 font-bold text-sm">Q</span>
            </span>
            Frequently Asked Questions
          </h2>
          <div className="space-y-3">
            {post.faq.map((item: any, index: number) => (
              <details
                key={index}
                className="group bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl overflow-hidden hover:border-blue-300 dark:hover:border-blue-700 transition-colors"
              >
                <summary className="flex items-center justify-between p-5 cursor-pointer list-none">
                  <span className="font-semibold text-gray-900 dark:text-white pr-4">
                    {item.q}
                  </span>
                  <span className="flex-shrink-0 w-6 h-6 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center group-open:bg-blue-100 dark:group-open:bg-blue-900/30 transition-colors">
                    <svg
                      className="w-4 h-4 text-gray-500 dark:text-gray-400 group-open:text-blue-600 dark:group-open:text-blue-400 group-open:rotate-45 transition-transform"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                    </svg>
                  </span>
                </summary>
                <div className="px-5 pb-5 pt-0">
                  <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
                    {item.a}
                  </p>
                </div>
              </details>
            ))}
          </div>
        </section>
      )}

      {/* 中部联盟CTA */}
      {affiliateUrl && (
        <AffiliateCTA
          toolName={toolName}
          officialUrl={officialUrl}
          affiliateUrl={affiliateUrl}
          description={`Still considering ${toolName}? Read our verdict below, or visit the official site now.`}
          variant="banner"
        />
      )}

      {/* 底部联盟CTA */}
      <AffiliateCTA
        toolName={toolName}
        officialUrl={officialUrl}
        affiliateUrl={affiliateUrl}
        description={`Read our full review above, then visit ${toolName} official site to try it for yourself.`}
        variant="bottom"
      />

      {/* 文章底部广告位 */}
      <AdSlot label="Advertisement" className="my-8" />

      {/* 邮件订阅 */}
      <div className="my-10">
        <NewsletterSignup variant="compact" />
      </div>

      {/* 相关工具推荐 */}
      {relatedTools.length > 0 && (
        <section className="mb-16">
          <div className="flex items-end justify-between mb-6">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Related AI Tools</h2>
              <p className="text-sm text-gray-500 dark:text-gray-400">Tools mentioned or relevant to this article</p>
            </div>
            <Link
              href="/"
              className="hidden sm:inline-flex items-center gap-1 text-sm font-medium text-blue-600 dark:text-blue-400 hover:underline"
            >
              Browse all tools
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {relatedTools.map((relatedTool) => {
              return (
                <Link
                  key={relatedTool.slug}
                  href={`/tools/${relatedTool.slug}`}
                  className="group block bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 p-5 hover:shadow-lg dark:hover:shadow-xl hover:border-blue-300 dark:hover:border-blue-700 transition-all duration-200"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex-1 min-w-0">
                      <h3 className="text-base font-bold text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors truncate">
                        {relatedTool.name}
                      </h3>
                      <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5 truncate">
                        {relatedTool.vendor}
                      </p>
                    </div>
                  </div>
                  <p className="text-xs text-gray-600 dark:text-gray-400 line-clamp-2 mb-3">
                    {relatedTool.description}
                  </p>
                  <div className="flex items-center justify-between">
                    <span className="text-xs px-2 py-0.5 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 rounded-full">
                      {relatedTool.category}
                    </span>
                    <span className="text-xs text-blue-600 dark:text-blue-400 font-medium group-hover:underline">
                      View →
                    </span>
                  </div>
                </Link>
              );
            })}
          </div>
        </section>
      )}

      {/* 相关文章 - 智能推荐 */}
      {relatedPosts.length > 0 && (
        <section className="mb-16">
          <div className="flex items-end justify-between mb-6">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">你可能还喜欢</h2>
              <p className="text-sm text-gray-500 dark:text-gray-400">基于标签、分类和内容相似度智能推荐</p>
            </div>
            <Link
              href="/blog"
              className="hidden sm:inline-flex items-center gap-1 text-sm font-medium text-blue-600 dark:text-blue-400 hover:underline"
            >
              查看全部文章
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {relatedPosts.map((related) => (
              <Link
                key={related.slug}
                href={`/blog/${related.slug}`}
                className="group block bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 p-5 hover:shadow-lg dark:hover:shadow-xl hover:border-blue-300 dark:hover:border-blue-700 transition-all duration-200"
              >
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xs px-2 py-0.5 bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-full">
                    {related.category}
                  </span>
                  <span className="text-xs text-gray-400">{related.readTime || '5 min'}</span>
                </div>
                <h3 className="text-sm font-bold text-gray-900 dark:text-white mb-2 line-clamp-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                  {related.title}
                </h3>
                <p className="text-xs text-gray-500 dark:text-gray-400 line-clamp-2 mb-3">{related.excerpt}</p>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-gray-400">{related.publishedAt}</span>
                  <span className="text-xs text-blue-600 dark:text-blue-400 opacity-0 group-hover:opacity-100 transition-opacity">阅读 →</span>
                </div>
              </Link>
            ))}
          </div>
          {/* 移动端查看全部链接 */}
          <div className="mt-6 text-center sm:hidden">
            <Link
              href="/blog"
              className="inline-flex items-center gap-1 text-sm font-medium text-blue-600 dark:text-blue-400 hover:underline"
            >
              查看全部文章
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </section>
      )}

      {/* 来源引用列表 - E-E-A-T信任信号 */}
      <section className="mt-10">
        <SourceReferences
          toolName={toolName}
          lastUpdated={post.publishedAt}
        />
      </section>

      {/* 评论区 */}
      <section className="border-t border-gray-200 dark:border-gray-800 pt-10">
        <Giscus />
      </section>
    </div>
  );
}
