import { notFound } from 'next/navigation';
import Link from 'next/link';
import toolsData from '@/data/tools-index.json';
import type { Tool } from '@/types';
import { ToolList } from '@/components/tools/ToolList';
import { Breadcrumb } from '@/components/ui/Breadcrumb';
import { FadeIn } from '@/components/animations';

type AudienceSlug = 'developers' | 'content-creators' | 'students' | 'startups' | 'writers';

const AUDIENCE_CONFIG: Record<
  AudienceSlug,
  {
    title: string;
    description: string;
    metaTitle: string;
    metaDescription: string;
    intro: string;
    buyingGuide: string[];
    faqs: { q: string; a: string }[];
    filter: (tool: Tool) => boolean;
  }
> = {
  developers: {
    title: 'Best AI Tools for Developers',
    description:
      'Hand-picked AI coding assistants, debuggers, and dev tools for software engineers in 2026.',
    metaTitle: 'Best AI Tools for Developers 2026: Coding Assistants & IDEs',
    metaDescription:
      'Discover the best AI tools for developers in 2026. Compare GitHub Copilot, Cursor, Windsurf, and more — pricing, features, and honest reviews.',
    intro:
      'AI has transformed software development in 2026. From intelligent code completion to AI-native IDEs that understand your entire codebase, developers now have a powerful new set of tools. The best AI developer tools fall into three categories: AI code assistants (GitHub Copilot, Cursor, Windsurf) that suggest completions and generate entire functions; AI debugging and testing tools that automatically find bugs and write tests; and AI DevOps tools that help with deployment, monitoring, and infrastructure. When choosing AI tools for development, consider your primary language, IDE preference, whether you need codebase-level understanding, privacy requirements (your code should not be used for training), and budget. Individual developers typically spend $10-20/month on their AI stack, while enterprise teams pay $19-39 per seat.',
    buyingGuide: [
      'Start with your IDE: If you love VS Code, try GitHub Copilot or Cursor; if you prefer JetBrains IDEs, use Copilot or Tabnine.',
      'Choose AI-native for deep work: Cursor and Windsurf offer AI-native IDE experiences with codebase indexing, multi-file edits, and AI terminal access.',
      'Privacy matters: Enterprise developers and OSS contributors should choose tools that guarantee your code is never used for training (Tabnine Enterprise, Copilot Business).',
      'Stack complementary tools: Use Copilot for daily completion, Cursor for refactoring large features, and an AI testing tool for generating unit tests.',
      'Budget: $10-20/month per developer covers the essentials. Try free tiers first before committing to paid plans.',
    ],
    faqs: [
      {
        q: 'Will AI tools replace developers?',
        a: "No. AI coding tools are force multipliers, not replacements. AI excels at boilerplate code, repetitive patterns, and test generation, but human developers are still needed for architecture, complex logic, security review, and product decisions. Developers who use AI tools will replace those who don't.",
      },
      {
        q: 'Cursor vs GitHub Copilot: which is better?',
        a: 'GitHub Copilot is an IDE plugin that works in VS Code and JetBrains, offering high-quality inline completions. Cursor is an AI-native IDE based on VS Code with codebase understanding, multi-file edits, and AI refactoring. Use Copilot for fast inline suggestions and Cursor for larger refactoring tasks. Many developers use both.',
      },
      {
        q: 'Is my code safe with AI tools?',
        a: 'Reputable tools (GitHub Copilot, Cursor, Tabnine) have enterprise plans that guarantee your code is never used for training. Read the terms carefully — free tiers may use your code for model improvement. For sensitive or proprietary code, always use enterprise plans with data privacy guarantees.',
      },
    ],
    filter: (tool) => {
      const t = tool as Tool;
      const cat = (t.category || '').toLowerCase();
      const tags = (t.tags || []).map((x: string) => x.toLowerCase()).join(' ');
      const bestFor = (t.bestFor || '').toLowerCase();
      return (
        cat === 'code' ||
        tags.includes('developer tools') ||
        tags.includes('code assistant') ||
        tags.includes('ai programming') ||
        bestFor.includes('developer') ||
        bestFor.includes('engineer')
      );
    },
  },
  'content-creators': {
    title: 'Best AI Tools for Content Creators',
    description:
      'AI tools for YouTubers, podcasters, designers, and social media creators — from scriptwriting to editing.',
    metaTitle: 'Best AI Tools for Content Creators 2026: Video, Audio & Design',
    metaDescription:
      'The best AI tools for content creators in 2026. From video editing and voice synthesis to design and scriptwriting — compare top tools with pricing and reviews.',
    intro:
      "Content creation has been revolutionized by AI in 2026. Whether you're a YouTuber, podcaster, social media manager, or designer, AI tools can dramatically speed up your workflow. The essential AI toolkit for content creators includes: AI video generation and editing tools (Runway, Descript, CapCut AI) for creating and polishing videos; AI voice and music tools (ElevenLabs, Suno) for voiceovers, narration, and background music; AI image and design tools (Midjourney, Canva AI, Adobe Firefly) for thumbnails, illustrations, and marketing assets; and AI writing tools (ChatGPT, Claude, Jasper) for scripts, captions, and descriptions. The best creators use a stack of 3-5 AI tools rather than relying on a single platform.",
    buyingGuide: [
      'Video first: Choose Runway Gen-3 for AI video generation, Descript for podcast/video editing, and CapCut AI for quick social videos.',
      'Audio quality matters: ElevenLabs delivers the most realistic AI voices for narration; Suno generates royalty-free background music.',
      'Design stack: Canva AI for quick social graphics, Midjourney for custom illustrations, Adobe Firefly for product mockups.',
      'Scriptwriting: Use Claude or ChatGPT for scripts and outlines, then edit for your personal voice — AI drafts, you polish.',
      'Budget: Start with free tiers, then invest $30-50/month in the tools that save you the most time.',
    ],
    faqs: [
      {
        q: 'Which AI tools do top YouTubers use?',
        a: 'Most top creators use a stack: ChatGPT or Claude for scripting, Runway or Descript for editing, ElevenLabs for voiceovers, and Canva/Midjourney for thumbnails. The key is finding tools that integrate smoothly and save the most time per video.',
      },
      {
        q: 'Can AI-generated videos be monetized on YouTube?',
        a: 'Yes, YouTube allows AI-generated content as long as it adds value and follows community guidelines. Clearly label AI-generated content where required. Many channels successfully use AI for voiceovers, background visuals, and editing while maintaining human creative direction.',
      },
      {
        q: 'Is it worth paying for AI tools as a content creator?',
        a: 'If you create content regularly (weekly or more), yes. The time saved on editing, thumbnails, and voiceovers usually justifies $30-50/month. Start with free tiers, identify the biggest time drain, and upgrade that specific tool first.',
      },
    ],
    filter: (tool) => {
      const t = tool as Tool;
      const cat = (t.category || '').toLowerCase();
      const tags = (t.tags || []).map((x: string) => x.toLowerCase()).join(' ');
      const bestFor = (t.bestFor || '').toLowerCase();
      return (
        ['video', 'audio', 'image', 'design', 'writing'].includes(cat) ||
        bestFor.includes('content') ||
        bestFor.includes('creator') ||
        tags.includes('voice ai') ||
        tags.includes('tts')
      );
    },
  },
  students: {
    title: 'Best Free AI Tools for Students',
    description:
      'Free and affordable AI tools for studying, writing papers, coding, research, and productivity in 2026.',
    metaTitle: 'Best Free AI Tools for Students 2026: Study, Write & Research',
    metaDescription:
      'Top free AI tools for students in 2026. ChatGPT free, Claude, Perplexity, Notion AI, and more — best study assistants, writing tools, and research helpers.',
    intro:
      "Students have never had better free AI tools at their disposal. From writing assistants to research tools, from coding tutors to productivity organizers, AI can be a supercharged study companion. The best free AI tools for students include: ChatGPT Free and Claude Free for homework help, essay feedback, and concept explanation; Perplexity Free for research with cited sources; Notion AI for note-taking and organization; GitHub Copilot Student Pack (free for students) for coding help; and Khanmigo for personalized learning. When using AI as a student, always check your school's academic integrity policy, use AI as a learning aid rather than a shortcut, and verify AI-generated answers with primary sources.",
    buyingGuide: [
      'General assistant: ChatGPT Free or Claude Free — explain concepts, brainstorm essays, practice problems.',
      'Research: Perplexity Free for cited answers, or Google Scholar + AI summarization for academic sources.',
      'Note-taking: Notion AI or Obsidian with AI plugins for organizing notes and creating study guides.',
      'Coding: GitHub Student Pack gives Copilot free; Replit has a free tier for practice.',
      'Budget: Everything on this list has a free tier. Premium upgrades cost $10-20/month if you need higher limits.',
    ],
    faqs: [
      {
        q: 'Is it cheating to use AI tools as a student?',
        a: "It depends on how you use them and your school's policy. AI as a tutor (explaining concepts, practicing problems, getting feedback on drafts) is generally encouraged. AI to do your homework or write essays for you violates academic integrity. Always disclose AI use where required, and use it as a learning tool rather than a replacement for understanding.",
      },
      {
        q: 'Which free AI tool is best for studying?',
        a: 'For most students, Claude Free offers the best balance: strong writing analysis, long context for reading papers, and generous free limits. Perplexity Free is best for research with citations. ChatGPT Free is best for general Q&A and coding help. Use all three free tiers.',
      },
      {
        q: 'Can AI help me write better essays?',
        a: 'Yes — use AI to brainstorm outlines, check grammar, get feedback on clarity, and identify weak arguments. Never ask AI to write the essay for you. The best workflow: draft yourself, then use AI as a writing coach to improve structure, tone, and clarity. This actually improves your own writing skills over time.',
      },
    ],
    filter: (tool) => {
      const t = tool as Tool;
      const cat = (t.category || '').toLowerCase();
      const tags = (t.tags || []).map((x: string) => x.toLowerCase()).join(' ');
      const bestFor = (t.bestFor || '').toLowerCase();
      return (
        (cat === 'chat' ||
          cat === 'writing' ||
          cat === 'productivity' ||
          cat === 'search' ||
          cat === 'code') &&
        (tool as Tool).hasFreeTier &&
        (bestFor.includes('student') ||
          bestFor.includes('learn') ||
          bestFor.includes('education') ||
          tags.includes('education'))
      );
    },
  },
  startups: {
    title: 'Best AI Tools for Startups',
    description:
      'Essential AI tools for founders and small teams — from product development to marketing, sales, and operations.',
    metaTitle: 'Best AI Tools for Startups 2026: Product, Marketing & Operations',
    metaDescription:
      'The best AI tools for startups in 2026. Build faster with AI coding, market smarter with AI content, and automate operations — all on a budget.',
    intro:
      'Startups in 2026 can do the work of a much larger team with the right AI stack. From building your product to marketing it, AI tools compress timelines and reduce costs dramatically. The essential AI toolkit for startups includes: AI development tools (Cursor, GitHub Copilot, Vercel AI) to ship product faster with fewer engineers; AI marketing tools (Jasper, Copy.ai, Canva AI) for content creation and design; AI customer support tools (Intercom Fin, Chatbase) for automated support; and AI productivity tools (Notion AI, Otter.ai, ChatGPT) for meetings, documentation, and planning. The key is to pick tools that integrate well with your existing stack and automate the most time-consuming repetitive tasks first.',
    buyingGuide: [
      'Build faster: Use Cursor or Copilot for coding, Vercel for deployment, and Supabase/Firebase for backend — ship MVP in weeks, not months.',
      'Content at scale: Jasper or Copy.ai for marketing copy, Canva AI for design, Descript for video — create content without a large team.',
      'Customer support: Deploy an AI chatbot (Intercom Fin, Chatbase) to handle common queries 24/7, freeing your team for complex issues.',
      'Operations: Notion AI for documentation, Otter.ai for meeting notes, and AI automation tools (Zapier AI, n8n) to connect everything.',
      'Budget: Focus on tools that directly impact revenue or engineering velocity. Start with $100-200/month total, then scale as you grow.',
    ],
    faqs: [
      {
        q: 'Which AI tools should a startup adopt first?',
        a: "Start with engineering tools (Cursor/Copilot) and documentation tools (Notion AI) — these have the highest ROI for early-stage teams. Add marketing tools once you have a product to promote, and customer support AI once you have real users. Don't try to adopt everything at once.",
      },
      {
        q: 'Can AI replace a marketing team for a startup?',
        a: 'AI can handle 60-70% of routine marketing work (blog drafts, social posts, email sequences, basic design), but you still need someone to set strategy, review content for brand voice, and handle high-stakes campaigns. AI replaces the grunt work, not the strategic thinking.',
      },
      {
        q: 'How much should a startup spend on AI tools?',
        a: 'Early-stage startups ($0-10k MRR) should spend $50-200/month total on AI tools. Focus on free tiers and tools that directly accelerate engineering or sales. As you grow, allocate 1-3% of revenue to productivity tools. Never let tool spending outpace revenue growth.',
      },
    ],
    filter: (tool) => {
      const t = tool as Tool;
      const cat = (t.category || '').toLowerCase();
      const bestFor = (t.bestFor || '').toLowerCase();
      const tags = (t.tags || []).map((x: string) => x.toLowerCase()).join(' ');
      return (
        cat === 'productivity' ||
        cat === 'code' ||
        cat === 'writing' ||
        bestFor.includes('startup') ||
        bestFor.includes('business') ||
        bestFor.includes('team') ||
        tags.includes('enterprise-grade')
      );
    },
  },
  writers: {
    title: 'Best AI Tools for Writers',
    description:
      'AI writing assistants, editors, and productivity tools for authors, bloggers, and copywriters in 2026.',
    metaTitle: 'Best AI Tools for Writers 2026: Writing Assistants & Editors',
    metaDescription:
      'The best AI tools for writers in 2026. Compare Claude, ChatGPT, Jasper, and Sudowrite — find the perfect writing assistant for your craft.',
    intro:
      "Writing has been transformed by AI in 2026, but the best writers know that AI is a tool, not a ghostwriter. For authors, bloggers, and copywriters, AI tools excel at the parts of writing that slow you down: overcoming writer's block, brainstorming ideas, restructuring awkward paragraphs, checking consistency across a long manuscript, and generating alternatives when you're stuck. The best AI writing tools fall into categories: general AI assistants (Claude, ChatGPT) with strong long-form writing capabilities; specialized fiction tools (Sudowrite, NovelCrafter) designed for novelists with story structure and character consistency; marketing copy tools (Jasper, Copy.ai) for ads, emails, and landing pages; and editing tools (ProWritingAid, Grammarly) that polish your prose. The golden rule: AI generates options and feedback — you make the creative decisions.",
    buyingGuide: [
      "Fiction writers: Start with Claude (free tier) for brainstorming and feedback, then consider Sudowrite for story-specific features like Show, Don't Tell.",
      'Bloggers and content writers: Claude or ChatGPT for outlines and drafts, ProWritingAid for editing, and Jasper if you need marketing templates.',
      'Copywriters: Jasper or Copy.ai for template-driven copy, Claude for original creative work — use AI for speed, not voice.',
      'Editing stack: Grammarly Premium for basic grammar, ProWritingAid for deep style and structure analysis, Claude for a second opinion on flow.',
      'Budget: Claude free tier covers most needs. Premium tools cost $12-49/month depending on your volume and specialization.',
    ],
    faqs: [
      {
        q: 'Will AI replace human writers?',
        a: "No — AI replaces repetitive writing tasks, not human creativity and voice. AI can generate a first draft in seconds, but it cannot match a writer's unique perspective, emotional intelligence, or understanding of audience. Writers who use AI will produce more work in less time; writers who don't will be outcompeted by those who do.",
      },
      {
        q: 'Is Claude better than ChatGPT for writing?',
        a: 'For long-form writing, Claude generally produces more natural, less formulaic prose and has a longer context window (up to 200K tokens), making it ideal for reviewing entire chapters or long articles. ChatGPT is stronger for research-backed writing and multi-step reasoning. Many writers use both — Claude for drafting, ChatGPT for research.',
      },
      {
        q: 'How do I keep my writing voice when using AI?',
        a: 'Give AI examples of your writing style, explicitly ask it to match your tone, and always edit AI output to add your unique voice and insights. The best approach: use AI for brainstorming, outlines, and first drafts — then rewrite in your own voice. Think of AI as a very fast first reader or writing partner, not a replacement.',
      },
    ],
    filter: (tool) => {
      const t = tool as Tool;
      const cat = (t.category || '').toLowerCase();
      const bestFor = (t.bestFor || '').toLowerCase();
      return (
        cat === 'writing' ||
        cat === 'chat' ||
        bestFor.includes('writer') ||
        bestFor.includes('writing') ||
        bestFor.includes('blog')
      );
    },
  },
};

