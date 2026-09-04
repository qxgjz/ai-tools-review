/**
 * 为每篇博客文章生成FAQ（常见问题）
 * 基于文章标题、分类和内容生成相关的常见问题
 */

const fs = require("fs");
const path = require("path");

const postsPath = path.join(__dirname, "..", "data", "posts.json");
const posts = JSON.parse(fs.readFileSync(postsPath, "utf-8"));

// 通用FAQ模板（基于分类）
const categoryFAQs = {
  "AI Chat": [
    { q: "What is the best AI chatbot in 2026?", a: "The best AI chatbot depends on your needs. GPT-4o excels in general conversation and reasoning, Claude 3.5 Sonnet offers superior long context handling, and Gemini Advanced provides strong multimodal capabilities." },
    { q: "Are AI chatbots free to use?", a: "Most AI chatbots offer free tiers with limited usage. ChatGPT free uses GPT-3.5, Claude free offers limited messages daily, and Gemini Advanced requires a subscription for full features. Paid plans typically range from $15-30/month." },
    { q: "Can AI chatbots understand and generate multiple languages?", a: "Yes, modern AI chatbots like GPT-4o, Claude, and Gemini support dozens of languages including English, Chinese, Spanish, French, German, Japanese, and many more. Performance varies by language, with English typically being the most polished." },
  ],
  "AI Writing": [
    { q: "What is the best AI writing tool for content creators?", a: "The best AI writing tool depends on your workflow. Jasper excels in marketing copy, Sudowrite is ideal for fiction writers, and Writesonic offers a balance of quality and affordability. For SEO-focused content, consider Surfer SEO or Frase." },
    { q: "Can AI writing tools produce plagiarism-free content?", a: "AI writing tools generate original content based on patterns learned from training data. While the output is typically unique, it's recommended to run it through plagiarism checkers like Copyscape or Grammarly. Always review and edit AI-generated content to ensure accuracy and your unique voice." },
    { q: "Do AI writing tools help with SEO?", a: "Yes, many AI writing tools include SEO features. Surfer SEO and Frase analyze top-ranking pages and provide content optimization recommendations. Jasper and Writesonic offer SEO mode with keyword optimization. However, AI should assist, not replace, your SEO strategy and human judgment." },
  ],
  "AI Image": [
    { q: "What is the best AI image generator in 2026?", a: "The best AI image generator depends on your needs. Midjourney v6 offers the most artistic and photorealistic results, DALL-E 3 integrates seamlessly with ChatGPT, Stable Diffusion provides full control and open-source flexibility, and Ideogram excels at text rendering in images." },
    { q: "Are AI-generated images copyright-free?", a: "The copyright status of AI-generated images is complex and varies by jurisdiction. In the US, the Copyright Office has ruled that purely AI-generated works cannot be copyrighted, but works with significant human creative input may be eligible. Always review the tool's terms of service and use licensed models for commercial work." },
    { q: "Can AI image generators create images with text?", a: "Yes, modern AI image generators can render text, though quality varies. Ideogram is specifically designed for text rendering and excels at logos and posters. Midjourney v6 and DALL-E 3 also improved text capabilities. For precise text, it's still best to add it manually in Photoshop or Canva after generation." },
  ],
  "AI Coding": [
    { q: "What is the best AI coding assistant in 2026?", a: "The best AI coding assistant depends on your workflow. GitHub Copilot offers seamless IDE integration and excellent code completion, Cursor provides a full AI-native editor experience, Claude 3.5 Sonnet excels at large codebase understanding and refactoring, and Codeium offers a strong free tier." },
    { q: "Can AI coding assistants write production-ready code?", a: "AI coding assistants can generate high-quality code snippets and even complete functions, but they should not be trusted blindly for production code. Always review AI-generated code for security vulnerabilities, edge cases, performance issues, and adherence to your codebase standards. AI is a tool to augment, not replace, skilled developers." },
    { q: "Are AI coding assistants free?", a: "Many AI coding assistants offer free tiers. GitHub Copilot has a free tier for students, teachers, and maintainers of popular open-source projects. Codeium offers a generous free tier for individuals. Cursor has a free tier with limited usage. Paid plans typically range from $10-20/month for individuals." },
  ],
  "AI Video": [
    { q: "What is the best AI video generator in 2026?", a: "The best AI video generator depends on your needs. Sora by OpenAI offers the most realistic and creative text-to-video generation, Runway ML provides professional-grade editing tools and Gen-3 model, Pika Labs excels at stylized and animated content, and Synthesia is ideal for AI avatar-based corporate videos." },
    { q: "Can AI video generators create videos from text?", a: "Yes, modern AI video generators can create videos from text prompts. Sora, Runway Gen-3, and Pika 2.0 can generate 5-15 second clips from text descriptions. For longer videos, you'll need to generate multiple clips and edit them together. Quality varies, with photorealistic human motion still being challenging." },
    { q: "Are AI video generators expensive?", a: "AI video generators are typically more expensive than image generators due to higher computational costs. Runway ML plans start at $12/month for basic usage, Pika Labs offers a free tier with watermarks and paid plans from $10/month, and Synthesia starts at $22/month. Sora access is currently limited and pricing is being rolled out." },
  ],
  "AI Audio": [
    { q: "What is the best AI voice generator in 2026?", a: "The best AI voice generator depends on your needs. ElevenLabs offers the most natural and expressive voices with multilingual support, Murf AI is ideal for corporate and educational content with a wide voice library, Play.ht provides excellent voice cloning and commercial licensing, and Descript offers integrated podcast editing with AI voice overdub." },
    { q: "Can AI voice generators clone my voice?", a: "Yes, many AI voice generators offer voice cloning. ElevenLabs allows cloning with just 1 minute of audio, Play.ht requires more samples for higher quality, and Descript's Overdub feature creates a clone of your voice for editing. Always ensure you have the right to clone a voice and use it ethically, especially for commercial purposes." },
    { q: "Are AI-generated voices allowed for commercial use?", a: "Most AI voice generators offer commercial licenses on paid plans. ElevenLabs, Murf AI, and Play.ht all include commercial usage rights on their paid tiers. However, always review the specific terms of service, as some may have restrictions on certain use cases like audiobooks or advertising. Free tiers typically don't include commercial rights." },
  ],
  "AI Productivity": [
    { q: "What is the best AI productivity tool in 2026?", a: "The best AI productivity tool depends on your workflow. Notion AI integrates seamlessly with your notes and databases, Microsoft Copilot works across the entire Microsoft 365 suite, Google Gemini is built into Google Workspace, and Raycast AI offers powerful command-line productivity for Mac users." },
    { q: "Can AI tools really save time at work?", a: "Yes, AI productivity tools can save significant time when used effectively. Common use cases include summarizing long documents, drafting emails, organizing notes, automating repetitive tasks, and generating first drafts of reports. Most users report saving 1-3 hours per week, though results depend on how well you integrate AI into your specific workflow." },
    { q: "Are AI productivity tools secure for confidential work?", a: "Security varies by provider. Enterprise plans from Microsoft, Google, and Notion typically offer better data protection and may not use your data for model training. For highly confidential work, look for tools with SOC 2 compliance, data encryption, and clear privacy policies. Always check whether the provider uses your inputs for training their models." },
  ],
  "Comparison": [
    { q: "How do I choose between two AI tools?", a: "Start by identifying your primary use case and must-have features. Then compare factors like output quality, pricing and value, ease of use, integration with your existing tools, customer support, and data privacy. Our detailed reviews provide side-by-side comparisons and recommendations for different user profiles." },
    { q: "Is it worth paying for multiple AI tools?", a: "It depends on your workflow. Many people find that one general-purpose AI tool like ChatGPT or Claude covers most needs. However, specialized tools like Midjourney for images, ElevenLabs for voice, or GitHub Copilot for coding can be worth the investment if you use them regularly. Start with one, then add specialized tools as you identify gaps." },
    { q: "Can I switch AI tools without losing my work?", a: "Most AI tools allow exporting your data, though the process varies. ChatGPT lets you export all conversations, Notion supports full workspace export, and many coding tools integrate with Git. For generated content like images or videos, you can typically download your creations. Some tools may have proprietary formats, so check export options before committing." },
  ],
};

