# 多平台社媒截图 提示词优化模板

> 适用场景：视频号 / 小红书 / 快手 / 微博 / 微信 / 知乎 / X 推文 — 抖音见 douyin_ui.md
> 核心要求：UI 高仿真但合规（不画真实平台 logo）、99% 中文文字渲染

---

## 优化指令（Claude 主进程读这段）

读完本文件后，把用户的简单输入展开成 250-400 字的英文+中文混合 prompt。

### 必须遵守的硬规则

1. **9:16 竖屏 1024×1536**（手机截图标准比例），除非用户明确指定其他
2. **不画真实平台 logo**：用通用图标（音符 / 心形 / 信封 / 飞机）替代
3. **平台用文字标识**：APP 名直接以中文文字出现 「视频号」「小红书」「快手」等
4. **所有用户名 / 头像 / 内容必须虚构**，明显演示用
5. **状态栏一致**：iPhone 风格状态栏（时间 / 信号 / wifi / 100% 电池）
6. **中文文字用「」**括起来精确渲染

### 子场景路由

- 包含"视频号""微信视频" → 视频号子模板
- 包含"小红书""xhs""小红薯" → 小红书子模板
- 包含"快手" → 快手子模板
- 包含"微博""weibo""热搜" → 微博子模板
- 包含"X""推特""tweet" → X 推文子模板
- 包含"微信""朋友圈""聊天" → 微信子模板
- 包含"知乎""高赞回答" → 知乎子模板
- 都不命中 → 提示用户具体平台

---

## 子模板 1: 视频号截图

### Prompt 模板

```
A 9:16 vertical mobile screenshot mockup, 1024×1536, of a Chinese 
short-video platform similar to WeChat Video. NOT real WeChat logo — 
use a generic green camera icon. App label appears as 「视频号」.

LAYOUT:
- Status bar (50px): time "20:14", signal/wifi/battery icons.
- Top header (70px): centered title 「视频号」 in 18pt bold black, 
  small back arrow ← top-left, dot menu ⋮ top-right.
- Main video area (top 65% of remaining): full-width video thumbnail of 
  {scene_description}, with white video title overlay 「{video_title_chinese}」 
  bottom-left in 24pt bold with thick black outline.
- Below video: account row (60px tall):
  · Circular avatar 50px (generic stylized portrait icon)
  · Username 「{handle_chinese}」 18pt bold
  · 「关注」 button right-side, green pill
- Engagement strip (50px): like/comment/share/forward icons with counts
  「赞 {like_count}」「评论 {comment_count}」「转发 {share_count}」
- Recommended tags row: 3-4 hashtag pills 「#{tag1}」「#{tag2}」「#{tag3}」
- Bottom 100px: comment input bar 「写评论...」 + emoji icon

COLOR: dominant white #FFFFFF + WeChat green #07C160 accents.

STYLE: clean WeChat-family iOS UI, sharp pixel-perfect Chinese rendering, 
flat design, NO AI smoothness.
```

### 示例

**用户输入**：`生成视频号内容截图，主题：中老年不要盲目催婚`
**填充**：scene=家庭聚餐场景虚构插画, video_title=「父母催婚就是爱我吗？答案让人破防」, handle=「@温柔表达者」

---

## 子模板 2: 小红书笔记截图

### Prompt 模板

```
A 9:16 vertical mobile screenshot mockup, 1024×1536, of a Chinese 
lifestyle/notes platform similar to RED. NOT real Xiaohongshu logo — 
use a generic flame or book icon. App label appears as 「小红书」.

LAYOUT:
- Status bar (50px).
- Top header (60px): 「小红书」 brand text top-left in red #FF2D55 18pt bold, 
  search bar 「搜索灵感」 center, message icon top-right.
- Main note thumbnail (top 55%): square image of {visual_description}, 
  centered title overlay 「{note_title_chinese}」 in 28pt bold white with 
  shadow, on top of {bg_color} gradient.
- Below image: 2-line note title 「{note_title_chinese}」 18pt black bold.
- Author row (60px):
  · Circular avatar 40px
  · Username 「@{handle_chinese}」 14pt
  · 「{location_chinese}」 12pt gray
- Engagement bar: 心 {like_count}  收藏 {save_count}  💬 {comment_count}
- Tags row: 「#{tag1}」「#{tag2}」「#{tag3}」 in light pink pills #FFE5EC
- Bottom 150px: 2-3 comment previews with avatars
- Bottom nav (80px): 5 icons — 首页 / 购物 / + / 消息 / 我

COLOR: dominant white + Xiaohongshu red #FF2442 + pink accents.

STYLE: clean iOS lifestyle app UI, vibrant warm colors, sharp pixel-perfect 
Chinese rendering.
```

