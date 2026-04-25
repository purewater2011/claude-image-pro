#!/usr/bin/env python3
"""
main.py — claude-image-pro 用户友好 CLI 门面

适合在 shell 手动跑（不通过 Claude Code）。三种模式：

  1. raw 模式：用户输入直接当 prompt 喂 generator（最快，无优化）
       python3 main.py "a red apple" --output out.png

  2. enhance 模式：先调 enhancer 准备 request.md，提示用户用 LLM 完成展开
       python3 main.py "画一张抖音热搜榜" --enhance --output out.png
       # → 输出 request.md 路径，等用户手动/Claude 写 enhanced.txt

  3. 已优化 prompt 模式：直接传 enhanced 文件
       python3 main.py --prompt-file enhanced.txt --output out.png

通过 Claude Code 调用时不需要这个脚本——SKILL.md 直接编排 enhancer.py + generator.py。
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

# 让本目录的兄弟模块可以 import
sys.path.insert(0, str(Path(__file__).resolve().parent))

from generator import generate, load_env_file  # noqa: E402
from enhancer import build_request, _default_enhanced_path  # noqa: E402
from templates_loader import route  # noqa: E402


def cmd_raw(prompt: str, output: str, size: str) -> int:
    """直接出图，无优化"""
    try:
        result = generate(prompt=prompt, output=output, size=size)
    except Exception as e:
        print(f"❌ 出图失败: {e}", file=sys.stderr)
        return 1
    print(
        f"✅ → {result['path']}  ({result['elapsed_s']}s · ¥{result['cost_cny']} · {result['model']})"
    )
    return 0


def cmd_enhance(user_input: str, output: str, size: str) -> int:
    """调 enhancer 准备 request，提示用户完成优化步骤"""
    timestamp = int(time.time() * 1000)
    enhanced_path = Path(f"/tmp/cip_enhanced_{timestamp}.txt")
    request_path = build_request(user_input, output_path=enhanced_path)

    matched = route(user_input)
    print(f"📝 已生成优化请求: {request_path}")
    if matched:
        print(f"   命中模板: {matched.name}")
    else:
        print(f"   未命中具体模板（走通用增强）")
    print(f"\n⏳ 下一步：让 Claude 主进程读这份 md 并展开 prompt → 写到:")
    print(f"   {enhanced_path}")
    print(f"\n完成后跑：")
    print(
        f"   python3 {Path(__file__).name} "
        f"--prompt-file {enhanced_path} --output {output} --size {size}"
    )
    return 0


def cmd_from_file(prompt_file: str, output: str, size: str) -> int:
    """从已优化的 prompt 文件出图"""
    p = Path(prompt_file)
    if not p.exists():
        print(f"❌ 找不到 prompt 文件: {p}", file=sys.stderr)
        return 1
    prompt = p.read_text(encoding="utf-8").strip()
    if not prompt:
        print(f"❌ prompt 文件为空: {p}", file=sys.stderr)
        return 1

    try:
        result = generate(prompt=prompt, output=output, size=size)
    except Exception as e:
        print(f"❌ 出图失败: {e}", file=sys.stderr)
        return 1
    print(
        f"✅ → {result['path']}  ({result['elapsed_s']}s · ¥{result['cost_cny']} · {result['model']})"
    )
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="claude-image-pro CLI 入口",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument(
        "user_input",
        nargs="?",
        help="用户原始输入文本（搭配 --enhance 走优化流程，否则直接当 prompt）",
    )
    src.add_argument(
        "--prompt-file",
        help="已优化的 prompt 文件（跳过用户输入）",
    )

    ap.add_argument("--output", "-o", required=True, help="输出 PNG 路径")
    ap.add_argument(
        "--size", default="1024x1536", help="尺寸（默认 1024x1536，9:16 抖音）"
    )
    ap.add_argument(
        "--enhance",
        action="store_true",
        help="走优化流程：先调 enhancer 准备 request，再让 Claude 展开",
    )

    args = ap.parse_args()

    # 加载用户配置
    load_env_file(Path.home() / ".claude-image-pro" / ".env")

    if args.prompt_file:
        return cmd_from_file(args.prompt_file, args.output, args.size)

    if args.enhance:
        return cmd_enhance(args.user_input, args.output, args.size)

    return cmd_raw(args.user_input, args.output, args.size)


if __name__ == "__main__":
    sys.exit(main())
