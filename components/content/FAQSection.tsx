'use client';

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';
import { defaultFAQs } from './faqData';
import type { FAQItem } from './faqData';

export type { FAQItem } from './faqData';

interface FAQSectionProps {
  items: FAQItem[];
  title?: string;
}

export function FAQSection({ items, title = 'Frequently Asked Questions' }: FAQSectionProps) {
  if (!items || items.length === 0) return null;

  return (
    <section className="my-8">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">{title}</h2>
      <Accordion type="single" collapsible className="w-full">
        {items.map((item, index) => (
          <AccordionItem key={index} value={`item-${index}`}>
            <AccordionTrigger className="text-left font-medium text-gray-900 dark:text-white hover:text-emerald-600 dark:hover:text-emerald-400">
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
