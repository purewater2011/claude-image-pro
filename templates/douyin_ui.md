# 抖音 UI 截图 提示词优化模板

> 适用场景：抖音热搜榜 / 视频封面 / 评论区 / 直播间画面 / 个人主页

---

## 优化指令（Claude 主进程读这段）

你是 GPT Image 2 的提示词工程师。读完本文件后，把用户的简单输入展开成一条 200-350 字的结构化英文+中文混合 prompt，交给 generator.py 出图。

### 必须遵守的硬规则

1. **禁止仿真任何真实账号、真实主体、真实事件**——所有出现的用户名、头像、热搜内容必须虚构，且明显是"演示用"
2. **禁止使用真实平台 logo 或真实品牌商标**——可以画"抖音风格 UI"但不画真实抖音 logo（用通用音符或 D 字母替代）
3. **9:16 竖屏（1024×1536）必选**，除非用户在输入中明确指定其他比例
4. **中文文字内容必须用中文双引号「」括起来**，让 GPT Image 2 知道这是要精确渲染的字符
5. **指定字号层级**（主标题 / 副标题 / 正文 / 辅助文字 4 级）
6. **指定配色 hex 值**（不要只说"红色"，说 `#FF2D55`）

### 必须包含的视觉元素（按子场景）

| 子场景关键词 | 必含元素 |
|---|---|
| 热搜榜 / 热点榜 | 状态栏 + 顶部标题区"热点榜" + 10 条列表（编号 1-10）+ 底部导航栏 |
| 视频封面 | 大字标题 + 主体图 + 底部账号栏 + 点赞数 + 评论数 + 分享数 |
| 评论区 | 视频缩略图 + 评论输入框 + 5-8 条评论（含头像/昵称/时间/点赞数） |
| 直播间 | 主播画面 + 礼物特效 + 弹幕 + 底部礼物栏 + 在线人数 |
| 个人主页 | 头像 + 昵称 + 简介 + 关注/粉丝数 + 9 宫格作品 |

### 子场景路由（按用户输入关键词）

- 包含"热搜""热点""榜单" → 热搜榜子模板
- 包含"封面""标题图" → 视频封面子模板
- 包含"评论" → 评论区子模板
- 包含"直播" → 直播间子模板
- 包含"主页""个人页" → 个人主页子模板
- 都不命中 → 默认热搜榜

---

## 字段填充清单（共通）

每次填这 7 个字段，缺哪个用括号里的默认值：

1. **subject_text**（用户输入提取的核心主题文字）
2. **scene_type**（热搜榜 / 封面 / 评论区 / 直播间 / 主页，按上面路由）
3. **mood**（爽 / 严肃 / 反转 / 神秘，按 subject 推断；默认"爽"）
4. **author_handle**（虚构账号名，"@演示账号" 或行业相关昵称如 "@AI实验室"）
5. **timestamp**（虚构时间，"刚刚" / "3 分钟前" / "1 小时前"）
6. **engagement_data**（点赞 / 评论 / 转发数，虚构合理量级，如"328 万 / 12.6 万 / 8.7 万"）
7. **bg_style**（白底浅色 / 深色模式 / 渐变背景，按 mood 推断）

---

## 子模板 1: 热搜榜（Day14 主演示）

### Prompt 模板

