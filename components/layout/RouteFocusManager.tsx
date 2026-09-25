"use client";

import { useEffect, useRef } from "react";
import { usePathname } from "next/navigation";

/**
 * RouteFocusManager - Accessibility: move focus to main content after client-side navigation.
 *
 * Next.js App Router announces route changes to screen readers via its built-in
 * route announcer, but it does NOT move keyboard focus. Focus remains on the
 * link that was clicked (which is then unmounted), causing the next Tab press
 * to restart from the top of the document.
 *
 * This component moves focus to the main content heading after each route change,
 * satisfying WCAG 2.4.3 (Focus Order) and providing a predictable keyboard experience.
 *
 * Strategy:
 * 1. On pathname change, find the first <h1> in the document
 * 2. If found, ensure it has tabIndex={-1} (set via ref) and focus it
 * 3. If no h1, fall back to the <main id="main-content"> element
 * 4. Skip focus management on initial page load (server-rendered, focus is fine)
 */
export function RouteFocusManager() {
  const pathname = usePathname();
  const isInitialLoad = useRef(true);

  useEffect(() => {
    // Skip on initial load - the page is server-rendered and focus starts at top
    if (isInitialLoad.current) {
      isInitialLoad.current = false;
      return;
    }

    // Small delay to allow the new page content to render
    const timer = setTimeout(() => {
      // Try h1 first (most specific page title)
      const heading = document.querySelector("h1");
      if (heading) {
        heading.setAttribute("tabindex", "-1");
        (heading as HTMLElement).focus({ preventScroll: false });
        return;
      }

      // Fall back to main content area
      const main = document.getElementById("main-content");
      if (main) {
        main.setAttribute("tabindex", "-1");
        main.focus({ preventScroll: false });
      }
    }, 50);

    return () => clearTimeout(timer);
  }, [pathname]);

  return null;
}
