# 信息图与拆解图 提示词优化模板

> 适用场景：产品拆解爆炸图 / 菜谱步骤流程图 / 书法字帖 / 信息密集科普图
> 核心要求：信息密度高、文字清晰、布局严谨

---

## 优化指令（Claude 主进程读这段）

读完本文件后，把用户的简单输入展开成 250-400 字的英文+中文混合 prompt。

### 必须遵守的硬规则

1. **Aspect ratio 必须明确**：拆解图建议 16:9（1536×1024）展示横向布局；菜谱 / 字帖 / 科普图默认 9:16（1024×1536）
2. **信息层级清晰**：标题 / 子标题 / 正文 / 标注 / 注释 5 级字号
3. **中文必用「」**括起来，英文和数字不用
4. **箭头/连线必须明示**：标注类图必须有从主体到标签的引线
5. **背景纯色**：信息图背景永远纯色（white #FFFFFF / cream #F5F0E8 / charcoal #1A1A1A）

### 子场景路由

- 包含"拆解""爆炸图""分解" → 产品拆解子模板
- 包含"菜谱""做法""步骤""流程图" → 菜谱步骤子模板
- 包含"字帖""书法""临摹" → 字帖子模板
- 包含"科普""信息图""infographic" → 信息密集子模板
- 都不命中 → 信息密集子模板（兜底）

---

## 子模板 1: 产品拆解爆炸图（参考 Case 53 Sony A7）

### Prompt 模板

```
Ultra-detailed exploded-view technical illustration, 16:9 horizontal 1536×1024.

SUBJECT: {product_name} disassembled into all major components, displayed on 
clean {bg_color} background with subtle drop shadows.

LAYOUT:
- Center 70%: hero composition — main body of the {product} in center, 
  surrounded by exploded components floating outward in their installation 
  direction, each component spaced ~20-40px from neighbors
- Each component connected to its label by thin gray dotted line (1px)
- Top 10%: title bar 「{product_chinese_name} 完整拆解图」 in 36pt bold black
- Bottom 8%: small disclaimer 「示意图 · 非官方拆解指南」 in 12pt gray

COMPONENT LABELS (each):
- Component name in Chinese 「{component_chinese}」 (14pt bold #1A1A1A)
- Optional spec line in 11pt gray 「{spec_or_material}」
- All labels positioned on left/right edge of canvas, NOT overlapping image

STYLE:
- Photo-realistic component renderings (NOT line drawing)
- Soft global illumination, no harsh shadows
- Subtle metallic highlights where applicable
- Clean technical manual aesthetic, like Apple service guide

NEGATIVE: NO real brand logo on parts (use generic "model X" labels), 
NO AI smoothness, NO over-saturated colors.
```

### 示例

**用户输入**：`画一张机械键盘拆解图`
**填充**：product=客制化 65% 机械键盘, components=外壳上盖+定位板+轴体+键帽组+电路板+电池+泡棉夹层+硅胶垫+USB-C 接口

---

## 子模板 2: 菜谱步骤流程图（参考 Case 55 烹饪流程）

### Prompt 模板

```
A vertical 9:16 cooking recipe flowchart, 1024×1536.

DISH: {dish_chinese_name}.

LAYOUT:
- Top 10%: title 「{dish_chinese}制作流程」 in 56pt bold custom Chinese 
  display font, subtitle 「{cuisine_label} · {difficulty_stars}」 in 18pt
- Middle 80%: 6-9 step cards arranged in vertical flow, each card:
  · Step number circle 「步骤 N」 in red #D4291C (40pt)
  · Step illustrated icon (cute hand-drawn, NOT photo)
  · Step description 「{action_chinese}」 in 18pt black, max 2 lines
  · Time/temperature note in 12pt gray 「{time_min}分钟 · {temp}」
  · Down-arrow connector to next step (thin red 2px line)
- Bottom 10%: ingredient list in 2 columns, each item 14pt 
  「{ingredient}：{amount}」

VISUAL STYLE: warm illustrated cookbook aesthetic, hand-drawn icons, 
beige #F5F0E8 background, red and brown accent palette.

CHINESE TYPOGRAPHY: custom designed display font for title 
(brushstroke / 楷体 mix), system clean font for body.

NEGATIVE: NO real food photography mixed in, NO AI smoothness, 
NO chaos — strict vertical flow only.
```

### 示例

**用户输入**：`画一张红烧肉制作流程图`
**填充**：dish=红烧肉, cuisine=家常菜, difficulty=★★★, ingredients=五花肉+冰糖+老抽+生抽+料酒+八角+葱姜

