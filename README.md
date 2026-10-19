# ABG

Patient education webpages with web AR 3D models for the Alveolar Bone Graft (ABG) Education Models Study, Nagoya University. Three stages of alveolar bone grafting for a cleft lip and palate: before the operation, soon after it, and years later after braces.

## Site layout

- `index.html`: language choice. The QR code points here.
- `en/`, `ja/`: home page for each language, with one button per stage, in clinical order.
- `en/pre-op/`, `en/short-term/`, `en/long-term/` (and the same under `ja/`): one page per stage, each with its own 3D model, numbered dots, removable-part buttons, patient text and sources. Each page links to the stages before and after it.
- Hosted on GitHub Pages from `main` (Settings > Pages > Deploy from a branch > `main` / root).

## Patient text and sources

- Page strings, numbered dots, buttons and colour key: `content/ui-en.json`, `content/ui-ja.json`.
- Patient text for each stage: `content/<stage>-en.html`, `content/<stage>-ja.html`, with citations as `[[key]]` (keys in `content/references.json`).
- Run `python3 tools/build.py` to write all pages. Do not edit the pages under `en/` and `ja/` by hand.
- Text is the same in every format (webpage, pamphlet, print card); the pamphlet and print card will be built from these same files.
- Clinical sequence, Australian ages and sources: `docs/clinical-check.md`.

## Checks

- `python3 tools/readability.py`: Flesch-Kincaid grade of every English section (`tools/readability-report.md`). Every text section is grade 6 or below. Page titles score higher only because of the term "alveolar bone grafting".
- `python3 tools/wording_check.py`: no "you/your" in English; no あなた or 私 and only kanji taught by grade 6 (MEXT 2020 list) in Japanese.
- Needs `pip install textstat==0.7.3 beautifulsoup4 numpy`.

## 3D models

Put the models in `models/` as `abg-<stage>.glb` (Draco, under 5 MB) and `abg-<stage>.usdz`, then run `tools/build.py`. Part names, numbered-dot empties, colours, teeth per stage and print fits are in `docs/model-spec.md`. Until a stage's model is added, its page says the model is not ready yet.

## Licences

- Draco decoder in `vendor/draco/` (from three.js r163, Apache 2.0).
- 3D viewer: `@google/model-viewer` 3.5.0 (Apache 2.0), loaded from jsDelivr.
- No Nagoya University logo is used. Images, if added, must be CC0, CC BY or CC BY-SA, credited.
