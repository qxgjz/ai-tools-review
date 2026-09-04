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
    slug: "alex-chen",
    name: "Alex Chen",
    role: "Editor-in-Chief",
    bio: "10+ years in tech journalism. Former senior editor at a leading tech publication. Covers AI strategy, product analysis, and editorial standards. Alex ensures every review meets our rigorous quality standards and maintains editorial independence.",
    expertise: ["AI Strategy", "Product Analysis", "Editorial Standards", "Tech Journalism"],
    avatar: "AC",
    color: "from-blue-500 to-indigo-600",
  },
  {
    slug: "sarah-kim",
    name: "Sarah Kim",
    role: "Senior Reviewer - Developer Tools",
    bio: "Full-stack developer turned tech reviewer with 8 years of coding experience. Sarah has built production applications at multiple startups and now specializes in testing AI coding assistants, IDEs, and developer productivity tools. She brings a practitioner's perspective to every review.",
    expertise: ["AI Coding", "DevTools", "Code Quality", "Full-Stack Development"],
    avatar: "SK",
    color: "from-emerald-500 to-teal-600",
  },
  {
    slug: "marcus-rodriguez",
    name: "Marcus Rodriguez",
    role: "Senior Reviewer - Creative AI",
    bio: "Digital artist and designer with 12 years of professional experience. Marcus has created work for major brands and now focuses on testing AI image, video, and audio generation tools. He is passionate about the intersection of AI and human creativity, and evaluates creative tools from a working artist's perspective.",
    expertise: ["AI Image", "AI Video", "Design Tools", "Digital Art"],
    avatar: "MR",
    color: "from-orange-500 to-rose-600",
  },
  {
    slug: "emily-watson",
    name: "Emily Watson",
    role: "Reviewer - Productivity & Writing",
    bio: "Content strategist and productivity consultant. Former marketing director at a SaaS company. Emily helps teams adopt AI writing and office tools, and evaluates them based on real-world workflow integration. She focuses on tools that deliver measurable productivity gains.",
    expertise: ["AI Writing", "Productivity", "Marketing AI", "Content Strategy"],
    avatar: "EW",
    color: "from-purple-500 to-pink-600",
  },
  {
    slug: "david-park",
    name: "David Park",
    role: "Reviewer - AI Chat & Search",
    bio: "AI researcher and former NLP engineer. David has worked on conversational AI systems and now specializes in reviewing AI chatbots, search engines, and language models. He evaluates these tools with deep technical understanding of their capabilities and limitations.",
    expertise: ["AI Chat", "AI Search", "LLMs", "NLP"],
    avatar: "DP",
    color: "from-cyan-500 to-blue-600",
  },
  {
    slug: "lisa-anderson",
    name: "Lisa Anderson",
    role: "Reviewer - Business & Enterprise AI",
    bio: "Former IT director at a Fortune 500 company. Lisa has led enterprise AI adoption initiatives and now reviews business-focused AI tools, including automation platforms, analytics tools, and enterprise AI solutions. She evaluates tools through the lens of scalability, security, and ROI.",
    expertise: ["Enterprise AI", "Automation", "Business AI", "IT Strategy"],
    avatar: "LA",
    color: "from-amber-500 to-orange-600",
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
