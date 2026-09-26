"""
Add 3 new sections to tool detail pages:
1. Who Should Use This?
2. Who Should Skip This?
3. Best Free Alternative

Inserted after the "Real User Experience" (How We Tested) section.
Uses existing card component styles. No style changes.
"""

with open('app/tools/[slug]/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# The 3 new sections JSX block
new_sections = '''
      {/* Who Should Use / Skip / Best Free Alternative (E-E-A-T decision guidance) */}
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        {/* Who Should Use This? */}
        <div className="bg-white dark:bg-zinc-900 rounded-xl border border-emerald-200 dark:border-emerald-900/50 p-6">
          <h3 className="text-base font-bold text-emerald-700 dark:text-emerald-400 mb-3 flex items-center gap-2">
            <span className="w-6 h-6 rounded-full bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center text-emerald-600 text-sm">✓</span>
            Who Should Use This?
          </h3>
          <p className="text-sm text-zinc-600 dark:text-gray-300 leading-relaxed">
            {tool.bestFor || (
              tool.category === 'image' ? 'Digital artists, designers, and marketers who need high-quality AI-generated visuals for campaigns, social media, and creative projects.' :
              tool.category === 'code' ? 'Developers and engineering teams who want to speed up coding, debugging, and code reviews with AI assistance.' :
              tool.category === 'chat' ? 'Professionals and teams looking for an AI assistant for writing, research, brainstorming, and daily productivity tasks.' :
              tool.category === 'audio' ? 'Content creators, podcasters, and video editors who need AI tools for voice generation, transcription, and audio editing.' :
              tool.category === 'agent' ? 'Power users and developers who want to automate multi-step workflows with autonomous AI agents.' :
              tool.category === 'productivity' ? 'Knowledge workers and teams who want to streamline daily tasks, summarize content, and boost productivity with AI.' :
              'Users who want to leverage AI to save time and improve their workflow. If you\'re evaluating tools in this category, this one is worth trying.'
            )}
          </p>
        </div>

        {/* Who Should Skip This? */}
        <div className="bg-white dark:bg-zinc-900 rounded-xl border border-amber-200 dark:border-amber-900/50 p-6">
          <h3 className="text-base font-bold text-amber-700 dark:text-amber-400 mb-3 flex items-center gap-2">
            <span className="w-6 h-6 rounded-full bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center text-amber-600 text-sm">!</span>
            Who Should Skip This?
          </h3>
          <p className="text-sm text-zinc-600 dark:text-gray-300 leading-relaxed">
            {tool.notIdealFor || (
              tool.hasFreeTier === false ? 'Casual users who only need occasional AI help may find the pricing hard to justify. Start with a free alternative first before committing to a paid plan.' :
              'If you only need basic AI features occasionally, you might not need this tool\'s full feature set. Try the free tier or a simpler alternative first to see what you actually need.'
            )}
          </p>
        </div>

        {/* Best Free Alternative */}
        <div className="bg-white dark:bg-zinc-900 rounded-xl border border-blue-200 dark:border-blue-900/50 p-6">
          <h3 className="text-base font-bold text-blue-700 dark:text-blue-400 mb-3 flex items-center gap-2">
            <span className="w-6 h-6 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center text-blue-600 text-sm">★</span>
            Best Free Alternative
          </h3>
          <p className="text-sm text-zinc-600 dark:text-gray-300 leading-relaxed mb-3">
            {tool.hasFreeTier ? `This tool offers a free tier that covers most basic needs. Start there before upgrading to a paid plan.` :
            (tool.category === 'image' ? 'Try DALL-E 3 (free with ChatGPT) or Bing Image Creator — both produce solid results at no cost.' :
            tool.category === 'code' ? 'Try GitHub Copilot free tier or Codeium — solid AI coding assistance without a monthly fee.' :
            tool.category === 'chat' ? 'Try ChatGPT free tier or Google Gemini — both handle most everyday AI tasks for free.' :
            tool.category === 'audio' ? 'Try ElevenLabs free tier or Google Text-to-Speech for basic voice generation at no cost.' :
            tool.category === 'agent' ? 'Try AutoGPT or OpenAI Agents (free tier) for exploring AI agent workflows without spending.' :
            'Check if there\'s a free tier or open-source alternative in this category before committing to a paid plan.')}
          </p>
          <a href={tool.officialUrl} target="_blank" rel="noopener noreferrer" className="text-xs font-medium text-blue-600 dark:text-blue-400 hover:underline">
            Check free options →
          </a>
        </div>
      </section>

'''

# Find the insertion point: after the Real User Experience section closes (line 652)
# The Real User Experience section ends with:
#         </section>
#       )}
#
#       {/* Performance Test Results

# We insert between the Real User Experience closing and Performance Test Results
insert_marker = '''      )}

      {/* Performance Test Results - Quantitative E-E-A-T data */}'''

if insert_marker in content:
    content = content.replace(insert_marker, '      )}\n' + new_sections + '      {/* Performance Test Results - Quantitative E-E-A-T data */}')
    print("[OK] Inserted 3 new sections after Real User Experience section")
else:
    print("[ERROR] Could not find insertion marker")
    # Try alternative marker
    alt_marker = '      {/* Performance Test Results'
    if alt_marker in content:
        content = content.replace(alt_marker, new_sections + alt_marker, 1)
        print("[OK] Inserted using alternative marker")

with open('app/tools/[slug]/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
with open('app/tools/[slug]/page.tsx', 'r', encoding='utf-8') as f:
    verify = f.read()

print(f"  'Who Should Use This?' present: {'Who Should Use This?' in verify}")
print(f"  'Who Should Skip This?' present: {'Who Should Skip This?' in verify}")
print(f"  'Best Free Alternative' present: {'Best Free Alternative' in verify}")
