# 海报与插画 提示词优化模板

> 适用场景：旅游宣传 / 电影海报 / 赛事邀请 / 攻略地图 / 角色关系图 / 超市价格图 / 视觉冲击力宣传图

---

## 优化指令（Claude 主进程读这段）

读完本文件后，把用户的简单输入展开成 250-400 字的结构化英文+中文混合 prompt，交给 generator.py 出图。

### 必须遵守的硬规则

1. **Aspect ratio 必须明确**：海报默认 9:16 竖版（1024×1536）；电影海报建议 2:3（682×1024）；横版宣传 16:9（1536×1024）
2. **中文文字内容必须用「」括起来**，让 GPT Image 2 知道这是要精确渲染的字符
3. **指定字体风格**（无衬线 / 衬线 / 手写 / 黑体 / 宋体 / 楷体）
4. **指定主色调 hex**（不要只说"红色"，说 `#D4291C`）
5. **指定光线**（自然光 / 影棚光 / 戏剧光 / 神秘光）
6. **明确禁止**：真实品牌 logo / 真人面部 / 仿冒主体

### 子场景路由（按用户输入关键词）

- 包含"旅游""城市""景点" → 旅游海报子模板
- 包含"电影""海报""港片" → 电影海报子模板
- 包含"赛事""邀请""比赛" → 赛事宣传子模板
- 包含"攻略""地图""美食" → 攻略地图子模板
- 包含"角色关系""关系图""人物图谱" → 角色关系子模板
- 包含"超市""价格""促销""特价" → 超市价格子模板
- 包含"视觉冲击""大字""人物海报" → 视觉冲击子模板
- 都不命中 → 视觉冲击子模板（万能兜底）

---

## 子模板 1: 旅游海报（参考 Case 63 杭州西湖）

### Prompt 模板

```
A vertical 9:16 travel poster, 1024×1536, promoting {city_name} {season} tourism.

VISUAL STYLE: vintage travel poster aesthetic mixed with modern illustration. 
Color palette: {3-color_palette_with_hex}, evoking {mood_word}.

COMPOSITION (top to bottom):
- Top 30%: large illustrated landmark of {famous_landmark} ({material_style})
- Center 40%: hero text 「{city_name_chinese}」 in 100pt bold custom-designed 
  Chinese characters, with subtle tactile texture (NOT system font)
- Below hero: subtitle 「{season_chinese} · {tagline_chinese}」 in 28pt
- Bottom 30%: smaller scenic vignettes (3 small icons of local food / activity / 
  natural feature), each labeled in 14pt Chinese
- Bottom margin: small line 「{date_range} · {organizer_chinese}」 in 12pt

TYPOGRAPHY: Chinese characters in custom designed style with brushstroke 
references, NOT generic font.

DETAIL: hand-drawn illustration feel, NOT photo-realistic, NOT AI smooth.
```

### 示例

**用户输入**：`画一张杭州西湖春季旅游海报`
**填充关键字段**：city=杭州, landmark=断桥+雷峰塔, season=春季, palette=#7BB3D9 湖蓝/#E8B7C5 樱粉/#F5DEB3 暖米, mood=诗意, tagline=「烟雨入江南」

---

## 子模板 2: 电影海报（参考 Case 65 90 年代港片）

### Prompt 模板

```
A 2:3 vertical movie poster, 682×1024, in {era_style} style.

VISUAL: hero subject {character_description} in {pose}, {emotion} expression. 
Background: {scene_setting} with {atmosphere}.

LIGHTING: {dramatic_lighting_style}, {key_light_color} key light from {direction}, 
strong contrast, cinematic mood.

TYPOGRAPHY:
- Top 15%: small Chinese title 「{director_credit}」 in 18pt
- Bottom 30%: HUGE Chinese movie title 「{movie_title}」 in 120pt 
  bold {font_style} (e.g., 黑体 / 楷体 / 手写), with optional gold/red outline
- Below title: English subtitle 「{english_title}」 in 24pt
- Bottom margin: cast names + release date in 12pt

COLOR GRADING: {color_grade_description}, NOT modern HDR look.
Style: looks like a real {era} cinema lobby card. NO AI smoothness.
```

