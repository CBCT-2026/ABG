ABG education models (Stages 1-3) - file notes
================================================

Files (Desktop)
- ABG-stage-1.blend / .glb / _draco.glb, ABG-stage-1-STL\, ABG-stage-1-renders\
- ABG-stage-2.blend / .glb / _draco.glb, ABG-stage-2-STL\, ABG-stage-2-renders\
- ABG-stage-3.blend / .glb / _draco.glb, ABG-stage-3-STL\, ABG-stage-3-renders\
- Web copies (metres, +Y up, Draco, about 105-130k triangles each, no animations):
  abg-1-pre-op.glb      nodes and materials: bone, teeth, soft-tissue, canine
  abg-2-short-term.glb  nodes and materials: bone, teeth, graft, soft-tissue, braces
  abg-3-long-term.glb   nodes and materials: bone, teeth, graft, soft-tissue,
                        option-implant, option-bridge, option-denture (all in seated position)
  braces, option-implant and option-denture carry their part colours as vertex colours.
- Archive of the old 3-month Stage 2: ABG-stage-2-3month-archive.blend / .glb / _draco.glb,
  ABG-stage-2-3month-archive-STL\, ABG-stage-2-3month-archive-renders\

Stages
- Stage 1, pre-graft, age 9-10, repaired UCLP (left): open alveolar cleft, small anterior
  oronasal opening (palatal side), mixed dentition, 23 unerupted in the labial window.
- Stage 2, about 2-3 years after the graft, during fixed orthodontics (age about 12-13):
  graft integrated, 23 erupted beside the graft, second molars erupting (partly covered by
  gum), lateral-incisor-width space at 22, removable braces strip with a false 22 on the
  wire. The canine window is closed.
- Stage 3, braces off (age 16+): canine window closed, empty 22 space by default, three
  removable options on one shared keyed seat in the 22 space: b implant + crown,
  c one-wing resin-bonded (Maryland) bridge, d removable partial denture.
  The impacted-canine option has been dropped.

Units
- STL files are in millimetres. Blender / GLB files are in metres.
- The models are about 1.5 x life size (bone about 97 mm wide).

Soft-tissue overlay (all stages): TPU design
- Print in TPU 95A, 100 % infill (solid), 2-3 walls. All other parts are rigid.
- One insertion path, along (0, 0.6, 0.8) in Blender coordinates (Z = tooth long axis,
  Y = palatal). Undercuts are blocked out, except a small grip at the tooth necks:
  the overlay passes over the necks with up to about 0.4 mm of flex (model scale)
  and sits passively at rest (contact under 0.1 mm). Around the first and second
  molars the gum flaps flex up to about 1.5 mm (model scale) when it is taken off.
  If this is too tight on the print, trim the flaps behind the molars slightly.
- Gum is about 1.2 mm thick at the tooth margins and about 1.8 mm over the bone and palate.
  Nothing presses on the bone.
- Two locating pins (no magnets).
- Stage 1: flat skin over the canine window (no grip there), so the window stays empty.
  The Stage 3 overlay has a hole over the 22 seat; the Stage 2 overlay does not.

Removable rigid parts
- Stage 2: braces strip (brackets, archwire to the first-molar tubes, false 22). It comes
  out along (0, -0.2, -1). No brackets on the erupting second molars.
- Stage 3: b implant body + abutment and crown 22, c Maryland bridge 22 (wing on 21),
  d partial denture (palatal plate, clasps on 16 and 26). All come out along (0, -0.2, -1).
- All removable parts are checked against the overlay, bone, graft and teeth: no overlap
  at rest (under 0.1 mm) and a clear path out.

STL files per stage
- maxilla+graft+teeth (one print) and maxilla+teeth_without-graft (to print the graft
  separately in another colour), graft, soft-tissue-overlay_TPU, removable parts,
  base-plate (same footprint for all stages).

Licence and credit
- Tooth geometry is derived from BodyParts3D, (c) The Database Center for Life Science,
  licensed under CC BY-SA 2.1 Japan. Credit "BodyParts3D, (c) The Database Center for Life
  Science, CC BY-SA 2.1 JP" wherever the models or images are shown. Derived models carry
  the same licence.
- The maxilla base was adapted by hand in Blender from Luke's pre-op model (abg-pre-op_v6).
