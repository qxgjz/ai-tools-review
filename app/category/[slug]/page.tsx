import { notFound } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, MessageSquare, PenTool, Image as ImageIcon, Code, Video, Music, Briefcase, Search as SearchIcon, Layers, Palette, Bot, CheckCircle, HelpCircle } from "lucide-react";
import type { LucideIcon } from "lucide-react";
import toolsData from "@/data/tools.json";
import postsData from "@/data/posts.json";
import type { Tool } from "@/types";
import { calculateScoreResult } from "@/lib/scoring";
import { ToolList } from "@/components/tools/ToolList";
import { CategoryToolsClient } from "@/components/tools/CategoryToolsClient";
import { Breadcrumb } from "@/components/ui/Breadcrumb";

// 分类详细内容（用于SEO主题集群）
const CATEGORY_CONTENT: Record<string, {
  intro: string;
  buyingGuide: string[];
  faqs: { q: string; a: string }[];
}> = {
  chat: {
    intro: "AI对话助手是目前应用最广泛的AI工具类型，能够通过自然语言交互完成问答、写作、分析、编程等多种任务。2026年，AI对话工具已经从简单的聊天机器人进化为具备推理、多模态理解、工具调用能力的智能助手。主流产品包括ChatGPT、Claude、Gemini、Perplexity等，各有特色：ChatGPT在生态和插件方面领先，Claude在长文本和写作方面表现优异，Gemini深度整合Google生态，Perplexity则以实时搜索和引用见长。选择AI对话工具时，需要考虑你的主要用途（日常问答/专业写作/编程辅助/研究搜索）、预算、隐私需求以及是否需要特定功能（如代码解释器、文件上传、语音对话）。",
    buyingGuide: [
      "明确主要用途：日常问答选ChatGPT免费版即可，专业写作选Claude，研究搜索选Perplexity，编程选ChatGPT或Cursor",
      "评估上下文需求：处理长文档（50页以上PDF）优先选Claude（200K上下文）或Gemini（1M上下文）",
      "考虑多模态需求：需要图片理解、语音对话、视频分析选ChatGPT Plus或Gemini Advanced",
      "隐私和数据安全：企业用户或处理敏感数据优先考虑有企业版和数据不用于训练承诺的产品",
      "预算考量：个人用户$20/月可获得大部分高级功能，企业用户$25-30/人/月可获得管理功能和安全保障"
    ],
    faqs: [
      { q: "AI对话工具能完全替代搜索引擎吗？", a: "不能完全替代。AI对话工具擅长综合回答和解释，但可能产生幻觉（编造信息），且知识有截止日期。对于需要最新信息、精确事实或多源对比的查询，仍需结合搜索引擎使用。Perplexity等结合了搜索的AI工具是更好的折中方案。" },
      { q: "免费版和付费版的主要区别是什么？", a: "付费版（通常$20/月）的主要优势包括：更强大的模型（GPT-4o/Claude 3.5 Opus等）、更高的使用限额、更快的响应速度、高级功能（代码解释器、文件上传、DALL-E图像生成、语音对话）、优先访问新功能。免费版适合轻度使用和体验，重度用户或专业人士建议升级付费版。" }
    ]
  },
  code: {
    intro: "AI编程工具正在革命性地改变软件开发方式，从代码补全到整个功能的自动生成，AI已经成为开发者的得力助手。2026年，AI编程工具主要分为三类：代码补全工具（如GitHub Copilot、Tabnine）在IDE中实时提供代码建议；AI原生IDE（如Cursor、Windsurf）将AI深度整合到开发环境中，支持代码生成、重构、调试、终端操作；云端开发平台（如Replit、GitHub Codespaces）提供零配置的云端开发环境，配合AI助手实现从想法到部署的全流程。选择AI编程工具时，需要考虑你的编程语言、IDE偏好、项目规模、隐私需求以及预算。",
    buyingGuide: [
      "选择合适的类型：已有IDE习惯选GitHub Copilot插件，想要AI原生体验选Cursor，快速原型选Replit",
      "语言和框架支持：确保工具支持你常用的语言（Python/JavaScript/TypeScript/Go/Rust等）和框架",
      "上下文理解能力：大型项目需要能理解整个代码库的工具（Cursor的Codebase Indexing、Copilot的Workspace Intelligence）",
      "隐私和合规：企业代码或开源项目贡献者需确认代码不会被用于训练，Tabnine和Copilot Business有相应保障",
      "预算：个人开发者$10-20/月，企业团队$19-39/人/月，免费试用后再决定"
    ],
    faqs: [
      { q: "AI编程工具会取代程序员吗？", a: "不会。AI编程工具是增强开发者生产力的助手，而非替代品。AI擅长生成模板代码、补全重复模式、解释陌生代码、生成测试用例，但仍需要人类开发者进行架构设计、需求理解、复杂逻辑实现、代码审查和质量把控。会用AI工具的开发者会取代不会用AI工具的开发者，但AI本身不会取代程序员。" },
      { q: "GitHub Copilot和Cursor哪个更好？", a: "取决于你的需求。GitHub Copilot是IDE插件，支持VS Code、JetBrains等主流IDE，代码补全质量高，适合已有IDE习惯的开发者。Cursor是AI原生IDE，基于VS Code但深度整合AI，支持代码库级理解、AI重构、多文件编辑、终端AI操作，适合愿意尝试新开发体验的开发者。两者可以同时使用：Cursor做主力开发，Copilot做额外补全。" }
    ]
  },
  image: {
    intro: "AI图像生成工具已经从实验性技术发展为设计师、营销人员和创作者的日常工具。2026年，AI图像工具在图像质量、文字渲染、一致性控制、编辑能力等方面都有了巨大进步。主流产品包括：Midjourney以艺术感和美学著称，适合创作高质量艺术图像；DALL-E 3深度整合ChatGPT，擅长根据详细描述生成精准图像；Stable Diffusion是开源模型，可本地部署和自定义训练，适合技术用户和需要隐私的场景；Leonardo AI专注于游戏资产和概念设计；Firefly是Adobe的AI工具，与Photoshop等创意软件深度整合。选择AI图像工具时，需要考虑你的用途（艺术创作/产品图/营销素材/游戏资产）、对图像一致性的要求、是否需要编辑能力、预算以及技术水平。",
    buyingGuide: [
      "明确用途：艺术创作选Midjourney，营销素材选DALL-E 3或Firefly，游戏资产选Leonardo AI，技术用户选Stable Diffusion",
      "图像质量和风格：Midjourney美学最佳，DALL-E 3文字理解最准，Stable Diffusion通过模型定制可实现各种风格",
      "编辑和修改能力：需要局部重绘、扩展、背景移除选Firefly或Leonardo AI，Midjourney编辑能力较弱",
      "一致性需求：产品图或角色系列需要高一致性选DALL-E 3（ChatGPT记忆）或Stable Diffusion（LoRA训练）",
      "预算和技术：$10-30/月可获得大部分工具，Stable Diffusion免费但需要GPU和技术能力"
    ],
    faqs: [
      { q: "AI生成的图片有版权吗？可以商用吗？", a: "AI生成图片的版权问题在不同国家有不同规定。美国版权局目前不授予纯AI生成作品版权，但人类对AI输出进行了实质性修改和创作的部分可能受保护。商用方面：Midjourney付费版允许商用，DALL-E 3允许商用，Stable Diffusion基于开源许可证通常允许商用，Firefly付费版允许商用。但建议：重要商业用途咨询法律意见，对AI输出进行实质性修改，保留创作过程记录，避免生成与现有受保护作品高度相似的内容。" },
      { q: "Midjourney和DALL-E 3哪个更适合新手？", a: "DALL-E 3更适合新手。DALL-E 3通过ChatGPT界面使用，自然语言理解能力强，能根据详细描述生成精准图像，不需要学习复杂的参数和提示词技巧。Midjourney通过Discord使用，需要学习参数（--ar、--v、--style等）和提示词技巧，上手门槛较高，但图像质量和艺术感更好。建议：新手从DALL-E 3开始，有一定经验后再尝试Midjourney以获得更高质量的艺术图像。" }
    ]
  },
  writing: {
    intro: "AI写作工具正在改变内容创作的方式，从博客文章到营销文案，从邮件到报告，AI已经成为写作者的得力助手。2026年，AI写作工具主要分为两类：通用AI助手（ChatGPT、Claude、Gemini）具备强大的写作能力，适合各种写作场景；专业AI写作工具（Jasper、Copy.ai、Writesonic）专为营销和内容创作设计，提供模板、品牌声音、SEO优化、团队协作等功能。选择AI写作工具时，需要考虑你的写作类型（博客/营销文案/社交媒体/技术文档）、是否需要SEO优化、团队协作需求、品牌声音一致性、预算以及对AI味的控制能力。",
    buyingGuide: [
      "明确写作类型：通用写作选ChatGPT或Claude，营销文案选Jasper，社交媒体选Copy.ai，长文博客选Claude",
      "SEO优化需求：需要关键词优化、内容评分、SEO建议选Jasper或Writesonic（内置SEO功能）",
      "品牌声音一致性：需要保持品牌语调选Jasper（Brand Voice）或Copy.ai（Brand Profile）",
      "团队协作：多人协作选Jasper或Copy.ai（团队工作区、审批流程、共享模板）",
      "去AI味：通用AI助手输出更自然，专业工具模板化输出可能AI味较重，需人工编辑润色"
    ],
    faqs: [
      { q: "AI写作工具生成的内容会被Google惩罚吗？", a: "Google明确表示不惩罚AI内容本身，而是惩罚低质量内容——无论是否由AI生成。Google的Helpful Content Update针对的是对用户没有帮助、为搜索引擎而写的内容。高质量的AI内容（有原创见解、经过人工编辑、提供真实价值、有EEAT信号）可以获得好排名。建议：用AI生成初稿但必须人工编辑，添加原创见解和个人经验，确保内容对读者有实质帮助，建立作者署名和专业背景，避免批量生成低质量内容。" },
      { q: "专业AI写作工具（Jasper等）比通用AI（ChatGPT）好在哪里？", a: "专业AI写作工具的优势在于：营销模板（博客大纲、Facebook广告、邮件序列等开箱即用）、品牌声音（学习并保持品牌语调）、SEO集成（关键词优化、内容评分、Surfer SEO集成）、团队协作（共享工作区、审批流程、内容日历）、多语言支持、 plagiarism检查。但通用AI（ChatGPT/Claude）的优势是：写作质量更高更自然，模型更强大，灵活性更高，价格更低。建议：营销团队和内容机构选专业工具，个人写作者和通用需求选ChatGPT/Claude。" }
    ]
  },
  video: {
    intro: "AI视频生成工具是2024-2026年发展最快的AI领域之一，从文本到视频的生成质量有了惊人的进步。2026年，AI视频工具主要分为：文生视频模型（Runway Gen-3、Sora、Pika、Kling）根据文本描述生成短视频；AI视频编辑工具（Descript、CapCut AI）提供AI辅助的剪辑、字幕、背景移除；数字人工具（Synthesia、HeyGen）生成AI数字人讲解视频。选择AI视频工具时，需要考虑你的用途（短视频创作/营销视频/培训视频/影视特效）、视频长度、质量要求、是否需要数字人、编辑能力、预算以及技术水平。",
    buyingGuide: [
      "明确用途：创意短视频选Runway或Pika，电影级质量选Sora，数字人讲解选Synthesia或HeyGen，AI剪辑选Descript",
      "视频长度：目前AI生成视频多为5-15秒，需要长视频选支持扩展的工具或拼接多个片段",
      "质量和真实感：Sora质量最高但访问受限，Runway Gen-3质量优秀且易获得，Kling在中文场景表现好",
      "数字人需求：培训、营销、讲解视频选Synthesia（模板多）或HeyGen（质量高、多语言）",
      "预算：$12-40/月可获得大部分工具，高质量生成消耗积分较快，需评估使用量"
    ],
    faqs: [
      { q: "AI生成的视频可以商用吗？", a: "大多数付费AI视频工具允许商用生成的视频，但有一些限制：不能生成违法或有害内容，不能冒充真实人物（数字人工具除外），不能生成与受保护作品高度相似的内容，部分工具对大规模商用或高流量使用有额外要求。建议：阅读各工具的服务条款，重要商业用途咨询法律意见，对AI输出进行实质性编辑，保留创作记录。数字人工具通常明确允许商用，但需确保不用于欺诈或冒充。" },
      { q: "AI视频生成会取代视频剪辑师吗？", a: "短期内不会完全取代。AI视频生成工具目前擅长生成短视频片段和辅助剪辑，但在叙事结构、情感表达、精细剪辑、色彩调色、声音设计等方面仍需人类专业人士。AI会改变视频制作流程：剪辑师从手动剪辑转向AI辅助+创意指导，效率大幅提升。会用AI工具的视频创作者会更有竞争力。对于简单的营销视频、社交媒体短视频、培训视频，AI工具已经可以独立完成大部分工作。" }
    ]
  },
  audio: {
    intro: "AI音频工具正在革新语音和音乐创作，从逼真的语音合成到原创歌曲生成，AI已经成为音频创作者的得力工具。2026年，AI音频工具主要分为：语音合成工具（ElevenLabs）生成逼真的人类语音，支持多语言、多角色、情感控制；音乐生成工具（Suno、Udio）根据文本描述生成包含人声的完整歌曲；会议转录工具（Otter.ai、Fireflies）实时转录会议并生成摘要和行动项；音频编辑工具（Descript）提供AI辅助的音频编辑、降噪、语音克隆。选择AI音频工具时，需要考虑你的用途（语音合成/音乐创作/会议转录/播客制作）、语音质量要求、多语言需求、商业使用权限、预算。",
    buyingGuide: [
      "明确用途：语音合成选ElevenLabs，AI音乐选Suno，会议转录选Otter.ai，播客制作选Descript",
      "语音质量：ElevenLabs语音最逼真，支持情感控制和多角色，适合 audiobook、视频配音、IVR",
      "音乐创作：Suno人声质量最佳，支持自定义歌词和风格，适合内容创作者和音乐人做demo",
      "会议效率：Otter.ai转录准确，支持实时字幕、摘要、行动项提取，适合远程团队",
      "商用权限：语音合成商用需付费版，音乐商用权限各工具不同，需仔细阅读条款"
    ],
    faqs: [
      { q: "AI语音合成可以用来克隆别人的声音吗？", a: "技术上可以，但伦理和法律上有严格限制。ElevenLabs等工具明确禁止未经授权克隆他人声音，要求用户只能克隆自己有权使用的声音，并提供了声音保护机制（个人可以注册自己的声音防止被克隆）。法律上，未经授权克隆他人声音可能侵犯肖像权、声音权，用于欺诈可能构成犯罪。建议：只克隆自己或获得明确授权的声音，明确标注AI生成内容，不用于误导或欺诈，关注各地区AI声音相关法规。" },
      { q: "AI生成的音乐可以用于视频和播客吗？", a: "可以，但需要注意商用权限。Suno等工具的付费版通常允许将生成的音乐用于视频、播客、游戏等内容，但有一些限制：不能将AI音乐作为纯音乐作品在流媒体平台发行（部分工具限制），不能用于NFT，高流量或大规模商用可能需要更高档位。建议：阅读工具的商用条款，在内容描述中注明AI生成，重要商业项目咨询法律意见，保留生成记录和付费凭证。对于需要纯背景音乐的场景，也可以考虑Epidemic Sound等版权音乐库。" }
    ]
  },
  productivity: {
    intro: "AI生产力工具正在改变我们的工作方式，从文档处理到会议管理，从邮件回复到任务规划，AI已经成为职场人士的得力助手。2026年，AI生产力工具主要分为：办公套件AI助手（Microsoft 365 Copilot、Google Duet AI）深度整合Word/Excel/PPT/Gmail等办公应用；笔记和知识管理AI（Notion AI、Obsidian插件）帮助整理、总结、检索信息；会议AI助手（Otter.ai、Fireflies、Fathom）实时转录、总结、提取行动项；邮件AI助手（Superhuman、Shortwave）帮助快速处理邮件。选择AI生产力工具时，需要考虑你使用的办公生态（Microsoft/Google/Notion）、主要痛点（文档/会议/邮件/笔记）、团队协作需求、隐私和安全要求、预算。",
    buyingGuide: [
      "选择办公生态：Microsoft 365用户选Copilot，Google Workspace用户选Duet AI，Notion用户选Notion AI",
      "明确主要痛点：文档处理选Copilot/Duet AI，会议管理选Otter.ai/Fathom，邮件处理选Superhuman",
      "团队协作：企业用户选有管理后台、SSO、审计日志的企业版，小团队选基础版即可",
      "隐私安全：处理敏感数据选有企业版、数据不用于训练、合规认证（SOC2/GDPR）的工具",
      "预算：$10-30/人/月可获得大部分工具，企业版价格更高但有安全保障"
    ],
    faqs: [
      { q: "Microsoft 365 Copilot值得买吗？", a: "取决于你的使用频率和角色。Copilot ($30/月+M365订阅) 适合：每天大量使用Office的职场人士（写文档、做PPT、处理邮件、开会），能显著提升效率；企业团队统一部署，协作效率提升明显。不值得买：轻度Office用户（每周只用几次），性价比不高；预算有限的个人用户，ChatGPT Plus ($20/月) 更灵活；非Microsoft生态用户。建议：先试用30天评估实际使用频率和效率提升，重度用户值得购买，轻度用户用ChatGPT等通用AI即可。" },
      { q: "AI会议转录工具的准确率如何？", a: "2026年主流AI会议转录工具（Otter.ai、Fireflies、Fathom）的英文转录准确率可达90-95%，中文准确率约80-90%，取决于口音、背景噪音、专业术语等因素。多人对话时说话人识别准确率约80-90%。摘要和行动项提取的质量取决于转录准确性和AI模型，主流工具表现良好但仍需人工核对。建议：重要会议人工核对转录和行动项，专业术语多的会议可能需要自定义词汇表，英文会议效果优于中文会议。" }
    ]
  },
  search: {
    intro: "AI搜索工具正在改变我们获取信息的方式，从传统的关键词搜索到自然语言问答，AI搜索提供了更直接、更高效的信息获取体验。2026年，AI搜索工具主要分为：AI搜索引擎（Perplexity、You.com）结合实时搜索和AI综合，提供带引用的答案；浏览器内置AI（Arc Search、Opera Aria）在浏览器中提供AI搜索和摘要；企业搜索（Glean、Cortex）搜索企业内部文档和知识。选择AI搜索工具时，需要考虑你的搜索类型（研究/日常/企业内部）、对引用和来源的需求、隐私要求、是否需要深度研究功能、预算。",
    buyingGuide: [
      "明确搜索类型：研究和深度问答选Perplexity，日常搜索选You.com或浏览器AI，企业内部搜索选Glean",
      "引用和来源：需要可验证的来源和引用选Perplexity（每个论断都有来源链接）",
      "深度研究：需要多步搜索、综合分析、长报告选Perplexity Pro Search或Deep Research模式",
      "隐私要求：不希望搜索数据被用于训练选有隐私模式的工具，企业用户选企业版",
      "预算：免费版可满足日常使用，$20/月Pro版可获得无限深度搜索和高级功能"
    ],
    faqs: [
      { q: "AI搜索会取代Google吗？", a: "短期内不会完全取代，但会显著分流。AI搜索（Perplexity等）在研究、问答、综合类查询上体验更好——直接给出答案和引用，省去点击多个链接的时间。但Google在本地搜索、购物、图片、视频、地图、最新新闻等方面仍有优势。2026年的趋势是：Google也在整合AI（AI Overview），AI搜索工具也在增加更多搜索功能。建议：研究和学习用AI搜索，日常和本地用Google，两者结合使用效率最高。" },
      { q: "AI搜索的答案可靠吗？会有幻觉吗？", a: "AI搜索的答案比纯聊天AI更可靠，因为它基于实时搜索结果并提供引用，但仍可能出现问题：引用的来源可能质量不高（博客、内容农场），可能断章取义或曲解来源，可能遗漏重要信息，综合多个来源时可能产生矛盾。建议：重要信息点击引用链接核实原文，交叉验证多个来源，对有争议的话题注意来源偏见，AI搜索作为研究起点而非最终答案。Perplexity等工具的Pro Search模式质量更高，但仍需验证。" }
    ]
  },
  design: {
    intro: "AI设计工具正在革新UI/UX设计和创意设计流程，从线框图到高保真原型，从图像编辑到设计系统，AI已经成为设计师的得力助手。2026年，AI设计工具主要分为：UI设计AI（Figma AI、Magician、Galileo AI）在设计工具中提供AI辅助的布局生成、组件设计、文案生成；图像编辑AI（Adobe Firefly、Canva AI、Photoshop Generative Fill）提供AI辅助的图像生成、编辑、背景移除、扩展；设计系统AI（Frontitude、Stitch）帮助管理和生成设计系统。选择AI设计工具时，需要考虑你的设计类型（UI/UX/平面/产品）、使用的设计工具（Figma/Adobe/Canva）、对设计质量的要求、团队协作需求、预算。",
    buyingGuide: [
      "明确设计类型：UI/UX设计选Figma AI，平面设计选Canva AI或Firefly，照片编辑选Photoshop Generative Fill",
      "设计工具生态：Figma用户选Figma AI或Magician插件，Adobe用户选Firefly，Canva用户选Canva AI",
      "设计质量：需要高质量UI设计选Figma AI（基于设计系统生成），需要创意图像选Firefly或Midjourney",
      "团队协作：设计团队选有团队工作区、共享设计系统、版本控制的工具",
      "预算：$10-30/月可获得大部分工具，Adobe Creative Cloud订阅包含Firefly"
    ],
    faqs: [
      { q: "AI设计工具会取代UI设计师吗？", a: "不会完全取代，但会改变设计师的工作方式。AI设计工具擅长：生成布局变体、创建重复组件、生成占位文案、快速原型、图像编辑辅助。但仍需要人类设计师进行：用户研究、设计策略、信息架构、交互细节、品牌一致性、设计系统维护、可访问性确保。AI会让设计师从重复劳动中解放出来，更专注于创意和策略。会用AI工具的设计师效率会大幅提升，不会用AI工具的设计师可能面临竞争压力。建议：设计师学习使用AI工具作为助手，而不是担心被取代。" },
      { q: "Figma AI和Adobe Firefly哪个更好？", a: "取决于你的设计场景。Figma AI专注于UI/UX设计，在Figma中提供AI辅助的布局生成、组件设计、设计系统应用，适合UI/UX设计师和产品团队。Adobe Firefly专注于图像生成和编辑，与Photoshop、Illustrator等创意软件深度整合，适合平面设计师、摄影师和创意专业人士。两者不是直接竞争关系，而是针对不同设计场景。很多设计师同时使用：Figma AI做UI设计，Firefly做图像素材。建议：UI/UX设计师选Figma AI，平面/创意设计师选Firefly，两者都需要的可以都用。" }
    ]
  },
  agent: {
    intro: "AI Agent框架是2025-2026年最热门的AI技术方向之一，能够让AI自主完成复杂任务，从网页浏览到代码编写，从数据分析到工作流自动化。AI Agent不同于传统的AI对话——它能够规划任务、调用工具、执行操作、迭代改进，最终完成多步骤的复杂目标。主流AI Agent框架包括：LangChain（最流行的开源框架）、LlamaIndex（专注于数据连接和RAG）、AutoGPT（自主AI代理）、CrewAI（多Agent协作）、Dify（可视化AI应用开发平台）、n8n（工作流自动化+AI节点）。选择AI Agent框架时，需要考虑你的技术水平、使用场景（自主代理/RAG/工作流/多Agent）、是否需要可视化界面、部署方式（云/本地/自托管）、编程语言偏好。",
    buyingGuide: [
      "技术水平：开发者选LangChain或LlamaIndex，非技术用户选Dify或n8n（可视化），想要自主代理选AutoGPT或CrewAI",
      "使用场景：RAG和数据连接选LlamaIndex，通用Agent开发选LangChain，工作流自动化选n8n，可视化AI应用选Dify",
      "多Agent协作：需要多个AI角色协作选CrewAI或AutoGen，适合复杂任务分解",
      "部署方式：云服务选Dify Cloud或LangChain Cloud，自托管选开源框架自行部署，本地运行选Ollama+开源框架",
      "学习资源：LangChain社区最大文档最全，Dify有中文社区和教程，n8n有丰富的模板库"
    ],
    faqs: [
      { q: "AI Agent和AI聊天机器人有什么区别？", a: "AI聊天机器人（ChatGPT等）是单轮或多轮对话，用户每次输入一个指令，AI给出一个回答，需要用户逐步引导。AI Agent是自主的——用户给出一个目标（如'帮我调研竞品并生成报告'），Agent会自主规划任务步骤、调用工具（搜索、浏览器、代码执行、文件操作）、执行操作、检查结果、迭代改进，最终完成整个目标。AI Agent的核心能力是：规划（分解任务）、工具调用（使用外部工具）、记忆（记住之前的操作和结果）、自主迭代（根据反馈调整策略）。简单说：聊天机器人是你问一句它答一句，Agent是你给一个目标它自己干完。" },
      { q: "非技术用户可以使用AI Agent吗？", a: "可以，但需要选择合适的工具。非技术用户建议：Dify（可视化拖拽搭建AI应用和Agent，有中文界面和教程）、n8n（工作流自动化工具，有AI节点，可视化连接）、ChatGPT插件/自定义GPT（通过自然语言配置简单的Agent）、Coze（字节跳动的AI Bot开发平台，可视化）。这些工具不需要写代码，通过可视化界面和自然语言配置即可创建AI Agent。但更复杂的Agent（多Agent协作、自定义工具、深度集成）仍需要技术能力。建议：非技术用户从Dify或n8n开始，有一定基础后再学习LangChain等开发框架。" }
    ]
  },
  "agent-framework": {
    intro: "AI Agent框架是构建自主AI系统的基础工具，提供任务规划、工具调用、记忆管理、多Agent协作等核心能力。2026年，AI Agent框架已经从实验性技术发展为生产级工具，被广泛应用于自动化工作流、客服机器人、数据分析、代码编写等场景。主流框架包括：LangChain（最流行的开源框架，生态丰富）、LlamaIndex（专注于数据连接和RAG）、CrewAI（多Agent协作）、AutoGen（微软的多Agent框架）、Dify（可视化AI应用开发平台）。选择AI Agent框架时，需要考虑你的技术水平、使用场景、是否需要可视化界面、部署方式以及编程语言偏好。",
    buyingGuide: [
      "评估技术水平：非技术用户优先选Dify或Coze等可视化平台，开发者可选LangChain或LlamaIndex",
      "明确使用场景：简单自动化选n8n+AI节点，复杂多Agent选CrewAI或AutoGen，RAG应用选LlamaIndex",
      "考虑部署方式：云服务优先选Dify或Coze，自托管选LangChain或CrewAI，企业级选AutoGen",
      "评估生态和社区：LangChain生态最丰富，教程和插件最多；CrewAI多Agent协作最成熟；Dify可视化最好",
      "成本考量：开源框架免费但需要自己部署和维护，云平台有免费额度但高级功能付费"
    ],
    faqs: [
      { q: "AI Agent框架和AI Agent平台有什么区别？", a: "AI Agent框架（如LangChain、CrewAI）是代码库，需要开发者编写代码来构建Agent，灵活性高但需要技术能力。AI Agent平台（如Dify、Coze）是可视化工具，通过拖拽和自然语言配置即可创建Agent，易用性高但灵活性有限。选择取决于你的技术水平和需求复杂度：简单场景用平台，复杂场景用框架。" },
      { q: "哪个AI Agent框架最适合初学者？", a: "初学者建议从Dify开始，它提供可视化界面、中文文档、丰富的模板，不需要写代码就能创建AI Agent和应用。有一定编程基础后，可以学习LangChain，它是最流行的框架，生态最丰富，教程最多。如果对多Agent协作感兴趣，可以学习CrewAI，它的概念简单，上手快。" }
    ]
  },
  "agent-runtime": {
    intro: "AI Agent运行时是执行和管理AI Agent的平台，提供Agent部署、监控、调度、扩展等能力。2026年，随着AI Agent从实验走向生产，Agent运行时成为关键基础设施。主流运行时包括：LangGraph（LangChain的Agent执行引擎，支持状态管理和复杂工作流）、AutoGen（微软的多Agent运行时）、CrewAI（内置运行时的多Agent框架）、Modal（Serverless AI运行时）、Banana（GPU云运行时）。选择AI Agent运行时时，需要考虑你的Agent框架、部署环境、性能需求、监控需求以及成本。",
    buyingGuide: [
      "匹配Agent框架：LangChain生态选LangGraph，多Agent选AutoGen或CrewAI，Serverless选Modal",
      "评估性能需求：高并发选Modal或Banana等GPU云，低延迟选自托管LangGraph",
      "考虑监控和可观测性：生产环境需要完善的日志、追踪、性能监控，AutoGen和LangGraph支持较好",
      "成本考量：Serverless按使用量付费适合波动负载，自托管适合稳定负载但需要运维能力",
      "社区和支持：选择活跃的社区和良好的文档，遇到问题能快速找到解决方案"
    ],
    faqs: [
      { q: "我需要单独的Agent运行时吗？", a: "取决于你的场景。如果只是实验或简单应用，框架内置的执行能力就够了。如果是生产环境，需要高可用、监控、扩展、调度等能力，就需要专门的Agent运行时。建议：先从框架开始，当Agent复杂度增加或需要生产部署时，再引入运行时。" },
      { q: "LangGraph和AutoGen哪个更好？", a: "各有优势。LangGraph是LangChain生态的一部分，擅长状态管理和复杂工作流，与LangChain工具和集成无缝配合，适合构建有明确流程的Agent。AutoGen是微软的多Agent框架，擅长多Agent对话和协作，支持人机交互，适合构建需要多个Agent协作的复杂系统。选择取决于你的技术栈和需求：LangChain用户选LangGraph，多Agent协作选AutoGen。" }
    ]
  },
  rag: {
    intro: "RAG（检索增强生成，Retrieval-Augmented Generation）是将外部知识库与大语言模型结合的技术，能够让AI基于你的私有数据回答问题，减少幻觉，提高准确性。2026年，RAG已经成为企业AI应用的核心技术，被广泛应用于客服机器人、知识库问答、文档摘要、法律合规等场景。主流RAG框架和工具包括：LlamaIndex（最流行的RAG框架）、LangChain（支持RAG的通用框架）、Dify（可视化RAG平台）、Haystack（企业级RAG框架）、Weaviate/Pinecone（向量数据库）。选择RAG工具时，需要考虑你的数据类型、技术水平、是否需要可视化、部署方式以及性能需求。",
    buyingGuide: [
      "评估数据类型：结构化数据选LangChain+SQL Agent，非结构化文档选LlamaIndex或Dify，多模态选Pinecone+CLIP",
      "技术水平：非技术用户选Dify（可视化配置），开发者选LlamaIndex或LangChain（灵活定制）",
      "性能需求：大规模数据选Pinecone或Weaviate（专用向量数据库），小规模选Chroma或FAISS（本地向量库）",
      "部署方式：云服务选Dify或Pinecone，自托管选LlamaIndex+Weaviate，企业级选Haystack",
      "成本考量：开源框架免费但需要自己维护，云平台有免费额度但大规模使用付费"
    ],
    faqs: [
      { q: "RAG和微调（Fine-tuning）有什么区别？", a: "RAG是在推理时检索外部知识，不需要修改模型，知识更新即时生效，成本低，适合频繁变化的知识。微调是在训练时将知识融入模型参数，需要训练数据和计算资源，知识更新需要重新训练，成本高，适合稳定的领域知识和风格学习。建议：大多数场景优先用RAG，当需要特定风格或领域深度理解时再考虑微调。" },
      { q: "RAG能完全解决AI幻觉问题吗？", a: "不能完全解决，但能大幅减少。RAG通过提供相关上下文，让模型基于真实数据回答，显著降低幻觉概率。但如果检索到的信息不准确、不完整，或者模型忽略了上下文，仍可能产生幻觉。最佳实践是：RAG+来源引用+人工审核，关键场景需要人工确认。" }
    ]
  },
  database: {
    intro: "AI数据库是专为AI应用设计的数据存储和检索系统，包括向量数据库、图数据库、时序数据库等，能够高效存储和检索AI模型需要的高维向量、复杂关系和实时数据。2026年，AI数据库已经成为AI基础设施的核心组件，被广泛应用于RAG、推荐系统、图像搜索、异常检测等场景。主流AI数据库包括：Pinecone（托管向量数据库）、Weaviate（开源向量数据库）、Chroma（轻量级向量数据库）、Milvus（分布式向量数据库）、Neo4j（图数据库）。选择AI数据库时，需要考虑你的数据规模、查询类型、性能需求、部署方式以及成本。",
    buyingGuide: [
      "数据规模：小规模（<100万向量）选Chroma或FAISS，中规模（100万-1亿）选Weaviate或Pinecone，大规模（>1亿）选Milvus",
      "查询类型：纯向量相似性搜索选Pinecone或Chroma，向量+过滤选Weaviate，复杂关系查询选Neo4j",
      "性能需求：低延迟高并发选Pinecone或Milvus，开发原型选Chroma，企业级高可用选Weaviate Enterprise",
      "部署方式：托管服务选Pinecone，自托管选Weaviate或Milvus，嵌入式选Chroma或FAISS",
      "成本考量：开发阶段用Chroma（免费），生产阶段根据规模选Weaviate（开源免费）或Pinecone（托管付费）"
    ],
    faqs: [
      { q: "向量数据库和传统数据库有什么区别？", a: "传统数据库（如MySQL、PostgreSQL）擅长存储结构化数据，支持精确匹配和复杂查询，但不擅长高维向量相似性搜索。向量数据库专门设计用于存储和检索高维向量（如文本、图像的embedding），支持近似最近邻（ANN）搜索，能够快速找到语义相似的数据。建议：AI应用中通常需要两者结合，传统数据库存储元数据，向量数据库存储embedding。" },
      { q: "我需要专门的向量数据库吗？", a: "取决于你的场景。如果只是简单的RAG原型，用pgvector（PostgreSQL扩展）或Chroma就够了。如果需要生产级的性能、扩展、高可用，或者数据量超过100万向量，就需要专门的向量数据库如Pinecone、Weaviate或Milvus。建议：先从简单方案开始，当性能成为瓶颈时再迁移到专业向量数据库。" }
    ]
  },
  memory: {
    intro: "AI记忆系统是让AI应用具备长期记忆和上下文管理能力的技术，能够存储和检索用户历史对话、偏好、知识，提供个性化和连贯的交互体验。2026年，随着AI助手和Agent的普及，记忆系统成为提升用户体验的关键组件。主流AI记忆工具和框架包括：LangChain Memory（LangChain的记忆模块）、Zep（开源AI记忆服务器）、Mem0（AI记忆层）、LangGraph Memory（状态管理）、Redis（缓存和短期记忆）。选择AI记忆系统时，需要考虑你的应用类型、记忆时长、隐私需求、部署方式以及与AI框架的兼容性。",
    buyingGuide: [
      "应用类型：对话机器人选Zep或Mem0（长期记忆），Agent选LangGraph Memory（状态管理），短期上下文选Redis",
      "记忆时长：短期记忆（会话内）选LangChain Memory或Redis，长期记忆（跨会话）选Zep或Mem0",
      "隐私需求：敏感数据选自托管Zep或Mem0，一般数据选云服务，需要符合GDPR/HIPAA选企业版",
      "部署方式：快速原型选LangChain Memory（内置），生产环境选Zep或Mem0（独立服务），Serverless选Redis Cloud",
      "框架兼容性：LangChain用户选LangChain Memory或Zep，多框架选Mem0，自定义选Redis+自己实现"
    ],
    faqs: [
      { q: "AI记忆系统和RAG有什么区别？", a: "RAG是检索外部知识库（如文档、网页），通常是静态的、与用户无关的知识。AI记忆系统是存储用户特定的历史交互、偏好、行为，通常是动态的、个性化的。两者可以结合使用：RAG提供通用知识，记忆系统提供个性化上下文。建议：对话型AI应用两者都需要，知识库问答只需要RAG。" },
      { q: "AI记忆会带来隐私问题吗？", a: "是的，AI记忆存储用户的个人信息、对话历史、偏好，可能涉及隐私和合规问题。最佳实践包括：明确告知用户记忆功能、提供记忆删除选项、敏感数据加密存储、符合GDPR/CCPA等法规、定期清理过期记忆。建议：在产品设计时就考虑隐私，提供用户控制记忆的能力。" }
    ]
  },
  observability: {
    intro: "AI可观测性是监控、追踪、分析AI应用性能和行为的技术，能够帮助开发者发现和解决AI应用中的问题，如延迟、错误、幻觉、成本超支等。2026年，随着AI应用从实验走向生产，可观测性成为确保AI应用可靠性和成本效益的关键工具。主流AI可观测性工具包括：LangSmith（LangChain的可观测性平台）、Weights & Biases（ML实验追踪）、Arize AI（AI可观测性）、Helicone（LLM可观测性）、Langfuse（开源LLM可观测性）。选择AI可观测性工具时，需要考虑你的AI框架、监控需求、部署方式、成本以及团队规模。",
    buyingGuide: [
      "AI框架：LangChain用户首选LangSmith（无缝集成），多框架选Langfuse或Arize，OpenAI专用选Helicone",
      "监控需求：实验追踪选Weights & Biases，生产监控选Arize或Langfuse，成本追踪选Helicone",
      "部署方式：快速开始选LangSmith或Helicone（云服务），自托管选Langfuse（开源），企业级选Arize",
      "团队规模：小团队选LangSmith或Helicone（简单易用），大团队选Arize或Weights & Biases（企业功能）",
      "成本考量：开发阶段用免费额度，生产阶段根据调用量选择付费计划，开源方案可自托管降低成本"
    ],
    faqs: [
      { q: "AI可观测性和传统APM有什么区别？", a: "传统APM（应用性能监控）关注系统指标如延迟、错误率、吞吐量，适合传统软件。AI可观测性除了系统指标，还关注AI特有的指标，如token使用量、模型成本、幻觉率、输出质量、提示词效果、检索相关性等。AI应用的不确定性更高，需要专门的工具来监控和调试。建议：AI应用需要两者结合，传统APM监控基础设施，AI可观测性监控AI行为。" },
      { q: "我什么时候需要AI可观测性？", a: "从第一天就应该开始。即使在开发阶段，可观测性工具能帮助你调试提示词、评估输出质量、追踪成本。当应用进入生产环境，可观测性成为必需，帮助你发现性能问题、成本异常、用户体验问题。建议：至少接入一个基础的可观测性工具（如LangSmith或Langfuse），从开发阶段开始收集数据。" }
    ]
  },
  "dev-tools": {
    intro: "AI开发工具是帮助开发者构建、测试、部署AI应用的工具集合，包括SDK、API、测试框架、部署工具等。2026年，AI开发工具生态已经非常成熟，覆盖从模型调用到应用部署的全流程。主流AI开发工具包括：OpenAI API（最流行的LLM API）、Anthropic API（Claude模型）、Hugging Face（模型库和部署平台）、Vercel AI SDK（Next.js AI应用开发）、LangChain（AI应用框架）、PromptLayer（提示词管理）。选择AI开发工具时，需要考虑你的技术栈、模型需求、部署环境、成本以及团队规模。",
    buyingGuide: [
      "技术栈：Next.js/React选Vercel AI SDK，Python选LangChain或LlamaIndex，全栈选Supabase+Edge Functions",
      "模型需求：通用LLM选OpenAI或Anthropic，开源模型选Hugging Face，多模型选Router（如LiteLLM）",
      "部署环境：Serverless选Vercel或Cloudflare Workers，容器化选Docker+Kubernetes，边缘部署选Cloudflare",
      "成本考量：开发阶段用免费额度，生产阶段根据调用量优化（缓存、批处理、小模型），开源模型可自托管降低成本",
      "团队协作：提示词管理选PromptLayer或LangSmith，实验追踪选Weights & Biases，代码协作选GitHub"
    ],
    faqs: [
      { q: "我应该用哪个LLM API？", a: "取决于你的需求。通用场景选OpenAI GPT-4o（生态最丰富，功能最全），长文本和写作选Anthropic Claude（上下文长，写作质量高），成本敏感选OpenAI GPT-3.5或开源模型，多模态选GPT-4o或Gemini。建议：先用一个主流API（如OpenAI）开发，当有特定需求时再引入其他模型，使用LiteLLM等路由工具统一接口。" },
      { q: "Vercel AI SDK和LangChain怎么选？", a: "Vercel AI SDK是轻量级的前端/全栈AI开发工具，专注于Next.js/React生态，提供流式响应、UI组件、模型路由，适合构建用户-facing的AI应用。LangChain是功能丰富的AI应用框架，支持复杂工作流、RAG、Agent、工具调用，适合构建复杂的后端AI应用。建议：前端交互多用Vercel AI SDK，复杂后端逻辑用LangChain，两者可以结合使用。" }
    ]
  }
};

