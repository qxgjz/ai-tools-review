"""
AIToolCrux Auto Backup Script
Daily backup of critical JSON data files.
Keeps last 30 days of backups.
"""
import json
import shutil
import os
from datetime import datetime, timedelta
from pathlib import Path

PROJECT = Path(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")
BACKUP_DIR = PROJECT / "iteration_center" / "backup"
RETENTION_DAYS = 30

FILES_TO_BACKUP = [
    "data/posts.json",
    "data/tools.json",
    "data/comparisons.json",
]


def backup():
    today = datetime.now().strftime("%Y-%m-%d")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    for rel_path in FILES_TO_BACKUP:
        src = PROJECT / rel_path
        if not src.exists():
            results.append(f"⚠️ SKIP: {rel_path} not found")
            continue

        # Create backup filename: posts_2026-09-16.json
        filename = f"{src.stem}_{today}{src.suffix}"
        dst = BACKUP_DIR / filename

        shutil.copy2(src, dst)
        size_kb = dst.stat().st_size / 1024
        results.append(f"✅ {filename} ({size_kb:.0f}KB)")

    # Clean up old backups
    cutoff = datetime.now() - timedelta(days=RETENTION_DAYS)
    deleted = 0
    for f in BACKUP_DIR.glob("*.json"):
        mtime = datetime.fromtimestamp(f.stat().st_mtime)
        if mtime < cutoff:
            f.unlink()
            deleted += 1

    # Write backup manifest
    manifest = {
        "backup_date": today,
        "timestamp": datetime.now().isoformat(),
        "files_backed_up": len(results),
        "files_deleted_old": deleted,
        "retention_days": RETENTION_DAYS,
        "remaining_backups": len(list(BACKUP_DIR.glob("*.json"))),
    }
    with open(BACKUP_DIR / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("=== Auto Backup Complete ===")
    for r in results:
        print(f"  {r}")
    print(f"  🗑️  Deleted {deleted} old backups (>{RETENTION_DAYS} days)")
    print(f"  📁 Total backups kept: {manifest['remaining_backups']}")
    print(f"  📍 Backup dir: {BACKUP_DIR}")
    return manifest


if __name__ == "__main__":
    backup()
