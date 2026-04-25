# 角色设计与人物杂志封面 提示词优化模板

> 适用场景：游戏/动漫角色设定卡（多视角分解）/ 杂志封面级人物大片
> 核心要求：角色一致性 + 中文显示字体精准 + 高级杂志气质

---

## 优化指令（Claude 主进程读这段）

读完本文件后，把用户的简单输入展开成 300-500 字的英文+中文混合 prompt。

### 必须遵守的硬规则

1. **多视角图必须明确视角列表**：正面 / 侧面 / 背面 / 表情变化 / 装备拆解 / 配色板
2. **杂志封面必须包含**：标题刊名 / 期号 / 主标 / 副标 / 条形码 / 售价 / 出版日期
3. **中文文字用「」**括起来确保精确渲染
4. **背景留白**：角色卡用纯白背景；杂志封面留出顶部 15% 给标题
5. **人物面部一致性**：多视角必须强调"same face structure across all views"

### 子场景路由

- 包含"角色卡""设定图""多视角""三面图""分解" → 多视角角色子模板
- 包含"杂志封面""杂志大片""Vogue""Bazaar""ELLE" → 杂志封面子模板
- 都不命中 → 多视角角色子模板（兜底）

---

## 子模板 1: 多视角角色分解（参考 Case 5 Official Character Sheet）

### Prompt 模板

```
A 16:9 horizontal official character design sheet, 1536×1024, 
in clean character concept art style.

CHARACTER: {character_name_or_archetype} — {age} {gender}, 
{distinctive_features}, wearing {outfit_description}.

LAYOUT (clean white background, organized like an official game art bible):

ROW 1 - Three-view turnaround (top 50% of canvas):
- Front view (centered) — full body, T-pose or relaxed standing pose
- Side view (left of front) — perfect profile, same height alignment
- Back view (right of front) — same pose mirrored
- All three figures: SAME face/body structure, same lighting, neutral expression
- Below each view, small label 「正面」「侧面」「背面」 in 14pt

ROW 2 - Expression variations (next 25%):
- 5-6 head-shot circles showing different expressions:
  「平静」「微笑」「愤怒」「惊讶」「悲伤」「沉思」 (or chosen subset)
- Each circle ~150px diameter, captioned with expression name in 12pt

ROW 3 - Equipment/outfit details (bottom 15%):
- 4-6 detail vignettes showing close-ups of: weapon / accessory / 
  shoe / hairstyle detail / pattern detail
- Each labeled in 12pt 「{detail_chinese}」

ROW 4 - Color palette + world note (bottom 10%):
- Color palette swatches: 5-7 hex color blocks in a row, each with 
  small hex label below
- Right side: 1 short paragraph 「世界观：{world_setting_3_lines}」 
  in 12pt italic

STYLE: clean professional concept art, soft cell-shading or subtle 
painterly rendering. Pure white #FFFFFF background. NO complex backdrop. 
NO heavy shadows. NO photorealistic skin (this is concept art, not photo).
```

### 示例

**用户输入**：`做一张赛博朋克程序员的角色设定图`
**填充**：character=代号"零号工程师"30岁亚洲男性短发眼镜, outfit=深灰科技夹克带数据线, expressions=平静/微笑/震惊/愤怒/沉思/嘲讽, equipment=机械键盘/手腕显示器/U盘项链/能量饮料

---

## 子模板 2: 杂志封面（参考 Case 62 Vogue 级 9:16 封面）

### Prompt 模板

```
A vertical 9:16 high-end editorial fashion magazine cover, 1024×1536, 
rivaling Vogue / Harper's Bazaar / ELLE quality.

【SUBJECT (CRITICAL — IDENTITY & REALISM)】
- Generic stylized fictional model, NOT real public figure
- {age} {gender} {ethnicity_descriptor}, {hair_description}, 
  {distinctive_features}
- Photorealistic skin (visible pores, natural variation), NO 
  Instagram filter look
- Eye spacing/nose bridge/jawline must be consistent and believable

【OUTFIT】
{outfit_description with specific fabric textures (silk/satin/wool/leather)}, 
{color_palette_hex}, {accessories}.

【SETTING & ATMOSPHERE】
Location: {location_description}.
Lighting: {natural_or_studio_light_description} with {fill_quality}, 
gold/silver specular highlights NOT blown out.
Color grade: cinematic, rich, NOT muddy. {grade_keywords}.

【CAMERA】
85mm lens for medium shot or 50mm for full body, f/2.0, ISO 200.
Subject's eyes razor-sharp.

【MAGAZINE TYPOGRAPHY】
- Top 12%: HUGE magazine masthead 「{magazine_name_chinese}」 in 130pt 
  bold serif (Didot / Bodoni style), white or color depending on background
- Top-left under masthead: small text 「Vol. {issue_number} · {month_chinese}」
- Top-right under masthead: 「￥{price} · {date}」
- Center-right or bottom: 1 hero cover line 「{cover_line_chinese}」 in 
  48pt bold custom Chinese display font
- Bottom-left: 2-3 secondary cover lines, each 18-24pt, e.g.,
  「· {topic_1_chinese}」
  「· {topic_2_chinese}」
  「· {topic_3_chinese}」
- Bottom-right corner: small barcode + ISBN-style number

COMPOSITION: clean magazine layout with deliberate negative space at top 
for masthead. Hero subject's face in upper-third golden ratio position.

NEGATIVE: NO real magazine logo, NO real celebrity face, NO torn paper 
effect, NO over-saturated HDR.
```

### 示例

**用户输入**：`做一张程序员主题杂志封面，主题"代码即时尚"`
**填充**：subject=亚洲男性 32 岁短发眼镜, outfit=深灰高领+oversize 西装, location=玻璃幕墙后的办公空间, magazine=「码农志 CODER」, cover_line=「代码即时尚」, sub_topics=「Vibe Coding 元年」「30岁转 AI 来得及吗」「我用 Claude 写完了我的婚礼请柬」

---

## 通用避坑

1. **多视角不一致**：模型常把三个视角画成不同人。强制 prompt 加 "EXACT same face structure / same body proportions / same outfit details across front/side/back views — this is critical"

2. **杂志真名风险**：禁止用真实杂志名（Vogue / ELLE / Bazaar），用虚构刊名（「码农志」「极客 GEEK」「时代 TIMES」）。可以说"in Vogue style"作为风格参考但不画刊名

3. **真人冒名**：禁止用真实公众人物作为参考。如果用户输入指向真人（如"做一张刘亦菲杂志封面"），改为"亚洲女性长发古典气质 fictional"

4. **角色卡背景不要复杂**：多视角必须纯白底，否则三个视角对比时背景干扰会让模型画错

5. **Identity Drift**：杂志封面如果用真人作为参考，最容易翻车。用 generic 描述更稳
