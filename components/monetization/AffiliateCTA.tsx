"use client";

import Link from "next/link";

interface AffiliateCTAProps {
  toolName: string;
  officialUrl?: string;
  affiliateUrl?: string;
  description?: string;
  variant?: "inline" | "banner" | "bottom";
}

/**
 * 联盟CTA组件
 * 在评测页中显示"访问官网"按钮，带联盟链接
 */
export function AffiliateCTA({
  toolName,
  officialUrl,
  affiliateUrl,
  description,
  variant = "banner",
}: AffiliateCTAProps) {
  const url = affiliateUrl || officialUrl || "#";
  const isAffiliate = !!affiliateUrl;

  if (variant === "inline") {
    return (
      <span className="inline-flex items-center gap-1">
        <a
          href={url}
          target="_blank"
          rel="noopener noreferrer sponsored"
          className="text-blue-600 dark:text-blue-400 hover:underline font-medium"
        >
          Try {toolName}
        </a>
        {isAffiliate && <span className="text-xs text-gray-400">(affiliate)</span>}
      </span>
    );
  }

  if (variant === "bottom") {
    return (
      <div className="bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-950/30 dark:to-emerald-950/30 border border-green-200 dark:border-green-800 rounded-xl p-6 my-8">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h3 className="text-lg font-bold text-gray-900 dark:text-white">
              Ready to try {toolName}?
            </h3>
            {description && (
              <p className="text-gray-600 dark:text-gray-300 text-sm mt-1">{description}</p>
            )}
          </div>
          <a
            href={url}
            target="_blank"
            rel="noopener noreferrer sponsored"
            className="inline-flex items-center gap-2 px-6 py-3 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 transition-colors whitespace-nowrap"
          >
            Visit {toolName} Official Site
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
          </a>
        </div>
        {isAffiliate && (
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-3">
            <em>Disclosure: This is an affiliate link. We may earn a commission if you sign up, at no extra cost to you. This never affects our rating or recommendation.</em>
          </p>
        )}
      </div>
    );
  }

  // banner variant (default)
  return (
    <div className="bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-800 rounded-xl p-5 my-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div>
          <p className="text-sm font-semibold text-blue-900 dark:text-blue-100">
            👉 Try {toolName} Today
          </p>
          {description && (
            <p className="text-blue-700 dark:text-blue-300 text-xs mt-1">{description}</p>
          )}
        </div>
        <a
          href={url}
          target="_blank"
          rel="noopener noreferrer sponsored"
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-blue-600 text-white rounded-lg font-semibold text-sm hover:bg-blue-700 transition-colors whitespace-nowrap"
        >
          Get Started
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
          </svg>
        </a>
      </div>
    </div>
  );
}

/**
 * 对比表格中的联盟链接按钮
 */
export function CompareAffiliateButton({ toolName, url }: { toolName: string; url?: string }) {
  if (!url) return <span className="text-gray-400 text-sm">N/A</span>;
  return (
    <a
      href={url}
      target="_blank"
      rel="noopener noreferrer sponsored"
      className="inline-flex items-center gap-1 text-blue-600 dark:text-blue-400 hover:underline text-sm font-medium"
    >
      Visit
      <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
      </svg>
    </a>
  );
}
