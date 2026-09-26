import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Submit Your AI Tool | AIToolCrux",
  description: "Submit your AI tool for review on AIToolCrux. Get featured in our comprehensive AI tools directory with honest, hands-on reviews.",
  robots: { index: false, follow: true },
  alternates: {
    canonical: "https://www.aitoolcrux.com/submit",
  },
};

export default function SubmitLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
