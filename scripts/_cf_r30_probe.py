# -*- coding: utf-8 -*-
"""r30: CF 今日流量 + Bot 保护权限探测（token 从 api_keys.json 读取，防 GH013）"""
import urllib.request, json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE, 'iteration_center', 'api_keys.json'), encoding='utf-8') as f:
    _tok = json.load(f)
CF_TOKEN = _tok['cloudflare_api_token']
CF_ZONE = _tok['cloudflare_zone_id']

def gql(query, variables):
    body = json.dumps({'query': query, 'variables': variables}).encode('utf-8')
    req = urllib.request.Request('https://api.cloudflare.com/client/v4/graphql', data=body, method='POST')
    req.add_header('Authorization', 'Bearer ' + CF_TOKEN)
    req.add_header('Content-Type', 'application/json')
    return json.loads(urllib.request.urlopen(req, timeout=60).read().decode('utf-8'))

q = """query($zone: String!) {
  viewer { zones(filter: {zoneTag: $zone}) {
    httpRequests1dGroups(limit: 7, filter: {date_geq: "2026-10-11"}, orderBy: [date_ASC]) {
      dimensions { date }
      sum { requests pageViews }
      uniq { uniques }
    }
  } }
}"""
try:
    res = gql(q, {'zone': CF_ZONE})
    groups = res['data']['viewer']['zones'][0]['httpRequests1dGroups']
    print('=== Daily requests 10/11-10/17 ===')
    for g in groups:
        d = g['dimensions']['date']
        s = g.get('sum', {})
        u = g.get('uniq', {}).get('uniques', 0)
        r = s.get('requests', 0)
        p = s.get('pageViews', 0)
        print(f"{d}  req={r}  pv={p}  uniq={u}  pv/req={round(p/max(r,1),3)}")
except Exception as e:
    print('GQL ERR:', str(e)[:300])
