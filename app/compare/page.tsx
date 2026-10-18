import fs from 'fs';
import path from 'path';
import type { Tool } from '@/types';
import CompareClient from '@/components/compare/CompareClient';

export const dynamicParams = false;

export default function ComparePage() {
  const tools: Tool[] = JSON.parse(
    fs.readFileSync(path.join(process.cwd(), 'public/data/tools-index.json'), 'utf-8'),
  );
  return <CompareClient initialTools={tools} />;
}
