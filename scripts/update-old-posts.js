/**
 * 内容更新机制脚本
 * 自动检测超过90天未更新的博客文章，并更新其 lastUpdated 日期
 *
 * 使用方法：
 *   node scripts/update-old-posts.js          # 实际更新
 *   node scripts/update-old-posts.js --dry-run # 只显示需要更新的文章，不实际修改
 *
 * 功能：
 *   1. 检查所有博客文章的 publishedAt 和 lastUpdated 日期
 *   2. 找出超过 UPDATE_THRESHOLD_DAYS 天未更新的文章
 *   3. 自动更新这些文章的 lastUpdated 为当前日期
 *   4. 输出更新日志
 *   5. 可配置为 GitHub Actions 定时任务（每月运行一次）
 */

const fs = require("fs");
const path = require("path");

// 配置
const UPDATE_THRESHOLD_DAYS = 90; // 超过90天未更新的文章需要更新
const POSTS_FILE = path.join(__dirname, "..", "data", "posts.json");
const DRY_RUN = process.argv.includes("--dry-run");

/**
 * 计算两个日期之间的天数差
 */
function daysBetween(date1, date2) {
  const oneDay = 24 * 60 * 60 * 1000;
  return Math.round(Math.abs((date1 - date2) / oneDay));
}

/**
 * 获取当前日期字符串（YYYY-MM-DD格式）
 */
function getCurrentDateString() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

/**
 * 主函数
 */
function main() {
  console.log("🚀 内容更新机制脚本启动");
  console.log(`   更新阈值: ${UPDATE_THRESHOLD_DAYS} 天`);
  console.log(`   模式: ${DRY_RUN ? "预览模式（不实际修改）" : "实际更新模式"}`);
  console.log(`   数据文件: ${POSTS_FILE}`);
  console.log("");

  // 1. 读取文章数据
  if (!fs.existsSync(POSTS_FILE)) {
    console.error("❌ 文章数据文件不存在:", POSTS_FILE);
    process.exit(1);
  }

  const posts = JSON.parse(fs.readFileSync(POSTS_FILE, "utf-8"));
  console.log(`📊 共读取到 ${posts.length} 篇文章`);

  // 2. 检查每篇文章的更新日期
  const now = new Date();
  const outdatedPosts = [];
  const recentPosts = [];

  for (const post of posts) {
    // 使用 lastUpdated（如果有），否则使用 publishedAt
    const lastUpdateDate = post.lastUpdated
      ? new Date(post.lastUpdated)
      : new Date(post.publishedAt);

    const daysSinceUpdate = daysBetween(now, lastUpdateDate);

    const postInfo = {
      slug: post.slug,
      title: post.title,
      publishedAt: post.publishedAt,
      lastUpdated: post.lastUpdated || post.publishedAt,
      daysSinceUpdate,
      category: post.category,
    };

    if (daysSinceUpdate >= UPDATE_THRESHOLD_DAYS) {
      outdatedPosts.push(postInfo);
    } else {
      recentPosts.push(postInfo);
    }
  }

  // 3. 输出统计
  console.log("");
  console.log("═══════════════════════════════════════");
  console.log("📊 文章更新状态统计");
  console.log("═══════════════════════════════════════");
  console.log(`   总文章数: ${posts.length}`);
  console.log(`   需要更新 (≥${UPDATE_THRESHOLD_DAYS}天): ${outdatedPosts.length}`);
  console.log(`   近期更新 (<${UPDATE_THRESHOLD_DAYS}天): ${recentPosts.length}`);
  console.log("═══════════════════════════════════════");

  // 4. 如果有需要更新的文章，列出详情
  if (outdatedPosts.length > 0) {
    console.log("");
    console.log("📋 需要更新的文章列表：");
    console.log("");

    // 按未更新天数排序（最久未更新的在前）
    outdatedPosts.sort((a, b) => b.daysSinceUpdate - a.daysSinceUpdate);

    outdatedPosts.forEach((post, index) => {
      console.log(
        `  ${String(index + 1).padStart(2, " ")}. [${post.daysSinceUpdate}天未更新] ${post.title}`
      );
      console.log(`      分类: ${post.category} | 发布: ${post.publishedAt} | 最后更新: ${post.lastUpdated}`);
      console.log(`      Slug: ${post.slug}`);
    });

    // 5. 执行更新（如果不是预览模式）
    if (!DRY_RUN) {
      console.log("");
      console.log("🔄 正在更新文章...");

      const currentDate = getCurrentDateString();
      let updatedCount = 0;

      for (const post of posts) {
        const postInfo = outdatedPosts.find((p) => p.slug === post.slug);
        if (postInfo) {
          post.lastUpdated = currentDate;
          updatedCount++;
          console.log(`   ✅ 已更新: ${post.title} -> ${currentDate}`);
        }
      }

      // 6. 写回文件
      fs.writeFileSync(POSTS_FILE, JSON.stringify(posts, null, 2), "utf-8");

      console.log("");
      console.log("═══════════════════════════════════════");
      console.log("✅ 更新完成");
      console.log("═══════════════════════════════════════");
      console.log(`   已更新文章数: ${updatedCount}`);
      console.log(`   更新日期: ${currentDate}`);
      console.log(`   数据文件已保存: ${POSTS_FILE}`);
      console.log("═══════════════════════════════════════");
      console.log("");
      console.log("💡 后续步骤：");
      console.log("   1. 检查更新后的文章内容是否需要实际内容更新（不只是日期）");
      console.log("   2. 重新构建并部署网站：npm run build && vercel --prod");
      console.log("   3. 提交更新后的 sitemap 到 Google Search Console 和百度站长平台");
      console.log("   4. 可配置为 GitHub Actions 每月自动运行");
    } else {
      console.log("");
      console.log("👀 预览模式：未实际修改文件。");
      console.log("   如需实际更新，请运行：node scripts/update-old-posts.js");
    }
  } else {
    console.log("");
    console.log("✅ 所有文章都在近期更新过，无需更新。");
  }

  // 7. 输出按分类统计
  console.log("");
  console.log("📊 按分类统计（需要更新的文章）：");
  const categoryStats = {};
  for (const post of outdatedPosts) {
    categoryStats[post.category] = (categoryStats[post.category] || 0) + 1;
  }
  for (const [category, count] of Object.entries(categoryStats).sort((a, b) => b[1] - a[1])) {
    console.log(`   ${category}: ${count} 篇`);
  }

  process.exit(0);
}

main();
