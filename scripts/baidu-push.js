/**
 * 百度站长平台 API 主动推送脚本
 * 自动提交网站所有URL到百度搜索引擎，提升收录速度
 *
 * 使用方法：
 * 1. 在百度站长平台（https://ziyuan.baidu.com）验证网站
 * 2. 进入"普通收录" -> "API提交"，获取调用地址
 * 3. 将 site 和 token 填入下方常量
 * 4. 运行：node scripts/baidu-push.js
 *
 * 环境变量：
 *   BAIDU_SITE - 网站域名（如 www.aitoolcrux.com）
 *   BAIDU_TOKEN - API token
 */

const https = require("https");
const http = require("http");

// 百度站长平台配置（请填入你的 site 和 token）
const BAIDU_SITE = process.env.BAIDU_SITE || "";
const BAIDU_TOKEN = process.env.BAIDU_TOKEN || "";
const SITE_URL = "https://www.aitoolcrux.com";
const BATCH_SIZE = 2000; // 百度API一次最多提交2000条

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
 * 提交 URL 列表到百度 API
 */
async function pushToBaidu(urls) {
  if (!BAIDU_SITE || !BAIDU_TOKEN) {
    throw new Error(
      "未配置百度站长平台 site 或 token。请设置环境变量 BAIDU_SITE 和 BAIDU_TOKEN，或在脚本中填入常量。"
    );
  }

  const postData = urls.join("\n");
  const options = {
    hostname: "data.zz.baidu.com",
    path: `/urls?site=${encodeURIComponent(BAIDU_SITE)}&token=${BAIDU_TOKEN}`,
    method: "POST",
    headers: {
      "Content-Type": "text/plain",
      "Content-Length": Buffer.byteLength(postData),
    },
  };

  return new Promise((resolve, reject) => {
    const req = http.request(options, (res) => {
      let body = "";
      res.on("data", (chunk) => (body += chunk));
      res.on("end", () => {
        try {
          resolve({ statusCode: res.statusCode, data: JSON.parse(body) });
        } catch (e) {
          resolve({ statusCode: res.statusCode, data: body });
        }
      });
    });
    req.on("error", reject);
    req.write(postData);
    req.end();
  });
}

/**
 * 主函数
 */
async function main() {
  try {
    console.log("🚀 百度站长平台 API 主动推送脚本启动");
    console.log(`   网站: ${SITE_URL}`);
    console.log(`   Site: ${BAIDU_SITE || "(未配置)"}`);
    console.log(`   Token: ${BAIDU_TOKEN ? BAIDU_TOKEN.substring(0, 8) + "..." : "(未配置)"}`);
    console.log("");

    if (!BAIDU_SITE || !BAIDU_TOKEN) {
      console.log("⚠️  未配置百度站长平台 site 或 token");
      console.log("");
      console.log("配置方法：");
      console.log("  1. 访问 https://ziyuan.baidu.com 并登录");
      console.log("  2. 进入'普通收录' -> 'API提交'");
      console.log("  3. 复制调用地址中的 site 和 token");
      console.log("  4. 设置环境变量：");
      console.log("     $env:BAIDU_SITE='www.aitoolcrux.com'");
      console.log("     $env:BAIDU_TOKEN='your_token_here'");
      console.log("     node scripts/baidu-push.js");
      process.exit(0);
    }

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
    let totalNotToday = 0;
    let totalFailed = 0;

    for (let i = 0; i < batches; i++) {
      const start = i * BATCH_SIZE;
      const end = Math.min(start + BATCH_SIZE, urls.length);
      const batchUrls = urls.slice(start, end);

      console.log(`📤 第 ${i + 1}/${batches} 批: 提交 ${batchUrls.length} 个 URL (${start + 1}-${end})`);

      try {
        const result = await pushToBaidu(batchUrls);
        totalSubmitted += batchUrls.length;

        if (result.statusCode === 200 && result.data.success !== undefined) {
          totalSuccess += result.data.success || 0;
          totalNotToday += result.data.not_same_site || 0;
          console.log(`   ✅ 成功: ${result.data.success}, 非本日: ${result.data.not_same_site || 0}`);
          if (result.data.remain !== undefined) {
            console.log(`   📊 今日剩余可提交: ${result.data.remain}`);
          }
        } else {
          totalFailed += batchUrls.length;
          console.log(`   ❌ 提交失败: HTTP ${result.statusCode}`);
          console.log(`   响应: ${JSON.stringify(result.data)}`);
        }
      } catch (err) {
        totalFailed += batchUrls.length;
        console.log(`   ❌ 提交异常: ${err.message}`);
      }

      // 每批之间等待 1 秒
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
    console.log(`   非本日/重复: ${totalNotToday}`);
    console.log(`   失败: ${totalFailed}`);
    console.log("═══════════════════════════════════════");
    console.log("");
    console.log("💡 提示：");
    console.log("   - 百度API每天有提交配额，新站通常每天5000条");
    console.log("   - 建议每天运行一次，或在发布新内容后运行");
    console.log("   - 可配置为 GitHub Actions 定时任务自动执行");
    console.log("   - 提交后百度需要时间来爬取和索引，通常1-7天");

    process.exit(totalFailed > 0 ? 1 : 0);
  } catch (err) {
    console.error("❌ 脚本执行失败:", err.message);
    process.exit(1);
  }
}

main();
