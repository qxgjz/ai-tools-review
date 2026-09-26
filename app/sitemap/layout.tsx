import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Sitemap | AIToolCrux',
  description:
    'Browse all AI tools, reviews, comparisons, and guides on AIToolCrux. Find your way around our complete directory of 500+ AI tools.',
  alternates: {
    canonical: 'https://www.aitoolcrux.com/sitemap',
  },
};

export default function SitemapLayout({ children }: { children: React.ReactNode }) {
  return children;
}
