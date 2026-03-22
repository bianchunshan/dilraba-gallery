import re

# 第二批标题映射
title_mapping = {
    'auto_reba_032.jpg': ('白裙慵懒', '黑长卷发 · 露背白裙 · 清冷眼神'),
    'auto_reba_033.jpg': ('活力少女', '高马尾 · 白T短裙 · 长腿细腰'),
    'auto_reba_034.jpg': ('粉裙优雅', '波浪卷发 · 刺绣粉裙 · 珠宝点缀'),
    'auto_reba_037.jpg': ('花间精灵', '红裙印花 · 躺卧姿态 · 慵懒风情'),
    'auto_reba_038.jpg': ('酷飒双辫', '拳击辫 · 皮质上衣 · 凌厉眼神'),
    'auto_reba_039.jpg': ('红裙女王', '修身鱼尾 · 宝石腰链 · 高贵冷艳'),
    'auto_reba_040.jpg': ('亮片闪耀', '粉紫亮片 · 垫肩深V · 妩媚动人'),
    'auto_reba_041.jpg': ('花海仙子', '立体花瓣 · 渐变裙摆 · 户外自然'),
    'auto_reba_042.jpg': ('金鹰女神', '金色战袍 · 皇冠加冕 · 舞台光芒'),
    'auto_reba_043.jpg': ('逆光温柔', '侧颜轮廓 · 裸粉长裙 · 珍珠耳饰'),
}

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

for filename, (title, desc) in title_mapping.items():
    old_pattern = rf"{{ file: '{filename}', title: '[^']*', desc: '[^']*'"
    new_text = f"{{ file: '{filename}', title: '{title}', desc: '{desc}'"
    content_new = re.sub(old_pattern, new_text, content)
    if content_new != content:
        content = content_new
        print(f"✅ {filename} -> {title}")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n已更新 {len(title_mapping)} 张")
