import Link from "next/link";
import { notFound } from "next/navigation";
import posts from "@/data/posts.json";


// Helper: convert tag name to URL-friendly slug
function slugifyTag(name: string): string {
  return name
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-');
}

// Helper: get all tags for a post as (slug, displayName) pairs
function getPostTagSlugs(post: any): { slug: string; name: string }[] {
  const tags: string[] = post.tags || [];
  return tags.map((name) => ({ slug: slugifyTag(name), name }));
}

interface TagPageProps {
  params: { slug: string };
}

export function generateMetadata({ params }: TagPageProps) {
  const tagPosts = posts.filter((p) =>
    getPostTagSlugs(p).some((t) => t.slug === params.slug)
  );
  let tagName = params.slug;
  for (const post of posts) {
    const match = getPostTagSlugs(post).find((t) => t.slug === params.slug);
    if (match) {
      tagName = match.name;
      break;
    }
  }
  const articleCount = tagPosts.length;
  return {
    title: `Best ${tagName} AI Tools & Articles 2026 | AIToolCrux`,
    description: `Explore ${articleCount} expert-reviewed ${tagName} AI tools and articles on AIToolCrux. In-depth comparisons and honest reviews.`,
    alternates: {
      canonical: `https://www.aitoolcrux.com/blog/tag/${params.slug}`,
    },
  };
}

export default function TagPage({ params }: TagPageProps) {
  const tagPosts = posts.filter((p) =>
    getPostTagSlugs(p).some((t) => t.slug === params.slug)
  );

  if (tagPosts.length === 0) {
    notFound();
  }

  let tagName = params.slug;
  for (const post of posts) {
    const match = getPostTagSlugs(post).find((t) => t.slug === params.slug);
    if (match) {
      tagName = match.name;
      break;
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-12">
      {/* Return按钮 */}
      <Link
        href="/blog"
        className="inline-flex items-center text-sm text-gray-600 dark:text-gray-400 hover:text-emerald-600 dark:hover:text-emerald-400 mb-8 transition-colors"
      >
        ← Back to Blog
      </Link>

      {/* Tags title */}
      <div className="mb-10">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Tags: #{tagName}
        </h1>
        <p className="text-gray-600 dark:text-gray-400">{tagPosts.length} articles</p>
      </div>

      {/* Article list */}
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
                className="text-xs font-medium text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-900/20 px-2 py-1 rounded hover:bg-emerald-100 dark:hover:bg-emerald-900/30 transition-colors"
              >
                {post.category}
              </Link>
              <span className="text-xs text-gray-500 dark:text-gray-400">{post.readTime} min read</span>
            </div>
            <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-2 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors">
              {post.title}
            </h2>
            <p className="text-gray-600 dark:text-gray-400 text-sm mb-3 line-clamp-2">{post.excerpt}</p>
            <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
              <span>{post.author}</span>
              <span>{post.date}</span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
