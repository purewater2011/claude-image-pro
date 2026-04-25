# claude-image-pro

> 让 Claude Code 在终端里输入一句中文，自动展开成两百字专业提示词，调 GPT Image 2 出可商用图。

```
你输入：    画一张抖音热搜榜，第一名 Claude 账号死了
工具自动：  展开成 200+ 字结构化 prompt（指定字号 / hex 配色 / UI 元素 / 虚构内容）
GPT Image 2: 3 秒出图  ¥0.78
```

—— **本仓库的 Day14 演示封面就是它直播生成的。**

---

## 为什么做这个

GPT Image 2（2026-04-22 全量上线）号称 99% 中文文字渲染、Image Arena 历史最大领先 242 分。但实测发现：**模型再强，普通用户喂的简单 prompt 还是出垃圾图**——必须经过结构化优化才能榨出 99%。

社区已有的 [`baoyu-imagine`](https://github.com/JimLiu/baoyu-skills) 把"出图引擎"做得很完备（10+ provider，支持 batch、参考图、多模态），但**没做 prompt 自动优化层**。这就是 claude-image-pro 的差异化定位。

| 维度 | baoyu-imagine | claude-image-pro |
|---|---|---|
| 出图引擎 | ✅ 10+ provider | ⚠️ 仅 OpenAI 兼容（够用） |
| Batch / 参考图 | ✅ | ❌（v1 不做） |
| **Prompt 自动优化层** | ❌ | ✅ **核心卖点** |
| **5 大中文场景模板** | ❌ | ✅ |
| **A/B 对比模式** | ❌ | ✅ |

我们不抢 baoyu-imagine 的活——它是出图引擎，我们是它前面的提示词工程师。

---

## 核心特性

- 🎯 **一句话出图**：中文输入 → 自动 200+ 字结构化 prompt → 出图
- 🎨 **5 大中文场景模板**：抖音 UI / 微博 / 小红书 / 海报 / X 推文
- ⚖️ **A/B 对比模式**：同一句话跑两次（未优化 vs skill 优化），看清差距
- 📐 **9:16 抖音预设**：默认竖屏 1024×1536，社媒博主友好
- 🔌 **任意 OpenAI 兼容接口**：官方 / 自建中转站 / 第三方网关都行
- 🪶 **零额外 LLM 成本**：优化层用 Claude Code 主进程做，不调外部 API
- 🧩 **Claude Code Skill 原生**：`/image 画一张...` 即可触发

---

## 安装（3 步）

### 1. 克隆仓库

```bash
git clone https://github.com/<your-handle>/claude-image-pro.git
cd claude-image-pro
```

### 2. 准备配置

```bash
mkdir -p ~/.claude-image-pro
cp .env.example ~/.claude-image-pro/.env
# 编辑填入你的 API key 和 base url
```

### 3. 注册成 Claude Code Skill

把仓库根目录链接到 Claude Code 的 skills 目录：

```bash
# macOS / Linux
ln -s "$(pwd)" ~/.claude/skills/claude-image-pro
```

或者 Claude Code plugin 形式（v0.2 计划支持）。

### 依赖

- Python 3.10+
- `requests`（HTTP 调用）
- `Pillow`（A/B 对比拼图，可选）

```bash
pip3 install requests pillow
```

---

## 配置 OpenAI 兼容接口

claude-image-pro 通过 OpenAI 协议调 gpt-image-2，**任何支持 `/v1/images/generations` 的服务都能跑**。

### 推荐使用作者自建中转站

> **[填你的中转站名]** — 直连官方反代，gpt-image-2 day-1 接入，失败不计费。

接入步骤：

1. 注册：[**填你的中转站注册地址**]
2. 充值：建议先充 ¥10 测试
3. 创建 API Key → 复制
4. 编辑 `~/.claude-image-pro/.env`：
   ```
   OPENAI_API_KEY=sk-xxx
   OPENAI_BASE_URL=https://[填你的中转站域名]/v1
   OPENAI_IMAGE_MODEL=gpt-image-2
   ```
5. 测试：
   ```bash
   python3 scripts/main.py "测试一张图" --output /tmp/test.png
   ```

### 用其他中转站？

把 `OPENAI_BASE_URL` 换成对应域名即可。常见错误码：

| HTTP 状态 | 含义 | 解决 |
|---|---|---|
| 401 | API key 无效 | 检查 key 是否粘对 |
| 404 | 模型不存在 | 中转站可能没接入 gpt-image-2，咨询客服 |
| 429 | 限速 | 等几秒重试，或升级套餐 |
| 500-503 | 中转站抖动 | 换时段或换中转站 |

---

## 用法

### 在 Claude Code 里（推荐）

```
你: /image 画一张抖音热搜榜，第一名 Claude 账号死了
Claude: [按 SKILL.md 4 步流程执行]
        - Step 1: 检查配置 ✓
        - Step 2: 调 enhancer 准备 request
        - Step 3: 读模板 + 用户输入，展开成 250 字 prompt
        - Step 4: 调 generator 出图
        ✅ → ./out.png  (3.2s · ¥1.20 · gpt-image-2)
```

### 在 shell 手动跑

```bash
# 模式 1: 直接出图（无优化，最快）
python3 scripts/main.py "a red apple" --output apple.png

# 模式 2: 走优化流程（先准备 request，让 Claude 完成）
python3 scripts/main.py "画一张抖音热搜榜" --enhance --output cover.png

# 模式 3: 用已优化的 prompt 文件
python3 scripts/main.py --prompt-file enhanced.txt --output cover.png

# 模式 4: A/B 对比（需要两个已生成的图）
python3 scripts/ab_compare.py --raw raw.png --enhanced enhanced.png --output compare.png
```

---

## 模板库（v0.1）

| 模板 | 子场景 | 状态 |
|---|---|---|
| `douyin_ui.md` | 热搜榜 / 视频封面 / 评论区 / 直播间 / 个人主页 | ✅ |
| `weibo_ui.md` | 推文 / 热搜 / 评论区 | ⏳ v0.2 |
| `xiaohongshu_ui.md` | 笔记封面 / 笔记正文 / 评论区 | ⏳ v0.2 |
| `poster.md` | 苹果极简 / Supreme 潮牌 / 国潮潮玩 / 科技发布会 | ⏳ v0.2 |
| `x_tweet.md` | 推文截图 / 个人主页 | ⏳ v0.2 |

每个模板包含：优化指令 / 字段填充清单 / 200+ 字 prompt 模板 / 5 个原始→优化对照示例 / 反例。

---

## 路线图

- ✅ v0.1: Day14 抖音上线（核心引擎 + douyin_ui 模板 + A/B 对比）
- ⏳ v0.2: 5 大场景模板补全（微博 / 小红书 / 海报 / X 推文）
- ⏳ v0.3: 通用增强模板（未匹配场景的兜底）
- ⏳ v0.4: 多图一致性 batch 模式（GPT Image 2 一次出 8 张）
- ⏳ v0.5: 模板社区贡献机制 + 模板评分

---

## 致谢

- [JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills) — 出图引擎参考架构
- [EvoLinkAI/awesome-gpt-image-2-prompts](https://github.com/EvoLinkAI/awesome-gpt-image-2-prompts) — 模板灵感
- OpenAI gpt-image-2 — 99% 中文文字渲染让这一切成为可能

---

## License

MIT — 见 [LICENSE](./LICENSE)

---

## 反馈 & 贡献

提 Issue 或 PR 都欢迎。模板贡献优先合入。
