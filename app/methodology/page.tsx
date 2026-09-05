import type { Metadata } from "next";
import Link from "next/link";
import {
  Shield,
  Award,
  Star,
  CheckCircle2,
  Clock,
  Target,
  Zap,
  HeartHandshake,
  Code2,
  LifeBuoy,
  Scale,
  TrendingUp,
  ExternalLink,
} from "lucide-react";

export const metadata: Metadata = {
  title: "Review Methodology - How We Score AI Tools | AIToolCrux",
  description:
    "Learn how AIToolCrux evaluates AI tools with our transparent six-dimensional weighted scoring framework. We test every tool for 14+ days across functionality, UX, pricing, integrations, support, and ethics.",
  alternates: {
    canonical: "https://www.aitoolcrux.com/methodology",
  },
};

const DIMENSIONS = [
  {
    key: "functionality",
    name: "Functionality & Output Quality",
    weight: "25%",
    icon: Zap,
    color: "from-blue-500 to-indigo-600",
    description:
      "Core feature completeness, output accuracy, and real-world performance.",
    criteria: [
      "Feature completeness vs. advertised capabilities",
      "Output accuracy on standardized test cases (10+ scenarios)",
      "Consistency of results across repeated tests",
      "Advanced features (multimodal, API, automation)",
      "Error handling and edge case performance",
    ],
    scoring: {
      "9-10": "Exceptional: Industry-leading output quality, near-perfect accuracy",
      "7-8": "Strong: Reliable output with minor inconsistencies",
      "5-6": "Average: Functional but noticeable quality gaps",
      "3-4": "Weak: Significant output quality issues",
      "1-2": "Poor: Frequent errors, unreliable output",
    },
  },
  {
    key: "ux",
    name: "User Experience",
    weight: "20%",
    icon: HeartHandshake,
    color: "from-pink-500 to-rose-600",
    description:
      "Interface design, onboarding, learning curve, and overall usability.",
    criteria: [
      "First-time user onboarding experience",
      "Interface intuitiveness and navigation",
      "Learning curve for advanced features",
      "Mobile responsiveness and performance",
      "Accessibility compliance (WCAG 2.1 AA)",
    ],
    scoring: {
      "9-10": "Exceptional: Polished, intuitive, delightful to use",
      "7-8": "Strong: Clean interface with minor UX friction",
      "5-6": "Average: Functional but lacks polish",
      "3-4": "Weak: Confusing interface, steep learning curve",
      "1-2": "Poor: Frustrating experience, significant usability issues",
    },
  },
  {
    key: "pricing",
    name: "Pricing & Value",
    weight: "20%",
    icon: TrendingUp,
    color: "from-emerald-500 to-teal-600",
    description:
      "Cost-effectiveness, pricing transparency, and value for money.",
    criteria: [
      "Free tier availability and limitations",
      "Price vs. feature set comparison",
      "Pricing transparency (no hidden fees)",
      "Scalability and enterprise pricing",
      "Money-back guarantee and trial options",
    ],
    scoring: {
      "9-10": "Exceptional: Outstanding value, generous free tier",
      "7-8": "Strong: Fair pricing with good value",
      "5-6": "Average: Reasonable pricing but could be better",
      "3-4": "Weak: Expensive for what's offered",
      "1-2": "Poor: Overpriced, poor value proposition",
    },
  },
  {
    key: "integration",
    name: "Integrations & Developer Experience",
    weight: "15%",
    icon: Code2,
    color: "from-purple-500 to-violet-600",
    description:
      "API quality, third-party integrations, and developer-friendliness.",
    criteria: [
      "API documentation quality and completeness",
      "SDK availability (Python, JavaScript, etc.)",
      "Third-party integrations (Zapier, Slack, Notion)",
      "Webhook and automation support",
      "Rate limits and API reliability",
    ],
    scoring: {
      "9-10": "Exceptional: Best-in-class API, extensive integrations",
      "7-8": "Strong: Good API with solid integrations",
      "5-6": "Average: Basic API, limited integrations",
      "3-4": "Weak: Poor API documentation, few integrations",
      "1-2": "Poor: No API, no third-party integrations",
    },
  },
  {
    key: "support",
    name: "Support & Reliability",
    weight: "10%",
    icon: LifeBuoy,
    color: "from-amber-500 to-orange-600",
    description:
      "Customer support quality, platform uptime, and issue resolution.",
    criteria: [
      "Support response time (measured via test tickets)",
      "Support quality and knowledgeability",
      "Platform uptime and reliability (90-day monitoring)",
      "Self-service resources (docs, community, tutorials)",
      "Issue resolution time and follow-up",
    ],
    scoring: {
      "9-10": "Exceptional: 24/7 support, <2hr response, 99.9% uptime",
      "7-8": "Strong: Good support, <24hr response, high reliability",
      "5-6": "Average: Basic support, 1-3 day response",
      "3-4": "Weak: Slow support, frequent downtime",
      "1-2": "Poor: No support, unreliable platform",
    },
  },
  {
    key: "ethics",
    name: "Ethics & Transparency",
    weight: "10%",
    icon: Scale,
    color: "from-cyan-500 to-blue-600",
    description:
      "Data privacy, AI ethics, content policies, and business transparency.",
    criteria: [
      "Data privacy policy and user data handling",
      "AI safety measures and content moderation",
      "Transparency about AI-generated content",
      "Affiliate relationship disclosure",
      "Company background and team visibility",
    ],
    scoring: {
      "9-10": "Exceptional: Exemplary ethics, full transparency",
      "7-8": "Strong: Good privacy practices, clear policies",
      "5-6": "Average: Basic compliance, some transparency gaps",
      "3-4": "Weak: Privacy concerns, lack of transparency",
      "1-2": "Poor: Unethical practices, no transparency",
    },
  },
];

