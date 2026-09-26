import type { Metadata } from "next";
import Link from "next/link";
import trafficData from "@/data/traffic-ranking.json";

export const metadata: Metadata = {
  title: "Top AI Tools by Traffic 2026",
  description:
    "Discover the most visited AI tools in 2026 ranked by monthly web traffic. We analyze 50+ leading AI tools with estimated monthly visits, growth rates, and honest reviews.",
  openGraph: {
    title: "Top AI Tools by Traffic 2026 | AIToolCrux",
    description: "The most visited AI tools ranked by monthly traffic. Updated weekly.",
    type: "website",
  },
  alternates: {
    canonical: "https://www.aitoolcrux.com/top-ai-tools-by-traffic",
  },
};

type TrafficEntry = {
  rank: number;
  name: string;
  slug: string;
  monthlyVisits: string;
  visitsNum: number;
  growth: string;
  description: string;
};

const data = trafficData as TrafficEntry[];

function formatVisits(n: number): string {
  if (n >= 1e9) return (n / 1e9).toFixed(1) + "B";
  if (n >= 1e6) return (n / 1e6).toFixed(0) + "M";
  if (n >= 1e3) return (n / 1e3).toFixed(0) + "K";
  return String(n);
}

function growthBadge(g: string) {
  const up = g.startsWith("+");
  const color = up
    ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400"
    : "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400";
  return (
    <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-semibold ${color}`}>
      {g}
    </span>
  );
}

export default function TrafficRankingPage() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* JSON-LD */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            name: "Top AI Tools by Traffic 2026",
            description:
              "Ranking of the most visited AI tools by monthly web traffic.",
            url: "https://www.aitoolcrux.com/top-ai-tools-by-traffic",
            isPartOf: {
              "@type": "WebSite",
              name: "AIToolCrux",
              url: "https://www.aitoolcrux.com",
            },
          }),
        }}
      />

      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        {/* Hero */}
        <div className="mb-8">
          <nav className="text-sm text-gray-500 dark:text-gray-400 mb-4">
            <Link href="/" className="hover:text-emerald-600">Home</Link>
            <span className="mx-2">/</span>
            <span>Top AI Tools by Traffic</span>
          </nav>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-gray-900 dark:text-white mb-3">
            Top 50 AI Tools by{" "}
            <span className="bg-gradient-to-r from-emerald-600 to-cyan-600 bg-clip-text text-transparent">
              Monthly Traffic
            </span>
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-400 max-w-3xl">
            The most visited AI tools of 2026, ranked by estimated monthly web
            visits. Data updated weekly from SimilarWeb and public analytics.
          </p>
          <div className="mt-4 flex flex-wrap gap-2 text-sm">
            <span className="px-3 py-1 rounded-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-300">
              50 tools ranked
            </span>
            <span className="px-3 py-1 rounded-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-300">
              Updated weekly
            </span>
            <span className="px-3 py-1 rounded-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-300">
              Source: SimilarWeb estimates
            </span>
          </div>
        </div>

        {/* Ranking table */}
        <div className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 overflow-hidden shadow-sm">
          {/* Header */}
          <div className="hidden md:grid grid-cols-12 gap-4 px-6 py-4 bg-gray-50 dark:bg-gray-800/50 border-b border-gray-200 dark:border-gray-800 text-sm font-semibold text-gray-500 dark:text-gray-400">
            <div className="col-span-1">#</div>
            <div className="col-span-4">Tool</div>
            <div className="col-span-2 text-right">Monthly Visits</div>
            <div className="col-span-2 text-right">Growth</div>
            <div className="col-span-3">Description</div>
          </div>

          {data.map((tool, idx) => (
            <div
              key={tool.slug + idx}
              className={`grid grid-cols-12 gap-4 px-6 py-4 items-center border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/30 transition-colors ${
                idx === data.length - 1 ? "border-b-0" : ""
              }`}
            >
              <div className="col-span-1">
                <div
                  className={`w-8 h-8 flex items-center justify-center rounded-lg text-sm font-bold ${
                    tool.rank <= 3
                      ? "bg-gradient-to-br from-amber-400 to-orange-500 text-white"
                      : "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400"
                  }`}
                >
                  {tool.rank}
                </div>
              </div>
              <div className="col-span-4">
                <Link
                  href={`/tools/${tool.slug}`}
                  prefetch={false}
                  className="font-semibold text-gray-900 dark:text-white hover:text-emerald-600 dark:hover:text-emerald-400"
                >
                  {tool.name}
                </Link>
              </div>
              <div className="col-span-2 text-right">
                <span className="font-mono font-bold text-gray-900 dark:text-white">
                  {tool.monthlyVisits}
                </span>
              </div>
              <div className="col-span-2 text-right">{growthBadge(tool.growth)}</div>
              <div className="col-span-3 text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
                {tool.description}
              </div>
            </div>
          ))}
        </div>

        {/* Disclaimer */}
        <div className="mt-8 p-6 bg-gray-50 dark:bg-gray-800/50 rounded-xl text-sm text-gray-500 dark:text-gray-400">
          <p className="font-semibold text-gray-700 dark:text-gray-300 mb-2">
            About This Ranking
          </p>
          <p>
            Traffic estimates are based on SimilarWeb public data and industry
            reports as of September 2026. Actual visits may vary. This ranking
            is updated weekly. We independently review every tool listed — see
            our{" "}
            <Link href="/about" className="text-emerald-600 hover:underline">
              methodology
            </Link>{" "}
            for details.
          </p>
        </div>
      </div>
    </div>
  );
}