```
A vertical 9:16 mobile screenshot mockup, 1024×1536, in the style of a Chinese 
short-video app trending list page (NOT real Douyin logo, use a generic music-note 
icon in top-left corner instead).

Layout, top to bottom:

1. Status bar (h≈50px): time "20:14", signal/wifi/battery icons (3 dots, fan, 100%)
2. Header (h≈100px): centered Chinese title 「热点榜」(font 36pt bold black #1A1A1A), 
   sub-title 「实时更新 · 每 5 分钟刷新」(font 14pt gray #999), search icon top-right
3. Trending list (h≈1100px): 10 rows, each row 100px tall, separated by 1px #F0F0F0 line
   Row format:
   - Left: large rank number (32pt bold)
     · Rank 1 in red #FF2D55
     · Rank 2 in orange #FF9500
     · Rank 3 in yellow #FFCC00
     · Rank 4-10 in gray #999
   - Center: title text (16pt #1A1A1A, max 22 chinese chars per line, can wrap to 2 lines)
   - Right: badge tag (round pill) — rank 1 has red 「爆」 badge, rank 2-3 「沸」, 
     rank 4-6 「热」, rank 7-10 no badge
   - Below title: heat value in gray (12pt) "热度 XXXX万"
4. Bottom nav (h≈80px): 5 icons evenly spaced — house「首页」, friends「朋友」, 
   center plus button (red circle), inbox「消息」, profile「我」

Trending list content (rank 1 = user-provided subject, rank 2-10 = plausibly fabricated 
NON-REAL trending topics that fit a tech-savvy 30-something male audience):

  1. 「{subject_text}」  · 热度 {generated_heat}万  · 「爆」
  2. 「{plausible_tech_topic_1}」 · 热度 {decreasing_heat}万 · 「沸」
  3. 「{plausible_tech_topic_2}」 · 热度 {decreasing_heat}万 · 「沸」
  4. 「{plausible_lifestyle_1}」 · 热度 {decreasing_heat}万 · 「热」
  5. 「{plausible_entertainment_1}」 · 热度 {decreasing_heat}万 · 「热」
  6. 「{plausible_tech_topic_3}」 · 热度 {decreasing_heat}万 · 「热」
  7. 「{plausible_random_topic_1}」 · 热度 {decreasing_heat}万
  8. 「{plausible_random_topic_2}」 · 热度 {decreasing_heat}万
  9. 「{plausible_random_topic_3}」 · 热度 {decreasing_heat}万
  10. 「{plausible_random_topic_4}」 · 热度 {decreasing_heat}万

Style: clean iOS-style mobile UI, white background, sharp pixel-perfect Chinese 
character rendering, no AI smoothness. Lighting flat. No texture, no shadow under 
text. Reference: feels like a phone screenshot uploaded to social media.
```

### 填充示例（完整版）

**用户输入：** `画一张抖音热搜榜，第一名 Claude 账号死了`

**优化后 prompt（200+ 字版本）：**

```
A vertical 9:16 mobile screenshot mockup, 1024×1536, in the style of a Chinese 
short-video app trending list. NOT real Douyin logo — use a generic music-note 
icon top-left.

Status bar: "20:14", signal/wifi/100% battery icons.
Header: bold black 「热点榜」(36pt), gray sub-title 「实时更新 · 每 5 分钟刷新」(14pt), 
search icon top-right.

Trending list (10 rows, 100px each, white #FFFFFF background):
  1. 「Claude 账号死了」 ·  热度 982 万 · red pill badge 「爆」
  2. 「OpenAI 又发新模型」 · 热度 765 万 · orange pill 「沸」
  3. 「程序员副业接单指南」 · 热度 654 万 · orange pill 「沸」
  4. 「30 岁转行 AI 来得及吗」 · 热度 543 万 · red pill 「热」
  5. 「独立开发月入十万」 · 热度 421 万 · red pill 「热」
  6. 「GitHub 年度报告出炉」 · 热度 387 万 · red pill 「热」
  7. 「VS Code 又出新功能」 · 热度 298 万
  8. 「机械键盘选购避坑」 · 热度 254 万
  9. 「打工人续命神器」 · 热度 198 万
  10. 「AI 帮我写周报真香」 · 热度 165 万

Rank colors: 1=red #FF2D55, 2=orange #FF9500, 3=yellow #FFCC00, 4-10=gray #999.
Bottom nav: 5 evenly-spaced icons — 「首页」「朋友」 [red plus] 「消息」「我」.

Style: clean iOS mobile UI, sharp pixel-perfect Chinese rendering, flat lighting, 
no AI smoothness, looks like a real phone screenshot. White background.
```

### 反例（这些 prompt 容易出垃圾图）

❌ **太抽象：** "画一张抖音热搜榜显示 Claude 死了"
   → 缺少 UI 细节描述，GPT Image 2 会乱排版，文字可能糊
   