### 示例

**用户输入**：`生成小红书笔记，主题：精致女孩背后都有网贷`
**填充**：visual=粉色调办公桌 + 信用卡 + 化妆品 + 焦虑表情贴纸, title=「精致女孩背后都有网贷｜30 岁前的财务陷阱」, handle=「精致到破产」, tags=「#年轻人理财」「#避坑指南」「#月光族」

---

## 子模板 3: 快手内容截图

### Prompt 模板

```
A 9:16 vertical mobile screenshot mockup, 1024×1536, of a Chinese 
short-video platform similar to Kuaishou. NOT real Kuaishou logo — 
use a generic K letter icon. App label appears as 「快手」.

LAYOUT:
- Full-screen video background of {scene_description}, slightly desaturated 
  for UI overlay readability.
- Top status bar.
- Top tabs: 「关注」 「同城」 「精选」, 「同城」 in bold orange, others gray.
- Right-edge floating column (vertical):
  · Circular avatar 60px with red 「+」 follow indicator
  · ❤ {like_count}
  · 💬 {comment_count}
  · ↗ {share_count}
  · 🎵 rotating music disc
- Bottom-left text overlay (3-4 lines):
  · 「@{handle_chinese}」 in 16pt bold white
  · Video caption 「{caption_chinese}」 18pt white
  · Music label 「♪ {music_chinese}」 14pt
- Bottom nav: 5 icons — 首页 / 同城 / + / 消息 / 我
- For LIVE content: top-left red pill 「直播中 · {viewer_count}人观看」

COLOR: high contrast, dominant orange-red Kuaishou accents #FF5500.

STYLE: vibrant grassroots aesthetic, slightly chaotic, full-screen 
immersive video experience.
```

### 示例

**用户输入**：`生成快手直播离婚预告截图`
**填充**：scene=家庭客厅暖黄灯光下夫妻背对背, handle=「真实人间记录」, caption=「今晚 8 点直播 · 我们的故事告一段落」, viewer=12.3万

---

## 子模板 4: 微博截图

### Prompt 模板

```
A 9:16 vertical mobile screenshot mockup, 1024×1536, of a Chinese 
microblog platform similar to Weibo. NOT real Weibo eye logo — 
use a generic chat bubble icon. App label appears as 「微博」.

LAYOUT:
- Status bar.
- Top header (50px): 「微博」 text top-left, search top-center, +新建 top-right.
- Tabs row: 「关注」「热门」「同城」「视频」, 「热门」 active orange underline.
- Main feed: 1-2 weibo posts, each post:
  · Avatar 50px + 「@{handle_chinese}」 + verification 「V」 if applicable
  · Timestamp 「{time_chinese}」 + 「来自 {device_chinese}」
  · Post body 「{post_chinese}」 (16pt black, max 6 lines)
  · Optional 1 image preview or 9-grid thumbnail
  · Engagement: 转发 {repost_count}  评论 {comment_count}  ❤ {like_count}
- For TRENDING: top section shows 「热搜榜」 with rank list, each row:
  · Rank number (1-3 red, 4+ gray)
  · Trending topic 「{topic_chinese}」 with optional 「热」/「新」/「沸」 badge
  · Heat number 「{heat_count}」
- Bottom nav: 5 icons.

COLOR: white #FFFFFF + Weibo orange #FF8200 accents.

STYLE: information-dense, slightly older iOS UI feel.
```

### 示例

**用户输入**：`生成微博热搜截图，第一名 Claude 账号死了`
**填充**：参考 douyin_ui.md 热搜榜结构，调整为微博风格

---

## 子模板 5: X (Twitter) 推文截图

### Prompt 模板

```
A 9:16 vertical mobile screenshot mockup, 1024×1536, of X (Twitter), 
DARK MODE.

LAYOUT:
- Status bar (white text on black background).
- Top header (50px): X logo top-center (small geometric X), back arrow left.
- Main tweet card (centered, takes 60-70% of canvas):
  · Avatar 50px circular (generic, NOT real public figure)
  · Display name 「{name_english_or_chinese}」 17pt bold white + 
    optional blue verification ✓
  · @handle 14pt gray
  · Tweet body 「{tweet_text}」 23pt regular white, can include emoji and 
    line breaks
  · Optional embedded image
  · Timestamp + view count 「{time} · {view_count} Views」 13pt gray
- Engagement bar: 💬 {reply}  🔁 {repost}  ❤ {like}  📊 {bookmark}  ↗ {share}
- Below: top reply 「{reply_text}」 in slightly smaller card

COLOR: pitch black #000000 background + white text + Twitter blue 
#1D9BF0 + verified blue checkmark.

STYLE: official X iOS app UI, sharp text rendering, modern flat design, 
NO AI smoothness, NO real celebrity face.
```

