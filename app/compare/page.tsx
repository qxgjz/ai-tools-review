import fs from 'fs';
import path from 'path';
import Link from 'next/link';
import type { Tool } from '@/types';
import CompareClient from '@/components/compare/CompareClient';
import comparisonsData from '@/data/comparisons.json';

export const dynamicParams = false;

const COMPARE_KEEP_FIELDS = [
  'slug',
  'name',
  'vendor',
  'category',
  'description',
  'scores',
  'tags',
  'hasFreeTier',
  'pricing',
  'lastUpdated',
] as const; // 保留：客户端 fetch 全量后按需使用（r65 起 SSR 不再 slim 映射，直接 slice 30）

export default function ComparePage() {
  const allTools: Tool[] = JSON.parse(
    fs.readFileSync(path.join(process.cwd(), 'public/data/tools-index.json'), 'utf-8'),
  );
  // r65: SSR 只内联前 30 个完整工具（首屏选择器立即可用），全量 533 个由
  // CompareClient 挂载后 fetch /data/tools-index.json 替换 —— 砍掉 ~430KB
  // Flight payload（页面曾 813KB > 500KB，seo_audit P1）。
  const tools: Tool[] = allTools.slice(0, 30);
  return (
    <>
      <CompareClient initialTools={tools} />
      {/* Comparison Hub: programmatic list of all in-depth comparison articles (hub-and-spoke internal linking) */}
      <section className="max-w-5xl mx-auto px-4 sm:px-6 pb-12">
        <div className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm p-6 sm:p-8">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
            <GitCompareIcon />
            Popular Comparison Articles
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-6">
            In-depth side-by-side reviews of the most compared AI tools in 2026.
          </p>
          <div className="grid gap-4 md:grid-cols-2">
            {(comparisonsData as Array<{ slug: string; title: string; toolA: { name: string }; toolB: { name: string } }>).map(
              (cmp) => (
                <Link
                  key={cmp.slug}
                  href={`/compare/${cmp.slug}`}
                  className="group bg-gray-50 dark:bg-gray-800/50 rounded-xl border border-gray-100 dark:border-gray-800 p-4 hover:border-blue-300 dark:hover:border-blue-700 hover:shadow-md transition-all"
                >
                  <div className="flex items-center justify-between gap-2 mb-2">
                    <span className="text-xs font-bold text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20 px-2 py-0.5 rounded-md">
                      {cmp.toolA.name} vs {cmp.toolB.name}
                    </span>
                    <span className="text-gray-400 group-hover:text-blue-500 group-hover:translate-x-1 transition-transform">
                      →
                    </span>
                  </div>
                  <h3 className="text-sm font-semibold text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors leading-snug">
                    {cmp.title}
                  </h3>
                </Link>
              ),
            )}
          </div>
        </div>
      </section>
    </>
  );
}

function GitCompareIcon() {
  return (
    <svg className="w-5 h-5 text-teal-600 dark:text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"
      />
    </svg>
  );
}
