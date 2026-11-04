# ABG models v3: parts per stage

Scale about **1.5 x life**. STL in mm, GLB in metres (+Y up). Blender axes: Z = tooth long axis (crowns at -Z, base plate at +Z), Y = palatal, X = patient's left (cleft side). All values are model mm.

`ABG-stage-N_draco.glb` contains every part seated (all Stage 3 options at once). Renders: `stageN-ABG-stage-N_<view>_<state>.png`.

## All stages

| Part | Material | Loose? | Path | Fit |
|---|---|---|---|---|
| Body: bone + teeth + base plate (+ Stage 1 canine) | PLA | no, one piece | n/a | plate-down print |
| Gum overlay | TPU 95A | yes | on along (0, 0.6, 0.8), off the opposite way | 0.35 mm gap to bone, ~0.07-0.13 mm contact at rest at the necks, walls ≥ 1.2 mm; 2 PLA pins Ø3 x 2 mm on the palate, holes +0.15 mm |

Overlay deflection needed on removal (max depth the gum must flex over each tooth while sliding off, all teeth, model mm):

| Stage | Incisors | Canines | Premolars / primary molars | First molars | Second molars | Bone |
|---|---|---|---|---|---|---|
| 1 | 2.0-2.7 | 3.5-4.0 | 3.6-4.1 | 4.4-4.6 | - | 0.3 |
| 2 | 2.0-2.6 | 2.3-3.1 | 4.2-4.5 | 4.3-4.5 | 1.1-1.2 | 0.3 |
| 3 | 2.0-2.6 | 3.1-3.3 | 4.2-4.5 | 4.3-4.5 | 5.7-6.0 | 0.3 |

These are the interdental papillae and palatal cuffs passing the contact points and the crown bulge. Slits: behind 16/26 (Stage 1 also between all primary teeth); behind 17/27 and between 16/17, 26/27 (Stages 2-3).

## Stage 1 (pre-graft, 9-10 y)
- Body includes the unerupted 23 (fused, not removable; separate node only in the web file).
- Overlay: flat skin over the canine window, opening at the anterior oronasal fistula.

## Stage 2 (2-3 y after graft, braces, 12-13 y)
| Part | Material | Path | Fit |
|---|---|---|---|
| Graft plug | PLA contrast | out labially along (0.05, -1, 0) | 0.2 mm clearance, 3° taper, finger lip; path clear |
| Braces strip (brackets, flat 2.0 x 1.2 mm wire, molar tubes, wire tails 2.2 mm, false 22) | PLA | clips off labially | bracket bases on the teeth; 0.1-0.7 mm snap over the premolars (retention) |

## Stage 3 (braces off, 16+)
| Part | Material | Path | Fit |
|---|---|---|---|
| Graft plug with the seat | PLA contrast | as Stage 2 | seat: double-D bore Ø3.2, flats 2.3 apart, 9 mm deep, spot-faced for the collar |
| b Implant body + collar + post | PLA grey | along the seat axis (0, -0.196, -0.981) | 0.25 mm clearance, 2 crush ribs 0.12 mm, collar Ø4.6 stops on the graft; body ends 0.3 mm above the floor |
| b Crown 22 | PLA white | off the post | 0.25 mm gap on the post, sits on the collar 1 mm below the gum margin |
| option-none ridge plug | TPU / pink PLA | as implant | same peg; cap flush with the overlay |
| c Maryland bridge | PLA | (0, 0.1, -0.995) | wing 1.3 mm on the palatal of 21, palatal connector; ≤0.07 mm drag on 21 |
| d Hawley partial denture | pink PLA + painted wires | (0, 0, -1) | Ø1.8 Adams clasps 16/26 and labial bow; 0.1-0.4 mm undercut engagement (retention) |

## Known limits
- Overlay flaps must still flex 4-6 mm over the molars and premolars (table above); TPU 95A should do this with the slits, but test the cleft-side half first.
- Seat is Ø3.2 (not Ø5.2): the graft is only 5.1-5.5 mm wide at the crest, so Ø3.2 with flats keeps walls ≥ 1.2 mm.
- Maryland connector is palatal but a sliver may show in the 21/22 embrasure in some views.
- Stage 1: one premolar bud tip may show as a dot on the labial bone with the overlay off.
- Graft texture is web-only; use fuzzy skin when printing.
- Tooth geometry from BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 JP.
