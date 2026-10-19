# Records face hook footage from the webcam via ffmpeg dshow.
# First run with no -Camera name lists available video devices.
param([int]$Seconds = 6, [string]$Camera = "")
$ff = "..\render\node_modules\@remotion\compositor-win32-x64-msvc\ffmpeg.exe"
if (-not (Test-Path $ff)) { $ff = "ffmpeg" }
if (-not $Camera) {
  & $ff -hide_banner -list_devices true -f dshow -i dummy 2>&1 | Select-String 'video'
  Write-Host ""
  Write-Host "Pick a camera name from the list above and rerun:"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\record-webcam.ps1 -Camera \"<device name>\""
  exit 0
}
New-Item -ItemType Directory -Force ..\001-ai-lost-cause\assets | Out-Null
& $ff -y -f dshow -framerate 30 -i "video=$Camera" -t $Seconds `
  -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080" `
  -c:v libx264 -crf 20 -pix_fmt yuv420p "..\001-ai-lost-cause\assets\face-hook.mp4"
Write-Host "Saved ..\001-ai-lost-cause\assets\face-hook.mp4 ($Seconds s)"
