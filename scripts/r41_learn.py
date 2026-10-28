# -*- coding: utf-8 -*-
import io,json,os
from datetime import datetime
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='iteration_center/state.json'
s=json.load(io.open(fn,encoding='utf-8'))
now=datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')
new={
 'id':'LEARN-20261029-EEAT','task':'E-E-A-T落地：每篇加具名作者byline+author bio页(LinkedIn/年限/认证)；每篇2-3条主源外链(官方文档/研究原报告，非二手博客)；文首加1个first-hand experience bullet(实测截图/真实使用时长/具体踩坑)；统计数据必须带(年份+机构)；YMYL类(隐私/定价/安全)加reviewed by+更新日期；Article/Person schema结构化数据；季度E-E-A-T自检清单',
 'priority':'P1','assigned_to':['打磨师','创作家'],'status':'pending','source':'learn-eeat-20261029','created_at':now,
 'close_note':'','completed_at':'','progress_note':'E-E-A-T学习落地任务'
}
ids=[t['id'] for t in s.get('next_iteration_focus',[])]
if new['id'] not in ids:
    s.setdefault('next_iteration_focus',[]).insert(0,new)
json.dump(s,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('state ok')

# commander_learning.md
cl=r'C:\Users\通明街\Doubao\chats\2026-09-02\new-chat\commander_learning.md'
block=f"""

## 2026-10-29 打磨师学习：E-E-A-T（5权威源，15知识点）
来源：Google Search Central / Backlinko / Visiblytics / Metaflow / Rellify / AuthorityStack / TheGuideX。
1. E-E-A-T = Experience(一手经验) / Expertise(专业知识) / Authoritativeness(权威) / Trust(可信)。
2. Trust是最重要一环，缺Trust其他再好也白搭。
3. E-E-A-T不是单一排名分，而是Google通过数百信号评估的质量框架。
4. 2022-12加入第一个E(Experience)，因为Google区分"纸面专业"和"真实使用过"。
5. YMYL(健康/财务/法律/安全/重大生活决策)要求最高，AItools站涉及定价/隐私/安全属轻度YMYL。
6. 每篇必须有具名作者byline(不能By Editorial Team)，链接到author bio页(照片+年限+认证+LinkedIn+代表作)。
7. YMYL内容需reviewed by(具名专家+头衔)标识。
8. 外链引主源(官方文档/原始研究/政府/peer-reviewed)，不引二手总结博客；每篇2-3条。
9. 所有统计带(年份+机构)，2019旧数据害信任分。
10. 一手经验=真实截图/具体使用时长/真实踩坑，AI批量文最缺这一点。
11. Article/Person/Organization schema结构化数据让Google读懂作者关系。
12. Published Date + Last Updated Date双日期，evergreen每年复审刷新。
13. 编辑QA流程：SME审校+事实核查+可读性+更新计划，显示有编辑监督。
14. AI内容本身不被惩罚，但无人工核查/无原创经验/无引用的AI文得最低分。
15. AI Overviews/AI答案引用同一信任池，E-E-A-T强的站更易被AI答案引用。
落地：已写入state.json LEARN-20261029-EEAT(P1，打磨师+创作家)。
"""
with io.open(cl,'a',encoding='utf-8',newline='') as f: f.write(block)
print('cl ok')
