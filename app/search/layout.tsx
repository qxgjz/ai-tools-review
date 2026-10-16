import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'AI Tool Search: Find 500+ Tools by Name | AIToolCrux',
  description:
    'Search through 500+ AI tools by name, category, or use case. Find the perfect AI tool for your needs.',
  alternates: {
    canonical: 'https://www.aitoolcrux.com/search',
  },
  robots: {
    index: false,
    follow: true,
  },
};

export default function SearchLayout({ children }: { children: React.ReactNode }) {
  return children;
}
