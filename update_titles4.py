import re

title_mapping = {
    'auto_reba_055.jpg': ('红韵', '复古红唇 · 格纹长裙 · 慵懒姿态'),
    'auto_reba_056.jpg': ('春漾', '清新印花 · 温柔长发 · 明媚眼神'),
    'auto_reba_057.jpg': ('星璨', '亮片外套 · 精致珠宝 · 梦幻光影'),
    'auto_reba_058.jpg': ('绯色', '红色纱裙 · 俏皮短发 · 甜美笑容'),
    'auto_reba_059.jpg': ('鎏金', '金色刺绣 · 卢浮宫外 · 优雅侧颜'),
    'auto_reba_060.jpg': ('炽艳', '红色吊带 · 钻饰肩带 · 自信凝视'),
    'auto_reba_061.jpg': ('晴空', '高马尾辫 · 蓝白配饰 · 活力清新'),
    'auto_reba_062.jpg': ('香槟', '褶皱礼服 · 绑带设计 · 修长身姿'),
    'auto_reba_063.jpg': ('灰调', '立体褶皱 · 艺术造型 · 简约背景'),
    'auto_reba_064.jpg': ('夜魅', '黑色纱衣 · 烟雾缭绕 · 神秘冷艳'),
}

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

for filename, (title, desc) in title_mapping.items():
    old_pattern = rf"{{ file: '{filename}', title: '[^']*', desc: '[^']*'"
    new_text = f"{{ file: '{filename}', title: '{title}', desc: '{desc}'"
    content_new = re.sub(old_pattern, new_text, content)
    if content_new != content:
        content = content_new

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

remaining = content.count('精选写真')
print(f"已更新，还剩 {remaining} 张待更新")