export const dynamic = 'force-static';

export function generateStaticParams() {
  return Object.keys(AUDIENCE_CONFIG).map((slug) => ({ audience: slug }));
}

export async function generateMetadata({ params }: { params: { audience: string } }) {
  const config = AUDIENCE_CONFIG[params.audience as AudienceSlug];
  if (!config) return {};
  return {
    title: config.metaTitle,
    description: config.metaDescription,
    alternates: { canonical: `https://www.aitoolcrux.com/best-for/${params.audience}` },
    openGraph: {
      title: config.metaTitle,
      description: config.metaDescription,
      type: 'article',
      url: `https://www.aitoolcrux.com/best-for/${params.audience}`,
    },
  };
}

export default function BestForPage({ params }: { params: { audience: string } }) {
  const config = AUDIENCE_CONFIG[params.audience as AudienceSlug];
  if (!config) notFound();

  const filteredTools = (toolsData as Tool[])
    .filter(config.filter)
    .sort((a, b) => ((b as Tool).overallScore || 0) - ((a as Tool).overallScore || 0))
    .slice(0, 30);

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <Breadcrumb
        items={[
          { name: 'Home', url: '/' },
          { name: 'Best For', url: '/best-for/developers' },
          { name: config.title },
        ]}
        className="mb-6"
      />

      <FadeIn delay={0.1} y={30}>
        <section className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-violet-600 via-teal-600 to-fuchsia-600 p-8 text-white mb-8 shadow-lg">
          <div className="absolute -top-10 -right-10 w-40 h-40 bg-white/10 rounded-full blur-2xl" />
          <div className="relative">
            <h1 className="text-3xl font-extrabold mb-3">{config.title}</h1>
            <p className="text-white/85 max-w-3xl">{config.description}</p>
          </div>
        </section>
      </FadeIn>

      {/* Quick Answer */}
      <FadeIn delay={0.1} y={20}>
        <section className="bg-emerald-50 dark:bg-emerald-900/20 rounded-2xl border-l-4 border-emerald-500 p-6 mb-8">
          <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-2">Quick Answer</h2>
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
            The best AI tools for {params.audience.replace('-', ' ')} in 2026 are:{' '}
            {filteredTools.slice(0, 5).map((t, i) => (
              <span key={t.id}>
                <Link
                  href={`/tools/${(t as Tool).slug}`}
                  className="text-emerald-600 dark:text-emerald-400 hover:underline font-medium"
                >
                  {(t as Tool).name}
                </Link>
                {i < 4 ? ', ' : ''}
              </span>
            ))}
            . We evaluated {filteredTools.length} tools based on functionality, ease of use,
            pricing, and real user feedback.
          </p>
        </section>
      </FadeIn>

      {/* Key Takeaways */}
      <FadeIn delay={0.15} y={20}>
        <section className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-6 mb-8">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Key Takeaways</h2>
          <ul className="space-y-2">
            {config.buyingGuide.slice(0, 4).map((tip, i) => (
              <li key={i} className="flex gap-3">
                <span className="text-emerald-500 font-bold flex-shrink-0">✓</span>
                <span className="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">
                  {tip}
                </span>
              </li>
            ))}
          </ul>
        </section>
      </FadeIn>

      {/* Tool list */}
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
        Top {filteredTools.length} AI Tools for {params.audience.replace('-', ' ')}
      </h2>
      <ToolList tools={filteredTools} />

      {/* Introduction */}
      <FadeIn delay={0.1} y={20}>
        <section className="mt-12 bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-8">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            Complete Guide to AI Tools for {params.audience.replace('-', ' ')}
          </h2>
          <p className="text-gray-600 dark:text-gray-300 leading-relaxed">{config.intro}</p>
        </section>
      </FadeIn>

      {/* Buying Guide */}
      <FadeIn delay={0.15} y={20}>
        <section className="mt-8 bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-8">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">How to Choose</h2>
          <div className="space-y-4">
            {config.buyingGuide.map((tip, i) => (
              <div key={i} className="flex gap-4">
                <div className="flex-shrink-0 w-8 h-8 flex items-center justify-center rounded-full bg-violet-50 dark:bg-violet-900/30 text-violet-600 dark:text-violet-400 font-bold text-sm">
                  {i + 1}
                </div>
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed pt-1">{tip}</p>
              </div>
            ))}
          </div>
        </section>
      </FadeIn>

      {/* FAQ */}
      <FadeIn delay={0.2} y={20}>
        <section className="mt-8 bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-8">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
            Frequently Asked Questions
          </h2>
          <div className="space-y-6">
            {config.faqs.map((faq, i) => (
              <div key={i}>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  {faq.q}
                </h3>
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed">{faq.a}</p>
              </div>
            ))}
          </div>
        </section>
      </FadeIn>

      {/* JSON-LD FAQPage */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'FAQPage',
            mainEntity: config.faqs.map((faq) => ({
              '@type': 'Question',
              name: faq.q,
              acceptedAnswer: { '@type': 'Answer', text: faq.a },
            })),
          }),
        }}
      />
    </div>
  );
}
