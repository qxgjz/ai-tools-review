/**
 * Shared helper to skip full static generation in preview/CI environments.
 *
 * In Vercel preview deployments, pre-rendering all 533 tool pages + 105 blog
 * pages makes builds very slow. Setting SKIP_STATIC_GEN=true (or running on
 * VERCEL_ENV=preview) makes generateStaticParams return [], so pages render
 * on-demand instead of at build time.
 *
 * Production builds always pre-render normally.
 */
export function shouldSkipStaticGen(): boolean {
  if (process.env.SKIP_STATIC_GEN === "true") return true;
  // Vercel sets VERCEL_ENV to "preview" for preview deployments
  if (process.env.VERCEL_ENV === "preview") return true;
  return false;
}
