import re

title_mapping = {
    'auto_reba_065.jpg': ('人鱼公主', '渐变蓝裙 · 亮片闪耀 · 奖杯在握'),
    'auto_reba_066.jpg': ('慵懒午后', '毛绒外套 · 金环耳饰 · 微卷长发'),
    'auto_reba_067.jpg': ('红韵摩登', '丝绒红裙 · 黑丝高跟 · 复古风情'),
    'auto_reba_068.jpg': ('暖阳浅笑', '驼色大衣 · 丸子头 · 回眸温柔'),
    'auto_reba_069.jpg': ('优雅侧颜', '珍珠白裙 · 银杏耳坠 · 卷发如瀑'),
    'auto_reba_070.jpg': ('海边映画', '三格拼图 · 落日余晖 · 清新自然'),
    'auto_reba_072.jpg': ('酷飒双丸', '黑色皮衣 · 星星发饰 · wink俏皮'),
    'auto_reba_074.jpg': ('红衣魅影', '三格连拍 · 光影朦胧 · 冷艳凝视'),
    'auto_reba_075.jpg': ('元气马尾', '白色T恤 · 彩色发夹 · 甜美邻家'),
    'auto_reba_076.jpg': ('珠光晚宴', '黑色抹胸 · 珍珠项链 · 举杯浅笑'),
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
print(f"已更新10张，还剩 {remaining} 张待更新")
