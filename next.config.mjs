/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true, // Enable SWC minification for faster builds

  // 图片优化
  images: {
    formats: ["image/avif", "image/webp"],
    remotePatterns: [
      { protocol: "https", hostname: "**" },
    ],
    minimumCacheTTL: 60 * 60 * 24 * 30, // 30天缓存
    deviceSizes: [480, 640, 750, 828, 1080],
    imageSizes: [32, 48, 64, 96, 128, 256],
    dangerouslyAllowSVG: true,
    contentDispositionType: "attachment",
    contentSecurityPolicy: "default-src 'self'; script-src 'none'; sandbox;",
  },

  // 压缩
  compress: true,

  // 包导入优化
  experimental: {
    optimizePackageImports: ["lucide-react", "framer-motion"],
  },

  // 生成Etags
  generateEtags: true,

  // 禁用X-Powered-By头
  poweredByHeader: false,

  // 静态资源HTTP缓存头
  async headers() {
    return [
      {
        source: "/:all*(svg|jpg|jpeg|png|webp|avif|gif|woff|woff2|ttf|eot|otf)",
        locale: false,
        headers: [
          {
            key: "Cache-Control",
            value: "public, max-age=31536000, immutable",
          },
        ],
      },
      {
        source: "/_next/static/:all*",
        headers: [
          {
            key: "Cache-Control",
            value: "public, max-age=31536000, immutable",
          },
        ],
      },
      {
        source: "/sitemap.xml",
        headers: [
          {
            key: "Cache-Control",
            value: "public, max-age=3600",
          },
          {
            key: "Content-Type",
            value: "application/xml",
          },
        ],
      },
      {
        source: "/robots.txt",
        headers: [
          {
            key: "Cache-Control",
            value: "public, max-age=86400",
          },
        ],
      },
      {
        source: "/rss.xml",
        headers: [
          {
            key: "Cache-Control",
            value: "public, max-age=3600",
          },
          {
            key: "Content-Type",
            value: "application/rss+xml; charset=utf-8",
          },
        ],
      },
      // 安全头
      {
        source: "/:path*",
        headers: [
          {
            key: "Strict-Transport-Security",
            value: "max-age=63072000; includeSubDomains; preload",
          },
          {
            key: "X-Content-Type-Options",
            value: "nosniff",
          },
          {
            key: "X-Frame-Options",
            value: "SAMEORIGIN",
          },
          {
            key: "Referrer-Policy",
            value: "strict-origin-when-cross-origin",
          },
          {
            key: "Permissions-Policy",
            value: "camera=(), microphone=(), geolocation=()",
          },
          {
            key: "Content-Security-Policy",
            value: "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://pagead2.googlesyndication.com https://www.googletagmanager.com https://googletagmanager.com https://www.google-analytics.com https://analytics.umami.is https://hm.baidu.com https://*.baidu.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob: https:; font-src 'self' data:; connect-src 'self' https://www.google-analytics.com https://analytics.umami.is https://pagead2.googlesyndication.com https://*.baidu.com; frame-src https://googleads.g.doubleclick.net https://tpc.googlesyndication.com https://pagead2.googlesyndication.com; object-src 'none'; base-uri 'self'; form-action 'self'",
          },
        ],
      },
    ];
  },

  // 重定向配置
  async redirects() {
    return [
      // 根域名到www
      {
        source: "/",
        has: [
          {
            type: "host",
            value: "aitoolcrux.com",
          },
        ],
        destination: "https://www.aitoolcrux.com/",
        permanent: true,
      },
      // 旧博客URL 301重定向到新URL（修复GSC中已索引的404页面）
      {
        source: "/blog/stable-diffusion-review",
        destination: "/blog/stable-diffusion-review-2026",
        permanent: true,
      },
      {
        source: "/blog/chatgpt-deep-review-2",
        destination: "/blog/chatgpt-deep-review-2026",
        permanent: true,
      },
      {
        source: "/blog/chatgpt-vs-claude-2026",
        destination: "/blog/chatgpt-vs-claude-2026-comparison",
        permanent: true,
      },
      // Old review URLs that 404 - redirect to actual published posts
      {
        source: "/blog/dify-review",
        destination: "/blog/dify-vs-langchain-2026",
        permanent: true,
      },
      {
        source: "/blog/cursor-review",
        destination: "/blog/cursor-vs-windsurf-2026",
        permanent: true,
      },
      {
        source: "/blog/midjourney-review",
        destination: "/blog/midjourney-vs-dalle-3-2026",
        permanent: true,
      },
      {
        source: "/blog/gemini-review",
        destination: "/blog/gemini-alternatives-2026",
        permanent: true,
      },
      {
        source: "/blog/notion-ai-review",
        destination: "/blog/notion-ai-vs-obsidian-2026",
        permanent: true,
      },
      {
        source: "/blog/elevenlabs-review",
        destination: "/blog/best-ai-voice-generators-2026",
        permanent: true,
      },
      // Duplicate blog category slugs -> canonical URLs (fix duplicate titles)
      {
        source: "/blog/category/productivity",
        destination: "/blog/category/ai-productivity",
        permanent: true,
      },
      {
        source: "/blog/category/writing",
        destination: "/blog/category/ai-writing",
        permanent: true,
      },
      {
        source: "/blog/category/image",
        destination: "/blog/category/ai-image",
        permanent: true,
      },
      {
        source: "/blog/category/agent",
        destination: "/blog/category/ai-agents",
        permanent: true,
      },
      {
        source: "/blog/category/tools",
        destination: "/blog/category/ai-tools",
        permanent: true,
      },
      {
        source: "/blog/category/coding",
        destination: "/blog/category/ai-coding",
        permanent: true,
      },
      {
        source: "/blog/category/chat",
        destination: "/blog/category/ai-chat",
        permanent: true,
      },
      {
        source: "/blog/category/search",
        destination: "/blog/category/ai-search",
        permanent: true,
      },
      {
        source: "/blog/category/design",
        destination: "/blog/category/ai-design",
        permanent: true,
      },
      {
        source: "/blog/category/code",
        destination: "/blog/category/ai-coding",
        permanent: true,
      },
      // GSC 404 fixes - blog category slugs
      {
        source: "/blog/category/video",
        destination: "/blog/category/ai-video",
        permanent: true,
      },
      {
        source: "/blog/category/audio",
        destination: "/blog/category/ai-audio",
        permanent: true,
      },
      {
        source: "/blog/category/marketing",
        destination: "/blog/category/ai-marketing",
        permanent: true,
      },
      {
        source: "/blog/category/research",
        destination: "/blog/category/ai-productivity",
        permanent: true,
      },
      // GSC 404 fixes - blog post slugs
      {
        source: "/blog/gemini-38-flash-review-2026",
        destination: "/blog/gemini_38_flash_review",
        permanent: true,
      },
      {
        source: "/blog/claude-fable-51-review-2026",
        destination: "/blog/claude_fable_51_review",
        permanent: true,
      },
      {
        source: "/blog/openai-astra-review-2026",
        destination: "/blog/openai_astra_review",
        permanent: true,
      },
      {
        source: "/blog/midjourney-v7-review-2026",
        destination: "/blog/article-api-20260904-215236-midjourney-v7-review-2026-is-it-still-the-best-ai-image-generator-md",
        permanent: true,
      },
      {
        source: "/blog/canva-ai-alternatives-2026",
        destination: "/alternatives/canva-alternatives",
        permanent: true,
      },
      // GSC 404 fixes - wrong tool slugs
      {
        source: "/tools/murf",
        destination: "/tools/murf-ai",
        permanent: true,
      },
      {
        source: "/tools/luma",
        destination: "/tools/luma-dream-machine",
        permanent: true,
      },
      {
        source: "/tools/kling",
        destination: "/tools/kling-ai",
        permanent: true,
      },
      {
        source: "/tools/wellsaid",
        destination: "/tools/wellsaid-labs",
        permanent: true,
      },
      {
        source: "/tools/soundraw",
        destination: "/category/audio",
        permanent: true,
      },
      {
        source: "/tools/playht",
        destination: "/category/audio",
        permanent: true,
      },
      {
        source: "/tools/aiva",
        destination: "/category/audio",
        permanent: true,
      },
      {
        source: "/tools/mubert",
        destination: "/category/audio",
        permanent: true,
      },
      {
        source: "/tools/udio",
        destination: "/category/audio",
        permanent: true,
      },
      {
        source: "/tools/obsidian",
        destination: "/category/productivity",
        permanent: true,
      },
      {
        source: "/tools/google",
        destination: "/category/chat",
        permanent: true,
      },
      {
        source: "/tools/hemingway",
        destination: "/category/writing",
        permanent: true,
      },
      {
        source: "/tools/amazon-q",
        destination: "/category/code",
        permanent: true,
      },
      {
        source: "/tools/languagetool",
        destination: "/category/writing",
        permanent: true,
      },
      {
        source: "/tools/prowritingaid",
        destination: "/category/writing",
        permanent: true,
      },
      {
        source: "/tools/designs-ai",
        destination: "/category/image",
        permanent: true,
      },
      {
        source: "/tools/adobe-express",
        destination: "/tools/adobe-firefly",
        permanent: true,
      },
      {
        source: "/tools/galileo",
        destination: "/category/chat",
        permanent: true,
      },
      // GSC 404 fix - /category root
      {
        source: "/category",
        destination: "/",
        permanent: true,
      },
      // OpenSEO fix: /tools list page 404 -> redirect to rankings
      {
        source: "/tools",
        destination: "/ranking",
        permanent: true,
      },
      // OpenSEO fix: /tools/amazon-polly 404 -> /category/audio
      {
        source: "/tools/amazon-polly",
        destination: "/category/audio",
        permanent: true,
      },
      // OpenSEO fix: /tools/amazon-q-developer 404 -> /category/code
      {
        source: "/tools/amazon-q-developer",
        destination: "/category/code",
        permanent: true,
      },
      // OpenSEO fix: /tools/anthropic-claude 404 -> /category/chat
      {
        source: "/tools/anthropic-claude",
        destination: "/category/chat",
        permanent: true,
      },
      // OpenSEO fix: /tools/anytype 404 -> /category/productivity
      {
        source: "/tools/anytype",
        destination: "/category/productivity",
        permanent: true,
      },
      // OpenSEO fix: /tools/bolt-new 404 -> /category/code
      {
        source: "/tools/bolt-new",
        destination: "/category/code",
        permanent: true,
      },
      // OpenSEO fix: /tools/capacities 404 -> /category/productivity
      {
        source: "/tools/capacities",
        destination: "/category/productivity",
        permanent: true,
      },
      // OpenSEO fix: /tools/closerscopy 404 -> /category/writing
      {
        source: "/tools/closerscopy",
        destination: "/category/writing",
        permanent: true,
      },
      // OpenSEO fix: /tools/coda 404 -> /category/productivity
      {
        source: "/tools/coda",
        destination: "/category/productivity",
        permanent: true,
      },
      // OpenSEO fix: /tools/coqui 404 -> /category/audio
      {
        source: "/tools/coqui",
        destination: "/category/audio",
        permanent: true,
      },
      // OpenSEO fix: /tools/craft 404 -> /category/productivity
      {
        source: "/tools/craft",
        destination: "/category/productivity",
        permanent: true,
      },
      // OpenSEO fix: /tools/figma 404 -> /category/design
      {
        source: "/tools/figma",
        destination: "/category/design",
        permanent: true,
      },
      // OpenSEO fix: /tools/firefly 404 -> /category/design
      {
        source: "/tools/firefly",
        destination: "/category/design",
        permanent: true,
      },
      // OpenSEO fix: /tools/frase 404 -> /category/writing
      {
        source: "/tools/frase",
        destination: "/category/writing",
        permanent: true,
      },
      // OpenSEO fix: /tools/getimg 404 -> /category/image
      {
        source: "/tools/getimg",
        destination: "/category/image",
        permanent: true,
      },
      // OpenSEO fix: /tools/google 404 -> /category/chat
      {
        source: "/tools/google",
        destination: "/category/chat",
        permanent: true,
      },
      // OpenSEO fix: /tools/google-text-to-speech 404 -> /category/audio
      {
        source: "/tools/google-text-to-speech",
        destination: "/category/audio",
        permanent: true,
      },
      // OpenSEO fix: /tools/heptabase 404 -> /category/productivity
      {
        source: "/tools/heptabase",
        destination: "/category/productivity",
        permanent: true,
      },
      // OpenSEO fix: /tools/ink 404 -> /category/productivity
      {
        source: "/tools/ink",
        destination: "/category/productivity",
        permanent: true,
      },
      // OpenSEO fix: /tools/jetbrains-ai 404 -> /category/code
      {
        source: "/tools/jetbrains-ai",
        destination: "/category/code",
        permanent: true,
      },
      // OpenSEO fix: /tools/llama 404 -> /category/chat
      {
        source: "/tools/llama",
        destination: "/category/chat",
        permanent: true,
      },
      // OpenSEO fix: /tools/logseq 404 -> /category/productivity
      {
        source: "/tools/logseq",
        destination: "/category/productivity",
        permanent: true,
      },
      // OpenSEO fix: /tools/lumen5 404 -> /category/video
      {
        source: "/tools/lumen5",
        destination: "/category/video",
        permanent: true,
      },
      // OpenSEO fix: /tools/mem-ai 404 -> /category/productivity
      {
        source: "/tools/mem-ai",
        destination: "/category/productivity",
        permanent: true,
      },
      // OpenSEO fix: /tools/mutable-ai 404 -> /category/image
      {
        source: "/tools/mutable-ai",
        destination: "/category/image",
        permanent: true,
      },
      // OpenSEO fix: /tools/natural-reader 404 -> /category/audio
      {
        source: "/tools/natural-reader",
        destination: "/category/audio",
        permanent: true,
      },
      // OpenSEO fix: /tools/playground 404 -> /category/image
      {
        source: "/tools/playground",
        destination: "/category/image",
        permanent: true,
      },
      // OpenSEO fix: /tools/recraft 404 -> /category/image
      {
        source: "/tools/recraft",
        destination: "/category/image",
        permanent: true,
      },
      // OpenSEO fix: /tools/reflect 404 -> /category/productivity
      {
        source: "/tools/reflect",
        destination: "/category/productivity",
        permanent: true,
      },
      // OpenSEO fix: /tools/replit-agent 404 -> /category/code
      {
        source: "/tools/replit-agent",
        destination: "/category/code",
        permanent: true,
      },
      // OpenSEO fix: /tools/resemble-ai 404 -> /category/audio
      {
        source: "/tools/resemble-ai",
        destination: "/category/audio",
        permanent: true,
      },
      // OpenSEO fix: /tools/snappa 404 -> /category/design
      {
        source: "/tools/snappa",
        destination: "/category/design",
        permanent: true,
      },
      // OpenSEO fix: /tools/stencil 404 -> /category/design
      {
        source: "/tools/stencil",
        destination: "/category/design",
        permanent: true,
      },
      // OpenSEO fix: /tools/surfer 404 -> /category/writing
      {
        source: "/tools/surfer",
        destination: "/category/writing",
        permanent: true,
      },
      // OpenSEO fix: /tools/tana 404 -> /category/productivity
      {
        source: "/tools/tana",
        destination: "/category/productivity",
        permanent: true,
      },
      // OpenSEO fix: /tools/tensor-art 404 -> /category/image
      {
        source: "/tools/tensor-art",
        destination: "/category/image",
        permanent: true,
      },
      // OpenSEO fix: /tools/visme 404 -> /category/design
      {
        source: "/tools/visme",
        destination: "/category/design",
        permanent: true,
      },
    ];
  },
};

export default nextConfig;
