"use client";

import Link from "next/link";
import { Sparkles, LayoutGrid, Trophy, GitCompare, Search as SearchIcon, BookOpen, Info } from "lucide-react";
import { SearchBox } from "@/components/search/SearchBox";
import { ThemeToggle } from "@/components/theme/ThemeToggle";
import { AffiliateDisclosure } from "@/components/monetization/AffiliateDisclosure";

export function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 dark:bg-zinc-950/80 backdrop-blur-md border-b border-zinc-200 dark:border-zinc-800">
      <AffiliateDisclosure />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-4">
        {/* Logo - solid color, no gradient */}
        <Link href="/" className="flex items-center gap-2 flex-shrink-0">
          <div className="w-8 h-8 flex items-center justify-center rounded-lg bg-emerald-600 text-white">
            <Sparkles className="w-4 h-4" />
          </div>
          <span className="text-base font-bold text-zinc-900 dark:text-white hidden sm:block">
            AIToolCrux
          </span>
        </Link>

        {/* Search */}
        <div className="flex-1 max-w-md hidden md:block">
          <SearchBox />
        </div>

        {/* Navigation - single line, no icons on desktop */}
        <nav className="flex items-center gap-1">
          <Link
            href="/"
            className="px-3 py-2 rounded-lg text-sm font-medium text-zinc-600 dark:text-zinc-400 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-emerald-50 dark:hover:bg-emerald-900/20 transition-colors"
          >
            <LayoutGrid className="w-5 h-5 sm:hidden" />
            <span className="hidden sm:inline">Home</span>
          </Link>
          <Link
            href="/ranking"
            className="px-3 py-2 rounded-lg text-sm font-medium text-zinc-600 dark:text-zinc-400 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-emerald-50 dark:hover:bg-emerald-900/20 transition-colors"
          >
            <Trophy className="w-5 h-5 sm:hidden" />
            <span className="hidden sm:inline">Ranking</span>
          </Link>
          <Link
            href="/compare"
            className="px-3 py-2 rounded-lg text-sm font-medium text-zinc-600 dark:text-zinc-400 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-emerald-50 dark:hover:bg-emerald-900/20 transition-colors"
          >
            <GitCompare className="w-5 h-5 sm:hidden" />
            <span className="hidden sm:inline">Compare</span>
          </Link>
          <Link
            href="/generator"
            className="px-3 py-2 rounded-lg text-sm font-medium text-zinc-600 dark:text-zinc-400 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-emerald-50 dark:hover:bg-emerald-900/20 transition-colors"
          >
            <SearchIcon className="w-5 h-5 sm:hidden" />
            <span className="hidden sm:inline">Matcher</span>
          </Link>
          <Link
            href="/blog"
            className="px-3 py-2 rounded-lg text-sm font-medium text-zinc-600 dark:text-zinc-400 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-emerald-50 dark:hover:bg-emerald-900/20 transition-colors"
          >
            <BookOpen className="w-5 h-5 sm:hidden" />
            <span className="hidden sm:inline">Blog</span>
          </Link>
          <Link
            href="/about"
            className="px-3 py-2 rounded-lg text-sm font-medium text-zinc-600 dark:text-zinc-400 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-emerald-50 dark:hover:bg-emerald-900/20 transition-colors"
          >
            <Info className="w-5 h-5 sm:hidden" />
            <span className="hidden sm:inline">About</span>
          </Link>
          <ThemeToggle />
        </nav>
      </div>
    </header>
  );
}
