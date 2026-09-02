/**
 * 461个开源AI工具数据转换脚本
 * 将 awesome-ai-agent-tools 数据集转换为网站工具格式，并生成六维评分
 */

const fs = require("fs");
const path = require("path");

// 读取源数据
const sourceData = JSON.parse(
  fs.readFileSync(path.join(__dirname, "../data/ai-tools-461.json"), "utf-8")
);

// 读取现有工具数据
const existingTools = JSON.parse(
  fs.readFileSync(path.join(__dirname, "../data/tools.json"), "utf-8")
);

// 分类映射：英文分类 → 中文分类
const CATEGORY_MAP = {
  "agent-frameworks": "agent",
  "memory-knowledge": "agent",
  "tool-integration": "agent",
  "observability-evaluation": "agent",
  "enterprise-agent-platforms": "agent",
  "voice-agents": "audio",
  "no-code-agent-builders": "productivity",
  "coding-agents": "code",
  "agent-protocols": "agent",
  "browser-web-agents": "agent",
  "sandboxes-execution": "agent",
};

// 分类中文标签
const CATEGORY_TAGS = {
  "agent-frameworks": ["AI Agent", "框架", "开源"],
  "memory-knowledge": ["RAG", "知识库", "记忆"],
  "tool-integration": ["工具集成", "API", "自动化"],
  "observability-evaluation": ["监控", "评估", "可观测"],
  "enterprise-agent-platforms": ["企业级", "Agent平台", "商用"],
  "voice-agents": ["语音AI", "TTS", "语音助手"],
  "no-code-agent-builders": ["无代码", "可视化", "工作流"],
  "coding-agents": ["AI编程", "代码助手", "开发者工具"],
  "agent-protocols": ["协议", "MCP", "标准"],
  "browser-web-agents": ["浏览器自动化", "网页Agent", "爬虫"],
  "sandboxes-execution": ["沙箱", "执行环境", "安全"],
};

/**
 * 基于 stars 数量计算功能分（1-10）
 * stars 越高，功能越完善
 */
function calcFunctionality(stars, score) {
  // 基础分：基于 stars 对数缩放
  const base = Math.min(10, 4 + Math.log10(Math.max(stars, 100)) * 1.2);
  // 加上数据集的 score（0-1）作为调整
  const adjusted = base * 0.7 + (score || 0.5) * 10 * 0.3;
  return Math.round(Math.min(10, Math.max(3, adjusted)) * 10) / 10;
}

/**
 * 基于分类计算用户体验分
 * no-code 工具 UX 好，framework UX 差
 */
function calcUX(categories) {
  if (categories.includes("no-code-agent-builders")) return 8.0;
  if (categories.includes("coding-agents")) return 7.5;
  if (categories.includes("voice-agents")) return 7.0;
  if (categories.includes("browser-web-agents")) return 6.5;
  if (categories.includes("enterprise-agent-platforms")) return 6.5;
  // 纯框架类，需要技术能力，UX 较低
  return 5.5 + Math.random() * 1.5;
}

/**
 * 价格分：都是免费开源，给高分
 */
function calcPricing(pricing) {
  if (pricing === "open-source") return 9.5;
  if (pricing === "free") return 9.0;
  return 7.0;
}

/**
 * 集成分：基于是否有 tool-integration 分类和 stars
 */
function calcIntegration(categories, stars) {
  const base = categories.includes("tool-integration") ? 8.0 : 6.0;
  const bonus = Math.min(2, Math.log10(Math.max(stars, 100)) * 0.3);
  return Math.round(Math.min(10, base + bonus) * 10) / 10;
}

/**
 * 支持分：基于更新频率（releases_6m 和 last_commit）
 */
function calcSupport(releases6m, lastCommit) {
  // 发布频率分
  const releaseScore = Math.min(3, (releases6m || 0) * 0.5);
  // 最近更新分：越新越好
  const lastDate = new Date(lastCommit || "2024-01-01");
  const now = new Date();
  const monthsSince = (now - lastDate) / (1000 * 60 * 60 * 24 * 30);
  const recencyScore = Math.max(1, 5 - monthsSince * 0.5);
  return Math.round(Math.min(10, 2 + releaseScore + recencyScore) * 10) / 10;
}

/**
 * 伦理分：开源工具伦理分高
 */
function calcEthics(pricing, categories) {
  let base = pricing === "open-source" ? 8.5 : 8.0;
  if (categories.includes("sandboxes-execution")) base += 0.5;
  if (categories.includes("observability-evaluation")) base += 0.3;
  return Math.round(Math.min(10, base) * 10) / 10;
}

/**
 * 生成优缺点
 */
function generateProsCons(tool) {
  const pros = [];
  const cons = [];

  // 通用优点
  if (tool.pricing === "open-source") {
    pros.push("完全开源免费，可自托管，数据自主可控");
  } else {
    pros.push("免费使用，社区活跃");
  }

  if (tool.stars > 50000) {
    pros.push("GitHub 高星项目，社区生态成熟，文档完善");
  } else if (tool.stars > 10000) {
    pros.push("社区活跃，持续更新迭代");
  }

  if (tool.categories.includes("tool-integration")) {
    pros.push("支持丰富的工具集成和 API 连接");
  }

  if (tool.categories.includes("no-code-agent-builders")) {
    pros.push("可视化操作，无需编程即可搭建工作流");
  }

  if (tool.categories.includes("coding-agents")) {
    pros.push("深度集成开发环境，提升编码效率");
  }

  if (tool.categories.includes("memory-knowledge")) {
    pros.push("支持 RAG 和知识库，可接入私有数据");
  }

  // 通用缺点
  if (tool.categories.includes("agent-frameworks") && !tool.categories.includes("no-code-agent-builders")) {
    cons.push("需要一定技术能力，学习曲线较陡");
  }

  if (tool.pricing === "open-source") {
    cons.push("自托管需要服务器资源和运维能力");
  }

  if (tool.stars < 5000) {
    cons.push("相对较新，社区生态仍在建设中");
  }

  if (tool.categories.includes("enterprise-agent-platforms")) {
    cons.push("企业级功能复杂，小型团队可能用不上");
  }

  // 确保至少 3 个优点和 2 个缺点
  while (pros.length < 3) {
    pros.push("基于开源社区驱动，功能迭代快速");
  }
  while (cons.length < 2) {
    cons.push("部分高级功能需要额外配置");
  }

  return {
    pros: pros.slice(0, 4),
    cons: cons.slice(0, 3),
  };
}

