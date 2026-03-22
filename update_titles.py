import re

# 标题映射（文件名 -> 新标题和描述）
title_mapping = {
    'auto_reba_022.jpg': ('黑金女王', '丝绒质感 · 钻饰肩袖 · 冷艳坐姿'),
    'auto_reba_024.jpg': ('晨光私语', '丝缎露背 · 慵懒姿态 · 柔和光影'),
    'auto_reba_025.jpg': ('暗夜玫瑰', '金属耳饰 · 红唇深邃 · 神秘紫调'),
    'auto_reba_027.jpg': ('江景微醺', '丝绒吊带 · 城市天际 · 飘逸长发'),
    'auto_reba_028.jpg': ('鎏金鱼尾', '亮片长裙 · 修身剪裁 · 华贵气场'),
    'auto_reba_029.jpg': ('星海梦境', '薄纱层叠 · 银线刺绣 · 静谧蓝调'),
    'auto_reba_030.jpg': ('格纹雅痞', '西装廓形 · 复古格纹 · 随性倚坐'),
    'auto_reba_036.jpg': ('流光侧影', '金色亮片 · 光晕背景 · 优雅回眸'),
    'auto_reba_026.jpg': ('人鱼泪光', '渐变亮片 · 流苏耳坠 · 梦幻发饰'),
    'auto_reba_031.jpg': ('甜酷红心', '皮衣质感 · 毛绒心形 · 俏皮混搭'),
}

# 读取index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 更新每个映射的标题
for filename, (title, desc) in title_mapping.items():
    # 查找并替换
    old_pattern = rf"{{ file: '{filename}', title: '[^']*', desc: '[^']*'"
    new_text = f"{{ file: '{filename}', title: '{title}', desc: '{desc}'"
    content_new = re.sub(old_pattern, new_text, content)
    if content_new != content:
        content = content_new
        print(f"✅ 已更新: {filename} -> {title}")
    else:
        print(f"⚠️ 未找到: {filename}")

# 保存
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n已更新标题")
