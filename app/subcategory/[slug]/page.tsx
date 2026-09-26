import { notFound } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';
import toolsData from '@/data/tools-index.json';
import subcatsData from '@/data/subcategories.json';
import type { Tool } from '@/types';
import { calculateScoreResult } from '@/lib/scoring';
import { ToolList } from '@/components/tools/ToolList';
import { Breadcrumb } from '@/components/ui/Breadcrumb';
import { FadeIn, GradientText } from '@/components/animations';

type SubcatMeta = { name: string; parent: string; toolCount: number };
const subcats = subcatsData as Record<string, SubcatMeta>;

export const dynamic = 'force-static';

export function generateStaticParams() {
  return Object.keys(subcats)
    .filter((s) => subcats[s].toolCount > 0)
    .map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: { params: { slug: string } }) {
  const sub = subcats[params.slug];
  if (!sub) return { title: 'Not Found' };
  return {
    title: `${sub.name} - Top AI Tools 2026 | AIToolCrux`,
    description: `Discover the best ${sub.name.toLowerCase()} AI tools of 2026. We test and review ${sub.toolCount}+ tools with real hands-on experience, pricing, and pros/cons.`,
    alternates: {
      canonical: `https://www.aitoolcrux.com/subcategory/${params.slug}`,
    },
  };
}

const CATEGORY_NAMES: Record<string, string> = {
  chat: 'AI Chat',
  writing: 'AI Writing',
  image: 'AI Image',
  video: 'AI Video',
  audio: 'AI Audio',
  code: 'AI Coding',
  productivity: 'AI Productivity',
  agent: 'AI Agents',
  'agent-framework': 'Agent Frameworks',
  'agent-runtime': 'Agent Runtime',
  rag: 'RAG',
  dev: 'Dev Tools',
  'dev-tools': 'Dev Tools',
  design: 'Design',
  database: 'Database',
  memory: 'Memory',
  search: 'AI Search',
  observability: 'Observability',
};

export default function SubcategoryPage({ params }: { params: { slug: string } }) {
  const sub = subcats[params.slug];
  if (!sub || sub.toolCount === 0) notFound();

  const tools = (toolsData as Tool[]).filter((t) => (t as any).subcategory === params.slug);

  const parentName = CATEGORY_NAMES[sub.parent] || sub.parent;

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Breadcrumb
          items={[
            { name: 'Home', url: '/' },
            { name: 'Categories', url: '/category' },
            { name: parentName, url: `/category/${sub.parent}` },
            { name: sub.name },
          ]}
        />

        <FadeIn>
          <div className="mb-8">
            <Link
              href={`/category/${sub.parent}`}
              className="inline-flex items-center text-sm text-emerald-600 hover:text-emerald-700 mb-3"
            >
              <ArrowLeft className="w-4 h-4 mr-1" />
              Back to {parentName}
            </Link>
            <h1 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white mb-2">
              Top {sub.toolCount} <GradientText>{sub.name}</GradientText>
            </h1>
            <p className="text-lg text-gray-600 dark:text-gray-400 max-w-3xl">
              We tested and reviewed the best {sub.name.toLowerCase()} tools in 2026. Every tool is
              evaluated on functionality, UX, pricing, and real-world performance.
            </p>
          </div>
        </FadeIn>

        <ToolList tools={tools} />
      </div>
    </div>
  );
}
