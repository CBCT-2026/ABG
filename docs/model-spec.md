# 3D model spec (web AR and print)

The webpage reads its interactive parts from the model files, so the names below must match.
Clinical content (ages, teeth, sources) is in [clinical-check.md](clinical-check.md).

## Files

| Stage | Web (Draco, under 5 MB) | iPhone AR | Print |
|---|---|---|---|
| 1. Pre-op | `models/abg-pre-op.glb` | `models/abg-pre-op.usdz` | STL per part |
| 2. Short-term post-op | `models/abg-short-term.glb` | `models/abg-short-term.usdz` | STL per part |
| 3. Long-term post-op | `models/abg-long-term.glb` | `models/abg-long-term.usdz` | STL per part |

Units: metres in the GLB (Blender default), Y up, front of the mouth facing +Z. Unilateral cleft on the same side in all three stages.

## Materials (one per part)

The buttons under the model change these materials. A button only shows if its material is in the model.

| Material name | What it is | Colour (sRGB) | Stages | Button |
|---|---|---|---|---|
| `bone` | Maxilla | `#e6dccb` | all | See-through bone (stages 1 and 2) |
| `teeth` | Erupted teeth (adult and baby) | `#f7f4ee` | all | – |
| `canine` | Unerupted cleft-side adult canine | `#7fb3d5` | 1, 2 | – (seen through the bone) |
| `soft-tissue` | Repaired gum and palate cover (closed shell, 1.5 to 2 mm thick) | `#e79a9a` | 1 (2 optional) | Take off the gum cover |
| `graft` | Bone graft in the alveolar cleft | `#fbf7ef` (lighter, warmer than `bone`) | 2 | – |
| `crown` | Crown or build-up on the canine (lateral incisor shape) | `#f3d27a` on screen; tooth colour in print | 3 | Take off the crown |
| `replacement-tooth` | Optional: implant crown or bonded bridge in the lateral incisor space (other choice) | `#f3d27a` | 3 | Show the other choice |

Blender may add `.001` to a duplicated material name; the page accepts `bone.001` as `bone`.

## Numbered dots and views

Add an **Empty** in Blender for each numbered dot, named `hotspot-1`, `hotspot-2` ..., placed on the surface of the part. Numbers match `content/ui-en.json`:

- Pre-op: 1 gap in gum bone, 2 gum and palate cover, 3 unerupted canine, 4 lateral incisor space, 5 central incisor, 6 baby teeth, 7 first adult molar.
- Short-term: 1 bone graft, 2 unerupted canine, 3 lateral incisor space, 4 central incisor, 5 baby teeth, 6 first adult molar.
- Long-term: 1 grafted bone, 2 canine in lateral incisor place, 3 crown, 4 first premolar in canine place, 5 central incisor, 6 second molar.

Optional empties `view-canine` (stages 1 and 2) and `view-front` (stage 3) set where the zoom buttons look.
`python3 tools/build.py` reads the empties and writes the dot positions into the pages. Dots without an empty are left out.
Export with **Include > Custom Properties** off and **Punctual Lights** off; empties are exported by default.

## Teeth at each stage

See the table in [clinical-check.md](clinical-check.md#teeth-each-model-should-show-unilateral-cleft). In short: stage 1 and 2 are mixed dentition (8 to 11 years) with the cleft-side canine unerupted and root about half formed; stage 3 is permanent dentition (15 to 18 years) without wisdom teeth, canine in the lateral incisor space, first premolar in the canine place, braces off.

## Removable parts for the print

| Joint | Resin (SLA/DLP) | FDM (PLA/PETG) |
|---|---|---|
| Friction peg in hole (D-shaped so it fits one way) | 0.10 to 0.15 mm per side | 0.20 to 0.25 mm per side |
| Dovetail slide (10 to 15° flank, along the arch) | 0.10 mm per side | 0.20 mm per side |
| Minimum wall around a socket | 1.2 mm | 1.6 mm |

- Stage 1 soft tissue cover: flexible resin or TPU, 1.5 to 2 mm thick, 2 or 3 pegs into the palate.
- Stage 2 graft: dovetail sliding up into the cleft from below.
- Stage 3 crown: friction cap over a reduced canine with a D-shaped key.
- Print a test coupon in each material first. These are engineering defaults, not values from the clinical literature.

## Export

1. Blender: File > Export > glTF Binary (.glb), selected parts and empties, +Y up.
2. Compress: `npx @gltf-transform/cli@4.1.1 draco in.glb models/abg-<stage>.glb`.
3. USDZ for iPhone AR: Reality Converter (macOS) or Blender USD export, then zip as `.usdz`.
4. Run `python3 tools/build.py`, then open the page and check the dots and buttons.
