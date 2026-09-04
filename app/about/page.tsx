import type { Metadata } from "next";
import Link from "next/link";
import { Shield, Award, Users, Mail, Github, ExternalLink, CheckCircle2, Star } from "lucide-react";

export const metadata: Metadata = {
  title: "About Us - AIToolCrux | Professional AI Tool Reviews",
  description: "Learn about AIToolCrux's mission, editorial team, and six-dimensional review methodology. We provide independent, data-driven AI tool reviews to help you make informed decisions.",
  alternates: {
    canonical: "https://www.aitoolcrux.com/about",
  },
};

export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-12">
      {/* Hero */}
      <div className="text-center mb-16">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-full text-sm font-medium mb-6">
          <Shield className="w-4 h-4" />
          Independent & Transparent
        </div>
        <h1 className="text-4xl sm:text-5xl font-extrabold text-gray-900 dark:text-white mb-6">
          About AIToolCrux
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto leading-relaxed">
          We help developers, creators, and businesses find the best AI tools through independent, data-driven reviews based on our six-dimensional evaluation framework.
        </p>
      </div>

      {/* Our Mission */}
      <section className="mb-16">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
          <Award className="w-7 h-7 text-blue-600" />
          Our Mission
        </h2>
        <div className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-8 shadow-sm">
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
            In 2026, there are over 5,000 AI tools available, spanning chat, writing, image generation, coding, video, audio, and more. For users and businesses, navigating this vast landscape to find the right tool is overwhelming.
          </p>
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
            AIToolCrux was founded to solve this problem. We believe that <strong>good tool selection should be based on data, not marketing hype</strong>. Our mission is to provide independent, comprehensive, and actionable AI tool reviews that help users make informed decisions.
          </p>
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
            We test every tool ourselves, use standardized test cases, and score each tool across six dimensions. Our reviews are free from vendor influence — we don't accept payment for higher ratings.
          </p>
        </div>
      </section>

      {/* Our Methodology */}
      <section className="mb-16">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
          <Star className="w-7 h-7 text-amber-500" />
          Our Review Methodology
        </h2>
        <p className="text-gray-600 dark:text-gray-400 mb-6">
          We use a six-dimensional weighted scoring framework to evaluate every AI tool. Each dimension is scored 1-10, then weighted to produce an overall score.
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {[
            { dim: "Functionality & Output Quality", weight: "25%", desc: "Core feature completeness, output accuracy, test case coverage, consistency" },
            { dim: "User Experience", weight: "20%", desc: "Interface design, onboarding curve, documentation quality, response speed" },
            { dim: "Pricing & Value", weight: "20%", desc: "Cost transparency, free tier generosity, ROI, pricing flexibility" },
            { dim: "Integration & Developer Experience", weight: "15%", desc: "API quality, platform compatibility, ecosystem, developer support" },
            { dim: "Support & Reliability", weight: "10%", desc: "Uptime, update frequency, customer support responsiveness, community" },
            { dim: "Ethics & Transparency", weight: "10%", desc: "Data privacy, bias disclosure, responsible AI, transparency" },
          ].map((item, i) => (
            <div key={i} className="bg-white dark:bg-gray-900 rounded-xl border border-gray-100 dark:border-gray-800 p-5">
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-bold text-gray-900 dark:text-white text-sm">{item.dim}</h3>
                <span className="px-2 py-0.5 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded text-xs font-bold">{item.weight}</span>
              </div>
              <p className="text-xs text-gray-500 dark:text-gray-400 leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
        <div className="mt-6 p-4 bg-amber-50 dark:bg-amber-900/10 rounded-xl border border-amber-200 dark:border-amber-800">
          <p className="text-sm text-amber-800 dark:text-amber-300">
            <strong>Grade Mapping:</strong> S (9.0+) | A (8.0-8.9) | B (7.0-7.9) | C (6.0-6.9) | D (5.0-5.9) | F ({'<5.0'})
          </p>
        </div>
      </section>

      {/* Editorial Independence */}
      <section className="mb-16">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
          <Shield className="w-7 h-7 text-emerald-600" />
          Editorial Independence
        </h2>
        <div className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-8 shadow-sm">
          <div className="space-y-4">
            {[
              "We do not accept payment for higher ratings or favorable reviews.",
              "Our scoring is based on standardized test cases and real usage, not vendor claims.",
              "Vendors cannot edit or influence our review content.",
              "We update reviews regularly to reflect product changes and price updates.",
              "Our team has full editorial control over all content.",
            ].map((item, i) => (
              <div key={i} className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-500 mt-0.5 flex-shrink-0" />
                <p className="text-gray-700 dark:text-gray-300">{item}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Affiliate Disclosure */}
      <section className="mb-16">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
          <ExternalLink className="w-7 h-7 text-purple-600" />
          Affiliate Disclosure
        </h2>
        <div className="bg-purple-50 dark:bg-purple-900/10 rounded-2xl border border-purple-200 dark:border-purple-800 p-8">
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
            AIToolCrux may contain affiliate links. If you purchase a tool through these links, we may earn a commission at no additional cost to you.
          </p>
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
            <strong>This does not affect our ratings or reviews.</strong> Affiliate revenue helps us maintain the site and continue producing independent reviews. We only recommend tools that we have tested and believe provide value to our readers.
          </p>
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
            We clearly disclose affiliate relationships on every review page, in accordance with FTC guidelines.
          </p>
        </div>
      </section>

      {/* Our Team */}
      <section className="mb-16">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
          <Users className="w-7 h-7 text-indigo-600" />
          Our Editorial Team
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {[
            {
              name: "Alex Chen",
              role: "Editor-in-Chief",
              bio: "10+ years in tech journalism. Former senior editor at a leading tech publication. Covers AI, cloud computing, and developer tools.",
              expertise: ["AI Strategy", "Product Analysis", "Editorial Standards"],
            },
            {
              name: "Sarah Kim",
              role: "Senior Reviewer - Developer Tools",
              bio: "Full-stack developer turned tech reviewer. 8 years of coding experience. Specializes in AI coding assistants, IDEs, and developer productivity tools.",
              expertise: ["AI Coding", "DevTools", "Code Quality"],
            },
            {
              name: "Marcus Rodriguez",
              role: "Senior Reviewer - Creative AI",
              bio: "Digital artist and designer with 12 years of experience. Tests AI image, video, and audio generation tools. Passionate about the intersection of AI and creativity.",
              expertise: ["AI Image", "AI Video", "Design Tools"],
            },
            {
              name: "Emily Watson",
              role: "Reviewer - Productivity & Writing",
              bio: "Content strategist and productivity consultant. Helps teams adopt AI writing and office tools. Former marketing director at a SaaS company.",
              expertise: ["AI Writing", "Productivity", "Marketing AI"],
            },
          ].map((member, i) => (
            <div key={i} className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-6 shadow-sm hover:shadow-md transition-shadow">
              <div className="flex items-center gap-4 mb-4">
                <div className="w-14 h-14 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white text-xl font-bold">
                  {member.name.charAt(0)}
                </div>
                <div>
                  <h3 className="font-bold text-gray-900 dark:text-white">{member.name}</h3>
                  <p className="text-sm text-blue-600 dark:text-blue-400">{member.role}</p>
                </div>
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400 leading-relaxed mb-4">{member.bio}</p>
              <div className="flex flex-wrap gap-2">
                {member.expertise.map((exp, j) => (
                  <span key={j} className="px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 rounded text-xs">
                    {exp}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
        <div className="mt-6 text-center">
          <Link href="/authors" className="inline-flex items-center gap-2 text-blue-600 dark:text-blue-400 font-medium hover:text-blue-700 dark:hover:text-blue-300">
            View all authors and their articles
            <ExternalLink className="w-4 h-4" />
          </Link>
        </div>
      </section>

      {/* Contact */}
      <section className="mb-16">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
          <Mail className="w-7 h-7 text-rose-600" />
          Contact Us
        </h2>
        <div className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-8 shadow-sm">
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-6">
            We welcome feedback, corrections, and suggestions. If you disagree with a review, found an error, or want to suggest a tool for review, please reach out.
          </p>
          <div className="space-y-3">
            <div className="flex items-center gap-3">
              <Mail className="w-5 h-5 text-gray-400" />
              <a href="mailto:editor@aitoolcrux.com" className="text-blue-600 dark:text-blue-400 hover:underline">editor@aitoolcrux.com</a>
            </div>
            <div className="flex items-center gap-3">
              <Github className="w-5 h-5 text-gray-400" />
              <a href="https://github.com/qxgjz/ai-tools-review" target="_blank" rel="noopener noreferrer" className="text-blue-600 dark:text-blue-400 hover:underline">github.com/qxgjz/ai-tools-review</a>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="text-center">
        <div className="bg-gradient-to-br from-blue-600 to-indigo-700 dark:from-blue-700 dark:to-indigo-800 rounded-3xl p-10 sm:p-12 text-white">
          <h2 className="text-2xl sm:text-3xl font-bold mb-4">Start Exploring AI Tools</h2>
          <p className="text-blue-100 mb-8 max-w-xl mx-auto">
            Browse our directory of 540+ AI tools, read in-depth reviews, and find the perfect tool for your needs.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/ranking" className="inline-flex items-center justify-center gap-2 px-8 py-3 bg-white text-blue-600 font-bold rounded-xl hover:shadow-lg transition-shadow">
              View Top Rated Tools
            </Link>
            <Link href="/blog" className="inline-flex items-center justify-center gap-2 px-8 py-3 bg-blue-500/30 text-white font-bold rounded-xl border border-white/30 hover:bg-blue-500/40 transition-colors">
              Read Latest Reviews
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
