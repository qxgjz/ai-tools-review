# -*- coding: utf-8 -*-
# 生成实际执行版清理脚本：替换COM回收站统计为文件系统统计（避免卡住），保留 Clear-RecycleBin
import io

src = r'C:\Users\通明街\AppData\Local\DoubaoWork\User Data\Default\.doubaowork\agent_mode\workspace\.skills\doubao-pc-optimizer\scripts\win_clean.ps1'
out = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\scripts\win_clean_l1_exec_20261010.ps1'
txt = io.open(src, encoding='utf-8-sig').read()

# 追加白名单
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

# 替换COM回收站统计为文件系统统计（避免 COM 枚举卡住）
old_rb = '''$rb = (New-Object -ComObject Shell.Application).NameSpace(0xA).Items() | Measure-Object -Property Size -Sum
$rbSize = $rb.Sum; if (-not $rbSize) { $rbSize = 0 }
if ($IncludeRecycleBin) {
  if ($DryRun) { Log ("[预演] 回收站: 可清空 {0} MB(清空后不可恢复)" -f [math]::Round($rbSize/1MB)) }
  else {
    Clear-RecycleBin -Force -ErrorAction SilentlyContinue
    # 清空后重测,只计入实际清掉的部分
    $rbAfter = ((New-Object -ComObject Shell.Application).NameSpace(0xA).Items() | Measure-Object -Property Size -Sum).Sum
    if (-not $rbAfter) { $rbAfter = 0 }
    $script:freed += ($rbSize - $rbAfter)
    Log ("[完成] 回收站: 清空 {0} MB" -f [math]::Round(($rbSize-$rbAfter)/1MB))
  }
} else {
  Log ("[跳过] 回收站({0} MB)— 默认不清空(用户误删文件的恢复渠道);用户单项确认后加 -IncludeRecycleBin 执行" -f [math]::Round($rbSize/1MB))
}'''
new_rb = '''$rbSize = (Get-ChildItem "C:\\$Recycle.Bin" -Recurse -Force -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer } | Measure-Object Length -Sum).Sum
if (-not $rbSize) { $rbSize = 0 }
if ($IncludeRecycleBin) {
  if ($DryRun) { Log ("[预演] 回收站: 可清空 {0} MB(清空后不可恢复)" -f [math]::Round($rbSize/1MB)) }
  else {
    Clear-RecycleBin -Force -ErrorAction SilentlyContinue
    $rbAfter = (Get-ChildItem "C:\\$Recycle.Bin" -Recurse -Force -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer } | Measure-Object Length -Sum).Sum
    if (-not $rbAfter) { $rbAfter = 0 }
    $script:freed += ($rbSize - $rbAfter)
    Log ("[完成] 回收站: 清空 {0} MB" -f [math]::Round(($rbSize-$rbAfter)/1MB))
  }
} else {
  Log ("[跳过] 回收站({0} MB)— 默认不清空(用户误删文件的恢复渠道);用户单项确认后加 -IncludeRecycleBin 执行" -f [math]::Round($rbSize/1MB))
}'''
assert old_rb in txt, 'rb block not found'
txt = txt.replace(old_rb, new_rb)
io.open(out, 'w', encoding='utf-8-sig').write(txt)
print('OK generated exec script:', out)
print('bytes:', len(txt.encode('utf-8')))
