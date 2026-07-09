#!/usr/bin/env python3
"""从 new_photos.json 生成 index.html。

用法：
  python3 generate_thumbs.py   # 先生成/更新缩略图
  python3 build_gallery.py

卡片顺序与 JSON 顺序一致（按 rank 排序），保证 verify_gallery.py 通过。
"""
import json
import time
from collections import Counter
from pathlib import Path

TEMPLATE_HEAD = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>迪丽热巴 · 影像画廊</title>
<meta name="description" content="迪丽热巴精选写真画廊，共 __COUNT__ 张，按高级性感程度排序。">
<meta property="og:title" content="迪丽热巴 · 影像画廊">
<meta property="og:description" content="精选公开写真、红毯与时尚大片，共 __COUNT__ 张。">
<meta property="og:type" content="website">
<meta property="og:image" content="__OG_IMAGE__">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="迪丽热巴 · 影像画廊">
<meta name="twitter:description" content="精选公开写真、红毯与时尚大片，共 __COUNT__ 张。">
<meta name="twitter:image" content="__OG_IMAGE__">
<link rel="icon" href="__OG_IMAGE__" type="image/jpeg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@600;700&family=Noto+Sans+SC:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#0d0b10;
  --bg-soft:#16131c;
  --card:#1c1824;
  --text:#f2eee8;
  --muted:#9a93a5;
  --gold:#d8b16a;
  --gold-soft:rgba(216,177,106,.16);
  --radius:14px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;
  background:
    radial-gradient(1200px 500px at 50% -100px, rgba(216,177,106,.08), transparent 60%),
    var(--bg);
  color:var(--text);
  font-family:"Noto Sans SC",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  -webkit-font-smoothing:antialiased;
}

/* ---------- 头部 ---------- */
header{
  padding:64px 20px 28px;
  text-align:center;
}
.kicker{
  display:inline-block;
  font-size:12px;
  letter-spacing:.42em;
  text-indent:.42em;
  color:var(--gold);
  text-transform:uppercase;
  margin-bottom:18px;
}
h1{
  margin:0;
  font-family:"Noto Serif SC",serif;
  font-weight:700;
  font-size:clamp(30px,6vw,52px);
  letter-spacing:.08em;
  line-height:1.2;
}
h1 .dot{color:var(--gold)}
.sub{
  margin:14px auto 0;
  max-width:560px;
  color:var(--muted);
  font-size:14px;
  line-height:1.8;
}
.stats{
  display:flex;
  justify-content:center;
  gap:28px;
  margin-top:26px;
}
.stat{text-align:center}
.stat b{
  display:block;
  font-family:"Noto Serif SC",serif;
  font-size:24px;
  color:var(--gold);
  font-weight:600;
}
.stat span{font-size:12px;color:var(--muted);letter-spacing:.1em}
.rule{
  width:56px;height:1px;margin:30px auto 0;
  background:linear-gradient(90deg,transparent,var(--gold),transparent);
}

/* ---------- 筛选栏 ---------- */
.toolbar{
  position:sticky;top:0;z-index:20;
  display:flex;justify-content:center;gap:8px;flex-wrap:wrap;
  padding:12px 16px;
  background:rgba(13,11,16,.82);
  backdrop-filter:blur(14px);
  -webkit-backdrop-filter:blur(14px);
  border-bottom:1px solid rgba(255,255,255,.05);
}
.chip{
  appearance:none;border:1px solid rgba(255,255,255,.12);
  background:transparent;color:var(--muted);
  padding:7px 14px;border-radius:999px;
  font-size:13px;font-family:inherit;cursor:pointer;
  transition:all .25s ease;
}
.chip .n{opacity:.55;margin-left:4px;font-size:11px}
.chip:hover{color:var(--text);border-color:rgba(216,177,106,.5)}
.chip.active{
  background:var(--gold-soft);
  border-color:var(--gold);
  color:var(--gold);
}
.chip.active .n{opacity:.8}

