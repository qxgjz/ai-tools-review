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

// 默认FAQ数据 - AITool Reviews网站通用问题
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
    answer: "Start by clarifying your use case and budget, then refer to our reviews and comparison articles. We recommend trying the free version first before deciding whether to upgrade to a paid plan. If you have specific needs, check our category pages or use the comparison tool.",
  },
  {
    question: "Is my data safe with AI tools?",
    answer: "We evaluate each tool's privacy policy and data security measures in our reviews. Most mainstream AI tools use encrypted transmission and strict data protection policies. We recommend carefully reading the tool's privacy policy before use, especially when handling sensitive data.",
  },
  {
    question: "How do I get the latest AI tool updates?",
    answer: "We regularly update our reviews and add newly released AI tools. You can subscribe to our newsletter or follow our social media to get the latest AI tool news and review updates.",
  },
];
