import re

title_mapping = {
    'auto_reba_077.jpg': ('金辉时刻', '金色亮片裙 · 深V吊带 · 手持滑板'),
    'auto_reba_078.jpg': ('清新代言', '白色T恤 · 高马尾 · 品牌活动'),
    'auto_reba_079.jpg': ('摩登星客', '黑色透视上衣 · 格纹裙 · 墨镜造型'),
    'auto_reba_080.jpg': ('人鱼姬光', '渐变蓝礼服 · 露肩设计 · 手持奖杯'),
    'auto_reba_081.jpg': ('明媚少女', '白色休闲装 · 流苏短裙 · 户外阳光'),
    'auto_reba_082.jpg': ('蓝调魅影', '银色吊带裙 · 红唇特写 · 氛围感光影'),
    'auto_reba_083.jpg': ('蕾丝优雅', '黑色蕾丝裙 · 丸子头 · 侧颜微笑'),
    'auto_reba_084.jpg': ('明黄风情', '黄色吊带裙 · 湿发造型 · 慵懒坐姿'),
    'auto_reba_085.jpg': ('鎏金闪耀', '金色亮片裙 · 露背设计 · 逆光轮廓'),
    'auto_reba_086.jpg': ('纯白仙姿', '白色抹胸裙 · 蛇形耳饰 · 清冷气质'),
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
