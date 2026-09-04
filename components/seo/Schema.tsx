"use client";

import { useEffect } from "react";

interface ReviewSchemaProps {
  name: string;
  reviewBody: string;
  ratingValue: number;
  bestRating?: number;
  worstRating?: number;
  author?: string;
  datePublished?: string;
  itemReviewed?: string;
}

/**
 * Review Schema - 评测文章结构化数据
 * 帮助搜索引擎理解评测内容，显示评分星级
 */
export function ReviewSchema({
  name,
  reviewBody,
  ratingValue,
  bestRating = 10,
  worstRating = 1,
  author = "AIToolCrux Editorial Team",
  datePublished = new Date().toISOString().split("T")[0],
  itemReviewed,
}: ReviewSchemaProps) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "Review",
    name: name,
    reviewBody: reviewBody,
    reviewRating: {
      "@type": "Rating",
      ratingValue: ratingValue,
      bestRating: bestRating,
      worstRating: worstRating,
    },
    author: {
      "@type": "Organization",
      name: author,
    },
    datePublished: datePublished,
    itemReviewed: {
      "@type": "SoftwareApplication",
      name: itemReviewed || name,
      applicationCategory: "AI Tool",
    },
    publisher: {
      "@type": "Organization",
      name: "AIToolCrux",
      url: "https://www.aitoolcrux.com",
    },
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}

interface FAQSchemaProps {
  faqs: Array<{
    question: string;
    answer: string;
  }>;
}

/**
 * FAQ Schema - 常见问题结构化数据
 * 帮助搜索引擎在搜索结果中显示FAQ富摘要
 */
export function FAQSchema({ faqs }: FAQSchemaProps) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: faqs.map((faq) => ({
      "@type": "Question",
      name: faq.question,
      acceptedAnswer: {
        "@type": "Answer",
        text: faq.answer,
      },
    })),
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}

interface ProductSchemaProps {
  name: string;
  description: string;
  brand?: string;
  category?: string;
  ratingValue?: number;
  reviewCount?: number;
  price?: string;
  image?: string;
  url?: string;
}

/**
 * Product Schema - 产品/工具结构化数据
 * 帮助搜索引擎理解工具产品信息，显示价格和评分
 */
export function ProductSchema({
  name,
  description,
  brand,
  category = "AI Tool",
  ratingValue,
  reviewCount = 1,
  price = "Free",
  image,
  url,
}: ProductSchemaProps) {
  const schema: any = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    name: name,
    description: description,
    applicationCategory: category,
    operatingSystem: "Web",
    offers: {
      "@type": "Offer",
      price: price === "Free" ? "0" : price,
      priceCurrency: "USD",
      availability: "https://schema.org/InStock",
    },
  };

  if (brand) {
    schema.brand = {
      "@type": "Organization",
      name: brand,
    };
  }

  if (ratingValue) {
    schema.aggregateRating = {
      "@type": "AggregateRating",
      ratingValue: ratingValue,
      reviewCount: reviewCount,
      bestRating: 10,
      worstRating: 1,
    };
  }

  if (image) {
    schema.image = image;
  }

  if (url) {
    schema.url = url;
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}

interface BreadcrumbSchemaProps {
  items: Array<{
    name: string;
    url: string;
  }>;
}

/**
 * Breadcrumb Schema - 面包屑导航结构化数据
 * 帮助搜索引擎理解页面层级关系
 */
export function BreadcrumbSchema({ items }: BreadcrumbSchemaProps) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: items.map((item, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: item.name,
      item: `https://www.aitoolcrux.com${item.url}`,
    })),
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}

/**
 * Organization Schema - 网站组织信息结构化数据
 * 全局注入，帮助搜索引擎理解网站身份
 */
export function OrganizationSchema() {
  const schema = {
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
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}

/**
 * WebSite Schema - 网站信息结构化数据
 * 包含站内搜索功能，帮助搜索引擎显示搜索框
 */
export function WebSiteSchema() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: "AIToolCrux",
    url: "https://www.aitoolcrux.com",
    description: "Professional AI tool reviews, comparisons, and recommendations.",
    potentialAction: {
      "@type": "SearchAction",
      target: {
        "@type": "EntryPoint",
        urlTemplate: "https://www.aitoolcrux.com/search?q={search_term_string}",
      },
      "query-input": "required name=search_term_string",
    },
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
