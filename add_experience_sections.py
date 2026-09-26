#!/usr/bin/env python3
"""
Add Real User Experience and Performance Test Results sections to tool detail page.
Inserts after the Testing Methodology section.
"""

import re

file_path = 'app/tools/[slug]/page.tsx'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The new sections to insert after Testing Methodology section
# We find the closing of Testing Methodology section (line with </section> followed by the Key Features comment)
new_sections = '''
      {/* Real User Experience - E-E-A-T Experience signal (first-person usage) */}
      {((tool as any).realExperience || (tool as any).usageScenarios) && (
        <section className="bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 p-6 sm:p-8 mb-6">
          <h2 className="text-lg font-bold text-zinc-900 dark:text-white mb-4 flex items-center gap-2">
            <Users className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
            Real User Experience
          </h2>
          {(tool as any).realExperience && (
            <div className="bg-emerald-50 dark:bg-emerald-900/10 border-l-4 border-emerald-500 rounded-r-xl p-4 mb-5">
              <div className="text-xs text-emerald-600 dark:text-emerald-400 uppercase tracking-wide mb-2 font-semibold">First-Hand Review</div>
              <p className="text-sm text-zinc-700 dark:text-gray-300 leading-relaxed">{(tool as any).realExperience}</p>
            </div>
          )}
          {(tool as any).usageScenarios && Array.isArray((tool as any).usageScenarios) && (tool as any).usageScenarios.length > 0 && (
            <div className="mb-5">
              <div className="text-xs text-zinc-500 dark:text-zinc-400 uppercase tracking-wide mb-3 font-semibold">Tested Use Cases</div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {(tool as any).usageScenarios.map((scenario: string, i: number) => (
                  <div key={i} className="bg-zinc-50 dark:bg-gray-800/50 rounded-xl p-4 border border-zinc-100 dark:border-zinc-700/50">
                    <div className="flex items-start gap-3">
                      <span className="flex-shrink-0 w-6 h-6 flex items-center justify-center rounded-full bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 text-xs font-bold">{i + 1}</span>
                      <p className="text-sm text-zinc-600 dark:text-gray-300 leading-relaxed">{scenario}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
          {(tool as any).notableObservations && Array.isArray((tool as any).notableObservations) && (tool as any).notableObservations.length > 0 && (
            <div>
              <div className="text-xs text-zinc-500 dark:text-zinc-400 uppercase tracking-wide mb-3 font-semibold">Key Observations</div>
              <ul className="space-y-2">
                {(tool as any).notableObservations.map((obs: string, i: number) => (
                  <li key={i} className="flex gap-3 text-sm text-zinc-600 dark:text-gray-300 leading-relaxed">
                    <Lightbulb className="w-4 h-4 flex-shrink-0 text-amber-500 mt-0.5" />
                    {obs}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </section>
      )}

      {/* Performance Test Results - Quantitative E-E-A-T data */}
      {(tool as any).testMetrics && Array.isArray((tool as any).testMetrics) && (tool as any).testMetrics.length > 0 && (
        <section className="bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 p-6 sm:p-8 mb-6">
          <h2 className="text-lg font-bold text-zinc-900 dark:text-white mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            Performance Test Results
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-zinc-200 dark:border-zinc-700">
                  <th className="text-left py-3 px-3 text-xs font-semibold text-zinc-500 dark:text-zinc-400 uppercase tracking-wide">Metric</th>
                  <th className="text-left py-3 px-3 text-xs font-semibold text-zinc-500 dark:text-zinc-400 uppercase tracking-wide">Result</th>
                  <th className="text-left py-3 px-3 text-xs font-semibold text-zinc-500 dark:text-zinc-400 uppercase tracking-wide hidden md:table-cell">Test Method</th>
                  <th className="text-left py-3 px-3 text-xs font-semibold text-zinc-500 dark:text-zinc-400 uppercase tracking-wide hidden lg:table-cell">Comparison</th>
                </tr>
              </thead>
              <tbody>
                {(tool as any).testMetrics.map((metric: any, i: number) => (
                  <tr key={i} className="border-b border-zinc-100 dark:border-zinc-800/50 hover:bg-zinc-50 dark:hover:bg-zinc-800/30 transition-colors">
                    <td className="py-3 px-3 font-medium text-zinc-900 dark:text-white">{metric.metric}</td>
                    <td className="py-3 px-3">
                      <span className="inline-block bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 px-2.5 py-1 rounded-full text-xs font-bold">{metric.value}</span>
                    </td>
                    <td className="py-3 px-3 text-zinc-600 dark:text-gray-400 text-xs hidden md:table-cell">{metric.test}</td>
                    <td className="py-3 px-3 text-zinc-500 dark:text-zinc-500 text-xs hidden lg:table-cell">{metric.comparison}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-4 italic">
            Test results are based on our independent benchmarking. Results may vary based on hardware, network conditions, and software versions.
          </p>
        </section>
      )}
'''

# Find the insertion point: before the Key Features comment
pattern = r'(\{/\* Key Features \*/)'
match = re.search(pattern, content)

if match:
    insertion_point = match.start()
    # Insert new sections before the Key Features comment
    new_content = content[:insertion_point] + new_sections + '\n      ' + content[insertion_point:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Successfully inserted Real User Experience and Performance Test Results sections.")
    print(f"File size: {len(new_content)} chars (was {len(content)} chars)")
else:
    print("ERROR: Could not find insertion point (Key Features comment)")
