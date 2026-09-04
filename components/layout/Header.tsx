"use client";

import Link from "next/link";
import { Sparkles, LayoutGrid, Trophy, Search as SearchIcon, GitCompare, BookOpen, Info } from "lucide-react";
import { SearchBox } from "@/components/search/SearchBox";
import { ThemeToggle } from "@/components/theme/ThemeToggle";

export function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-b border-gray-100 dark:border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-4">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 flex-shrink-0">
          <div className="w-9 h-9 flex items-center justify-center rounded-xl bg-gradient-to-br from-blue-600 to-indigo-600 text-white shadow-md">
            <Sparkles className="w-5 h-5" />
          </div>
          <span className="text-lg font-extrabold text-gray-900 dark:text-white hidden sm:block">
            AI工具测评台
          </span>
        </Link>

        {/* 搜索框 */}
        <div className="flex-1 max-w-md hidden md:block">
          <SearchBox />
        </div>

        {/* 导航 */}
        <nav className="flex items-center gap-1 sm:gap-2">
          <Link
            href="/"
            className="p-2 sm:px-3 sm:py-2 rounded-lg text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors"
          >
            <LayoutGrid className="w-5 h-5 sm:hidden" />
            <span className="hidden sm:inline">首页</span>
          </Link>
          <Link
            href="/ranking"
            className="p-2 sm:px-3 sm:py-2 rounded-lg text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors"
          >
            <Trophy className="w-5 h-5 sm:hidden" />
            <span className="hidden sm:inline">排行榜</span>
          </Link>
          <Link
            href="/compare"
            className="p-2 sm:px-3 sm:py-2 rounded-lg text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors"
          >
            <GitCompare className="w-5 h-5 sm:hidden" />
            <span className="hidden sm:inline">对比</span>
          </Link>
          <Link
            href="/generator"
            className="p-2 sm:px-3 sm:py-2 rounded-lg text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors"
          >
            <SearchIcon className="w-5 h-5 sm:hidden" />
            <span className="hidden sm:inline">智能匹配</span>
          </Link>
          <Link
            href="/blog"
            className="p-2 sm:px-3 sm:py-2 rounded-lg text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors"
          >
            <BookOpen className="w-5 h-5 sm:hidden" />
            <span className="hidden sm:inline">博客</span>
          </Link>
          <Link
            href="/about"
            className="p-2 sm:px-3 sm:py-2 rounded-lg text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors"
          >
            <Info className="w-5 h-5 sm:hidden" />
            <span className="hidden sm:inline">关于</span>
          </Link>
          <ThemeToggle />
        </nav>
      </div>
    </header>
  );
}
