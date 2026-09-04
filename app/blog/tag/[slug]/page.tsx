import Link from "next/link";
import { notFound } from "next/navigation";
import posts from "@/data/posts.json";

export const dynamic = "force-dynamic";

interface TagPageProps {
  params: { slug: string };
}

export function generateMetadata({ params }: TagPageProps) {
  const tagPosts = posts.filter((p) => p.tagSlugs.includes(params.slug));
  let tagName = params.slug;
  for (const post of posts) {
    const idx = post.tagSlugs.indexOf(params.slug);
    if (idx !== -1) {
      tagName = post.tags[idx];
      break;
    }
  }
  return {
    title: `#${tagName} - AIToolCrux博客`,
    description: `AIToolCrux博客 - 标签 #${tagName} 的所有文章`,
  };
}

export default function TagPage({ params }: TagPageProps) {
  const tagPosts = posts.filter((p) => p.tagSlugs.includes(params.slug));

  if (tagPosts.length === 0) {
    notFound();
  }

  let tagName = params.slug;
  for (const post of posts) {
    const idx = post.tagSlugs.indexOf(params.slug);
    if (idx !== -1) {
      tagName = post.tags[idx];
      break;
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-12">
      {/* 返回按钮 */}
      <Link
        href="/blog"
        className="inline-flex items-center text-sm text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 mb-8 transition-colors"
      >
        ← 返回博客列表
      </Link>

      {/* 标签标题 */}
      <div className="mb-10">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          标签：#{tagName}
        </h1>
        <p className="text-gray-600 dark:text-gray-400">{tagPosts.length} articles</p>
      </div>

      {/* 文章列表 */}
      <div className="space-y-4">
        {tagPosts.map((post) => (
          <Link
            key={post.slug}
            href={`/blog/${post.slug}`}
            className="block bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 p-6 hover:shadow-md dark:hover:shadow-lg transition-shadow"
          >
            <div className="flex items-center gap-2 mb-2">
              <Link
                href={`/blog/category/${post.categorySlug}`}
                className="text-xs font-medium text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20 px-2 py-1 rounded hover:bg-blue-100 dark:hover:bg-blue-900/30 transition-colors"
              >
                {post.category}
              </Link>
              <span className="text-xs text-gray-500 dark:text-gray-400">{post.readTime} min read</span>
            </div>
            <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-2 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
              {post.title}
            </h2>
            <p className="text-gray-600 dark:text-gray-400 text-sm mb-3 line-clamp-2">{post.excerpt}</p>
            <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
              <span>{post.author}</span>
              <span>{post.publishedAt}</span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
