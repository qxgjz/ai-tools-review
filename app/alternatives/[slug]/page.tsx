import { Metadata } from "next";
import Link from "next/link";
import { Zap, BookOpen, CheckCircle2, Star, Lightbulb, Award } from "lucide-react";
import { notFound } from "next/navigation";
import alternativesData from "@/data/alternatives.json";
import toolsData from "@/data/tools.json";
import { FAQSchema, BreadcrumbSchema } from "@/components/seo/Schema";
import { AffiliateCTA } from "@/components/monetization/AffiliateCTA";

interface Alternative {
  slug: string;
  name: string;
  rating: number;
  reason: string;
  pricing: string;
}

interface ComparisonRow {
  feature: string;
  bestAlternative: string;
  [key: string]: string;
}

interface FAQ {
  question: string;
  answer: string;
}

interface AlternativePage {
  slug: string;
  title: string;
  description: string;
  keywords: string[];
  targetTool: string;
  intro: string;
  alternatives: Alternative[];
  comparisonTable: ComparisonRow[];
  faq: FAQ[];
}


// ISR: revalidate alternatives every 24h
export const revalidate = 86400;

export function generateStaticParams() {
  return alternativesData.map((item: AlternativePage) => ({
    slug: item.slug,
  }));
}

export async function generateMetadata({
  params,
}: {
  params: { slug: string };
}): Promise<Metadata> {
  const page = alternativesData.find(
    (item: AlternativePage) => item.slug === params.slug
  );

  if (!page) {
    return {
      title: "Alternatives Not Found | AIToolCrux",
    };
  }

  return {
    title: page.title.length > 60 ? page.title.slice(0, 57) + "..." : page.title,
    description: page.description,
    keywords: page.keywords.join(", "),
    alternates: {
      canonical: `https://www.aitoolcrux.com/alternatives/${page.slug}`,
    },
    openGraph: {
      title: page.title.length > 60 ? page.title.slice(0, 57) + "..." : page.title,
      description: page.description,
      url: `https://www.aitoolcrux.com/alternatives/${page.slug}`,
      type: "article",
      siteName: "AIToolCrux",
    },
    twitter: {
      card: "summary_large_image",
      title: page.title.length > 60 ? page.title.slice(0, 57) + "..." : page.title,
      description: page.description,
    },
  };
}

