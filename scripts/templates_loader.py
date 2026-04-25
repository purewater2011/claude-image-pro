#!/usr/bin/env python3
"""
templates_loader.py — 关键词路由 + 模板加载

根据用户输入关键词匹配 templates/ 下的模板文件。
不调 LLM，纯字符串匹配。
"""
from __future__ import annotations

import re
from pathlib import Path

# 默认模板目录（相对本文件）
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

# 路由表：(正则模式, 模板文件名)
# 顺序敏感——前面优先级更高，更具体的关键词放前面
KEYWORD_MAP: list[tuple[str, str]] = [
    # 抖音（专门模板，含热搜/封面/评论/直播间/主页 5 子场景）
    (r"抖音|douyin|短视频热搜|短视频封面|抖音直播", "douyin_ui.md"),

    # 信息图（拆解/菜谱/字帖/科普）
    (r"拆解图?|爆炸图|分解图|菜谱|做法|步骤|流程图|字帖|书法|临摹|科普|infographic", "infographic.md"),

    # 角色设计（多视角/杂志封面）
    (r"角色(卡|图|设定)|设定(图|卡)|多视角|三面图|角色分解|杂志封面|杂志大片", "character.md"),

    # 海报（旅游/电影/赛事/攻略/关系图/超市/视觉冲击）
    (r"海报|poster|发布会|宣传图|banner|旅游图|电影海报|攻略图|地图|角色关系|关系图|超市|价格图|促销", "poster.md"),

    # 真实摄影（产品广告/真实人像/户外）
    (r"产品图|开箱图?|广告图|真实场景|真实人像|DSLR|户外照?|户外人像|户外摄影|街拍|写实摄影|人像写真", "photo.md"),

    # 通用 UI 截图（视频号/小红书/快手/微博/X 推文/微信/知乎，不抖音）
    (r"视频号|小红书|xiaohongshu|xhs|小红薯|快手|微博|weibo|推文|推特|tweet|X 推|x推|twitter|微信|朋友圈|聊天截图|知乎", "ui_general.md"),
]


def route(user_input: str, templates_dir: Path = TEMPLATES_DIR) -> Path | None:
    """根据用户输入匹配模板路径。未命中返回 None"""
    for pattern, filename in KEYWORD_MAP:
        if re.search(pattern, user_input, re.IGNORECASE):
            template_path = templates_dir / filename
            if template_path.exists():
                return template_path
    return None


def list_available(templates_dir: Path = TEMPLATES_DIR) -> list[str]:
    """列出 templates/ 下已存在的模板"""
    if not templates_dir.exists():
        return []
    return sorted(p.name for p in templates_dir.glob("*.md"))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python3 templates_loader.py '用户输入文本'")
        print("\n已注册路由：")
        for pattern, filename in KEYWORD_MAP:
            print(f"  {pattern!r:40} → {filename}")
        print("\n已存在的模板文件：")
        for name in list_available():
            print(f"  {name}")
        sys.exit(0)

    user_input = " ".join(sys.argv[1:])
    matched = route(user_input)
    if matched:
        print(f"✅ 命中模板: {matched}")
    else:
        print(f"⚠️  未命中任何模板，将走通用增强")
