# 3D model spec (web AR and print)

The webpage reads its interactive parts from the model files, so the names below must match.
Clinical content (ages, teeth, sources) is in [clinical-check.md](clinical-check.md).

## Files

| Stage | Web (Draco, under 5 MB) | iPhone AR | Print |
|---|---|---|---|
| 1. Pre-op | `models/abg-pre-op.glb` | `models/abg-pre-op.usdz` | STL per part |
| 2. Short-term post-op | `models/abg-short-term.glb` | `models/abg-short-term.usdz` | STL per part |
| 3. Long-term post-op, canine as lateral incisor (crown) | `models/abg-long-term-canine.glb` | `models/abg-long-term-canine.usdz` | STL per part |
| 3. Long-term post-op, implant | `models/abg-long-term-implant.glb` | `models/abg-long-term-implant.usdz` | STL per part |
| 3. Long-term post-op, cantilever bridge | `models/abg-long-term-bridge.glb` | `models/abg-long-term-bridge.usdz` | STL per part |

Stage 3 has one file per choice, because the implant and bridge need the lateral incisor space kept open with the canine in its own place, so the teeth differ. The choice buttons swap the file, so AR shows the chosen one.

Units: metres in the GLB (Blender default), Y up, front of the mouth facing +Z. Unilateral cleft on the same side in all three stages.

## Materials (one per part)

The buttons under the model change these materials. A button only shows if its material is in the model.

| Material name | What it is | Colour (sRGB) | Stages | Button |
|---|---|---|---|---|
| `bone` | Maxilla | `#e6dccb` | all | See-through bone (stages 1 and 2) |
| `teeth` | Erupted teeth (adult and baby) | `#f7f4ee` | all | – |
| `canine` | Unerupted cleft-side adult canine | `#7fb3d5` | 1, 2 | – (seen through the bone) |
| `soft-tissue` | Repaired gum and palate cover (closed shell, 1.5 to 2 mm thick) | `#e79a9a` | 1 (2 optional) | Take off the gum cover |

Under the cover, stage 1 `bone` keeps both the alveolar cleft and a residual bony gap in the hard palate (palate repair closes soft tissue only; see clinical-check.md). Stage 2 graft fills the alveolar cleft and front of the palate; a smaller residual palatal bony gap may stay under the soft tissue.
| `graft` | Bone graft in the alveolar cleft | `#fbf7ef` (lighter, warmer than `bone`) | 2 | – |
| `crown` | Crown or build-up on the canine (lateral incisor shape) | `#f3d27a` on screen; tooth colour in print | 3 canine | Take off the crown |
| `implant-crown` | Lateral incisor crown on the implant | `#f3d27a` | 3 implant | Take off the implant crown |
| `implant-post` | Titanium implant and abutment in the grafted bone | `#9aa3ad` | 3 implant | – (seen when the crown is off) |
| `bridge` | Cantilever resin-bonded bridge: lateral incisor pontic plus one palatal wing on the cleft-side central incisor | `#f3d27a` | 3 bridge | Take off the bridge |

Blender may add `.001` to a duplicated material name; the page accepts `bone.001` as `bone`.

## Numbered dots and views

Add an **Empty** in Blender for each numbered dot, named `hotspot-1`, `hotspot-2` ..., placed on the surface of the part. Numbers match `content/ui-en.json`:

- Pre-op: 1 gap in gum bone, 2 gap in the bone of the hard palate, 3 gum and palate cover, 4 unerupted canine, 5 lateral incisor space, 6 central incisor, 7 baby teeth, 8 first adult molar.
- Short-term: 1 bone graft, 2 unerupted canine, 3 lateral incisor space, 4 central incisor, 5 baby teeth, 6 first adult molar.
- Long-term (each file has only its own dots): 1 grafted bone (all), 2 canine in lateral incisor place (canine), 3 crown (canine), 4 first premolar in canine place (canine), 5 implant crown (implant), 6 bridge (bridge), 7 canine in its own place (implant, bridge), 8 central incisor (all), 9 second molar (all).

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
- Stage 3, one printed base with a removable cleft-side segment (canine to central incisor area), held by a dovetail slide so the segments swap:
  - Segment A, canine as lateral incisor: canine in the lateral incisor space, first premolar in the canine place. Crown is a friction cap over a reduced canine with a D-shaped key (shows recontouring and a crown).
  - Segment B, space open: canine in its own place and a gap for the lateral incisor, with a 3 to 4 mm D-shaped socket in the grafted bone.
  - Implant (fits segment B): post printed in grey, friction fit in the socket; crown is a friction cap on the post's D-shaped abutment, so it comes off to show the post.
  - Bridge (fits segment B): pontic with one 0.8 to 1 mm palatal wing that clips onto the back of the cleft-side central incisor (snap over the cingulum, 0.10 mm resin / 0.20 mm FDM clearance). One wing only, as in a cantilever resin-bonded bridge.
- Print a test coupon in each material first. These are engineering defaults, not values from the clinical literature.

## Export

1. Blender: File > Export > glTF Binary (.glb), selected parts and empties, +Y up.
2. Compress: `npx @gltf-transform/cli@4.1.1 draco in.glb models/abg-<stage>.glb`.
3. USDZ for iPhone AR: Reality Converter (macOS) or Blender USD export, then zip as `.usdz`.
4. Run `python3 tools/build.py`, then open the page and check the dots and buttons.