export default function AlternativePage({
  params,
}: {
  params: { slug: string };
}) {
  const page = alternativesData.find(
    (item: AlternativePage) => item.slug === params.slug
  );

  if (!page) {
    notFound();
  }

  const targetTool = toolsData.find((t: any) => t.slug === page.targetTool);

  return (
    <div className="min-h-screen bg-white dark:bg-gray-950">
      {/* Structured Data */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "Article",
            headline: page.title,
            description: page.description,
            url: `https://www.aitoolcrux.com/alternatives/${page.slug}`,
            author: {
              "@type": "Organization",
              name: "AIToolCrux Editorial Team",
            },
            datePublished: "2026-09-11",
            dateModified: "2026-09-11",
            publisher: {
              "@type": "Organization",
              name: "AIToolCrux",
            },
          }),
        }}
      />
      <FAQSchema faqs={page.faq.map((f) => ({ question: f.question, answer: f.answer }))} />
      <BreadcrumbSchema
        items={[
          { name: "Home", url: "https://www.aitoolcrux.com" },
          { name: "Alternatives", url: "https://www.aitoolcrux.com/alternatives" },
          { name: page.title.split(":")[0], url: `https://www.aitoolcrux.com/alternatives/${page.slug}` },
        ]}
      />

      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950/30 dark:to-indigo-950/30 py-16 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <nav className="text-sm text-gray-500 dark:text-gray-400 mb-4">
            <Link href="/" className="hover:text-blue-600">Home</Link>
            <span className="mx-2">/</span>
            <Link href="/alternatives" className="hover:text-blue-600">Alternatives</Link>
            <span className="mx-2">/</span>
            <span className="text-gray-700 dark:text-gray-300">{page.title.split(":")[0]}</span>
          </nav>
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4 leading-tight">
            {page.title}
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            {page.description}
          </p>
          <div className="mt-6 flex flex-wrap justify-center gap-2">
            {page.keywords.slice(0, 4).map((keyword, i) => (
              <span
                key={i}
                className="px-3 py-1 bg-white dark:bg-gray-800 rounded-full text-sm text-gray-600 dark:text-gray-300 shadow-sm"
              >
                {keyword}
              </span>
            ))}
          </div>
        </div>
      </section>

      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* AEO/GEO Optimization: Quick Answer - Answer First for AI Search Citation */}
        <section className="bg-emerald-50 dark:bg-emerald-950/20 rounded-xl border border-emerald-100 dark:border-emerald-900/50 p-6 sm:p-8 mb-8">
          <div className="flex items-center gap-2 mb-4">
            <Zap className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
            <h2 className="text-xl font-bold text-zinc-900 dark:text-white">Quick Answer</h2>
          </div>
          <div className="space-y-4">
            <div>
              <h3 className="font-semibold text-zinc-800 dark:text-zinc-200 mb-2">What are the best {page.targetTool} alternatives?</h3>
              <p className="text-zinc-700 dark:text-zinc-300 leading-relaxed">Based on our comprehensive six-dimension evaluation, the top {page.alternatives.length} alternatives to {page.targetTool} are {page.alternatives.slice(0, 3).map(a => a.name).join(", ")}. Each alternative offers different strengths in features, pricing, and use cases.</p>
            </div>
            <div>
              <h3 className="font-semibold text-zinc-800 dark:text-zinc-200 mb-2">Which alternative is best for me?</h3>
              <p className="text-zinc-700 dark:text-zinc-300 leading-relaxed">The best alternative depends on your specific needs: {page.alternatives[0]?.name} is ideal for {page.alternatives[0]?.reason || "most users"}, while {page.alternatives[1]?.name} excels at {page.alternatives[1]?.reason || "specific use cases"}. Compare features and pricing side-by-side below to find your best fit.</p>
            </div>
            <div>
              <h3 className="font-semibold text-zinc-800 dark:text-zinc-200 mb-2">Are these alternatives free to use?</h3>
              <p className="text-zinc-700 dark:text-zinc-300 leading-relaxed">Most alternatives offer free tiers or free trials. {page.alternatives.filter(a => (a.pricing || "").toLowerCase().includes("free") || (a.pricing || "").includes("$0")).length} of {page.alternatives.length} tools have free options available. We recommend starting with the free plan to evaluate whether the tool meets your needs before upgrading.</p>
            </div>
          </div>
        </section>

        {/* AEO/GEO Optimization: Key Takeaways - Structured for AI Citation */}
        <section className="bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 p-6 sm:p-8 mb-8">
          <div className="flex items-center gap-2 mb-4">
            <BookOpen className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
            <h2 className="text-xl font-bold text-zinc-900 dark:text-white">Key Takeaways</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 flex-shrink-0 flex items-center justify-center rounded-lg bg-emerald-100 dark:bg-emerald-900/30">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              </div>
              <div>
                <h4 className="font-semibold text-zinc-800 dark:text-zinc-200 text-sm">Best Overall</h4>
                <p className="text-zinc-600 dark:text-zinc-400 text-sm">{page.alternatives[0]?.name || "Top pick"} - {page.alternatives[0]?.reason || "Best overall alternative based on our comprehensive evaluation"}.</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 flex-shrink-0 flex items-center justify-center rounded-lg bg-blue-100 dark:bg-blue-900/30">
                <Star className="w-4 h-4 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <h4 className="font-semibold text-zinc-800 dark:text-zinc-200 text-sm">Top Rated</h4>
                <p className="text-zinc-600 dark:text-zinc-400 text-sm">{page.alternatives[0]?.rating || "N/A"}/10 average rating across {page.alternatives.length} alternatives, independently evaluated by our editorial team.</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 flex-shrink-0 flex items-center justify-center rounded-lg bg-amber-100 dark:bg-amber-900/30">
                <Lightbulb className="w-4 h-4 text-amber-600 dark:text-amber-400" />
              </div>
              <div>
                <h4 className="font-semibold text-zinc-800 dark:text-zinc-200 text-sm">Key Consideration</h4>
                <p className="text-zinc-600 dark:text-zinc-400 text-sm">Evaluate features, pricing, learning curve, and integration options. The cheapest option isn&apos;t always the best value long-term.</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 flex-shrink-0 flex items-center justify-center rounded-lg bg-purple-100 dark:bg-purple-900/30">
                <Award className="w-4 h-4 text-purple-600 dark:text-purple-400" />
              </div>
              <div>
                <h4 className="font-semibold text-zinc-800 dark:text-zinc-200 text-sm">Expert Verdict</h4>
                <p className="text-zinc-600 dark:text-zinc-400 text-sm">Read detailed reviews below for each alternative, including pros, cons, pricing, and real-world use cases to make an informed decision.</p>
              </div>
            </div>
          </div>
          <div className="mt-6 pt-4 border-t border-zinc-100 dark:border-zinc-800">
            <p className="text-xs text-zinc-500 dark:text-zinc-400">
              <strong>Source:</strong> AIToolCrux Editorial Team | <strong>Last updated:</strong> 2026-09-11 | <strong>Methodology:</strong> Six-dimension evaluation | <Link href="/methodology" className="text-emerald-600 dark:text-emerald-400 hover:underline">Full methodology</Link>
            </p>
          </div>
        </section>

        {/* Introduction */}
        <section className="mb-12">
          <div className="prose prose-lg dark:prose-invert max-w-none">
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed text-lg">
              {page.intro}
            </p>
          </div>
        </section>

        {/* Quick Summary Table */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
            Quick Comparison: Top {page.alternatives.length} Alternatives
          </h2>
          <div className="overflow-x-auto rounded-xl border border-gray-200 dark:border-gray-700">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 dark:bg-gray-800">
                <tr>
                  <th className="px-4 py-3 text-left font-semibold text-gray-900 dark:text-white">Rank</th>
                  <th className="px-4 py-3 text-left font-semibold text-gray-900 dark:text-white">Tool</th>
                  <th className="px-4 py-3 text-left font-semibold text-gray-900 dark:text-white">Rating</th>
                  <th className="px-4 py-3 text-left font-semibold text-gray-900 dark:text-white">Best For</th>
                  <th className="px-4 py-3 text-left font-semibold text-gray-900 dark:text-white">Pricing</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                {page.alternatives.map((alt, i) => (
                  <tr key={alt.slug} className="hover:bg-gray-50 dark:hover:bg-gray-800/50">
                    <td className="px-4 py-3 font-bold text-gray-900 dark:text-white">#{i + 1}</td>
                    <td className="px-4 py-3">
                      <Link
                        href={`/tools/${alt.slug}`}
                        className="font-semibold text-blue-600 dark:text-blue-400 hover:underline"
                      >
                        {alt.name}
                      </Link>
                    </td>
                    <td className="px-4 py-3">
                      <span className="inline-flex items-center px-2 py-1 rounded-full bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-200 font-semibold">
                        {alt.rating}/10
                      </span>
                    </td>
                    <td className="px-4 py-3 text-gray-600 dark:text-gray-300">{alt.reason}</td>
                    <td className="px-4 py-3 text-gray-600 dark:text-gray-300 font-medium">{alt.pricing}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* Detailed Alternatives */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
            Detailed Reviews of Each Alternative
          </h2>
          <div className="space-y-6">
            {page.alternatives.map((alt, i) => (
              <div
                key={alt.slug}
                className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 p-6 shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white">
                      #{i + 1} {alt.name}
                    </h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                      Rating: <span className="font-semibold text-green-600">{alt.rating}/10</span>
                    </p>
                  </div>
                  <Link
                    href={`/tools/${alt.slug}`}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold text-sm hover:bg-blue-700 transition-colors"
                  >
                    Full Review →
                  </Link>
                </div>
                <p className="text-gray-700 dark:text-gray-300 mb-3">
                  <span className="font-semibold">Why it's a great alternative:</span> {alt.reason}
                </p>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  <span className="font-semibold">Pricing:</span> {alt.pricing}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* Feature Comparison Table */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
            Feature Comparison: {page.targetTool.charAt(0).toUpperCase() + page.targetTool.slice(1)} vs Alternatives
          </h2>
          <div className="overflow-x-auto rounded-xl border border-gray-200 dark:border-gray-700">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 dark:bg-gray-800">
                <tr>
                  <th className="px-4 py-3 text-left font-semibold text-gray-900 dark:text-white">Feature</th>
                  <th className="px-4 py-3 text-left font-semibold text-gray-900 dark:text-white">
                    {page.targetTool.charAt(0).toUpperCase() + page.targetTool.slice(1)}
                  </th>
                  <th className="px-4 py-3 text-left font-semibold text-gray-900 dark:text-white">Best Alternative</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                {(page.comparisonTable as ComparisonRow[]).map((row, i) => (
                  <tr key={i} className="hover:bg-gray-50 dark:hover:bg-gray-800/50">
                    <td className="px-4 py-3 font-medium text-gray-900 dark:text-white">{row.feature}</td>
                    <td className="px-4 py-3 text-gray-600 dark:text-gray-300">{row[page.targetTool] || "N/A"}</td>
                    <td className="px-4 py-3 text-gray-600 dark:text-gray-300">{row.bestAlternative}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* CTA */}
        {targetTool && (
          <div className="mb-12">
            <AffiliateCTA
              toolName={targetTool.name}
              officialUrl={targetTool.officialUrl}
              description={`Still considering ${targetTool.name}? Read our full review to see how it compares.`}
              variant="banner"
            />
          </div>
        )}

        {/* FAQ Section */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
            Frequently Asked Questions
          </h2>
          <div className="space-y-4">
            {page.faq.map((faq, i) => (
              <div
                key={i}
                className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 p-6"
              >
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                  {faq.question}
                </h3>
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                  {faq.answer}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* Bottom CTA */}
        <section className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl p-8 text-center text-white">
          <h2 className="text-2xl font-bold mb-3">
            Still Not Sure Which Tool to Choose?
          </h2>
          <p className="text-blue-100 mb-6 max-w-xl mx-auto">
            Use our AI tool comparison tool to compare up to 3 tools side-by-side and find the perfect fit for your needs.
          </p>
          <Link
            href="/compare"
            className="inline-flex items-center gap-2 px-8 py-3 bg-white text-blue-600 rounded-lg font-bold hover:bg-blue-50 transition-colors"
          >
            Compare Tools Now
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </Link>
        </section>
      </div>
    </div>
  );
}
