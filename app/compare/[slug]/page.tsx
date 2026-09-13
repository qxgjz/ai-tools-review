import { notFound } from "next/navigation";
import Link from "next/link";
import {
  ArrowLeft,
  Check,
  X,
  Trophy,
  Zap,
  Target,
  Users,
  Clock,
  DollarSign,
  Sparkles,
  ShieldCheck,
  Lightbulb,
  GitCompare,
  Award,
  ExternalLink,
  BookOpen,
  TrendingUp,
} from "lucide-react";
import comparisonsData from "@/data/comparisons.json";
import toolsData from "@/data/tools.json";
import type { Tool } from "@/types";
import { calculateScoreResult, DIMENSION_LABELS } from "@/lib/scoring";
import { RadarChart } from "@/components/charts/RadarChart";
import { MultiRadarChart } from "@/components/charts/MultiRadarChart";
import { FAQSection } from "@/components/content/FAQSection";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { FadeIn } from "@/components/animations";
import {
  BreadcrumbSchema,
  FAQSchema,
  ComparisonSchema,
} from "@/components/seo/Schema";

interface ComparisonPageProps {
  params: { slug: string };
}

export function generateStaticParams() {
  return comparisonsData.map((c: any) => ({ slug: c.slug }));
}

export function generateMetadata({ params }: ComparisonPageProps) {
  const comparison = comparisonsData.find((c: any) => c.slug === params.slug);
  if (!comparison) return {};

  return {
    title: comparison.title,
    description: comparison.metaDescription,
    keywords: `${comparison.toolA.name} vs ${comparison.toolB.name}, ${comparison.toolA.name} comparison, ${comparison.toolB.name} comparison, best AI tool 2026`,
    openGraph: {
      title: comparison.title,
      description: comparison.metaDescription,
      type: "article",
      url: `https://www.aitoolcrux.com/compare/${comparison.slug}`,
    },
    alternates: {
      canonical: `https://www.aitoolcrux.com/compare/${comparison.slug}`,
    },
  };
}

