#!/usr/bin/env python3
"""
generator.py — claude-image-pro 出图引擎

调用 OpenAI 兼容接口（/v1/images/generations）生成图片。
支持作者自建中转站、APIYI、速创API、官方 OpenAI 等任意 OpenAI 协议端点。

CLI 用法:
    python3 generator.py --prompt "a red apple" --output out.png
    python3 generator.py --prompt-file prompt.txt --output out.png --size 1024x1536

库用法:
    from generator import generate
    result = generate("a red apple", "out.png", size="1024x1024")
    # → {"path": "out.png", "cost_cny": 0.78, "elapsed_s": 3.2, "model": "gpt-image-2"}
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

import requests

# 单图成本估算（人民币，基于 OpenAI 官方定价 + 中转站常见加价）
# 实际价格依赖中转站，这里给保守估算用于打印
COST_TABLE_CNY = {
    "1024x1024": 1.50,
    "1024x1536": 1.20,
    "1536x1024": 1.20,
    "2048x2048": 4.00,
    "auto": 1.20,
}


def load_env_file(env_path: Path) -> None:
    """简易 .env 加载器，不引入 python-dotenv 依赖"""
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip("'\"")
        os.environ.setdefault(key, val)


def _resolve_base_url() -> str:
    """从环境变量取 base url，规范化（去掉尾部 /v1）"""
    base = os.environ.get("OPENAI_BASE_URL", "").rstrip("/")
    if base.endswith("/v1"):
        base = base[:-3]
    if not base:
        raise RuntimeError(
            "缺少 OPENAI_BASE_URL。请编辑 ~/.claude-image-pro/.env"
        )
    return base


def estimate_cost_cny(size: str) -> float:
    return COST_TABLE_CNY.get(size, 1.20)


class RetryableError(Exception):
    """可重试的临时错误"""


class FatalError(Exception):
    """不可重试的永久错误（认证错 / 模型不存在 / 请求格式错）"""


def _attempt_once(
    base: str, key: str, model: str, prompt: str, size: str, timeout: int
) -> dict:
    """单次尝试。成功返回 API 解析后的 item dict；失败抛 RetryableError 或 FatalError。"""
    try:
        resp = requests.post(
            f"{base}/v1/images/generations",
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            data=json.dumps({"model": model, "prompt": prompt, "n": 1, "size": size}),
            timeout=timeout,
        )
    except (requests.Timeout, requests.ConnectionError) as e:
        raise RetryableError(f"网络错误: {type(e).__name__}: {e}") from e

    sc = resp.status_code
    body_preview = resp.text[:300]

    # 真正的认证/请求格式错才不可重试
    if sc in (401, 403):
        raise FatalError(f"HTTP {sc} 认证/权限错: {body_preview}")
    if sc == 400:
        raise FatalError(f"HTTP {sc} 请求格式错: {body_preview}")

    # 中转站常见的临时错（包括 404 DeploymentNotFound、upstream_error 等）
    # 用户明确告知 gpt-image-2 供应商不稳定，所以把 404 / 502 / 503 等都归入可重试
    if sc != 200:
        raise RetryableError(f"HTTP {sc} 中转站抖动可重试: {body_preview}")

    try:
        body = resp.json()
    except Exception as e:
        raise RetryableError(f"JSON 解析失败: {e} body[:300]={resp.text[:300]}") from e

    items = body.get("data") or []
    if not items:
        # 中转站偶发返回空 data，归为可重试
        raise RetryableError(f"返回 data 为空: {json.dumps(body)[:300]}")

    item = items[0]
    if not (item.get("b64_json") or item.get("url")):
        raise RetryableError(f"data[0] 无 b64_json 也无 url: {json.dumps(item)[:300]}")

    return item


def _backoff_seconds(attempt: int) -> float:
    """指数退避封顶 60s：1, 2, 4, 8, 16, 32, 60, 60, ..."""
    return min(2 ** (attempt - 1), 60)


def generate(
    prompt: str,
    output: str,
    size: str = "1024x1536",
    model: str | None = None,
    timeout: int = 360,
    max_retries: int = 10,
) -> dict:
    """生成单张图片，自动重试。返回 {path, cost_cny, elapsed_s, model, size, attempts}"""
    base = _resolve_base_url()
    model = model or os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-2")
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("缺少 OPENAI_API_KEY。请编辑 ~/.claude-image-pro/.env")

    t0 = time.time()
    item = None
    last_err: Exception | None = None

    for attempt in range(1, max_retries + 1):
        try:
            print(
                f"   尝试 {attempt}/{max_retries} → POST {base}/v1/images/generations",
                file=sys.stderr,
            )
            item = _attempt_once(base, key, model, prompt, size, timeout)
            break
        except FatalError as e:
            # 不可恢复，立刻 raise
            raise RuntimeError(f"❌ 永久错误（不重试）: {e}") from e
        except RetryableError as e:
            last_err = e
            if attempt == max_retries:
                break
            wait = _backoff_seconds(attempt)
            print(
                f"   ⚠ 第 {attempt} 次失败: {e}\n"
                f"     {wait:.0f}s 后重试...",
                file=sys.stderr,
            )
            time.sleep(wait)

    if item is None:
        raise RuntimeError(
            f"❌ 重试 {max_retries} 次均失败。最后一次错误: {last_err}"
        )

    # 保存图片
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if item.get("b64_json"):
        output_path.write_bytes(base64.b64decode(item["b64_json"]))
    else:
        # url 方式（同样要重试下载）
        for attempt in range(1, 4):
            try:
                img_resp = requests.get(item["url"], timeout=60)
                img_resp.raise_for_status()
                output_path.write_bytes(img_resp.content)
                break
            except Exception as e:
                if attempt == 3:
                    raise RuntimeError(f"下载图片失败: {e}") from e
                time.sleep(2 * attempt)

    elapsed = time.time() - t0
    return {
        "path": str(output_path),
        "cost_cny": estimate_cost_cny(size),
        "elapsed_s": round(elapsed, 1),
        "model": model,
        "size": size,
        "attempts": attempt,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="claude-image-pro 出图引擎")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--prompt", "-p", help="提示词文本")
    src.add_argument("--prompt-file", help="从文件读提示词")
    ap.add_argument("--output", "-o", required=True, help="输出 PNG 路径")
    ap.add_argument("--size", default="1024x1536", help="尺寸，默认 1024x1536（9:16 抖音）")
    ap.add_argument("--model", help="覆盖模型（默认 env OPENAI_IMAGE_MODEL 或 gpt-image-2）")
    ap.add_argument("--json", action="store_true", help="输出 JSON 结果")
    args = ap.parse_args()

    # 加载用户配置
    load_env_file(Path.home() / ".claude-image-pro" / ".env")

    if args.prompt_file:
        prompt = Path(args.prompt_file).read_text(encoding="utf-8").strip()
    else:
        prompt = args.prompt

    try:
        result = generate(
            prompt=prompt,
            output=args.output,
            size=args.size,
            model=args.model,
        )
    except Exception as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(
            f"✅ 出图成功 → {result['path']}\n"
            f"   model={result['model']} size={result['size']} "
            f"耗时 {result['elapsed_s']}s 估算成本 ¥{result['cost_cny']} "
            f"尝试 {result.get('attempts', 1)} 次"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
