# Geliştirme ortamını başlat
Write-Host "Geliştirme ortamı başlatılıyor..." -ForegroundColor Green

# .env dosyalarını kontrol et
if (-not (Test-Path "backend/.env")) {
    Write-Host "backend/.env dosyası bulunamadı. Örnek dosyadan kopyalanıyor..." -ForegroundColor Yellow
    Copy-Item "backend/.env.example" "backend/.env"
}

if (-not (Test-Path "frontend/.env")) {
    Write-Host "frontend/.env dosyası bulunamadı. Örnek dosyadan kopyalanıyor..." -ForegroundColor Yellow
    Copy-Item "frontend/.env.example" "frontend/.env"
}

# Docker Compose ile geliştirme ortamını başlat
Write-Host "Docker Compose başlatılıyor..." -ForegroundColor Cyan
docker-compose up --build -d

# Servislerin durumunu kontrol et
Write-Host "Servis Durumları:" -ForegroundColor Magenta
docker-compose ps

Write-Host "Geliştirme ortamı hazır!" -ForegroundColor Green
Write-Host "Frontend: http://localhost:3000"
Write-Host "Backend: http://localhost:8000"
Write-Host "Prometheus: http://localhost:9090" 