param([string]$Python='python',[string]$Node='node',[string]$PrivateWorkspace='')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
Push-Location $root
try {
  & $Python -B -m unittest discover -s tests -v
  if($LASTEXITCODE -ne 0){throw 'Offline tests failed'}
  & $Node --check scripts/build.mjs
  if($LASTEXITCODE -ne 0){throw 'Document script syntax failed'}
  & $Node scripts/build.mjs
  if($LASTEXITCODE -ne 0){throw 'Document build failed'}
  & $Node --test tests/preview-security.test.mjs
  if($LASTEXITCODE -ne 0){throw 'Preview security regression failed'}
  & $Python scripts/check_release.py
  if($LASTEXITCODE -ne 0){throw 'Release scan failed'}
  if($PrivateWorkspace) {
    $front=Join-Path (Resolve-Path -LiteralPath $PrivateWorkspace).Path 'frontend'
    if(-not(Test-Path -LiteralPath (Join-Path $front 'package.json'))){throw 'Authorized frontend not found'}
    Push-Location $front
    try { & npm.cmd run build; if($LASTEXITCODE -ne 0){throw 'Private Vue build failed'} } finally {Pop-Location}
  } else { Write-Output 'Private Vue application build: NOT INCLUDED; optional -PrivateWorkspace is local-only.' }
} finally {Pop-Location}
