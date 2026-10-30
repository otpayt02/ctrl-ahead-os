# v12 correction note — 005 model leaks

v12 supersedes v10 and v11 for the 005 video.

What was wrong before:
- v10/v11 treated the viral title phrase as a search for a model called Claude REA that could not be found, and folded Anthropic's policy/account bans into it.
- v10/v11 shipped-list visuals did not give the Opus 5.5 and Argon dates, leaving them looking new in the week of Oct 25, 2026.

What v12 corrects:
- REA = Reverse Engineer Anything, github.com/morluto/rea — a GitHub repo, MIT-licensed MCP server + CLI that lets coding agents use reverse-engineering tools on software they own/are authorized to examine, analysis runs locally, viral mid-October 2026. NOT a model, NOT a Claude product, NO Anthropic ban of REA.
- Anthropic bans are separate: Oct 8, 2026 usage policy effective Nov 12, 2026; Oct 12, 2026 tens of thousands of accounts banned for distillation.
- Shipped dates: Claude Opus 5.5 released Sep 22, 2026; Gemini 4 Argon announced Sep 30, 2026, generally available Oct 13, 2026 — neither new in the week of Oct 25, 2026.

Do NOT publish v10-render.mp4, v10-render-blue.mp4, or v11-render.mp4 as the 005 video. They remain on disk for comparison only.
