# Source-page captures

The adjacent `provenance.json` is the per-file log. It records each exact requested URL, UTC open time, Playwright Chromium as the capture tool, HTTP status, loaded/blocked state, and the owner-provided **paraphrase** of the model-test finding that prompted the visit. The `model_reply_sentence` field is intentionally null: no raw reply transcript was found locally, so no verbatim model sentence is claimed. A source page cannot establish that a model opened or cited it; only Oliver's pending screen recording can do that.

Each `*.full.jpg` was captured from the loaded page before its matching 1920×1080 `*.png` viewport image. The page images are browser screenshots, not drawings. The Omniglot and Oxford images show access walls, are marked `blocked` in the log, and must not be used as if their article paragraphs were visible. No invented article text was placed in those images.

The viewport screenshots are editorial receipts of what was actually visible on Oct 20, 2026. They are not substitutes for the two-model comparison recording. The test graphics live separately in `../graphics/` and are marked “GRAPHIC, NOT A CAPTURE.”
