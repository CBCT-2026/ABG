ABG education models (Stages 1-3), v3 - file notes
====================================================

Files (Desktop)
- ABG-stage-N.blend / .glb / _draco.glb, ABG-stage-N-STL\, ABG-stage-N-renders\  (N = 1, 2, 3)
- Web copies (metres, +Y up, Draco, about 110-135k triangles each, no animations):
  abg-1-pre-op.glb      nodes and materials: bone, teeth, soft-tissue, canine
  abg-2-short-term.glb  nodes and materials: bone, teeth, graft, soft-tissue, braces (no pontic)
  abg-3-long-term.glb   nodes and materials: bone, teeth, graft, soft-tissue, option-implant,
                        option-bridge, option-denture, option-none (all in seated position)
  soft-tissue, braces, option-implant/bridge/denture carry their part colours as vertex colours
  (gum, paler scar lines, darker alveolar mucosa; steel/titanium; acrylic).
- Archive of the old 3-month Stage 2: ABG-stage-2-3month-archive.*

Scale and units
- About 1.5 x life size (bone about 97 mm wide). STL in millimetres; Blender/GLB in metres.

Stages
- Stage 1, pre-graft, age 9-10, repaired UCLP (left): teardrop alveolar cleft (about 7.5 mm at the
  crest, narrowing to the nasal floor), narrow residual palatal gap behind it, lesser segment slightly
  rotated and raised (small step at the cleft); mixed dentition with primary-form 53/63/54/64/55/65,
  lateral-size 12, rotated 21; 23 high over the 63 root at the cleft margin, about half its root
  formed with an open apex, crown seen through the labial window.
- Stage 2, about 2-3 years after the graft, during fixed orthodontics (age about 12-13): graft
  integrated (full height), 23 erupted through the graft about 1 mm short of 13, second molars
  partly erupted; 21 part-derotated; removable braces strip (brackets 13-16, 11/12, 21-26, flat archwire straight across the open 22 space, no pontic).
- Stage 3, braces off (16+): arch aligned, canine window closed, ridge at 22 slightly lower and
  narrower, empty-space default = gum-coloured ridge plug (option-none); options on one keyed seat:
  b implant + crown (visible titanium collar), c one-wing resin-bonded (Maryland) bridge on 21,
  d single-tooth removable denture: small palatal plate with the 22 pontic and two hidden palatal ball clasps (11/21 and 23/24 embrasures); nothing but the tooth shows from the front.

Parts and colours (print)
- Body (one piece, PLA bone colour, plate-down): bone + teeth + base plate; Stage 1 also the
  unerupted canine (fused - it does not come out). Paint or multi-colour the teeth if wanted.
