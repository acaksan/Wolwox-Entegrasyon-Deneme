# Temizlik scripti
Write-Host "🧹 Temizlik başlatılıyor..." -ForegroundColor Yellow

# Docker konteynerlerini ve volumelerini temizle
Write-Host "🐳 Docker temizliği yapılıyor..." -ForegroundColor Cyan
docker-compose down -v

# Geçici dosyaları temizle
Write-Host "🗑️ Geçici dosyalar temizleniyor..." -ForegroundColor Magenta

# Frontend temizliği
if (Test-Path "frontend/.next") {
    Remove-Item -Recurse -Force frontend/.next
}
if (Test-Path "frontend/node_modules") {
    Remove-Item -Recurse -Force frontend/node_modules
}

# Backend temizliği
if (Test-Path "backend/__pycache__") {
    Get-ChildItem -Path backend -Filter "__pycache__" -Recurse | Remove-Item -Recurse -Force
}
if (Test-Path "backend/logs") {
    Remove-Item -Recurse -Force backend/logs
}

# Cache dosyalarını temizle
Write-Host "💾 Cache temizleniyor..." -ForegroundColor Blue
if (Test-Path ".pytest_cache") {
    Remove-Item -Recurse -Force .pytest_cache
}
if (Test-Path ".coverage") {
    Remove-Item -Force .coverage
}

Write-Host "`n✨ Temizlik tamamlandı!" -ForegroundColor Green 