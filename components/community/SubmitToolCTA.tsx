import Link from "next/link";
import { Upload, Sparkles } from "lucide-react";

/**
 * Community Flywheel CTA block (P2-GROWTH-COMMUNITY-FLYWHEEL-001)
 * Invites users to submit their AI tool/project for editorial review.
 * Pure UI component — no backend logic. Links to /submit page.
 */
export function SubmitToolCTA() {
  return (
    <section className="bg-gradient-to-br from-emerald-50 to-teal-50 dark:from-emerald-950/30 dark:to-teal-950/30 rounded-2xl p-8 border border-emerald-100 dark:border-emerald-900">
      <div className="flex flex-col sm:flex-row items-start sm:items-center gap-6">
        <div className="flex-shrink-0 w-14 h-14 flex items-center justify-center rounded-xl bg-emerald-600 text-white">
          <Upload className="w-6 h-6" aria-hidden="true" />
        </div>
        <div className="flex-1 min-w-0">
          <h2 className="text-xl font-bold text-zinc-900 dark:text-white mb-1 flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-emerald-600 dark:text-emerald-400" aria-hidden="true" />
            Built an AI tool? Get it reviewed.
          </h2>
          <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed">
            Submit your AI tool or project for our independent 6-dimension evaluation.
            Top-rated tools get featured in our rankings, newsletter, and social shoutouts.
            Free for creators — no paid placements, ever.
          </p>
        </div>
        <Link
          href="/submit"
          className="inline-flex items-center gap-2 px-6 py-3.5 bg-emerald-600 hover:bg-emerald-500 dark:bg-emerald-500 dark:hover:bg-emerald-400 text-white text-sm font-semibold rounded-lg transition-colors shadow-sm hover:shadow-md active:scale-95 flex-shrink-0"
        >
          <Upload className="w-4 h-4" aria-hidden="true" />
          Submit Your Tool
        </Link>
      </div>
    </section>
  );
}
