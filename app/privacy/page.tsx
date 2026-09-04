import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Privacy Policy | AIToolCrux",
  description: "Privacy policy for AIToolCrux - how we collect, use, and protect your data.",
  alternates: {
    canonical: "https://www.aitoolcrux.com/privacy",
  },
};

export default function PrivacyPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Privacy Policy</h1>
      <p className="text-sm text-gray-500 dark:text-gray-400 mb-8">Last updated: September 2, 2026</p>

      <div className="prose dark:prose-invert max-w-none">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mt-8 mb-3">1. Introduction</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          Welcome to AIToolCrux ("we," "our," or "us"). We respect your privacy and are committed to protecting your personal data. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you visit our website https://www.aitoolcrux.com.
        </p>

        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mt-8 mb-3">2. Information We Collect</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-3">We may collect the following types of information:</p>
        <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-4 space-y-2">
          <li><strong>Usage data:</strong> Pages visited, time spent on pages, click patterns, referring URLs, browser type, device type, and approximate geographic location (country/region level).</li>
          <li><strong>Email address:</strong> Only if you voluntarily subscribe to our newsletter or contact us.</li>
          <li><strong>Cookies and similar technologies:</strong> We use cookies and similar tracking technologies to track activity on our website and improve your experience.</li>
        </ul>

        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mt-8 mb-3">3. How We Use Your Information</h2>
        <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-4 space-y-2">
          <li>To operate and maintain our website</li>
          <li>To improve and personalize your experience</li>
          <li>To understand how users interact with our content (via Google Analytics and Umami)</li>
          <li>To send you newsletters and updates (only if you subscribe)</li>
          <li>To respond to your inquiries and provide customer support</li>
          <li>To detect, prevent, and address technical issues or security threats</li>
        </ul>

        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mt-8 mb-3">4. Analytics Tools</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-3">We use the following analytics tools:</p>
        <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-4 space-y-2">
          <li><strong>Google Analytics 4 (GA4):</strong> Tracks website traffic, user behavior, and audience demographics. IP addresses are anonymized.</li>
          <li><strong>Umami:</strong> Privacy-focused website analytics. Does not use cookies and does not collect personal data.</li>
        </ul>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          You can opt out of Google Analytics by installing the <a href="https://tools.google.com/dlpage/gaoptout" className="text-blue-600 dark:text-blue-400 underline">Google Analytics Opt-out Browser Add-on</a>.
        </p>

        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mt-8 mb-3">5. Cookies</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          We use cookies to remember your preferences (such as dark/light mode), understand how you use our website, and improve our services. You can control cookies through your browser settings. Most browsers allow you to refuse cookies or alert you when cookies are being sent.
        </p>

        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mt-8 mb-3">6. Affiliate Links and Third-Party Services</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          Our website contains affiliate links to products and services we recommend. If you click on an affiliate link and make a purchase, we may earn a commission at no additional cost to you. These third-party services have their own privacy policies, and we are not responsible for their practices. We encourage you to review their privacy policies before providing any personal information.
        </p>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          We also use Giscus for comments, which is powered by GitHub Discussions. When you comment, your GitHub profile information may be visible. Please review GitHub's privacy policy for more information.
        </p>

        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mt-8 mb-3">7. Data Retention</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          We retain your personal data only for as long as necessary to fulfill the purposes outlined in this Privacy Policy. Analytics data is retained for up to 26 months (Google Analytics default). If you subscribe to our newsletter, we retain your email address until you unsubscribe.
        </p>

        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mt-8 mb-3">8. Your Data Rights</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-3">Depending on your location, you may have the following rights:</p>
        <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-4 space-y-2">
          <li>Access the personal data we hold about you</li>
          <li>Request correction of inaccurate data</li>
          <li>Request deletion of your personal data</li>
          <li>Object to or restrict processing of your data</li>
          <li>Data portability (receive your data in a usable format)</li>
          <li>Withdraw consent at any time</li>
        </ul>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          To exercise any of these rights, please contact us at <a href="mailto:840754587@qq.com" className="text-blue-600 dark:text-blue-400 underline">840754587@qq.com</a>.
        </p>

        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mt-8 mb-3">9. Children's Privacy</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          Our website is not intended for children under the age of 13. We do not knowingly collect personal data from children under 13. If you believe we have collected data from a child, please contact us and we will promptly delete it.
        </p>

        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mt-8 mb-3">10. Changes to This Privacy Policy</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          We may update this Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page and updating the "Last updated" date. You are advised to review this Privacy Policy periodically for any changes.
        </p>

        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mt-8 mb-3">11. Contact Us</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          If you have any questions about this Privacy Policy, please contact us at:
        </p>
        <p className="text-gray-700 dark:text-gray-300">
          Email: <a href="mailto:840754587@qq.com" className="text-blue-600 dark:text-blue-400 underline">840754587@qq.com</a><br />
          Website: <a href="https://www.aitoolcrux.com/contact" className="text-blue-600 dark:text-blue-400 underline">https://www.aitoolcrux.com/contact</a>
        </p>
      </div>
    </div>
  );
}
