# 提权清空回收站（管理员运行，结果写入日志供 agent 读取）
$log = "C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\scripts\rb_clean_admin_log.txt"
$before = (Get-ChildItem "C:\$Recycle.Bin" -Recurse -Force -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer } | Measure-Object Length -Sum).Sum
if (-not $before) { $before = 0 }
Add-Content -Path $log -Value ("=== 提权清空回收站 {0} ===" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss")) -Encoding UTF8
Add-Content -Path $log -Value ("清理前回收站: {0} MB" -f [math]::Round($before/1MB)) -Encoding UTF8
try {
    Clear-RecycleBin -Force -ErrorAction Stop
    Add-Content -Path $log -Value "Clear-RecycleBin 调用成功" -Encoding UTF8
} catch {
    Add-Content -Path $log -Value ("Clear-RecycleBin 失败: " + $_.Exception.Message) -Encoding UTF8
}
$after = (Get-ChildItem "C:\$Recycle.Bin" -Recurse -Force -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer } | Measure-Object Length -Sum).Sum
if (-not $after) { $after = 0 }
Add-Content -Path $log -Value ("清理后回收站: {0} MB, 释放 {1} MB" -f [math]::Round($after/1MB), [math]::Round(($before-$after)/1MB)) -Encoding UTF8
Add-Content -Path $log -Value ("C盘空闲: {0} GB" -f [math]::Round((Get-PSDrive C).Free/1GB,2)) -Encoding UTF8
Add-Content -Path $log -Value "=== 完成 ===" -Encoding UTF8
