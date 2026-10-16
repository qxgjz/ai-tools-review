'use client';

import { useEffect, Suspense, useRef } from 'react';
import { usePathname, useSearchParams } from 'next/navigation';
import { classifyPageType } from '@/lib/page-type';

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
 * architect r28 (GA4-20261017-003): 首屏 gtag 异步加载（afterInteractive）可能晚于
 * 本组件 useEffect 执行，导致首屏 page_view 丢失 → GA4 landing page '(not set)'（28天437 sessions, 18%）。
 * 首屏改为轮询等待 gtag 就绪（最多 2s）后再发送。
 *
 * Custom dimensions (must be registered in GA4 Admin → Custom definitions):
 * - page_type (User-scoped or Event-scoped parameter)
 */
function PageViewTrackerInner() {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const isFirst = useRef(true);

  useEffect(() => {
    if (typeof window === 'undefined' || !pathname) return;

    // Build full path with query string if present
    const query = searchParams?.toString();
    const pagePath = query ? `${pathname}?${query}` : pathname;

    // Classify page type for RPM tracking and content analysis
    const pageType = classifyPageType(pathname);

    const send = (): boolean => {
      if (typeof window.gtag !== 'function') return false;
      window.gtag('event', 'page_view', {
        page_path: pagePath,
        page_location: window.location.href,
        page_title: document.title,
        page_type: pageType,
        send_to: 'G-7XYFQR3ETF',
      });
      return true;
    };

    if (isFirst.current) {
      isFirst.current = false;
      // 首屏：gtag.js afterInteractive 异步加载，轮询等待就绪（最多 2s = 10×200ms）
      let tries = 0;
      const trySend = () => {
        if (send()) return;
        tries += 1;
        if (tries < 10) setTimeout(trySend, 200);
      };
      trySend();
    } else {
      // 后续路由变化：gtag 已就绪，直接发送
      send();
    }
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
