---
name: claude-image-pro
description: |
  Let Claude Code call GPT Image 2 from the terminal. One short Chinese sentence in,
  auto-expand to a 200+ char structured prompt, and get a publishable image out.
  Covers 5 high-frequency Chinese scenarios: Douyin UI / Weibo / Xiaohongshu / poster /
  X tweet. Defaults to 9:16 vertical 2K for short-video platforms.
  Use when user says "画图" "画一张" "生成图片" "/image" "出张图" "做封面".
version: 0.1.0
triggers:
  - 画图
  - 画一张
  - 生成图片
  - /image
  - 出张图
  - 做封面
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
---

# claude-image-pro

让 Claude Code 在终端调 GPT Image 2 出可商用图。**核心差异化：自动 prompt 优化层**——用户输入一句中文，工具自动展开成 200+ 字结构化 prompt，再调 gpt-image-2 出图。

> **架构关键**：所有 LLM 优化工作都由你（Claude 主进程）完成——不调外部 API，零额外成本。Python 脚本只做 deterministic 工作（路由模板、组装 request、调出图接口）。

---

## 工作流（4 步严格按顺序执行）

### Step 1: 加载配置 ⛔ BLOCKING

**绝对前置：必须检查 `~/.claude-image-pro/.env` 存在且关键变量齐全。否则停止流程引导用户配置。**

用 Bash 跑：

```bash
ENV_FILE="$HOME/.claude-image-pro/.env"
if [ ! -f "$ENV_FILE" ]; then
  echo "MISSING_ENV"
else
  # 加载并检查关键变量
  set -a; source "$ENV_FILE"; set +a
  for var in OPENAI_API_KEY OPENAI_BASE_URL OPENAI_IMAGE_MODEL; do
    if [ -z "${!var}" ]; then
      echo "MISSING_VAR: $var"
    fi
  done
fi
```

- 若输出 `MISSING_ENV` → 提示用户：「请先 `mkdir -p ~/.claude-image-pro && cp <SKILL_DIR>/.env.example ~/.claude-image-pro/.env`，然后编辑填入 API key」并停止。
- 若输出 `MISSING_VAR: xxx` → 提示用户补该变量。
- 三个变量齐全 → 继续 Step 2。

`SKILL_DIR` 是本 SKILL.md 所在的目录（仓库根）。

---

### Step 2: 调用 enhancer 准备 request

用户说什么去画，把那句话原文存成 `USER_INPUT` 变量。然后跑：

```bash
USER_INPUT="<用户的原话>"
TIMESTAMP=$(python3 -c 'import time; print(int(time.time()*1000))')
ENHANCED_PATH="/tmp/cip_enhanced_${TIMESTAMP}.txt"

python3 "$SKILL_DIR/scripts/enhancer.py" "$USER_INPUT" --output "$ENHANCED_PATH"
```

enhancer 会做这些事：
- 用关键词路由匹配 `templates/` 下的模板（抖音/微博/小红书/海报/X 推文）
- 把"用户输入 + 模板内容 + 给你的指令"组装成一份 markdown
- 写到 `/tmp/cip_request_<TIMESTAMP>.md`
- 标准输出会显示 request 路径和命中的模板

**记下 request 路径**——它会在脚本输出的第一行，格式是 `✅ Request 已写入: /tmp/cip_request_xxx.md`。

---

### Step 3: 你（Claude 主进程）读 request 并展开 prompt

**这是核心智能步骤。**

1. 用 Read 工具读 Step 2 拿到的 `cip_request_<TIMESTAMP>.md`
2. 严格按 request 里「模板内容」的「优化指令」+「字段填充清单」+「Prompt 模板」展开：
   - 把用户原始输入里的关键信息填入模板的 `{placeholder}`
   - 虚构其他必要字段（账号名/数字/列表内容），合理且明显是演示用
   - 中文文字内容用 `「」` 括起来
   - 配色用 hex 值（不要只说颜色名）
   - 字号层级清晰
3. 输出 200-350 字英文+中文混合 prompt
4. **不要输出多余解释**，只写 prompt 本身
5. 用 Write 工具写到 `/tmp/cip_enhanced_<TIMESTAMP>.txt`（路径在 request md 末尾标明）

