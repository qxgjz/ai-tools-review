import type { Metadata } from "next";
import { Mail, MessageSquare, Clock, Globe } from "lucide-react";

export const metadata: Metadata = {
  title: "Contact Us | AIToolCrux",
  description: "Contact AIToolCrux - questions, feedback, partnership inquiries, and correction requests.",
  alternates: {
    canonical: "https://www.aitoolcrux.com/contact",
  },
};

export default function ContactPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Contact Us</h1>
      <p className="text-gray-600 dark:text-gray-400 mb-10">
        Have a question, feedback, or partnership inquiry? We'd love to hear from you.
      </p>

      <div className="grid md:grid-cols-2 gap-6 mb-10">
        <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
              <Mail className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            </div>
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Email</h2>
          </div>
          <p className="text-gray-600 dark:text-gray-400 mb-3">
            For general inquiries, feedback, and partnership opportunities:
          </p>
          <a
            href="mailto:840754587@qq.com"
            className="text-blue-600 dark:text-blue-400 font-medium hover:underline"
          >
            840754587@qq.com
          </a>
        </div>

        <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
              <MessageSquare className="w-5 h-5 text-green-600 dark:text-green-400" />
            </div>
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Comments & Discussions</h2>
          </div>
          <p className="text-gray-600 dark:text-gray-400 mb-3">
            Join the conversation on any article using our comments section (powered by GitHub Discussions):
          </p>
          <a
            href="https://github.com/qxgjz/ai-tools-review/discussions"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 dark:text-blue-400 font-medium hover:underline"
          >
            GitHub Discussions
          </a>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-6 mb-10">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center">
            <Clock className="w-5 h-5 text-purple-600 dark:text-purple-400" />
          </div>
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Response Time</h2>
        </div>
        <p className="text-gray-600 dark:text-gray-400">
          We typically respond to emails within <strong>24-48 hours</strong>. For urgent matters, please include "URGENT" in the subject line.
        </p>
      </div>

      <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 bg-orange-100 dark:bg-orange-900/30 rounded-lg flex items-center justify-center">
            <Globe className="w-5 h-5 text-orange-600 dark:text-orange-400" />
          </div>
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Before You Contact Us</h2>
        </div>
        <ul className="space-y-3 text-gray-600 dark:text-gray-400">
          <li className="flex gap-3">
            <span className="text-blue-500 font-bold">•</span>
            <span><strong>For tool-specific questions:</strong> Please check the tool's official documentation first, as we may not be able to provide technical support for third-party tools.</span>
          </li>
          <li className="flex gap-3">
            <span className="text-blue-500 font-bold">•</span>
            <span><strong>For correction requests:</strong> If you find an error in one of our reviews, please include the article URL and the specific correction needed. We review all correction requests promptly.</span>
          </li>
          <li className="flex gap-3">
            <span className="text-blue-500 font-bold">•</span>
            <span><strong>For partnership inquiries:</strong> Please include your company name, product/service, and what type of partnership you're interested in (affiliate, sponsored content, etc.).</span>
          </li>
          <li className="flex gap-3">
            <span className="text-blue-500 font-bold">•</span>
            <span><strong>For affiliate program questions:</strong> Please note that we do not manage affiliate programs for the tools we review. Contact the tool's affiliate program directly for affiliate-related questions.</span>
          </li>
        </ul>
      </div>
    </div>
  );
}
