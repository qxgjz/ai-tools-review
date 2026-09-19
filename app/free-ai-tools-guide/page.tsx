import Link from "next/link";
import posts from "@/data/posts.json";

export const metadata = {
  title: "Free AI Tools Guide: No Credit Card, No Hidden Fees",
  description:
    "Curated guide to the best free AI tools in 2026. No credit card required, no hidden fees. Image generation, writing, video, and design tools you can use for free today.",
  alternates: {
    canonical: "https://www.aitoolcrux.com/free-ai-tools-guide",
  },
};

// Categorize articles by topic
const categories = [
  {
    title: "Image Generation",
    description: "Free AI image generators, art tools, and photo editors",
    slugs: [
      "best-ai-image-generators-2026",
      "midjourney-review-2026",
      "dall-e-3-review-2026",
      "stable-diffusion-review-2026",
      "leonardo-ai-review-2026",
      "adobe-firefly-review-2026",
      "midjourney-alternatives-2026",
      "stable-diffusion-alternatives-2026",
      "midjourney-vs-dalle-3-2026-comparison",
      "best-ai-photo-editors-2026",
      "best-ai-logo-generators-2026",
    ],
  },
  {
    title: "Writing & Content",
    description: "Free AI writing assistants, grammar checkers, and email tools",
    slugs: [
      "best-ai-writing-tools-2026",
      "copy-ai-review-2026",
      "jasper-review-2026",
      "writesonic-review-2026",
      "best-ai-grammar-checkers-2026",
      "best-ai-email-tools-2026",
      "best-free-ai-tools-2026",
      "ai-tools-for-beginners-2026",
    ],
  },
  {
    title: "Video & Audio",
    description: "Free AI video generators, voice tools, and audio editors",
    slugs: [
      "best-ai-video-generators-2026",
      "best-ai-video-editors-2026",
      "runway-review-2026",
      "sora-review-2026",
      "pika-review-2026",
      "kling-review-2026",
      "synthesia-review-2026",
      "heygen-review-2026",
      "elevenlabs-review-2026",
      "best-ai-voice-generators-2026",
      "best-ai-audio-tools-2026",
    ],
  },
  {
    title: "Design & Productivity",
    description: "Free AI design tools, presentation makers, and productivity apps",
    slugs: [
      "best-ai-design-tools-2026",
      "figma-ai-review-2026",
      "best-ai-presentation-tools-2026",
      "best-ai-productivity-tools-2026",
      "best-ai-note-taking-tools-2026",
      "best-ai-scheduling-tools-2026",
    ],
  },
];

export default function FreeAIGuidePage() {
  const allPosts = posts as any[];

  // Build a slug -> post map for quick lookup
  const postMap: Record<string, any> = {};
  for (const p of allPosts) {
    postMap[p.slug] = p;
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-12">
      {/* Hero */}
      <div className="mb-12 text-center">
        <h1 className="text-4xl sm:text-5xl font-extrabold text-gray-900 dark:text-white mb-4">
          Free AI Tools Guide
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-400 mb-2">
          No Credit Card · No Hidden Fees · Start Today
        </p>
        <p className="text-sm text-gray-500 dark:text-gray-500 max-w-2xl mx-auto">
          Every tool listed below has a genuinely free tier or free plan. We
          tested them all — no upsell traps, no "free trial" that vanishes in 7
          days.
        </p>
      </div>

      {/* Categories */}
      <div className="space-y-10">
        {categories.map((cat) => {
          // Look up posts for this category
          const catPosts = cat.slugs
            .map((slug) => postMap[slug])
            .filter(Boolean);

          if (catPosts.length === 0) return null;

          return (
            <section key={cat.title}>
              <div className="mb-5">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
                  {cat.title}
                </h2>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  {cat.description}
                </p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {catPosts.map((post) => (
                  <Link
                    key={post.slug}
                    href={`/blog/${post.slug}`}
                    className="block bg-white dark:bg-zinc-900 rounded-xl border border-gray-200 dark:border-zinc-800 p-5 hover:shadow-lg hover:border-emerald-300 dark:hover:border-emerald-700 transition-all"
                  >
                    <h3 className="font-semibold text-gray-900 dark:text-white text-sm mb-2 leading-snug">
                      {post.title}
                    </h3>
                    <p className="text-xs text-gray-500 dark:text-gray-400 line-clamp-2">
                      {post.excerpt || ""}
                    </p>
                    <span className="inline-flex items-center gap-1 text-xs font-medium text-emerald-600 dark:text-emerald-400 mt-3">
                      Read Guide →
                    </span>
                  </Link>
                ))}
              </div>
            </section>
          );
        })}
      </div>

      {/* Footer note */}
      <div className="mt-16 p-6 bg-emerald-50 dark:bg-emerald-900/10 rounded-xl border border-emerald-200 dark:border-emerald-900/30 text-center">
        <p className="text-sm text-emerald-800 dark:text-emerald-300">
          💡 All tools on this page were hands-on tested by our team. Pricing
          and free tiers change — always verify on the official site before
          signing up.
        </p>
      </div>
    </div>
  );
}