### 示例

**用户输入**：`做一张90年代港片风格电影海报，主角程序员，标题《代码江湖》`
**填充**：era=1990s 港片, character=穿白衬衫的程序员手持光剑般键盘, pose=回眸, lighting=戏剧化侧光带烟雾, color_grade=胶片颗粒+橙青对比

---

## 子模板 3: 赛事宣传（参考 Case 13 粤超邀请）

### Prompt 模板

```
A vertical 9:16 event poster, 1024×1536, for {event_name}.

LAYOUT:
- Top 25%: event official emblem (geometric, NOT real sports logo)
- Center 50%: dynamic illustration of {sport_or_action_visual}, full of 
  motion blur and energy
- Below: HUGE Chinese event title 「{event_chinese_title}」 in 90pt bold 
  sports-display font, with {accent_color} outline
- Date stripe: 「{date_range_chinese}」 in 36pt
- Venue: 「{venue_chinese}」 in 24pt
- Bottom margin: small sponsors row (geometric icons, NOT real brand logos)

COLOR PALETTE: {primary_color_hex} as dominant, {accent_color_hex} for highlights.

STYLE: bold poster art, high contrast, energy-packed, modern sports promo.
```

### 示例

**用户输入**：`做一张程序员马拉松邀请海报`
**填充**：event=Code Marathon 2026, sport=程序员手指在键盘上飞舞带着光轨, palette=#1A237E 深蓝 + #FFD700 金黄, venue=深圳科技园

---

## 子模板 4: 攻略地图（参考 Case 3 成都美食地图）

### Prompt 模板

```
A vertical 9:16 illustrated city food/travel map, 1024×1536.

CITY: {city_name}. Map style: hand-drawn illustration, NOT realistic GIS map.

LAYOUT:
- Top 12%: header banner with title 「{city_name}{topic}地图」 in 60pt 
  bold custom Chinese, subtitle 「{tagline}」 in 18pt
- Main 75%: stylized aerial view of {city_landmarks_list} as cute icons, 
  with curving roads connecting them
- Each landmark/spot has a small label in 12pt Chinese: 「{spot_name}」
- 5-8 callout cards floating around the map, each with:
  · Spot name 「{name}」 (14pt bold)
  · 1-line description in 11pt (e.g., 「人均 ¥30 · 必点担担面」)
  · Small icon (chopsticks / camera / star)
- Bottom 13%: legend row + small note 「{author_handle}制图」

COLOR PALETTE: warm illustrated colors (not photo-real), 
{primary} as base + {accent} for highlights.

STYLE: cute hand-drawn travel guide illustration, like a child's 
storybook map. Wibbly lines OK. NO AI smoothness.
```

### 示例

**用户输入**：`画一张成都美食地图`
**填充**：city=成都, topic=美食, landmarks=春熙路+宽窄巷子+锦里+人民公园, palette=#F5DEB3 暖米 + #D4291C 川辣红

---

## 子模板 5: 角色关系图（参考 Case 34 Character Relationship Map）

### Prompt 模板

```
A vertical 9:16 character relationship diagram poster, 1024×1536.

THEME: {story_or_world_name}.

LAYOUT:
- Top 15%: title 「{title_chinese}」 in 70pt bold, subtitle 「人物关系图」
- Center 70%: 5-9 character portrait nodes arranged in {layout_pattern} 
  (radial / tree / grid). Each node:
  · Circular portrait 200px (illustrated, NOT photo, NOT real person)
  · Character name 「{name}」 in 18pt bold below
  · Role label in 11pt 「{role}」 (e.g., 主角 / 反派 / 师父)
- Connecting lines between nodes, each line labeled in 11pt:
  · Solid line for direct relations
  · Dashed line for hidden/past relations
  · Color-coded: red=敌对, blue=友谊, pink=爱情, gray=师徒
- Bottom 15%: legend explaining color codes + note 「{world_setting_one_liner}」

ILLUSTRATION STYLE: clean modern illustration, similar character art style 
across all nodes. Each character clearly distinguishable by 
hairstyle/clothing/color theme.

NO AI smoothness. NO real-celebrity faces. All characters fictional.
```

