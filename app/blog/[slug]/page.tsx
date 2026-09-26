import Link from 'next/link';
import { notFound } from 'next/navigation';
import nextDynamic from 'next/dynamic';
import {
  ArrowRight,
  Image as ImageIcon,
  Zap,
  BookOpen,
  CheckCircle2,
  Star,
  Lightbulb,
  Award,
} from 'lucide-react';
import posts from '@/data/posts.json';
import tools from '@/data/tools.json';
import { AffiliateCTA } from '@/components/monetization/AffiliateCTA';
import { NewsletterSignup } from '@/components/monetization/NewsletterSignup';
import { AdSlot } from '@/components/monetization/AdSlot';
import { ReviewSchema, BreadcrumbSchema, ComparisonSchema } from '@/components/seo/Schema';
import { Breadcrumb } from '@/components/ui/Breadcrumb';
import { AuthorBio } from '@/components/author/AuthorBio';
import { SourceReferences } from '@/components/seo/SourceReferences';
import { HandsOnExperience } from '@/components/content/HandsOnExperience';
import { FAQSection, defaultFAQs } from '@/components/content/FAQSection';
import { ToolScreenshot } from '@/components/content/ToolScreenshot';
import { ReadingProgress } from '@/components/blog/ReadingProgress';
import { TableOfContents } from '@/components/blog/TableOfContents';
import { PostNavigation } from '@/components/blog/PostNavigation';
import { markdownToHtmlSafe } from '@/lib/markdown';

// 动态Import重型Component，减少初始JS包大小
const Giscus = nextDynamic(() => import('@/components/comments/Giscus'), {
  ssr: false,
  loading: () => (
    <div className="h-40 flex items-center justify-center text-gray-400 text-sm">
      Loading comments...
    </div>
  ),
});

// Helper: convert tag name to URL-friendly slug
function slugifyTag(name: string): string {
  return name
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-');
}
const ReviewTabs = nextDynamic(() => import('@/components/content/ReviewTabs'), {
  ssr: false,
  loading: () => (
    <div className="h-40 flex items-center justify-center text-gray-400 text-sm">
      Loading scores...
    </div>
  ),
});

interface PostPageProps {
  params: { slug: string };
}

export const dynamicParams = false;

export const dynamic = 'force-static';

export function generateStaticParams() {
  return posts.map((post) => ({ slug: post.slug }));
}

// Truncate text at word boundary for SEO-friendly titles and descriptions
function truncateAtWord(text: string, maxLen: number): string {
  if (text.length <= maxLen) return text;
  const truncated = text.slice(0, maxLen - 3);
  const lastSpace = truncated.lastIndexOf(' ');
  const result = lastSpace > maxLen * 0.6 ? truncated.slice(0, lastSpace) : truncated;
  return result.replace(/[\s,;:\-–—]+$/, '') + '...';
}

