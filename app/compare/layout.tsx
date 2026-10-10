import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Best AI Tool Comparison 2026: Top 10 Ranked & Tested',
  description:
    'Compare 500+ AI tools side by side in 2026 with honest ratings, real pricing, and pros & cons from 3-week hands-on testing. Find your perfect AI tool.',
  keywords: [
    'ai tool comparison',
    'compare ai tools',
    'best ai tools comparison',
    'chatgpt vs claude',
    'midjourney vs dall-e',
    'ai software comparison',
    'ai tools side by side',
    'ai tool ratings comparison',
    'best ai tools 2026',
  ],
  alternates: {
    canonical: 'https://www.aitoolcrux.com/compare/',
  },
  openGraph: {
    title: 'Best AI Tool Comparison 2026: Top 10 Ranked & Tested',
    description:
      'Compare the best AI tools side by side. Features, pricing, ratings, and detailed six-dimension analysis for 500+ AI tools — tested hands-on for 3+ weeks.',
    url: 'https://www.aitoolcrux.com/compare/',
    type: 'website',
    siteName: 'AIToolCrux',
    images: [
      {
        url: 'https://www.aitoolcrux.com/api/og?title=Best+AI+Tool+Comparison+2026&description=Top+10+ranked+%26+tested+side-by-side+with+honest+ratings+and+pricing&category=Comparison',
        width: 1200,
        height: 630,
        alt: 'Best AI Tool Comparison 2026 - AIToolCrux',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Best AI Tool Comparison 2026: Top 10 Ranked & Tested',
    description:
      'Compare the best AI tools side by side. Features, pricing, ratings, and detailed six-dimension analysis — tested hands-on for 3+ weeks.',
  },
};

export default function CompareLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