/* ---------- 画廊 ---------- */
.gallery{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(240px,1fr));
  gap:14px;
  padding:22px clamp(14px,3vw,36px) 40px;
  max-width:1720px;
  margin:0 auto;
}
@media (max-width:640px){
  .gallery{grid-template-columns:repeat(2,1fr);gap:10px;padding:14px 12px 30px}
}
.card{
  position:relative;
  display:block;
  border-radius:var(--radius);
  overflow:hidden;
  background:var(--card);
  text-decoration:none;
  color:var(--text);
  box-shadow:0 2px 10px rgba(0,0,0,.35);
  transform:translateZ(0);
  transition:transform .35s cubic-bezier(.2,.7,.3,1),box-shadow .35s ease;
  opacity:0;
  animation:reveal .6s ease forwards;
}
@keyframes reveal{to{opacity:1}}
.card:hover{
  transform:translateY(-4px);
  box-shadow:0 14px 34px rgba(0,0,0,.5);
}
.card img{
  width:100%;aspect-ratio:2/3;object-fit:cover;display:block;
  transition:transform .6s cubic-bezier(.2,.7,.3,1),filter .4s ease;
}
.card:hover img{transform:scale(1.035)}
.card::after{
  content:"";position:absolute;inset:0;
  background:linear-gradient(to top,rgba(0,0,0,.55),transparent 38%);
  opacity:0;transition:opacity .35s ease;pointer-events:none;
}
.card:hover::after{opacity:1}
.badge{
  position:absolute;left:10px;top:10px;z-index:2;
  display:inline-flex;align-items:center;gap:6px;
  background:rgba(10,8,14,.66);
  border:1px solid rgba(255,255,255,.1);
  padding:4px 10px;border-radius:999px;
  font-size:11px;letter-spacing:.03em;color:#e9e4dc;
  backdrop-filter:blur(6px);
  -webkit-backdrop-filter:blur(6px);
  opacity:.72;transition:opacity .25s ease;
}
.card:hover .badge{opacity:1}
.badge .score{color:var(--gold);font-weight:500}
.card.hide{display:none}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .card{animation:none;opacity:1;transition:none}
  .card img,.card::after,.badge,.chip,.lb-btn,.to-top{transition:none}
  .card:hover,.card:hover img{transform:none}
}

/* ---------- 灯箱 ---------- */
.lightbox{
  position:fixed;inset:0;z-index:100;
  display:none;align-items:center;justify-content:center;
  background:rgba(8,6,11,.94);
  backdrop-filter:blur(10px);
  -webkit-backdrop-filter:blur(10px);
}
.lightbox.open{display:flex}
.lightbox img{
  max-width:min(94vw,1400px);max-height:86vh;
  border-radius:10px;
  box-shadow:0 20px 80px rgba(0,0,0,.7);
}
.lb-meta{
  position:fixed;left:0;right:0;bottom:20px;
  text-align:center;font-size:13px;color:var(--muted);
  letter-spacing:.06em;
}
.lb-meta .score{color:var(--gold)}
.lb-btn{
  position:fixed;top:50%;transform:translateY(-50%);
  width:46px;height:46px;border-radius:50%;
  border:1px solid rgba(255,255,255,.14);
  background:rgba(20,17,26,.6);color:var(--text);
  font-size:18px;cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  transition:all .25s ease;
}
.lb-btn:hover{border-color:var(--gold);color:var(--gold)}
.lb-prev{left:18px}
.lb-next{right:18px}
.lb-close{
  position:fixed;top:16px;right:18px;transform:none;
}
@media (max-width:640px){
  .lb-btn{width:38px;height:38px;font-size:15px}
  .stats{gap:18px}
}

/* ---------- 回顶部 & 页脚 ---------- */
.to-top{
  position:fixed;right:20px;bottom:24px;z-index:30;
  width:42px;height:42px;border-radius:50%;
  border:1px solid rgba(216,177,106,.4);
  background:rgba(20,17,26,.8);color:var(--gold);
  font-size:16px;cursor:pointer;
  opacity:0;pointer-events:none;
  transition:opacity .3s ease;
}
.to-top.show{opacity:1;pointer-events:auto}
footer{
  padding:34px 20px 46px;
  text-align:center;color:var(--muted);
  font-size:12px;letter-spacing:.08em;
}
footer .rule{margin-bottom:22px}
</style>
</head>
<body>

<header>
  <span class="kicker">Dilraba Dilmurat</span>
  <h1>迪丽热巴<span class="dot"> · </span>影像画廊</h1>
  <p class="sub">精选公开写真、红毯与时尚大片，按高级性感程度排序。点击任意照片进入全屏浏览。</p>
  <div class="stats">
    <div class="stat"><b>__COUNT__</b><span>作品</span></div>
    <div class="stat"><b>__TOPSCORE__</b><span>最高评分</span></div>
    <div class="stat"><b>__UPDATED__</b><span>更新</span></div>
  </div>
  <div class="rule"></div>
