# Corpus status — 2026-10-18

- First-party source: `the-brain-v1.pdf` fetched from Oliver's Drive and summarized in `brain.md`; the PDF itself remains in Drive.
- GitHub: authenticated account currently has **49** owned repositories. The importer read **192** README/spec Markdown documents from **47** repositories into ignored local SQLite. One API/content retrieval error was recorded; one other repository yielded no matching README/spec document. The earlier 41-repo figure is a prior inventory, not the current count.
- Five selected first-party Drive documents are now in the ignored local database: Creativity Essay, HIST 105 Race and Reunion essay, improvisers-first-five-chords, KOA v4 project tracker, and personal statement. Their original Drive URLs are the artifact source URIs. The PDF summary is a sixth `drive` row.
- ChatGPT export, Perplexity export, Google Takeout (YouTube/Drive/Keep), Evernote, dictated prompts, and the other Drive documents: **not ingested**. This pass intentionally stops at the five known files.
- Current local count: **198 artifacts** (192 GitHub documents, 5 original Drive documents, 1 PDF-derived brain summary). The mining pass emits **70 review-required candidates** across 12 lanes; 44 currently include at least one original Drive receipt in their first three cited artifacts.
- The current local DB and generated mining/concept JSON are ignored. Regenerate them with `ingest.py`, `mine.py`, and `angles.py`; this status file is a provenance summary, not a copy of private content.
