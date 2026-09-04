import { ImageResponse } from '@vercel/og';
import { NextRequest } from 'next/server';

export const runtime = 'edge';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  
  // 获取参数
  const title = searchParams.get('title') || 'AIToolCrux';
  const description = searchParams.get('description') || 'Discover the best AI tools with expert reviews and comparisons';
  const category = searchParams.get('category') || 'AI Tools';
  const rating = searchParams.get('rating');
  
  // 截断标题
  const displayTitle = title.length > 60 ? title.substring(0, 57) + '...' : title;
  const displayDesc = description.length > 80 ? description.substring(0, 77) + '...' : description;
  
  return new ImageResponse(
    (
      <div
        style={{
          width: '1200px',
          height: '630px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          background: 'linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #0f0f23 100%)',
          padding: '60px',
          fontFamily: 'system-ui, -apple-system, sans-serif',
        }}
      >
        {/* 顶部：Logo和分类 */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div
              style={{
                width: '56px',
                height: '56px',
                background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                borderRadius: '14px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '28px',
                fontWeight: 'bold',
                color: 'white',
              }}
            >
              AI
            </div>
            <div>
              <div style={{ fontSize: '28px', fontWeight: 'bold', color: 'white' }}>AIToolCrux</div>
              <div style={{ fontSize: '16px', color: '#94a3b8' }}>Expert AI Tool Reviews & Comparisons</div>
            </div>
          </div>
          <div
            style={{
              background: 'rgba(99, 102, 241, 0.2)',
              border: '1px solid rgba(99, 102, 241, 0.5)',
              borderRadius: '20px',
              padding: '8px 20px',
              fontSize: '16px',
              color: '#a5b4fc',
              fontWeight: '500',
            }}
          >
            {category}
          </div>
        </div>

        {/* 中间：标题和描述 */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', maxWidth: '1000px' }}>
          <div
            style={{
              fontSize: '52px',
              fontWeight: 'bold',
              color: 'white',
              lineHeight: 1.2,
              letterSpacing: '-0.02em',
            }}
          >
            {displayTitle}
          </div>
          <div
            style={{
              fontSize: '24px',
              color: '#94a3b8',
              lineHeight: 1.5,
            }}
          >
            {displayDesc}
          </div>
          {rating && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginTop: '8px' }}>
              <div style={{ fontSize: '32px', color: '#fbbf24' }}>★★★★★</div>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#fbbf24' }}>{rating}/10</div>
              <div style={{ fontSize: '18px', color: '#64748b' }}>Expert Rating</div>
            </div>
          )}
        </div>

        {/* 底部：统计和网址 */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
          <div style={{ display: 'flex', gap: '40px' }}>
            <div>
              <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#6366f1' }}>500+</div>
              <div style={{ fontSize: '16px', color: '#64748b' }}>AI Tools Reviewed</div>
            </div>
            <div>
              <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#8b5cf6' }}>6</div>
              <div style={{ fontSize: '16px', color: '#64748b' }}>Dimension Scoring</div>
            </div>
            <div>
              <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#a855f7' }}>2026</div>
              <div style={{ fontSize: '16px', color: '#64748b' }}>Latest Updates</div>
            </div>
          </div>
          <div style={{ fontSize: '20px', color: '#64748b', fontWeight: '500' }}>
            aitoolcrux.com
          </div>
        </div>
      </div>
    ),
    {
      width: 1200,
      height: 630,
    }
  );
}