### Step 4: 调 generator 出图

```bash
OUTPUT_PATH="${OUTPUT_PATH:-./out.png}"
SIZE="${SIZE:-1024x1536}"  # 9:16 抖音默认；用户指定其他比例时换

python3 "$SKILL_DIR/scripts/generator.py" \
  --prompt-file "$ENHANCED_PATH" \
  --output "$OUTPUT_PATH" \
  --size "$SIZE"
```

成功输出格式：
```
✅ 出图成功 → ./out.png
   model=gpt-image-2 size=1024x1536 耗时 3.2s 估算成本 ¥1.20
```

把这条结果（含路径、耗时、成本）展示给用户。

---

## A/B 对比模式（演示 skill 价值用）

用户在输入里包含 "对比" / "/image-ab" / "ab模式" 时，跑两次出图：

1. **Raw 路径**：跳过 Step 2/3，直接把用户输入当 prompt 喂 generator
   ```bash
   python3 "$SKILL_DIR/scripts/generator.py" \
     -p "$USER_INPUT" \
     --output "/tmp/ab/raw.png" --size "1024x1536"
   ```

2. **Enhanced 路径**：完整跑 Step 2/3/4
   ```bash
   # ... Step 2/3 同上 ...
   python3 "$SKILL_DIR/scripts/generator.py" \
     --prompt-file "$ENHANCED_PATH" \
     --output "/tmp/ab/enhanced.png" --size "1024x1536"
   ```

3. **拼图**：用 ab_compare.py 把两张图左右拼成对比图
   ```bash
   python3 "$SKILL_DIR/scripts/ab_compare.py" \
     --raw "/tmp/ab/raw.png" \
     --enhanced "/tmp/ab/enhanced.png" \
     --output "/tmp/ab/compare.png"
   ```

向用户展示三张图（raw / enhanced / compare），重点呈现 enhanced 远优于 raw。

---

## 用法示例

```
用户: /image 画一张抖音热搜榜，第一名 Claude 账号死了
你:   [按 Step 1-4 执行，最终交付 out.png]

用户: /image 做一张科技海报，主题"GPT Image 2 上线" 输出到 day14-cover.png
你:   [Step 4 把 OUTPUT_PATH 设成 day14-cover.png]

用户: /image-ab 画一张小红书笔记，标题"我用AI画图月入5000"
你:   [跑 A/B 对比模式]
```

---

## 错误处理

- **API 返回 4xx/5xx**：检查 `OPENAI_BASE_URL` 是否带 `/v1` 后缀（generator.py 会自动去掉，但若仍 4xx 提示用户检查 key 余额）
- **enhancer 没命中模板**：走通用增强（GENERIC_INSTRUCTION），按通用规则展开
- **Step 3 写文件失败**：检查 `/tmp` 写权限
- **生成的图明显错乱**：建议用户提供更具体的输入（如"抖音热搜榜"代替"画个图")

---

## 配置项参考

`~/.claude-image-pro/.env` 必填：

| 变量 | 说明 | 示例 |
|---|---|---|
| `OPENAI_API_KEY` | OpenAI 兼容接口的 key | `sk-xxx` |
| `OPENAI_BASE_URL` | OpenAI 兼容接口的 base url | `https://your-gateway.com/v1` |
| `OPENAI_IMAGE_MODEL` | 出图模型名 | `gpt-image-2` |

任意支持 OpenAI 协议的中转站都可以跑。详见 README 的「中转站接入」章节。

---

## 不要做的事

- ❌ 不要跳过 Step 1 直接出图（会因配置缺失炸）
- ❌ 不要跳过 Step 2/3 直接把用户输入喂 generator（除非用户明确说"raw 模式"或 ab 模式的 raw 路径）
- ❌ 不要在 Step 3 输出除 prompt 之外的解释文字（generator 会把整个文件当 prompt 读）
- ❌ 不要仿真任何真实账号 / 真实平台 logo / 真实公众人物——所有出现的用户名、头像、热搜内容必须虚构
- ❌ 不要忘记 9:16 默认（`1024x1536`）——用户没指定其他比例时不要切横屏
