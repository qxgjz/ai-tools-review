import { Metadata } from "next";
import Link from "next/link";
import { Shield, Brain, Users, CheckCircle, RefreshCw, Mail, Award, FileText, Eye, Zap } from "lucide-react";

export const metadata: Metadata = {
  title: "AI Usage Policy & Editorial Standards | AIToolCrux",
  description: "Learn how AIToolCrux uses AI tools responsibly in our content creation process. Our commitment to transparency, accuracy, and editorial integrity.",
  alternates: {
    canonical: "https://www.aitoolcrux.com/ai-policy",
  },
};

export default function AIPolicyPage() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 text-white py-16 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-white/20 rounded-full mb-6">
            <Shield className="w-8 h-8" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            AI Usage Policy
          </h1>
          <p className="text-xl text-blue-100 max-w-2xl mx-auto">
            Our commitment to transparency, accuracy, and editorial integrity in the age of AI
          </p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* Last Updated */}
        <div className="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400 mb-8">
          <RefreshCw className="w-4 h-4" />
          <span>Last updated: September 11, 2026</span>
        </div>

        {/* Introduction */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-3">
            <Brain className="w-6 h-6 text-blue-600" />
            Our Approach to AI
          </h2>
          <div className="prose dark:prose-invert max-w-none">
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed text-lg">
              At AIToolCrux, we believe in the responsible and transparent use of artificial intelligence.
              As a platform dedicated to reviewing and comparing AI tools, we recognize the importance
              of maintaining the highest editorial standards while leveraging AI to enhance our workflow.
            </p>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              This policy outlines how we use AI tools in our content creation process, the safeguards
              we have in place to ensure accuracy, and our commitment to maintaining the trust of our readers.
            </p>
          </div>
        </section>

        {/* Content Creation Process */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
            <FileText className="w-6 h-6 text-purple-600" />
            Our Content Creation Process
          </h2>

          <div className="space-y-6">
            {/* Step 1 */}
            <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-10 h-10 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center">
                  <span className="text-blue-600 dark:text-blue-400 font-bold">1</span>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    Research & Hands-On Testing
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    Every tool review begins with extensive research and hands-on testing by our editorial team.
                    We spend hours using each tool, testing its features, evaluating its performance, and
                    documenting our real-world experience. This human-led process forms the foundation of every review.
                  </p>
                </div>
              </div>
            </div>

            {/* Step 2 */}
            <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-10 h-10 bg-purple-100 dark:bg-purple-900/30 rounded-full flex items-center justify-center">
                  <span className="text-purple-600 dark:text-purple-400 font-bold">2</span>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    AI-Assisted Drafting
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    We may use AI language models to assist with drafting, organizing, and formatting our
                    research findings. AI helps us structure information efficiently, but the core insights,
                    evaluations, and recommendations always come from our human editors who have actually
                    used the tools.
                  </p>
                </div>
              </div>
            </div>

            {/* Step 3 */}
            <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-10 h-10 bg-pink-100 dark:bg-pink-900/30 rounded-full flex items-center justify-center">
                  <span className="text-pink-600 dark:text-pink-400 font-bold">3</span>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    Human Editorial Review
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    Every piece of content undergoes thorough review by our experienced editorial team.
                    Our editors verify all claims, check for accuracy, ensure the content reflects our
                    actual testing experience, and add their expert analysis and insights. No content is
                    published without human approval.
                  </p>
                </div>
              </div>
            </div>

            {/* Step 4 */}
            <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-10 h-10 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center">
                  <span className="text-green-600 dark:text-green-400 font-bold">4</span>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    Fact-Checking & Verification
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    Before publication, all factual claims—including pricing, features, specifications,
                    and comparisons—are verified against official sources and our own testing data.
                    We maintain a rigorous fact-checking process to ensure the information we provide
                    is accurate and up-to-date.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* What AI Does and Doesn't Do */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
            <Zap className="w-6 h-6 text-yellow-500" />
            What AI Does and Doesn&apos;t Do
          </h2>

          <div className="grid md:grid-cols-2 gap-6">
            {/* AI Helps With */}
            <div className="bg-green-50 dark:bg-green-900/20 rounded-xl p-6 border border-green-200 dark:border-green-800">
              <h3 className="text-lg font-semibold text-green-800 dark:text-green-400 mb-4 flex items-center gap-2">
                <CheckCircle className="w-5 h-5" />
                AI Helps With
              </h3>
              <ul className="space-y-3">
                <li className="flex items-start gap-2 text-green-700 dark:text-green-300">
                  <span className="text-green-500 mt-1">✓</span>
                  Organizing and structuring research notes
                </li>
                <li className="flex items-start gap-2 text-green-700 dark:text-green-300">
                  <span className="text-green-500 mt-1">✓</span>
                  Drafting initial content outlines
                </li>
                <li className="flex items-start gap-2 text-green-700 dark:text-green-300">
                  <span className="text-green-500 mt-1">✓</span>
                  Grammar and spelling assistance
                </li>
                <li className="flex items-start gap-2 text-green-700 dark:text-green-300">
                  <span className="text-green-500 mt-1">✓</span>
                  Formatting and readability improvements
                </li>
                <li className="flex items-start gap-2 text-green-700 dark:text-green-300">
                  <span className="text-green-500 mt-1">✓</span>
                  Summarizing lengthy documentation
                </li>
                <li className="flex items-start gap-2 text-green-700 dark:text-green-300">
                  <span className="text-green-500 mt-1">✓</span>
                  Generating comparison tables from verified data
                </li>
              </ul>
            </div>

            {/* AI Never Does */}
            <div className="bg-red-50 dark:bg-red-900/20 rounded-xl p-6 border border-red-200 dark:border-red-800">
              <h3 className="text-lg font-semibold text-red-800 dark:text-red-400 mb-4 flex items-center gap-2">
                <Eye className="w-5 h-5" />
                AI Never Does
              </h3>
              <ul className="space-y-3">
                <li className="flex items-start gap-2 text-red-700 dark:text-red-300">
                  <span className="text-red-500 mt-1">✗</span>
                  Make subjective evaluations or ratings
                </li>
                <li className="flex items-start gap-2 text-red-700 dark:text-red-300">
                  <span className="text-red-500 mt-1">✗</span>
                  Provide personal opinions or recommendations
                </li>
                <li className="flex items-start gap-2 text-red-700 dark:text-red-300">
                  <span className="text-red-500 mt-1">✗</span>
                  Fabricate testing experiences or data
                </li>
                <li className="flex items-start gap-2 text-red-700 dark:text-red-300">
                  <span className="text-red-500 mt-1">✗</span>
                  Publish content without human review
                </li>
                <li className="flex items-start gap-2 text-red-700 dark:text-red-300">
                  <span className="text-red-500 mt-1">✗</span>
                  Make factual claims without verification
                </li>
                <li className="flex items-start gap-2 text-red-700 dark:text-red-300">
                  <span className="text-red-500 mt-1">✗</span>
                  Replace our expert editorial judgment
                </li>
              </ul>
            </div>
          </div>
        </section>

        {/* Our Commitments */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
            <Award className="w-6 h-6 text-amber-500" />
            Our Commitments to You
          </h2>

          <div className="grid md:grid-cols-2 gap-4">
            <div className="flex items-start gap-3 p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
              <Users className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-semibold text-gray-900 dark:text-white">Human-Led Reviews</h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">Every review is based on real hands-on testing by our human editors.</p>
              </div>
            </div>

            <div className="flex items-start gap-3 p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
              <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-semibold text-gray-900 dark:text-white">Transparent Process</h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">We clearly disclose how AI is used in our content creation process.</p>
              </div>
            </div>

            <div className="flex items-start gap-3 p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
              <Shield className="w-5 h-5 text-purple-600 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-semibold text-gray-900 dark:text-white">Editorial Independence</h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">Our evaluations are never influenced by affiliate relationships or sponsorships.</p>
              </div>
            </div>

            <div className="flex items-start gap-3 p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
              <RefreshCw className="w-5 h-5 text-pink-600 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-semibold text-gray-900 dark:text-white">Regular Updates</h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">We continuously update our reviews to reflect the latest features and pricing.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Correction Policy */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-3">
            <FileText className="w-6 h-6 text-blue-600" />
            Correction & Update Policy
          </h2>
          <div className="prose dark:prose-invert max-w-none">
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              We strive for accuracy in everything we publish, but we recognize that mistakes can happen
              and information can become outdated. If you find an error in our content, please let us know
              and we will promptly review and correct it.
            </p>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              All corrections are clearly noted with the date of the correction and a brief explanation
              of what was changed. We also regularly review and update our content to ensure it remains
              accurate and relevant as AI tools evolve.
            </p>
          </div>
        </section>

        {/* Contact */}
        <section className="mb-12">
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white text-center">
            <Mail className="w-12 h-12 mx-auto mb-4 opacity-90" />
            <h2 className="text-2xl font-bold mb-3">Questions or Concerns?</h2>
            <p className="text-blue-100 mb-6 max-w-lg mx-auto">
              If you have questions about our AI usage policy or would like to report an error,
              we&apos;d love to hear from you.
            </p>
            <Link
              href="mailto:support@aitoolcrux.com"
              className="inline-flex items-center gap-2 px-6 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
            >
              <Mail className="w-4 h-4" />
              Contact Our Team
            </Link>
          </div>
        </section>

        {/* Related Links */}
        <section className="border-t border-gray-200 dark:border-gray-700 pt-8">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Learn More</h3>
          <div className="flex flex-wrap gap-3">
            <Link
              href="/methodology"
              className="px-4 py-2 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors text-sm font-medium"
            >
              Our Review Methodology
            </Link>
            <Link
              href="/about"
              className="px-4 py-2 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors text-sm font-medium"
            >
              About AIToolCrux
            </Link>
            <Link
              href="/privacy"
              className="px-4 py-2 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors text-sm font-medium"
            >
              Privacy Policy
            </Link>
            <Link
              href="/terms"
              className="px-4 py-2 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors text-sm font-medium"
            >
              Terms of Service
            </Link>
          </div>
        </section>
      </div>
    </div>
  );
}
