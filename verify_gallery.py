#!/usr/bin/env python3
"""校验画廊数据一致性：JSON 条目 = images/ 图片 = index.html 引用 = thumbs。

用法：python3 verify_gallery.py
对应 CURATION_STANDARD.md 入库流程第 7 步。
"""
import json
import os
import re
import sys
from pathlib import Path


def check_main_gallery():
    errors = []
    with open('new_photos.json') as f:
        entries = json.load(f)
    json_files = [e['filename'] for e in entries]

    actual = sorted(
        f for f in os.listdir('images')
        if not f.startswith('.') and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
    )

    with open('index.html') as f:
        html = f.read()
    # 只统计画廊卡片链接，排除 favicon / og 等其它 images/ 引用
    html_files = re.findall(r'class="card" href="images/([^"?]+)', html)

    if len(json_files) != len(set(json_files)):
        errors.append('new_photos.json 存在重复 filename')
    if set(json_files) != set(actual):
        missing = set(json_files) - set(actual)
        extra = set(actual) - set(json_files)
        if missing:
            errors.append(f'JSON 引用但 images/ 缺失: {sorted(missing)}')
        if extra:
            errors.append(f'images/ 存在但 JSON 未收录: {sorted(extra)}')
    if json_files != html_files:
        errors.append('index.html 引用顺序/内容与 new_photos.json 不一致')

    ranks = [e['rank'] for e in entries]
    if ranks != list(range(1, len(entries) + 1)):
        errors.append('rank 不是从 1 开始的连续序列')

    for f in actual:
        with open(os.path.join('images', f), 'rb') as fh:
            data = fh.read(8)
        if f.lower().endswith(('.jpg', '.jpeg')):
            if not data.startswith(b'\xff\xd8'):
                errors.append(f'images/{f} 不是有效 JPEG')
        elif f.lower().endswith('.png'):
            if not data.startswith(b'\x89PNG'):
                errors.append(f'images/{f} 不是有效 PNG')

    # 缩略图
    for e in entries:
        stem = Path(e['filename']).stem
        for w in (480, 720):
            thumb = Path(f'thumbs/{w}/{stem}.webp')
            if not thumb.exists():
                errors.append(f'缺少缩略图: {thumb}')
            else:
                with open(thumb, 'rb') as fh:
                    if fh.read(4) != b'RIFF':
                        errors.append(f'{thumb} 不是有效 WebP')

    # HTML 应引用 thumbs
    if 'thumbs/720/' not in html or 'srcset=' not in html:
        errors.append('index.html 未使用 thumbs srcset')

    return len(json_files), errors


def check_candidate_v2():
    """候选集可选：目录不存在则跳过（已从 Pages 发布范围排除）。"""
    errors = []
    base = 'candidate-500-v2'
    if not os.path.isdir(base):
        return 0, errors, True  # skipped

    manifest_path = os.path.join(base, 'candidate500_v2_manifest.json')
    if not os.path.isfile(manifest_path):
        return 0, [f'{base} 存在但缺少 manifest'], False

    with open(manifest_path) as f:
        manifest = json.load(f)
    mf = [e['file'].replace('images/', '') for e in manifest]

    img_dir = os.path.join(base, 'images')
    actual = sorted(f for f in os.listdir(img_dir) if not f.startswith('.')) if os.path.isdir(img_dir) else []

    index_path = os.path.join(base, 'index.html')
    refs = []
    if os.path.isfile(index_path):
        with open(index_path) as f:
            html = f.read()
        refs = sorted(set(re.findall(r'(?:href|src)="images/([^"?]+)', html)))

    if set(mf) != set(actual):
        errors.append('candidate manifest 与 images/ 不一致')
    if refs and set(refs) != set(actual):
        errors.append('candidate index.html 引用与 images/ 不一致')

    return len(actual), errors, False


def main():
    n_main, errs = check_main_gallery()
    n_cand, errs2, skipped = check_candidate_v2()
    errs += errs2
    if skipped:
        print(f'主画廊: {n_main} 张；candidate-500-v2: 已跳过（未纳入发布）')
    else:
        print(f'主画廊: {n_main} 张；candidate-500-v2: {n_cand} 张')
    if errs:
        for e in errs:
            print('[FAIL]', e)
        sys.exit(1)
    print('[OK] 所有一致性检查通过')


if __name__ == '__main__':
    main()
