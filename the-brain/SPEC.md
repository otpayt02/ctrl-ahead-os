# the-brain — Spec

## Purpose
A versioned knowledge module Codex loads before producing anything in Oliver's name. It operationalizes the-brain-v1.pdf (5 eras, intent→register routing table, 9 cross-era constants) into runnable code.

**Prime rule (from v1): nothing here invents. The engine restructures Oliver; it never originates for him. If the corpus didn't say it, the output doesn't say it.**

## Architecture
- `brain.md` — brain-v1 content as living docs (eras, routing table, constants, devices, tones, moods, pre-behaviors).
- `artifacts/` — normalized corpus: ChatGPT export (76 conversations), Perplexity data export, Google Takeout (YouTube watch history + Drive + Keep), 21 Drive files (Creativity Essay, HIST 105, improvisers-first-five-chords, KOA tracker, etc.), 41 GitHub repo READMEs/specs, Evernote, dictated prompts.
- `ingest.py` — normalize all exports into SQLite + embedding index. Free-tier only: local embeddings or TF-IDF. No paid APIs.
- `mine.py` — sentiment-life/viber-nexus-style inference: constants detection, positive/unique trait extraction, cross-domain artifact candidates (each must cite its source artifact), confidence tiers.
- `angles.py` — calls the angle-engine skill (.codex/skills/angle-engine/SKILL.md): creativity slider + angle/mode taxonomy → concept cards.
- `concepts/` — emitted concept cards (JSON + MD).

## Invariants
- Provenance over portrait — every claim traces to an artifact.
- Human-in-the-loop absolutism — approval gates on anything risky.
- `*.db`, exports, and API keys stay git-ignored.
- Brain updates are commits (docs: brain), not silent file edits.