/**
 * IndexNow 主动提交脚本
 * 自动提交网站所有URL到 IndexNow API（Bing/Yandex等搜索引擎）
 *
 * 使用方法：
 *   node scripts/indexnow-submit.js
 *
 * 环境变量：
 *   INDEXNOW_KEY - IndexNow API Key（默认使用 26d1e3b4048b4e36984404ef990e5a16）
 *   SITE_URL - 网站URL（默认 https://www.aitoolcrux.com）
 */

const https = require("https");
const { URL } = require("url");

const INDEXNOW_KEY = process.env.INDEXNOW_KEY || "26d1e3b4048b4e36984404ef990e5a16";
const SITE_URL = process.env.SITE_URL || "https://www.aitoolcrux.com";
const BATCH_SIZE = 10000; // IndexNow 一次最多提交 10000 个 URL

/**
 * 从 sitemap.xml 获取所有 URL
 */
async function getUrlsFromSitemap() {
  const sitemapUrl = `${SITE_URL}/sitemap.xml`;
  console.log(`📡 正在获取 sitemap: ${sitemapUrl}`);

  return new Promise((resolve, reject) => {
    https
      .get(sitemapUrl, (res) => {
        let data = "";
        res.on("data", (chunk) => (data += chunk));
        res.on("end", () => {
          if (res.statusCode !== 200) {
            reject(new Error(`获取 sitemap 失败: HTTP ${res.statusCode}`));
            return;
          }
          // 解析 XML 中的 <loc> 标签
          const urlRegex = /<loc>([^<]+)<\/loc>/g;
          const urls = [];
          let match;
          while ((match = urlRegex.exec(data)) !== null) {
            urls.push(match[1]);
          }
          resolve(urls);
        });
      })
      .on("error", reject);
  });
}

/**
 * 提交 URL 列表到 IndexNow API
 */
async function submitToIndexNow(urls) {
  const payload = JSON.stringify({
    host: new URL(SITE_URL).hostname,
    key: INDEXNOW_KEY,
    keyLocation: `${SITE_URL}/${INDEXNOW_KEY}.txt`,
    urlList: urls,
  });

  // 尝试多个 API 端点
  const endpoints = [
    "https://api.indexnow.org/IndexNow",
    "https://www.bing.com/indexnow",
  ];

  let lastError = null;

  for (const endpoint of endpoints) {
    try {
      const url = new URL(endpoint);
      const options = {
        hostname: url.hostname,
        path: url.pathname,
        method: "POST",
        headers: {
          "Content-Type": "application/json; charset=utf-8",
          "Content-Length": Buffer.byteLength(payload),
        },
      };

      console.log(`   尝试端点: ${endpoint}`);

      const result = await new Promise((resolve, reject) => {
        const req = https.request(options, (res) => {
          let body = "";
          res.on("data", (chunk) => (body += chunk));
          res.on("end", () => {
            resolve({ statusCode: res.statusCode, body });
          });
        });
        req.on("error", reject);
        req.write(payload);
        req.end();
      });

      if (result.statusCode === 200 || result.statusCode === 202) {
        return result;
      }

      lastError = `HTTP ${result.statusCode}: ${result.body}`;
      console.log(`   端点返回 ${result.statusCode}，尝试下一个...`);
    } catch (err) {
      lastError = err.message;
      console.log(`   端点异常: ${err.message}，尝试下一个...`);
    }
  }

  throw new Error(`所有端点均失败: ${lastError}`);
}

/**
 * 主函数
 */
async function main() {
  try {
    console.log("🚀 IndexNow 主动提交脚本启动");
    console.log(`   网站: ${SITE_URL}`);
    console.log(`   API Key: ${INDEXNOW_KEY.substring(0, 8)}...`);
    console.log("");

    // 1. 获取所有 URL
    const urls = await getUrlsFromSitemap();
    console.log(`✅ 获取到 ${urls.length} 个 URL`);

    if (urls.length === 0) {
      console.log("⚠️  没有获取到 URL，退出");
      process.exit(0);
    }

    // 2. 分批提交
    const batches = Math.ceil(urls.length / BATCH_SIZE);
    console.log(`📦 分 ${batches} 批提交（每批最多 ${BATCH_SIZE} 个）`);
    console.log("");

    let totalSubmitted = 0;
    let totalSuccess = 0;
    let totalFailed = 0;

    for (let i = 0; i < batches; i++) {
      const start = i * BATCH_SIZE;
      const end = Math.min(start + BATCH_SIZE, urls.length);
      const batchUrls = urls.slice(start, end);

      console.log(`📤 第 ${i + 1}/${batches} 批: 提交 ${batchUrls.length} 个 URL (${start + 1}-${end})`);

      try {
        const result = await submitToIndexNow(batchUrls);
        totalSubmitted += batchUrls.length;

        if (result.statusCode === 200) {
          totalSuccess += batchUrls.length;
          console.log(`   ✅ 提交成功 (HTTP ${result.statusCode})`);
        } else if (result.statusCode === 202) {
          totalSuccess += batchUrls.length;
          console.log(`   ⏳ 已接受，待处理 (HTTP ${result.statusCode})`);
        } else {
          totalFailed += batchUrls.length;
          console.log(`   ❌ 提交失败 (HTTP ${result.statusCode}): ${result.body}`);
        }
      } catch (err) {
        totalFailed += batchUrls.length;
        console.log(`   ❌ 提交异常: ${err.message}`);
      }

      // 每批之间等待 1 秒，避免请求过快
      if (i < batches - 1) {
        await new Promise((resolve) => setTimeout(resolve, 1000));
      }
    }

    // 3. 输出总结
    console.log("");
    console.log("═══════════════════════════════════════");
    console.log("📊 提交完成总结");
    console.log("═══════════════════════════════════════");
    console.log(`   总 URL 数: ${urls.length}`);
    console.log(`   已提交: ${totalSubmitted}`);
    console.log(`   成功: ${totalSuccess}`);
    console.log(`   失败: ${totalFailed}`);
    console.log(`   成功率: ${totalSubmitted > 0 ? ((totalSuccess / totalSubmitted) * 100).toFixed(1) : 0}%`);
    console.log("═══════════════════════════════════════");
    console.log("");
    console.log("💡 提示：");
    console.log("   - IndexNow 会将 URL 推送给 Bing、Yandex 等搜索引擎");
    console.log("   - 首次提交后，搜索引擎需要时间来爬取和索引");
    console.log("   - 建议每周运行一次，或在发布新内容后运行");
    console.log("   - 可配置为 GitHub Actions 定时任务自动执行");

    process.exit(totalFailed > 0 ? 1 : 0);
  } catch (err) {
    console.error("❌ 脚本执行失败:", err.message);
    process.exit(1);
  }
}

main();
