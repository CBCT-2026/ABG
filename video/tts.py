"""Make the narration audio for each stage, and a timeline (subtitles and scenes) for the narrated video.

Usage: python video/tts.py en|ja --model-dir DIR
DIR holds kokoro-v1.0.onnx and voices-v1.0.bin (Kokoro-82M, Apache 2.0) from
https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0
Writes video/audio/<lang>/stage-<n>.wav and .mp3 (one file per stage, to play with the 3D print)
and video/build/<lang>/timeline.json (all stages, for the video). Prints each stage's length.
"""
import argparse
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

HERE = Path(__file__).resolve().parent
LEAD_IN = 0.5   # silence before the first word
TAIL = 0.8      # silence after the last word


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lang", choices=["en", "ja"])
    ap.add_argument("--model-dir", required=True)
    args = ap.parse_args()

    script = json.loads((HERE / f"script-{args.lang}.json").read_text(encoding="utf-8"))
    kokoro = Kokoro(f"{args.model_dir}/kokoro-v1.0.onnx", f"{args.model_dir}/voices-v1.0.bin")
    if args.lang == "ja":
        from misaki import ja
        g2p = ja.JAG2P()
    else:
        # British English pronunciation from misaki (needs spaCy en_core_web_sm); sounds less robotic than espeak.
        from misaki import en
        english = en.G2P(trf=False, british=True, fallback=None)
        g2p = lambda text: english(text)[0]

    sr = 24000
    audio_dir = HERE / "audio" / args.lang
    build_dir = HERE / "build" / args.lang
    audio_dir.mkdir(parents=True, exist_ok=True)
    build_dir.mkdir(parents=True, exist_ok=True)
    timeline = {"chapters": []}
    for ch in script["chapters"]:
        chunks = [np.zeros(int(LEAD_IN * sr), dtype=np.float32)]
        t = LEAD_IN
        cues, scenes = [], []
        for p, para in enumerate(ch["paragraphs"]):
            start = t
            for s, sent in enumerate(para["sentences"]):
                result = g2p(sent)
                phonemes = result[0] if isinstance(result, tuple) else result
                audio, sr = kokoro.create(phonemes, voice=script["voice"], speed=script["speed"],
                                          lang="ja" if args.lang == "ja" else "en-gb", is_phonemes=True)
                dur = len(audio) / sr
                cues.append({"start": round(t, 3), "end": round(t + dur, 3), "text": sent})
                chunks.append(audio.astype(np.float32))
                t += dur
                last = s == len(para["sentences"]) - 1
                if not (last and p == len(ch["paragraphs"]) - 1):
                    gap = script["paragraph_gap"] if last else script["sentence_gap"]
                    chunks.append(np.zeros(int(gap * sr), dtype=np.float32))
                    t += gap
            scenes.append({"scene": para["scene"], "labels": para["labels"], "start": round(start, 3), "end": round(t, 3)})
        chunks.append(np.zeros(int(TAIL * sr), dtype=np.float32))
        t += TAIL
        wav = audio_dir / f"stage-{ch['stage']}.wav"
        sf.write(wav, np.concatenate(chunks), sr)
        if shutil.which("ffmpeg"):
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-b:a", "96k",
                            str(wav.with_suffix(".mp3"))], check=True)
        timeline["chapters"].append({"stage": ch["stage"], "title": ch["title"], "audio": wav.name,
                                     "duration": round(t, 2), "cues": cues, "scenes": scenes})
        print(f"{args.lang} stage {ch['stage']}: {t:.1f} s")
    (build_dir / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
