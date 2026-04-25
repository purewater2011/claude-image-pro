#!/usr/bin/env python3
"""
ab_compare.py — A/B 对比拼图

把"raw（未优化）"和"enhanced（skill 优化）"两张图左右拼成对比图，
带顶部标签和分隔线。Day14 抖音副演示用。

用法:
    python3 ab_compare.py --raw raw.png --enhanced enhanced.png --output compare.png

A/B 协调流程在 SKILL.md 里，本脚本只负责拼图。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print(
        "❌ 需要 Pillow 库。安装：pip3 install pillow",
        file=sys.stderr,
    )
    sys.exit(1)


# 视觉风格常量
LABEL_BAND_HEIGHT = 80
LABEL_BG_LEFT = (200, 50, 50, 230)      # 暗红半透明
LABEL_BG_RIGHT = (50, 150, 80, 230)     # 暗绿半透明
LABEL_TEXT_COLOR = (255, 255, 255)
DIVIDER_WIDTH = 6
DIVIDER_COLOR = (255, 215, 0)            # 金色分割线
PADDING = 20
LABEL_FONT_SIZE = 36


def find_font() -> ImageFont.FreeTypeFont:
    """找一个能渲染中文的字体（macOS 优先 PingFang，跨平台 fallback）"""
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, LABEL_FONT_SIZE)
            except OSError:
                continue
    # 最后退化到默认（不一定支持中文）
    return ImageFont.load_default()


def make_compare(
    raw_path: Path,
    enhanced_path: Path,
    output_path: Path,
    label_left: str = "❌ 直接画 · 未优化",
    label_right: str = "✅ skill 自动优化",
) -> Path:
    """生成左右对比图"""
    img_l = Image.open(raw_path).convert("RGB")
    img_r = Image.open(enhanced_path).convert("RGB")

    # 对齐高度（取较大）
    target_h = max(img_l.height, img_r.height)
    if img_l.height != target_h:
        new_w = int(img_l.width * (target_h / img_l.height))
        img_l = img_l.resize((new_w, target_h), Image.Resampling.LANCZOS)
    if img_r.height != target_h:
        new_w = int(img_r.width * (target_h / img_r.height))
        img_r = img_r.resize((new_w, target_h), Image.Resampling.LANCZOS)

    total_w = img_l.width + DIVIDER_WIDTH + img_r.width
    total_h = LABEL_BAND_HEIGHT + target_h

    canvas = Image.new("RGB", (total_w, total_h), (245, 245, 245))

    # 贴两张图
    canvas.paste(img_l, (0, LABEL_BAND_HEIGHT))
    canvas.paste(img_r, (img_l.width + DIVIDER_WIDTH, LABEL_BAND_HEIGHT))

    # 画金色分割线
    draw = ImageDraw.Draw(canvas)
    draw.rectangle(
        [
            (img_l.width, 0),
            (img_l.width + DIVIDER_WIDTH, total_h),
        ],
        fill=DIVIDER_COLOR,
    )

    # 顶部 label band（半透明色块）
    overlay = Image.new("RGBA", (total_w, LABEL_BAND_HEIGHT), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    odraw.rectangle(
        [(0, 0), (img_l.width, LABEL_BAND_HEIGHT)], fill=LABEL_BG_LEFT
    )
    odraw.rectangle(
        [
            (img_l.width + DIVIDER_WIDTH, 0),
            (total_w, LABEL_BAND_HEIGHT),
        ],
        fill=LABEL_BG_RIGHT,
    )
    canvas.paste(overlay, (0, 0), overlay)

    # 画 label 文字
    font = find_font()
    draw = ImageDraw.Draw(canvas)
    # 居中（粗略估算）
    for label, x_start, x_end in [
        (label_left, 0, img_l.width),
        (label_right, img_l.width + DIVIDER_WIDTH, total_w),
    ]:
        try:
            bbox = draw.textbbox((0, 0), label, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
        except Exception:
            text_w, text_h = len(label) * 20, 30
        cx = (x_start + x_end) // 2
        text_x = cx - text_w // 2
        text_y = (LABEL_BAND_HEIGHT - text_h) // 2 - 4
        draw.text((text_x, text_y), label, font=font, fill=LABEL_TEXT_COLOR)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path, format="PNG", optimize=True)
    return output_path


def main() -> int:
    ap = argparse.ArgumentParser(description="A/B 对比拼图")
    ap.add_argument("--raw", required=True, help="未优化版图片路径")
    ap.add_argument("--enhanced", required=True, help="skill 优化版图片路径")
    ap.add_argument("--output", required=True, help="输出对比图路径")
    ap.add_argument("--label-left", default="❌ 直接画 · 未优化")
    ap.add_argument("--label-right", default="✅ skill 自动优化")
    args = ap.parse_args()

    raw = Path(args.raw)
    enhanced = Path(args.enhanced)

    for label, p in [("raw", raw), ("enhanced", enhanced)]:
        if not p.exists():
            print(f"❌ 找不到 {label} 图: {p}", file=sys.stderr)
            return 1

    output = make_compare(
        raw_path=raw,
        enhanced_path=enhanced,
        output_path=Path(args.output),
        label_left=args.label_left,
        label_right=args.label_right,
    )
    print(f"✅ 对比图 → {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
