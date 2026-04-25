# 真实摄影 提示词优化模板

> 适用场景：商业广告产品图 / 真实人像 / 户外摄影
> 核心要求：照片级写实、无 AI 油腻感、专业摄影质感

---

## 优化指令（Claude 主进程读这段）

读完本文件后，把用户的简单输入展开成 250-400 字的英文+中文混合 prompt。

### 必须遵守的硬规则

1. **必含"Ultra-realistic" + 具体相机型号**：DSLR / Sony A7 IV / Canon R5 / Hasselblad，越具体越能驱动写实倾向
2. **必含镜头规格**：50mm f/1.4 / 85mm f/1.8 / 35mm f/2，规格驱动景深控制
3. **必含光线类型**：natural daylight / golden hour / studio softbox / window light
4. **必含质感词**：skin pores / fabric texture / fine grain / sharp focus
5. **必明确禁止 AI 痕迹**：NO AI smoothness, NO plastic skin, NO over-saturated HDR
6. **真人面部限制**：用"虚构角色"或"generic"修饰，禁止指向真人

### 子场景路由

- 包含"广告""产品图""开箱" → 广告产品子模板
- 包含"户外""街拍""自然光" → 户外人像子模板
- 包含"真人""真实""DSLR""写实" → 影棚写实子模板
- 都不命中 → 影棚写实子模板（兜底）

---

## 子模板 1: 广告产品图（参考 Case 22 绿茶胶卷套装）

### Prompt 模板

```
Ultra-realistic commercial product photography, 1024×1536 vertical 9:16.

PRODUCT: {product_name} displayed frontally / 3/4 angle / flat lay (pick one).

PRODUCT DETAILS:
- Material: {material_description with surface texture}
- Color palette: {brand_colors_hex}
- Packaging: {packaging_style} with visible 「{brand_text}」 label in 
  custom designed font (NOT generic system font)
- Accessories: {accessory_list spread around the product}

SETTING:
- Background: {background_color/material}, clean and minimal
- Surface: {surface_material} with subtle natural texture
- Props: 2-4 contextual props (tea leaves / film rolls / fabric / etc.)

LIGHTING:
- Main: large softbox from {direction}, creating soft directional shadow
- Fill: {fill_light_description}
- Highlight: subtle specular highlight on glossy surfaces
- NO harsh top-down studio light

CAMERA:
- Hasselblad medium format / Sony A7R V with 90mm macro lens
- f/8 aperture for full product sharpness
- ISO 100 for clean grain-free image

DETAILS:
- Sharp focus on product label text — must be 100% legible
- Subtle natural shadows under product
- Visible material texture (paper grain, fabric weave, metal brushed surface)

STYLE: high-end e-commerce photography reminiscent of Aesop / MUJI / 
Apple product shots. NO AI smoothness, NO plastic look, NO HDR halos.
```

### 示例

**用户输入**：`拍一张机械键盘开箱广告图`
**填充**：product=客制化机械键盘 GMK Olivia 配色, brand_text=「KEYS for CODERS」, accessories=拔键器+清洁刷+定制键帽收纳盒, background=浅灰水泥纹

---

## 子模板 2: 户外人像（参考 Case 58 户外白人女性）

### Prompt 模板

```
Ultra-realistic full-body outdoor photograph, 9:16 vertical 1024×1536.

SUBJECT: {gender}, {age_range}, {ethnicity_or_generic}, {hair_description}, 
wearing {outfit_description with fabric/color details}. NOT a real public 
figure — generic stylized face.

POSE: {natural_pose}, {body_orientation}, {expression} expression.

LOCATION: {outdoor_setting_description with environmental details}.

WEATHER & LIGHT:
- Time: {time_of_day} (e.g., golden hour / overcast noon / blue hour)
- Weather: {weather_condition}
- Key light: {natural_light_direction and quality}
- Fill: {natural_fill description}

CAMERA:
- Sony A7 IV with 85mm f/1.4 GM lens
- f/2.0 aperture, shallow depth of field, bokeh background
- ISO 400, 1/250s shutter

POST:
- Natural skin tones (NOT over-smoothed, visible pores)
- Slight film grain for organic feel
- Color grade: {grade_style} — e.g., Kodak Portra 400 / Fujifilm Pro 400H / 
  modern editorial

NEGATIVE: NO AI smoothness, NO plastic skin, NO Instagram filter look, 
NO over-saturated HDR, NO impossible lighting.
```

### 示例

**用户输入**：`拍一张程序员周末骑行户外照`
**填充**：subject=亚洲男性 30 岁短发, outfit=黑色骑行服+亮黄安全帽, location=城市郊外水泥公路, time=黄昏金光, grade=Kodak Portra 400

---

## 子模板 3: 影棚真实人像（参考 Case 25 DSLR 写实）

### Prompt 模板

```
Ultra-realistic cinematic DSLR photograph, 9:16 vertical 1024×1536.

SUBJECT: {age} {gender} {ethnicity_or_generic}, {hair}, {facial_feature_keywords}, 
wearing {outfit}. Generic face, NOT a real public figure.

POSE: {pose_description}, {gaze_direction}, {expression}.

SETTING: {studio_or_environment_setting} with {props}.

LIGHTING (cinematic):
- Key: large diffused softbox at 45° from {direction}, creates Rembrandt 
  triangle on cheek
- Rim: subtle backlight separating subject from background
- Background: {background_color_hex} seamless paper / textured wall

CAMERA:
- Canon EOS R5 with RF 85mm f/1.2L lens
- f/1.8 aperture, razor-sharp eye focus
- ISO 200, perfect exposure

DETAILS (CRITICAL FOR REALISM):
- Skin: visible pores, subtle skin oil sheen, natural skin tone variations
- Eyes: catchlight from key light source, sharp iris pattern
- Hair: individual strand definition, natural lighting interaction
- Fabric: visible weave / texture
- NO smooth plastic skin, NO blurred features, NO AI generic face

COLOR: cinematic color grade, {grade_style} (e.g., teal-orange / 
warm Portra / cool blue-pink / desaturated film).
```

### 示例

**用户输入**：`拍一张创业者人物特写`
**填充**：subject=亚洲男性 35 岁短发眼镜, outfit=深灰高领+橄榄色西装外套, pose=半身侧坐回望镜头, lighting=低位 Rembrandt key, background=深绿 #2A4A3A 旧布纹, grade=teal-orange cinematic

---

## 通用避坑

1. **AI 油腻感判断**：如果生成的脸看起来像"修过的网红照"，说明 prompt 缺少 "visible pores / natural skin tone variations / NO plastic skin"

2. **真人冒名**：禁止 prompt 中出现真实公众人物姓名（明星 / 政治人物 / 企业家），用"generic stylized face"或泛化描述

3. **HDR 灾难**：默认加 "NO over-saturated HDR, NO HDR halos around edges, natural dynamic range"

4. **景深控制**：背景虚化要明确指定 f-stop（f/1.4 浅 / f/8 中 / f/16 深）

5. **grain 细节**：胶片质感加 "subtle film grain Kodak Portra 400" / "Fujifilm Pro 400H grain pattern"

6. **品牌 logo 禁令**：服装 / 道具上禁止出现真实品牌商标，用"generic logo"或"unbranded"
