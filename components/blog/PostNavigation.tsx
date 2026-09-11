import Link from "next/link";
import { ArrowLeft, ArrowRight } from "lucide-react";

interface Post {
  slug: string;
  title: string;
  category?: string;
  categorySlug?: string;
  publishedAt?: string;
}

interface PostNavigationProps {
  previousPost?: Post;
  nextPost?: Post;
  className?: string;
}

/**
 * PostNavigation - 文章上一篇/下一篇导航
 * 基于GitHub高星博客项目最佳实践：
 * - 左右分栏布局
 * - 显示文章标题和分类
 * - 悬停效果
 * - 响应式设计
 */
export function PostNavigation({ previousPost, nextPost, className = "" }: PostNavigationProps) {
  if (!previousPost && !nextPost) return null;

  return (
    <nav className={`grid grid-cols-1 md:grid-cols-2 gap-4 ${className}`}>
      {/* 上一篇 */}
      {previousPost ? (
        <Link
          href={`/blog/${previousPost.slug}`}
          className="group flex items-start gap-3 p-4 bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 hover:border-blue-300 dark:hover:border-blue-700 hover:shadow-md transition-all duration-200"
        >
          <div className="flex-shrink-0 mt-0.5">
            <div className="w-8 h-8 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center group-hover:bg-blue-100 dark:group-hover:bg-blue-900/30 transition-colors">
              <ArrowLeft className="w-4 h-4 text-gray-500 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors" />
            </div>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">← Previous Article</p>
            <h4 className="text-sm font-medium text-gray-900 dark:text-white line-clamp-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
              {previousPost.title}
            </h4>
            {previousPost.category && (
              <span className="inline-block mt-1.5 text-xs text-blue-600 dark:text-blue-400">
                {previousPost.category}
              </span>
            )}
          </div>
        </Link>
      ) : (
        <div className="hidden md:block" />
      )}

      {/* 下一篇 */}
      {nextPost ? (
        <Link
          href={`/blog/${nextPost.slug}`}
          className="group flex items-start gap-3 p-4 bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 hover:border-blue-300 dark:hover:border-blue-700 hover:shadow-md transition-all duration-200 md:text-right"
        >
          <div className="flex-1 min-w-0 md:order-1">
            <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">Next Article →</p>
            <h4 className="text-sm font-medium text-gray-900 dark:text-white line-clamp-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
              {nextPost.title}
            </h4>
            {nextPost.category && (
              <span className="inline-block mt-1.5 text-xs text-blue-600 dark:text-blue-400">
                {nextPost.category}
              </span>
            )}
          </div>
          <div className="flex-shrink-0 mt-0.5 md:order-2">
            <div className="w-8 h-8 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center group-hover:bg-blue-100 dark:group-hover:bg-blue-900/30 transition-colors">
              <ArrowRight className="w-4 h-4 text-gray-500 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors" />
            </div>
          </div>
        </Link>
      ) : (
        <div className="hidden md:block" />
      )}
    </nav>
  );
}
