import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI Tool Comparison 2026: Compare Top AI Tools Side by Side | AIToolCrux",
  description: "Compare the best AI tools side by side in 2026. ChatGPT vs Claude, Midjourney vs DALL-E, Cursor vs Copilot. Features, pricing, ratings, and six-dimension analysis.",
  keywords: ["ai tool comparison", "compare ai tools", "best ai tools comparison", "chatgpt vs claude", "midjourney vs dall-e", "ai software comparison", "ai tools side by side", "ai tool ratings comparison"],
  alternates: {
    canonical: "https://www.aitoolcrux.com/compare",
  },
  openGraph: {
    title: "AI Tool Comparison 2026: Compare Top AI Tools Side by Side",
    description: "Compare the best AI tools side by side. Features, pricing, ratings, and detailed six-dimension analysis for 500+ AI tools.",
    url: "https://www.aitoolcrux.com/compare",
    type: "website",
    siteName: "AIToolCrux",
    images: [{
      url: "https://www.aitoolcrux.com/api/og?title=AI+Tool+Comparison+2026&description=Compare+top+AI+tools+side+by+side+with+detailed+ratings+and+pricing&category=Comparison",
      width: 1200,
      height: 630,
      alt: "AI Tool Comparison - AIToolCrux",
    }],
  },
  twitter: {
    card: "summary_large_image",
    title: "AI Tool Comparison 2026: Compare Top AI Tools Side by Side",
    description: "Compare the best AI tools side by side. Features, pricing, ratings, and detailed six-dimension analysis.",
  },
};

export default function CompareLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
