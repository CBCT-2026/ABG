ABG education models (Stages 1-3), v3 - file notes
====================================================

Files (Desktop)
- ABG-stage-N.blend / .glb / _draco.glb, ABG-stage-N-STL\, ABG-stage-N-renders\  (N = 1, 2, 3)
- Web copies (metres, +Y up, Draco, about 110-135k triangles each, no animations):
  abg-1-pre-op.glb      nodes and materials: bone, teeth, soft-tissue, canine
  abg-2-short-term.glb  nodes and materials: bone, teeth, graft, soft-tissue, braces (incl. false 22)
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
  partly erupted; 21 part-derotated; removable braces strip with a false 22 on a flat archwire.
- Stage 3, braces off (16+): arch aligned, canine window closed, ridge at 22 slightly lower and
  narrower, empty-space default = gum-coloured ridge plug (option-none); options on one keyed seat:
  b implant + crown (visible titanium collar), c one-wing resin-bonded (Maryland) bridge on 21,
  d Hawley-type removable partial denture (Adams clasps 16/26, labial bow).

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
