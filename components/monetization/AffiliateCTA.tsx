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
 * Track CTA click via Vercel Analytics (already loaded in layout)
 * Uses window.va.track if available, falls back to custom event
 */
function trackCtaClick(toolName: string, variant: string, isAffiliate: boolean) {
  if (typeof window !== "undefined" && (window as any).va) {
    (window as any).va.track("affiliate_cta_click", {
      tool: toolName,
      variant: variant,
      is_affiliate: isAffiliate,
      page: window.location.pathname,
    });
  }
  if (typeof window !== "undefined") {
    window.dispatchEvent(
      new CustomEvent("cta:click", {
        detail: { tool: toolName, variant, isAffiliate, page: window.location.pathname },
      })
    );
  }
}

/**
 * 联盟CTAComponent
 * 在评测页中显示"Visit Website"按钮，带联盟链接和点击追踪
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
          className="text-emerald-600 dark:text-emerald-400 hover:underline font-medium"
          data-cta-type="affiliate"
          data-tool={toolName}
          onClick={() => trackCtaClick(toolName, "inline", isAffiliate)}
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
          <div className="flex flex-col items-start gap-2">
            <a
              href={url}
              target="_blank"
              rel="noopener noreferrer sponsored"
              className="inline-flex items-center gap-2 px-6 py-3.5 bg-emerald-600 text-white rounded-lg font-semibold hover:bg-emerald-700 transition-colors whitespace-nowrap shadow-sm hover:shadow-md"
              data-cta-type="affiliate"
              data-tool={toolName}
              onClick={() => trackCtaClick(toolName, "bottom", isAffiliate)}
            >
              Visit {toolName} Official Site
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
            </a>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-5">No credit card required</p>
          </div>
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
    <div className="bg-gradient-to-r from-emerald-50 to-teal-50 dark:from-emerald-950/40 dark:to-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-xl p-5 my-6 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-300">
              ✓ Free Trial Available
            </span>
            <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-emerald-100 text-emerald-800 dark:bg-emerald-900/50 dark:text-emerald-300">
              ⚡ Quick Setup
            </span>
          </div>
          <p className="text-sm font-bold text-emerald-900 dark:text-emerald-100">
            Ready to Try {toolName}?
          </p>
          {description && (
            <p className="text-emerald-700 dark:text-emerald-300 text-xs mt-1">{description}</p>
          )}
        </div>
        <div className="flex flex-col items-start gap-2">
          <a
            href={url}
            target="_blank"
            rel="noopener noreferrer sponsored"
            className="inline-flex items-center gap-2 px-6 py-3.5 bg-gradient-to-r from-emerald-600 to-emerald-600 text-white rounded-lg font-bold text-sm hover:from-emerald-700 hover:to-emerald-700 transition-all shadow-md hover:shadow-lg transform hover:-translate-y-0.5 whitespace-nowrap"
            data-cta-type="affiliate"
            data-tool={toolName}
            onClick={() => trackCtaClick(toolName, "banner", isAffiliate)}
          >
            Start Free Trial
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </a>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-5">No credit card required</p>
        </div>
      </div>
      {isAffiliate && (
        <p className="text-xs text-gray-500 dark:text-gray-400 mt-3 pt-3 border-t border-emerald-100 dark:border-emerald-900/50">
          <em>Disclosure: This is an affiliate link. We may earn a commission if you sign up, at no extra cost to you. This never affects our rating or recommendation.</em>
        </p>
      )}
    </div>
  );
}

/**
 * CompareTable格中的联盟链接按钮
 */
export function CompareAffiliateButton({ toolName, url }: { toolName: string; url?: string }) {
  if (!url) return <span className="text-gray-400 text-sm">N/A</span>;
  return (
    <a
      href={url}
      target="_blank"
      rel="noopener noreferrer sponsored"
      className="inline-flex items-center gap-1 text-emerald-600 dark:text-emerald-400 hover:underline text-sm font-medium"
      data-cta-type="affiliate"
      data-tool={toolName}
      onClick={() => trackCtaClick(toolName, "compare", true)}
    >
      Visit
      <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
      </svg>
    </a>
  );
}
