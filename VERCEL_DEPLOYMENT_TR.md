# Vercel Deployment - Türkçe Kılavuz

## 🎉 Hazırlık Tamamlandı!

Tüm kod değişiklikleri ve yapılandırma dosyaları oluşturuldu. NextGent CRM sisteminiz artık Vercel'e deploy edilmeye hazır!

## 📋 Yapılanlar (Otomatik)

### ✅ Oluşturulan/Güncellenen Dosyalar

1. **`vercel.json`** - Vercel yapılandırması
2. **`frontend/.env.production`** - Üretim ortamı değişkenleri
3. **`backend/app/main.py`** - CORS yapılandırması güncellendi
4. **`backend/.env.example`** - Üretim ortamı örnekleri eklendi
5. **`frontend/src/composables/useWebSocket.js`** - WebSocket yapılandırması güncellendi
6. **`.gitignore`** - Backup klasörü eklendi

### ✅ Oluşturulan Scriptler

- `scripts/export-database.ps1` - Veritabanını dışa aktarma (Windows)
- `scripts/export-database.sh` - Veritabanını dışa aktarma (Linux/Mac)
- `scripts/import-database.ps1` - Vercel Postgres'e aktarma
- `scripts/README.md` - Script dokümantasyonu

### ✅ Oluşturulan Dokümantasyon

- `VERCEL_DEPLOYMENT_GUIDE.md` - Detaylı deployment kılavuzu (İngilizce)
- `QUICK_START_VERCEL.md` - Hızlı başlangıç kılavuzu (İngilizce)
- `DEPLOYMENT_SUMMARY.md` - Özet dokümantasyon
- `VERCEL_DEPLOYMENT_TR.md` - Bu dosya (Türkçe)

## 🚀 5 Adımda Deployment

### Adım 1: Vercel Storage Kurulumu (10-15 dakika)

1. https://vercel.com/dashboard adresine gidin
2. **Storage** → **Create Database** → **Postgres** seçin
3. İsim: `nextgent-db`, Bölge: `Frankfurt (fra1)`
4. Bağlantı bilgilerini kopyalayın
5. Aynı şekilde **KV** (Redis) oluşturun

**Detaylı talimatlar**: `QUICK_START_VERCEL.md` - Step 1

### Adım 2: Veritabanını Aktarma (15-20 dakika)

**2.1. Docker'dan Dışa Aktarma:**

```powershell
# PowerShell'de çalıştırın
.\scripts\export-database.ps1
```

Bu script:
- Docker container'ının çalıştığını kontrol eder
- Veritabanını `backups` klasörüne kaydeder
- Hem binary (.dump) hem de SQL (.sql) formatında yedek alır

**2.2. Vercel Postgres'e Aktarma:**

```powershell
# Vercel connection string'inizi kullanın
.\scripts\import-database.ps1 "postgres://user:pass@host.vercel-storage.com:5432/verceldb" ".\backups\nextgent_backup_XXXXXX.dump"
```

**Detaylı talimatlar**: `scripts/README.md`

### Adım 3: Backend'i Railway/Render'a Deploy Etme (20-30 dakika)

**Railway kullanarak (Önerilen):**

1. https://railway.app adresine gidin ve hesap oluşturun
2. **New Project** → **Deploy from GitHub repo**
3. NextGent repository'nizi seçin
4. Root Directory: `backend`
5. Environment Variables ekleyin (aşağıdaki listeden)
6. Deploy edin
7. Public URL'yi kopyalayın (örn: `https://nextgent-backend.up.railway.app`)

**Gerekli Environment Variables:**

```env
# Uygulama
PROJECT_NAME=NextGent
API_V1_STR=/api/v1
ENVIRONMENT=production
DEBUG=false

# Güvenlik (YENİ ANAHTARLAR OLUŞTURUN!)
SECRET_KEY=yeni-secret-key-buraya
ENCRYPTION_KEY=yeni-encryption-key-buraya

# Veritabanı (Vercel Postgres'ten)
POSTGRES_SERVER=your-host.vercel-storage.com
POSTGRES_USER=default
POSTGRES_PASSWORD=your-password
POSTGRES_DB=verceldb
POSTGRES_PORT=5432
DATABASE_URL=postgres://...

# Redis (Vercel KV'den)
REDIS_HOST=your-redis-host.vercel-storage.com
REDIS_PORT=6379
REDIS_PASSWORD=your-password
REDIS_URL=redis://...

# CORS (Frontend URL'yi ekleyin)
BACKEND_CORS_ORIGINS=http://localhost:5173,https://your-domain.vercel.app

# OpenAI (opsiyonel)
OPENAI_API_KEY=your-key
AI_MODEL=gpt-4o-mini
AI_ENABLED=true
```

