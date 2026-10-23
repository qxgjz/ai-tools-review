# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='iteration_center/state.json'
s=json.load(io.open(fn,encoding='utf-8'))
now='2026-10-23T21:30:00'
cid='P0-GEO-TLDR-TABLE-20261023'
note=('R28完成：GSC live_pull聚合仅8篇博客有曝光（openai_astra_review 1083/best-ai-voice-changers 1020/adobe-firefly 441/beginners 374/ai-coding-comparison 186/review-guide 66/comparison 18/agents 2），'
'补足12篇高价值comparison/listicle共20篇，每篇顶部加## TL;DR(2-3句直接答案，取自自身quickAnswer/title，无编造)；14篇已有markdown表格，6篇无表者用正文真实H2建Guide-at-a-glance表。'
'验收：20篇均含TL;DR+表格，原生check_draft 73-88无回退；随机抽3篇(openai_astra/note-taking/chatgpt-vs-gemini)llmevalkit evaluate_content score100、无幻觉、AIprob<0.3、TL;DR块存在。'
'同轮低分优化5篇双达标(zens88+Flesch>50)：project-mgmt51.9/design61.3/email60.4/transcription53.4/video-editors51.4；midjourney-vs-dalle3 zens88但Flesch46.9留正文批改。')
done=False
for t in s['next_iteration_focus']:
    if t.get('id')==cid and t.get('status')=='pending':
        t['status']='completed'; t['completed_at']=now; t['close_note']=note; done=True
        if not any(x.get('id')==cid for x in s.get('completed_tasks',[])):
            s.setdefault('completed_tasks',[]).insert(0,dict(t))
json.dump(s,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('closed',done)
