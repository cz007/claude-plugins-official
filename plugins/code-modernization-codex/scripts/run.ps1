# Codex adapter, cz007, 2026-10-20. Does not install any software.
[CmdletBinding()]
param(
  [string]$Python,
  [Parameter(ValueFromRemainingArguments=$true)][string[]]$RunnerArgs
)
$ErrorActionPreference = 'Stop'
$candidates = @()
if ($Python) { $candidates += ,@($Python) }
elseif ($env:CODE_MODERNIZATION_PYTHON) { $candidates += ,@($env:CODE_MODERNIZATION_PYTHON) }
else {
  $candidates += ,@('python3')
  $candidates += ,@('python')
  $candidates += ,@('py','-3')
}
foreach ($candidate in $candidates) {
  $exe = $candidate[0]
  $prefix = @($candidate | Select-Object -Skip 1)
  if (-not (Get-Command $exe -ErrorAction SilentlyContinue)) { continue }
  & $exe @prefix -c 'import sys; sys.exit(0 if sys.version_info >= (3,8) else 2)' 2>$null
  if ($LASTEXITCODE -ne 0) { continue }
  & $exe @prefix -B (Join-Path $PSScriptRoot 'codex_runner.py') @RunnerArgs
  exit $LASTEXITCODE
}
throw 'Python 3.8+ unavailable. Supply -Python with a verified executable path. Nothing was installed.'
