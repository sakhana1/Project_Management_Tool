$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$python = Join-Path $PSScriptRoot '.planora-venv\Scripts\python.exe'
if (-not (Test-Path $python)) {
    Write-Host 'Creating a clean Planora Python environment...' -ForegroundColor Cyan
    py -m venv (Join-Path $PSScriptRoot '.planora-venv')
}
Write-Host 'Installing backend dependencies (first run can take a few minutes)...' -ForegroundColor Cyan
& $python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw 'pip upgrade failed. Check your internet connection and try again.' }
& $python -m pip install --no-cache-dir -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed. Read the error above before retrying.' }
Write-Host 'Preparing the local SQLite database...' -ForegroundColor Cyan
& $python manage.py migrate
if ($LASTEXITCODE -ne 0) { throw 'Database migration failed. Read the error above.' }
Write-Host 'Starting Planora API at http://127.0.0.1:8000' -ForegroundColor Green
& $python manage.py runserver
