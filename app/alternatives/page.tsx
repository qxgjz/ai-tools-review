import { Metadata } from "next";
import Link from "next/link";
import alternativesData from "@/data/alternatives.json";

export const metadata: Metadata = {
  title: "Best AI Tool Alternatives 2026: Comprehensive Comparison Guide | AIToolCrux",
  description: "Discover the best alternatives to popular AI tools. Compare ChatGPT alternatives, Midjourney alternatives, Jasper alternatives, and more. Find the perfect AI tool for your needs.",
  keywords: "ai tool alternatives, chatgpt alternatives, midjourney alternatives, jasper alternatives, best ai tools",
  alternates: {
    canonical: "https://www.aitoolcrux.com/alternatives",
  },
};

export default function AlternativesPage() {
  return (
    <div className="min-h-screen bg-white dark:bg-gray-950">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950/30 dark:to-indigo-950/30 py-16 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4 leading-tight">
            Best AI Tool Alternatives 2026
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Find the perfect alternative to your favorite AI tools. We've tested and compared the top alternatives to help you make an informed decision.
          </p>
        </div>
      </section>

      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* Introduction */}
        <section className="mb-12">
          <div className="prose prose-lg dark:prose-invert max-w-none">
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              The AI tool landscape is evolving rapidly, and there are often excellent alternatives to the most popular tools. Whether you're looking for better value, different features, improved privacy, or specialized capabilities, our comprehensive alternative guides help you find the right tool for your specific needs.
            </p>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              Each alternative guide includes detailed comparisons, pricing information, feature breakdowns, and real-world use cases to help you make the best choice.
            </p>
          </div>
        </section>

        {/* Alternatives Grid */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
            Browse All Alternative Guides
          </h2>
          <div className="grid gap-6 md:grid-cols-2">
            {alternativesData.map((item: any) => (
              <Link
                key={item.slug}
                href={`/alternatives/${item.slug}`}
                className="group bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 p-6 shadow-sm hover:shadow-lg hover:border-blue-300 dark:hover:border-blue-700 transition-all"
              >
                <div className="flex items-start justify-between mb-3">
                  <h3 className="text-lg font-bold text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                    {item.title.split(":")[0]}
                  </h3>
                  <span className="text-blue-600 dark:text-blue-400 group-hover:translate-x-1 transition-transform">
                    →
                  </span>
                </div>
                <p className="text-gray-600 dark:text-gray-300 text-sm mb-4 line-clamp-3">
                  {item.description}
                </p>
                <div className="flex flex-wrap gap-2">
                  {item.keywords.slice(0, 3).map((keyword: string, i: number) => (
                    <span
                      key={i}
                      className="px-2 py-1 bg-gray-100 dark:bg-gray-800 rounded-full text-xs text-gray-600 dark:text-gray-400"
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
                <div className="mt-4 pt-4 border-t border-gray-100 dark:border-gray-800">
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    <span className="font-semibold text-gray-700 dark:text-gray-300">{item.alternatives.length}</span> alternatives compared
                  </p>
                </div>
              </Link>
            ))}
          </div>
        </section>

        {/* Why Choose Alternatives */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
            Why Explore AI Tool Alternatives?
          </h2>
          <div className="grid gap-6 md:grid-cols-3">
            <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
              <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/50 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">Better Value</h3>
              <p className="text-gray-600 dark:text-gray-300 text-sm">
                Many alternatives offer similar or better features at a lower price point, helping you get more value for your budget.
              </p>
            </div>
            <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
              <div className="w-12 h-12 bg-green-100 dark:bg-green-900/50 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">Specialized Features</h3>
              <p className="text-gray-600 dark:text-gray-300 text-sm">
                Alternatives often specialize in specific use cases, offering features that general-purpose tools may lack.
              </p>
            </div>
            <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
              <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/50 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">Privacy & Control</h3>
              <p className="text-gray-600 dark:text-gray-300 text-sm">
                Open-source and self-hostable alternatives give you greater control over your data and privacy.
              </p>
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl p-8 text-center text-white">
          <h2 className="text-2xl font-bold mb-3">
            Can't Find What You're Looking For?
          </h2>
          <p className="text-blue-100 mb-6 max-w-xl mx-auto">
            Browse our complete directory of 533+ AI tools or use our comparison tool to find the perfect tool for your needs.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link
              href="/ranking"
              className="inline-flex items-center gap-2 px-6 py-3 bg-white text-blue-600 rounded-lg font-bold hover:bg-blue-50 transition-colors"
            >
              Browse All Tools
            </Link>
            <Link
              href="/compare"
              className="inline-flex items-center gap-2 px-6 py-3 bg-blue-700 text-white rounded-lg font-bold hover:bg-blue-800 transition-colors border border-blue-500"
            >
              Compare Tools
            </Link>
          </div>
        </section>
      </div>
    </div>
  );
}
