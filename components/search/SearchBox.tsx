"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Search, X, Loader2 } from "lucide-react";
import toolsData from "@/data/tools.json";
import type { Tool, Grade } from "@/types";
import { calculateScoreResult } from "@/lib/scoring";

const GRADE_TEXT_COLOR: Record<Grade, string> = {
  S: "text-amber-500 dark:text-amber-400",
  A: "text-emerald-500 dark:text-emerald-400",
  B: "text-blue-500 dark:text-blue-400",
  C: "text-yellow-500 dark:text-yellow-400",
  D: "text-red-500 dark:text-red-400",
  F: "text-gray-500 dark:text-gray-400",
};

interface SearchBoxProps {
  className?: string;
  placeholder?: string;
}

export function SearchBox({ className = "", placeholder = "搜索AI工具、厂商、标签..." }: SearchBoxProps) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Tool[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const [isSearching, setIsSearching] = useState(false);

  const inputRef = useRef<HTMLInputElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const router = useRouter();
  const debounceTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const performSearch = useCallback((value: string) => {
    const q = value.toLowerCase().trim();
    if (!q) {
      setResults([]);
      setIsOpen(false);
      setIsSearching(false);
      return;
    }
    const filtered = (toolsData as Tool[]).filter(
      (tool) =>
        tool.name.toLowerCase().includes(q) ||
        tool.vendor.toLowerCase().includes(q) ||
        tool.description.toLowerCase().includes(q) ||
        tool.tags.some((tag) => tag.toLowerCase().includes(q))
    ).slice(0, 8);
    setResults(filtered);
    setIsOpen(true);
    setIsSearching(false);
  }, []);

  const handleInputChange = useCallback(
    (value: string) => {
      setQuery(value);
      setSelectedIndex(-1);
      if (debounceTimer.current) clearTimeout(debounceTimer.current);
      if (!value.trim()) {
        setResults([]);
        setIsOpen(false);
        setIsSearching(false);
        return;
      }
      setIsSearching(true);
      debounceTimer.current = setTimeout(() => performSearch(value), 300);
    },
    [performSearch]
  );

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const goToSearchPage = useCallback(() => {
    if (query.trim()) {
      setIsOpen(false);
      router.push(`/search?q=${encodeURIComponent(query.trim())}`);
    }
  }, [query, router]);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === "Enter") {
        e.preventDefault();
        if (selectedIndex >= 0 && results[selectedIndex]) {
          setIsOpen(false);
          router.push(`/tools/${results[selectedIndex].slug}`);
        } else {
          goToSearchPage();
        }
      } else if (e.key === "ArrowDown") {
        e.preventDefault();
        setSelectedIndex((prev) => Math.min(prev + 1, results.length - 1));
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        setSelectedIndex((prev) => Math.max(prev - 1, -1));
      } else if (e.key === "Escape") {
        setIsOpen(false);
      }
    },
    [selectedIndex, results, goToSearchPage, router]
  );

  const handleClear = useCallback(() => {
    setQuery("");
    setResults([]);
    setIsOpen(false);
    setSelectedIndex(-1);
    if (debounceTimer.current) clearTimeout(debounceTimer.current);
    inputRef.current?.focus();
  }, []);

  return (
    <div ref={containerRef} className={`relative ${className}`}>
      <div className="relative">
        <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 dark:text-gray-500 pointer-events-none" />
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={(e) => handleInputChange(e.target.value)}
          onKeyDown={handleKeyDown}
          onFocus={() => results.length > 0 && setIsOpen(true)}
          placeholder={placeholder}
          aria-label="搜索AI工具"
          autoComplete="off"
          spellCheck={false}
          className="w-full pl-10 pr-10 py-2.5 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl text-sm text-gray-700 dark:text-gray-200 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:border-blue-400 dark:focus:border-blue-500 focus:ring-2 focus:ring-blue-100 dark:focus:ring-blue-900/30 transition-all"
        />
        <div className="absolute right-2.5 top-1/2 -translate-y-1/2">
          {isSearching ? (
            <Loader2 className="w-4 h-4 text-gray-400 dark:text-gray-500 animate-spin" />
          ) : query ? (
            <button onClick={handleClear} aria-label="清除搜索" className="p-1 text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 transition-colors rounded">
              <X className="w-4 h-4" />
            </button>
          ) : null}
        </div>
      </div>

      {isOpen && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-white dark:bg-gray-900 rounded-xl border border-gray-100 dark:border-gray-800 shadow-xl shadow-gray-200/60 dark:shadow-black/30 overflow-hidden z-50">
          {results.length > 0 ? (
            <>
              <div className="px-4 py-2.5 text-xs text-gray-400 dark:text-gray-500 border-b border-gray-50 dark:border-gray-800 flex items-center justify-between bg-gray-50/50 dark:bg-gray-800/50">
                <span>找到 <span className="font-semibold text-gray-600 dark:text-gray-300">{results.length}</span> 个匹配工具</span>
                <button onClick={goToSearchPage} className="text-blue-500 dark:text-blue-400 hover:text-blue-600 dark:hover:text-blue-300 font-semibold transition-colors">
                  查看全部 →
                </button>
              </div>
              <ul className="max-h-80 overflow-y-auto">
                {results.map((tool, index) => {
                  const { total, grade } = calculateScoreResult(tool.scores);
                  return (
                    <li key={tool.id}>
                      <Link
                        href={`/tools/${tool.slug}`}
                        onClick={() => setIsOpen(false)}
                        className={`flex items-center gap-3 px-4 py-3 transition-colors ${index === selectedIndex ? "bg-blue-50 dark:bg-blue-900/20" : "hover:bg-gray-50 dark:hover:bg-gray-800"}`}
                      >
                        <div className="w-9 h-9 flex-shrink-0 flex items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-indigo-600 text-white text-sm font-bold shadow-sm">
                          {tool.name.charAt(0).toUpperCase()}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="text-sm font-semibold text-gray-900 dark:text-white truncate">{tool.name}</div>
                          <div className="text-xs text-gray-400 dark:text-gray-500 truncate">{tool.vendor} · {tool.category}</div>
                        </div>
                        <div className="text-right flex-shrink-0">
                          <div className="text-sm font-bold text-gray-900 dark:text-white">{total.toFixed(1)}</div>
                          <div className={`text-xs font-bold ${GRADE_TEXT_COLOR[grade]}`}>{grade}级</div>
                        </div>
                      </Link>
                    </li>
                  );
                })}
              </ul>
            </>
          ) : (
            <div className="px-4 py-8 text-center">
              <div className="text-sm font-medium text-gray-600 dark:text-gray-300 mb-1">没有找到匹配的工具</div>
              <button onClick={goToSearchPage} className="text-xs text-blue-500 dark:text-blue-400 hover:text-blue-600 dark:hover:text-blue-300 font-semibold">
                搜索 "{query}" →
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
