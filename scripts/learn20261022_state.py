# -*- coding: utf-8 -*-
import io,json,os,datetime
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='iteration_center/state.json'
s=json.load(io.open(fn,encoding='utf-8'))
now='2026-10-22T06:05:00'
NEW=[
{
 "id":"P1-READABILITY-SENTENCE-PARA-20261022",
 "task":"可读性批次打磨（学习落地，来源Google Search Central/Yoast/NNg/ClaritySEO）：①平均句长15-20词，>25词句子拆成2-3句（Yoast: >20词句子占比>25%即标红）；②段落2-4句/<100词（Yoast绿<150词、红>200词），一段只讲一个意思；③主动语态占比>90%（被动>10%标红）；④加过渡词（however/for example/after that）连接，避免连续同结构句；⑤目标Flesch Reading Ease 60-70（电商65-75，grade6-7），先保SOP硬线Flesch>50。批量过现存低分/长文，一次≥5篇。",
 "priority":"P1","assigned_to":["window5","打磨师"],"status":"pending",
 "source":"learning_readability_20261022","created_at":now
},
{
 "id":"P1-SCAN-FORMAT-20261022",
 "task":"可扫描性改造（NN/g F-pattern：用户扫读而非逐字读）：①功能/价格/优缺点对比不要埋进段落，改用markdown表格或bullet list；②每个H2下不超过300-400词无小标题；③关键短语少量加粗（用得越少越突出）；④锚文本用信息词（写具体工具名/功能，禁用click here/more）；⑤删掉无信息的凑字开头（filler intro）；⑥长篇配图/图卡打断文字墙。",
 "priority":"P1","assigned_to":["window5","打磨师"],"status":"pending",
 "source":"learning_readability_20261022","created_at":now
},
{
 "id":"P1-LLM-ANSWER-BLOCK-20261022",
 "task":"LLM/Perplexity可提取块（与现有ANSWER-FIRST互补，加量化规则）：①首100词内给直接答案（BLUF），含命名实体+具体数字+货币+日期；②每个问句H2下紧跟40-60词自包含直答块（不依赖前文指代，匹配RAG~512-token分块）；③FAQ用用户真实搜索问句；④事实带年份/更新日期，避免悬空代词。",
 "priority":"P1","assigned_to":["window5","打磨师"],"status":"pending",
 "source":"learning_readability_20261022","created_at":now
}
]
existing={t.get('id') for t in s['next_iteration_focus']}
added=0
for e in NEW:
    if e['id'] not in existing:
        s['next_iteration_focus'].insert(0,e); added+=1
s['last_learning_topic']='readability-scannability-LLM-extraction'
s['last_learning_update']=now
json.dump(s,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('added',added,'total pending',sum(1 for t in s['next_iteration_focus'] if t.get('status')=='pending'))
