import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'AI Tool Recommender: Find Your Perfect AI Tool | AIToolCrux',
  description:
    'Answer 6 quick questions and get personalized AI tool recommendations. Find the best AI tool for your workflow, budget, and use case in 2026.',
  alternates: {
    canonical: 'https://www.aitoolcrux.com/generator',
  },
};

export default function GeneratorLayout({ children }: { children: React.ReactNode }) {
  return children;
}