### 示例

**用户输入**：`画一张程序员公司人物关系图`
**填充**：title=「码农江湖」, characters=技术总监+架构师+前端组长+后端组长+实习生+测试妹子+产品经理+HR

---

## 子模板 6: 超市价格促销（参考 Case 49 日本超市 Sale Flyer）

### Prompt 模板

```
A vertical 9:16 supermarket promotional flyer, 1024×1536, in {country_style} 
supermarket flyer style (NOT real brand logo).

LAYOUT:
- Top 12%: red banner 「特价促销」 / 「タイムセール」 / similar in 60pt 
  bold yellow font on red background, lightning-bolt icons on sides
- Main 80%: 8-12 product cards arranged in 3-4 column grid, each card:
  · Product photo (illustrated, NOT real brand)
  · Product name 「{product_name}」 in 16pt black
  · Original price 「¥{old_price}」 with strike-through in 14pt gray
  · BIG sale price 「¥{new_price}」 in 36pt red bold
  · Optional yellow callout 「半价」/「2件」/「限购」 in 18pt
- Bottom 8%: store info bar 「营业至 {time}」 in 14pt

COLORS: dominant red #D4291C + sale-yellow #FFD700 + black text #1A1A1A 
+ white #FFFFFF backgrounds for product cards.

STYLE: dense information layout, supermarket-flyer aesthetic, slightly 
chaotic but readable, looks printed not digital.
```

### 示例

**用户输入**：`画一张程序员神器特价宣传图`
**填充**：products=机械键盘/人体工学椅/27寸4K显示器/防蓝光眼镜/咖啡机/降噪耳机, country_style=日式 + 中文混排

---

## 子模板 7: 视觉冲击宣传图（参考 Case 67 鹿鼎记角色海报，万能兜底）

### Prompt 模板

```
A vertical 9:16 high-impact character/concept poster, 1024×1536.

HERO SUBJECT: {subject_description}, in {dramatic_pose}, with {emotion} 
expression. {Material/clothing details with specific texture}.

BACKGROUND: {background_setting} with {atmosphere_effects}, slight motion 
blur for depth.

LIGHTING: cinematic key light from {direction} in {color_temperature}, 
strong rim light, deep shadows. Color grade: {grade_style}.

TYPOGRAPHY:
- Top 10%: small Chinese label 「{category_label}」 in 18pt thin
- Center-left or bottom: HUGE vertical Chinese title 「{title_chinese}」 
  in 120pt bold custom display font, with optional gold/silver foil effect
- Bottom 8%: 1-line tagline 「{tagline_chinese}」 in 24pt elegant Chinese

COMPOSITION: rule of thirds, hero subject occupies 60-70% of frame, 
deliberate negative space for typography.

DETAIL: high-end Chinese character design (not generic font), photorealistic 
subject rendering with sharp facial features (NO AI smoothness, NO 
plastic skin), professional retouching feel.
```

### 示例

**用户输入**：`画一张赛博朋克程序员视觉冲击海报`
**填充**：subject=戴黑框眼镜的程序员被代码雨包围, pose=仰视, lighting=蓝紫赛博光从屏幕反射, title=「代码即权力」, tagline=「献给所有 996 的灵魂」

---

## 通用避坑（所有子模板都用）

1. **真人面部禁令**：禁止仿真任何真实公众人物（明星 / 政治人物 / 企业家），人物面部用"虚构角色 generic stylized face"

2. **品牌 logo 禁令**：禁止画真实品牌 logo（Apple / Nike / Coca-Cola 等），用"通用几何标识"代替

3. **字体不要默认**：Chinese characters 默认 GPT Image 2 会生成系统字体（思源 / 苹方），加 "custom designed display font" / "brushstroke font" / "tactile texture" 强制风格化

4. **避免 AI 油腻感**：所有 prompt 末尾加 "NO AI smoothness, NO over-processed plastic look, NO over-saturated HDR"

5. **9:16 默认**：抖音 / 朋友圈分享场景；电影海报例外用 2:3
