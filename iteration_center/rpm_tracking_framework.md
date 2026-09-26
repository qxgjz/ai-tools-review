# AIToolCrux RPM Tracking Framework
> Created: 2026-09-24 | Status: Framework ready, revenue data pending

## Overview
RPM (Revenue Per Mille) = (Total Revenue / Total Pageviews) × 1000

This framework tracks revenue performance by page type to identify which content
types generate the most revenue per thousand pageviews, guiding content investment.

## Page Type Classification

| Page Type | URL Pattern | Monetization Weight | Primary Revenue Source |
|-----------|-------------|-------------------|----------------------|
| tool_page | /tools/[slug] | 10 | Affiliate links |
| review_page | /blog/[slug] containing "review" | 9 | Affiliate + ads |
| comparison_page | /compare, /compare/[slug] | 9 | Affiliate links |
| listing_page | /alternatives/*, /best-for/*, /ranking | 7 | Affiliate + ads |
| category_page | /category/*, /subcategory/* | 6 | AdSense |
| article_page | /blog/[slug] (non-review) | 5 | AdSense |
| homepage | / | 5 | AdSense |
| utility_page | /generator, /search, /sitemap | 2 | Minimal |
| static_page | /about, /contact, /privacy, etc. | 0 | None |

## Implementation

### 1. GA4 Custom Dimension (page_type)
- **Component:** `components/analytics/GA4PageTracker.tsx`
- **Utility:** `lib/page-type.ts` — `classifyPageType(pathname)`
- **GA4 Setup:** Register custom dimension `page_type` (Event-scoped) in
  GA4 Admin → Custom definitions → Create custom dimension
- **Data:** Every `page_view` event now includes `page_type` parameter

### 2. Revenue Tracking Events
- **affiliate_click:** Tracked in `GA4EventTracker.tsx` (outbound links with affiliate/ref/partner/utm_source)
- **AdSense revenue:** Pull from AdSense API or manual input
- **Future:** Mark `affiliate_click` as Key Event (conversion) in GA4

### 3. RPM Calculation Script
- **Script:** `rpm_tracker.py` (in project directory)
- **Data source:** GA4 Data API v1beta (pageviews by page_type)
- **Revenue input:** `--adsense-revenue`, `--affiliate-revenue`, `--other-revenue`
- **Allocation methods:**
  - `weighted` (default): Revenue allocated by monetization weight × pageviews
  - `pageview`: Revenue allocated purely by pageview share

### Usage
```bash
python rpm_tracker.py \
  --start-date 2026-09-17 --end-date 2026-09-23 \
  --adsense-revenue 12.50 --affiliate-revenue 45.00 \
  --output iteration_center/rpm_report.md
```

## Current Status
- [x] page_type classification utility created (`lib/page-type.ts`)
- [x] GA4PageTracker sends page_type with every page_view
- [x] RPM calculation script created (`rpm_tracker.py`)
- [ ] GA4 custom dimension `page_type` registered (manual step in GA4 Admin)
- [ ] AdSense API integration (pending AdSense API access)
- [ ] Affiliate platform API integration (Rewardful/Impact/FirstPromoter)
- [ ] affiliate_click marked as Key Event in GA4
- [ ] First RPM report generated (needs revenue data)

## Action Items
1. **Register page_type custom dimension in GA4** (Admin → Custom definitions)
2. **Mark affiliate_click as Key Event** (GA4 Admin → Events → Mark as conversion)
3. **Set up AdSense API** for automated revenue data
4. **Run first RPM report** once revenue data available
5. **Weekly RPM tracking** — add to Monday data analysis routine
