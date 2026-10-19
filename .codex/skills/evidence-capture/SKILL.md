---
name: evidence-capture
description: Automatically capture, annotate, and extract every snippet the angle engine uses as proof — screenshots, screen recordings, audio clips, text blocks, code lines, AI-generated images, and uniquely-human artifacts from the brain corpus — each packaged for direct render-manifest inclusion. Use whenever concept cards, scripts, or snippet ledgers cite evidence.
---

# Evidence Capture (v2)

## Purpose
Kill the manual scavenger hunt AND the image-generation bill. When the engine claims a connection, this skill produces the on-screen proof automatically: the exact artifact, highlighted, annotated, extracted, and slotted into the render manifest as video time fillers — real evidence instead of generated art wherever possible.

## Snippet types
- png: Playwright screenshot (element or page)
- webm: Playwright screen recording
- audio_snippet: trimmed clip from an audio file (voice memos, music, recordings) + waveform visualization for on-screen display + transcript line if speech
- text_block: extracted passage with source citation
- code_line: code with file path + line range, syntax-highlighted
- ai_generated_image: flagged with provenance (tool, date) — labeled as AI-generated on screen
- human_artifact: uniquely-Oliver content (dictation typos, signatures, naming habits, freewrites) — labeled as human origin

## Evidence pointer schema
```
{
  "id": "...",
  "snippet_type": "png | webm | audio_snippet | text_block | code_line | ai_generated_image | human_artifact",
  "artifact_type": "github_file | gdrive_doc | local_file | sheet | web | audio | image",
  "uri": "...",
  "locator": "selector or text",
  "line_range": [10, 20],
  "highlight_range": [12, 14],
  "cursor_path": [[x1,y1],[x2,y2]] | null,
  "duration_sec": 6,
  "extracted_text": "the exact text/content visible in the capture",
  "annotation": {
    "reason_for_connection": "why this snippet makes the connection through the selected angle",
    "search_context": "what the search was looking for when it found this",
    "candidate_rationale": "why this was a good candidate",
    "supporting_details": "..."
  },
  "recommended_animation": "Remotion component + motion spec",
  "manifest_slot": { "scene": "S6", "time_range": [390, 415] },
  "provenance": { "source_artifact": "...", "captured_at": "...", "checksum": "..." }
}
```

## Capture methods (Python + Playwright)
- GitHub files: open blob URL with #L10-L20 anchors; locator.screenshot() or page screenshot; locator.highlight() borders for emphasis shots.
- Google Docs: open URL, locate passage by text, scrollIntoViewIfNeeded(), inject highlight CSS, screenshot.
- Local files/code: serve a generated HTML viewer (syntax-highlighted, line-numbered) on localhost; scroll to line; capture. Same for PDF pages and spreadsheet rows.
- Web: direct navigation + element capture.
- Audio: ffmpeg trim (in/out points), waveform PNG generation, optional transcript alignment.

## Cursor handling (the gotcha)
Playwright's native video recording does NOT render a visible cursor. Two modes:
- real-interaction mode: page.mouse.move() with steps + real clicks — for tutorials where authentic input matters.
- cinematic mode (DEFAULT for videos): capture clean, then composite a synthetic cursor with click ripples and camera push-ins in Remotion — deterministic, editable, cinematic.
- Playwright MCP browser_video_show_actions (cursor=pointer) animates a pointer between action points when recording via MCP.

## Animation standard (visually appealing, CTV-scaled reasonableness)
- Default treatments: keyframed push-in to the highlighted range, crop browser chrome, cursor-track overlay, kinetic labels, waveform pulse for audio.
- Reasonableness scales with CTV index: low = literal, intuitive framing; high = stretchy, poetic transitions between snippet and topic dynamics (flagged per entry in ctv_stretch_note on the ledger).
- Follow FACELESS-VISUAL-SYSTEM.md overlay and pacing standards.

## Output
- videos/<video-id>/evidence/evidence_manifest.json + captured PNGs/WEBMs/audio clips.
- Every capture stores extracted_text so script citations are GUARANTEED to match what appears on screen.
- Ledger manifest_slots merge into manifest.json as time fillers — real evidence fills time so fewer images get generated.

## Verification
- No concept card ships with unresolved evidence pointers.
- Every capture includes provenance (source artifact, timestamp, checksum).
- AI-generated vs human-origin content is always labeled on screen.