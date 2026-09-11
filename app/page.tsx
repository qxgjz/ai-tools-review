import Link from "next/link";
import dynamic from "next/dynamic";
import {
  Sparkles,
  Trophy,
  ArrowRight,
  MessageSquare,
  PenTool,
  Image as ImageIcon,
  Code,
  Video,
  Music,
  Briefcase,
  Search as SearchIcon,
  Bot,
  Palette,
  CheckCircle2,
  Star,
  Zap,
  Shield,
  Layers,
  TrendingUp,
  FileText,
} from "lucide-react";
import toolsData from "@/data/tools.json";
import postsData from "@/data/posts.json";
import type { Tool } from "@/types";
import { FadeIn } from "@/components/animations";
import { calculateScoreResult } from "@/lib/scoring";

// Dynamic import heavy components
const ToolList = dynamic(() => import("@/components/tools/ToolList").then(m => m.ToolList), {
  loading: () => <div className="animate-pulse h-64 bg-zinc-100 dark:bg-zinc-800 rounded-xl" />,
});
const NewsletterSignup = dynamic(() => import("@/components/monetization/NewsletterSignup").then(m => m.NewsletterSignup), {
  ssr: false,
  loading: () => null,
});

const CATEGORIES = [
  { slug: "chat", name: "AI Chat", icon: MessageSquare },
  { slug: "writing", name: "AI Writing", icon: PenTool },
  { slug: "image", name: "AI Image", icon: ImageIcon },
  { slug: "code", name: "AI Coding", icon: Code },
  { slug: "video", name: "AI Video", icon: Video },
  { slug: "audio", name: "AI Audio", icon: Music },
  { slug: "productivity", name: "AI Office", icon: Briefcase },
  { slug: "search", name: "AI Search", icon: SearchIcon },
  { slug: "agent", name: "AI Agent", icon: Bot },
  { slug: "design", name: "AI Design", icon: Palette },
];

const METHODOLOGY = [
  { icon: Zap, title: "Features & Output Quality", weight: "25%", desc: "Core feature completeness, output accuracy, and use case coverage" },
  { icon: Layers, title: "User Experience", weight: "20%", desc: "Interface design, learning curve, documentation quality" },
  { icon: Star, title: "Price vs. Value", weight: "20%", desc: "Cost transparency, free tier, return on investment" },
  { icon: Code, title: "Integrations & Developers", weight: "15%", desc: "API quality, platform compatibility, ecosystem" },
  { icon: Shield, title: "Support & Reliability", weight: "10%", desc: "Uptime, update frequency, customer support" },
  { icon: CheckCircle2, title: "Ethics and Transparency", weight: "10%", desc: "Data privacy, bias disclosure, responsible AI" },
];

