# Nemotron models found via web library search — 2026-10-25

No Ollama binary was installed, so `ollama list` could not be run locally.
The list below is from web search on 2026-10-25 only. Do not treat third-party
sizes as Ollama official sizes unless marked official.

## Official Ollama registry page fetched
- `nemotron-3-nano:30b` — registry page text fetched 2026-10-25 shows
  two entries: 18 GB and 24 GB (Q4_K_M, 31.6B parameters in one entry).
  The same page lists `ollama run nemotron-3-nano:4b` as a tag name,
  but the fetched 30b page text did NOT give a verified file size for the 4b tag.
  Source: https://registry.ollama.com:443/library/nemotron-3-nano:30b

## Third-party / secondary reports (not verified on the official page in this run)
- `nemotron-3.5-bolt` — 24 GB, 74B mixture-of-experts, 9B active.
  Source: https://computingforgeeks.com/ollama-models-cheat-sheet/
- `nemotron-3.5-super` — 90 GB, 120B, 12B active.
  Source: https://computingforgeeks.com/ollama-models-cheat-sheet/
- `nemotron-3.5-lightning` — 30B total, 3B active, Q4_K_M about 25 GB.
  Source: https://ollama.com/oamazonasgabriel/nemotron-3.5-lightning
- `nemotron-3-nano:4b` — reported as only 2.8 GB on a third-party site.
  This was NOT verified on an official Ollama page in this run, and is
  therefore treated as unverified for a run decision, except that even
  2.8 GB exceeds the available RAM measured here (1.6–1.7 GiB).
  Source: https://nvidia-nemotron-3-nano-3-ytamra2.gamma.site/
- `nemotron-3.5-bolt-e4b` — vendor target envelope about 4 GB, but the
  Q4_K_M GGUF on Hugging Face is reported as 6.18 GB, which is over the
  5 GB hard stop in this task.
  Source: https://www.marktechpost.com/2026/10/23/nvidia-nemotron-3-5-bolt-e4b-4gb/

## Hard-stop check against this machine
- Task hard stop: do NOT pull a model larger than 5 GB.
- Task hard stop: do NOT run if available RAM is under the model size.
- Task hard stop: do NOT use swap. There is no swap (0 B, see diagnostics.txt).

Result: Bolt, Super, Lightning, and Nano 30B all fail the 5 GB stop.
Nano 4B (2.8 GB, unverified) passes the 5 GB stop but fails the
available-RAM stop: 2.8 GB > 1.6–1.7 GiB available.
Bolt E4B (6.18 GB file, reported) fails the 5 GB stop.

No model was pulled. No model was run. No output text was generated.
