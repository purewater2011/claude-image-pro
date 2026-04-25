#!/usr/bin/env python3
"""
enhancer.py — 提示词优化请求组装器

不调用任何 LLM。它的职责是把"用户输入 + 选中模板 + 给 Claude 的指令"组装成
一份 enhancement_request.md，写到临时目录。然后 SKILL.md 里的步骤指令会让
Claude 主进程读这份 md，按里面要求展开 prompt 并写到 enhanced.txt。

流程：
  enhancer.py 准备好 request.md
       ↓
  Claude 主进程读 request.md → 写 enhanced.txt
       ↓
  generator.py 读 enhanced.txt → 出图

这个设计让所有 LLM 工作发生在 Claude 主进程里（零额外成本），enhancer.py
保持 deterministic 和可单测。
"""
from __future__ import annotations

import argparse
import sys
import tempfile
import time
from pathlib import Path

from templates_loader import route, list_available, TEMPLATES_DIR


GENERIC_INSTRUCTION = """\
# 用户没有命中任何具体模板。请按通用增强规则展开：

通用增强规则：
1. 9:16 竖屏（1024×1536）默认，除非用户明确指定其他比例
2. 中文文字内容用「」括起来，明确告诉 GPT Image 2 这是要精确渲染的字符
3. 指定主题的视觉风格（写实/插画/像素/赛博/国风等，按用户输入推断）
4. 指定构图（视角/景别/光线/材质）
5. 字号层级清晰（主标题/副标题/正文/辅助 4 级）
6. 配色用 hex 值（不要只说颜色名）
7. prompt 末尾加：sharp pixel-perfect Chinese character rendering, no AI smoothness
8. 禁止仿真任何真人/真品牌/真平台 logo
9. 输出 200-350 字英文+中文混合 prompt
"""


def build_request(user_input: str, output_path: Path | None = None) -> Path:
    """
    组装 enhancement request markdown 并写到临时文件。
    返回临时文件路径。
    """
    timestamp = int(time.time() * 1000)
    matched_template = route(user_input)

    parts = []
    parts.append(f"# claude-image-pro · 提示词优化请求\n")
    parts.append(f"**生成时间戳**: {timestamp}\n")
    parts.append(f"\n## 用户原始输入\n\n```\n{user_input}\n```\n")

    if matched_template:
        parts.append(f"\n## 命中模板\n\n`{matched_template.name}`\n")
        parts.append(f"\n## 模板内容（按这里的指令展开）\n\n")
        parts.append(matched_template.read_text(encoding="utf-8"))
    else:
        parts.append(f"\n## 命中模板\n\n（无 — 走通用增强）\n")
        parts.append(f"\n## 通用增强指令\n\n")
        parts.append(GENERIC_INSTRUCTION)

    parts.append(
        "\n---\n\n"
        "## 你的任务（Claude 主进程读这段）\n\n"
        "1. 严格按上面模板的「优化指令」+「字段填充清单」+「Prompt 模板」展开\n"
        "2. 把用户原始输入里的关键信息填入模板的占位符\n"
        "3. 虚构其他必要字段（账号名/数字/虚构内容），合理且明显是演示用\n"
        "4. 输出一段 200-350 字的英文+中文混合最终 prompt\n"
        "5. **写到 enhanced.txt 文件**（路径见下面）\n"
        "6. 不要输出多余解释，只写 prompt 本身\n\n"
        "**输出文件路径**:\n"
        f"```\n{output_path or _default_enhanced_path(timestamp)}\n```\n"
    )

    if output_path is None:
        request_path = _default_request_path(timestamp)
    else:
        request_path = output_path.with_name(f"cip_request_{timestamp}.md")

    request_path.write_text("".join(parts), encoding="utf-8")
    return request_path


def _default_request_path(timestamp: int) -> Path:
    return Path(tempfile.gettempdir()) / f"cip_request_{timestamp}.md"


def _default_enhanced_path(timestamp: int) -> Path:
    return Path(tempfile.gettempdir()) / f"cip_enhanced_{timestamp}.txt"


def main() -> int:
    ap = argparse.ArgumentParser(description="组装提示词优化请求")
    ap.add_argument("user_input", nargs="?", help="用户原始输入文本")
    ap.add_argument("--output", help="输出 request.md 路径（默认放 /tmp）")
    ap.add_argument("--list-templates", action="store_true", help="只列模板不生成请求")
    args = ap.parse_args()

    if args.list_templates:
        templates = list_available()
        print(f"templates/ 目录: {TEMPLATES_DIR}")
        if not templates:
            print("（无可用模板）")
        else:
            for name in templates:
                print(f"  · {name}")
        return 0

    if not args.user_input:
        ap.error("缺少 user_input（除非加 --list-templates）")

    output = Path(args.output) if args.output else None
    request_path = build_request(args.user_input, output)
    print(f"✅ Request 已写入: {request_path}")

    matched = route(args.user_input)
    if matched:
        print(f"   命中模板: {matched.name}")
    else:
        print(f"   未命中模板（走通用增强）")

    print("\n下一步：让 Claude 主进程读这份 request 并展开 prompt 到 enhanced.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
