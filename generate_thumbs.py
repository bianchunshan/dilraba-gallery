#!/usr/bin/env python3
"""从 images/ 生成 WebP 缩略图到 thumbs/480 与 thumbs/720。

用法：python3 generate_thumbs.py
"""
from pathlib import Path
from PIL import Image
import statistics

SIZES = (480, 720)
QUALITY = 78


def generate():
    src = Path('images')
    files = sorted(src.glob('*.jpg')) + sorted(src.glob('*.jpeg')) + sorted(src.glob('*.png'))
    if not files:
        raise SystemExit('images/ 下没有图片')

    for w in SIZES:
        Path(f'thumbs/{w}').mkdir(parents=True, exist_ok=True)

    print(f'生成缩略图：{len(files)} 张')
    for i, p in enumerate(files, 1):
        im = Image.open(p).convert('RGB')
        for w in SIZES:
            out = Path(f'thumbs/{w}') / (p.stem + '.webp')
            if out.exists() and out.stat().st_mtime >= p.stat().st_mtime:
                continue
            h = int(round(im.height * (w / im.width)))
            resized = im.resize((w, h), Image.Resampling.LANCZOS)
            resized.save(out, 'WEBP', quality=QUALITY, method=4)
        if i % 40 == 0 or i == len(files):
            print(f'  {i}/{len(files)}')

    for w in SIZES:
        sizes = [p.stat().st_size for p in Path(f'thumbs/{w}').glob('*.webp')]
        print(
            f'thumbs/{w}: {len(sizes)} 张，'
            f'合计 {sum(sizes)/1024/1024:.1f}MB，'
            f'均 {statistics.mean(sizes)/1024:.0f}KB'
        )


if __name__ == '__main__':
    generate()