const GRADES = [
  { grade: "S", range: "9.0 - 10.0", label: "Excellent", color: "from-amber-400 to-amber-600", desc: "Exceptional quality, industry-leading performance across all dimensions. Highly recommended for all users." },
  { grade: "A", range: "8.0 - 8.9", label: "Great", color: "from-emerald-400 to-emerald-600", desc: "Strong overall performance with minor areas for improvement. Recommended for most use cases." },
  { grade: "B", range: "7.0 - 7.9", label: "Good", color: "from-blue-400 to-blue-600", desc: "Solid performance with noticeable strengths and weaknesses. Worth considering for specific needs." },
  { grade: "C", range: "6.0 - 6.9", label: "Average", color: "from-yellow-400 to-yellow-500", desc: "Functional but has significant room for improvement. Best for users with specific budget constraints." },
  { grade: "D", range: "5.0 - 5.9", label: "Poor", color: "from-red-400 to-red-600", desc: "Below average with multiple issues. Not recommended unless no alternatives exist." },
  { grade: "F", range: "< 5.0", label: "Not Recommended", color: "from-gray-400 to-gray-500", desc: "Severe quality, reliability, or ethical issues. We strongly advise against using this tool." },
];

const TESTING_STEPS = [
  {
    step: 1,
    title: "Initial Research & Setup",
    duration: "Day 1-2",
    description: "Research the tool's features, pricing, and market positioning. Create test accounts and document the onboarding experience.",
  },
  {
    step: 2,
    title: "Standardized Test Cases",
    duration: "Day 3-7",
    description: "Run 10+ standardized test cases across all core features. Test output accuracy, consistency, and edge case handling. Compare results with competing tools.",
  },
  {
    step: 3,
    title: "Real-World Integration",
    duration: "Day 8-12",
    description: "Use the tool as part of our daily workflow for 5+ days. Test integrations, API calls, and automation workflows. Document any issues or workarounds.",
  },
  {
    step: 4,
    title: "Support & Reliability Testing",
    duration: "Day 13-14",
    description: "Submit test support tickets and measure response time. Monitor platform uptime and performance. Test self-service resources and community support.",
  },
  {
    step: 5,
    title: "Scoring & Review Writing",
    duration: "Day 15",
    description: "Score each dimension based on test results. Calculate weighted total and grade. Write comprehensive review with pros, cons, and recommendations.",
  },
  {
    step: 6,
    title: "Editorial Review & Publication",
    duration: "Day 16",
    description: "Senior editor reviews the review for accuracy and completeness. Verify all claims and data points. Publish with full methodology disclosure.",
  },
];

