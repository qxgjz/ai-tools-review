import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, Calendar, Clock, FileText, Award } from "lucide-react";
import postsData from "@/data/posts.json";

const AUTHORS: Record<string, any> = {
  "alex-chen": {
    name: "Alex Chen",
    role: "Editor-in-Chief",
    bio: "10+ years in tech journalism. Former senior editor at a leading tech publication. Covers AI strategy, product analysis, and editorial standards. Alex ensures every review meets our rigorous quality standards and maintains editorial independence.",
    expertise: ["AI Strategy", "Product Analysis", "Editorial Standards", "Tech Journalism"],
    avatar: "AC",
    color: "from-blue-500 to-indigo-600",
  },
  "sarah-kim": {
    name: "Sarah Kim",
    role: "Senior Reviewer - Developer Tools",
    bio: "Full-stack developer turned tech reviewer with 8 years of coding experience. Sarah has built production applications at multiple startups and now specializes in testing AI coding assistants, IDEs, and developer productivity tools.",
    expertise: ["AI Coding", "DevTools", "Code Quality", "Full-Stack Development"],
    avatar: "SK",
    color: "from-emerald-500 to-teal-600",
  },
  "marcus-rodriguez": {
    name: "Marcus Rodriguez",
    role: "Senior Reviewer - Creative AI",
    bio: "Digital artist and designer with 12 years of professional experience. Marcus has created work for major brands and now focuses on testing AI image, video, and audio generation tools from a working artist's perspective.",
    expertise: ["AI Image", "AI Video", "Design Tools", "Digital Art"],
    avatar: "MR",
    color: "from-orange-500 to-rose-600",
  },
  "emily-watson": {
    name: "Emily Watson",
    role: "Reviewer - Productivity & Writing",
    bio: "Content strategist and productivity consultant. Former marketing director at a SaaS company. Emily helps teams adopt AI writing and office tools, evaluating them based on real-world workflow integration and measurable productivity gains.",
    expertise: ["AI Writing", "Productivity", "Marketing AI", "Content Strategy"],
    avatar: "EW",
    color: "from-purple-500 to-pink-600",
  },
  "david-park": {
    name: "David Park",
    role: "Reviewer - AI Chat & Search",
    bio: "AI researcher and former NLP engineer. David has worked on conversational AI systems and now specializes in reviewing AI chatbots, search engines, and language models with deep technical understanding of their capabilities and limitations.",
    expertise: ["AI Chat", "AI Search", "LLMs", "NLP"],
    avatar: "DP",
    color: "from-cyan-500 to-blue-600",
  },
  "lisa-anderson": {
    name: "Lisa Anderson",
    role: "Reviewer - Business & Enterprise AI",
    bio: "Former IT director at a Fortune 500 company. Lisa has led enterprise AI adoption initiatives and now reviews business-focused AI tools, including automation platforms, analytics tools, and enterprise AI solutions.",
    expertise: ["Enterprise AI", "Automation", "Business AI", "IT Strategy"],
    avatar: "LA",
    color: "from-amber-500 to-orange-600",
  },
};

export function generateStaticParams() {
  return Object.keys(AUTHORS).map((slug) => ({ slug }));
}

export function generateMetadata({ params }: { params: { slug: string } }): Metadata {
  const author = AUTHORS[params.slug];
  if (!author) return {};
  return {
    title: `${author.name} - ${author.role}`,
    description: author.bio,
    alternates: {
      canonical: `https://www.aitoolcrux.com/authors/${params.slug}`,
    },
  };
}

export default function AuthorPage({ params }: { params: { slug: string } }) {
  const author = AUTHORS[params.slug];
  if (!author) notFound();

  const posts = (postsData as any[]).filter(
    (p) => p.author?.includes(author.name.split(" ")[0]) || p.author === "AIToolCrux Editorial Team"
  );

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-12">
      {/* Back */}
      <Link
        href="/authors"
        className="inline-flex items-center gap-2 text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 mb-8 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to all authors
      </Link>

      {/* Author Header */}
      <div className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-8 shadow-sm mb-12">
        <div className="flex flex-col sm:flex-row items-start gap-6">
          <div className={`w-24 h-24 rounded-full bg-gradient-to-br ${author.color} flex items-center justify-center text-white text-4xl font-bold shadow-lg flex-shrink-0`}>
            {author.avatar}
          </div>
          <div className="flex-1">
            <h1 className="text-3xl font-extrabold text-gray-900 dark:text-white mb-2">{author.name}</h1>
            <p className="text-lg text-blue-600 dark:text-blue-400 font-medium mb-4">{author.role}</p>
            <p className="text-gray-600 dark:text-gray-400 leading-relaxed mb-4">{author.bio}</p>
            <div className="flex flex-wrap gap-2">
              {author.expertise.map((exp: string, i: number) => (
                <span key={i} className="px-3 py-1 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 rounded-full text-sm">
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
          <FileText className="w-7 h-7 text-blue-600" />
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Articles by {author.name.split(" ")[0]}
          </h2>
          <span className="px-3 py-1 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-full text-sm font-bold">
            {posts.length}
          </span>
        </div>

        {posts.length === 0 ? (
          <div className="text-center py-12 bg-gray-50 dark:bg-gray-900/50 rounded-2xl">
            <FileText className="w-12 h-12 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
            <p className="text-gray-500 dark:text-gray-400">No articles found for this author.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {posts.map((post) => (
              <Link
                key={post.slug}
                href={`/blog/${post.slug}`}
                className="block bg-white dark:bg-gray-900 rounded-xl border border-gray-100 dark:border-gray-800 p-6 hover:shadow-md hover:border-blue-200 dark:hover:border-blue-800 transition-all"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <h3 className="text-lg font-bold text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors mb-2">
                      {post.title}
                    </h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400 line-clamp-2 mb-3">
                      {post.excerpt}
                    </p>
                    <div className="flex items-center gap-4 text-xs text-gray-400 dark:text-gray-500">
                      <span className="inline-flex items-center gap-1">
                        <Calendar className="w-3 h-3" />
                        {post.publishedAt}
                      </span>
                      {post.readingTime && (
                        <span className="inline-flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          {post.readingTime}
                        </span>
                      )}
                      {post.category && (
                        <span className="px-2 py-0.5 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded">
                          {post.category}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </section>

      {/* Editorial Standards CTA */}
      <section className="mt-16 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/10 dark:to-indigo-900/10 rounded-2xl p-8 text-center">
        <Award className="w-10 h-10 text-blue-600 mx-auto mb-4" />
        <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Editorial Independence</h3>
        <p className="text-gray-600 dark:text-gray-400 text-sm max-w-lg mx-auto mb-4">
          All reviews are independent and based on hands-on testing. We do not accept payment for higher ratings.
        </p>
        <Link href="/about" className="inline-flex items-center gap-2 text-blue-600 dark:text-blue-400 font-medium hover:text-blue-700 dark:hover:text-blue-300">
          Learn about our methodology
        </Link>
      </section>
    </div>
  );
}
