#!/usr/bin/env python3
"""校验画廊数据一致性：JSON 条目 = images/ 图片 = index.html 引用。

用法：python3 verify_gallery.py
对应 CURATION_STANDARD.md 入库流程第 7 步。
"""
import json
import os
import re
import sys


def check_main_gallery():
    errors = []
    with open('new_photos.json') as f:
        entries = json.load(f)
    json_files = [e['filename'] for e in entries]

    actual = sorted(f for f in os.listdir('images') if not f.startswith('.'))

    with open('index.html') as f:
        html = f.read()
    html_files = re.findall(r'href="images/([^"?]+)', html)

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
            data = fh.read()
        if f.lower().endswith(('.jpg', '.jpeg')):
            if not data.startswith(b'\xff\xd8'):
                errors.append(f'images/{f} 不是有效 JPEG')
        elif f.lower().endswith('.png'):
            if not data.startswith(b'\x89PNG'):
                errors.append(f'images/{f} 不是有效 PNG')

    return len(json_files), errors


def check_candidate_v2():
    errors = []
    base = 'candidate-500-v2'
    with open(os.path.join(base, 'candidate500_v2_manifest.json')) as f:
        manifest = json.load(f)
    mf = [e['file'].replace('images/', '') for e in manifest]

    actual = sorted(f for f in os.listdir(os.path.join(base, 'images'))
                    if not f.startswith('.'))

    with open(os.path.join(base, 'index.html')) as f:
        html = f.read()
    refs = sorted(set(re.findall(r'(?:href|src)="images/([^"?]+)', html)))

    if set(mf) != set(actual):
        errors.append('candidate manifest 与 images/ 不一致')
    if set(refs) != set(actual):
        errors.append('candidate index.html 引用与 images/ 不一致')

    return len(actual), errors


def main():
    n_main, errs = check_main_gallery()
    n_cand, errs2 = check_candidate_v2()
    errs += errs2
    print(f'主画廊: {n_main} 张；candidate-500-v2: {n_cand} 张')
    if errs:
        for e in errs:
            print('[FAIL]', e)
        sys.exit(1)
    print('[OK] 所有一致性检查通过')


if __name__ == '__main__':
    main()
