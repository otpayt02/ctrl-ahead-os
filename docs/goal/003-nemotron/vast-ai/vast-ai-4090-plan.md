# Vast.ai RTX 4090 test for Nemotron 3.5 Bolt — the ~$1.50 plan
Date: 2026-10-25. Prices are search results, not a live Vast.ai quote — read the live offer before Rent.

## The catch on "$1.50"
- Usage for 2-3 hours on a 4090 at $0.34-$0.74/hr is $0.68-$2.22.
- BUT Vast.ai minimum deposit is $5. So cash outlay is $5, usage is ~$1.50, the rest stays as Vast credit for later.
- RunPod is worse on entry: minimum $10 by card, even though its 4090 Community rate is also $0.34/hr.
- Vast bills per second, no minimum rental time. Stop = pause (storage still charges). Delete = all charges end.
- Disk size cannot be changed later. Pick at least 60 GB: 25 GB for Bolt + Ollama + OS + test outputs.

## Exact rent spec to pick
- GPU: 1x RTX 4090, 24 GB (or RTX 3090, also 24 GB, usually cheaper)
- Template: Vast Ollama standalone template if listed, otherwise a CUDA / PyTorch template, then install Ollama yourself
- Disk: 60 GB minimum, 100 GB safer
- Reliability: do NOT pick the absolute cheapest host with a bad reliability score — a host that dies mid-pull wastes the download time
- Type: On-demand, NOT interruptible/spot — spot can be reclaimed mid-download

## Steps, in order
1. vast.ai > Sign up, verify email, Billing > add $5 credit (card / crypto, per Vast docs)
2. Add SSH key if you want SSH, or use Vast's Jupyter terminal
3. Search > filter GPU = RTX 4090, 1 GPU, max price $0.75/hr, on-demand
4. Rent, wait for start (cached image = fast, fresh pull = 10-60 min)
5. SSH in, run: nvidia-smi  — must show RTX 4090, 24 GB
6. If Ollama template: check ollama --version. If not: curl -fsSL https://ollama.com/install.sh | sh
7. Run the script in vast-bolt-test.sh, in order: serve, pull, short test, ollama ps + nvidia-smi, video question
8. Screen-record / screenshot: nvidia-smi output, ollama ps showing 100% GPU, and the actual answer text
9. Copy /tmp/bolt-test1.txt, /tmp/bolt-test2.txt, and the screenshots OFF the instance
10. Vast dashboard > Delete instance. Do NOT just Stop — Stop still charges storage.

## What to expect on a 4090
- Bolt's registry manifest is ~24.7 GB total (22.0 GB model layer). NVIDIA's own llama.cpp notes say it fits whole at 32K context, and its 64K recipe asks for 32 GB+.
- So on a 24 GB card: keep context small for the first test (Ollama default, short prompts). If ollama ps shows less than 100% GPU or nvidia-smi shows the model spilling to RAM, that IS the result — record it, don't force a 256K context.
- Download time is the wildcard: 25 GB on a host's network, could be 10-40 min. Budget 3 hours total, not 1.

## Cost math
- 2 hr @ $0.50/hr = $1.00
- 3 hr @ $0.50/hr = $1.50
- 3 hr @ $0.74/hr (RunPod Secure rate, for comparison) = $2.22
- Plus small storage/bandwidth charges on Vast, which vary by host — read the offer line before Rent.

## What I cannot do without you
- I cannot create your Vast.ai account, add your card, or rent in your name. You do that part, then paste me the SSH command Vast gives you (host + port, NOT a password/private key), and I can walk you through the commands live, and record the session the same livestream way we did for Ollama on my VM.
- Never paste a Vast API key, password, or private SSH key in chat. If you want me to use an API key, use the Secure Vault flow, same as the YouTube key.
