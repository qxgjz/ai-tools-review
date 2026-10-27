import Link from 'next/link';
import { notFound } from 'next/navigation';
import posts from '@/data/posts.json';
import { shouldSkipStaticGen } from '@/lib/static-gen';

interface CategoryPageProps {
  params: { slug: string };
}

export const dynamic = 'force-static';

export async function generateStaticParams() {
  const slugs = new Set(posts.map((p) => p.categorySlug).filter(Boolean));
  if (shouldSkipStaticGen()) return [];
  return Array.from(slugs).map((slug) => ({ slug }));
}

export function generateMetadata({ params }: CategoryPageProps) {
  const categoryPosts = posts.filter((p) => p.categorySlug === params.slug);
  // 用全部文章的分类集合做差异化 title，避免不同 slug 产生相同 title（SEO 重复）
  const cats = Array.from(new Set(categoryPosts.map((p) => p.category).filter(Boolean)));
  const categoryName = cats.join(' & ') || params.slug;
  const articleCount = categoryPosts.length;
  // SEO 长度规范：title ≤60 字符、description ≤155 字符；截断但保留关键词与站点标识
  const fullTitle = `${categoryName} AI Tools Reviews | AIToolCrux`;
  const title =
    fullTitle.length > 60
      ? `${fullTitle.slice(0, 56).replace(/[|&\s]+$/, '')}...`
      : fullTitle;
  const fullDescription = `Read ${articleCount} expert ${categoryName} AI articles and reviews on AIToolCrux. In-depth guides, comparisons, and testing results.`;
  const description =
    fullDescription.length > 155
      ? `${fullDescription.slice(0, 152).trimEnd()}...`
      : fullDescription;
  return {
    title,
    description,
    alternates: {
      canonical: `https://www.aitoolcrux.com/blog/category/${params.slug}`,
    },
  };
}

export default function CategoryPage({ params }: CategoryPageProps) {
  const categoryPosts = posts.filter((p) => p.categorySlug === params.slug);

  if (categoryPosts.length === 0) {
    notFound();
  }

  const categoryName = categoryPosts[0].category;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-12">
      {/* Return按钮 */}
      <Link
        href="/blog"
        className="inline-flex items-center text-sm text-gray-600 dark:text-gray-400 hover:text-emerald-600 dark:hover:text-emerald-400 mb-8 transition-colors"
      >
        ← ← Back to Blog
      </Link>

      {/* Categories标题 */}
      <div className="mb-10">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Category: {categoryName}
        </h1>
        <p className="text-gray-600 dark:text-gray-400">{categoryPosts.length} articles</p>
      </div>

      {/* 文章列Table */}
      <div className="space-y-4">
        {categoryPosts.map((post) => (
          <Link
            key={post.slug}
            href={`/blog/${post.slug}`}
            className="block bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 p-6 hover:shadow-md dark:hover:shadow-lg transition-shadow"
          >
            <div className="flex items-center gap-2 mb-2">
              <Link
                href={`/blog/category/${post.categorySlug}`}
                className="text-xs font-medium text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-900/20 px-2 py-1 rounded hover:bg-emerald-100 dark:hover:bg-emerald-900/30 transition-colors"
              >
                {post.category}
              </Link>
              <span className="text-xs text-gray-500 dark:text-gray-400">
                {post.readTime} min read
              </span>
            </div>
            <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-2 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors">
              {post.title}
            </h2>
            <p className="text-gray-600 dark:text-gray-400 text-sm mb-3 line-clamp-2">
              {post.excerpt}
            </p>
            <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
              <span>{post.author}</span>
              <span>{post.date || post.publishedAt}</span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
