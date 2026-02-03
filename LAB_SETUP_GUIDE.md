# 🧪 NextGent Lab Ortamı Kurulum Kılavuzu

Bu dokümantasyon, NextGent projesinin development, staging ve production ortamlarının kurulumu için adım adım rehberdir.

---

## 📋 Ön Gereksinimler

### Tüm Ekip Üyeleri İçin

#### Yazılım Gereksinimleri
- **Git**: v2.40+
- **Docker Desktop**: v24.0+ (Windows için)
- **Node.js**: v18+ (LTS)
- **Python**: v3.11+
- **PostgreSQL Client**: v15+ (opsiyonel, debugging için)
- **Redis CLI**: v7+ (opsiyonel, debugging için)
- **VS Code** veya **PyCharm Professional**

#### VS Code Extensions (Önerilen)
- Python (Microsoft)
- Pylance
- Volar (Vue.js)
- ESLint
- Prettier
- Docker
- GitLens
- Thunder Client (API testing)

#### Sistem Gereksinimleri
- **RAM**: Minimum 16GB (32GB önerilen)
- **Disk**: 50GB boş alan
- **CPU**: 4 core+ (8 core önerilen)

---

## 🚀 Hızlı Başlangıç (Quick Start)

### 1. Repository Clone

```powershell
# Ana dizine git
cd C:\Users\<username>\Desktop

# Repository'yi clone et
git clone <repository-url> NEXT-GENT
cd NEXT-GENT

# Branch oluştur (her developer kendi branch'inde çalışacak)
git checkout -b feature/<isim>-<feature-name>
# Örnek: git checkout -b feature/dogukan-chatbot-ui
```

### 2. Otomatik Setup (Önerilen)

```powershell
# Setup script'ini çalıştır
.\scripts\setup-dev-env.ps1

# Script şunları yapacak:
# - Python virtual environment oluşturma
# - Backend dependencies kurulumu
# - Frontend dependencies kurulumu
# - .env dosyası oluşturma
# - Docker container'ları başlatma
# - Database migration
# - Sample data seeding
```

### 3. Manuel Setup (Alternatif)

#### Backend Setup

```powershell
cd backend

# Virtual environment oluştur
python -m venv .venv

# Virtual environment'ı aktifleştir
.\.venv\Scripts\Activate.ps1

# Dependencies kur
pip install -r requirements.txt

# .env dosyası oluştur
cp .env.example .env

# .env dosyasını düzenle (gerekirse)
notepad .env
```

#### Frontend Setup

```powershell
cd frontend

# Dependencies kur
npm install

# Development server başlat (test için)
npm run dev
```

#### Docker Services Başlat

```powershell
# Ana dizinde
cd C:\Users\<username>\Desktop\NEXT-GENT

# Development ortamı için
docker-compose -f docker-compose.dev.yml up -d

# Servislerin durumunu kontrol et
docker-compose ps

# Logları izle
docker-compose logs -f
```

#### Database Migration ve Seeding

```powershell
cd backend

# Virtual environment aktif olmalı
.\.venv\Scripts\Activate.ps1

# Database migration
python init_db.py

# Sample data seeding
python comprehensive_seed.py

# Verileri kontrol et
python check_db_data.py
```

---

## 🏗️ Ortam Konfigürasyonları

### Development Ortamı

**Amaç**: Local geliştirme, hot reload, debug mode

**Servisler**:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- ML Service: http://localhost:8001 (gelecekte)

**Özellikler**:
- Hot reload aktif
- Debug mode açık
- Verbose logging
- Sample data otomatik yüklenir
- CORS tüm origin'lere açık

**Başlatma**:
```powershell
docker-compose -f docker-compose.dev.yml up -d
```

### Staging Ortamı

**Amaç**: Production-like testing, UAT, integration testing

**Servisler**:
- Frontend: https://staging.nextgent.com
- Backend API: https://api-staging.nextgent.com
- PostgreSQL: Ayrı staging database
- Redis: Ayrı staging instance

**Özellikler**:
- Production build
- SSL/TLS certificates
- Monitoring (Prometheus, Grafana)
- Real-world data (anonymized)
- CORS sadece staging domain

**Başlatma**:
```powershell
docker-compose -f docker-compose.staging.yml up -d
```

### Production Ortamı

**Amaç**: Canlı sistem, gerçek kullanıcılar

**Servisler**:
- Frontend: https://app.nextgent.com
- Backend API: https://api.nextgent.com
- PostgreSQL: Managed database (AWS RDS / Azure Database)
- Redis: Managed cache (AWS ElastiCache / Azure Cache)

