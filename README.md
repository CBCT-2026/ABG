# ABG

Web pages with web AR 3D models for the study "Seeing the stages: comparing 2D, augmented reality, video and 3D printed education materials to explain alveolar bone grafting in cleft lip and palate" (Aichi Gakuin University and Nagoya University). Three stages in clinical order: before surgery, about 3 months after, and years later. The model shows a left-sided cleft with no left lateral incisor (agenesis).

## Site layout

- `index.html`: home page. Choose the AR web page or the narrated video, in English or Japanese. At the bottom: buttons to the study's Microsoft Forms (information sheet and survey; paste the links into `FORM_EN` and `FORM_JA` in `tools/build.py`), and a QR code to this home page that opens full screen when tapped (`images/qr-home.svg`, made by `tools/make_qr.py`).
- **Device check:** each stage page tells touch screens to swipe and pinch, and mouse users to drag and scroll. In study mode, the time-up screen shows the device (phone, tablet or computer, touch or mouse, screen size) for the researcher to note on the form. Nothing is sent anywhere.
- `en/pre-op/`, `en/short-term/`, `en/long-term/` (and the same under `ja/`): one page per stage, with a 1-2-3 stepper, the 3D model, labels, preset views, AR, the "Take off the gum" animation, patient text and sources. `en/` and `ja/` forward to stage 1.
- `video/en/`, `video/ja/`: narrated video page (one video per language, one chapter per stage). The video is not made yet.
- **Study mode:** open stage 1 with `?study=1&t=<seconds>`, for example `en/pre-op/?study=1&t=120`. One fixed viewing time covers all three stage pages in that browser tab. A countdown shows in the corner, the language switch and home link are hidden, and when time is up a full-page message asks the participant to tell the researcher. Set `t` to the viewing time chosen in the pilot.
- **Start again:** the button at the bottom of each stage page resets everything for the next participant (light mode, labels on, gum part on, stage 1, and a fresh timer in study mode).
- Same content in every material (sheet, AR page, print, video): `docs/feature-parity.md`.
- Hosted on GitHub Pages from `main` (Settings > Pages > Deploy from a branch > `main` / root).
- Design: one 640px column like the wisdom tooth site, neutral slate and steel blue, light mode by default with a dark mode toggle (kept for the browser tab only). Aichi Gakuin University logo first, then Nagoya University.

## Text and sources

- Patient text: `content/<stage>-en.html` and `content/<stage>-ja.html`, with citations as `[[key]]` (keys in `content/references.json`). Buttons and short strings: `content/ui.json`. Labels on the model: `H` in `tools/build.py`.
- Run `python3 tools/build.py` to write every page. Do not edit pages under `en/`, `ja/` or `video/` by hand.
- Every pull request runs `.github/workflows/check.yml`: it rebuilds the pages (they must match `content/`) and runs `pitk check`. A red check means fix before merging.
- Checks: [patient-education-toolkit](https://github.com/CBCT-2026/patient-education-toolkit) with `.patient-info.json` (`pitk check`). The text speaks to the reader as "you". English: Flesch-Kincaid grade 1.4 to 1.5 per page, SMOG 4.5 to 5.6. Japanese: kanji taught by grade 6 only, jReadability 4.1 to 4.3. Japanese needs a native-speaker check.

## 3D models

- `models/abg-placeholder.glb` (Draco-compressed, 62 KB; decoder served from `vendor/draco/`) / `.usdz`, and `abg-placeholder-poster.webp` (shown while the 3D model loads): the placeholder pre-op model (ABG-pre-op-example), used on all three stage pages until the stage models are built. Made with `python3 tools/recolour_model.py ABG-pre-op-example.glb models/abg-placeholder.glb` (bone, tooth and gum colours; gum part animations "remove" and "replace"), then `npx @gltf-transform/cli@4.1.1 draco` on the .glb, then `python3 tools/make_usdz.py models/abg-placeholder.glb models/abg-placeholder.usdz` (needs `pip install trimesh pygltflib usd-core rtree`).
- To add a stage model: put `abg-<stage>.glb` and `.usdz` in `models/` and point that stage at it in `tools/build.py`. The gum button works on any model with a material named `gum` and animations named `remove` and `replace`. Part and material plan: `docs/model-spec.md`.

## Licences

- Draco decoder in `vendor/draco/` (from three.js r163, Apache 2.0).
- 3D viewer: `@google/model-viewer` 3.5.0 (Apache 2.0), loaded from jsDelivr.
- `images/aichi-gakuin-logo.png` and `images/nagoya-logo.png` belong to Aichi Gakuin University and Nagoya University. They are **not** covered by any open licence of this project. Use them only as each university's brand guidelines allow.
