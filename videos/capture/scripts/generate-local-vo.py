"""Generate private chapter VO with a local reference and Sopro zero-shot TTS.

The reference, chapter WAVs, and model cache are local inputs/outputs. No voice
sample or synthesized audio belongs in Git.
"""

import argparse
from pathlib import Path
import re
import time

import soundfile as sf
from sopro import SoproTTS


ROOT = Path(__file__).resolve().parents[3]
VIDEO = ROOT / "videos" / "001-ai-lost-cause"
DEFAULT_REFERENCE = ROOT / "videos" / "capture" / "capture-inputs" / "voice-candidates" / "past-reference-final.wav"


def narration_chapters(script_path: Path, sgaw_spoken: str):
    script = script_path.read_text(encoding="utf-8")
    narration = script.split("## Final narration", 1)[1].split("## Production gate", 1)[0]
    matches = list(re.finditer(r"^### CH([1-8])[^\n]*$", narration, re.MULTILINE))
    if len(matches) != 8:
        raise ValueError(f"Expected eight chapters; found {len(matches)}")
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(narration)
        text = narration[match.end():end].strip()
        text = re.sub(r"\*{1,2}", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        # Spoken forms are for the synthesizer only; the written script remains exact.
        text = text.replace("S’gaw", sgaw_spoken).replace("S'gaw", sgaw_spoken)
        text = text.replace("Sonnet 5.5", "Sonnet five point five")
        text = text.replace("UNCITED", "uncited")
        text = text.replace("1,050,000", "one million and fifty thousand")
        yield index + 1, text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("chapters", nargs="*", type=int, default=list(range(1, 9)))
    parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    parser.add_argument("--script", type=Path, default=VIDEO / "script.md")
    parser.add_argument("--output", type=Path, default=VIDEO / "vo")
    parser.add_argument("--sgaw-spoken", default="suh gaw")
    args = parser.parse_args()
    requested = set(args.chapters or range(1, 9))
    if not requested.issubset(set(range(1, 9))):
        parser.error("chapters must be numbers from 1 through 8")
    if not args.reference.is_file():
        parser.error(f"local voice reference missing: {args.reference}")
    args.output.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    print("Loading Sopro v2 turbo on CPU; reference stays local", flush=True)
    tts = SoproTTS.from_pretrained(device="cpu", quantization="int8")
    reference = tts.prepare_reference(ref_audio_path=args.reference)
    for chapter, text in narration_chapters(args.script, args.sgaw_spoken):
        if chapter not in requested:
            continue
        out = args.output / f"S{chapter}.wav"
        print(f"S{chapter}: {len(text)} characters / {len(text.split())} words", flush=True)
        chapter_started = time.monotonic()
        audio = tts.synthesize(text, ref=reference, lang="en")
        tts.save_wav(out, audio)
        samples, sample_rate = sf.read(out)
        duration = len(samples) / sample_rate
        print(f"S{chapter}: {duration:.2f}s, {out.stat().st_size} bytes, {time.monotonic()-chapter_started:.1f}s elapsed", flush=True)
    print(f"Finished in {time.monotonic()-started:.1f}s", flush=True)


if __name__ == "__main__":
    main()