export default function MethodologyPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-12">
      {/* Structured Data */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "Article",
            headline: "AIToolCrux Review Methodology: Six-Dimensional AI Tool Evaluation",
            description: "Transparent methodology for evaluating AI tools across six dimensions: functionality, UX, pricing, integrations, support, and ethics.",
            author: {
              "@type": "Organization",
              name: "AIToolCrux Editorial Team",
            },
            publisher: {
              "@type": "Organization",
              name: "AIToolCrux",
              logo: {
                "@type": "ImageObject",
                url: "https://www.aitoolcrux.com/logo.svg",
              },
            },
            datePublished: "2026-01-01",
            dateModified: "2026-09-05",
            mainEntityOfPage: "https://www.aitoolcrux.com/methodology",
          }),
        }}
      />

      {/* Hero */}
      <div className="text-center mb-16">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-full text-sm font-medium mb-6">
          <Shield className="w-4 h-4" />
          Transparent & Data-Driven
        </div>
        <h1 className="text-4xl sm:text-5xl font-extrabold text-gray-900 dark:text-white mb-6">
          Our Review Methodology
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto leading-relaxed">
          Every AI tool on AIToolCrux is evaluated through our rigorous six-dimensional weighted scoring framework. We test each tool for 14+ days, run standardized test cases, and score based on real-world performance — not marketing hype.
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-16">
        {[
          { value: "6", label: "Evaluation Dimensions" },
          { value: "14+", label: "Days of Testing" },
          { value: "10+", label: "Standardized Test Cases" },
          { value: "533", label: "Tools Reviewed" },
        ].map((stat, i) => (
          <div key={i} className="bg-white dark:bg-gray-900 rounded-xl border border-gray-100 dark:border-gray-800 p-4 text-center">
            <div className="text-3xl font-extrabold text-blue-600 dark:text-blue-400">{stat.value}</div>
            <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">{stat.label}</div>
          </div>
        ))}
      </div>

      {/* Six Dimensions */}
      <section className="mb-16">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2 flex items-center gap-3">
          <Star className="w-7 h-7 text-amber-500" />
          Six Evaluation Dimensions
        </h2>
        <p className="text-gray-600 dark:text-gray-400 mb-8">
          Each dimension is scored 1-10, then weighted to produce an overall score. The weights reflect what matters most for AI tool selection in 2026.
        </p>

        <div className="space-y-6">
          {DIMENSIONS.map((dim) => {
            const Icon = dim.icon;
            return (
              <div key={dim.key} className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 overflow-hidden">
                <div className={`bg-gradient-to-r ${dim.color} p-6 text-white`}>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center">
                        <Icon className="w-6 h-6" />
                      </div>
                      <div>
                        <h3 className="text-xl font-bold">{dim.name}</h3>
                        <p className="text-white/80 text-sm">{dim.description}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-3xl font-extrabold">{dim.weight}</div>
                      <div className="text-xs text-white/70">Weight</div>
                    </div>
                  </div>
                </div>
                <div className="p-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h4 className="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider mb-3">Evaluation Criteria</h4>
                      <ul className="space-y-2">
                        {dim.criteria.map((criterion, i) => (
                          <li key={i} className="flex items-start gap-2 text-sm text-gray-600 dark:text-gray-300">
                            <CheckCircle2 className="w-4 h-4 text-green-500 flex-shrink-0 mt-0.5" />
                            {criterion}
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <h4 className="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider mb-3">Scoring Guidelines</h4>
                      <div className="space-y-2">
                        {Object.entries(dim.scoring).map(([range, desc]) => (
                          <div key={range} className="flex gap-3 text-sm">
                            <span className="font-bold text-blue-600 dark:text-blue-400 w-12 flex-shrink-0">{range}</span>
                            <span className="text-gray-600 dark:text-gray-300">{desc}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Weight Calculation */}
      <section className="mb-16">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
          <Target className="w-7 h-7 text-blue-600" />
          How We Calculate the Total Score
        </h2>
        <div className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-8">
          <p className="text-gray-600 dark:text-gray-300 mb-6">
            The overall score is a weighted average of all six dimensions. Here's the formula:
          </p>
          <div className="bg-gray-50 dark:bg-gray-800 rounded-xl p-6 font-mono text-sm text-gray-700 dark:text-gray-300 overflow-x-auto">
            <div className="mb-2">Total Score = (</div>
            <div className="pl-4">Functionality × 0.25 +</div>
            <div className="pl-4">User Experience × 0.20 +</div>
            <div className="pl-4">Pricing & Value × 0.20 +</div>
            <div className="pl-4">Integrations × 0.15 +</div>
            <div className="pl-4">Support & Reliability × 0.10 +</div>
            <div className="pl-4">Ethics & Transparency × 0.10</div>
            <div className="mt-2">)</div>
          </div>
          <p className="text-gray-600 dark:text-gray-300 mt-6 text-sm">
            <strong>Example:</strong> If a tool scores 8.5 in Functionality, 8.0 in UX, 7.5 in Pricing, 7.0 in Integrations, 8.0 in Support, and 7.5 in Ethics:
          </p>
          <div className="bg-blue-50 dark:bg-blue-900/20 rounded-xl p-4 mt-4 text-sm text-blue-800 dark:text-blue-200">
            Total = (8.5×0.25) + (8.0×0.20) + (7.5×0.20) + (7.0×0.15) + (8.0×0.10) + (7.5×0.10) = <strong>7.875 → B Grade (Good)</strong>
          </div>
        </div>
      </section>

      {/* Grade Scale */}
      <section className="mb-16">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
          <Award className="w-7 h-7 text-amber-500" />
          Grade Scale
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {GRADES.map((g) => (
            <div key={g.grade} className="bg-white dark:bg-gray-900 rounded-xl border border-gray-100 dark:border-gray-800 p-5">
              <div className="flex items-center gap-3 mb-3">
                <div className={`w-12 h-12 bg-gradient-to-br ${g.color} rounded-xl flex items-center justify-center text-white text-xl font-extrabold`}>
                  {g.grade}
                </div>
                <div>
                  <div className="font-bold text-gray-900 dark:text-white">{g.label}</div>
                  <div className="text-xs text-gray-500 dark:text-gray-400">{g.range}</div>
                </div>
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-300">{g.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Testing Process */}
      <section className="mb-16">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
          <Clock className="w-7 h-7 text-blue-600" />
          Our 16-Day Testing Process
        </h2>
        <p className="text-gray-600 dark:text-gray-400 mb-8">
          Every tool goes through a standardized 16-day testing process before publication. This ensures consistent, comparable, and reliable reviews.
        </p>
        <div className="space-y-4">
          {TESTING_STEPS.map((step) => (
            <div key={step.step} className="flex gap-4 bg-white dark:bg-gray-900 rounded-xl border border-gray-100 dark:border-gray-800 p-5">
              <div className="flex-shrink-0 w-10 h-10 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold text-lg">
                {step.step}
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between mb-1">
                  <h3 className="font-bold text-gray-900 dark:text-white">{step.title}</h3>
                  <span className="text-xs text-blue-600 dark:text-blue-400 font-medium">{step.duration}</span>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-300">{step.description}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Independence Statement */}
      <section className="mb-16">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
          <Shield className="w-7 h-7 text-green-600" />
          Our Independence Promise
        </h2>
        <div className="bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-950/20 dark:to-emerald-950/20 rounded-2xl border border-green-200 dark:border-green-800 p-8">
          <div className="space-y-4">
            <div className="flex gap-3">
              <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
              <p className="text-gray-700 dark:text-gray-300"><strong>No paid placements:</strong> We do not accept payment for higher ratings or featured positions.</p>
            </div>
            <div className="flex gap-3">
              <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
              <p className="text-gray-700 dark:text-gray-300"><strong>Real testing:</strong> Every tool is tested by our editorial team for 14+ days using standardized test cases.</p>
            </div>
            <div className="flex gap-3">
              <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
              <p className="text-gray-700 dark:text-gray-300"><strong>Affiliate disclosure:</strong> Some links on our site are affiliate links. We may earn a commission if you sign up, at no extra cost to you. This never affects our ratings or recommendations.</p>
            </div>
            <div className="flex gap-3">
              <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
              <p className="text-gray-700 dark:text-gray-300"><strong>Transparent methodology:</strong> Our complete scoring methodology is published on this page and referenced in every review.</p>
            </div>
            <div className="flex gap-3">
              <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
              <p className="text-gray-700 dark:text-gray-300"><strong>Regular updates:</strong> Reviews are updated quarterly or when major product changes occur. Each review shows the last updated date.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Ready to Find Your Perfect AI Tool?
        </h2>
        <p className="text-gray-600 dark:text-gray-400 mb-8 max-w-xl mx-auto">
          Browse our independently tested and scored AI tools across 18 categories.
        </p>
        <div className="flex flex-wrap justify-center gap-4">
          <Link
            href="/ranking"
            className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition-colors"
          >
            <TrendingUp className="w-5 h-5" />
            View Top Ranked Tools
          </Link>
          <Link
            href="/category/chat"
            className="inline-flex items-center gap-2 px-6 py-3 bg-white dark:bg-gray-900 text-gray-900 dark:text-white rounded-xl font-semibold border border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-700 transition-colors"
          >
            <ExternalLink className="w-5 h-5" />
            Browse by Category
          </Link>
        </div>
      </section>
    </div>
  );
}
