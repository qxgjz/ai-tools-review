"""Fix P1-PERF-INP-002: defer CTA tracking to requestIdleCallback.
Fix GHACT-CRON-001: stagger workflow cron times off top of hour.
"""
import re
from pathlib import Path

PROJECT = Path(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")

# ============================================================
# 1. AffiliateCTA.tsx — wrap trackCtaClick in requestIdleCallback
# ============================================================
cta_path = PROJECT / "components" / "monetization" / "AffiliateCTA.tsx"
cta = cta_path.read_text(encoding="utf-8")

old_track = '''function trackCtaClick(toolName: string, variant: string, isAffiliate: boolean) {
  if (typeof window !== "undefined" && (window as any).va) {
    (window as any).va.track("affiliate_cta_click", {
      tool: toolName,
      variant: variant,
      is_affiliate: isAffiliate,
      page: window.location.pathname,
    });
  }
  if (typeof window !== "undefined") {
    window.dispatchEvent(
      new CustomEvent("cta:click", {
        detail: { tool: toolName, variant, isAffiliate, page: window.location.pathname },
      })
    );
  }
}'''

new_track = '''function trackCtaClick(toolName: string, variant: string, isAffiliate: boolean) {
  // Defer non-urgent analytics to idle time so the click→navigation path
  // is as fast as possible (improves INP). The link opens in a new tab,
  // so blocking the click handler wastes interactivity budget.
  const run = () => {
    if (typeof window !== "undefined" && (window as any).va) {
      (window as any).va.track("affiliate_cta_click", {
        tool: toolName,
        variant: variant,
        is_affiliate: isAffiliate,
        page: window.location.pathname,
      });
    }
    if (typeof window !== "undefined") {
      window.dispatchEvent(
        new CustomEvent("cta:click", {
          detail: { tool: toolName, variant, isAffiliate, page: window.location.pathname },
        })
      );
    }
  };
  if (typeof window === "undefined") return;
  const ric = (window as any).requestIdleCallback as ((cb: () => void, opts?: { timeout: number }) => number) | undefined;
  if (ric) {
    ric(run, { timeout: 1500 });
  } else {
    setTimeout(run, 0);
  }
}'''

if old_track in cta:
    cta = cta.replace(old_track, new_track)
    cta_path.write_text(cta, encoding="utf-8")
    print("OK: AffiliateCTA.tsx trackCtaClick deferred to requestIdleCallback")
else:
    print("WARN: old trackCtaClick block not found — file may already be patched or changed")

# ============================================================
# 2. Stagger GitHub Actions cron times
# ============================================================
workflows = {
    "context-update.yml": ("'0 17 * * *'", "'17 17 * * *'", "# Daily at 01:17 Beijing time = 17:17 UTC"),
    "gsc-fetch.yml": ("'0 18 * * *'", "'23 18 * * *'", "# Daily at 02:23 Beijing time = 18:23 UTC"),
    "seo-check.yml": ("'0 19 * * *'", "'11 19 * * *'", "# Daily at 03:11 Beijing time = 19:11 UTC"),
    "index-monitor.yml": ("'0 20 * * 0'", "'37 20 * * 0'", "# Weekly Monday 04:37 Beijing time = Sunday 20:37 UTC"),
}

wf_dir = PROJECT / ".github" / "workflows"
for fname, (old_cron, new_cron, new_comment) in workflows.items():
    p = wf_dir / fname
    txt = p.read_text(encoding="utf-8")
    if old_cron in txt:
        txt = txt.replace(old_cron, new_cron)
        # also update the comment line above
        txt = re.sub(
            r"# Daily at [^\n]*\n\s*- cron: '" + re.escape(new_cron.strip("'")) + r"'",
            new_comment + "\n    - cron: " + new_cron,
            txt,
        )
        p.write_text(txt, encoding="utf-8")
        print(f"OK: {fname} cron {old_cron} -> {new_cron}")
    else:
        print(f"WARN: {fname} cron {old_cron} not found (may already be changed)")

# uptime-monitor: keep */10 (already spread), no change needed.
print("\nDone.")