const CATEGORIES: Record<string, { name: string; description: string; icon: LucideIcon; gradient: string }> = {
  chat: { name: "AI 对话助手", description: "智能对话、问答交互、多轮聊天", icon: MessageSquare, gradient: "from-blue-600 to-cyan-500" },
  writing: { name: "AI 写作工具", description: "文章撰写、文案创作、内容润色", icon: PenTool, gradient: "from-purple-600 to-pink-500" },
  image: { name: "AI 绘画设计", description: "图像生成、艺术创作、设计辅助", icon: ImageIcon, gradient: "from-orange-500 to-red-500" },
  code: { name: "AI 编程开发", description: "代码生成、程序开发、技术辅助", icon: Code, gradient: "from-emerald-600 to-teal-500" },
  video: { name: "AI 视频制作", description: "视频生成、剪辑制作、多媒体创作", icon: Video, gradient: "from-rose-500 to-orange-500" },
  audio: { name: "AI 音频音乐", description: "语音合成、音乐生成、音频处理", icon: Music, gradient: "from-violet-600 to-purple-500" },
  productivity: { name: "AI 效率办公", description: "文档处理、会议纪要、团队协作", icon: Briefcase, gradient: "from-indigo-600 to-blue-500" },
  search: { name: "AI 智能搜索", description: "智能搜索、信息检索、知识问答", icon: SearchIcon, gradient: "from-sky-600 to-blue-500" },
  agent: { name: "AI Agent 框架", description: "智能体开发、自动化工作流、自主AI系统", icon: Bot, gradient: "from-indigo-600 to-purple-600" },
  design: { name: "AI 设计工具", description: "UI设计、原型制作、创意设计辅助", icon: Palette, gradient: "from-pink-500 to-rose-500" },
  "agent-framework": { name: "AI Agent 框架", description: "多智能体编排、角色协作、自动化框架", icon: Bot, gradient: "from-indigo-600 to-blue-600" },
  "agent-runtime": { name: "AI Agent 运行时", description: "智能体执行平台、开发环境、运行时工具", icon: Code, gradient: "from-emerald-600 to-teal-600" },
  rag: { name: "RAG 检索增强", description: "检索增强生成、文档问答、知识库系统", icon: SearchIcon, gradient: "from-sky-600 to-cyan-600" },
  memory: { name: "AI 记忆系统", description: "长期记忆、知识存储、上下文管理", icon: Briefcase, gradient: "from-violet-600 to-purple-600" },
  "dev-tools": { name: "AI 开发工具", description: "开发者工具、SDK、API、测试框架", icon: Code, gradient: "from-gray-600 to-slate-600" },
  database: { name: "AI 数据库", description: "向量数据库、数据存储、数据处理", icon: Briefcase, gradient: "from-amber-600 to-orange-600" },
  observability: { name: "AI 可观测性", description: "监控、日志、追踪、性能分析", icon: SearchIcon, gradient: "from-teal-600 to-emerald-600" },
};