**Yeni Anahtarlar Oluşturma:**

```bash
# SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# ENCRYPTION_KEY
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

**Detaylı talimatlar**: `VERCEL_DEPLOYMENT_GUIDE.md` - Phase 4

### Adım 4: Frontend'i Vercel'e Deploy Etme (10-15 dakika)

**4.1. Backend URL'sini Güncelleme:**

`frontend/.env.production` dosyasını düzenleyin:

```env
VITE_API_BASE_URL=https://nextgent-backend.up.railway.app/api/v1
```

**4.2. Vercel'e Deploy:**

```bash
# Proje klasörüne gidin
cd c:\Users\icene\Desktop\NEXT-GENT

# Vercel'e login olun
vercel login

# Production'a deploy edin
vercel --prod
```

Ya da Vercel Dashboard kullanın:
1. https://vercel.com/new
2. **Import Git Repository** → NextGent'i seçin
3. Ayarlar:
   - Build Command: `cd frontend && npm install && npm run build`
   - Output Directory: `frontend/dist`
   - Environment Variable: `VITE_API_BASE_URL=https://backend-url/api/v1`
4. **Deploy**

**4.3. Vercel URL'sini Kopyalayın**

Örnek: `https://nextgent.vercel.app`

**Detaylı talimatlar**: `VERCEL_DEPLOYMENT_GUIDE.md` - Phase 5

### Adım 5: CORS Güncelleme ve Test (10 dakika)

**5.1. Backend CORS Güncelleme:**

Railway dashboard'a gidin ve `BACKEND_CORS_ORIGINS` değişkenini güncelleyin:

```
https://nextgent.vercel.app,https://sizin-domain.com
```

Backend'i yeniden deploy edin.

**5.2. Test:**

1. `https://nextgent.vercel.app` adresine gidin
2. Test hesaplarıyla giriş yapın:
   - Beauty: `BEA-000001` / PIN: `1234`
   - Hotel: `HOS-000001` / PIN: `1234`
   - Medical: `MED-000001` / PIN: `1234`
3. Dashboard'un yüklendiğini kontrol edin
4. API çağrılarının çalıştığını kontrol edin (Browser DevTools → Network)
5. WebSocket bağlantısını kontrol edin (sağ alt köşe göstergesi)

## 🌐 Özel Domain Bağlama (Opsiyonel)

### Domain Ekleme

1. Vercel Dashboard → Projeniz → **Settings** → **Domains**
2. Domain'inizi ekleyin (örn: `nextgent.com`)
3. DNS kayıtlarını güncelleyin:
   - **A Record**: `@` → `76.76.21.21`
   - veya **CNAME**: `www` → `cname.vercel-dns.com`

### CORS Güncelleme

Backend CORS'a domain'inizi ekleyin:

```
BACKEND_CORS_ORIGINS=https://nextgent.vercel.app,https://nextgent.com
```

Backend'i yeniden deploy edin.

## 💰 Maliyet Tahmini

| Servis | Paket | Aylık Maliyet |
|--------|-------|---------------|
| Vercel (Frontend) | Hobby/Pro | $0-20 |
| Vercel Postgres | Pro | $5-10 |
| Vercel KV (Redis) | Free/Pro | $0-1 |
| Railway (Backend) | Starter | $5-20 |

**Toplam**: ~$10-50/ay (production-ready kurulum)

## 📚 Dokümantasyon

| Dosya | Açıklama | Ne Zaman Kullanılır |
|-------|----------|---------------------|
| `QUICK_START_VERCEL.md` | Hızlı başlangıç (İngilizce) | Buradan başlayın! |
| `VERCEL_DEPLOYMENT_GUIDE.md` | Detaylı kılavuz (İngilizce) | Detaylı talimatlar için |
| `scripts/README.md` | Script dokümantasyonu | Veritabanı aktarımı için |
| `DEPLOYMENT_SUMMARY.md` | Özet bilgiler | Genel bakış için |
| `VERCEL_DEPLOYMENT_TR.md` | Türkçe kılavuz | Bu dosya |

## 🔧 Yapılandırma Dosyaları

| Dosya | Durum | Açıklama |
|-------|-------|----------|
| `vercel.json` | ✅ Oluşturuldu | Vercel yapılandırması |
| `frontend/.env.production` | ⚠️ Güncellenmeli | Backend URL eklenecek |
| `backend/.env.example` | ✅ Güncellendi | Production örnekleri |
| `backend/app/main.py` | ✅ Güncellendi | CORS yapılandırması |
| `frontend/src/composables/useWebSocket.js` | ✅ Güncellendi | WebSocket yapılandırması |

