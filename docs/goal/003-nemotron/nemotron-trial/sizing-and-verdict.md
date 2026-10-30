# Nemotron trial — sizing calculation and verdict
Date: 2026-10-25, America/New_York
Machine: Muse Linux VM, 2 CPUs (AMD EPYC 9D25), no GPU, no nvidia-smi, no swap

## Measured here, 2026-10-25 07:48–07:49 EDT
- RAM total: 7.7 GiB (7,935 MiB, 8,125,588 kB)
- RAM used: 6.1 GiB
- RAM free: 441 MiB at 07:48, 392 MiB at 07:49
- RAM available: 1,739 MiB (1.7 GiB) at 07:48, 1.6 GiB at 07:49
- Swap: 0 B total, 0 B used
- Disk free in home: 99 GiB
- Ollama installed: No, before or after this trial

## Vendor claim to be tested (003 script topic)
- NVIDIA Nemotron 3.5 Bolt: 74B total, 9B active per token.
- Claimed to fit in 24 GB with 2-bit quantization on RTX / DGX Spark.
- That is a GPU / VRAM claim, not a CPU-only 7.7 GiB RAM claim.

## Sizing arithmetic, no invented VRAM
- Bolt claimed need: ~24 GB
- This machine total RAM: 7.7 GiB
- Shortfall vs total: 24 - 7.7 = 16.3 GB short, even before the operating
  system, the agent, Ollama itself, or any KV cache.
- This machine available RAM at trial time: 1.6–1.7 GiB
- Shortfall vs available: 24 - 1.7 = 22.3 GB short.
- Ratio: 24 / 7.7 = about 3.1x total RAM, 24 / 1.7 = about 14x available RAM.
- Even the smallest reported Nemotron variant, Nano 4B at 2.8 GB
  (third-party report, unverified on the official page here):
  2.8 GB > 1.7 GiB available, so it also fails the available-RAM rule,
  before adding Ollama overhead or KV cache.
- No GPU was present, so no VRAM figure was measured here, and none is claimed.

## Ollama install result — STOP point
All three no-sudo download attempts returned the same 9-byte file
containing the text "Not Found", not a gzip archive:
1. curl -L https://ollama.com/download/ollama-linux-amd64.tgz
   -> 9 bytes, "Not Found"
   -> tar: "gzip: stdin: not in gzip format", "tar: Child returned status 1",
      "tar: Error is not recoverable: exiting now"
2. curl -L https://github.com/ollama/ollama/releases/latest/download/ollama-linux-amd64.tgz
   -> 9 bytes, "Not Found"
3. curl -L https://github.com/ollama/ollama/releases/download/v0.40.11/ollama-linux-amd64.tgz
   -> 9 bytes, "Not Found"
No sudo was used. No system pip was used. Target dir
~/workspace/ollama-bin remained empty.

Per the task rule, install failure is the stop point. No model was
pulled, no model was run, no prompt was sent, and no model output exists.

## Verdict, in plain language
This computer cannot run Bolt 74B. The vendor 24 GB claim cannot be
verified here, because this machine has no GPU, only 7.7 GiB total RAM,
only 1.6–1.7 GiB available, and no swap, and Ollama could not even be
installed from the official binary URLs in this VM on 2026-10-25.
That is a real, usable result for the 003 video: the test is "try to
break the vendor claim, measure it" — and the honest measurement here
is that the claim fails on hardware grounds before any inference runs.
To actually test Bolt, it needs a machine with at least 24 GB of GPU
memory (or the vendor's stated RTX / DGX Spark setup), not this Muse VM.

## What was NOT done
- No Nemotron model was run, locally or in the cloud.
- No latency, tokens per second, VRAM use, or model output is claimed.
- No key or secret is in any log in this folder.
- Cloud tags (for example :30b-cloud) were not used, because that would
  not be a local run on this computer, and would need separate sign-in.