export function generateStaticParams() {
  const categories = new Set(toolsData.map((t) => t.category));
  return Array.from(categories).map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: { params: { slug: string } }) {
  const category = CATEGORIES[params.slug];
  if (!category) return { title: "Category Not Found | AIToolCrux" };

  const tools = toolsData.filter((t) => t.category === params.slug) as Tool[];
  const toolCount = tools.length;
  const topTools = [...tools]
    .sort((a, b) => calculateScoreResult(b.scores).total - calculateScoreResult(a.scores).total)
    .slice(0, 3)
    .map((t) => t.name)
    .join(", ");

  const categoryName = category.name.replace(/^AI\s+/, "").replace(/^AI/, "");
  const title = `Best ${categoryName} AI Tools 2026: Top ${toolCount} Rated & Reviewed | AIToolCrux`;
  const description = `Discover the best ${categoryName} AI tools in 2026. Expert reviews with 6-dimension ratings, pricing comparison, pros & cons. Top picks: ${topTools}. Find the perfect ${categoryName} tool for your needs.`;

  return {
    title: title,
    description: description.slice(0, 160),
    keywords: [`best ${categoryName} AI tools`, `${categoryName} AI tools 2026`, `${categoryName} tool reviews`, `top ${categoryName} AI`, "AI tool comparison", "AI software reviews", ...tools.slice(0, 5).map((t) => t.name)],
    alternates: {
      canonical: `https://www.aitoolcrux.com/category/${params.slug}`,
    },
    openGraph: {
      title: title,
      description: description.slice(0, 160),
      url: `https://www.aitoolcrux.com/category/${params.slug}`,
      type: "website",
    },
    twitter: {
      card: "summary_large_image",
      title: title,
      description: description.slice(0, 160),
    },
  };
}

