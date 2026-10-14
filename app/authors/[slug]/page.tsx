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
  return Object.keys(AUTHORS).map((slug) => ({ slug }));
}

export function generateMetadata({ params }: { params: { slug: string } }): Metadata {
  const author = AUTHORS[params.slug];
  if (!author) return {};
  return {
    title: `${author.name} - ${author.role}`,
    description: `Independent AI tool reviewers following a transparent six-dimensional methodology. We test every tool 14+ days and never accept payment for ratings.`,
    alternates: {
      canonical: `https://www.aitoolcrux.com/authors/${params.slug}`,
    },
  };
}

function getAuthorPosts(slug: string) {
  const author = AUTHORS[slug];
  if (!author) return [];
  return (postsData as any[])
    .filter(
      (p) =>
        p.author?.includes(author.name.split(' ')[0]) || p.author === 'AIToolCrux Editorial Team',
    )
    .map((p) => ({
      slug: p.slug,
      title: p.title,
      date: p.date || p.publishedAt,
      readingTime: p.readingTime,
      category: p.category,
    }));
}

export default function AuthorPage({ params }: { params: { slug: string } }) {
  const author = AUTHORS[params.slug];
  if (!author) notFound();

  const allPosts = getAuthorPosts(params.slug);
  const page = 1;
  const totalPages = Math.max(1, Math.ceil(allPosts.length / PAGE_SIZE));
  const posts = allPosts.slice(0, PAGE_SIZE);

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
