param([string]$Python='python',[string]$Node='node')
$ErrorActionPreference='Stop'
& $Python -c "import sys; assert sys.version_info >= (3,11); print('Python compatibility: PASS')"
if($LASTEXITCODE -ne 0){throw 'Python 3.11+ required'}
& $Node -e "if(Number(process.versions.node.split('.')[0])<22)process.exit(1); console.log('Node compatibility: PASS')"
if($LASTEXITCODE -ne 0){throw 'Node 22+ required'}
Write-Output 'Portfolio scope: no database, crawler or API credentials needed.'
