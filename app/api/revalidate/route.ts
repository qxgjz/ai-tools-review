import { NextRequest, NextResponse } from 'next/server';
import { revalidatePath, revalidateTag } from 'next/cache';

/**
 * On-demand ISR revalidation endpoint.
 * 
 * Usage:
 *   POST /api/revalidate
 *   Headers: x-revalidate-token: <REVALIDATE_SECRET>
 *   Body: { "path": "/blog/some-slug" }  or  { "tag": "posts" }  or  { "all": true }
 * 
 * Security: requires REVALIDATE_SECRET env var (set in Vercel).
 * Without the token, returns 401.
 */
export async function POST(request: NextRequest) {
  const secret = request.headers.get('x-revalidate-token');
  const expectedSecret = process.env.REVALIDATE_SECRET;

  if (!expectedSecret) {
    return NextResponse.json(
      { error: 'REVALIDATE_SECRET not configured on server' },
      { status: 500 }
    );
  }

  if (secret !== expectedSecret) {
    return NextResponse.json(
      { error: 'Invalid revalidate token' },
      { status: 401 }
    );
  }

  try {
    const body = await request.json();
    const { path, tag, all } = body;

    const revalidated: string[] = [];

    if (all) {
      // Revalidate entire site layout
      revalidatePath('/', 'layout');
      revalidated.push('/ (layout)');
    }

    if (tag) {
      revalidateTag(tag);
      revalidated.push(`tag:${tag}`);
    }

    if (path) {
      revalidatePath(path);
      revalidated.push(path);
    }

    if (revalidated.length === 0) {
      return NextResponse.json(
        { error: 'No path, tag, or "all" specified in body' },
        { status: 400 }
      );
    }

    return NextResponse.json({
      revalidated: true,
      targets: revalidated,
      now: Date.now(),
    });
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    return NextResponse.json(
      { error: 'Revalidation failed', detail: message },
      { status: 500 }
    );
  }
}

// Also support GET for simple webhook triggers (e.g. ?token=xxx&path=/blog/xxx)
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const secret = searchParams.get('token');
  const expectedSecret = process.env.REVALIDATE_SECRET;

  if (!expectedSecret || secret !== expectedSecret) {
    return NextResponse.json(
      { error: 'Invalid or missing revalidate token' },
      { status: 401 }
    );
  }

  const path = searchParams.get('path');
  const tag = searchParams.get('tag');
  const all = searchParams.get('all') === 'true';

  const revalidated: string[] = [];

  if (all) {
    revalidatePath('/', 'layout');
    revalidated.push('/ (layout)');
  }
  if (tag) {
    revalidateTag(tag);
    revalidated.push(`tag:${tag}`);
  }
  if (path) {
    revalidatePath(path);
    revalidated.push(path);
  }

  if (revalidated.length === 0) {
    return NextResponse.json(
      { error: 'Specify ?path=, ?tag=, or ?all=true' },
      { status: 400 }
    );
  }

  return NextResponse.json({
    revalidated: true,
    targets: revalidated,
    now: Date.now(),
  });
}
