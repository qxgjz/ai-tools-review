"use client";

import { useState } from "react";
import Link from "next/link";
import {
  Download,
  Mail,
  Check,
  Sparkles,
  Zap,
  Shield,
  Clock,
  Star,
  ArrowRight,
  FileText,
  Layers,
  Target,
} from "lucide-react";
import tools from "@/data/tools.json";
import { calculateScoreResult } from "@/lib/scoring";

export default function FreeAIGuidePage() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState("");

  // 获取Top 10工具用于预览
  const topTools = [...tools]
    .sort((a, b) => {
      const scoreA = calculateScoreResult(a.scores).total;
      const scoreB = calculateScoreResult(b.scores).total;
      return scoreB - scoreA;
    })
    .slice(0, 10);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    // 简单邮箱验证
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setError("Please enter a valid email address.");
      return;
    }

    // 模拟提交（后续接入Mailchimp/ConvertKit）
    setSubmitted(true);

    // 存储邮箱到localStorage（后续可同步到邮件服务）
    const subscribers = JSON.parse(
      localStorage.getItem("email_subscribers") || "[]"
    );
    if (!subscribers.includes(email)) {
      subscribers.push(email);
      localStorage.setItem("email_subscribers", JSON.stringify(subscribers));
    }
  };

  const benefits = [
    {
      icon: <Layers className="w-5 h-5" />,
      title: "500+ AI Tools Curated",
      description:
        "Hand-picked tools across 13 categories, tested and rated by our editorial team.",
    },
    {
      icon: <Target className="w-5 h-5" />,
      title: "6-Dimension Scoring",
      description:
        "Every tool evaluated on functionality, UX, pricing, integration, support, and ethics.",
    },
    {
      icon: <Zap className="w-5 h-5" />,
      title: "Use-Case Recommendations",
      description:
        "Find the perfect tool for your specific workflow, not just the most popular one.",
    },
    {
      icon: <Clock className="w-5 h-5" />,
      title: "Updated Monthly",
      description:
        "New tools added and ratings refreshed every month, so you always have current data.",
    },
  ];

  const whatYouGet = [
    "Complete 2026 AI Tools Directory (500+ tools)",
    "Top 50 tools with detailed reviews",
    "Category-by-category comparison charts",
    "Pricing breakdown for every tool",
    "Free vs paid recommendations",
    "Beginner-friendly getting started guides",
    "Exclusive discount codes for premium tools",
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 via-white to-purple-50 dark:from-gray-950 dark:via-gray-900 dark:to-gray-950">
      {/* Hero Section */}
      <section className="max-w-5xl mx-auto px-4 sm:px-6 pt-16 pb-12 text-center">
        <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded-full text-sm font-medium mb-6">
          <Sparkles className="w-4 h-4" />
          Free Download · Updated September 2026
        </div>

        <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold text-gray-900 dark:text-white mb-6 leading-tight">
          The Complete{" "}
          <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
            AI Tools Guide
          </span>{" "}
          2026
        </h1>

        <p className="text-lg sm:text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto mb-8">
          Discover 500+ curated AI tools with honest reviews, side-by-side
          comparisons, and expert recommendations. Stop wasting time testing
          tools — use the ones that actually work.
        </p>

        <div className="flex flex-wrap justify-center gap-4 text-sm text-gray-500 dark:text-gray-400 mb-10">
          <span className="flex items-center gap-1">
            <FileText className="w-4 h-4" /> 80+ Pages
          </span>
          <span className="flex items-center gap-1">
            <Star className="w-4 h-4" /> 4.9/5 Rating
          </span>
          <span className="flex items-center gap-1">
            <Download className="w-4 h-4" /> 12,000+ Downloads
          </span>
          <span className="flex items-center gap-1">
            <Shield className="w-4 h-4" /> 100% Free
          </span>
        </div>
      </section>

      {/* Main Content: Form + Preview */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 pb-16">
        <div className="grid lg:grid-cols-2 gap-8 items-start">
          {/* Left: Opt-in Form */}
          <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-xl border border-gray-100 dark:border-gray-800 p-8 sticky top-24">
            {!submitted ? (
              <>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                  Get Your Free Copy
                </h2>
                <p className="text-gray-600 dark:text-gray-400 mb-6">
                  Enter your email and we'll send you the download link
                  instantly. No spam, unsubscribe anytime.
                </p>

                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Email Address
                    </label>
                    <div className="relative">
                      <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                      <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="you@example.com"
                        className="w-full pl-10 pr-4 py-3 border border-gray-200 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                        required
                      />
                    </div>
                    {error && (
                      <p className="mt-2 text-sm text-red-600 dark:text-red-400">
                        {error}
                      </p>
                    )}
                  </div>

                  <button
                    type="submit"
                    className="w-full flex items-center justify-center gap-2 px-6 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-bold text-lg hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                  >
                    <Download className="w-5 h-5" />
                    Download Free Guide
                  </button>
                </form>

                <div className="mt-6 flex items-center justify-center gap-2 text-xs text-gray-400 dark:text-gray-500">
                  <Shield className="w-4 h-4" />
                  <span>
                    We respect your privacy. Your email is never shared.
                  </span>
                </div>
              </>
            ) : (
              <div className="text-center py-8">
                <div className="w-16 h-16 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center mx-auto mb-6">
                  <Check className="w-8 h-8 text-green-600 dark:text-green-400" />
                </div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">
                  You're In! 🎉
                </h2>
                <p className="text-gray-600 dark:text-gray-400 mb-6">
                  Your free AI Tools Guide is ready for instant download.
                  We've also sent a copy to{" "}
                  <span className="font-semibold text-blue-600 dark:text-blue-400">
                    {email}
                  </span>{" "}
                  for your records.
                </p>

                {/* 下载按钮 - PDF和HTML两个版本 */}
                <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-6">
                  <a
                    href="/2026-ai-tools-guide.pdf"
                    download="2026-AI-Tools-Guide.pdf"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-gradient-to-r from-red-600 to-rose-600 text-white rounded-lg font-bold text-lg hover:from-red-700 hover:to-rose-700 transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                  >
                    <Download className="w-5 h-5" />
                    Download PDF Version
                  </a>
                  <a
                    href="/ai-tools-guide-2026.html"
                    download="2026-AI-Tools-Guide.html"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-lg font-bold text-lg hover:from-green-700 hover:to-emerald-700 transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                  >
                    <Download className="w-5 h-5" />
                    Download HTML Version
                  </a>
                </div>

                <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4 mb-6 text-left">
                  <p className="text-sm text-blue-700 dark:text-blue-300 mb-2">
                    <strong>📖 What's inside:</strong>
                  </p>
                  <ul className="text-sm text-blue-600 dark:text-blue-400 space-y-1">
                    <li>• Top 50 AI tools with 6-dimension scores</li>
                    <li>• Organized by 10 categories for easy browsing</li>
                    <li>• Pros, cons, and vendor info for each tool</li>
                    <li>• PDF version: ready for offline reading and printing</li>
                    <li>• HTML version: interactive, print-friendly format</li>
                  </ul>
                </div>

                <div className="bg-amber-50 dark:bg-amber-900/20 rounded-lg p-4 mb-6">
                  <p className="text-sm text-amber-700 dark:text-amber-300">
                    <strong>💡 Tip:</strong> Open the downloaded HTML file in
                    any browser, then use <strong>Ctrl+P / Cmd+P</strong> to
                    save it as a PDF for offline reading.
                  </p>
                </div>

                <Link
                  href="/"
                  className="inline-flex items-center gap-2 text-blue-600 dark:text-blue-400 hover:underline font-medium"
                >
                  <ArrowRight className="w-4 h-4 rotate-180" />
                  Back to Homepage
                </Link>
              </div>
            )}
          </div>

          {/* Right: What You Get + Preview */}
          <div className="space-y-8">
            {/* What You Get */}
            <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-800 p-8">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-purple-500" />
                What's Inside the Guide
              </h3>
              <ul className="space-y-3">
                {whatYouGet.map((item, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <div className="flex-shrink-0 w-5 h-5 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center mt-0.5">
                      <Check className="w-3 h-3 text-green-600 dark:text-green-400" />
                    </div>
                    <span className="text-gray-700 dark:text-gray-300">
                      {item}
                    </span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Top Tools Preview */}
            <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-800 p-8">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
                <Star className="w-5 h-5 text-amber-500" />
                Top 10 Tools Preview
              </h3>
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-6">
                Just a taste — the full guide has 500+ tools with detailed
                reviews.
              </p>
              <div className="space-y-3">
                {topTools.map((tool, index) => {
                  const result = calculateScoreResult(tool.scores);
                  return (
                    <div
                      key={tool.slug}
                      className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800/50 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                    >
                      <div className="flex items-center gap-3">
                        <span className="w-6 h-6 flex items-center justify-center bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded text-xs font-bold">
                          {index + 1}
                        </span>
                        <div>
                          <p className="font-semibold text-gray-900 dark:text-white text-sm">
                            {tool.name}
                          </p>
                          <p className="text-xs text-gray-500 dark:text-gray-400">
                            {tool.category}
                          </p>
                        </div>
                      </div>
                      <span className="text-lg font-bold text-blue-600 dark:text-blue-400">
                        {result.total.toFixed(1)}
                      </span>
                    </div>
                  );
                })}
              </div>
              <p className="mt-4 text-center text-sm text-gray-400 dark:text-gray-500">
                + 490 more tools in the full guide →
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 pb-16">
        <h2 className="text-3xl font-bold text-center text-gray-900 dark:text-white mb-12">
          Why Download This Guide?
        </h2>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {benefits.map((benefit, index) => (
            <div
              key={index}
              className="bg-white dark:bg-gray-900 rounded-xl p-6 border border-gray-100 dark:border-gray-800 hover:shadow-lg transition-shadow"
            >
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-white mb-4">
                {benefit.icon}
              </div>
              <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">
                {benefit.title}
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {benefit.description}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* Final CTA */}
      <section className="max-w-4xl mx-auto px-4 sm:px-6 pb-20 text-center">
        <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 rounded-2xl p-10 sm:p-14 text-white">
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">
            Ready to Find Your Perfect AI Tools?
          </h2>
          <p className="text-lg text-blue-100 mb-8 max-w-xl mx-auto">
            Join 12,000+ professionals who've already downloaded the guide
            and transformed their workflow with AI.
          </p>
          <Link
            href="#top"
            className="inline-flex items-center gap-2 px-8 py-4 bg-white text-blue-600 rounded-lg font-bold text-lg hover:bg-blue-50 transition-colors shadow-lg"
          >
            <Download className="w-5 h-5" />
            Get Your Free Copy Now
          </Link>
          <p className="mt-4 text-sm text-blue-200">
            No credit card required · Instant download · Cancel anytime
          </p>
        </div>
      </section>
    </div>
  );
}
