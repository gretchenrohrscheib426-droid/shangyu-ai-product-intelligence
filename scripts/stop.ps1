$ErrorActionPreference='Stop'
$file=Join-Path (Split-Path $PSScriptRoot -Parent) '.run/server.json'
if(-not(Test-Path -LiteralPath $file)){Write-Output 'No portfolio preview process recorded.';exit 0}
$info=Get-Content -Raw -LiteralPath $file | ConvertFrom-Json
$process=Get-Process -Id $info.pid -ErrorAction SilentlyContinue
if($process){
  $recordedStart=[datetime]$info.started
  if($process.StartTime.ToUniversalTime().Ticks -ne $recordedStart.ToUniversalTime().Ticks){throw 'PID was reused; refusing to stop an unrelated process'}
  $detail=Get-CimInstance Win32_Process -Filter "ProcessId = $($info.pid)"
  if($detail.CommandLine -notmatch 'scripts[\\/]serve\.mjs'){throw 'Recorded process is not the preview server'}
  Stop-Process -Id $info.pid
}
Remove-Item -LiteralPath $file
Write-Output 'Recorded portfolio preview stopped; other services untouched.'
