'use client';

import { useEffect } from 'react';

declare global {
  interface Window {
    dataLayer: any[];
    gtag: (...args: any[]) => void;
  }
}

/**
 * Defer non-urgent gtag events to browser idle time via requestIdleCallback.
 * Falls back to direct call if requestIdleCallback is unavailable.
 * This prevents analytics event firing from competing with user input for main thread,
 * directly improving INP (Interaction to Next Paint).
 */
function trackEvent(...args: any[]) {
  if (typeof window === 'undefined' || !window.gtag) return;
  if (typeof window.requestIdleCallback === 'function') {
    window.requestIdleCallback(
      () => {
        window.gtag(...args);
      },
      { timeout: 3000 },
    );
  } else {
    window.gtag(...args);
  }
}

/** Extract tool slug from /tools/{slug} path */
function getToolSlugFromPath(): string | null {
  const match = window.location.pathname.match(/^\/tools\/([^/]+)/);
  return match ? match[1] : null;
}

/** Extract article slug from /blog/{slug} path */
function getArticleSlugFromPath(): string | null {
  const match = window.location.pathname.match(/^\/blog\/([^/]+)/);
  return match ? match[1] : null;
}

/** Check if a URL looks like an affiliate/partner link */
function isAffiliateUrl(href: string): boolean {
  const affiliatePatterns = [
    'affiliate',
    'ref',
    'partner',
    'utm_source',
    'utm_medium',
    'tracking',
    'clickid',
  ];
  return affiliatePatterns.some((p) => href.toLowerCase().includes(p));
}

/** Check if link text or context indicates a CTA button */
function isCtaButton(link: HTMLAnchorElement): boolean {
  const text = link.textContent?.trim().toLowerCase() || '';
  const ctaPatterns = [
    'visit',
    'try ',
    'get started',
    'sign up',
    'start free',
    'free trial',
    'go to',
    'learn more',
  ];
  const hasCtaClass =
    link.className.includes('bg-emerald') ||
    link.className.includes('bg-blue') ||
    link.className.includes('font-semibold');
  return ctaPatterns.some((p) => text.includes(p)) || hasCtaClass;
}

export function GA4EventTracker() {
  useEffect(() => {
    // 确保 gtag 可用
    if (typeof window === 'undefined' || !window.gtag) return;

    // 1. 外链点击追踪 + 转化事件
    const handleClick = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      const link = target.closest('a');
      if (!link) return;

      const href = link.getAttribute('href');
      if (!href) return;

      // 检测外链
      const isExternal = href.startsWith('http') && !href.includes('aitoolcrux.com');
      if (!isExternal) return;

      const linkText = link.textContent?.trim().substring(0, 100) || 'unknown';
      const pagePath = window.location.pathname;
      const toolSlug = getToolSlugFromPath();
      const articleSlug = getArticleSlugFromPath();
      const isAff = isAffiliateUrl(href);
      const isCta = isCtaButton(link);

      // 基础外链事件（保留兼容）
      trackEvent('event', 'outbound_click', {
        outbound_url: href,
        link_text: linkText,
        page_path: pagePath,
      });

      // === 转化事件：工具页出站点击（Key Event候选）===
      if (toolSlug) {
        trackEvent('event', 'tool_outbound_click', {
          tool_slug: toolSlug,
          outbound_url: href,
          link_text: linkText,
          is_affiliate: isAff,
          is_cta_button: isCta,
          cta_position: pagePath.includes('/tools/')
            ? // Infer position from scroll context
              window.scrollY > window.innerHeight * 2
              ? 'bottom'
              : window.scrollY > window.innerHeight * 0.5
                ? 'mid'
                : 'top'
            : 'unknown',
        });
      }

      // === 转化事件：Compare页CTA点击（Key Event候选）===
      if (pagePath === '/compare' && isCta) {
        trackEvent('event', 'compare_cta_click', {
          outbound_url: href,
          link_text: linkText,
          is_affiliate: isAff,
        });
      }

      // === 转化事件：文章内联盟链接点击（Key Event候选）===
      if (articleSlug && isAff) {
        trackEvent('event', 'article_affiliate_click', {
          article_slug: articleSlug,
          outbound_url: href,
          link_text: linkText,
        });
      }

      // 联盟链接点击（保留兼容）
      if (isAff) {
        trackEvent('event', 'affiliate_click', {
          outbound_url: href,
          link_text: linkText,
          page_path: pagePath,
          tool_slug: toolSlug || undefined,
          article_slug: articleSlug || undefined,
        });
      }
    };

    // 2. 滚动深度追踪
    const scrollDepths = [25, 50, 75, 100];
    const trackedDepths = new Set<number>();

    const handleScroll = () => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      if (docHeight <= 0) return;

      const scrollPercent = Math.round((scrollTop / docHeight) * 100);

      for (const depth of scrollDepths) {
        if (scrollPercent >= depth && !trackedDepths.has(depth)) {
          trackedDepths.add(depth);
          trackEvent('event', 'scroll_depth', {
            scroll_percent: depth,
            page_path: window.location.pathname,
          });
        }
      }
    };

    // 3. 工具选择追踪（compare页面）
    const handleToolSelect = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      const toolButton = target.closest('button');
      if (!toolButton) return;

      // 检测是否是工具选择按钮（在 compare 页面）
      if (window.location.pathname === '/compare') {
        const toolName = toolButton.querySelector('span')?.textContent?.trim();
        if (toolName && toolName.length < 50) {
          trackEvent('event', 'tool_selected', {
            tool_name: toolName,
            page_path: '/compare',
          });
        }
      }
    };

    document.addEventListener('click', handleClick);
    document.addEventListener('click', handleToolSelect);
    window.addEventListener('scroll', handleScroll, { passive: true });

    return () => {
      document.removeEventListener('click', handleClick);
      document.removeEventListener('click', handleToolSelect);
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return null;
}