export default function CategoryPage({ params }: { params: { slug: string } }) {
  const category = CATEGORIES[params.slug];
  if (!category) notFound();

  const Icon = category.icon;
  const tools = toolsData.filter((t) => t.category === params.slug) as Tool[];
  const sortedTools = [...tools].sort((a, b) => calculateScoreResult(b.scores).total - calculateScoreResult(a.scores).total);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      <Link href="/" className="inline-flex items-center gap-2 px-4 py-2 mb-4 text-sm font-medium text-gray-600 dark:text-gray-300 bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm hover:border-blue-300 dark:hover:border-blue-700 hover:text-blue-600 dark:hover:text-blue-400 transition-all">
        <ArrowLeft className="w-4 h-4" />
        返回首页
      </Link>

      {/* 可视化面包屑导航 */}
      <Breadcrumb
        items={[
          { name: "Home", url: "/" },
          { name: "Categories", url: "/ranking" },
          { name: category.name },
        ]}
        className="mb-6"
      />

      <section className={`relative overflow-hidden rounded-2xl bg-gradient-to-r ${category.gradient} p-8 text-white mb-8 shadow-lg`}>
        <div className="absolute -top-10 -right-10 w-40 h-40 bg-white/10 rounded-full blur-2xl" />
        <div className="relative flex items-center gap-6">
          <div className="w-16 h-16 flex items-center justify-center rounded-2xl bg-white/20 backdrop-blur-sm shadow-lg flex-shrink-0">
            <Icon className="w-8 h-8" />
          </div>
          <div className="flex-1 min-w-0">
            <h1 className="text-3xl font-extrabold mb-2">{category.name}</h1>
            <p className="text-white/80">{category.description}</p>
          </div>
          <div className="text-center flex-shrink-0">
            <div className="text-4xl font-extrabold">{sortedTools.length}</div>
            <div className="text-sm text-white/70">款工具</div>
          </div>
        </div>
      </section>

      <CategoryToolsClient tools={sortedTools} />

      {/* 分类详细内容 - SEO主题集群 */}
      {CATEGORY_CONTENT[params.slug] && (
        <div className="mt-12 space-y-10">
          {/* 分类详细介绍 */}
          <section className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-8">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">{category.name}完全指南</h2>
            <p className="text-gray-600 dark:text-gray-300 leading-relaxed">{CATEGORY_CONTENT[params.slug].intro}</p>
          </section>

          {/* 选购指南 */}
          <section className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-8">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">如何选择适合你的{category.name}</h2>
            <div className="space-y-4">
              {CATEGORY_CONTENT[params.slug].buyingGuide.map((tip, i) => (
                <div key={i} className="flex gap-4">
                  <div className="flex-shrink-0 w-8 h-8 flex items-center justify-center rounded-full bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 font-bold text-sm">
                    {i + 1}
                  </div>
                  <p className="text-gray-600 dark:text-gray-300 leading-relaxed pt-1">{tip}</p>
                </div>
              ))}
            </div>
          </section>

          {/* 该分类下的深度评测文章 - 内链 */}
          {(() => {
            const categoryPosts = postsData.filter((p) => {
              const postCat = (p.categorySlug || p.category || "").toLowerCase();
              return postCat.includes(params.slug) || 
                     (p.tags || []).some((t: string) => t.toLowerCase().includes(params.slug));
            }).slice(0, 6);
            if (categoryPosts.length === 0) return null;
            return (
              <section className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-8">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">{category.name}深度评测</h2>
                <p className="text-sm text-gray-500 dark:text-gray-400 mb-6">我们的编辑团队经过30天实测，为你带来最真实的工具评测</p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {categoryPosts.map((post) => (
                    <Link
                      key={post.slug}
                      href={`/blog/${post.slug}`}
                      className="group block p-4 rounded-xl border border-gray-100 dark:border-gray-800 hover:border-blue-200 dark:hover:border-blue-800 hover:bg-blue-50/50 dark:hover:bg-blue-900/10 transition-all"
                    >
                      <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-1 line-clamp-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                        {post.title}
                      </h3>
                      <p className="text-xs text-gray-500 dark:text-gray-400 line-clamp-2 mb-2">{post.excerpt}</p>
                      <div className="flex items-center gap-2 text-xs text-gray-400">
                        <span>{post.author}</span>
                        <span>·</span>
                        <span>{post.readTime || "5 min"}</span>
                      </div>
                    </Link>
                  ))}
                </div>
              </section>
            );
          })()}

          {/* FAQ */}
          <section className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-8">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
              <HelpCircle className="w-6 h-6 text-blue-500" />
              常见问题
            </h2>
            <div className="space-y-6">
              {CATEGORY_CONTENT[params.slug].faqs.map((faq, i) => (
                <div key={i} className="border-b border-gray-100 dark:border-gray-800 pb-6 last:border-0 last:pb-0">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">{faq.q}</h3>
                  <p className="text-gray-600 dark:text-gray-300 leading-relaxed">{faq.a}</p>
                </div>
              ))}
            </div>
          </section>
        </div>
      )}

      <section className="mt-12 pt-8 border-t border-gray-100 dark:border-gray-800">
        <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-4">浏览其他分类</h2>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {Object.entries(CATEGORIES).filter(([slug]) => slug !== params.slug).slice(0, 4).map(([slug, cat]) => {
            const CatIcon = cat.icon;
            const count = toolsData.filter((t) => t.category === slug).length;
            return (
              <Link key={slug} href={`/category/${slug}`} className="group flex items-center gap-3 p-4 bg-white dark:bg-gray-900 rounded-xl border border-gray-100 dark:border-gray-800 hover:border-blue-200 dark:hover:border-blue-800 hover:shadow-md transition-all">
                <div className={`w-10 h-10 flex items-center justify-center rounded-lg bg-gradient-to-br ${cat.gradient} text-white shadow-sm group-hover:scale-110 transition-transform flex-shrink-0`}>
                  <CatIcon className="w-5 h-5" />
                </div>
                <div className="min-w-0">
                  <div className="text-sm font-semibold text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors truncate">{cat.name}</div>
                  <div className="text-xs text-gray-400 dark:text-gray-500">{count} 款工具</div>
                </div>
              </Link>
            );
          })}
        </div>
      </section>
    </div>
  );
}
