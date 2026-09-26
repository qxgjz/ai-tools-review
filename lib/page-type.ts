/**
 * Page type classification for AIToolCrux.
 * Used for GA4 custom dimensions and RPM tracking.
 */

export type PageType =
  | 'homepage'
  | 'tool_page'
  | 'article_page'
  | 'review_page'
  | 'comparison_page'
  | 'category_page'
  | 'listing_page'
  | 'utility_page'
  | 'static_page'
  | 'unknown';

/**
 * Classify a URL pathname into a page type.
 *
 * Page types and their monetization potential:
 * - tool_page: /tools/[slug] — highest affiliate potential (533 pages)
 * - review_page: /blog/[slug] with "review" in slug — high affiliate potential
 * - article_page: /blog/[slug] without "review" — ad revenue + some affiliate
 * - comparison_page: /compare, /compare/[slug] — high affiliate intent
 * - category_page: /category/*, /subcategory/*, /blog/category/* — ad revenue
 * - listing_page: /alternatives/*, /best-for/*, /ranking, /top-ai-tools-by-traffic — ad + affiliate
 * - homepage: / — ad revenue
 * - utility_page: /generator, /search, /sitemap, /blog, /blog/tag/* — low monetization
 * - static_page: /about, /contact, /privacy, etc. — no monetization
 */
export function classifyPageType(pathname: string): PageType {
  const path = pathname.replace(/\/+$/, '') || '/';
  const segments = path.split('/').filter(Boolean);
  const first = segments[0] || '';
  const second = segments[1] || '';
  const slug = segments[segments.length - 1] || '';

  // Homepage
  if (path === '/') return 'homepage';

  // Tool detail pages: /tools/[slug]
  if (first === 'tools' && second) return 'tool_page';

  // Blog pages: /blog/[slug]
  if (first === 'blog') {
    if (!second) return 'utility_page'; // /blog listing
    if (second === 'category' || second === 'tag') return 'category_page';
    // Distinguish review pages from articles
    if (slug.includes('review') || slug.includes('_review') || slug.includes('-review')) {
      return 'review_page';
    }
    return 'article_page';
  }

  // Comparison pages: /compare, /compare/[slug]
  if (first === 'compare') return 'comparison_page';

  // Category pages: /category/[slug], /subcategory/[slug]
  if (first === 'category' || first === 'subcategory') return 'category_page';

  // Listing pages
  if (
    first === 'alternatives' ||
    first === 'best-for' ||
    first === 'ranking' ||
    first === 'top-ai-tools-by-traffic'
  ) {
    return 'listing_page';
  }

  // Utility pages
  if (first === 'generator' || first === 'search' || first === 'sitemap') {
    return 'utility_page';
  }

  // Static pages
  const staticPages = [
    'about',
    'contact',
    'privacy',
    'terms',
    'ai-policy',
    'disclosure',
    'methodology',
    'free-ai-tools-guide',
    'authors',
  ];
  if (staticPages.includes(first)) return 'static_page';

  return 'unknown';
}

/**
 * Monetization potential score (0-10) for each page type.
 * Used for RPM prioritization.
 */
export function getMonetizationScore(pageType: PageType): number {
  const scores: Record<PageType, number> = {
    tool_page: 10,
    review_page: 9,
    comparison_page: 9,
    listing_page: 7,
    category_page: 6,
    article_page: 5,
    homepage: 5,
    utility_page: 2,
    static_page: 0,
    unknown: 0,
  };
  return scores[pageType] ?? 0;
}