---

## 子模板 3: 书法字帖（参考 Case 33 Calligraphy Copybook）

### Prompt 模板

```
A vertical 9:16 traditional Chinese calligraphy copybook page, 1024×1536.

SCRIPT STYLE: {calligraphy_style} (e.g., 楷书 Kaishu / 行书 Xingshu / 
草书 Caoshu / 隶书 Lishu / 篆书 Zhuanshu).

LAYOUT:
- Top 10%: header strip — left: title 「{title_chinese}临摹字帖」 in 28pt 
  bold black; right: small label 「{calligrapher_name}笔法 · {script_chinese}」 
  in 14pt gray (e.g., 「颜真卿笔法 · 楷书」)
- Main 80%: 4×6 = 24 grid cells (Chinese mizi-ge 米字格 grid), each cell:
  · Light gray cross-grid lines (米字格 八宫格 style)
  · One large brushwritten Chinese character centered, in {ink_color} ink, 
    showing realistic brush stroke variation (thin to thick), with subtle 
    ink bleed at stroke ends
- Characters are taken from {phrase_or_poem_chinese}, in correct reading order 
  (left-to-right, top-to-bottom or right-to-left vertical depending on style)
- Bottom 10%: small footer 「{phrase_full_chinese}」 typeset in 14pt regular 
  font as reference

PAPER: aged off-white #F8F4E8 with subtle paper grain texture, faint vertical 
column lines if traditional vertical layout.

NEGATIVE: NO digital sharp edges on characters, brushstrokes must look 
ink-on-paper not vector. NO English text. NO modern UI elements.
```

### 示例

**用户输入**：`生成一张唐诗书法临摹字帖`
**填充**：style=楷书, calligrapher=颜真卿, phrase=「春眠不觉晓 处处闻啼鸟 夜来风雨声 花落知多少」

---

## 子模板 4: 信息密集科普图（兜底 · 参考 Case 55 Ultra-Dense）

### Prompt 模板

```
A vertical 9:16 ultra-dense educational infographic, 1024×1536.

THEME: {topic_chinese}.

LAYOUT (modular grid, generous information density):
- Top 12%: hero header with main title 「{topic_main_chinese}」 in 60pt 
  bold custom display font, subtitle 「{tagline_chinese}」 in 18pt
- Body 80%: 6-9 information modules arranged in irregular but balanced grid:
  · Module 1 (large, 1/2 width): main illustrated diagram with callouts
  · Modules 2-4 (medium): 3 information cards with icon + 「{title}」 + 
    「{description_2_lines}」
  · Modules 5-9 (small): mini-data points — circular ring chart / horizontal 
    bar / Top 5 list / quote box / definition card
- Each module has clear visual boundary: rounded rectangle, 1px border 
  #E0E0E0, white #FFFFFF or cream #FFFEF7 background
- Modules separated by 16px gap
- Bottom 8%: footer with source 「数据来源：{source}」 in 11pt gray

TYPOGRAPHY (5-level hierarchy):
- Hero title: 60pt bold custom display
- Section title: 24pt bold sans-serif
- Body: 14pt regular
- Caption/label: 11pt regular
- Data number (highlight): 36pt bold colored

COLORS: limited palette — {primary_color_hex} as accent, neutral 
grays/creams for backgrounds, ONE strong accent for data highlights.

STYLE: National Geographic infographic + Apple keynote aesthetic. Dense 
but airy. Each module readable on its own. NO chaos, strict alignment.
```

### 示例

**用户输入**：`画一张程序员工资分布科普图`
**填充**：topic=2026 中国程序员工资全景, modules=按城市/年龄/技术栈/学历/经验/性别 + 数据来源「Stack Overflow + 拉勾 + BOSS 直聘联合数据」

---

## 通用避坑

1. **信息密度悖论**：信息越密，越要严格对齐。"密"不等于"乱"——明确指定模块边界、间距 px、对齐方式

2. **中文文字渲染**：长文本（>20 字）必须用「」括起来标记为精确渲染内容，否则 GPT Image 2 会简化为意思相近但字不对的文本

3. **图标规则**：图标统一用"flat illustration / line icon / hand-drawn"中的一种，不要混用。混用是 AI 油腻感的常见来源

4. **数据可信度**：标"数据来源：xxx"小字脚注是细节加分项，让图看起来像专业研究而非随手做

5. **横版 vs 竖版**：
   - 拆解图、横向流程：16:9
   - 菜谱、字帖、科普长图：9:16
   - 1:1 适合社媒缩略图
