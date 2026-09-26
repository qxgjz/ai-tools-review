"""Apply P2-PERF-FONT-001 and P2-PERF-CONFIG-001 fixes."""
import re
from pathlib import Path

base = Path(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")

# 1. layout.tsx: remove unused preconnect/dns-prefetch to Google Fonts
layout_path = base / "app" / "layout.tsx"
text = layout_path.read_text(encoding="utf-8")

# Remove preconnect to fonts.gstatic.com (line 114)
text = text.replace(
    '          <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />\n',
    ''
)
# Remove dns-prefetch to fonts.googleapis.com (line 116)
text = text.replace(
    '          <link rel="dns-prefetch" href="https://fonts.googleapis.com" />\n',
    ''
)
# Update comment to reflect reality
text = text.replace(
    '          {/* Fonts self-hosted via next/font/google - no external Google Fonts request needed */}',
    '          {/* Fonts self-hosted via geist/font - no external Google Fonts request needed; preconnect/dns-prefetch to fonts.googleapis.com removed to save DNS overhead */}'
)

layout_path.write_text(text, encoding="utf-8")
print("layout.tsx: removed unused Google Fonts preconnect/dns-prefetch")

# 2. next.config.mjs: trim deviceSizes from 8 to 6 values
config_path = base / "next.config.mjs"
cfg = config_path.read_text(encoding="utf-8")

# Replace deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840]
# With: [640, 828, 1080, 1200, 1920, 2560] (drop 750, 2048, 3840; add 2560 for retina)
old_dev = "deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],"
new_dev = "deviceSizes: [640, 828, 1080, 1200, 1920, 2560],"
assert old_dev in cfg, "deviceSizes pattern not found"
cfg = cfg.replace(old_dev, new_dev)

# Trim imageSizes from 8 to 6: drop 16, 384; keep 32, 48, 64, 96, 128, 256
old_img = "imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],"
new_img = "imageSizes: [32, 48, 64, 96, 128, 256],"
assert old_img in cfg, "imageSizes pattern not found"
cfg = cfg.replace(old_img, new_img)

config_path.write_text(cfg, encoding="utf-8")
print("next.config.mjs: trimmed deviceSizes 8->6, imageSizes 8->6")
print("Done.")