/**
 * 生成定价方案
 */
function generatePricing(tool) {
  if (tool.pricing === "open-source") {
    return [
      {
        name: "自托管免费版",
        price: "$0",
        description: "完全开源，自行部署，无使用限制",
        recommended: true,
      },
      {
        name: "云服务版",
        price: "按需付费",
        description: "官方托管服务，免运维（如有）",
        recommended: false,
      },
    ];
  }
  return [
    {
      name: "免费版",
      price: "$0/月",
      description: "基础功能，社区支持",
      recommended: true,
    },
    {
      name: "付费版",
      price: "详见官网",
      description: "高级功能，专业支持",
      recommended: false,
    },
  ];
}

/**
 * 从 GitHub URL 提取厂商名
 */
function extractVendor(githubUrl) {
  try {
    const parts = githubUrl.replace("https://github.com/", "").split("/");
    return parts[0] || "Open Source";
  } catch {
    return "Open Source";
  }
}

/**
 * 转换单个工具
 */
function convertTool(source) {
  const scores = {
    functionality: calcFunctionality(source.stars, source.score),
    ux: calcUX(source.categories),
    pricing: calcPricing(source.pricing),
    integration: calcIntegration(source.categories, source.stars),
    support: calcSupport(source.releases_6m, source.last_commit),
    ethics: calcEthics(source.pricing, source.categories),
  };

  const { pros, cons } = generateProsCons(source);
  const pricing = generatePricing(source);
  const vendor = extractVendor(source.github);

  // 主分类：取第一个映射的分类
  const mainCategory = CATEGORY_MAP[source.categories[0]] || "agent";

  // 标签：所有分类的中文标签合并
  const tags = [...new Set(source.categories.flatMap((c) => CATEGORY_TAGS[c] || [c]))];

  // 最后更新日期
  const lastUpdated = source.last_commit
    ? source.last_commit.split("T")[0]
    : "2026-01-01";

  return {
    id: source.id,
    slug: source.id,
    name: source.name,
    category: mainCategory,
    vendor: vendor,
    description: source.tagline || `${source.name} - 开源AI工具`,
    scores: scores,
    pros: pros,
    cons: cons,
    pricing: pricing,
    tags: tags.slice(0, 5),
    hasFreeTier: true,
    officialUrl: source.website || source.github,
    lastUpdated: lastUpdated,
  };
}

// 执行转换
console.log("开始转换 461 个开源AI工具...");

const convertedTools = sourceData.map(convertTool);

// 去重：基于 slug
const seenSlugs = new Set();
const uniqueConverted = convertedTools.filter((tool) => {
  if (seenSlugs.has(tool.slug)) return false;
  seenSlugs.add(tool.slug);
  return true;
});

// 与现有工具合并（现有工具优先，避免覆盖）
const existingSlugs = new Set(existingTools.map((t) => t.slug));
const newTools = uniqueConverted.filter((t) => !existingSlugs.has(t.slug));

const mergedTools = [...existingTools, ...newTools];

// 保存合并后的数据
fs.writeFileSync(
  path.join(__dirname, "../data/tools.json"),
  JSON.stringify(mergedTools, null, 2),
  "utf-8"
);

// 统计
console.log(`\n=== 转换完成 ===`);
console.log(`源数据: ${sourceData.length} 个`);
console.log(`去重后: ${uniqueConverted.length} 个`);
console.log(`新增工具: ${newTools.length} 个`);
console.log(`现有工具: ${existingTools.length} 个`);
console.log(`合并后总计: ${mergedTools.length} 个`);

// 分类统计
const catStats = {};
mergedTools.forEach((t) => {
  catStats[t.category] = (catStats[t.category] || 0) + 1;
});
console.log(`\n=== 分类分布 ===`);
Object.entries(catStats)
  .sort((a, b) => b[1] - a[1])
  .forEach(([cat, count]) => console.log(`${count} - ${cat}`));

// 评分分布
const gradeStats = { S: 0, A: 0, B: 0, C: 0, D: 0, F: 0 };
mergedTools.forEach((t) => {
  const total =
    t.scores.functionality * 0.25 +
    t.scores.ux * 0.2 +
    t.scores.pricing * 0.2 +
    t.scores.integration * 0.15 +
    t.scores.support * 0.1 +
    t.scores.ethics * 0.1;
  if (total >= 9) gradeStats.S++;
  else if (total >= 8) gradeStats.A++;
  else if (total >= 7) gradeStats.B++;
  else if (total >= 6) gradeStats.C++;
  else if (total >= 5) gradeStats.D++;
  else gradeStats.F++;
});
console.log(`\n=== 评分等级分布 ===`);
Object.entries(gradeStats).forEach(([grade, count]) => console.log(`${grade}: ${count}`));

console.log(`\n✅ 数据已保存到 data/tools.json`);
