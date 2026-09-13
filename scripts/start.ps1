param([string]$Node='node',[int]$Port=8765)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$run=Join-Path $root '.run'
if(Test-Path -LiteralPath (Join-Path $run 'server.json')){throw 'A saved preview process exists; inspect or use stop.ps1 first'}
New-Item -ItemType Directory -Path $run -Force | Out-Null
$serverScript=Join-Path $PSScriptRoot 'serve.mjs'
$process=Start-Process -FilePath $Node -ArgumentList @(('"{0}"' -f $serverScript),"$Port") -WorkingDirectory $root -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $run 'stdout.log') -RedirectStandardError (Join-Path $run 'stderr.log')
@{pid=$process.Id;started=$process.StartTime.ToUniversalTime().ToString('o');port=$Port} | ConvertTo-Json | Set-Content -Encoding utf8 -LiteralPath (Join-Path $run 'server.json')
Write-Output "Portfolio preview started on loopback port $Port; open /docs/assets/demo/public-demo.html"
