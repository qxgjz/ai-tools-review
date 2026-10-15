import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import postsData from '@/data/posts.json';
import { shouldSkipStaticGen } from '@/lib/static-gen';
import AuthorPageContent, { PAGE_SIZE } from '@/components/authors/AuthorPageContent';

const AUTHORS: Record<string, any> = {
  'aitoolcrux-editorial-team': {
    name: 'AIToolCrux Editorial Team',
    role: 'Independent AI Tool Review Team',
    bio: 'The AIToolCrux Editorial Team is a collective of independent AI tool reviewers with decades of combined experience in tech, development, design, and content strategy. Our team follows a transparent six-dimensional evaluation methodology, tests every tool for 14+ days, and does not accept payment for higher ratings. We believe good tool selection should be based on data, not marketing hype.',
    expertise: [
      'AI Chatbots',
      'Image Generation',
      'Code Assistants',
      'Productivity Tools',
      'Video Generation',
      'Enterprise AI',
    ],
    avatar: 'AT',
    color: 'from-emerald-500 to-teal-600',
  },
};

export const dynamic = 'force-static';

export function generateStaticParams() {
  if (shouldSkipStaticGen()) return [];
  const params: { slug: string; page: string }[] = [];
  for (const slug of Object.keys(AUTHORS)) {
    const posts = (postsData as any[]).filter(
      (p) =>
        p.author?.includes(AUTHORS[slug].name.split(' ')[0]) ||
        p.author === 'AIToolCrux Editorial Team',
    );
    const totalPages = Math.max(1, Math.ceil(posts.length / PAGE_SIZE));
    for (let page = 2; page <= totalPages; page++) {
      params.push({ slug, page: String(page) });
    }
  }
  return params;
}

export function generateMetadata({
  params,
}: {
  params: { slug: string; page: string };
}): Metadata {
  const author = AUTHORS[params.slug];
  if (!author) return {};
  return {
    title: `${author.name} - AI Tool Reviews (Page ${params.page})`,
    description: `Independent AI tool reviewers following a transparent six-dimensional methodology. We test every tool 14+ days and never accept payment for ratings.`,
    alternates: {
      canonical: `https://www.aitoolcrux.com/authors/${params.slug}/page/${params.page}`,
    },
    robots: { index: true, follow: true },
  };
}

export default function AuthorPagePaged({
  params,
}: {
  params: { slug: string; page: string };
}) {
  const author = AUTHORS[params.slug];
  if (!author) notFound();

  const page = Number(params.page);
  if (!Number.isInteger(page) || page < 2) notFound();

  const allPosts = (postsData as any[])
    .filter(
      (p) =>
        p.author?.includes(author.name.split(' ')[0]) ||
        p.author === 'AIToolCrux Editorial Team',
    )
    .map((p) => ({
      slug: p.slug,
      title: p.title,
      date: p.date || p.publishedAt,
      readingTime: p.readingTime,
      category: p.category,
    }));

  const totalPages = Math.max(1, Math.ceil(allPosts.length / PAGE_SIZE));
  if (page > totalPages) notFound();

  const posts = allPosts.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  return (
    <AuthorPageContent
      author={author}
      authorSlug={params.slug}
      posts={posts}
      totalCount={allPosts.length}
      page={page}
      totalPages={totalPages}
    />
  );
}