### 示例

**用户输入**：`画一张X推文截图，匿名科技博主发"AGI已至"`
**填充**：display_name=「Anonymous Researcher」, handle=@anon_ai_2026, body=「going to bed. AGI is already here, we just haven't realized.」, reply=「it literally is」, like=82k, view=12M

---

## 子模板 6: 微信对话截图

### Prompt 模板

```
A 9:16 vertical mobile screenshot mockup, 1024×1536, of WeChat chat 
interface (1-on-1 conversation).

LAYOUT:
- Status bar.
- Top header (60px): centered name 「{contact_chinese}」 18pt bold black, 
  back arrow left, ⋮ menu right.
- Chat area (white #EDEDED background):
  · 6-10 message bubbles arranged chronologically
  · Friend's messages: gray bubble #FFFFFF, left-aligned, with avatar 40px
  · User's messages: green bubble #95EC69, right-aligned, with avatar
  · Each bubble: text in 16pt black, max 4 lines per bubble
  · Optional emoji or image preview
- Bottom input bar: 「{input_placeholder}」 + voice/+/emoji icons

CONTENT (chronological, must feel natural):
{6-10 message exchange between user and contact, building toward 
{punchline_or_climax_chinese}}

COLOR: WeChat signature green #07C160 + light gray bubble #FFFFFF + 
background #EDEDED.

STYLE: native WeChat iOS UI, sharp pixel-perfect Chinese rendering, 
NO real avatars, NO real names that match public figures.
```

### 示例

**用户输入**：`生成微信对话截图，老板让我加班的反差对话`
**填充**：contact=「@老板 大刘」, exchange=老板说"明天能加班吗"→我"可以呀加多少倍"→老板"没倍"→我"那不行"→老板已撤回, climax=对话戛然而止

---

## 子模板 7: 知乎高赞回答截图

### Prompt 模板

```
A 9:16 vertical mobile screenshot mockup, 1024×1536, of a Chinese Q&A 
platform similar to Zhihu. NOT real Zhihu logo — use a generic blue Z 
or chat icon. App label appears as 「知乎」.

LAYOUT:
- Status bar.
- Top header (50px): back arrow left, 「问题」 text center, 关注 + ⋮ right.
- Question card (top 25%):
  · Question title 「{question_chinese}」 in 22pt bold black
  · Stats bar: 关注 {follower_count} · 被浏览 {view_count}
- Top-voted answer (rest of canvas):
  · Author row: avatar + 「@{author_chinese}」 18pt bold + 
    「{credential_chinese}」 12pt gray (e.g., 「微软资深工程师」)
  · 「{vote_count} 人赞同了该回答」 14pt blue #0084FF
  · Answer body 「{answer_chinese}」 (16pt black, max 12 lines, 
    with paragraph breaks)
  · Optional inline image
  · Bottom of answer: 赞同 ▲ {like}  评论 {comment}  收藏  分享

COLOR: white #FFFFFF + Zhihu blue #0084FF + light gray dividers.

STYLE: clean reading-focused UI, slightly formal/professional aesthetic.
```

### 示例

**用户输入**：`生成知乎截图，问题：30岁转AI来得及吗，高赞回答`
**填充**：question=「30 岁转行 AI 还来得及吗？」, author=「@老张写代码」, credential=「前 BAT 技术总监 · 现 AI 创业者」, vote=12.8万

---

## 通用避坑

1. **平台 logo 真实化风险**：所有真实平台 logo 都不画，用通用图标 + 中文文字标识

2. **9 宫格头像合规**：用户头像必须 generic stylized icon（几何 / 卡通 / 抽象），禁止仿真真人

3. **热搜榜内容禁仿真**：所有出现的"热搜""推文""帖子"内容必须明显演示用，禁止模仿真实事件

4. **聊天对话用户名禁讳**：禁止用真实公众人物名做对话方名字

5. **暗色 vs 亮色**：X 推文默认暗色（社区习惯），其他平台默认亮色

6. **emoji 渲染**：emoji 在 GPT Image 2 里渲染稳定，可放心使用 ❤💬↗📊
