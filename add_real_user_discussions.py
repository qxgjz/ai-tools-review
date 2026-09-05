#!/usr/bin/env python3
"""在工具详情页添加Real User Discussions部分"""

import os

filepath = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\app\tools\[slug]\page.tsx"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 要插入的新部分
new_section = '''      </section>

      {/* Real User Discussions & Community Reviews */}
      <section className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm p-6 mb-6">
        <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
          <Users className="w-5 h-5 text-purple-600 dark:text-purple-400" />
          Real User Discussions & Community Reviews
        </h2>
        <p className="text-gray-600 dark:text-gray-300 mb-4 text-sm">
          Screenshots from real user discussions and reviews on Product Hunt, G2, Reddit, and AlternativeTo. These show how actual users experience {tool.name}.
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {/* Product Hunt */}
          <div className="border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden">
            <div className="bg-orange-50 dark:bg-orange-900/20 px-3 py-2 border-b border-gray-200 dark:border-gray-700">
              <span className="text-xs font-semibold text-orange-700 dark:text-orange-300">Product Hunt</span>
            </div>
            <img
              src={`/images/screenshots/${tool.slug}/product-hunt-search.png`}
              alt={`${tool.name} on Product Hunt`}
              className="w-full h-auto"
              onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }}
            />
          </div>
          {/* G2 */}
          <div className="border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden">
            <div className="bg-blue-50 dark:bg-blue-900/20 px-3 py-2 border-b border-gray-200 dark:border-gray-700">
              <span className="text-xs font-semibold text-blue-700 dark:text-blue-300">G2 Reviews</span>
            </div>
            <img
              src={`/images/screenshots/${tool.slug}/g2-search.png`}
              alt={`${tool.name} reviews on G2`}
              className="w-full h-auto"
              onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }}
            />
          </div>
          {/* Reddit */}
          <div className="border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden">
            <div className="bg-red-50 dark:bg-red-900/20 px-3 py-2 border-b border-gray-200 dark:border-gray-700">
              <span className="text-xs font-semibold text-red-700 dark:text-red-300">Reddit Discussions</span>
            </div>
            <img
              src={`/images/screenshots/${tool.slug}/reddit-discussion.png`}
              alt={`${tool.name} discussions on Reddit`}
              className="w-full h-auto"
              onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }}
            />
          </div>
          {/* AlternativeTo */}
          <div className="border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden">
            <div className="bg-green-50 dark:bg-green-900/20 px-3 py-2 border-b border-gray-200 dark:border-gray-700">
              <span className="text-xs font-semibold text-green-700 dark:text-green-300">AlternativeTo</span>
            </div>
            <img
              src={`/images/screenshots/${tool.slug}/alternativeto-search.png`}
              alt={`${tool.name} alternatives on AlternativeTo`}
              className="w-full h-auto"
              onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }}
            />
          </div>
        </div>
        <p className="text-xs text-gray-400 dark:text-gray-500 mt-3">
          Screenshots captured on 2026-09-05 from public community platforms. Content belongs to respective platforms and users.
        </p>
      </section>

      {/* Pricing */}'''

# 查找插入点：在ToolScreenshot组件之后、Pricing部分之前
# 匹配模式：ToolScreenshot组件结束后的 </section> 然后是 {/* Pricing */}
old_pattern = '''        />
      </section>

      {/* Pricing */}'''

if old_pattern in content:
    content = content.replace(old_pattern, new_section, 1)
    print("✅ 已在ToolScreenshot后添加Real User Discussions部分")
else:
    print("❌ 未找到插入点")
    # 尝试查找其他模式
    if "ToolScreenshot" in content:
        print("   ToolScreenshot组件存在，但插入点模式不匹配")
    if "{/* Pricing */}" in content:
        print("   Pricing部分存在")

# 写回文件
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 文件已更新")
