# Records the hook VO from your mic via ffmpeg dshow.
# First run with no -Mic name lists available audio devices.
param([int]$Seconds = 12, [string]$Mic = "")
$ff = "..\render\node_modules\@remotion\compositor-win32-x64-msvc\ffmpeg.exe"
if (-not (Test-Path $ff)) { $ff = "ffmpeg" }
if (-not $Mic) {
  & $ff -hide_banner -list_devices true -f dshow -i dummy 2>&1 | Select-String 'audio'
  Write-Host ""
  Write-Host "Pick a mic name from the list above and rerun:"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\record-vo.ps1 -Mic \"<device name>\""
  exit 0
}
New-Item -ItemType Directory -Force capture-inputs | Out-Null
& $ff -y -f dshow -i "audio=$Mic" -t $Seconds -ar 48000 -ac 2 "capture-inputs\hook-vo.wav"
Write-Host "Saved capture-inputs\hook-vo.wav ($Seconds s)"
