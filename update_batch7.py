import re

title_mapping = {
    'auto_reba_087.jpg': ('荣耀时刻', '红裙曳地 · 双奖在握 · 笑靥如花'),
    'auto_reba_088.jpg': ('落日余晖', '海天一色 · 吊带轻盈 · 长发随风'),
    'auto_reba_089.jpg': ('俏皮丸子', '嘟嘴卖萌 · 卫衣休闲 · 暮色温柔'),
    'auto_reba_090.jpg': ('亮片璀璨', '短裙修身 · 长腿吸睛 · 气场全开'),
    'auto_reba_091.jpg': ('蝴蝶少女', '头巾复古 · 丝袜个性 · 暗黑甜酷'),
    'auto_reba_092.jpg': ('紫韵东方', '旗袍优雅 · 兰花相伴 · 温婉动人'),
    'auto_reba_093.jpg': ('高马尾', '侧颜精致 · 耳饰独特 · 笑容明媚'),
    'auto_reba_094.jpg': ('蝶翼仙子', '金鳞缀身 · 对镜自拍 · 梦幻华丽'),
    'auto_reba_095.jpg': ('酷飒舞姿', '皮衣干练 · urban律动 · 活力四射'),
    'auto_reba_099.jpg': ('综艺萌态', '风衣知性 · 表情生动 · 反差可爱'),
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
