import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

/**
 * Security headers middleware - CSP Report-Only mode
 *
 * Report-Only means violations are logged but NOT blocked.
 * This is safe to deploy immediately; review reports before
 * switching to enforcing mode (Content-Security-Policy).
 *
 * Third-party sources covered:
 * - GA4: googletagmanager.com, google-analytics.com, region1.google-analytics.com
 * - AdSense: pagead2.googlesyndication.com, googleads.g.doubleclick.net
 * - Giscus: giscus.app
 * - Umami: cloud.umami.is
 * - Vercel Analytics: va.vercel-scripts.com
 * - Baidu: hm.baidu.com
 */
export function middleware(request: NextRequest) {
  const response = NextResponse.next();

  // CSP Report-Only - safe to deploy, does not block anything
  const csp = [
    "default-src 'self'",
    // Scripts: self + inline (Next.js hydration, JSON-LD, gtag init) + eval (AdSense sometimes) + third-party
    "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://www.googletagmanager.com https://www.google-analytics.com https://region1.google-analytics.com https://pagead2.googlesyndication.com https://googleads.g.doubleclick.net https://giscus.app https://cloud.umami.is https://va.vercel-scripts.com https://hm.baidu.com",
    // Styles: self + inline (Tailwind, styled-jsx)
    "style-src 'self' 'unsafe-inline'",
    // Images: self + data: + all https (next/image remote patterns, screenshots)
    "img-src 'self' data: blob: https:",
    // Fonts: self (geist self-hosted) + data:
    "font-src 'self' data:",
    // Connect: self + analytics endpoints + Giscus + Crisp (if added later)
    "connect-src 'self' https://www.google-analytics.com https://region1.google-analytics.com https://giscus.app https://cloud.umami.is https://va.vercel-scripts.com https://www.googletagmanager.com",
    // Frames: AdSense + Giscus
    "frame-src https://pagead2.googlesyndication.com https://googleads.g.doubleclick.net https://giscus.app",
    // Worker: self + blob (Giscus, service workers)
    "worker-src 'self' blob:",
    // Object: none (no Flash, Java applets)
    "object-src 'none'",
    // Base URI: self
    "base-uri 'self'",
    // Form actions: self
    "form-action 'self'",
    // Upgrade insecure requests
    'upgrade-insecure-requests',
  ].join('; ');

  response.headers.set('Content-Security-Policy-Report-Only', csp);

  // Additional security headers
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('X-Frame-Options', 'SAMEORIGIN');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  response.headers.set(
    'Permissions-Policy',
    'camera=(), microphone=(), geolocation=(), interest-cohort=()'
  );

  return response;
}

export const config = {
  matcher: [
    // Apply to all routes except static assets and API
    '/((?!_next/static|_next/image|favicon.ico|api/|sitemap.xml|robots.txt|llms.txt|llms-full.txt|rss.xml).*)',
  ],
};
