# Codex prompt — copy and paste this whole prompt into Codex

Build a reusable 9:16 Short video boilerplate in this repo, exactly matching the visual system below. Do not copy any other creator's brand, logo, watermark text, ebook title, comment keyword, or product screenshots — use our own brand text in the watermark slot and our own screenshots/artifacts in the card slot.

## The visual system to replicate (from a reference Short I watched)
- Canvas: 9:16, pure white background. No camera movement — all motion is graphic animation.
- Type: bold black grotesque sans (Inter/Helvetica-style, tight letter-spacing, centered). Italic cuts of the same family for accent words only.
- Karaoke headlines (the core feature): baked in, word-by-word, no box, centered in the middle of the frame. Not-yet-spoken words are gray. The word being spoken pops bold black in sync with narration. Already-spoken words fade back to light gray. Punch words are extra-large (1.3-1.5x). This is NOT a bottom sentence caption — it IS the headline.
- Number cards: for each numbered item, a dark product/artifact screenshot floats center with a soft drop shadow, below it a giant numeral in a vertical black-to-transparent gradient, overlapping the item name in bold black beneath.
- Detail beats, one device at a time only: either a floating dark-UI screenshot card, OR a pixel-art sticker character (terracotta #D07A52-ish, white sticker border, drop shadow, rotated about -20 degrees), OR a sparkle (✦) bullet list revealing one item at a time in narration order. Never more than one device at once. No emojis.
- Highlights: hook only gets a black rectangular box with white text for the final hook phrase. Elsewhere use extra-large punch words, italic accents, and terracotta asterisk/floral motifs in the top-right and bottom-left corners.
- Transitions: quick ~0.3s blur crossfades between beats. Visuals change every 3-5 seconds. A numbered section runs ~10-16 seconds.
- Watermark: light gray, bottom-center, persistent, with OUR brand text.
- CTA: italic prompt word + giant quoted keyword in bold black, faint light-gray "+" grid in the lower half, a small tilted mockup, then an end card with a follow prompt (italic accent) + brand in large light-gray type + brand mark centered with drop shadow over the "+" grid. End cards must loop cleanly back to the hook.
- Audio: continuous rapid voiceover, no gaps. No sound effect per word.

## What to build
1. A Remotion project (preferred) OR an ffmpeg + PIL pipeline if Remotion is not available in this repo — pick one, state which, and make it actually render.
2. Components/functions for: KaraokeHeadline (gray -> black pop -> light-gray fade, word timings from a phrase list), NumberCard (screenshot + gradient numeral + name), SparkleList (✦ items revealing in order), HookCard (black box, white text), CornerAsterisks, Watermark, CTACard, EndCard.
3. A CLI / script that takes: a script JSON (phrases with start/end/words, numbered items with screenshot paths, sparkle items, CTA keyword, brand text) and outputs a 1080x1920 MP4, plus a 16:9 long version using the same karaoke + number-card system centered on white with side margins (do not stretch the vertical frame).
4. Timing: every beat must end when its spoken phrase ends, not on a fixed grid. Word timings may be estimated from word-count proportion until measured TTS timestamps exist — label that as an estimate in the output manifest.
5. Labelling: every screenshot/graphic/AI visual must be labelled on its face (live / rendered / AI / graphic). Never present a render as a live screenshot, and never invent a tool, price, token count, or provider count not in the evidence. If a screenshot and a headline disagree on a number, flag it and use the evidence number.

## Deliverables
- Working code + a sample render (at least 15 seconds, 1080x1920) proving the karaoke, number card, and sparkle list all work.
- A README with the visual system, the CLI usage, and the known limitations (e.g. if ffmpeg ASS cannot do the fade-back to light gray, say so and implement it in Remotion instead).
- A render manifest JSON for the sample: timings (estimated vs measured), labels for every visual, and any number discrepancies flagged.