❌ **指定真实 logo：** "画一张抖音 APP 截图带抖音 logo"
   → 法律风险 + 平台限流；用"音符图标"替代

❌ **太多英文混入：** "Generate a Douyin hot search showing Claude died"
   → 99% 中文渲染优势用不上，文字可能出英文乱码

❌ **没指定字号：** 只说"标题字大"
   → 排版会失控，第一名字号可能跟第十名一样大

❌ **省略色值：** "颜色用红色橙色黄色"
   → 出来的红可能是粉色或砖红色，要给 hex 才稳

---

## 子模板 2: 视频封面

### Prompt 模板

```
A vertical 9:16 short-video cover mockup, 1024×1536.

Layout:
- Top 60%: main visual related to {subject_text} (illustration or photo style per mood)
- Below visual: HUGE bold Chinese title overlay 「{subject_text}」 
  (font 80pt, color {high_contrast_color}, with thick black outline 4px for legibility)
- Optional sub-headline below title (font 36pt {accent_color})
- Bottom 15%: account bar — circular avatar (generic stylized portrait, no real person), 
  username 「{author_handle}」, follow button
- Right edge floating column: heart icon + 「{like_count}万」, comment + 「{comment_count}万」, 
  share + 「{share_count}」

Avoid: real platform logos, real celebrity faces, real trademarks.
Style: high contrast, clickbait energy, sharp Chinese typography.
```

---

## 子模板 3: 评论区

### Prompt 模板

```
A vertical 9:16 mobile comment section mockup, 1024×1536.

Layout:
- Top: video thumbnail (200px tall) with title overlay 「{video_title}」
- Header: 「评论 {comment_total}」(bold 24pt)
- 5-8 comment cards, each:
  · Circular avatar 40px (generic portrait, varied styles)
  · Username 「{varied_handle}」(14pt #1A1A1A bold) + 「{timestamp}」(12pt #999)
  · Comment body (16pt #1A1A1A, max 3 lines)
  · Heart icon + count, reply button
- Bottom: comment input 「说点什么...」 with emoji icon

All usernames and comment content fabricated, varied tones (positive / skeptical / funny).
```

---

## 子模板 4: 直播间画面（已强化 · 参考 UI Case 7 + 36）

### 子场景路由

- 包含"持牌""手举牌""手持牌"→ 持牌互动型直播
- 包含"礼物""特效""刷礼物" → 礼物特效型直播
- 都不命中 → 通用直播子模板（带轻量礼物特效）

### Prompt 模板（通用，核心）

```
A 9:16 vertical 1024×1536 high-detail realistic Chinese short-video 
livestream screenshot. NOT real Douyin/TikTok logo — use generic music-note 
icon top-left, app label appears as text 「直播」.

STREAMER SUBJECT:
{streamer_description — generic stylized face NOT a real public figure}, 
{age} {gender}, {expression} expression, {pose}, looking at the phone 
camera, {emotion_word} energy.

OPTIONAL HAND-HELD SIGN (when subject holds a sign):
The streamer holds a {sign_color} handwritten sign in one hand, clearly 
showing the text 「{sign_text_chinese}」 in 36pt bold marker handwriting.

LIVESTREAM ROOM ENVIRONMENT:
Professional livestream setup visible — phone tripod, ring light, desktop 
microphone, modern tech-lit background with {background_color_palette} 
neon ambience. Soft warm key light on streamer face.

UI ELEMENTS (overlaid, semi-transparent or solid):
- Top-left: red pulsing pill 「直播中 · {viewer_count}人观看」 in 14pt white
- Top-right: close × button + share ↗ icon
- Top-center: stream title 「{stream_title_chinese}」 in 16pt white outlined
- Right-edge floating column (vertical icons, 60px spacing):
  · Heart ❤ + 「{like_count}」
  · Comment 💬 + 「{comment_count}」
  · Share ↗ + 「{share_count}」
  · Gift 🎁 (gold accent)
- Bottom-left: streamer info pill — circular avatar 50px + 
  username 「{streamer_handle_chinese}」 + 「关注」 red button
- Below info: 5-7 scrolling Chinese bullet comments stacked, each:
  · Small avatar 30px + username 「@{viewer_handle}」 in 13pt
  · Comment 「{comment_chinese}」 in 14pt white on dark semi-bg

OPTIONAL GIFT EFFECT (when "礼物" or "特效" requested):
Eye-catching floating gift animation in center-screen — banner reads 
「{viewer_handle} 送出 {gift_name_chinese}」, with sparkle particles, 
golden glow, platform-style notification box at top of frame.

STYLE: photorealistic livestream feel, real natural skin texture (visible 
pores, NO plastic), warm bright lighting, modern tech depth-of-field, 
HD detail, cinematic. UI looks native to Douyin platform.

NEGATIVE: low definition, blur, cartoon, illustration, real celebrity 
face, real Douyin logo, AI smoothness, plastic skin, static lifeless eyes.
```