**Özellikler**:
- Optimized production build
- Auto-scaling
- Backup & disaster recovery
- 24/7 monitoring
- Rate limiting strict

---

## 🔧 Ekip Üyelerine Özel Setup

### 🎨 Frontend Developer (Doğukan) Setup

#### Odak Alanı
- Vue.js components
- UI/UX development
- Responsive design
- Frontend testing

#### Özel Konfigürasyon

```powershell
cd frontend

# Development server başlat
npm run dev

# Tarayıcıda aç: http://localhost:5173

# Backend API'ye bağlanmak için .env dosyası (opsiyonel)
# frontend/.env.local oluştur:
echo "VITE_API_BASE_URL=http://localhost:8000/api/v1" > .env.local
```

#### Hot Reload Test
1. `frontend/src/components/HelpdeskChatbot.vue` dosyasını aç
2. Bir değişiklik yap (örn: title değiştir)
3. Kaydet
4. Tarayıcıda otomatik güncellendiğini gör

#### Component Geliştirme Workflow
```powershell
# Yeni component oluştur
cd frontend/src/components
# Dosya oluştur: YeniComponent.vue

# Component'i import et (örn: App.vue veya Dashboard.vue)
# Test et: http://localhost:5173

# Commit et
git add .
git commit -m "feat: add YeniComponent"
git push origin feature/dogukan-<feature-name>
```

#### Frontend Testing
```powershell
# Unit tests çalıştır
npm run test:unit

# E2E tests çalıştır (gelecekte)
npm run test:e2e

# Coverage report
npm run test:unit -- --coverage
```

---

### ⚙️ Backend Developer (Musa) Setup

#### Odak Alanı
- FastAPI endpoints
- Database models
- Business logic
- API testing

#### Özel Konfigürasyon

```powershell
cd backend

# Virtual environment aktifleştir
.\.venv\Scripts\Activate.ps1

# Development server başlat
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Tarayıcıda API docs aç: http://localhost:8000/api/v1/docs
```

#### Database Bağlantısı Test
```powershell
# Python REPL aç
python

# Database bağlantısını test et
>>> from app.core.database import engine
>>> import asyncio
>>> async def test():
...     async with engine.connect() as conn:
...         result = await conn.execute("SELECT 1")
...         print(result.scalar())
>>> asyncio.run(test())
# Çıktı: 1
```

#### API Endpoint Geliştirme Workflow
```powershell
# Yeni endpoint oluştur
cd backend/app/api/v1/endpoints
# Dosya oluştur: yeni_endpoint.py

# Router'a ekle: backend/app/api/v1/api.py
# Test et: http://localhost:8000/api/v1/docs

# Unit test yaz
cd backend/tests
# test_yeni_endpoint.py oluştur

# Test çalıştır
pytest tests/test_yeni_endpoint.py -v

# Commit et
git add .
git commit -m "feat: add yeni endpoint"
git push origin feature/musa-<feature-name>
```

#### Backend Testing
```powershell
# Tüm testleri çalıştır
pytest tests/ -v

# Coverage ile çalıştır
pytest tests/ -v --cov=app --cov-report=html

# Coverage report aç
start htmlcov/index.html

# Sadece integration testleri
pytest tests/integration/ -v

# Sadece unit testleri
pytest tests/unit/ -v
```

---

### 👨‍💼 Lider (İceneşik) Setup

#### Odak Alanı
- Full-stack oversight
- DevOps & CI/CD
- ML strategy
- Code review

#### Özel Konfigürasyon

```powershell
# Tüm servisleri başlat
docker-compose -f docker-compose.dev.yml up -d

# Servislerin health check'ini yap
curl http://localhost:8000/api/v1/health

# Frontend kontrol
curl http://localhost:5173

# Database kontrol
docker exec -it nextgent_db psql -U postgres -d nextgent -c "SELECT COUNT(*) FROM customers;"

# Redis kontrol
docker exec -it nextgent_redis redis-cli ping
```

#### Code Review Workflow
```powershell
# PR'ları listele
gh pr list

# PR'ı checkout et
gh pr checkout <pr-number>

# Değişiklikleri incele
git diff main

# Local'de test et
docker-compose -f docker-compose.dev.yml up -d
pytest tests/ -v
npm run test:unit

# Approve veya request changes
gh pr review <pr-number> --approve
# veya
gh pr review <pr-number> --request-changes -b "Feedback mesajı"
```