- Graft plug (Stages 2-3, PLA in a contrasting colour, e.g. #C9A86A on #D3C29E bone): slides in from
  the labial along one straight path, 3-degree taper, 0.2 mm clearance, small finger lip. Use Bambu
  Studio "fuzzy skin" for the graft texture (the 0.2-0.4 mm web texture will not print).
- Gum overlay (all stages): TPU 95A, 100 % infill, 2-3 walls, at least 1.2 mm thick everywhere.
  Two PLA locating pins (3 mm, 0.3 mm draft) on the palate bone; holes in the TPU have 0.15 mm
  clearance. Slits behind the last molars (and between the Stage 1 primary teeth) let the flaps open.
- Stage 2 braces strip (PLA grey): flat 2.0 x 1.2 mm archwire, brackets, molar tubes, false 22.
- Stage 3: implant (PLA grey) with a double-D peg (Ø3.2, flats 2.3 apart, 0.25 mm clearance, two
  0.12 mm crush ribs) and a Ø4.6 collar that stops on the graft (shoulder); crown (PLA white) on the
  post with 0.25 mm gap; option-none plug (TPU or pink PLA) with the same peg; Maryland bridge (PLA
  white, wing 1.3 mm); Hawley denture (pink PLA plate, Ø1.8 mm clasps/bow - paint steel colour).

Tolerance coupon (print this first): ABG-stage-3-STL\ABG-tolerance-coupon_block.stl and three pegs
with 0.15 / 0.20 / 0.30 mm clearance per side. The coupon uses the real seat (double-D, Ø3.2); pick
the clearance that fits snugly and tell me if it is not 0.25 mm.

Print orientation
- Body: base plate down. Overlay: rim down, tree supports, 0.25 mm Z gap. Implant: lying on a
  D-flat. Crown, bridge, false 22, plug: with brim. Graft plug: labial face up.

Use
- Insert: overlay along (0, 0.6, 0.8) (Blender axes), then graft is already in, then options/braces.
  Remove: all rigid parts first (braces / options), then the overlay, then the graft plug.

First test print (suggested): cleft-side half of Stage 3 - body (bone + graft seat + base strip) in
PLA, the matching piece of the TPU overlay, implant + crown, and the coupon.

Rough budget: PLA about 250-300 g for all three stages (about 6-8 EUR), TPU about 80-100 g
(about 3-4 EUR); print time about 30-40 h in total.

Licence and credit
- Tooth geometry derived from BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 JP.
  Credit wherever the models or images are shown. Derived models carry the same licence.
- Maxilla base adapted by hand in Blender from Luke's pre-op model (abg-pre-op_v6).

v3.3 notes
- Gum line (Stages 2-3): exposed clinical crowns, model mm (life x 1.5): centrals 15.6, laterals 13.5, canines 15.6,
  premolars 12.0, first/second molars 9.8 (Stage 2 second molars 3.0, partly erupted). Bone crest 1.7 mm apical to the
  margin; zenith 0.6 mm distal on centrals and canines; papillae fill the embrasures up to ~5.5 mm coronal of the margins.
- Stage 3 implant: one coaxial assembly on the 22 crown axis; abutment collar flares from the Ø4.6 platform to the crown
  outline at the gum margin, the crown is cut at the same margin plane (no step).
- Build scripts: Desktop\ABG-scripts (each step runs in a background Blender: python run_step.py in.blend step.py out.blend).

v3.4 notes (Stage 1)
- Palate: one continuous bone plate. The round hole behind 22 and the small palatal dimples are closed; the alveolar
  cleft stays a notch through the alveolus only (no residual palatal opening). The unerupted 23 now sits 4 mm higher
  along its long axis, so its crown is fully inside bone on the palatal side and is seen only through the labial window.
- Overlay: one closed TPU skin over the palate (no fistula hole), scar line kept. Over the canine window it continues
  the neighbouring bone contour (convex, no crease), 2.4-5.0 mm thick; the inside bridges the window (no grip in it).
  Only openings: the two pin holes.
- Stage 1 renders now include a palatal view (overlay on/off) and an into-cleft view.
- Stages 2 and 3: palatal bone checked; there is no pin-socket dimple (the pins sit flush), so these are unchanged.

Stage 3b - canine substitution (left), alternative to Stage 3 options
- Files: ABG-stage-3b-substitution.blend, ABG-stage-3b.glb / _draco.glb, ABG-stage-3b-STL\, ABG-stage-3b-renders\
  (front, both 3/4, occlusal; overlay on/off). Web: abg-3b-substitution.glb (nodes/materials bone, teeth, graft, soft-tissue).
- Built from final Stage 3; right side unchanged. No options, no appliances, no implant seat.
- 23 moved mesially into the 22 space, contact with 21 (0.1 mm), reshaped as a lateral: cusp reduced to a flat incisal
  edge with rounded corners, labial prominence and cingulum reduced (labio-palatal x0.62 at the edge to x0.87 cervically),
  mesio-distal x0.90; incisal edge level with the right lateral (12). Gum margin set midway between 21 and 24
  (exposed crown 13.1 model mm; 21 15.6, 24 12.0).
- 24 in the canine position, rotated 12 deg mesio-labially; 25, 26, 27 mesialised about 11 model mm each (one tooth
  unit; molars finish in a Class II relationship on this side); all contacts closed (0.1 mm).
- Gum margins and papillae follow the new tooth positions; continuous scalloped crest; root cover shells; slits between and
  behind the second molars.
- Graft: same removable plug and colour (#C9A86A), remodelled. It is the bone around and labial of the moved 23 root
  (0.3 mm clearance round the root), flush with the bone surface, and slides out labially along the same tapered
  socket. Everything palatal of the roots stays as bone.
- Overlay: same TPU design, pins, insertion path (0, 0.6, 0.8) and base plate.
