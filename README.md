# ABG

Web pages with web AR 3D models for the study "Seeing the stages: comparing 2D, augmented reality, video and 3D printed education materials to explain alveolar bone grafting in cleft lip and palate" (Aichi Gakuin University and Nagoya University). Three stages in clinical order: before surgery, about 3 months after, and years later. The model shows a left-sided cleft with no left lateral incisor (agenesis).

## Site layout

- `index.html`: home page. Choose the AR web page or the narrated video, in English or Japanese.
- `en/pre-op/`, `en/short-term/`, `en/long-term/` (and the same under `ja/`): one page per stage, with a 1-2-3 stepper, the 3D model, labels, preset views, AR, the "Take off the gum" animation, patient text and sources. `en/` and `ja/` forward to stage 1.
- `video/en/`, `video/ja/`: narrated video page (one video per language, one chapter per stage). The video is not made yet.
- Hosted on GitHub Pages from `main` (Settings > Pages > Deploy from a branch > `main` / root).
- Design: one 640px column like the wisdom tooth site, neutral slate and steel blue, light mode by default with a dark mode toggle (kept for the browser tab only). Aichi Gakuin University logo first, then Nagoya University.

## Study materials (the same content in all four)

- **A. 2D information sheet:** `sheet/<lang>/<stage>/` (built by `tools/build.py` from the same `content/` text) and print-ready A4 PDFs `sheet/abg-sheet-<n>-<stage>-<lang>.pdf` (`node tools/sheet/pdf.js`). Only sentences about on-screen buttons change (`SHEET_SWAP` in `tools/build.py`). Pictures: `node tools/sheet/render.js` renders the model with the web page labels into `images/sheet-*.png`. Stage 2 and 3 pictures are marked placeholders until those models exist.
- **B. AR web page:** `en/`, `ja/`.
- **C. 3D printed model and D. narrated video:** narration script `content/narration.md` (one part per stage, 45 s or less each). `python3 tools/narration.py` writes `video/script-en.json` and `video/script-ja.json` (chapters, scenes, sentences, line labels with the web page names) for the text-to-speech voice and subtitles.
- **Study files (not on the web page):** `study/recruitment-flyer/` (A4 flyer EN/JA, `build_flyer.py` adds the form QR codes), `study/ms-forms/` (Microsoft Forms text EN/JA, Japanese review copy, setup guide), `study/narration/` (narration review copy). Build with the scripts in each folder.

## Text and sources

- Patient text: `content/<stage>-en.html` and `content/<stage>-ja.html`, with citations as `[[key]]` (keys in `content/references.json`). Buttons and short strings: `content/ui.json`. Labels on the model: `H` in `tools/build.py`.
- Run `python3 tools/build.py` to write every page. Do not edit pages under `en/`, `ja/` or `video/` by hand.
- Checks: [patient-education-toolkit](https://github.com/CBCT-2026/patient-education-toolkit) with `.patient-info.json` (`pitk check`). The text speaks to the reader as "you". English: Flesch-Kincaid grade 1.4 to 1.5 per page, SMOG 4.5 to 5.6. Japanese: kanji taught by grade 6 only, jReadability 4.1 to 4.3. Japanese needs a native-speaker check.

## 3D models

- `models/abg-placeholder.glb` / `.usdz`: the placeholder pre-op model (ABG-pre-op-example), used on all three stage pages until the stage models are built. Made with `python3 tools/recolour_model.py ABG-pre-op-example.glb models/abg-placeholder.glb` (bone, tooth and gum colours; gum part animations "remove" and "replace"), then `python3 tools/make_usdz.py models/abg-placeholder.glb models/abg-placeholder.usdz` (needs `pip install trimesh pygltflib usd-core rtree`).
- To add a stage model: put `abg-<stage>.glb` and `.usdz` in `models/` and point that stage at it in `tools/build.py`. The gum button works on any model with a material named `gum` and animations named `remove` and `replace`. Part and material plan: `docs/model-spec.md`.

## Licences

- 3D viewer: `@google/model-viewer` 3.5.0 (Apache 2.0), loaded from jsDelivr.
- `images/aichi-gakuin-logo.png` and `images/nagoya-logo.png` belong to Aichi Gakuin University and Nagoya University. They are **not** covered by any open licence of this project. Use them only as each university's brand guidelines allow.
