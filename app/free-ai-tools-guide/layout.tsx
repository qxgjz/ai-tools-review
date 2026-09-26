import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Free AI Tools Guide 2026: Best Free AI Tools | AIToolCrux',
  description:
    'Discover the best free AI tools in 2026. Expert-curated list of free ChatGPT, Midjourney, Claude and more. No credit card required, start using today.',
  alternates: {
    canonical: 'https://www.aitoolcrux.com/free-ai-tools-guide',
  },
};

export default function FreeAIGuideLayout({ children }: { children: React.ReactNode }) {
  return children;
}
