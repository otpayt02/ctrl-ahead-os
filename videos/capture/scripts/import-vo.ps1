param(
  [string]$Source = ""
)

$captureDir = Split-Path -Parent $PSScriptRoot
$inputsDir = Join-Path $captureDir "capture-inputs"
$ffmpeg = Join-Path $captureDir "..\render\node_modules\@remotion\compositor-win32-x64-msvc\ffmpeg.exe"
if (-not (Test-Path $ffmpeg)) { $ffmpeg = "ffmpeg" }

New-Item -ItemType Directory -Force $inputsDir | Out-Null

if (-not $Source) {
  $downloads = Join-Path $HOME "Downloads"
  $candidates = Get-ChildItem $downloads -File | Where-Object {
    $_.Extension -match '^\.(m4a|mp3|wav|ogg|aac|flac|wma)$' -or $_.Name -like '*voice*' -or $_.Name -like '*hook*' -or $_.Name -like '*audio*' -or $_.Name -like '*record*'
  } | Sort-Object LastWriteTime -Descending

  if ($candidates.Count -eq 0) {
    $candidates = Get-ChildItem $downloads -File | Sort-Object LastWriteTime -Descending | Select-Object -First 5
  }

  $Source = $candidates[0].FullName
  Write-Host "Auto-detected newest download file: $Source"
}

if (-not (Test-Path $Source)) {
  Write-Error "File not found: $Source"
  exit 1
}

$destWav = Join-Path $inputsDir "hook-vo.wav"
Write-Host "Converting '$Source' -> '$destWav' (48kHz Mono PCM)..."

& $ffmpeg -y -i $Source -ar 48000 -ac 1 $destWav

if (Test-Path $destWav) {
  Write-Host "Success: hook-vo.wav is ready at $destWav"
} else {
  Write-Error "Conversion failed."
  exit 1
}
