# ABG models: parts per stage

All models are about **1.5 x life size** (bone about 97 mm wide). STL files are in mm; GLB files are in metres (+Y up).
Blender axes used below: Z = tooth long axis (crowns point to -Z, the base plate is at +Z), Y = palatal, X = patient's left (cleft side).
All measurements are at model scale.

The `ABG-stage-N_draco.glb` files contain every part in its seated position, with the overlay and all options shown together.
Renders: `stageN-ABG-stage-N_<view>_<state>.png` (front, left three-quarter, occlusal; Stage 1 also into-cleft).

## Common to all stages

| Part | Material | Fixed / removable | Path | Clearance and grip |
|---|---|---|---|---|
| Maxilla + teeth (+ graft) | rigid | fixed print | n/a | n/a |
| Base plate | rigid | fixed | n/a | same footprint for all stages |
| Soft-tissue overlay | TPU 95A, 100 % infill, 2-3 walls | removable | inserted along **(0, 0.6, 0.8)**, removed the opposite way | 0.35 mm gap to bone; nothing presses on bone. Tooth necks: about 0.07 mm contact at rest and up to about 0.4 mm flex while passing. Gum 1.2 mm thick at tooth margins, 1.8 mm over bone and palate. Two locating pins, no magnets |

## Stage 1: pre-graft, age 9-10, repaired UCLP (left)

| Part | Fixed / removable | Path | Notes |
|---|---|---|---|
| Maxilla + mixed dentition | fixed | n/a | open alveolar cleft, small anterior oronasal opening (palatal side), premolar buds in bone |
| 23 unerupted canine | separate print, sits in the labial window | n/a | visible through the window |
| Overlay | removable | as above | flat skin over the canine window with no grip there, so the window stays empty; palatal scar line along the repaired cleft |

## Stage 2: about 2-3 years after the graft, during fixed orthodontics (age about 12-13)

| Part | Fixed / removable | Path | Clearance |
|---|---|---|---|
| Maxilla + teeth | fixed | n/a | 23 erupted beside the graft; second molars partly erupted and partly under the gum; canine window closed |
| Graft (integrated) | fixed, or printed separately in another colour using the without-graft STL | n/a | seat bore filled |
| Braces strip (brackets, archwire to the first-molar tubes, false 22 on the wire) | removable | out along **(0, -0.2, -1)** | contact with the overlay under 0.1 mm at rest; clear path out; no brackets on the erupting second molars |
| Overlay | removable | as above | no hole at 22 |

## Stage 3: braces off, age 16+

| Part | Fixed / removable | Path | Clearance |
|---|---|---|---|
| Maxilla + teeth | fixed | n/a | canine window closed; empty 22 space by default |
| Graft (healed) | fixed or separate print | n/a | contains the keyed (D-shaped) seat bore at 22 |
| b. Implant body + abutment | removable, in the seat bore | out along (0, -0.2, -1) | clear |
| b. Implant crown 22 | removable | out along (0, -0.2, -1) | 0.1 mm contact with the overlay at rest; clear path out |
| c. One-wing resin-bonded (Maryland) bridge, wing on 21 | removable | out along (0, -0.2, -1) | 0.1 mm contact with the overlay at rest; clear path out |
| d. Removable partial denture (palatal plate, clasps on 16 and 26) | removable | out along (0, -0.2, -1) | under 0.1 mm overlap at rest; clear path out |
| Overlay | removable | as above | hole over the 22 seat |

b, c and d share one seat and are shown one at a time.

## Known limits

- Around the first and second molars, the overlay's gum flaps flex up to about 1.5 mm on removal. This was chosen instead of slots cut through the gum behind the molars. If a print is too tight, trim those flaps slightly. In Stage 2 the flaps over the partly erupted second molars are part of this.
- The flat lateral bone wall at the canine region comes from the original pre-op v6 bone. After the window was closed (Stages 2 and 3), faint seam lines remain on it, visible only with the overlay off.
- In Stage 1 with the overlay on, a small strip of bone may show on the palatal side of 12/53.
- Tooth geometry derived from BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 JP.
