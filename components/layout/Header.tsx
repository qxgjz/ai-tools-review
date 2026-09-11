"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import {
  Sparkles,
  LayoutGrid,
  Trophy,
  GitCompare,
  Search as SearchIcon,
  BookOpen,
  Info,
  Menu,
  X,
} from "lucide-react";
import { SearchBox } from "@/components/search/SearchBox";
import { ThemeToggle } from "@/components/theme/ThemeToggle";
import { AffiliateDisclosure } from "@/components/monetization/AffiliateDisclosure";

const NAV_LINKS = [
  { href: "/", label: "Home", icon: LayoutGrid, ariaLabel: "Go to homepage" },
  { href: "/ranking", label: "Ranking", icon: Trophy, ariaLabel: "View AI tool rankings" },
  { href: "/compare", label: "Compare", icon: GitCompare, ariaLabel: "Compare AI tools" },
  { href: "/generator", label: "Matcher", icon: SearchIcon, ariaLabel: "AI tool matcher quiz" },
  { href: "/blog", label: "Blog", icon: BookOpen, ariaLabel: "Read AI tool reviews and guides" },
  { href: "/about", label: "About", icon: Info, ariaLabel: "About AIToolCrux" },
];

export function Header() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Scroll effect - UI/UX Pro Max: sticky header with background change
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // Close mobile menu on escape
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape") setMobileMenuOpen(false);
    };
    window.addEventListener("keydown", handleEscape);
    return () => window.removeEventListener("keydown", handleEscape);
  }, []);

  // Prevent body scroll when mobile menu open
  useEffect(() => {
    if (mobileMenuOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [mobileMenuOpen]);

  return (
    <>
      {/* Skip link - accessibility (UI/UX Pro Max Priority 1) */}
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>

      <header
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-200 ${
          isScrolled
            ? "bg-white/90 dark:bg-zinc-950/90 backdrop-blur-md shadow-sm border-b border-zinc-200 dark:border-zinc-800"
            : "bg-white/80 dark:bg-zinc-950/80 backdrop-blur-md border-b border-zinc-200/50 dark:border-zinc-800/50"
        }`}
      >
        <AffiliateDisclosure />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-4">
          {/* Logo - solid color, no gradient */}
          <Link
            href="/"
            className="flex items-center gap-2 flex-shrink-0 group"
            aria-label="AIToolCrux homepage"
          >
            <div className="w-8 h-8 flex items-center justify-center rounded-lg bg-emerald-600 text-white transition-transform group-hover:scale-105">
              <Sparkles className="w-4 h-4" aria-hidden="true" />
            </div>
            <span className="text-base font-bold text-zinc-900 dark:text-white hidden sm:block">
              AIToolCrux
            </span>
          </Link>

          {/* Search - desktop only */}
          <div className="flex-1 max-w-md hidden md:block">
            <SearchBox />
          </div>

          {/* Navigation - desktop */}
          <nav className="hidden md:flex items-center gap-1" aria-label="Main navigation">
            {NAV_LINKS.map((link) => {
              const Icon = link.icon;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className="px-3 py-2 rounded-lg text-sm font-medium text-zinc-600 dark:text-zinc-400 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-emerald-50 dark:hover:bg-emerald-900/20 transition-colors focus-visible:outline-2 focus-visible:outline-emerald-500 focus-visible:outline-offset-2"
                  aria-label={link.ariaLabel}
                >
                  {link.label}
                </Link>
              );
            })}
            <ThemeToggle />
          </nav>

          {/* Mobile menu button */}
          <div className="flex items-center gap-2 md:hidden">
            <ThemeToggle />
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors focus-visible:outline-2 focus-visible:outline-emerald-500 focus-visible:outline-offset-2"
              aria-label={mobileMenuOpen ? "Close menu" : "Open menu"}
              aria-expanded={mobileMenuOpen}
              aria-controls="mobile-menu"
            >
              {mobileMenuOpen ? (
                <X className="w-5 h-5" aria-hidden="true" />
              ) : (
                <Menu className="w-5 h-5" aria-hidden="true" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile menu - slide down */}
        {mobileMenuOpen && (
          <div
            id="mobile-menu"
            className="md:hidden bg-white dark:bg-zinc-950 border-t border-zinc-200 dark:border-zinc-800 shadow-lg"
          >
            {/* Mobile search */}
            <div className="px-4 py-3 border-b border-zinc-100 dark:border-zinc-800">
              <SearchBox />
            </div>

            {/* Mobile nav links */}
            <nav className="px-2 py-2" aria-label="Mobile navigation">
              {NAV_LINKS.map((link) => {
                const Icon = link.icon;
                return (
                  <Link
                    key={link.href}
                    href={link.href}
                    onClick={() => setMobileMenuOpen(false)}
                    className="flex items-center gap-3 px-3 py-3 rounded-lg text-base font-medium text-zinc-700 dark:text-zinc-300 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-emerald-50 dark:hover:bg-emerald-900/20 transition-colors min-h-[48px]"
                    aria-label={link.ariaLabel}
                  >
                    <Icon className="w-5 h-5 text-zinc-400" aria-hidden="true" />
                    {link.label}
                  </Link>
                );
              })}
            </nav>
          </div>
        )}
      </header>

      {/* Spacer for fixed header */}
      <div className="h-16" aria-hidden="true" />
    </>
  );
}