#### Monitoring ve Debugging
```powershell
# Container loglarını izle
docker-compose logs -f backend
docker-compose logs -f frontend

# Database loglarını izle
docker-compose logs -f db

# Redis loglarını izle
docker-compose logs -f redis

# Tüm container'ları yeniden başlat
docker-compose down
docker-compose -f docker-compose.dev.yml up -d --build
```

---

## 🗄️ Database Yönetimi

### Database Connection Bilgileri

**Development**:
```
Host: localhost
Port: 5432
Database: nextgent
Username: postgres
Password: postgres
```

### Database GUI Tools

#### pgAdmin (Önerilen)
```powershell
# Docker ile pgAdmin başlat
docker run -p 5050:80 -e "PGADMIN_DEFAULT_EMAIL=admin@nextgent.com" -e "PGADMIN_DEFAULT_PASSWORD=admin" -d dpage/pgadmin4

# Tarayıcıda aç: http://localhost:5050
# Login: admin@nextgent.com / admin
# Server ekle: localhost:5432
```

#### DBeaver (Alternatif)
- İndir: https://dbeaver.io/download/
- Connection: PostgreSQL
- Host: localhost, Port: 5432
- Database: nextgent, User: postgres, Password: postgres

### Database Migration

```powershell
cd backend

# Migration oluştur (gelecekte Alembic kullanılacak)
alembic revision --autogenerate -m "migration açıklaması"

# Migration uygula
alembic upgrade head

# Migration geri al
alembic downgrade -1
```

### Database Backup & Restore

```powershell
# Backup al
docker exec nextgent_db pg_dump -U postgres nextgent > backup_$(date +%Y%m%d).sql

# Restore et
docker exec -i nextgent_db psql -U postgres nextgent < backup_20260128.sql
```

---

## 🔴 Redis Yönetimi

### Redis Connection Bilgileri

**Development**:
```
Host: localhost
Port: 6379
Password: (yok)
```

### Redis CLI Kullanımı

```powershell
# Redis container'a bağlan
docker exec -it nextgent_redis redis-cli

# Komutlar:
PING                    # Bağlantı testi
KEYS *                  # Tüm key'leri listele
GET <key>               # Key'in değerini al
SET <key> <value>       # Key'e değer ata
DEL <key>               # Key'i sil
FLUSHALL                # Tüm cache'i temizle (dikkatli!)
INFO                    # Redis bilgileri
```

### Redis GUI Tool

#### RedisInsight (Önerilen)
- İndir: https://redis.com/redis-enterprise/redis-insight/
- Connection: localhost:6379

---

## 🤖 ML Service Setup (Gelecek)

### ML Service Kurulumu

```powershell
# ML service dizini oluştur
mkdir ml-service
cd ml-service

# Virtual environment oluştur
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Dependencies kur
pip install fastapi uvicorn transformers torch datasets

# requirements.txt oluştur
pip freeze > requirements.txt

# main.py oluştur (basit FastAPI app)
# Dockerfile oluştur
# docker-compose.yml'e ekle
```

### ML Model Training

```powershell
cd ml-service

# Dataset hazırla
python scripts/prepare_dataset.py

# Model eğit
python scripts/train_model.py --epochs 10 --batch-size 32

# Model test et
python scripts/test_model.py

# Model deploy et
docker build -t nextgent-ml-service .
docker run -p 8001:8001 nextgent-ml-service
```

---

## 🧪 Testing Stratejisi

### Test Seviyeleri

#### 1. Unit Tests
- **Amaç**: Fonksiyonların ve metodların doğruluğu
- **Kapsam**: %80+ code coverage
- **Araçlar**: pytest (backend), Vitest (frontend)

```powershell
# Backend unit tests
cd backend
pytest tests/unit/ -v --cov=app

# Frontend unit tests
cd frontend
npm run test:unit
```

#### 2. Integration Tests
- **Amaç**: Servislerin birbirleriyle entegrasyonu
- **Kapsam**: API endpoints, database, Redis
- **Araçlar**: pytest, httpx

```powershell
cd backend
pytest tests/integration/ -v
```

#### 3. E2E Tests
- **Amaç**: Kullanıcı akışlarının doğruluğu
- **Kapsam**: Login, dashboard, chatbot
- **Araçlar**: Playwright, Cypress

```powershell
cd frontend
npm run test:e2e
```

#### 4. Performance Tests
- **Amaç**: Sistem performansı ve ölçeklenebilirlik
- **Kapsam**: Load testing, stress testing
- **Araçlar**: Locust, k6

