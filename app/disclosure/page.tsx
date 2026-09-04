import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Affiliate Disclosure | AIToolCrux",
  description: "FTC-compliant affiliate disclosure for AIToolCrux - how we earn commissions from affiliate links.",
  alternates: {
    canonical: "https://www.aitoolcrux.com/disclosure",
  },
};

export default function DisclosurePage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Affiliate Disclosure</h1>
      <p className="text-sm text-gray-500 dark:text-gray-400 mb-8">Last updated: September 2, 2026</p>

      <div className="prose dark:prose-invert max-w-none">
        <div className="bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mb-6">
          <p className="text-blue-800 dark:text-blue-200 font-medium">
            AIToolCrux is reader-supported. When you buy through links on our site, we may earn an affiliate commission at no additional cost to you.
          </p>
        </div>

        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mt-8 mb-3">What is an Affiliate Link?</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          An affiliate link is a special URL that contains a unique tracking code. When you click on an affiliate link and purchase a product or service, the merchant knows that the referral came from AIToolCrux, and we receive a commission for that referral.
        </p>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          <strong>The price you pay is exactly the same</strong> whether you use our affiliate link or go directly to the merchant's website. We never recommend products solely because of commission potential.
        </p>

        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mt-8 mb-3">Our Editorial Independence</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          At AIToolCrux, our reviews and recommendations are based on <strong>independent testing, research, and analysis</strong>. We use a transparent 6-dimension scoring framework (functionality, user experience, pricing, integration, support, and ethics) to evaluate every tool we review.
        </p>
        <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-4 space-y-2">
          <li><strong>No paid placements:</strong> We do not accept payment to feature or rank a tool higher in our reviews.</li>
          <li><strong>No influence on scores:</strong> Affiliate relationships do not affect our scoring or recommendations.</li>
          <li><strong>Honest assessments:</strong> We highlight both strengths and weaknesses of every tool we review.</li>
          <li><strong>Transparent methodology:</strong> Our scoring framework is publicly available, and every review includes the date of last update.</li>
          <li><strong>Real testing:</strong> Our team tests tools for at least 30 days before publishing a review.</li>
        </ul>

        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mt-8 mb-3">Affiliate Programs We Participate In</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-3">
          AIToolCrux may participate in the following affiliate programs:
        </p>
        <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-4 space-y-2">
          <li><strong>AI tool affiliate programs:</strong> Jasper, Copy.ai, Writesonic, ElevenLabs, Synthesia, Pictory, InVideo, Surfer SEO, and other AI tools with their own affiliate programs.</li>
          <li><strong>PartnerStack:</strong> A SaaS affiliate network featuring tools like Notion, Monday.com, ClickUp, Webflow, and more.</li>
          <li><strong>Amazon Associates:</strong> An affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com.</li>
          <li><strong>ShareASale, Impact, CJ Affiliate:</strong> Additional affiliate networks featuring various software and technology products.</li>
        </ul>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          This list may change over time as we add or remove affiliate programs. The presence of an affiliate link does not influence our editorial content.
        </p>

        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mt-8 mb-3">Commission Structure</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-3">
          Commissions vary by program and product:
        </p>
        <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-4 space-y-2">
          <li><strong>SaaS tools:</strong> Typically 20-50% of the first payment or recurring commissions (15-30% for the lifetime of the customer subscription).</li>
          <li><strong>Amazon products:</strong> 1-10% depending on product category.</li>
          <li><strong>Other products:</strong> Varies by merchant and product.</li>
        </ul>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          Cookie durations typically range from 24 hours to 90 days, depending on the affiliate program.
        </p>

        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mt-8 mb-3">FTC Compliance</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          This disclosure is in compliance with the Federal Trade Commission (FTC) guidelines on endorsements and testimonials in advertising. We clearly disclose our affiliate relationships on every page containing affiliate links, including a persistent disclosure banner at the top of every page.
        </p>

        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mt-8 mb-3">Questions?</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          If you have any questions about our affiliate relationships or this disclosure, please contact us at <a href="mailto:840754587@qq.com" className="text-blue-600 dark:text-blue-400 underline">840754587@qq.com</a>.
        </p>
      </div>
    </div>
  );
}
