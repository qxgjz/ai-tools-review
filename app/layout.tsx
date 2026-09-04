import type { Metadata } from "next";
import Script from "next/script";
import Link from "next/link";
import "./globals.css";
import { Header } from "@/components/layout/Header";
import { ThemeProvider } from "@/components/theme/ThemeProvider";
import { AffiliateDisclosure } from "@/components/monetization/AffiliateDisclosure";
import { BaiduAnalytics } from "@/components/analytics/BaiduAnalytics";

export const metadata: Metadata = {
  metadataBase: new URL("https://www.aitoolcrux.com"),
  title: {
    default: "Best AI Tools 2026: Expert Reviews & Comparisons | AIToolCrux",
    template: "%s | AIToolCrux",
  },
  description: "Discover 500+ AI tools with expert 6-dimension reviews. Compare ChatGPT, Claude, Midjourney, GitHub Copilot & more. Find the perfect AI tool for your needs in 2026. Updated daily.",
  keywords: ["best AI tools 2026", "AI tool reviews", "AI tools comparison", "ChatGPT review", "Claude review", "Midjourney review", "AI tool directory", "top AI tools", "AI software reviews", "best AI tools for creators"],
  authors: [{ name: "AIToolCrux Editorial Team" }],
  creator: "AIToolCrux",
  publisher: "AIToolCrux",
  formatDetection: { email: false, address: false, telephone: false },
  alternates: {
    canonical: "https://www.aitoolcrux.com",
    languages: {
      "en": "https://www.aitoolcrux.com",
      "zh-CN": "https://www.aitoolcrux.com",
    },
    types: {
      "application/rss+xml": "https://www.aitoolcrux.com/rss.xml",
    },
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    alternateLocale: ["zh_CN"],
    url: "https://www.aitoolcrux.com",
    siteName: "AIToolCrux",
    title: "Best AI Tools 2026: Expert Reviews & Comparisons | AIToolCrux",
    description: "Discover 500+ AI tools with expert 6-dimension reviews. Compare ChatGPT, Claude, Midjourney & more. Find your perfect AI tool in 2026.",
  },
  twitter: {
    card: "summary_large_image",
    title: "Best AI Tools 2026: Expert Reviews & Comparisons | AIToolCrux",
    description: "Discover 500+ AI tools with expert 6-dimension reviews. Compare ChatGPT, Claude, Midjourney & more. Find your perfect AI tool in 2026.",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: { index: true, follow: true, "max-image-preview": "large", "max-snippet": -1 },
  },
  verification: {
    google: "npnKpSTQ27It6K-ajF27C1ZArzyIbSUhFlgQFS02-gs",
    other: {
      "baidu-site-verification": "codeva-UVziTZwCm7",
      "impact-site-verification": "b4de5532-56bb-418f-bd5a-7939cdd4f894",
    },
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100 transition-colors duration-200">
        <ThemeProvider>
          {/* 全局SEO结构化数据 - 服务器端渲染，确保搜索引擎可抓取 */}
          <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{
              __html: JSON.stringify({
                "@context": "https://schema.org",
                "@type": "Organization",
                name: "AIToolCrux",
                url: "https://www.aitoolcrux.com",
                logo: "https://www.aitoolcrux.com/logo.svg",
                description: "Professional AI tool reviews, comparisons, and recommendations based on a six-dimensional evaluation framework. Discover the best AI tools for creators, developers, and businesses.",
                foundingDate: "2026",
                sameAs: [
                  "https://github.com/qxgjz/ai-tools-review",
                  "https://twitter.com/aitoolcrux",
                  "https://www.linkedin.com/company/aitoolcrux",
                  "https://www.facebook.com/aitoolcrux",
                  "https://www.youtube.com/@aitoolcrux",
                  "https://www.reddit.com/r/aitoolcrux",
                ],
                contactPoint: {
                  "@type": "ContactPoint",
                  contactType: "customer support",
                  email: "support@aitoolcrux.com",
                  availableLanguage: ["English", "Chinese"],
                },
              }),
            }}
          />
          {/* 预连接关键第三方域名，优化资源加载 */}
          <link rel="preconnect" href="https://cloud.umami.is" crossOrigin="anonymous" />
          <link rel="preconnect" href="https://www.googletagmanager.com" crossOrigin="anonymous" />
          <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
          <link rel="dns-prefetch" href="https://giscus.app" />
          <link rel="dns-prefetch" href="https://fonts.googleapis.com" />
          {/* 性能优化：字体显示优化，避免FOIT */}
          <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
          <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" />
          {/* Umami 网站分析 */}
          <Script
            strategy="afterInteractive"
            src="https://cloud.umami.is/script.js"
            data-website-id="7d417a27-1151-407a-9bbb-ef8dd10189a2"
          />
          {/* Google Analytics 4 (GA4) */}
          <Script
            strategy="afterInteractive"
            src="https://www.googletagmanager.com/gtag/js?id=G-DGK601TM42"
          />
          <Script id="ga4-init" strategy="afterInteractive">
            {`
              window.dataLayer = window.dataLayer || [];
              function gtag(){dataLayer.push(arguments);}
              gtag('js', new Date());
              gtag('config', 'G-DGK601TM42', {
                page_path: window.location.pathname,
                anonymize_ip: true
              });
            `}
          </Script>
          {/* 百度统计（未配置ID时自动不加载） */}
          <BaiduAnalytics />
          <AffiliateDisclosure />
          <Header />
          <main className="pt-16">{children}</main>
          <footer className="mt-16 py-12 border-t border-gray-100 dark:border-gray-800 bg-white dark:bg-gray-900">
            <div className="max-w-7xl mx-auto px-4 sm:px-6">
              {/* 多列链接区域 */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-8">
                {/* 品牌列 */}
                <div className="col-span-2 md:col-span-1">
                  <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
                    AIToolCrux
                  </h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
                    Independent AI tool reviews and comparisons. Find the perfect AI tool for your needs.
                  </p>
                  <Link
                    href="/free-ai-tools-guide"
                    className="inline-flex items-center gap-1 text-sm font-medium text-blue-600 dark:text-blue-400 hover:underline mb-4"
                  >
                    📚 Get Free AI Tools Guide
                  </Link>
                  {/* 社交媒体链接 */}
                  <div className="flex items-center gap-3">
                    <a
                      href="https://github.com/qxgjz/ai-tools-review"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="w-8 h-8 bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-white transition-colors"
                      aria-label="GitHub"
                    >
                      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                    </a>
                    <a
                      href="https://twitter.com/aitoolcrux"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="w-8 h-8 bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-white transition-colors"
                      aria-label="Twitter/X"
                    >
                      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                    </a>
                    <a
                      href="https://www.linkedin.com/company/aitoolcrux"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="w-8 h-8 bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-white transition-colors"
                      aria-label="LinkedIn"
                    >
                      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                    </a>
                  </div>
                </div>

                {/* 主要页面列 */}
                <div>
                  <h4 className="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider mb-4">
                    Explore
                  </h4>
                  <ul className="space-y-2">
                    <li><Link href="/ranking" className="text-sm text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Tool Rankings</Link></li>
                    <li><Link href="/compare" className="text-sm text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Compare Tools</Link></li>
                    <li><Link href="/generator" className="text-sm text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">AI Tool Matcher</Link></li>
                    <li><Link href="/blog" className="text-sm text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Blog & Reviews</Link></li>
                    <li><Link href="/sitemap" className="text-sm text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Sitemap</Link></li>
                  </ul>
                </div>

                {/* 热门分类列 */}
                <div>
                  <h4 className="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider mb-4">
                    Categories
                  </h4>
                  <ul className="space-y-2">
                    <li><Link href="/category/chat" className="text-sm text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">AI Chat</Link></li>
                    <li><Link href="/category/writing" className="text-sm text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">AI Writing</Link></li>
                    <li><Link href="/category/image" className="text-sm text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">AI Image</Link></li>
                    <li><Link href="/category/code" className="text-sm text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">AI Coding</Link></li>
                    <li><Link href="/category/video" className="text-sm text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">AI Video</Link></li>
                    <li><Link href="/category/audio" className="text-sm text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">AI Audio</Link></li>
                  </ul>
                </div>

                {/* 资源列 */}
                <div>
                  <h4 className="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider mb-4">
                    Resources
                  </h4>
                  <ul className="space-y-2">
                    <li><Link href="/about" className="text-sm text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">About Us</Link></li>
                    <li><Link href="/privacy" className="text-sm text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Privacy Policy</Link></li>
                    <li><Link href="/disclosure" className="text-sm text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Affiliate Disclosure</Link></li>
                    <li><Link href="/contact" className="text-sm text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Contact Us</Link></li>
                    <li><a href="/sitemap.xml" target="_blank" rel="noopener noreferrer" className="text-sm text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">XML Sitemap</a></li>
                    <li><a href="/rss.xml" target="_blank" rel="noopener noreferrer" className="text-sm text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">RSS Feed</a></li>
                    <li><a href="/robots.txt" target="_blank" rel="noopener noreferrer" className="text-sm text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Robots.txt</a></li>
                  </ul>
                </div>
              </div>

              {/* 底部版权信息 */}
              <div className="pt-8 border-t border-gray-100 dark:border-gray-800">
                <p className="text-sm text-gray-400 dark:text-gray-500 text-center mb-2">
                  AIToolCrux · Scores based on public review methodology, affiliate revenue does not affect ratings
                </p>
                <p className="text-xs text-gray-300 dark:text-gray-600 text-center">
                  © 2026 AIToolCrux. All rights reserved.
                </p>
              </div>
            </div>
          </footer>
        </ThemeProvider>
      </body>
    </html>
  );
}
