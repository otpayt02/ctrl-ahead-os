#!/usr/bin/env bash
# vast-ltx2-setup.sh — LTX-2.3 video generation on the rented Vast.ai box
#
# Purpose (Oliver, 2026-10-29): the same rented 4090 that runs the Nemotron Bolt
# trial also runs LTX-2, so Ctrl-Ahead videos can use REAL generated video clips
# as the primary visual layer instead of still images + animation/motion effects.
# Captions/text overlays are still composited afterwards (LTX cannot render
# legible text), and generated clips stay metaphor/atmosphere — never proof.
#
# Facts verified 2026-10-29 (Lightricks + ComfyUI guides):
#   - Current model: LTX-2.3 (22B). For a 24 GB card use the FP8 build:
#     Hugging Face repo Lightricks/LTX-2.3-fp8 (~27 GB checkpoint).
#   - Official floor is 32 GB VRAM + 100 GB free disk; 24 GB (RTX 4090/3090)
#     is the practical floor via FP8 + ComfyUI offloading — works, just slower
#     (one guide measured ~90 s for a 5 s 720p clip on a 4090; unverified by us).
#   - The Gemma 3 12B text encoder is a SEPARATE required download.
#   - The audio VAE is a SEPARATE ~102 MB file (Lightricks/LTX-2, tree/main/audio).
#     WITHOUT it, MP4s render SILENT with no error. Do not skip step 5.
#   - Generation rules: dimensions divisible by 32; frame count = 8n+1;
#     the distilled workflow runs CFG 1 on its fixed sigma schedule.
#   - License: LTX-2 Community License — free under $10M ARR. Weights are free;
#     the only cost of any generation is the GPU rental time itself.
#
# Disk budget: Bolt (~25 GB) + LTX-2.3 FP8 set (~50 GB with encoder/VAEs)
#   => rent 100 GB+ disk, NOT the old 60 GB Bolt-only spec.
#
# If an `hf download` returns 403, the repo is license-gated: Oliver accepts the
# terms on the model page, then runs `hf auth login` with HIS OWN token on the
# box. Never send a token through chat.
set -u
cd ~

echo "== 0. GPU check =="
nvidia-smi || { echo "No NVIDIA GPU visible — wrong instance type."; exit 1; }

echo "== 1. ComfyUI =="
[ -d ComfyUI ] || git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
pip install -r requirements.txt
pip install -U "huggingface_hub[cli]"

echo "== 2. Lightricks LTXVideo nodes =="
cd custom_nodes
[ -d ComfyUI-LTXVideo ] || git clone https://github.com/Lightricks/ComfyUI-LTXVideo.git
cd ComfyUI-LTXVideo && pip install -r requirements.txt
cd ~/ComfyUI

echo "== 3. LTX-2.3 FP8 checkpoint (24 GB cards) =="
hf download Lightricks/LTX-2.3-fp8 --local-dir ~/hf/ltx23fp8
# Place the .safetensors checkpoint(s) where ComfyUI looks:
mkdir -p models/checkpoints
cp ~/hf/ltx23fp8/*.safetensors models/checkpoints/ 2>/dev/null || \
  echo "Check ~/hf/ltx23fp8 layout and copy the checkpoint manually."

echo "== 4. Gemma 3 12B text encoder =="
mkdir -p models/text_encoders
hf download Lightricks/LTX-2.3-fp8 --local-dir ~/hf/ltx23fp8 >/dev/null 2>&1 || true
# The encoder ships with the LTX-2.3 repos; if it is not in the fp8 repo, pull:
#   hf download Lightricks/LTX-2.3 --local-dir ~/hf/ltx23
# and copy the gemma*.safetensors into models/text_encoders/.

echo "== 5. Audio VAE (do not skip — silent MP4s without it) =="
mkdir -p models/vae
hf download Lightricks/LTX-2 audio --local-dir ~/hf/ltx2audio >/dev/null 2>&1 || \
  echo "Audio VAE download needs a manual pass: huggingface.co/Lightricks/LTX-2/tree/main/audio -> models/vae/"

echo "== 6. Launch (reserve 5 GB headroom to avoid first-step OOM) =="
echo "python main.py --listen 0.0.0.0 --port 8188 --reserve-vram 5"
echo "Then: Template Library -> Video -> LTX-2 distilled template is the fastest"
echo "known-good workflow; set 1280x720, frames = 8n+1 (e.g. 121 for ~5 s @24fps)."
