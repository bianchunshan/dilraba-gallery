# AGENTS.md

## Cursor Cloud specific instructions

This repository is a **purely static image gallery website**. There is no package
manager, build system, test suite, linter, or CI. It contains only static assets:

- `index.html` — the primary gallery page (a ranked Dilraba photo gallery).
- `images/` — the JPGs referenced by `index.html`.
- `new_photos.json` — metadata (ranking, score, category) for the gallery entries.
- `CURATION_STANDARD.md` — the human/vision curation policy used to build the gallery.
- `candidate-500-v2/` — a secondary gallery page (`index.html` + manifest). Note: its
  `images/` folder is **not committed** (it references large generated `.png` files
  that live outside the repo), so that page shows broken images when served locally.
  The primary, fully-working product is the root `index.html`.

### Running the site (dev)

There is nothing to install. Serve the repo root over HTTP and open the gallery:

```
python3 -m http.server 8000    # run from the repo root
# then open http://localhost:8000/
```

Serve over HTTP rather than opening `file://` so relative `images/...` paths and
lazy-loading behave like production (the site is normally deployed as static hosting,
e.g. GitHub Pages). Node's `npx serve` works equally well if preferred.

### Sanity check (there are no automated tests)

The curation pipeline maintains an invariant: the number of `<img>` references in
`index.html` equals the number of files in `images/` equals the number of entries in
`new_photos.json`. Quick check:

```
grep -o 'img src="images/' index.html | wc -l          # HTML refs
ls images/*.jpg | wc -l                                 # image files
python3 -c "import json;print(len(json.load(open('new_photos.json'))))"  # JSON entries
```

All three should match (currently 205).
