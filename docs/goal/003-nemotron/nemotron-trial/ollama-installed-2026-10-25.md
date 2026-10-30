# Nemotron trial update — Ollama installed, Bolt still cannot run here
Date: 2026-10-25, America/New_York
Ollama version: 0.40.11, installed at /usr/local/bin/ollama
Runner: /usr/local/lib/ollama/llama-server now present after full install completed
Serve: ollama serve running on 127.0.0.1:11434, models list empty, CPU only
Machine at check: 7.7 GiB total, 1.3 GiB available, no GPU
Ollama library sizes found by search 2026-10-25:
- nemotron-3.5-bolt: 24-25 GB (74B MoE, 9B active)
- nemotron-3.5-super: 90 GB (120B)
- nemotron-3.5-lightning: ~25 GB (30B, 3B active)
No smaller Nemotron 3.5 tag was found in the Ollama library in this check.
Verdict unchanged, now with a working Ollama: Bolt cannot run on this VM.
25 GB > 7.7 GiB total RAM, and > 1.3 GiB available RAM.
Pulling Bolt was NOT done, because a 25 GB download would still fail to load
on 1.3 GiB available and risks OOM. This is a sizing verdict, not a run.
To run Bolt, use a machine with at least 24 GB GPU memory, as the vendor states.
