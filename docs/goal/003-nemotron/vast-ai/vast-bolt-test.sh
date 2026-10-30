#!/bin/bash
# Vast.ai RTX 4090 (24 GB) - Nemotron 3.5 Bolt test
# Run AFTER: nvidia-smi shows a 4090, and ollama is installed
set -e
echo "=== GPU check ==="
nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv
free -h | head -2
ollama --version
echo "=== Start Ollama (if not already running) ==="
# Vast Ollama template may already run ollama serve; this is safe to re-run in background
(ollama serve > /tmp/ollama-vast.log 2>&1 &) || true
sleep 5
curl -s http://127.0.0.1:11434/api/tags | head -c 300; echo
echo "=== Pull Bolt (about 24.7 GB - this is the slow part, do NOT stop the instance here) ==="
ollama pull nemotron-3.5-bolt
ollama list
echo "=== Test 1 - short, low context ==="
ollama run nemotron-3.5-bolt "Say hello in one sentence, and say how much VRAM you need." 2>&1 | tee /tmp/bolt-test1.txt
echo "=== GPU usage during/after run ==="
ollama ps
nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv
echo "=== Test 2 - the video question ==="
ollama run nemotron-3.5-bolt "Explain in 3 sentences: does Nemotron 3.5 Bolt really fit on a 24 GB card, and what breaks first?" 2>&1 | tee /tmp/bolt-test2.txt
echo "DONE - save /tmp/bolt-test*.txt and /tmp/ollama-vast.log, then DELETE the instance in Vast.ai"