export default function HomePage() {
  const tools = toolsData as Tool[];
  const topTools = [...tools]
    .map((t) => ({ ...t, total: calculateScoreResult(t.scores).total }))
    .sort((a, b) => b.total - a.total)
    .slice(0, 8);

  const latestPosts = postsData.slice(0, 3);

  return (
    <div className="min-h-screen">
      {/* Schema.org structured data */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "WebSite",
            name: "AIToolCrux",
            url: "https://www.aitoolcrux.com",
            description: "Professional AI tool reviews, comparisons, and recommendations based on a six-dimensional evaluation framework.",
            inLanguage: "en",
            potentialAction: {
              "@type": "SearchAction",
              target: {
                "@type": "EntryPoint",
                urlTemplate: "https://www.aitoolcrux.com/search?q={search_term_string}",
              },
              "query-input": "required name=search_term_string",
            },
          }),
        }}
      />

      {/* === HERO SECTION - Asymmetric layout (Taste Skill: Anti-Center Bias) === */}
      <section className="relative bg-zinc-950 text-white overflow-hidden">
        {/* Subtle grid background - no neon gradients */}
        <div
          className="absolute inset-0 opacity-[0.03]"
          style={{
            backgroundImage: "linear-gradient(to right, white 1px, transparent 1px), linear-gradient(to bottom, white 1px, transparent 1px)",
            backgroundSize: "60px 60px",
          }}
        />

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 py-20 lg:py-28">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            {/* Left: Content (7 cols) - left-aligned, NOT centered */}
            <div className="lg:col-span-7">
              <FadeIn delay={0.1} y={20}>
                <div className="inline-flex items-center gap-2 px-3 py-1 bg-emerald-500/10 border border-emerald-500/20 rounded-full text-sm mb-6">
                  <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
                  <span className="text-emerald-300">Independent AI Tool Reviews</span>
                </div>
              </FadeIn>

              <FadeIn delay={0.2} y={30}>
                <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-6 leading-[1.1] tracking-tight">
                  Find the best AI tools,
                  <br />
                  <span className="text-emerald-400">tested and ranked.</span>
                </h1>
              </FadeIn>

              <FadeIn delay={0.3} y={20}>
                <p className="text-lg text-zinc-400 mb-8 max-w-xl leading-relaxed">
                  {tools.length}+ AI tools evaluated across six dimensions: features, UX, pricing, integrations, support, and ethics. No paid placements, no affiliate bias.
                </p>
              </FadeIn>

              <FadeIn delay={0.4} y={20}>
                <div className="flex flex-col sm:flex-row items-start gap-4 mb-10">
                  <Link
                    href="/ranking"
                    className="inline-flex items-center gap-2 px-6 py-3 bg-emerald-600 hover:bg-emerald-500 text-white font-medium rounded-lg transition-colors"
                  >
                    <Trophy className="w-4 h-4" />
                    View Rankings
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                  <Link
                    href="/generator"
                    className="inline-flex items-center gap-2 px-6 py-3 bg-transparent border border-zinc-700 hover:border-zinc-500 text-zinc-300 hover:text-white font-medium rounded-lg transition-colors"
                  >
                    <Sparkles className="w-4 h-4" />
                    AI Tool Matcher
                  </Link>
                </div>
              </FadeIn>

              {/* Stats - left aligned, not centered */}
              <FadeIn delay={0.5} y={20}>
                <div className="flex flex-wrap items-center gap-8">
                  <div>
                    <div className="text-2xl font-bold text-white">{tools.length}+</div>
                    <div className="text-sm text-zinc-500">Tools Reviewed</div>
                  </div>
                  <div className="w-px h-10 bg-zinc-800" />
                  <div>
                    <div className="text-2xl font-bold text-white">6</div>
                    <div className="text-sm text-zinc-500">Score Dimensions</div>
                  </div>
                  <div className="w-px h-10 bg-zinc-800" />
                  <div>
                    <div className="text-2xl font-bold text-white">100%</div>
                    <div className="text-sm text-zinc-500">Independent</div>
                  </div>
                </div>
              </FadeIn>
            </div>

            {/* Right: Top 3 Tools showcase - real data, no fake UI (Taste Skill rule) */}
            <div className="lg:col-span-5 hidden lg:block">
              <FadeIn delay={0.3} y={30}>
                <div className="space-y-3">
                  <div className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-2">Top 3 Rated Tools</div>
                  {topTools.slice(0, 3).map((tool, i) => (
                    <Link
                      key={tool.slug}
                      href={`/tools/${tool.slug}`}
                      className="flex items-center gap-4 p-4 bg-zinc-900/50 border border-zinc-800 rounded-xl hover:border-emerald-500/50 hover:bg-zinc-900 transition-all group"
                    >
                      <div className="w-10 h-10 flex-shrink-0 flex items-center justify-center rounded-lg bg-zinc-800 text-zinc-300 font-bold text-lg">
                        {tool.name.charAt(0).toUpperCase()}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="font-semibold text-white group-hover:text-emerald-400 transition-colors truncate">{tool.name}</div>
                        <div className="text-xs text-zinc-500 truncate">{tool.vendor}</div>
                      </div>
                      <div className="text-right">
                        <div className="text-xl font-bold text-emerald-400">{tool.total.toFixed(1)}</div>
                        <div className="text-[10px] text-zinc-500">/10</div>
                      </div>
                      <div className="w-6 h-6 flex items-center justify-center rounded-full bg-zinc-800 text-zinc-500 group-hover:bg-emerald-600 group-hover:text-white transition-colors">
                        <ArrowRight className="w-3 h-3" />
                      </div>
                    </Link>
                  ))}
                  <Link href="/ranking" className="flex items-center justify-center gap-2 text-sm text-emerald-400 hover:text-emerald-300 transition-colors pt-2">
                    View all {tools.length} rankings
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>
              </FadeIn>
            </div>
          </div>
        </div>
      </section>

      {/* === CATEGORIES SECTION - Clean grid, no gradient icons === */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 lg:py-20">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-10 gap-4">
          <div>
            <h2 className="text-2xl sm:text-3xl font-bold text-zinc-900 dark:text-white mb-2">
              Browse by Category
            </h2>
            <p className="text-zinc-500 dark:text-zinc-400">
              Explore tools across {CATEGORIES.length} categories
            </p>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
          {CATEGORIES.map((cat) => {
            const count = tools.filter((t) => t.category === cat.slug).length;
            const Icon = cat.icon;
            return (
              <Link
                key={cat.slug}
                href={`/category/${cat.slug}`}
                className="group p-4 bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 hover:border-emerald-500 dark:hover:border-emerald-500 hover:shadow-sm transition-all"
              >
                <div className="w-9 h-9 flex items-center justify-center rounded-lg bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 group-hover:bg-emerald-100 dark:group-hover:bg-emerald-900/30 group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition-colors mb-3">
                  <Icon className="w-4.5 h-4.5" />
                </div>
                <h3 className="text-sm font-semibold text-zinc-900 dark:text-white group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition-colors">
                  {cat.name}
                </h3>
                <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-0.5">{count} tools</p>
              </Link>
            );
          })}
        </div>
      </section>

      {/* === POPULAR TOOLS BY CATEGORY - Internal link optimization === */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 py-12 lg:py-16">
        <div className="mb-8">
          <h2 className="text-2xl sm:text-3xl font-bold text-zinc-900 dark:text-white mb-2">
            Popular Tools by Category
          </h2>
          <p className="text-zinc-500 dark:text-zinc-400">
            Explore the most searched AI tools across categories
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Image Generation */}
          <div className="bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 p-5">
            <h3 className="text-sm font-semibold text-zinc-900 dark:text-white mb-3 flex items-center gap-2">
              <ImageIcon className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              AI Image Generation
            </h3>
            <div className="space-y-2">
              {tools.filter(t => t.category === "image").slice(0, 4).map((tool) => {
                const total = calculateScoreResult(tool.scores).total;
                return (
                  <Link key={tool.slug} href={`/tools/${tool.slug}`} className="flex items-center justify-between py-1.5 hover:bg-zinc-50 dark:hover:bg-zinc-800/50 px-2 -mx-2 rounded transition-colors">
                    <span className="text-sm text-zinc-700 dark:text-zinc-300 hover:text-emerald-600 dark:hover:text-emerald-400 font-medium">{tool.name}</span>
                    <span className="text-xs text-zinc-400 dark:text-zinc-500 font-mono">{total.toFixed(1)}</span>
                  </Link>
                );
              })}
            </div>
            <Link href="/category/image" className="mt-3 inline-flex items-center gap-1 text-xs font-medium text-emerald-600 dark:text-emerald-400 hover:text-emerald-700 dark:hover:text-emerald-300">
              View all image tools
              <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          {/* AI Coding */}
          <div className="bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 p-5">
            <h3 className="text-sm font-semibold text-zinc-900 dark:text-white mb-3 flex items-center gap-2">
              <Code className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              AI Coding Tools
            </h3>
            <div className="space-y-2">
              {tools.filter(t => t.category === "code").slice(0, 4).map((tool) => {
                const total = calculateScoreResult(tool.scores).total;
                return (
                  <Link key={tool.slug} href={`/tools/${tool.slug}`} className="flex items-center justify-between py-1.5 hover:bg-zinc-50 dark:hover:bg-zinc-800/50 px-2 -mx-2 rounded transition-colors">
                    <span className="text-sm text-zinc-700 dark:text-zinc-300 hover:text-emerald-600 dark:hover:text-emerald-400 font-medium">{tool.name}</span>
                    <span className="text-xs text-zinc-400 dark:text-zinc-500 font-mono">{total.toFixed(1)}</span>
                  </Link>
                );
              })}
            </div>
            <Link href="/category/code" className="mt-3 inline-flex items-center gap-1 text-xs font-medium text-emerald-600 dark:text-emerald-400 hover:text-emerald-700 dark:hover:text-emerald-300">
              View all coding tools
              <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          {/* AI Audio */}
          <div className="bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 p-5">
            <h3 className="text-sm font-semibold text-zinc-900 dark:text-white mb-3 flex items-center gap-2">
              <Music className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              AI Audio & Voice
            </h3>
            <div className="space-y-2">
              {tools.filter(t => t.category === "audio").slice(0, 4).map((tool) => {
                const total = calculateScoreResult(tool.scores).total;
                return (
                  <Link key={tool.slug} href={`/tools/${tool.slug}`} className="flex items-center justify-between py-1.5 hover:bg-zinc-50 dark:hover:bg-zinc-800/50 px-2 -mx-2 rounded transition-colors">
                    <span className="text-sm text-zinc-700 dark:text-zinc-300 hover:text-emerald-600 dark:hover:text-emerald-400 font-medium">{tool.name}</span>
                    <span className="text-xs text-zinc-400 dark:text-zinc-500 font-mono">{total.toFixed(1)}</span>
                  </Link>
                );
              })}
            </div>
            <Link href="/category/audio" className="mt-3 inline-flex items-center gap-1 text-xs font-medium text-emerald-600 dark:text-emerald-400 hover:text-emerald-700 dark:hover:text-emerald-300">
              View all audio tools
              <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          {/* AI Productivity */}
          <div className="bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 p-5">
            <h3 className="text-sm font-semibold text-zinc-900 dark:text-white mb-3 flex items-center gap-2">
              <Briefcase className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              AI Productivity
            </h3>
            <div className="space-y-2">
              {tools.filter(t => t.category === "productivity").slice(0, 4).map((tool) => {
                const total = calculateScoreResult(tool.scores).total;
                return (
                  <Link key={tool.slug} href={`/tools/${tool.slug}`} className="flex items-center justify-between py-1.5 hover:bg-zinc-50 dark:hover:bg-zinc-800/50 px-2 -mx-2 rounded transition-colors">
                    <span className="text-sm text-zinc-700 dark:text-zinc-300 hover:text-emerald-600 dark:hover:text-emerald-400 font-medium">{tool.name}</span>
                    <span className="text-xs text-zinc-400 dark:text-zinc-500 font-mono">{total.toFixed(1)}</span>
                  </Link>
                );
              })}
            </div>
            <Link href="/category/productivity" className="mt-3 inline-flex items-center gap-1 text-xs font-medium text-emerald-600 dark:text-emerald-400 hover:text-emerald-700 dark:hover:text-emerald-300">
              View all productivity tools
              <ArrowRight className="w-3 h-3" />
            </Link>
          </div>
        </div>
      </section>

      {/* === TRENDING RANKING - Left aligned, different layout === */}
      <section className="bg-zinc-50 dark:bg-zinc-900/50 py-16 lg:py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6">
          <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-10 gap-4">
            <div>
              <h2 className="text-2xl sm:text-3xl font-bold text-zinc-900 dark:text-white mb-2">
                Top Rated AI Tools
              </h2>
              <p className="text-zinc-500 dark:text-zinc-400">
                Based on our six-dimension weighted scoring
              </p>
            </div>
            <Link
              href="/ranking"
              className="group inline-flex items-center gap-2 text-sm font-medium text-emerald-600 dark:text-emerald-400 hover:text-emerald-700 dark:hover:text-emerald-300"
            >
              View All Rankings
              <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
            </Link>
          </div>

          <ToolList tools={topTools} />
        </div>
      </section>

      {/* === METHODOLOGY SECTION - Asymmetric 2-col layout === */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 lg:py-20">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
          {/* Left: Sticky header */}
          <div className="lg:col-span-4">
            <div className="lg:sticky lg:top-24">
              <h2 className="text-2xl sm:text-3xl font-bold text-zinc-900 dark:text-white mb-4">
                How We Score
              </h2>
              <p className="text-zinc-500 dark:text-zinc-400 mb-6 leading-relaxed">
                Every tool is evaluated across six dimensions with transparent weighting. No affiliate revenue affects our ratings.
              </p>
              <Link
                href="/methodology"
                className="group inline-flex items-center gap-2 text-sm font-medium text-emerald-600 dark:text-emerald-400 hover:text-emerald-700 dark:hover:text-emerald-300"
              >
                Full Methodology
                <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
              </Link>
            </div>
          </div>

          {/* Right: Methodology items */}
          <div className="lg:col-span-8">
            <div className="space-y-0">
              {METHODOLOGY.map((item, index) => {
                const Icon = item.icon;
                return (
                  <div
                    key={index}
                    className="flex items-start gap-4 py-5 border-b border-zinc-100 dark:border-zinc-800 last:border-0"
                  >
                    <div className="w-10 h-10 flex-shrink-0 flex items-center justify-center rounded-lg bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400">
                      <Icon className="w-5 h-5" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between gap-4 mb-1">
                        <h3 className="text-base font-semibold text-zinc-900 dark:text-white">
                          {item.title}
                        </h3>
                        <span className="text-sm font-bold text-emerald-600 dark:text-emerald-400 flex-shrink-0">
                          {item.weight}
                        </span>
                      </div>
                      <p className="text-sm text-zinc-500 dark:text-zinc-400 leading-relaxed">
                        {item.desc}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </section>

      {/* === LATEST ARTICLES === */}
      {latestPosts.length > 0 && (
        <section className="bg-zinc-50 dark:bg-zinc-900/50 py-16 lg:py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6">
            <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-10 gap-4">
              <div>
                <h2 className="text-2xl sm:text-3xl font-bold text-zinc-900 dark:text-white mb-2">
                  Latest Reviews & Guides
                </h2>
                <p className="text-zinc-500 dark:text-zinc-400">
                  In-depth AI tool reviews and industry insights
                </p>
              </div>
              <Link
                href="/blog"
                className="group inline-flex items-center gap-2 text-sm font-medium text-emerald-600 dark:text-emerald-400 hover:text-emerald-700 dark:hover:text-emerald-300"
              >
                All Articles
                <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
              </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {latestPosts.map((post) => (
                <Link
                  key={post.slug}
                  href={`/blog/${post.slug}`}
                  className="group flex flex-col bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 hover:border-emerald-500 dark:hover:border-emerald-500 hover:shadow-md transition-all overflow-hidden"
                >
                  <div className="h-36 relative overflow-hidden bg-gradient-to-br from-emerald-500/10 via-zinc-100 to-zinc-200 dark:from-emerald-900/20 dark:via-zinc-800 dark:to-zinc-900">
                    {/* Decorative gradient orbs */}
                    <div className="absolute -top-8 -right-8 w-24 h-24 rounded-full bg-emerald-400/20 blur-2xl" />
                    <div className="absolute -bottom-6 -left-6 w-20 h-20 rounded-full bg-emerald-600/15 blur-xl" />
                    {/* Icon */}
                    <div className="absolute inset-0 flex items-center justify-center">
                      <div className="w-14 h-14 flex items-center justify-center rounded-2xl bg-white/80 dark:bg-zinc-900/80 backdrop-blur-sm shadow-md">
                        <PenTool className="w-7 h-7 text-emerald-600 dark:text-emerald-400" />
                      </div>
                    </div>
                    {/* Category badge */}
                    <div className="absolute top-3 left-3">
                      <span className="px-2.5 py-1 bg-white/90 dark:bg-zinc-900/90 backdrop-blur-sm text-zinc-700 dark:text-zinc-300 text-xs font-semibold rounded-md shadow-sm capitalize">
                        {post.category}
                      </span>
                    </div>
                  </div>
                  <div className="p-5 flex-1 flex flex-col">
                    <h3 className="text-base font-semibold text-zinc-900 dark:text-white group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition-colors line-clamp-2 mb-2">
                      {post.title}
                    </h3>
                    <p className="text-sm text-zinc-500 dark:text-zinc-400 line-clamp-2 flex-1 mb-4">
                      {post.excerpt}
                    </p>
                    <div className="flex items-center justify-between text-xs text-zinc-400 dark:text-zinc-500">
                      <span>{post.publishedAt}</span>
                      <span className="inline-flex items-center gap-1 text-emerald-600 dark:text-emerald-400 font-medium group-hover:gap-2 transition-all">
                        Read
                        <ArrowRight className="w-3 h-3" />
                      </span>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* === CTA SECTION - Clean, no gradient === */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 lg:py-20">
        <div className="bg-zinc-900 rounded-2xl p-10 sm:p-14 text-center text-white">
          <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold mb-4">
            Not sure which AI tool to choose?
          </h2>
          <p className="text-zinc-400 mb-8 max-w-xl mx-auto">
            Tell us your use case and priorities, and we'll match you with the perfect AI tool based on our six-dimension scoring.
          </p>
          <Link
            href="/generator"
            className="inline-flex items-center gap-2 px-8 py-3.5 bg-emerald-600 hover:bg-emerald-500 text-white font-medium rounded-lg transition-colors"
          >
            <Sparkles className="w-4 h-4" />
            Start Matching
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </section>

      {/* === NEWSLETTER === */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 pb-16">
        <NewsletterSignup />
      </section>
    </div>
  );
}
