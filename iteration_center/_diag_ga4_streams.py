# -*- coding: utf-8 -*-
"""诊断GA4新property数据流配置"""
import json, os
from google.oauth2 import service_account
from google.analytics.admin_v1beta import AnalyticsAdminServiceClient

cred_file = r'C:\Users\通明街\Downloads\aitoolcrux-automation-2f297efa91fb.json'
if not os.path.exists(cred_file):
    print('❌ 服务账号JSON不存在:', cred_file)
    exit()

creds = service_account.Credentials.from_service_account_file(
    cred_file, scopes=['https://www.googleapis.com/auth/analytics.readonly'])
client = AnalyticsAdminServiceClient(credentials=creds)

# 列出两个property的数据流
for prop in ['properties/549695344', 'properties/556518278']:
    try:
        streams = client.list_data_streams(parent=prop)
        for s in streams:
            print(f'{prop} → stream: name={s.name} displayName={s.display_name} type={s.type_.name}')
            wa = getattr(s, 'web_stream_data', None)
            if wa:
                print(f'    measurement_id={wa.measurement_id} default_uri={wa.default_uri}')
    except Exception as e:
        print(f'{prop} → 错误: {str(e)[:120]}')
