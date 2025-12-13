# WindyAI - Startup Script
# Chạy ứng dụng WindyAI với Streamlit

Write-Host "Starting WindyAI Application..." -ForegroundColor Green
Write-Host ""

# Check if running from correct directory
if (-not (Test-Path "app/main.py")) {
    Write-Host "Error: app/main.py not found!" -ForegroundColor Red
    Write-Host "Please run this script from the project root directory." -ForegroundColor Yellow
    exit 1
}

# Start Streamlit
Write-Host "Starting Streamlit app on port 8501..." -ForegroundColor Cyan
Write-Host ""

python -m streamlit run app/main.py --server.port 8501

Write-Host ""
Write-Host "Application stopped." -ForegroundColor Green