## ⚠️ Önemli Notlar

### Güvenlik Kontrol Listesi

Deployment öncesi kontrol edin:

- [ ] Yeni `SECRET_KEY` oluşturuldu
- [ ] Yeni `ENCRYPTION_KEY` oluşturuldu
- [ ] `BACKEND_CORS_ORIGINS` belirli domain'lerle güncellendi
- [ ] `DEBUG=false` production'da
- [ ] Veritabanı backup'ı alındı
- [ ] `.env` dosyaları Git'e commit edilmedi

### Backup Dosyaları

- Backup dosyaları `backups/` klasöründe saklanır
- Bu dosyalar hassas veri içerir - güvende tutun
- Git'e commit etmeyin (`.gitignore`'da mevcut)
- Deployment sonrası silmeyin - geri dönüş için gerekli

## 🆘 Yardım ve Sorun Giderme

### Sık Karşılaşılan Sorunlar

**CORS Hataları:**
- Çözüm: Backend `BACKEND_CORS_ORIGINS`'e Vercel URL'nizi ekleyin

**Veritabanı Bağlantı Hatası:**
- Çözüm: Vercel Postgres connection string'ini kontrol edin

**WebSocket Bağlanamıyor:**
- Çözüm: Console loglarını kontrol edin, backend WebSocket endpoint'ini doğrulayın

**Build Hatası:**
- Çözüm: Vercel build loglarını kontrol edin, `vercel.json`'u doğrulayın

### Kaynaklar

- Vercel Dokümantasyonu: https://vercel.com/docs
- Railway Dokümantasyonu: https://docs.railway.app
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/

## 🎯 Sonraki Adımlar

### Hemen Şimdi

1. `QUICK_START_VERCEL.md` dosyasını okuyun
2. Adım 1'den başlayın: Vercel Storage kurulumu
3. 5 adımı sırasıyla takip edin

### Deployment Sonrası

1. **Monitoring Kurulumu**: Vercel Analytics'i etkinleştirin
2. **Performance Testing**: API endpoint'lerinizi test edin
3. **Backup Stratejisi**: Otomatik veritabanı backup'ı ayarlayın
4. **CI/CD**: GitHub Actions ile otomatik test yapılandırın
5. **Dokümantasyon**: Ekip dokümantasyonunu yeni URL'lerle güncelleyin

## 📊 Mimari Karşılaştırma

### Öncesi (Docker)
```
Docker Compose
├── Vue.js + Nginx (Port 80)
├── FastAPI (Port 8001)
├── PostgreSQL (Port 5432)
└── Redis (Port 6379)

Erişim: http://localhost
```

### Sonrası (Vercel + Railway)
```
Domain → Vercel (Frontend)
           ↓
         Railway (Backend)
           ↓
    ┌──────┴──────┐
    ↓             ↓
Vercel Postgres   Vercel KV
```

**Avantajlar:**
- ✅ Global CDN (Dünya çapında hızlı erişim)
- ✅ Otomatik HTTPS ve SSL
- ✅ Yönetilen veritabanı ve Redis
- ✅ Otomatik ölçeklendirme
- ✅ Sıfır downtime deployment
- ✅ Otomatik backup'lar
- ✅ Monitoring ve analytics
- ✅ GitHub'dan otomatik deployment

## ✨ Özet

### Tamamlanan İşler

- ✅ 7 dosya oluşturuldu/güncellendi
- ✅ 2 kod dosyası güncellendi (CORS, WebSocket)
- ✅ 4 veritabanı migration script'i oluşturuldu
- ✅ 5 dokümantasyon dosyası oluşturuldu

### Yapılacaklar

- 📋 5 adımlı deployment sürecini takip edin
- ⏱️ Tahmini süre: 1-2 saat

### Başlamaya Hazır?

**İlk adım**: `QUICK_START_VERCEL.md` dosyasını açın ve Adım 1'den başlayın!

```powershell
# Hızlı başlangıç kılavuzunu açın
code QUICK_START_VERCEL.md

# Veritabanını dışa aktarın
.\scripts\export-database.ps1

# 5 adımlı süreci takip edin
```

---

**Başarılar! 🚀**

Sorularınız için tüm detaylı dokümantasyon hazır. Deployment sürecinde başarılar dileriz!

*Son güncelleme: 12 Şubat 2026*