export function generateMetadata({ params }: PostPageProps) {
  const post = posts.find((p) => p.slug === params.slug);
  if (!post) return {};

  // 判断文章语言（包含中文字符则为中文，否则为英文）
  const hasChinese = /[\u4e00-\u9fa5]/.test(post.title);
  const lang = hasChinese ? 'zh-CN' : 'en';

  // 从标题提取关键词
  const titleWords = post.title
    .toLowerCase()
    .split(/\s+/)
    .filter((w: string) => w.length > 3);
  const keywords = [
    ...titleWords.slice(0, 5),
    ...(post.tags || []),
    'AI tools',
    'AI review',
    'AIToolCrux',
  ];

  // 优化描述：确保150-160字符，包含关键词和CTA
  let description = post.excerpt || post.description || '';
  // Strip HTML tags from description
  description = description.replace(/<[^>]+>/g, '').trim();
  if (description.length > 155) {
    description = truncateAtWord(description, 155);
  } else if (description.length < 120) {
    description = `${description} Expert analysis by AIToolCrux. Updated ${(post.date || post.publishedAt || '2026').slice(0, 10)}.`;
    if (description.length > 155) {
      description = truncateAtWord(description, 155);
    }
  }

  return {
    title: truncateAtWord(post.title, 60),
    description: description,
    keywords: keywords,
    alternates: {
      canonical: `https://www.aitoolcrux.com/blog/${post.slug}`,
      languages: {
        [lang]: `https://www.aitoolcrux.com/blog/${post.slug}`,
      },
    },
    openGraph: {
      title: truncateAtWord(post.title, 60),
      description: description,
      url: `https://www.aitoolcrux.com/blog/${post.slug}`,
      type: 'article',
      publishedTime: post.date || post.publishedAt,
      modifiedTime: post.date || post.publishedAt,
      authors: ['AIToolCrux Editorial Team'],
      tags: post.tags || [],
      siteName: 'AIToolCrux',
      images: [
        {
          url: `https://www.aitoolcrux.com/api/og?title=${encodeURIComponent(post.title.slice(0, 50))}&description=${encodeURIComponent(description.slice(0, 100))}&category=${encodeURIComponent(post.category || 'AI Tools')}`,
          width: 1200,
          height: 630,
          alt: post.title,
        },
      ],
    },
    twitter: {
      card: 'summary_large_image',
      title: truncateAtWord(post.title, 60),
      description: description,
      images: [
        `https://www.aitoolcrux.com/api/og?title=${encodeURIComponent(post.title.slice(0, 50))}&description=${encodeURIComponent(description.slice(0, 100))}&category=${encodeURIComponent(post.category || 'AI Tools')}`,
      ],
    },
  };
}

