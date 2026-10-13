# -*- coding: utf-8 -*-
import io

src = r'C:\Users\通明街\AppData\Local\DoubaoWork\User Data\Default\.doubaowork\agent_mode\workspace\.skills\doubao-pc-optimizer\scripts\win_clean.ps1'
out = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\scripts\win_clean_l1_20261010.ps1'
txt = io.open(src, encoding='utf-8-sig').read()

add = '''
# --- 追加白名单项(2026-10-10 扫描确认的可再生大缓存) ---
CleanDir "pnpm store缓存" "$env:LOCALAPPDATA\pnpm\store"
CleanDir "Playwright浏览器缓存" "$env:LOCALAPPDATA\ms-playwright"
CleanDir "千帆更新缓存" "$env:LOCALAPPDATA\qianfan-desktop-app-updater"
CleanDir "PyInstaller残留解压目录" "$env:LOCALAPPDATA\hclaw-pyinstaller"
'''
marker = '$rb = (New-Object -ComObject Shell.Application)'
assert marker in txt, 'marker not found'
txt = txt.replace(marker, add + '\n' + marker)
io.open(out, 'w', encoding='utf-8-sig').write(txt)
print('OK generated:', out)
print('bytes:', len(txt.encode('utf-8')))
