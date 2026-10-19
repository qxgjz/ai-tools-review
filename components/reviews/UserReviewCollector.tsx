'use client';

import { useState } from 'react';
import { Star, MessageSquareText, ArrowDown } from 'lucide-react';

/**
 * UserReviewCollector — 工具页用户评价收集区（UGC = AI 引文燃料）
 * 战略：引导真实用户留下评分 + 评论（评论落在 Giscus 评论区，公开展示、可被 AI 爬虫引用）。
 * 不做假数据：不写 aggregateRating（Google 2026-07 政策），仅在用户产生真实 UGC 后
 * 由内容侧评估是否启用 schema 聚合。
 */
export function UserReviewCollector({ toolName }: { toolName: string }) {
  const [rating, setRating] = useState<number>(0);
  const [hover, setHover] = useState<number>(0);
  const [picked, setPicked] = useState(false);

  const scrollToComments = () => {
    document
      .getElementById('user-comments')
      ?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  return (
    <section
      aria-label="User reviews"
      className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-100 dark:border-zinc-800 shadow-sm p-6 sm:p-8 mb-6"
    >
      <div className="flex items-center gap-2 mb-1">
        <MessageSquareText className="w-5 h-5 text-blue-600 dark:text-blue-400" />
        <h2 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">
          Share Your Experience with {toolName}
        </h2>
      </div>
      <p className="text-sm text-zinc-600 dark:text-zinc-400 mb-4">
        Used {toolName}? Tell the community how it worked for you. Reviews are public,
        indexed by search engines, and help others pick the right tool.
      </p>

      <div className="flex items-center gap-1 mb-3" role="radiogroup" aria-label="Your rating">
        {[1, 2, 3, 4, 5].map((n) => (
          <button
            key={n}
            type="button"
            aria-label={`${n} star${n > 1 ? 's' : ''}`}
            onClick={() => {
              setRating(n);
              setPicked(true);
            }}
            onMouseEnter={() => setHover(n)}
            onMouseLeave={() => setHover(0)}
            className="p-1 -m-1 focus:outline-none"
          >
            <Star
              className={`w-7 h-7 transition-colors ${
                n <= (hover || rating)
                  ? 'fill-amber-400 text-amber-400'
                  : 'text-zinc-300 dark:text-zinc-600'
              }`}
            />
          </button>
        ))}
        <span className="ml-2 text-sm text-zinc-600 dark:text-zinc-400">
          {picked
            ? `You rated ${toolName} ${rating}/5 — now write the review below.`
            : 'Tap to rate, then share details below.'}
        </span>
      </div>

      <button
        type="button"
        onClick={scrollToComments}
        className="inline-flex items-center gap-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-2.5 transition-colors"
      >
        <ArrowDown className="w-4 h-4" />
        Write a full review in the comments
      </button>
    </section>
  );
}