```powershell
# Load test çalıştır
locust -f scripts/load-test.py --host http://localhost:8000
```

---

## 🔒 Security Best Practices

### Environment Variables
- **Asla** `.env` dosyasını commit etme
- `.env.example` dosyasını güncel tut
- Production'da secrets management kullan (AWS Secrets Manager, Azure Key Vault)

### API Keys
- OpenAI API key'i `.env` dosyasında sakla
- Asla hardcode etme
- Rate limiting uygula

### Database
- Strong password kullan (production)
- SSL/TLS connection (production)
- Regular backup al

### CORS
- Development: Tüm origin'lere açık
- Production: Sadece frontend domain'e izin ver

---

## 🐛 Troubleshooting

### Docker Container Başlamıyor

```powershell
# Container'ları durdur
docker-compose down

# Volume'leri temizle
docker volume prune

# Image'leri yeniden build et
docker-compose -f docker-compose.dev.yml up -d --build

# Logları kontrol et
docker-compose logs -f
```

### Database Bağlantı Hatası

```powershell
# Database container'ın çalıştığını kontrol et
docker ps | findstr nextgent_db

# Database loglarını kontrol et
docker-compose logs db

# Database'e manuel bağlan
docker exec -it nextgent_db psql -U postgres -d nextgent

# Connection string'i kontrol et (.env dosyası)
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/nextgent
```

### Frontend Build Hatası

```powershell
# node_modules sil
cd frontend
rm -rf node_modules

# Cache temizle
npm cache clean --force

# Dependencies yeniden kur
npm install

# Dev server başlat
npm run dev
```

### Backend Import Hatası

```powershell
# Virtual environment'ı yeniden oluştur
cd backend
rm -rf .venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Dependencies yeniden kur
pip install -r requirements.txt

# PYTHONPATH'i ayarla (gerekirse)
$env:PYTHONPATH = "C:\Users\<username>\Desktop\NEXT-GENT\backend"
```

### Port Zaten Kullanımda

```powershell
# Port'u kullanan process'i bul
netstat -ano | findstr :8000

# Process'i sonlandır (PID ile)
taskkill /PID <PID> /F

# Veya farklı port kullan
uvicorn app.main:app --reload --port 8001
```

---

## 📚 Faydalı Komutlar

### Git Workflow

```powershell
# Güncel kodu çek
git pull origin main

# Yeni branch oluştur
git checkout -b feature/<isim>-<feature>

# Değişiklikleri stage et
git add .

# Commit et
git commit -m "feat: açıklama"

# Push et
git push origin feature/<isim>-<feature>

# PR oluştur (GitHub web UI veya gh CLI)
gh pr create --title "Feature: Açıklama" --body "Detaylı açıklama"
```

### Docker Komutları

```powershell
# Tüm container'ları başlat
docker-compose up -d

# Tüm container'ları durdur
docker-compose down

# Logları izle
docker-compose logs -f

# Belirli bir servisin logunu izle
docker-compose logs -f backend

# Container'a shell ile bağlan
docker exec -it nextgent_backend bash

# Container'ları yeniden build et
docker-compose up -d --build

# Kullanılmayan image'leri temizle
docker image prune -a
```

### Python Komutları

```powershell
# Virtual environment aktifleştir
.\.venv\Scripts\Activate.ps1

# Dependencies kur
pip install -r requirements.txt

# Yeni package ekle
pip install <package-name>
pip freeze > requirements.txt

# Python REPL
python

# Script çalıştır
python script.py
```

### Node.js Komutları

```powershell
# Dependencies kur
npm install

# Package ekle
npm install <package-name>

# Dev server başlat
npm run dev

# Production build
npm run build

# Build'i preview et
npm run preview
```

---

## 🎯 Sonraki Adımlar

1. ✅ Bu dokümantasyonu oku
2. ✅ Gerekli yazılımları kur
3. ✅ Repository'yi clone et
4. ✅ Setup script'ini çalıştır veya manuel setup yap
5. ✅ Development environment'ı test et
6. ✅ İlk task'ını seç (task.md'den)
7. ✅ Feature branch oluştur
8. ✅ Geliştirmeye başla! 🚀

---

## 📞 Destek

Herhangi bir sorun yaşarsan:
1. Bu dokümantasyonun Troubleshooting bölümünü kontrol et
2. Ekip Slack/Discord kanalında sor
3. Lider ile 1-on-1 meeting ayarla

**İyi çalışmalar! 💪**
