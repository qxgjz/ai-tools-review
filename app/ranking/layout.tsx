import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Best AI Tools Ranking 2026: Top 533 Rated | AIToolCrux",
  description: "Discover the definitive ranking of the best AI tools in 2026. 533+ tools evaluated across 6 dimensions with expert reviews and pricing comparison.",
  keywords: ["best ai tools ranking", "top ai tools 2026", "ai tools comparison", "ai tool ratings", "best ai software", "ai tools directory", "ai tool reviews"],
  alternates: {
    canonical: "https://www.aitoolcrux.com/ranking",
  },
  openGraph: {
    title: "Best AI Tools Ranking 2026: Top 533 Rated | AIToolCrux",
    description: "Discover the definitive ranking of the best AI tools in 2026. 533+ tools evaluated across 6 dimensions with expert reviews.",
    url: "https://www.aitoolcrux.com/ranking",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Best AI Tools Ranking 2026: Top 533 Rated | AIToolCrux",
    description: "Discover the definitive ranking of the best AI tools in 2026. 533+ tools evaluated across 6 dimensions.",
  },
};

export default function RankingLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
