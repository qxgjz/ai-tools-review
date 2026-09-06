import { notFound } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, Check, X, Building2, Clock, Tag, ExternalLink, TrendingUp, Sparkles, Lightbulb, Image as ImageIcon, Award, Target, Users, Wrench, GitCompare, Microscope, Quote } from "lucide-react";
import toolsData from "@/data/tools.json";
import type { Tool, Grade, ScoreDimension } from "@/types";
import { calculateScoreResult, DIMENSION_LABELS, SCORE_WEIGHTS, GRADE_DESCRIPTIONS } from "@/lib/scoring";
import { RadarChart } from "@/components/charts/RadarChart";
import { ToolList } from "@/components/tools/ToolList";
import Giscus from "@/components/comments/Giscus";
import { BreadcrumbSchema, ProductSchema, FAQSchema } from "@/components/seo/Schema";
import { NewsletterSignup } from "@/components/monetization/NewsletterSignup";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { ToolScreenshot } from "@/components/content/ToolScreenshot";
import { AuthorBio } from "@/components/author/AuthorBio";

const GRADE_STYLES: Record<Grade, string> = {
  S: "bg-gradient-to-br from-amber-400 to-amber-600 text-white",
  A: "bg-gradient-to-br from-emerald-400 to-emerald-600 text-white",
  B: "bg-gradient-to-br from-blue-400 to-blue-600 text-white",
  C: "bg-gradient-to-br from-yellow-400 to-yellow-500 text-white",
  D: "bg-gradient-to-br from-red-400 to-red-600 text-white",
  F: "bg-gradient-to-br from-gray-400 to-gray-500 text-white",
};

const DIMENSION_ORDER: ScoreDimension[] = ["functionality", "ux", "pricing", "integration", "support", "ethics"];

export function generateStaticParams() {
  return toolsData.map((tool) => ({ slug: tool.slug }));
}

export async function generateMetadata({ params }: { params: { slug: string } }) {
  const tool = toolsData.find((t) => t.slug === params.slug);
  if (!tool) return { title: "Tool Not Found" };
  const { total, grade } = calculateScoreResult(tool.scores);
  const categoryFormatted = tool.category.charAt(0).toUpperCase() + tool.category.slice(1);
  const prosSummary = tool.pros.slice(0, 2).join(", ");
  const description = `${tool.name} by ${tool.vendor} — ${categoryFormatted} AI tool rated ${total.toFixed(1)}/10 (${grade} grade). Expert review: features, pricing, pros (${prosSummary}) & cons. Last updated ${tool.lastUpdated}. Find out if ${tool.name} is right for you.`;
  return {
    title: `${tool.name} Review 2026: ${total.toFixed(1)}/10 (${grade} Grade) | Best ${categoryFormatted} AI Tool`,
    description: description.slice(0, 160),
    keywords: [tool.name, `${tool.name} review`, `${tool.name} pricing`, tool.vendor, ...tool.tags, `best ${tool.category} AI tools`, "AI tool review", "AI software comparison"],
    alternates: {
      canonical: `https://www.aitoolcrux.com/tools/${tool.slug}`,
    },
    openGraph: {
      title: `${tool.name} Review 2026: ${total.toFixed(1)}/10 (${grade} Grade)`,
      description: description.slice(0, 160),
      url: `https://www.aitoolcrux.com/tools/${tool.slug}`,
      type: "article",
      publishedTime: tool.lastUpdated,
      modifiedTime: tool.lastUpdated,
      authors: ["AIToolCrux Editorial Team"],
    },
    twitter: {
      card: "summary_large_image",
      title: `${tool.name} Review 2026: ${total.toFixed(1)}/10 (${grade} Grade)`,
      description: description.slice(0, 160),
    },
  };
}

