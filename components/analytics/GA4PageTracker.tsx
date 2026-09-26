"use client";

import { useEffect, Suspense } from "react";
import { usePathname, useSearchParams } from "next/navigation";
import { classifyPageType } from "@/lib/page-type";

declare global {
  interface Window {
    dataLayer: any[];
    gtag: (...args: any[]) => void;
  }
}

/**
 * GA4 Page View Tracker for Next.js App Router.
 *
 * Problem: gtag('config') in root layout only fires once on initial load.
 * Next.js App Router client-side navigation does NOT trigger automatic
 * GA4 page_view events, so all subsequent page views are attributed to
 * the landing page path (causing pagePath="/" for all pages).
 *
 * Fix: Listen to pathname/searchParams changes and manually send
 * page_view events with the correct page_path + page_type custom dimension.
 * Must be used with send_page_view: false in gtag config to avoid
 * double-counting the initial page view.
 *
 * Custom dimensions (must be registered in GA4 Admin → Custom definitions):
 * - page_type (User-scoped or Event-scoped parameter)
 */
function PageViewTrackerInner() {
  const pathname = usePathname();
  const searchParams = useSearchParams();

  useEffect(() => {
    if (typeof window === "undefined" || !window.gtag) return;
    if (!pathname) return;

    // Build full path with query string if present
    const query = searchParams?.toString();
    const pagePath = query ? `${pathname}?${query}` : pathname;

    // Classify page type for RPM tracking and content analysis
    const pageType = classifyPageType(pathname);

    // Send manual page_view event with correct path + page_type
    window.gtag("event", "page_view", {
      page_path: pagePath,
      page_location: window.location.href,
      page_title: document.title,
      page_type: pageType,
      send_to: "G-DGK601TM42",
    });
  }, [pathname, searchParams]);

  return null;
}

/**
 * Suspense wrapper required because useSearchParams must be
 * inside a Suspense boundary in Next.js App Router.
 */
export function GA4PageTracker() {
  return (
    <Suspense fallback={null}>
      <PageViewTrackerInner />
    </Suspense>
  );
}