### 示例 1: 持牌互动直播

**用户输入**：`生成一张抖音直播截图，主播手持牌子写"今晚 8 点开播"`
**填充**：streamer=亚洲女性 25 岁干净马尾 generic 面孔, expression=灿烂笑容 excited, sign=「今晚 8 点 · AI 副业揭秘」, viewer=12.3万, stream_title=「30 岁副业转型分享」, handle=「副业老司机」, like=8.6万, comment=2.1万

### 示例 2: 礼物特效直播

**用户输入**：`生成抖音直播刷礼物特效截图`
**填充**：streamer=亚洲男性 30 岁短发眼镜程序员 generic, expression=惊喜半张嘴 surprised, gift_name=「火箭」, viewer_handle=「@代码诗人 233」, viewer=8.7万, like=15.2万

### 示例 3: 名人风格演示直播（meta 风）

**用户输入**：`生成抖音直播截图，硅谷大佬风格主播展示新发布的代码`
**填充**：streamer=西方面孔 40 岁短发科技 founder generic, expression=认真讲解 focused, stream_title=「亲自演示：我的新 AI 工具」, viewer=23.5万, like=42.8万, 注意：禁止用真名 Elon Musk / Sam Altman, 用"硅谷创始人 generic"

---

---

## 子模板 5: 个人主页

### Prompt 模板

```
A vertical 9:16 profile page mockup, 1024×1536.

Layout:
- Top 30%: header banner background (gradient or pattern)
- Avatar (circular 100px) overlapping bottom of banner
- Below avatar: username 「{author_handle}」(24pt bold), bio 「{bio_text}」(14pt #666)
- 3-column stats row: 「关注 {following_count}」「粉丝 {follower_count}」「获赞 {like_total}」
- Tab bar: 「作品」「私密」「喜欢」(works tab active)
- Below: 3×3 grid of video thumbnails, each with:
  · Thumbnail image
  · Bottom-left play count 「{play_count}」
  · Top-right indicator if pinned

All content fabricated. Style: clean app UI, sharp text rendering.
```

---

## 通用增强技巧（所有子模板都用）

1. **字号建议**（1024×1536 画布上的视觉字号）：
   - 主标题 / Hero：60-90pt
   - 章节标题：30-40pt
   - 正文：14-18pt
   - 辅助文字（时间/数字）：10-14pt

2. **配色避坑** — 优先用这些已验证 hex：
   - 警示红 `#FF2D55`
   - 强调橙 `#FF9500`
   - 可读黑 `#1A1A1A`（不用纯黑 `#000`，太刺眼）
   - 辅助灰 `#999999`
   - 浅分割线 `#F0F0F0`
   - 白底 `#FFFFFF`

3. **强制清晰中文渲染** — prompt 末尾加上：
   > "sharp pixel-perfect Chinese character rendering, no AI smoothness, looks like 
   > a real phone screenshot, NOT a stylized illustration"

4. **防止生成真人脸** — 头像位置加：
   > "generic stylized portrait icon (geometric or cartoon style), NOT a realistic face"
