/**
 * Affiliate link infrastructure (architect r55, P0-AFF-LINK-INFRA-20261024).
 *
 * All affiliate links route through /go/{slug} 302 (Cloudflare Pages _redirects)
 * so that: 1) the affiliate URL is cloaked, 2) clicks are attributed to one
 * canonical endpoint, 3) GA4 affiliate_click events can be keyed by slug.
 *
 * Non-affiliate official URLs stay direct (no redirect hop).
 */
export function ctaHref(
  affiliateUrl?: string,
  officialUrl?: string,
  slug?: string,
): string {
  if (affiliateUrl && slug) return `/go/${slug}`;
  return officialUrl || '#';
}
