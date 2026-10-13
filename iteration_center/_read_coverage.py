# -*- coding: utf-8 -*-
import os, csv, glob

folder = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\gsc_coverage_20261009'
for f in sorted(glob.glob(os.path.join(folder, '*.csv'))):
    print('=' * 60)
    print('文件:', os.path.basename(f), '大小:', os.path.getsize(f), 'B')
    try:
        with open(f, encoding='utf-8-sig', errors='replace') as fh:
            reader = csv.reader(fh)
            rows = list(reader)
        if not rows:
            print('  (空文件)')
            continue
        print('  行数:', len(rows))
        for row in rows[:30]:
            print('  |', ' | '.join(c[:60] for c in row))
    except Exception as e:
        print('  读取失败:', e)
