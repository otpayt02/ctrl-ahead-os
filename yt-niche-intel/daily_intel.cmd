@echo off
cd /d C:\Users\olive\Projects\ctrl-ahead-os\yt-niche-intel || exit /b 1
set "PYTHONIOENCODING=utf-8"
set "PYTHON=C:\Users\olive\Projects\ctrl-ahead-os\yt-niche-intel\.venv\Scripts\python.exe"
"%PYTHON%" yt_niche_intel.py harvest >> intel_log.txt 2>&1 || exit /b 1
"%PYTHON%" yt_niche_intel.py spikes >> intel_log.txt 2>&1 || exit /b 1
"%PYTHON%" yt_niche_intel.py rank >> intel_log.txt 2>&1 || exit /b 1
