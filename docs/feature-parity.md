# Same content in every material

The study compares four materials: A 2D information sheet, B AR web page, C 3D printed models and D narrated video. Each must show the same content, in the same clinical order, so that no material wins because it shows more. This table lists what the AR web page shows and how each other material shows the same thing. Anything one material cannot show is left out of all four.

| Content or feature on the AR page | A Sheet | C 3D print | D Video |
|---|---|---|---|
| Three stages in clinical order (before surgery, about 3 months after, years later) | Three panels in order | Three models (or swap-in parts) in order | Three chapters in order |
| Patient text for each stage (`content/<stage>-en/ja.html`) | Same text | Narration script (spoken, shorter) | Same narration, with subtitles |
| Labels: Gum, Gap in the bone, Eye tooth window, Front tooth, Missing tooth, Roof of the mouth | Same names as numbered call-outs | Named in the narration by colour and place (no stickers) | Same names as line labels |
| Take off the gum (slides down, then fades) | Two pictures: gum on, gum off | Gum part comes off by hand | Same animation |
| Turn the model, preset views (whole jaw, from below, left side) | Pictures from the same three views | Turned in the hand | Model turns through the same three views |
| AR (place in the room) | Not possible: left out of the comparison, recorded only as the AR check | Not possible | Not possible |
| Sources (numbered) | Same list | Same list on the researcher's sheet | Same list on the video page |
| Light/dark mode, language switch, timer, Start again | Not content: page tools only | – | – |

Open points for Luke:
- AR is the one feature the other materials cannot copy. The protocol already treats it as the "AR check", so it stays on the web page only.
- Labels in the video and the print narration must use the label names above word for word (patient-education-toolkit `label_sets` can check this once the video script exists).
