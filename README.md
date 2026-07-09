# Dilraba Gallery

主画廊：`index.html` + `images/`（原图）+ `thumbs/`（WebP 缩略图），元数据在 `new_photos.json`。

## 本地重建

```bash
python3 generate_thumbs.py   # 从 images/ 生成 thumbs/480、thumbs/720
python3 build_gallery.py     # 写入 index.html（含 srcset / 灯箱 / 筛选）
python3 verify_gallery.py    # JSON = images = HTML = thumbs
```

## 说明

- 网格用 480/720 WebP 缩略图，灯箱加载 `images/` 原图。
- `candidate-500-v2/` 为本地候选集，已加入 `.gitignore`，不随 Pages 发布。
- 筛选标准见 `CURATION_STANDARD.md`。