export default function ComparisonPage({ params }: ComparisonPageProps) {
  const comparison = comparisonsData.find((c: any) => c.slug === params.slug);
  if (!comparison) notFound();

  const toolA = toolsData.find((t: Tool) => t.slug === comparison.toolA.slug);
  const toolB = toolsData.find((t: Tool) => t.slug === comparison.toolB.slug);

  const scoreA = toolA ? calculateScoreResult(toolA.scores) : null;
  const scoreB = toolB ? calculateScoreResult(toolB.scores) : null;

  // Generate FAQs from comparison data
  const faqs = [
    {
      question: `Which is better: ${comparison.toolA.name} or ${comparison.toolB.name}?`,
      answer: comparison.quickAnswer,
    },
    {
      question: `How much does ${comparison.toolA.name} cost compared to ${comparison.toolB.name}?`,
      answer: `${comparison.toolA.name} and ${comparison.toolB.name} have different pricing models. ${comparison.toolA.name} is developed by ${comparison.toolA.vendor}, while ${comparison.toolB.name} is developed by ${comparison.toolB.vendor}. Visit their official websites for the most current pricing information. Both typically offer free tiers or trials.`,
    },
    {
      question: `Can I use both ${comparison.toolA.name} and ${comparison.toolB.name}?`,
      answer: `Yes! Many professionals use both ${comparison.toolA.name} and ${comparison.toolB.name} for different purposes. ${comparison.toolA.name} excels in certain areas while ${comparison.toolB.name} has different strengths. Using both allows you to leverage the unique capabilities of each tool for different tasks and use cases.`,
    },
    {
      question: `Which tool is better for beginners?`,
      answer: `For beginners, the better choice depends on your specific needs. ${comparison.toolA.name} and ${comparison.toolB.name} both offer user-friendly interfaces. We recommend trying the free tier of both tools to see which interface and capabilities better match your workflow and preferences.`,
    },
    {
      question: `Do these tools offer free trials or free plans?`,
      answer: `Most AI tools offer some form of free tier or trial period. ${comparison.toolA.name} and ${comparison.toolB.name} typically provide free plans with limited features or usage limits. We recommend starting with the free plan to evaluate whether the tool meets your needs before upgrading to a paid subscription. Check their official websites for current free trial offers.`,
    },
  ];

  const comparisonDimensions = [
    { label: "Overall Score", a: scoreA?.total?.toFixed(1) || "N/A", b: scoreB?.total?.toFixed(1) || "N/A" },
    { label: "Developer/Vendor", a: comparison.toolA.vendor, b: comparison.toolB.vendor },
    { label: "Category", a: toolA?.category || "AI Tool", b: toolB?.category || "AI Tool" },
    { label: "Free Tier", a: toolA?.hasFreeTier ? "Yes" : "Check website", b: toolB?.hasFreeTier ? "Yes" : "Check website" },
  ];

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8">
      {/* Structured Data */}
      <BreadcrumbSchema
        items={[
          { name: "Home", url: "https://www.aitoolcrux.com" },
          { name: "Compare", url: "https://www.aitoolcrux.com/compare" },
          { name: `${comparison.toolA.name} vs ${comparison.toolB.name}`, url: `https://www.aitoolcrux.com/compare/${comparison.slug}` },
        ]}
      />
      <FAQSchema faqs={faqs.map((f) => ({ question: f.question, answer: f.answer }))} />
      <ComparisonSchema
        name={comparison.title}
        description={comparison.metaDescription}
        items={[
          {
            name: comparison.toolA.name,
            description: toolA?.description || "",
            ratingValue: scoreA?.total,
            url: `https://www.aitoolcrux.com/tools/${comparison.toolA.slug}`,
          },
          {
            name: comparison.toolB.name,
            description: toolB?.description || "",
            ratingValue: scoreB?.total,
            url: `https://www.aitoolcrux.com/tools/${comparison.toolB.slug}`,
          },
        ]}
        datePublished="2026-09-13"
      />

      {/* Breadcrumb */}
      <Breadcrumb
        items={[
          { name: "Home", url: "/" },
          { name: "Compare", url: "/compare" },
          { name: `${comparison.toolA.name} vs ${comparison.toolB.name}` },
        ]}
      />

      {/* Header */}
      <FadeIn>
        <div className="text-center mb-8 mt-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 bg-blue-50 dark:bg-blue-950/30 text-blue-600 dark:text-blue-400 rounded-full text-xs font-medium mb-4">
            <GitCompare className="w-3.5 h-3.5" />
            Detailed Comparison 2026
          </div>
          <h1 className="text-3xl sm:text-4xl font-bold text-zinc-900 dark:text-white mb-4 leading-tight">
            {comparison.title}
          </h1>
          <p className="text-base text-zinc-600 dark:text-zinc-400 max-w-2xl mx-auto">
            {comparison.metaDescription}
          </p>
        </div>
      </FadeIn>

      {/* Quick Answer */}
      <FadeIn delay={0.1}>
        <div className="bg-gradient-to-br from-emerald-50 to-teal-50 dark:from-emerald-950/20 dark:to-teal-950/20 border border-emerald-200 dark:border-emerald-900/30 rounded-2xl p-6 mb-8">
          <h2 className="text-lg font-bold text-emerald-800 dark:text-emerald-400 mb-3 flex items-center gap-2">
            <Lightbulb className="w-5 h-5" />
            Quick Answer
          </h2>
          <p className="text-sm text-emerald-900 dark:text-emerald-200 leading-relaxed">
            {comparison.quickAnswer}
          </p>
        </div>
      </FadeIn>

      {/* Key Takeaways */}
      <FadeIn delay={0.15}>
        <div className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 p-6 mb-8">
          <h2 className="text-lg font-bold text-zinc-900 dark:text-white mb-4 flex items-center gap-2">
            <Trophy className="w-5 h-5 text-amber-500" />
            Key Takeaways
          </h2>
          <ul className="space-y-3">
            {comparison.keyTakeaways.map((takeaway: string, i: number) => (
              <li key={i} className="flex items-start gap-3">
                <span className="flex-shrink-0 w-6 h-6 bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-full text-xs font-bold flex items-center justify-center mt-0.5">
                  {i + 1}
                </span>
                <span className="text-sm text-zinc-700 dark:text-zinc-300 leading-relaxed">
                  {takeaway}
                </span>
              </li>
            ))}
          </ul>
        </div>
      </FadeIn>

      {/* Score Comparison */}
      {scoreA && scoreB && (
        <FadeIn delay={0.2}>
          <div className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 p-6 mb-8">
            <h2 className="text-lg font-bold text-zinc-900 dark:text-white mb-6 flex items-center gap-2">
              <Award className="w-5 h-5 text-purple-500" />
              Score Comparison
            </h2>
            <div className="grid grid-cols-2 gap-6">
              <div className="text-center">
                <Link href={`/tools/${comparison.toolA.slug}`} className="block">
                  <div className="text-4xl font-bold text-blue-600 dark:text-blue-400 mb-1">
                    {scoreA.total?.toFixed(1)}
                  </div>
                  <div className="text-sm font-semibold text-zinc-900 dark:text-white">
                    {comparison.toolA.name}
                  </div>
                  <div className="text-xs text-zinc-500 dark:text-zinc-400">
                    {scoreA.grade} Grade
                  </div>
                </Link>
              </div>
              <div className="text-center">
                <Link href={`/tools/${comparison.toolB.slug}`} className="block">
                  <div className="text-4xl font-bold text-purple-600 dark:text-purple-400 mb-1">
                    {scoreB.total?.toFixed(1)}
                  </div>
                  <div className="text-sm font-semibold text-zinc-900 dark:text-white">
                    {comparison.toolB.name}
                  </div>
                  <div className="text-xs text-zinc-500 dark:text-zinc-400">
                    {scoreB.grade} Grade
                  </div>
                </Link>
              </div>
            </div>
            <div className="mt-6">
              <MultiRadarChart
                tools={[
                  toolA && { ...toolA, color: "#3b82f6" },
                  toolB && { ...toolB, color: "#8b5cf6" },
                ].filter(Boolean) as any[]}
                size={300}
              />
            </div>
          </div>
        </FadeIn>
      )}

      {/* Comparison Table */}
      <FadeIn delay={0.25}>
        <div className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 p-6 mb-8 overflow-x-auto">
          <h2 className="text-lg font-bold text-zinc-900 dark:text-white mb-4 flex items-center gap-2">
            <Target className="w-5 h-5 text-blue-500" />
            Head-to-Head Comparison
          </h2>
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-zinc-200 dark:border-zinc-800">
                <th className="text-left py-3 px-2 font-semibold text-zinc-500 dark:text-zinc-400">Feature</th>
                <th className="text-center py-3 px-2 font-semibold text-blue-600 dark:text-blue-400">{comparison.toolA.name}</th>
                <th className="text-center py-3 px-2 font-semibold text-purple-600 dark:text-purple-400">{comparison.toolB.name}</th>
              </tr>
            </thead>
            <tbody>
              {comparisonDimensions.map((dim, i) => (
                <tr key={i} className="border-b border-zinc-100 dark:border-zinc-800/50">
                  <td className="py-3 px-2 font-medium text-zinc-700 dark:text-zinc-300">{dim.label}</td>
                  <td className="py-3 px-2 text-center text-zinc-600 dark:text-zinc-400">{dim.a}</td>
                  <td className="py-3 px-2 text-center text-zinc-600 dark:text-zinc-400">{dim.b}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </FadeIn>

      {/* Tool A Deep Dive */}
      {toolA && (
        <FadeIn delay={0.3}>
          <div className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 p-6 mb-6">
            <h2 className="text-lg font-bold text-zinc-900 dark:text-white mb-3 flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-blue-500"></span>
              {comparison.toolA.name} Deep Dive
            </h2>
            <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed mb-4">
              {toolA.description}
            </p>
            <div className="flex flex-wrap gap-2 mb-4">
              {toolA.pros?.slice(0, 4).map((pro: string, i: number) => (
                <span key={i} className="inline-flex items-center gap-1 px-2.5 py-1 bg-emerald-50 dark:bg-emerald-950/30 text-emerald-700 dark:text-emerald-400 rounded-md text-xs">
                  <Check className="w-3 h-3" /> {pro.length > 50 ? pro.slice(0, 50) + "..." : pro}
                </span>
              ))}
            </div>
            <Link
              href={`/tools/${comparison.toolA.slug}`}
              className="inline-flex items-center gap-1.5 text-sm text-blue-600 dark:text-blue-400 font-medium hover:underline"
            >
              Read full {comparison.toolA.name} review <ExternalLink className="w-3.5 h-3.5" />
            </Link>
          </div>
        </FadeIn>
      )}

      {/* Tool B Deep Dive */}
      {toolB && (
        <FadeIn delay={0.35}>
          <div className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 p-6 mb-8">
            <h2 className="text-lg font-bold text-zinc-900 dark:text-white mb-3 flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-purple-500"></span>
              {comparison.toolB.name} Deep Dive
            </h2>
            <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed mb-4">
              {toolB.description}
            </p>
            <div className="flex flex-wrap gap-2 mb-4">
              {toolB.pros?.slice(0, 4).map((pro: string, i: number) => (
                <span key={i} className="inline-flex items-center gap-1 px-2.5 py-1 bg-emerald-50 dark:bg-emerald-950/30 text-emerald-700 dark:text-emerald-400 rounded-md text-xs">
                  <Check className="w-3 h-3" /> {pro.length > 50 ? pro.slice(0, 50) + "..." : pro}
                </span>
              ))}
            </div>
            <Link
              href={`/tools/${comparison.toolB.slug}`}
              className="inline-flex items-center gap-1.5 text-sm text-purple-600 dark:text-purple-400 font-medium hover:underline"
            >
              Read full {comparison.toolB.name} review <ExternalLink className="w-3.5 h-3.5" />
            </Link>
          </div>
        </FadeIn>
      )}

      {/* FAQ Section */}
      <FadeIn delay={0.4}>
        <FAQSection items={faqs} title={`${comparison.toolA.name} vs ${comparison.toolB.name} FAQ`} />
      </FadeIn>

      {/* Final Verdict */}
      <FadeIn delay={0.45}>
        <div className="bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-blue-950/30 dark:via-indigo-950/30 dark:to-purple-950/30 rounded-2xl border border-blue-100 dark:border-blue-900/30 p-6 sm:p-8 mb-8 mt-8">
          <h2 className="text-lg font-bold text-zinc-900 dark:text-white mb-4 flex items-center gap-2">
            <Award className="w-5 h-5 text-amber-500" />
            Final Verdict
          </h2>
          <p className="text-sm sm:text-base text-zinc-700 dark:text-zinc-300 leading-relaxed">
            {comparison.verdict}
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Link
              href={`/tools/${comparison.toolA.slug}`}
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium rounded-lg transition-colors"
            >
              <ExternalLink className="w-4 h-4" />
              {comparison.toolA.name} Review
            </Link>
            <Link
              href={`/tools/${comparison.toolB.slug}`}
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-purple-600 hover:bg-purple-500 text-white text-sm font-medium rounded-lg transition-colors"
            >
              <ExternalLink className="w-4 h-4" />
              {comparison.toolB.name} Review
            </Link>
            <Link
              href="/compare"
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-zinc-200 dark:bg-zinc-700 hover:bg-zinc-300 dark:hover:bg-zinc-600 text-zinc-700 dark:text-zinc-300 text-sm font-medium rounded-lg transition-colors"
            >
              <GitCompare className="w-4 h-4" />
              Compare More Tools
            </Link>
          </div>
        </div>
      </FadeIn>

      <div className="mt-8 text-center text-xs text-zinc-400 dark:text-zinc-500">
        Last updated September 13, 2026. Scores based on our public evaluation methodology.
        Affiliate links may earn us a commission at no extra cost to you.
      </div>
    </div>
  );
}
