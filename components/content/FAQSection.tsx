"use client";

import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";

interface FAQItem {
  question: string;
  answer: string;
}

interface FAQSectionProps {
  items: FAQItem[];
  title?: string;
}

export function FAQSection({ items, title = "Frequently Asked Questions" }: FAQSectionProps) {
  if (!items || items.length === 0) return null;

  return (
    <section className="my-8">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">{title}</h2>
      <Accordion type="single" collapsible className="w-full">
        {items.map((item, index) => (
          <AccordionItem key={index} value={`item-${index}`}>
            <AccordionTrigger className="text-left font-medium text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400">
              {item.question}
            </AccordionTrigger>
            <AccordionContent className="text-gray-600 dark:text-gray-400 leading-relaxed">
              {item.answer}
            </AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>
    </section>
  );
}

// 默认FAQ数据 - AI工具评测网站通用问题
export const defaultFAQs: FAQItem[] = [
  {
    question: "Are these AI tools free?",
    answer: "Most AI tools offer free trials or free tiers. The specific free limits vary by tool. We detail the differences between free and paid versions in each review to help you choose the best option.",
  },
  {
    question: "Are your reviews objective?",
    answer: "Yes, our reviews are based on hands-on experience and objective test data. Each tool is scored across multiple dimensions including feature richness, usability, performance, value for money, and customer support. We may earn commissions through affiliate links for some tools, but this never influences our ratings or recommendations.",
  },
  {
    question: "How do I choose the best AI tool for me?",
    answer: "首先明确你的使用场景和预算，然后参考我们的评测和对比文章。我们建议先使用免费版试用，再决定是否升级到付费版。如果你有特定需求，可以查看我们的分类页面或使用对比工具。",
  },
  {
    question: "这些Is my data safe with AI tools?",
    answer: "我们在评测中会关注每款工具的隐私政策和数据安全措施。大部分主流AI工具都采用加密传输和严格的数据保护政策。建议在使用前仔细阅读工具的隐私政策，特别是处理敏感数据时。",
  },
  {
    question: "如何获取最新的AI工具更新？",
    answer: "我们会定期更新评测内容，添加新发布的AI工具。你可以订阅我们的邮件通讯，或关注我们的社交媒体，获取最新的AI工具资讯和评测更新。",
  },
];
