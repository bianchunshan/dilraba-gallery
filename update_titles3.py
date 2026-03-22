import re

# 第三批标题映射
title_mapping = {
    'auto_reba_045.jpg': ('碧蓝仙裙', '高马尾 · 水钻吊带 · 侧颜杀'),
    'auto_reba_046.jpg': ('烈焰红裙', '宝石肩带 · 腰链点缀 · 优雅站姿'),
    'auto_reba_047.jpg': ('花间少女', '玫瑰印花裙 · 黑色短西装 · 花环发饰'),
    'auto_reba_048.jpg': ('金色人鱼', '亮片鱼尾裙 · 深V设计 · 红毯女王'),
    'auto_reba_049.jpg': ('酷飒机能', '双马尾编发 · 网纱上衣 · 紫色光影'),
    'auto_reba_050.jpg': ('街头回眸', '灰色夹克 · 慵懒卷发 · 集装箱背景'),
    'auto_reba_051.jpg': ('花漾甜心', '丸子头 · 印花外套 · 阳光氛围'),
    'auto_reba_052.jpg': ('摩登短发', '齐刘海 · 狗狗T恤 · 金色配饰'),
    'auto_reba_053.jpg': ('纯白初恋', '空气刘海 · 月亮项链 · 海边清新'),
    'auto_reba_054.jpg': ('复古名伶', '黑色丝绒裙 · 网纱面纱 · 宫廷长桌'),
}

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

for filename, (title, desc) in title_mapping.items():
    old_pattern = rf"{{ file: '{filename}', title: '[^']*', desc: '[^']*'"
    new_text = f"{{ file: '{filename}', title: '{title}', desc: '{desc}'"
    content_new = re.sub(old_pattern, new_text, content)
    if content_new != content:
        content = content_new
        print(f"✅ {filename}")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n已更新 {len(title_mapping)} 张，还剩 {content.count('精选写真')} 张待更新")
