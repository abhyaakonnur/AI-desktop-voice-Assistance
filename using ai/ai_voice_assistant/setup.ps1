# Setup script for AI Voice Assistant on Windows PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AI Voice Assistant - Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check Python version
Write-Host "`nChecking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "Found: $pythonVersion" -ForegroundColor Green

# Install/upgrade required packages
Write-Host "`nInstalling/upgrading required packages..." -ForegroundColor Yellow
pip install --upgrade -r requirements.txt

# Clear Python cache
Write-Host "`nCleaning Python cache..." -ForegroundColor Yellow
if (Test-Path "__pycache__") {
    Remove-Item -Path "__pycache__" -Recurse -Force
}

# Check for .env file
Write-Host "`nChecking .env file..." -ForegroundColor Yellow
if (Test-Path ".env") {
    $envContent = Get-Content ".env"
    if ($envContent -match "your_api_key_here") {
        Write-Host ".env file found but OPENAI_API_KEY is not configured!" -ForegroundColor Red
        Write-Host "Please update .env file with your actual OpenAI API key:" -ForegroundColor Yellow
        Write-Host "  1. Visit https://platform.openai.com/account/api-keys" -ForegroundColor Cyan
        Write-Host "  2. Create a new API key" -ForegroundColor Cyan
        Write-Host "  3. Open .env and replace 'your_api_key_here' with your actual key" -ForegroundColor Cyan
        Write-Host "" -ForegroundColor Yellow
    } else {
        Write-Host ".env file is configured." -ForegroundColor Green
    }
} else {
    Write-Host ".env file not found. Creating one..." -ForegroundColor Yellow
    @"
# OpenAI API Key
# Get your API key from https://platform.openai.com/account/api-keys
OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_API_KEY_HERE
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host ".env file created. Please update with your API key." -ForegroundColor Red
}

# Test OpenAI connection
Write-Host "`nTesting OpenAI connection..." -ForegroundColor Yellow
python test_openai_client.py

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nTo run the web interface:" -ForegroundColor Yellow
Write-Host "  python app.py" -ForegroundColor Cyan
Write-Host "`nTo run the voice assistant:" -ForegroundColor Yellow
Write-Host "  python assistant.py" -ForegroundColor Cyan
Write-Host "`nThen visit: http://localhost:5000 in your browser" -ForegroundColor Yellow
