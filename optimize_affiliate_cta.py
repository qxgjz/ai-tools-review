import re

file_path = "components/monetization/AffiliateCTA.tsx"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换banner variant部分
old_banner = '''  // banner variant (default)
  return (
    <div className="bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-800 rounded-xl p-5 my-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div>
          <p className="text-sm font-semibold text-blue-900 dark:text-blue-100">
            👉 Try {toolName} Today
          </p>
          {description && (
            <p className="text-blue-700 dark:text-blue-300 text-xs mt-1">{description}</p>
          )}
        </div>
        <a
          href={url}
          target="_blank"
          rel="noopener noreferrer sponsored"
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-blue-600 text-white rounded-lg font-semibold text-sm hover:bg-blue-700 transition-colors whitespace-nowrap"
        >
          Get Started
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
          </svg>
        </a>
      </div>
    </div>
  );'''

new_banner = '''  // banner variant (default)
  return (
    <div className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950/40 dark:to-indigo-950/40 border border-blue-200 dark:border-blue-800 rounded-xl p-5 my-6 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-300">
              ✓ Free Trial Available
            </span>
            <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-300">
              ⚡ Quick Setup
            </span>
          </div>
          <p className="text-sm font-bold text-blue-900 dark:text-blue-100">
            Ready to Try {toolName}?
          </p>
          {description && (
            <p className="text-blue-700 dark:text-blue-300 text-xs mt-1">{description}</p>
          )}
        </div>
        <a
          href={url}
          target="_blank"
          rel="noopener noreferrer sponsored"
          className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-lg font-bold text-sm hover:from-blue-700 hover:to-indigo-700 transition-all shadow-md hover:shadow-lg transform hover:-translate-y-0.5 whitespace-nowrap"
        >
          Start Free Trial
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
        </a>
      </div>
      {isAffiliate && (
        <p className="text-xs text-gray-500 dark:text-gray-400 mt-3 pt-3 border-t border-blue-100 dark:border-blue-900/50">
          <em>Disclosure: This is an affiliate link. We may earn a commission if you sign up, at no extra cost to you. This never affects our rating or recommendation.</em>
        </p>
      )}
    </div>
  );'''

if old_banner in content:
    content = content.replace(old_banner, new_banner)
    print("✅ Banner variant updated successfully")
else:
    print("⚠️  Could not find exact banner variant match, trying alternative approach...")
    # 尝试用更简单的替换
    content = content.replace(
        'bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-800 rounded-xl p-5 my-6',
        'bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950/40 dark:to-indigo-950/40 border border-blue-200 dark:border-blue-800 rounded-xl p-5 my-6 shadow-sm hover:shadow-md transition-shadow'
    )
    content = content.replace(
        '👉 Try {toolName} Today',
        'Ready to Try {toolName}?'
    )
    content = content.replace(
        'Get Started',
        'Start Free Trial'
    )
    print("✅ Alternative updates applied")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ AffiliateCTA.tsx updated and saved")