export default function PostPage({ params }: PostPageProps) {
  const post = posts.find((p) => p.slug === params.slug);

  if (!post) {
    notFound();
  }

  // 智能Related Articles推荐：Tags重叠度(60%) + Categories匹配(25%) + 标题关键词相似度(15%)
  const calculateRelevance = (a: typeof post, b: typeof post): number => {
    let score = 0;
    // Tags重叠度（权重60%）
    const tagsA = a.tags || [];
    const tagsB = b.tags || [];
    const commonTags = tagsA.filter((t) => tagsB.includes(t));
    const tagOverlap = tagsA.length > 0 ? commonTags.length / Math.min(tagsA.length, 4) : 0;
    score += tagOverlap * 60;
    // Categories匹配（权重25%）
    if (a.category === b.category) score += 25;
    else if (a.categorySlug === b.categorySlug) score += 20;
    // 标题关键词相似度（权重15%）
    const wordsA = a.title
      .toLowerCase()
      .split(/\s+/)
      .filter((w) => w.length > 3);
    const wordsB = b.title
      .toLowerCase()
      .split(/\s+/)
      .filter((w) => w.length > 3);
    const commonWords = wordsA.filter((w) => wordsB.includes(w));
    const wordOverlap = wordsA.length > 0 ? commonWords.length / Math.min(wordsA.length, 6) : 0;
    score += wordOverlap * 15;
    return score;
  };
  const relatedPosts = posts
    .filter((p) => p.slug !== post.slug)
    .map((p) => ({ post: p, relevance: calculateRelevance(post, p) }))
    .filter((item) => item.relevance > 2) // 最低相关性阈值
    .sort((a, b) => b.relevance - a.relevance)
    .slice(0, 6)
    .map((item) => item.post);

  // 相关Tools推荐：基于Tags、Categories和标题关键词
  const calculateToolRelevance = (tool: any): number => {
    let score = 0;
    // Tags匹配（权重50%）
    const postTags = (post.tags || []).map((t: string) => t.toLowerCase());
    const toolName = tool.name.toLowerCase();
    const toolVendor = (tool.vendor || '').toLowerCase();
    const toolCategory = (tool.category || '').toLowerCase();
    const toolDesc = (tool.description || '').toLowerCase();

    for (const tag of postTags) {
      if (toolName.includes(tag) || toolVendor.includes(tag) || toolDesc.includes(tag)) {
        score += 15;
      }
    }

    // Categories匹配（权重30%）
    const postCategory = (post.category || '').toLowerCase();
    const categoryMap: Record<string, string[]> = {
      'ai chat': ['chat', 'agent'],
      'ai writing': ['writing', 'productivity'],
      'ai image': ['image', 'design'],
      'ai coding': ['code', 'dev-tools'],
      'ai video': ['video'],
      'ai audio': ['audio'],
      productivity: ['productivity', 'search'],
      comparison: ['chat', 'writing', 'image', 'code', 'video', 'audio'],
      guide: ['chat', 'writing', 'image', 'code', 'video', 'audio', 'productivity', 'agent'],
    };
    const mappedCategories = categoryMap[postCategory] || [postCategory];
    if (mappedCategories.includes(toolCategory)) {
      score += 30;
    }

    // 标题关键词匹配（权重20%）
    const titleWords = post.title
      .toLowerCase()
      .split(/\s+/)
      .filter((w: string) => w.length > 3);
    for (const word of titleWords) {
      if (toolName.includes(word) || toolDesc.includes(word)) {
        score += 5;
      }
    }

    return score;
  };

  // 查找关联Tools信息（用于联盟CTA和相关Tools推荐过滤）
  const toolSlug = post.slug.replace('-review-2026', '');

  const relatedTools = tools
    .filter((t) => t.slug !== toolSlug)
    .map((t) => ({ tool: t, relevance: calculateToolRelevance(t) }))
    .filter((item) => item.relevance > 2)
    .sort((a, b) => b.relevance - a.relevance)
    .reduce((acc: typeof tools, item) => {
      const cat = (item.tool.category || '').toLowerCase();
      const catCount = acc.filter((t) => (t.category || '').toLowerCase() === cat).length;
      if (catCount < 3) acc.push(item.tool);
      return acc;
    }, [])
    .slice(0, 12);

  const tool = tools.find((t) => t.slug === toolSlug);
  const toolName = tool?.name || 'this AI tool';
  const officialUrl = tool?.officialUrl || undefined;
  const affiliateUrl = tool?.affiliateUrl || undefined;

  // 计算Tools平均Rating（用于Review Schema）
  const avgScore = tool?.scores
    ? Object.values(tool.scores).reduce((a, b) => a + (typeof b === 'number' ? b : 0), 0) /
      Object.keys(tool.scores).filter((k) => typeof (tool.scores as any)[k] === 'number').length
    : 7.5;

  // 计算上一篇/下一篇文章
  const currentIndex = posts.findIndex((p) => p.slug === post.slug);
  const previousPost = currentIndex > 0 ? posts[currentIndex - 1] : undefined;
  const nextPost = currentIndex < posts.length - 1 ? posts[currentIndex + 1] : undefined;

  return (
    <>
      {/* 阅读进度条 */}
      <ReadingProgress />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-12">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* 主内容区 - 优化排版 */}
          <div className="flex-1 min-w-0 max-w-2xl">
            {/* SEO结构化数据 */}
            <BreadcrumbSchema
              items={[
                { name: 'Home', url: '/' },
                { name: 'Blog', url: '/blog' },
                { name: post.category, url: `/blog/category/${post.categorySlug}` },
                { name: post.title, url: `/blog/${post.slug}` },
              ]}
            />
            <ReviewSchema
              name={post.title}
              reviewBody={post.excerpt || post.description || ''}
              ratingValue={Math.round(avgScore * 10) / 10}
              bestRating={10}
              worstRating={1}
              author={post.author}
              datePublished={post.date || post.publishedAt}
              itemReviewed={toolName}
            />
            {/* Article Schema - Blog文章结构化数据 */}
            <script
              type="application/ld+json"
              dangerouslySetInnerHTML={{
                __html: JSON.stringify({
                  '@context': 'https://schema.org',
                  '@type': 'Article',
                  headline: post.title,
                  description: post.excerpt.slice(0, 155),
                  author: {
                    '@type': 'Person',
                    name: post.author || 'AIToolCrux Research Team',
                    jobTitle: 'Senior AI Tools Reviewer',
                    url: 'https://www.aitoolcrux.com/about',
                  },
                  datePublished: post.date || post.publishedAt,
                  dateModified:
                    (post as any).updatedAt ||
                    (post as any).lastUpdated ||
                    post.date ||
                    post.publishedAt,
                  publisher: {
                    '@type': 'Organization',
                    name: 'AIToolCrux',
                    url: 'https://www.aitoolcrux.com',
                    logo: {
                      '@type': 'ImageObject',
                      url: 'https://www.aitoolcrux.com/logo.svg',
                      width: 512,
                      height: 512,
                    },
                  },
                  mainEntityOfPage: {
                    '@type': 'WebPage',
                    '@id': `https://www.aitoolcrux.com/blog/${post.slug}`,
                  },
                  image: [
                    {
                      '@type': 'ImageObject',
                      url: `https://www.aitoolcrux.com/api/og?title=${encodeURIComponent(post.title.slice(0, 50))}&description=${encodeURIComponent((post.excerpt || '').slice(0, 100))}&category=${encodeURIComponent(post.category || 'AI Tools')}`,
                      width: 1920,
                      height: 1080,
                    },
                  ],
                  articleSection: post.category,
                  wordCount: post.content ? post.content.length : 1500,
                  inLanguage: 'en',
                  keywords: (post as any).tags ? (post as any).tags.join(', ') : post.category,
                  about: {
                    '@type': 'Thing',
                    name: post.category || 'AI Tools',
                  },
                }),
              }}
            />

            {/* Article content */}
            <article
              style={
                {
                  contentVisibility: 'auto',
                  containIntrinsicSize: 'auto 800px',
                } as React.CSSProperties
              }
              className="prose prose-lg dark:prose-invert max-w-none mb-10
          prose-headings:scroll-mt-24
          prose-h2:text-3xl prose-h2:font-bold prose-h2:mt-16 prose-h2:mb-6 prose-h2:tracking-tight prose-h2:text-gray-900 dark:prose-h2:text-white
          prose-h3:text-2xl prose-h3:font-semibold prose-h3:mt-12 prose-h3:mb-4 prose-h3:text-gray-800 dark:prose-h3:text-gray-200
          prose-p:leading-[1.7] prose-p:mb-8 prose-p:text-gray-700 dark:prose-p:text-gray-300 prose-p:text-[1.05rem]
          prose-a:text-emerald-600 dark:prose-a:text-emerald-400 prose-a:no-underline hover:prose-a:underline prose-a:font-medium
          prose-strong:text-gray-900 dark:prose-strong:text-white prose-strong:font-semibold
          prose-ul:my-8 prose-li:mb-3 prose-li:leading-relaxed
          prose-blockquote:border-l-4 prose-blockquote:border-emerald-500 prose-blockquote:bg-emerald-50/50 dark:prose-blockquote:bg-emerald-900/10 prose-blockquote:py-4 prose-blockquote:px-6 prose-blockquote:rounded-r-lg prose-blockquote:my-8 prose-blockquote:italic prose-blockquote:text-gray-600 dark:prose-blockquote:text-gray-400
          prose-img:rounded-2xl prose-img:shadow-lg prose-img:my-10 prose-img:border prose-img:border-gray-200 dark:prose-img:border-gray-800
          prose-table:w-full prose-table:border-collapse prose-table:my-10 prose-table:text-sm
          prose-th:bg-gray-50 dark:prose-th:bg-gray-800/50 prose-th:p-4 prose-th:text-left prose-th:font-semibold prose-th:text-gray-900 dark:prose-th:text-white prose-th:border-b prose-th:border-gray-200 dark:prose-th:border-gray-700
          prose-td:p-4 prose-td:border-b prose-td:border-gray-100 dark:prose-td:border-gray-800 prose-td:text-gray-600 dark:prose-td:text-gray-400
          prose-code:bg-gray-100 dark:prose-code:bg-gray-800 prose-code:px-2 prose-code:py-1 prose-code:rounded-md prose-code:text-sm prose-code:text-pink-600 dark:prose-code:text-pink-400 prose-code:font-mono
          prose-pre:bg-gray-900 prose-pre:rounded-2xl prose-pre:p-6 prose-pre:my-8 prose-pre:overflow-x-auto prose-pre:text-sm
          first-letter:text-5xl first-letter:font-bold first-letter:float-left first-letter:mr-3 first-letter:leading-none first-letter:text-emerald-600 dark:first-letter:text-emerald-400 first-letter:mt-1"
              dangerouslySetInnerHTML={markdownToHtmlSafe(post.content)}
            />

            {/* Free AI Tools Guide cross-link */}
            <section className="mb-16">
              <Link
                href="/free-ai-tools-guide"
                className="block bg-gradient-to-r from-emerald-50 to-teal-50 dark:from-emerald-900/10 dark:to-teal-900/10 rounded-xl border border-emerald-200 dark:border-emerald-900/30 p-6 hover:shadow-lg transition-all"
              >
                <div className="flex items-center gap-3">
                  <div className="flex-1">
                    <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-1">
                      Looking for free AI tools?
                    </h2>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Browse our curated guide to AI tools with no credit card required and no
                      hidden fees.
                    </p>
                  </div>
                  <span className="inline-flex items-center gap-1 text-sm font-medium text-emerald-600 dark:text-emerald-400 whitespace-nowrap">
                    View Guide <ArrowRight className="w-4 h-4" />
                  </span>
                </div>
              </Link>
            </section>

            {/* Related Articles - 智能推荐 */}
            {relatedPosts.length > 0 && (
              <section className="mb-16">
                <div className="flex items-end justify-between mb-6">
                  <div>
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                      You might also like
                    </h2>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      Smart recommendations based on tags, categories, and content similarity
                    </p>
                  </div>
                  <Link
                    href="/blog"
                    className="hidden sm:inline-flex items-center gap-1 text-sm font-medium text-emerald-600 dark:text-emerald-400 hover:underline"
                  >
                    View all articles
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {relatedPosts.map((related) => (
                    <Link
                      key={related.slug}
                      href={`/blog/${related.slug}`}
                      className="group block bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 p-5 hover:shadow-lg dark:hover:shadow-xl hover:border-emerald-300 dark:hover:border-emerald-700 transition-all duration-200"
                    >
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-xs px-2 py-0.5 bg-emerald-50 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 rounded-full">
                          {related.category}
                        </span>
                        <span className="text-xs text-gray-400">{related.readTime || '5 min'}</span>
                      </div>
                      <h3 className="text-sm font-bold text-gray-900 dark:text-white mb-2 line-clamp-2 group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition-colors">
                        {related.title}
                      </h3>
                      <p className="text-xs text-gray-500 dark:text-gray-400 line-clamp-2 mb-3">
                        {related.excerpt}
                      </p>
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-gray-400">
                          {related.date || related.publishedAt}
                        </span>
                        <span className="text-xs text-emerald-600 dark:text-emerald-400 opacity-0 group-hover:opacity-100 transition-opacity">
                          Read →
                        </span>
                      </div>
                    </Link>
                  ))}
                </div>
                {/* 移动端查看全部链接 */}
                <div className="mt-6 text-center sm:hidden">
                  <Link
                    href="/blog"
                    className="inline-flex items-center gap-1 text-sm font-medium text-emerald-600 dark:text-emerald-400 hover:underline"
                  >
                    View all articles
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>
              </section>
            )}

            {/* FAQ Section - visible accordion for users (JSON-LD removed: Google deprecated FAQ rich results May 2026) */}
            <section className="mb-16">
              <FAQSection
                items={
                  post.faq && post.faq.length > 0
                    ? post.faq.map((item: any) => ({ question: item.q, answer: item.a }))
                    : defaultFAQs
                }
                title="Frequently Asked Questions"
              />
            </section>

            {/* 来源引用列Table - E-E-A-T信任信号 */}
            <section className="mt-10">
              <SourceReferences toolName={toolName} lastUpdated={post.date || post.publishedAt} />
            </section>

            {/* Comments */}
            <section className="border-t border-gray-200 dark:border-gray-800 pt-10">
              <Giscus />
            </section>
          </div>

          {/* 右侧边栏 - 目录（桌面端固定） */}
          <aside className="hidden lg:block w-64 flex-shrink-0">
            <div className="sticky top-24">
              <TableOfContents contentHtml={post.content} />
            </div>
          </aside>
        </div>
      </div>
    </>
  );
}
