import type { Metadata } from "next";
import Link from "next/link";
import { Users, Award, FileText, ArrowRight } from "lucide-react";
import postsData from "@/data/posts.json";

export const metadata: Metadata = {
  title: "Authors - AIToolCrux | Meet Our Editorial Team",
  description: "Meet the AIToolCrux editorial team. Our reviewers bring decades of combined experience in tech, development, design, and content strategy.",
  alternates: {
    canonical: "https://www.aitoolcrux.com/authors",
  },
};

const AUTHORS = [
  {
    slug: "aitoolcrux-editorial-team",
    name: "AIToolCrux Editorial Team",
    role: "Independent AI Tool Review Team",
    bio: "The AIToolCrux Editorial Team is a collective of independent AI tool reviewers with decades of combined experience in tech, development, design, and content strategy. Our team follows a transparent six-dimensional evaluation methodology, tests every tool for 14+ days, and does not accept payment for higher ratings. We believe good tool selection should be based on data, not marketing hype.",
    expertise: ["AI Chatbots", "Image Generation", "Code Assistants", "Productivity Tools", "Video Generation", "Enterprise AI"],
    avatar: "AT",
    color: "from-blue-500 to-indigo-600",
  },
];

export default function AuthorsPage() {
  const posts = postsData as any[];

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-12">
      {/* Hero */}
      <div className="text-center mb-16">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-full text-sm font-medium mb-6">
          <Users className="w-4 h-4" />
          Our Editorial Team
        </div>
        <h1 className="text-4xl sm:text-5xl font-extrabold text-gray-900 dark:text-white mb-6">
          Meet Our Authors
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto leading-relaxed">
          Our reviewers bring decades of combined experience in technology, development, design, and content strategy. Every review is written by a subject matter expert who has hands-on experience with the tools they evaluate.
        </p>
      </div>

      {/* Author Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
        {AUTHORS.map((author) => {
          const authorPosts = posts.filter((p) => p.author?.includes(author.name.split(" ")[0]) || p.author === "AIToolCrux Editorial Team");
          return (
            <div
              key={author.slug}
              className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-6 shadow-sm hover:shadow-lg hover:border-blue-200 dark:hover:border-blue-800 transition-all duration-300"
            >
              <div className="flex items-center gap-4 mb-4">
                <div className={`w-16 h-16 rounded-full bg-gradient-to-br ${author.color} flex items-center justify-center text-white text-2xl font-bold shadow-lg`}>
                  {author.avatar}
                </div>
                <div>
                  <h2 className="text-lg font-bold text-gray-900 dark:text-white">{author.name}</h2>
                  <p className="text-sm text-blue-600 dark:text-blue-400">{author.role}</p>
                </div>
              </div>

              <p className="text-sm text-gray-600 dark:text-gray-400 leading-relaxed mb-4 line-clamp-4">
                {author.bio}
              </p>

              <div className="flex flex-wrap gap-2 mb-4">
                {author.expertise.map((exp, i) => (
                  <span key={i} className="px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 rounded text-xs">
                    {exp}
                  </span>
                ))}
              </div>

              <div className="flex items-center justify-between pt-4 border-t border-gray-100 dark:border-gray-800">
                <div className="flex items-center gap-1 text-sm text-gray-500 dark:text-gray-400">
                  <FileText className="w-4 h-4" />
                  <span>{authorPosts.length} articles</span>
                </div>
                <Link
                  href={`/authors/${author.slug}`}
                  className="inline-flex items-center gap-1 text-sm text-blue-600 dark:text-blue-400 font-medium hover:text-blue-700 dark:hover:text-blue-300"
                >
                  View articles
                  <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
            </div>
          );
        })}
      </div>

      {/* Editorial Standards */}
      <section className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/10 dark:to-indigo-900/10 rounded-3xl p-8 sm:p-12">
        <div className="max-w-3xl mx-auto text-center">
          <Award className="w-12 h-12 text-blue-600 mx-auto mb-4" />
          <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white mb-4">
            Our Editorial Standards
          </h2>
          <p className="text-gray-600 dark:text-gray-400 leading-relaxed mb-6">
            Every review on AIToolCrux follows our strict editorial process:
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-left">
            {[
              "Hands-on testing by subject matter experts",
              "Standardized test cases across all tools",
              "Six-dimensional weighted scoring framework",
              "No payment for ratings or favorable reviews",
              "Regular updates to reflect product changes",
              "Full disclosure of affiliate relationships",
            ].map((item, i) => (
              <div key={i} className="flex items-start gap-2">
                <span className="w-5 h-5 rounded-full bg-blue-600 text-white text-xs flex items-center justify-center flex-shrink-0 mt-0.5">
                  {i + 1}
                </span>
                <span className="text-sm text-gray-700 dark:text-gray-300">{item}</span>
              </div>
            ))}
          </div>
          <div className="mt-8">
            <Link
              href="/about"
              className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 transition-colors"
            >
              Learn More About Us
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