</header>

<nav class="toolbar" id="toolbar" aria-label="评分筛选">
__CHIPS__
</nav>

<main class="gallery" id="gallery">
"""

TEMPLATE_TAIL = """</main>

<div class="lightbox" id="lightbox" aria-hidden="true" role="dialog" aria-modal="true" aria-label="照片全屏浏览">
  <img id="lb-img" src="" alt="">
  <div class="lb-meta" id="lb-meta"></div>
  <button class="lb-btn lb-prev" id="lb-prev" aria-label="上一张">&#10094;</button>
  <button class="lb-btn lb-next" id="lb-next" aria-label="下一张">&#10095;</button>
  <button class="lb-btn lb-close" id="lb-close" aria-label="关闭">&#10005;</button>
</div>

<button class="to-top" id="toTop" aria-label="回到顶部">&#8593;</button>

<footer>
  <div class="rule"></div>
  共 __COUNT__ 张 · 按高级性感程度排序 · updated __STAMP__
</footer>

<script>
(function(){
  var cards = Array.prototype.slice.call(document.querySelectorAll('.card'));
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* 入场动画错峰 */
  if(!reduceMotion){
    cards.forEach(function(c,i){ c.style.animationDelay = Math.min(i*18, 500)+'ms'; });
  }

  /* 评分筛选 */
  var chips = document.querySelectorAll('.chip');
  chips.forEach(function(chip){
    chip.addEventListener('click', function(){
      chips.forEach(function(c){ c.classList.remove('active'); });
      chip.classList.add('active');
      var min = parseFloat(chip.dataset.min);
      cards.forEach(function(card){
        card.classList.toggle('hide', parseFloat(card.dataset.score) < min);
      });
    });
  });

  /* 灯箱 */
  var lb = document.getElementById('lightbox');
  var lbImg = document.getElementById('lb-img');
  var lbMeta = document.getElementById('lb-meta');
  var current = -1;
  var lastFocus = null;
  var preloadCache = Object.create(null);

  function visibleCards(){ return cards.filter(function(c){ return !c.classList.contains('hide'); }); }

  function preload(src){
    if(!src || preloadCache[src]) return;
    var img = new Image();
    img.src = src;
    preloadCache[src] = img;
  }

  function show(idx){
    var list = visibleCards();
    if(!list.length) return;
    current = (idx + list.length) % list.length;
    var card = list[current];
    lbImg.src = card.getAttribute('href');
    lbImg.alt = card.querySelector('img').alt || '';
    lbMeta.textContent = '#' + card.dataset.rank + ' / ' + list.length + '  ·  评分 ';
    var s = document.createElement('span');
    s.className = 'score';
    s.textContent = card.dataset.score;
    lbMeta.appendChild(s);
    lb.classList.add('open');
    lb.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    document.getElementById('lb-close').focus();
    /* 预加载相邻原图 */
    preload(list[(current + 1) % list.length].getAttribute('href'));
    preload(list[(current - 1 + list.length) % list.length].getAttribute('href'));
  }
  function close(){
    lb.classList.remove('open');
    lb.setAttribute('aria-hidden', 'true');
    lbImg.removeAttribute('src');
    document.body.style.overflow = '';
    if(lastFocus) lastFocus.focus();
  }

  cards.forEach(function(card){
    card.addEventListener('click', function(e){
      e.preventDefault();
      lastFocus = card;
      show(visibleCards().indexOf(card));
    });
  });
  document.getElementById('lb-prev').addEventListener('click', function(){ show(current-1); });
  document.getElementById('lb-next').addEventListener('click', function(){ show(current+1); });
  document.getElementById('lb-close').addEventListener('click', close);
  lb.addEventListener('click', function(e){ if(e.target === lb) close(); });
  document.addEventListener('keydown', function(e){
    if(!lb.classList.contains('open')) return;
    if(e.key === 'Escape') close();
    if(e.key === 'ArrowLeft') show(current-1);
    if(e.key === 'ArrowRight') show(current+1);
    if(e.key === 'Tab'){
      var focusables = [document.getElementById('lb-close'), document.getElementById('lb-prev'), document.getElementById('lb-next')];
      var i = focusables.indexOf(document.activeElement);
      if(e.shiftKey){
        e.preventDefault();
        focusables[(i <= 0 ? focusables.length : i) - 1].focus();
      } else {
        e.preventDefault();
        focusables[(i + 1) % focusables.length].focus();
      }
    }
  });

  /* 触屏滑动切换 */
  var touchX = null;
  lb.addEventListener('touchstart', function(e){ touchX = e.touches[0].clientX; }, {passive:true});
  lb.addEventListener('touchend', function(e){
    if(touchX === null) return;
    var dx = e.changedTouches[0].clientX - touchX;
    if(Math.abs(dx) > 48) show(current + (dx < 0 ? 1 : -1));
    touchX = null;
  }, {passive:true});

  /* 回顶部 */
  var toTop = document.getElementById('toTop');
  window.addEventListener('scroll', function(){
    toTop.classList.toggle('show', window.scrollY > 900);
  }, {passive:true});
  toTop.addEventListener('click', function(){ window.scrollTo({top:0, behavior: reduceMotion ? 'auto' : 'smooth'}); });
})();
</script>
</body>
</html>
"""


def chip_html(entries):
    thresholds = [
        (0, '全部'),
        (9, '9 分'),
        (8.5, '8.5 分以上'),
        (8, '8 分以上'),
        (7, '7 分以上'),
    ]
    scores = [e['sexiness_score'] for e in entries]
    parts = []
    for i, (mn, label) in enumerate(thresholds):
        n = sum(1 for s in scores if s >= mn)
        active = ' active' if i == 0 else ''
        parts.append(
            f'<button class="chip{active}" data-min="{mn}">{label}<span class="n">({n})</span></button>'
        )
    return '\n  '.join(parts)


def card_html(e, index):
    stem = Path(e['filename']).stem
    thumb480 = f'thumbs/480/{stem}.webp'
    thumb720 = f'thumbs/720/{stem}.webp'
    full = f"images/{e['filename']}"
    eager = index < 8
    loading = 'eager' if eager else 'lazy'
    fetch = ' fetchpriority="high"' if index < 4 else ''
    return (
        f'<a class="card" href="{full}" data-rank="{e["rank"]}" data-score="{e["sexiness_score"]}">'
        f'<span class="badge">#{e["rank"]} <span class="score">{e["sexiness_score"]}</span></span>'
        f'<img src="{thumb720}" srcset="{thumb480} 480w, {thumb720} 720w" '
        f'sizes="(max-width:640px) 50vw, (max-width:1200px) 25vw, 240px" '
        f'width="720" height="1080" loading="{loading}"{fetch} '
        f'alt="迪丽热巴 #{e["rank"]} · 评分 {e["sexiness_score"]}">'
        f'</a>'
    )


def build():
    with open('new_photos.json') as f:
        entries = json.load(f)
    entries = sorted(entries, key=lambda e: e['rank'])

    missing = []
    for e in entries:
        stem = Path(e['filename']).stem
        for w in (480, 720):
            if not Path(f'thumbs/{w}/{stem}.webp').exists():
                missing.append(f'thumbs/{w}/{stem}.webp')
    if missing:
        raise SystemExit(
            f'缺少 {len(missing)} 个缩略图，请先运行：python3 generate_thumbs.py\n'
            f'例如：{missing[0]}'
        )

    stamp = time.strftime('%Y%m%d_%H%M%S')
    updated = time.strftime('%m.%d')
    top = max(e['sexiness_score'] for e in entries)
    og = f"images/{entries[0]['filename']}"

    cards = [card_html(e, i) for i, e in enumerate(entries)]
    chips = chip_html(entries)

    html = (TEMPLATE_HEAD.replace('__CHIPS__', chips)
            + '\n'.join(cards) + '\n' + TEMPLATE_TAIL)
    html = (html.replace('__COUNT__', str(len(entries)))
                .replace('__TOPSCORE__', str(top))
                .replace('__UPDATED__', updated)
                .replace('__STAMP__', stamp)
                .replace('__OG_IMAGE__', og))

    with open('index.html', 'w') as f:
        f.write(html)

    score_dist = Counter(e['sexiness_score'] for e in entries)
    print(f'生成 index.html：{len(entries)} 张卡片')
    print(f'评分分布：{dict(sorted(score_dist.items(), reverse=True))}')


if __name__ == '__main__':
    build()
