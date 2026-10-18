# Artifact corpus

Put private exports in `private/` or `imports/`; both are ignored by Git. The database and generated concepts are ignored too. Import only files you select. `ingest.py` stores source paths, hashes, and extracted text in a local SQLite database. Keep the original export outside the repository or in these ignored folders.

Supported inputs: ChatGPT `conversations.json` or its ZIP export, Perplexity JSON/Markdown/HTML export, Google Takeout ZIP or folder (watch history JSON/HTML, Keep JSON/HTML, Drive text/Markdown/HTML), Evernote ENEX, dictated text/Markdown, and public GitHub README/spec files. Binary Drive documents are recorded as pending conversion, not silently treated as text.

`brain.md` records the first-party Drive PDF's versioned synthesis. The actual PDF and any personal exports are not tracked.
