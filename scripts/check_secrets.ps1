param([string]$Python='python')
$ErrorActionPreference='Stop'
& $Python (Join-Path $PSScriptRoot 'check_release.py') --secrets-only
if($LASTEXITCODE -ne 0){throw 'Initial secret scan failed'}
& $Python (Join-Path $PSScriptRoot 'security_scan.py')
if($LASTEXITCODE -ne 0){throw 'Secret/file scan failed; inspect locations without printing values'}