// 为每篇文章生成FAQ
function generateFAQ(post) {
  const category = post.category || "AI Chat";
  const baseFAQs = categoryFAQs[category] || categoryFAQs["AI Chat"];

  // 基于文章标题生成一个特定问题
  const toolName = post.title.split(" ")[0].replace(/[^a-zA-Z0-9]/g, "");
  const specificFAQ = {
    q: `Is ${toolName} worth the cost in 2026?`,
    a: `${toolName} offers strong value for users who need its specific capabilities. The pricing is competitive compared to alternatives, and the quality of output justifies the cost for regular users. However, if you only need basic features occasionally, the free tier or a lower-cost alternative may be sufficient. Consider your usage frequency and specific needs before subscribing.`,
  };

  // 组合：1个特定问题 + 2-3个分类通用问题
  const faqs = [specificFAQ, ...baseFAQs.slice(0, 3)];
  return faqs;
}

// 主函数
function main() {
  let updatedCount = 0;

  for (const post of posts) {
    if (!post.faq || post.faq.length === 0) {
      post.faq = generateFAQ(post);
      updatedCount++;
    }
  }

  // 保存更新后的数据
  fs.writeFileSync(postsPath, JSON.stringify(posts, null, 2), "utf-8");

  console.log(`✅ 已为 ${updatedCount} 篇文章生成FAQ`);
  console.log(`📊 总文章数: ${posts.length}`);
  console.log(`📝 每篇文章FAQ数: ${posts[0].faq.length}`);
  console.log(`\n示例FAQ（第一篇文章）:`);
  posts[0].faq.forEach((faq, i) => {
    console.log(`  Q${i + 1}: ${faq.q}`);
    console.log(`  A${i + 1}: ${faq.a.substring(0, 80)}...`);
  });
}

main();
