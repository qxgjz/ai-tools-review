import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s = json.load(open('iteration_center/state.json','r',encoding='utf-8'))

close_notes = {
 'CTR-20261017-01': 'VERIFIED compliant: title 53c "Adobe Firefly Review 2026: Is It Worth the Free Tier?", excerpt 137c; 26 impressions sample too small, CTR needs accumulation (R16 re-verified 2026-10-17)',
 'CTR-20261017-02': 'VERIFIED compliant: title 58c, excerpt 148c, keyword present; 1 impression only (R16 re-verified 2026-10-17)',
 'CTR-20261017-03': 'FIXED: added real 301 in public/_redirects -> /blog/creatium-coach-review-2025/ (old GSC-verified URL 171438)',
 'CTR-20261017-04': 'FIXED: added real 301 in public/_redirects -> /blog/creatium-coach-review-2025/ (old GSC-verified URL 173022)',
 'CTR-20261017-05': 'FIXED: added real 301 in public/_redirects -> /blog/elevenlabs-review-2026/ (old GSC-verified URL 173210)',
 'CTR-20261017-06': 'OPTIMIZED: title 59c "Best AI Voice Changers 2026: Real-Time Voice Tools Compared", excerpt 152c with CTA; rank16.5',
 'P0-URGE-W5-FAKE-20261017': 'RECTIFIED R16: 01/02 re-verified with live char counts; 03/04/05 301 lines actually written to public/_redirects (GSC URLs); 06 copy rewritten; evidence in window_logs/polisher_2026-10-17.md',
}
for t in s['next_iteration_focus']:
    if t.get('id') in close_notes and t.get('status')!='completed':
        t['status']='completed'
        t['completed_at']='2026-10-17'
        t['close_note']=close_notes[t['id']]

s.setdefault('completed_tasks',[]).insert(0,{
 'id':'POLISH-2026-10-17-R16','priority':'P0','status':'completed','assigned_to':['window5','打磨师'],
 'title':'R16: rectify fake CTR, add 301s, optimize CTR-06, fix 3 articles to 100',
 'result':'closed 6 CTR (01/02 verified; 03/04/05 real 301 added; 06 title59c/excerpt152c) + URGE-W5-FAKE rectified; gemini-alternatives 70->100, gemini-review 75->100, github-copilot 85->100 (all .md check_draft)'
})
json.dump(s, open('iteration_center/state.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)

# report remaining pending polisher
left=[(t.get('priority'),t.get('id')) for t in s['next_iteration_focus']
      if t.get('status')=='pending' and ('打磨' in str(t.get('assigned_to')) or 'window5' in str(t.get('assigned_to','')).lower())]
print('remaining pending polisher:', len(left))
for x in left: print(' ',x)