export default function ToolDetailPage({ params }: { params: { slug: string } }) {
  const tool = toolsData.find((t) => t.slug === params.slug) as Tool | undefined;
  if (!tool) notFound();

  const { total, grade, breakdown } = calculateScoreResult(tool.scores);
  const relatedTools = toolsData
    .filter((t) => t.category === tool.category && t.slug !== tool.slug)
    .slice(0, 6);

  // Schema.org structured data - Review
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "Review",
    itemReviewed: {
      "@type": "SoftwareApplication",
      name: tool.name,
      applicationCategory: "AIApplication",
      operatingSystem: "Web",
      offers: tool.pricing.map((tier) => ({
        "@type": "Offer",
        name: tier.name,
        price: tier.price.includes("$0") ? "0" : tier.price.replace(/[^0-9.]/g, ""),
        priceCurrency: "USD",
      })),
    },
    reviewRating: {
      "@type": "Rating",
      ratingValue: total.toFixed(1),
      bestRating: "10",
      worstRating: "0",
    },
    author: {
      "@type": "Organization",
      name: "AIToolCrux Editorial Team",
    },
    datePublished: tool.lastUpdated,
    reviewBody: tool.review || tool.description,
    name: `${tool.name} Review 2026: Expert Evaluation by AIToolCrux`,
    publisher: {
      "@type": "Organization",
      name: "AIToolCrux",
      url: "https://www.aitoolcrux.com",
    },
  };

  // Generate FAQ structured data for FAQPage rich snippet
  const toolFAQs = [
    {
      question: `What is ${tool.name}?`,
      answer: `${tool.name} is a ${tool.category} AI tool developed by ${tool.vendor}. ${tool.description} It is evaluated by AIToolCrux with a ${total.toFixed(1)}/10 overall score (${grade} grade) based on 6 dimensions: functionality, UX, pricing, integration, support, and ethics.`
    },
    {
      question: `How much does ${tool.name} cost?`,
      answer: `${tool.name} offers ${tool.pricing.length} pricing tier${tool.pricing.length > 1 ? 's' : ''}: ${tool.pricing.map(t => `${t.name} (${t.price})`).join(', ')}. ${tool.pricing.some(t => t.price?.includes('$0') || t.price?.toLowerCase().includes('free')) ? 'A free tier is available for users to try before committing to a paid plan.' : 'Paid plans start from ' + (tool.pricing[0]?.price || 'contact vendor') + '.'} Visit the official website for the most current pricing information.`
    },
    {
      question: `Is ${tool.name} worth using in 2026?`,
      answer: `Based on our comprehensive 6-dimension evaluation, ${tool.name} scored ${total.toFixed(1)}/10 (${grade} grade). It performs best in ${Object.entries(tool.scores || {}).sort((a,b) => b[1]-a[1])[0]?.[0] || 'functionality'} (${Object.entries(tool.scores || {}).sort((a,b) => b[1]-a[1])[0]?.[1] || 'N/A'}/10). We recommend it for users looking for a ${tool.category} solution. For the best fit, compare it with similar tools in our ranking.`
    },
    {
      question: `What are the best alternatives to ${tool.name}?`,
      answer: `Top alternatives to ${tool.name} include ${relatedTools.slice(0, 3).map(t => t.name).join(', ')}. Each alternative has different strengths and pricing models. We recommend comparing features, pricing, and use cases side-by-side to find the best fit for your specific needs. Visit our comparison page to compare ${tool.name} with up to 3 other tools simultaneously.`
    },
    {
      question: `Does ${tool.name} offer a free trial or free plan?`,
      answer: `${tool.pricing.some(t => t.price?.includes('$0') || t.price?.toLowerCase().includes('free') || t.price?.toLowerCase().includes('trial')) ? 'Yes, ' + tool.name + ' offers a free tier or free trial. ' : 'You can check ' + tool.name + "'s official website for current free trial offers and promotions. "}Most AI tools offer some form of free tier or trial period. We recommend starting with the free plan to evaluate whether the tool meets your needs before upgrading to a paid subscription.`
    },
    {
      question: `How does ${tool.name} compare to other AI tools?`,
      answer: `${tool.name} ranks among the top ${tool.category} AI tools with a ${total.toFixed(1)}/10 overall score. Compared to competitors, it offers ${(tool.keyFeatures?.[0] || tool.pros?.[0] || 'unique features and capabilities')}. See our detailed evaluation above for a comprehensive analysis of its strengths, weaknesses, pricing, and use cases. You can also use our comparison tool to see how it stacks up against specific alternatives.`
    },
    {
      question: `Is ${tool.name} safe and trustworthy?`,
      answer: `${tool.name} is developed by ${tool.vendor}, a company in the AI space. The tool uses standard security practices for data protection. Our ethics score for this tool is ${tool.scores?.ethics || 'N/A'}/10. As with any AI tool, we recommend reviewing their privacy policy and terms of service before inputting sensitive or confidential information. Always ensure you understand how your data is used, stored, and protected.`
    },
    {
      question: `Can ${tool.name} be used for commercial or business purposes?`,
      answer: `Commercial use rights for ${tool.name} depend on the specific pricing plan you choose. Most paid plans allow commercial use, while free tiers may have restrictions on commercial applications. We recommend carefully reviewing the tool's official terms of service, license agreement, or contacting their support team for the most accurate and up-to-date information about commercial licensing and usage rights.`
    }
  ];

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8">
      {/* Schema.org structured data */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
      />
      <BreadcrumbSchema
        items={[
          { name: "Home", url: "/" },
          { name: "Ranking", url: "/ranking" },
          { name: tool.name, url: `/tools/${tool.slug}` },
        ]}
      />
      {/* Product Schema - tool product structured data */}
      <ProductSchema
        name={tool.name}
        description={tool.description || `${tool.name} is an AI tool evaluated by AIToolCrux.`}
        brand={tool.vendor}
        category={tool.category}
        price={tool.pricing?.[0]?.price || "Free"}
        image={`https://www.aitoolcrux.com/og-image.svg`}
        url={`https://www.aitoolcrux.com/tools/${tool.slug}`}
      />

      {/* FAQPage Schema - for FAQ rich snippets in Google Search */}
      <FAQSchema faqs={toolFAQs.map(f => ({ question: f.question, answer: f.answer }))} />

      {/* Visual breadcrumb navigation */}
      <Breadcrumb
        items={[
          { name: "Ranking", url: "/ranking" },
          { name: tool.category, url: `/category/${tool.category}` },
          { name: tool.name },
        ]}
        className="mb-4"
      />

      <Link href="/ranking" className="inline-flex items-center gap-2 px-4 py-2 mb-6 text-sm font-medium text-gray-600 dark:text-gray-300 bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm hover:border-blue-300 dark:hover:border-blue-700 hover:text-blue-600 dark:hover:text-blue-400 transition-all">
        <ArrowLeft className="w-4 h-4" />
        Back to Ranking
      </Link>

      {/* Header */}
      <section className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm p-6 sm:p-8 mb-6">
        <div className="flex flex-col sm:flex-row sm:items-start gap-6">
          <div className="w-20 h-20 flex-shrink-0 flex items-center justify-center rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-600 text-white text-3xl font-extrabold shadow-lg">
            {tool.name.charAt(0).toUpperCase()}
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex flex-wrap items-center gap-3 mb-2">
              <h1 className="text-2xl sm:text-3xl font-extrabold text-gray-900 dark:text-white">{tool.name}</h1>
              <span className={`px-3 py-1 rounded-lg text-sm font-bold ${GRADE_STYLES[grade]}`}>
                {grade} Grade · {GRADE_DESCRIPTIONS[grade]}
              </span>
            </div>
            <div className="flex flex-wrap items-center gap-x-5 gap-y-2 text-sm text-gray-500 dark:text-gray-400">
              <span className="inline-flex items-center gap-1.5"><Building2 className="w-4 h-4" />{tool.vendor}</span>
              <span className="inline-flex items-center gap-1.5"><Clock className="w-4 h-4" />Updated {tool.lastUpdated}</span>
              <span className="inline-flex items-center gap-1.5"><Tag className="w-4 h-4" />{tool.category}</span>
              {tool.hasFreeTier && <span className="px-2 py-0.5 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400 rounded-md text-xs font-semibold">Free Tier Available</span>}
            </div>
          </div>
          <div className="text-center sm:text-right">
            <div className="text-5xl font-extrabold bg-gradient-to-r from-blue-600 to-indigo-600 dark:from-blue-400 dark:to-indigo-400 bg-clip-text text-transparent">{total.toFixed(1)}</div>
            <div className="text-xs text-gray-400 dark:text-gray-500 mt-1">Overall Score / 10</div>
          </div>
        </div>
        {(tool.officialUrl || (tool as any).affiliateUrl) && (
          <div className="mt-6 pt-6 border-t border-gray-50 dark:border-gray-800">
            <a href={(tool as any).affiliateUrl || tool.officialUrl} target="_blank" rel="noopener noreferrer sponsored" className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-sm font-semibold rounded-xl shadow-md hover:shadow-lg hover:-translate-y-0.5 transition-all">
              <ExternalLink className="w-4 h-4" />
              Visit Official Website
            </a>
            {(tool as any).affiliateUrl && (
              <p className="text-xs text-gray-400 dark:text-gray-500 mt-2">
                <em>Disclosure: This is an affiliate link. We may earn a commission if you sign up, at no extra cost to you.</em>
              </p>
            )}
          </div>
        )}
      </section>

      {/* Author Bio - E-E-A-T Expertise & Authoritativeness signal */}
      {(tool as any).author && (
        <section className="mb-6">
          <AuthorBio
            name={(tool as any).author.name}
            role={(tool as any).author.role}
            bio={(tool as any).author.bio}
          />
        </section>
      )}

      {/* Score card + Radar chart */}
      <section className="grid grid-cols-1 lg:grid-cols-5 gap-6 mb-6">
        <div className="lg:col-span-3 bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm p-6">
          <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-5 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            Six-Dimension Score Details
          </h2>
          <div className="space-y-4">
            {DIMENSION_ORDER.map((dim) => {
              const score = tool.scores[dim];
              const percent = (score / 10) * 100;
              return (
                <div key={dim}>
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      {DIMENSION_LABELS[dim]}
                      <span className="ml-2 text-xs text-gray-400 dark:text-gray-500">Weight {(SCORE_WEIGHTS[dim] * 100).toFixed(0)}%</span>
                    </span>
                    <span className="text-sm font-bold text-gray-900 dark:text-white">{score.toFixed(1)}</span>
                  </div>
                  <div className="h-2.5 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
                    <div className="h-full rounded-full bg-gradient-to-r from-blue-500 to-indigo-500 transition-all duration-700" style={{ width: `${percent}%` }} />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
        <div className="lg:col-span-2 bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm p-6 flex flex-col items-center justify-center">
          <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-4 self-start flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-purple-600 dark:text-purple-400" />
            Capability Radar Chart
          </h2>
          <RadarChart scores={tool.scores} size={260} showValues />
        </div>
      </section>

      {/* Pros and Cons */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm p-6">
          <h2 className="text-lg font-bold text-emerald-600 dark:text-emerald-400 mb-4 flex items-center gap-2">
            <div className="w-8 h-8 flex items-center justify-center rounded-lg bg-emerald-50 dark:bg-emerald-900/20"><Check className="w-5 h-5" /></div>
            Key Advantages
          </h2>
          <ul className="space-y-3">
            {tool.pros.map((pro, i) => (
              <li key={i} className="flex gap-3 text-sm text-gray-600 dark:text-gray-300 leading-relaxed">
                <span className="flex-shrink-0 w-5 h-5 flex items-center justify-center rounded-full bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 text-xs font-bold mt-0.5">{i + 1}</span>
                {pro}
              </li>
            ))}
          </ul>
        </div>
        <div className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm p-6">
          <h2 className="text-lg font-bold text-red-500 dark:text-red-400 mb-4 flex items-center gap-2">
            <div className="w-8 h-8 flex items-center justify-center rounded-lg bg-red-50 dark:bg-red-900/20"><X className="w-5 h-5" /></div>
            Key Disadvantages
          </h2>
          <ul className="space-y-3">
            {tool.cons.map((con, i) => (
              <li key={i} className="flex gap-3 text-sm text-gray-600 dark:text-gray-300 leading-relaxed">
                <span className="flex-shrink-0 w-5 h-5 flex items-center justify-center rounded-full bg-red-100 dark:bg-red-900/30 text-red-500 dark:text-red-400 text-xs font-bold mt-0.5">!</span>
                {con}
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* Detailed Description - E-E-A-T Experience signal */}
      {(tool as any).longDescription && (
        <section className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm p-6 sm:p-8 mb-6">
          <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
            <Quote className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            What is {tool.name}?
          </h2>
          <div className="text-sm sm:text-base text-gray-600 dark:text-gray-300 leading-relaxed space-y-4">
            {(tool as any).longDescription.split('\n\n').map((paragraph: string, i: number) => (
              <p key={i}>{paragraph}</p>
            ))}
          </div>
        </section>
      )}

      {/* Testing Methodology - E-E-A-T Experience & Trust signal */}
      {((tool as any).testingPeriod || (tool as any).testingDetails) && (
        <section className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm p-6 sm:p-8 mb-6">
          <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
            <Microscope className="w-5 h-5 text-purple-600 dark:text-purple-400" />
            Our Testing Methodology
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {(tool as any).testingPeriod && (
              <div className="bg-gray-50 dark:bg-gray-800/50 rounded-xl p-4">
                <div className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-1">Testing Period</div>
                <div className="text-sm font-semibold text-gray-900 dark:text-white">{(tool as any).testingPeriod}</div>
              </div>
            )}
            {(tool as any).testingDetails && (
              <div className="bg-gray-50 dark:bg-gray-800/50 rounded-xl p-4 md:col-span-2">
                <div className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-2">Testing Details</div>
                {typeof (tool as any).testingDetails === 'string' ? (
                  <div className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">{(tool as any).testingDetails}</div>
                ) : (
                  <div className="space-y-2">
                    {(tool as any).testingDetails.testing_methodology && (
                      <p className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">{(tool as any).testingDetails.testing_methodology}</p>
                    )}
                    {(tool as any).testingDetails.benchmark_tests && Array.isArray((tool as any).testingDetails.benchmark_tests) && (
                      <div>
                        <div className="text-xs font-semibold text-gray-500 dark:text-gray-400 mb-1">Benchmark Tests:</div>
                        <ul className="text-xs text-gray-600 dark:text-gray-400 space-y-0.5 list-disc list-inside">
                          {(tool as any).testingDetails.benchmark_tests.slice(0, 4).map((test: string, i: number) => (
                            <li key={i}>{test}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-4 italic">
            All ratings are based on hands-on testing by our editorial team. We do not accept payment for positive reviews, and affiliate relationships never influence our ratings or recommendations.
          </p>
        </section>
      )}

      {/* Key Features */}
      {(tool as any).keyFeatures && (tool as any).keyFeatures.length > 0 && (
        <section className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm p-6 sm:p-8 mb-6">
          <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-5 flex items-center gap-2">
            <Wrench className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            Key Features
          </h2>
          <ul className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {(tool as any).keyFeatures.map((feature: string, i: number) => (
              <li key={i} className="flex gap-3 text-sm text-gray-600 dark:text-gray-300 leading-relaxed bg-gray-50 dark:bg-gray-800/50 rounded-xl p-4">
                <span className="flex-shrink-0 w-5 h-5 flex items-center justify-center rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 text-xs font-bold mt-0.5">{i + 1}</span>
                {feature}
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* Use Cases */}
      {(tool as any).useCases && (tool as any).useCases.length > 0 && (
        <section className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm p-6 sm:p-8 mb-6">
          <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-5 flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
            Common Use Cases
          </h2>
          <ul className="space-y-3">
            {(tool as any).useCases.map((useCase: string, i: number) => (
              <li key={i} className="flex gap-3 text-sm text-gray-600 dark:text-gray-300 leading-relaxed">
                <Check className="w-5 h-5 flex-shrink-0 text-emerald-500 mt-0.5" />
                {useCase}
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* Best For / Not Ideal For */}
      {((tool as any).bestFor || (tool as any).notIdealFor) && (
        <section className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          {(tool as any).bestFor && (
            <div className="bg-emerald-50 dark:bg-emerald-950/20 rounded-2xl border border-emerald-100 dark:border-emerald-900/30 p-6">
              <h3 className="text-base font-bold text-emerald-700 dark:text-emerald-400 mb-3 flex items-center gap-2">
                <Users className="w-5 h-5" />
                Best For
              </h3>
              <p className="text-sm text-emerald-800 dark:text-emerald-300 leading-relaxed">{(tool as any).bestFor}</p>
            </div>
          )}
          {(tool as any).notIdealFor && (
            <div className="bg-amber-50 dark:bg-amber-950/20 rounded-2xl border border-amber-100 dark:border-amber-900/30 p-6">
              <h3 className="text-base font-bold text-amber-700 dark:text-amber-400 mb-3 flex items-center gap-2">
                <X className="w-5 h-5" />
                Not Ideal For
              </h3>
              <p className="text-sm text-amber-800 dark:text-amber-300 leading-relaxed">{(tool as any).notIdealFor}</p>
            </div>
          )}
        </section>
      )}

      {/* Tool Screenshot - E-E-A-T trust signal */}
      <section className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm p-6 mb-6">
        <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
          <ImageIcon className="w-5 h-5 text-blue-600 dark:text-blue-400" />
          {tool.name} Interface & Screenshots
        </h2>
        <p className="text-gray-600 dark:text-gray-300 mb-4 text-sm">
          Real screenshots from our hands-on testing. Click to enlarge.
        </p>
        <ToolScreenshot
          toolSlug={tool.slug}
          toolName={tool.name}
          vendor={tool.vendor}
        />
      </section>

      {/* Pricing */}
      <section className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm p-6 mb-6">
        <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-5">Pricing Plans</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead><tr className="border-b border-gray-100 dark:border-gray-800">
              <th className="text-left py-3 px-4 font-semibold text-gray-500 dark:text-gray-400">Plan</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-500 dark:text-gray-400">Price</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-500 dark:text-gray-400">Description</th>
            </tr></thead>
            <tbody>
              {tool.pricing.map((tier, i) => (
                <tr key={i} className={`border-b border-gray-50 dark:border-gray-800/50 hover:bg-gray-50 dark:hover:bg-gray-800/50 ${tier.recommended ? "bg-blue-50/50 dark:bg-blue-900/10" : ""}`}>
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-gray-900 dark:text-white">{tier.name}</span>
                      {tier.recommended && <span className="px-2 py-0.5 bg-blue-600 text-white text-xs rounded-md font-semibold">Recommended</span>}
                    </div>
                  </td>
                  <td className="py-3 px-4"><span className="font-bold text-blue-600 dark:text-blue-400">{tier.price}</span></td>
                  <td className="py-3 px-4 text-gray-500 dark:text-gray-400">{tier.description ?? "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Editor review summary / Final Verdict */}
      <section className="bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-blue-950/30 dark:via-indigo-950/30 dark:to-purple-950/30 rounded-2xl border border-blue-100 dark:border-blue-900/30 p-6 sm:p-8 mb-6">
        <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
          <Award className="w-5 h-5 text-amber-500" />
          Final Verdict & Recommendation
        </h2>
        <p className="text-sm sm:text-base text-gray-600 dark:text-gray-300 leading-relaxed">
          {(tool as any).verdict || `${tool.name} is a ${tool.category} AI tool by ${tool.vendor}, with an overall score of ${total.toFixed(1)}/10 and a ${grade} grade (${GRADE_DESCRIPTIONS[grade]}). ${tool.pros[0]}. It's worth noting that ${tool.cons[0]}. ${tool.hasFreeTier ? "This tool offers a free version, suitable for budget-conscious users to try before deciding whether to upgrade." : ""} Overall, ${total >= 8 ? "it's an excellent tool worth recommending." : total >= 7 ? "it's a solid performer, suitable for users with specific needs." : "overall performance is average, we recommend choosing carefully based on your requirements."}`}
        </p>
        <div className="mt-5 flex flex-wrap items-center gap-3">
          {(tool.officialUrl || (tool as any).affiliateUrl) && (
            <a href={(tool as any).affiliateUrl || tool.officialUrl} target="_blank" rel="noopener noreferrer sponsored" className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-sm font-semibold rounded-xl shadow-md hover:shadow-lg hover:-translate-y-0.5 transition-all">
              <ExternalLink className="w-4 h-4" />
              Visit {tool.name}
            </a>
          )}
          <span className="text-xs text-gray-500 dark:text-gray-400 italic">
            Score: {total.toFixed(1)}/10 · Grade: {grade} · Last updated: {tool.lastUpdated}
          </span>
        </div>
        <div className="mt-4 flex flex-wrap gap-2">
          {tool.tags.map((tag) => (
            <span key={tag} className="px-2.5 py-1 bg-white/70 dark:bg-gray-900/50 text-gray-600 dark:text-gray-300 rounded-md text-xs font-medium border border-gray-200 dark:border-gray-700">#{tag}</span>
          ))}
        </div>
      </section>

      {/* Alternatives - E-E-A-T comparison signal */}
      {(tool as any).alternatives && (tool as any).alternatives.length > 0 && (
        <section className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm p-6 sm:p-8 mb-6">
          <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-5 flex items-center gap-2">
            <GitCompare className="w-5 h-5 text-purple-600 dark:text-purple-400" />
            Top Alternatives to {tool.name}
          </h2>
          <div className="space-y-3">
            {(tool as any).alternatives.map((alt: any, i: number) => (
              <div key={i} className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800/50 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
                <div className="flex-1">
                  <Link href={`/tools/${alt.slug}`} className="text-sm font-semibold text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
                    {alt.name}
                  </Link>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{alt.reason}</p>
                </div>
                <Link href={`/tools/${alt.slug}`} className="text-xs text-blue-600 dark:text-blue-400 font-medium hover:underline ml-4">
                  Read Review →
                </Link>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Related recommendations */}
      {relatedTools.length > 0 && (
        <section className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm p-6 mb-6">
          <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-5 flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-purple-600 dark:text-purple-400" />
            Similar Tools Recommended
          </h2>
          <ToolList tools={relatedTools} />
        </section>
      )}

      {/* Newsletter signup CTA */}
      <div className="mb-6">
        <NewsletterSignup variant="compact" />
      </div>

      {/* Comments section */}
      <section className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm p-6 sm:p-8">
        <Giscus />
      </section>

      <div className="mt-8 text-center text-xs text-gray-400 dark:text-gray-500">
        Scores are based on our public evaluation methodology. Affiliate link revenue does not affect scores. Last updated {tool.lastUpdated}.
      </div>
    </div>
  );
}
