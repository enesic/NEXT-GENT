# NextGent Development Environment Setup Script
# Bu script tüm development environment'ı otomatik olarak kurar

Write-Host "🚀 NextGent Development Environment Setup Başlıyor..." -ForegroundColor Cyan
Write-Host ""

# Hata durumunda dur
$ErrorActionPreference = "Stop"

# Ana dizin
$ROOT_DIR = Split-Path -Parent $PSScriptRoot
Set-Location $ROOT_DIR

Write-Host "📁 Çalışma Dizini: $ROOT_DIR" -ForegroundColor Yellow
Write-Host ""

# ============================================================================
# 1. Gerekli Yazılımları Kontrol Et
# ============================================================================

Write-Host "🔍 Gerekli yazılımlar kontrol ediliyor..." -ForegroundColor Cyan

# Git kontrolü
try {
    $gitVersion = git --version
    Write-Host "✅ Git yüklü: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git bulunamadı! Lütfen Git'i yükleyin: https://git-scm.com/" -ForegroundColor Red
    exit 1
}

# Docker kontrolü
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker yüklü: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker bulunamadı! Lütfen Docker Desktop'ı yükleyin: https://www.docker.com/products/docker-desktop" -ForegroundColor Red
    exit 1
}

# Python kontrolü
try {
    $pythonVersion = python --version
    Write-Host "✅ Python yüklü: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python bulunamadı! Lütfen Python 3.11+ yükleyin: https://www.python.org/" -ForegroundColor Red
    exit 1
}

# Node.js kontrolü
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js yüklü: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js bulunamadı! Lütfen Node.js 18+ yükleyin: https://nodejs.org/" -ForegroundColor Red
    exit 1
}

Write-Host ""

# ============================================================================
# 2. Backend Setup
# ============================================================================

Write-Host "⚙️ Backend kurulumu başlıyor..." -ForegroundColor Cyan

Set-Location "$ROOT_DIR\backend"

# Virtual environment oluştur
if (Test-Path ".venv") {
    Write-Host "⚠️  Virtual environment zaten mevcut, siliniyor..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force .venv
}

Write-Host "📦 Virtual environment oluşturuluyor..." -ForegroundColor Cyan
python -m venv .venv

# Virtual environment aktifleştir
Write-Host "🔌 Virtual environment aktifleştiriliyor..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1

# Dependencies kur
Write-Host "📥 Backend dependencies kuruluyor..." -ForegroundColor Cyan
pip install --upgrade pip
pip install -r requirements.txt

# .env dosyası oluştur
if (-not (Test-Path ".env")) {
    Write-Host "📝 .env dosyası oluşturuluyor..." -ForegroundColor Cyan
    Copy-Item .env.example .env
    Write-Host "⚠️  .env dosyasını düzenlemeyi unutmayın!" -ForegroundColor Yellow
} else {
    Write-Host "✅ .env dosyası zaten mevcut" -ForegroundColor Green
}

Write-Host "✅ Backend kurulumu tamamlandı!" -ForegroundColor Green
Write-Host ""

# ============================================================================
# 3. Frontend Setup
# ============================================================================

Write-Host "🎨 Frontend kurulumu başlıyor..." -ForegroundColor Cyan

Set-Location "$ROOT_DIR\frontend"

# Dependencies kur
Write-Host "📥 Frontend dependencies kuruluyor..." -ForegroundColor Cyan
npm install

Write-Host "✅ Frontend kurulumu tamamlandı!" -ForegroundColor Green
Write-Host ""

# ============================================================================
# 4. Docker Services Başlat
# ============================================================================

Write-Host "🐳 Docker servisleri başlatılıyor..." -ForegroundColor Cyan

Set-Location $ROOT_DIR

# Eski container'ları durdur
Write-Host "🛑 Eski container'lar durduruluyor..." -ForegroundColor Cyan
docker-compose down 2>$null

# Development ortamı için docker-compose.dev.yml yoksa oluştur
if (-not (Test-Path "docker-compose.dev.yml")) {
    Write-Host "📝 docker-compose.dev.yml oluşturuluyor..." -ForegroundColor Cyan
    
    $devComposeContent = @"
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: nextgent_db_dev
    volumes:
      - postgres_data_dev:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=nextgent
    ports:
      - "5432:5432"
    networks:
      - nextgent_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: nextgent_redis_dev
    ports:
      - "6379:6379"
    volumes:
      - redis_data_dev:/data
    networks:
      - nextgent_network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    command: redis-server --appendonly yes

networks:
  nextgent_network:
    driver: bridge

volumes:
  postgres_data_dev:
  redis_data_dev:
"@
    
    $devComposeContent | Out-File -FilePath "docker-compose.dev.yml" -Encoding UTF8
}

