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

export function FAQSection({ items, title = "常见问题" }: FAQSectionProps) {
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
    question: "这些AI工具是免费的吗？",
    answer: "大部分AI工具提供免费试用版或免费额度，具体免费额度因工具而异。我们在每篇评测中都会详细说明免费版和付费版的区别，帮助你选择最适合的方案。",
  },
  {
    question: "你们的评测是客观的吗？",
    answer: "是的，我们的评测基于实际使用体验和客观测试数据。每款工具都经过多维度评分，包括功能丰富度、易用性、性能、性价比、客户支持等。我们可能会通过部分工具的联盟链接获得佣金，但这不会影响我们的评分和推荐。",
  },
  {
    question: "如何选择最适合我的AI工具？",
    answer: "首先明确你的使用场景和预算，然后参考我们的评测和对比文章。我们建议先使用免费版试用，再决定是否升级到付费版。如果你有特定需求，可以查看我们的分类页面或使用对比工具。",
  },
  {
    question: "这些AI工具的数据安全吗？",
    answer: "我们在评测中会关注每款工具的隐私政策和数据安全措施。大部分主流AI工具都采用加密传输和严格的数据保护政策。建议在使用前仔细阅读工具的隐私政策，特别是处理敏感数据时。",
  },
  {
    question: "如何获取最新的AI工具更新？",
    answer: "我们会定期更新评测内容，添加新发布的AI工具。你可以订阅我们的邮件通讯，或关注我们的社交媒体，获取最新的AI工具资讯和评测更新。",
  },
];
