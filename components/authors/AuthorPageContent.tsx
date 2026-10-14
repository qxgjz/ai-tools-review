import Link from 'next/link';
import { ArrowLeft, Calendar, Clock, FileText, Award, ChevronLeft, ChevronRight } from 'lucide-react';

export interface AuthorPost {
  slug: string;
  title: string;
  date: string;
  readingTime?: string;
  category?: string;
}

interface AuthorInfo {
  name: string;
  role: string;
  bio: string;
  expertise: string[];
  avatar: string;
  color: string;
}

export const PAGE_SIZE = 60;

export default function AuthorPageContent({
  author,
  authorSlug,
  posts,
  totalCount,
  page,
  totalPages,
}: {
  author: AuthorInfo;
  authorSlug: string;
  posts: AuthorPost[];
  totalCount: number;
  page: number;
  totalPages: number;
}) {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-12">
      {/* Back */}
      <Link
        href="/authors"
        className="inline-flex items-center gap-2 text-gray-500 dark:text-gray-400 hover:text-emerald-600 dark:hover:text-emerald-400 mb-8 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to all authors
      </Link>

      {/* Author Header */}
      <div className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-8 shadow-sm mb-12">
        <div className="flex flex-col sm:flex-row items-start gap-6">
          <div
            className={`w-24 h-24 rounded-full bg-gradient-to-br ${author.color} flex items-center justify-center text-white text-4xl font-bold shadow-lg flex-shrink-0`}
          >
            {author.avatar}
          </div>
          <div className="flex-1">
            <h1 className="text-3xl font-extrabold text-gray-900 dark:text-white mb-2">
              {author.name}
            </h1>
            <p className="text-lg text-emerald-600 dark:text-emerald-400 font-medium mb-4">
              {author.role}
            </p>
            <p className="text-gray-600 dark:text-gray-400 leading-relaxed mb-4">{author.bio}</p>
            <div className="flex flex-wrap gap-2">
              {author.expertise.map((exp: string, i: number) => (
                <span
                  key={i}
                  className="px-3 py-1 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 rounded-full text-sm"
                >
                  {exp}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Articles */}
      <section>
        <div className="flex items-center gap-3 mb-8">
          <FileText className="w-7 h-7 text-emerald-600" />
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Articles by {author.name.split(' ')[0]}
          </h2>
          <span className="px-3 py-1 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400 rounded-full text-sm font-bold">
            {totalCount}
          </span>
        </div>

        {posts.length === 0 ? (
          <div className="text-center py-12 bg-gray-50 dark:bg-gray-900/50 rounded-2xl">
            <FileText className="w-12 h-12 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
            <p className="text-gray-500 dark:text-gray-400">No articles found for this author.</p>
          </div>
        ) : (
          <>
            <div className="divide-y divide-gray-100 dark:divide-gray-800 border border-gray-100 dark:border-gray-800 rounded-xl bg-white dark:bg-gray-900 overflow-hidden">
              {posts.map((post) => (
                <Link
                  key={post.slug}
                  href={`/blog/${post.slug}`}
                  className="flex items-center justify-between gap-4 px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
                >
                  <span className="font-semibold text-gray-900 dark:text-white truncate min-w-0 text-sm">
                    {post.title}
                  </span>
                  <span className="flex items-center gap-3 text-xs text-gray-400 dark:text-gray-500 flex-shrink-0">
                    {post.readingTime && (
                      <span className="inline-flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {post.readingTime}
                      </span>
                    )}
                    {post.category && (
                      <span className="px-2 py-0.5 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400 rounded">
                        {post.category}
                      </span>
                    )}
                    <span className="inline-flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      {post.date}
                    </span>
                  </span>
                </Link>
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex items-center justify-between mt-8">
                {page > 1 ? (
                  <Link
                    href={page === 2 ? `/authors/${authorSlug}` : `/authors/${authorSlug}/page/${page - 1}`}
                    className="inline-flex items-center gap-1 px-4 py-2 rounded-lg border border-gray-200 dark:border-gray-700 text-sm text-gray-600 dark:text-gray-300 hover:border-emerald-300 dark:hover:border-emerald-700 transition-colors"
                  >
                    <ChevronLeft className="w-4 h-4" />
                    Previous
                  </Link>
                ) : (
                  <span />
                )}
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  Page {page} of {totalPages}
                </span>
                {page < totalPages ? (
                  <Link
                    href={`/authors/${authorSlug}/page/${page + 1}`}
                    className="inline-flex items-center gap-1 px-4 py-2 rounded-lg border border-gray-200 dark:border-gray-700 text-sm text-gray-600 dark:text-gray-300 hover:border-emerald-300 dark:hover:border-emerald-700 transition-colors"
                  >
                    Next
                    <ChevronRight className="w-4 h-4" />
                  </Link>
                ) : (
                  <span />
                )}
              </div>
            )}
          </>
        )}
      </section>

      {/* Editorial Standards CTA */}
      <section className="mt-16 bg-gradient-to-br from-emerald-50 to-teal-50 dark:from-emerald-900/10 dark:to-teal-900/10 rounded-2xl p-8 text-center">
        <Award className="w-10 h-10 text-emerald-600 mx-auto mb-4" />
        <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
          Editorial Independence
        </h3>
        <p className="text-gray-600 dark:text-gray-400 text-sm max-w-lg mx-auto mb-4">
          All reviews are independent and based on hands-on testing. We do not accept payment for
          higher ratings.
        </p>
        <Link
          href="/about"
          className="inline-flex items-center gap-2 text-emerald-600 dark:text-emerald-400 font-medium hover:text-emerald-700 dark:hover:text-emerald-300"
        >
          Learn about our methodology
        </Link>
      </section>
    </div>
  );
}