# Container'ları başlat
Write-Host "🚀 Container'lar başlatılıyor..." -ForegroundColor Cyan
docker-compose -f docker-compose.dev.yml up -d

# Container'ların hazır olmasını bekle
Write-Host "⏳ Container'ların hazır olması bekleniyor..." -ForegroundColor Cyan
Start-Sleep -Seconds 10

# Container durumlarını kontrol et
Write-Host ""
Write-Host "📊 Container Durumları:" -ForegroundColor Cyan
docker-compose -f docker-compose.dev.yml ps

Write-Host ""
Write-Host "✅ Docker servisleri başlatıldı!" -ForegroundColor Green
Write-Host ""

# ============================================================================
# 5. Database Migration ve Seeding
# ============================================================================

Write-Host "🗄️ Database migration ve seeding başlıyor..." -ForegroundColor Cyan

Set-Location "$ROOT_DIR\backend"

# Virtual environment aktifleştir
& .\.venv\Scripts\Activate.ps1

# Database migration
Write-Host "📊 Database migration çalıştırılıyor..." -ForegroundColor Cyan
python init_db.py

# Sample data seeding
Write-Host "🌱 Sample data seeding yapılıyor..." -ForegroundColor Cyan
python comprehensive_seed.py

# Verileri kontrol et
Write-Host "🔍 Database verileri kontrol ediliyor..." -ForegroundColor Cyan
python check_db_data.py

Write-Host "✅ Database hazır!" -ForegroundColor Green
Write-Host ""

# ============================================================================
# 6. Test Çalıştır
# ============================================================================

Write-Host "🧪 Testler çalıştırılıyor..." -ForegroundColor Cyan

# Backend testleri
Write-Host "⚙️ Backend testleri..." -ForegroundColor Cyan
pytest tests/ -v --tb=short

Write-Host "✅ Testler tamamlandı!" -ForegroundColor Green
Write-Host ""

# ============================================================================
# 7. Özet ve Sonraki Adımlar
# ============================================================================

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🎉 NextGent Development Environment Kurulumu Tamamlandı!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "📋 Servis Bilgileri:" -ForegroundColor Yellow
Write-Host "  🌐 Frontend:        http://localhost:5173" -ForegroundColor White
Write-Host "  ⚙️  Backend API:     http://localhost:8000" -ForegroundColor White
Write-Host "  📚 API Docs:        http://localhost:8000/api/v1/docs" -ForegroundColor White
Write-Host "  🗄️  PostgreSQL:      localhost:5432" -ForegroundColor White
Write-Host "  🔴 Redis:           localhost:6379" -ForegroundColor White
Write-Host ""

Write-Host "🔑 Test Kullanıcı:" -ForegroundColor Yellow
Write-Host "  ID:  MED-001234" -ForegroundColor White
Write-Host "  PIN: 1234" -ForegroundColor White
Write-Host ""

Write-Host "🚀 Sonraki Adımlar:" -ForegroundColor Yellow
Write-Host "  1. Frontend başlat:  cd frontend && npm run dev" -ForegroundColor White
Write-Host "  2. Backend başlat:   cd backend && .\.venv\Scripts\Activate.ps1 && uvicorn app.main:app --reload" -ForegroundColor White
Write-Host "  3. Tarayıcıda aç:    http://localhost:5173" -ForegroundColor White
Write-Host "  4. Login ol:         MED-001234 / 1234" -ForegroundColor White
Write-Host ""

Write-Host "📚 Dokümantasyon:" -ForegroundColor Yellow
Write-Host "  - Lab Setup Guide:   C:\Users\icene\.gemini\antigravity\brain\80a98173-e2fe-4a76-a4a4-d6be8a835af6\lab_setup_guide.md" -ForegroundColor White
Write-Host "  - Implementation Plan: C:\Users\icene\.gemini\antigravity\brain\80a98173-e2fe-4a76-a4a4-d6be8a835af6\implementation_plan.md" -ForegroundColor White
Write-Host ""

Write-Host "💡 İpucu: Docker loglarını izlemek için:" -ForegroundColor Yellow
Write-Host "  docker-compose -f docker-compose.dev.yml logs -f" -ForegroundColor White
Write-Host ""

Write-Host "İyi çalışmalar! 💪" -ForegroundColor Green
Write-Host ""

# Ana dizine dön
Set-Location $ROOT_DIR
