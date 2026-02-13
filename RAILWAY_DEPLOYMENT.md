# Railway Backend Deployment Kılavuzu - NextGent CRM

## 🎯 Genel Bakış

Bu kılavuz, NextGent CRM backend'ini Railway'e deploy etmenizi ve custom domain bağlantısını yapmanızı sağlar.

**Railway Avantajları:**
- ✅ $5 ücretsiz credit/ay
- ✅ Docker container desteği
- ✅ Otomatik HTTPS ve SSL
- ✅ Kolay deployment
- ✅ GitHub entegrasyonu
- ✅ Custom domain desteği

## 📋 Ön Gereksinimler

### Hazır Olanlar
- ✅ Frontend Vercel'de: https://nextgent.co
- ✅ Database backup: `backups\nextgent_backup_20260212_110141.dump`
- ✅ Docker image hazır: `backend/Dockerfile`

### Yapmanız Gerekenler
- [ ] Vercel Postgres database oluşturma
- [ ] Vercel KV (Redis) oluşturma
- [ ] Database import
- [ ] Railway hesabı
- [ ] GitHub repository erişimi

## 🚀 Adım 1: Vercel Storage Kurulumu (10 dakika)

### 1.1. Vercel Postgres Database

1. **Vercel Dashboard'a gidin**: https://vercel.com/dashboard
2. Sol menüden **Storage** seçin
3. **Create Database** → **Postgres** seçin
4. Database ayarları:
   - **Name**: `nextgent-db`
   - **Region**: **Frankfurt (fra1)**
   - **Pricing**: **Hobby** veya **Pro**
5. **Create** butonuna tıklayın
6. **Quickstart** sekmesine gidin
7. Connection string'leri kopyalayın:

```env
POSTGRES_URL="postgres://default:xxx@ep-xxx.vercel-storage.com:5432/verceldb"
POSTGRES_SERVER="ep-xxx.vercel-storage.com"
POSTGRES_USER="default"
POSTGRES_PASSWORD="xxx"
POSTGRES_DB="verceldb"
```

**Not**: Bu bilgileri güvenli bir yere kaydedin!

### 1.2. Vercel KV (Redis) Database

1. Vercel Dashboard → **Storage** → **Create Database**
2. **KV** (Redis) seçin
3. Database ayarları:
   - **Name**: `nextgent-redis`
   - **Region**: **Frankfurt (fra1)** (Postgres ile aynı)
   - **Pricing**: **Free** tier yeterli
4. **Create** butonuna tıklayın
5. **Quickstart** sekmesinden connection details'i kopyalayın:

```env
KV_URL="redis://default:xxx@xxx.vercel-storage.com:6379"
REDIS_HOST="xxx.vercel-storage.com"
REDIS_PORT="6379"
REDIS_PASSWORD="xxx"
```

### 1.3. Database Import

**PostgreSQL Client Kurulumu** (eğer yoksa):

```powershell
# Chocolatey ile
choco install postgresql

# Veya Winget ile
winget install PostgreSQL.PostgreSQL
```

**Database Import İşlemi:**

```powershell
# Import komutu (Vercel Postgres URL'nizi kullanın)
pg_restore -d "postgres://default:xxx@ep-xxx.vercel-storage.com:5432/verceldb" -v backups\nextgent_backup_20260212_110141.dump
```

**Beklenen Çıktı:**
```
pg_restore: creating TABLE "public.tenants"
pg_restore: creating TABLE "public.customers"
...
pg_restore: creating CONSTRAINT "public.tenants tenants_pkey"
```

**Not**: Bazı uyarılar normal (permission warnings). Önemli olan "ERROR:" olmadan tamamlanması.

**Doğrulama:**

Vercel Dashboard → Postgres database → **Data** sekmesinde tabloları görebilmelisiniz.

## 🚂 Adım 2: Railway Hesabı ve Deployment (20 dakika)

### 2.1. Railway Hesabı Oluşturma

1. **Railway'e gidin**: https://railway.app
2. **Start a New Project** butonuna tıklayın
3. **Login with GitHub** seçin
4. GitHub ile giriş yapın
5. Railway'e repository erişim izni verin

### 2.2. Backend Projesini Deploy Etme

1. Railway Dashboard'da **New Project** butonuna tıklayın
2. **Deploy from GitHub repo** seçin
3. **NextGent** repository'nizi seçin
4. Repository seçildikten sonra **bekleyin** (henüz deploy başlamamalı)

### 2.3. Service Settings

Deploy başlamadan önce ayarları yapılandırın:

1. **Settings** sekmesine gidin
2. Aşağıdaki ayarları yapın:
   - **Service Name**: `nextgent-backend`
   - **Root Directory**: `backend`
   - **Builder**: Docker (otomatik algılanmalı)
   - **Watch Paths**: `backend/**`

### 2.4. Environment Variables

**Variables** sekmesine gidin ve aşağıdaki değişkenleri ekleyin:

#### Uygulama Ayarları
```env
PROJECT_NAME=NextGent
API_V1_STR=/api/v1
ENVIRONMENT=production
DEBUG=false
```

#### Güvenlik Anahtarları (YENİ OLUŞTURUN!)

PowerShell'de çalıştırın:
```powershell
# SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# ENCRYPTION_KEY
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Çıktıları kopyalayın:
```env
SECRET_KEY=<yukarıdan-kopyala>
ENCRYPTION_KEY=<yukarıdan-kopyala>
```

#### Vercel Postgres (Adım 1'den)
```env
DATABASE_URL=postgres://default:xxx@ep-xxx.vercel-storage.com:5432/verceldb
POSTGRES_SERVER=ep-xxx.vercel-storage.com
POSTGRES_USER=default
POSTGRES_PASSWORD=xxx
POSTGRES_DB=verceldb
POSTGRES_PORT=5432
```

#### Vercel KV / Redis (Adım 1'den)
```env
REDIS_URL=redis://default:xxx@xxx.vercel-storage.com:6379
REDIS_HOST=xxx.vercel-storage.com
REDIS_PORT=6379
REDIS_PASSWORD=xxx
```

#### CORS
```env
BACKEND_CORS_ORIGINS=https://next-gent-bbxs21jcs-enesics-projects.vercel.app,https://nextgent.co
```

#### OpenAI (Opsiyonel)
```env
OPENAI_API_KEY=sk-proj-your-key-here
AI_MODEL=gpt-4o-mini
AI_ENABLED=true
```

### 2.5. Deploy Başlatma

1. Tüm environment variables'ı ekledikten sonra **Deploy** butonuna tıklayın
2. **Deployments** sekmesinde logları izleyin
3. Build süreci (3-5 dakika):
   ```
   Building Docker image...
   [+] Building 45.2s
   => [internal] load build definition
   => => transferring dockerfile: 1.23kB
   ...
   => exporting to image
   ✓ Built in 45s
   ```

4. Deployment başarılı olunca **Settings** → **Networking** sekmesinden public URL'yi alın:
   ```
   https://nextgent-backend-production.up.railway.app
   ```

### 2.6. Health Check

URL'yi test edin:
```powershell
curl https://nextgent-backend-production.up.railway.app/api/v1/health
```

Başarılı response:
```json
{
  "status": "healthy",
  "service": "NextGent",
  "environment": "production",
  "checks": {
    "database": {"status": "healthy", "message": "PostgreSQL connection successful"},
    "redis": {"status": "healthy", "message": "Redis connection successful"}
  }
}
```

## 🔄 Adım 3: Frontend Güncelleme (5 dakika)

### 3.1. Environment Variable Güncelleme

`frontend\.env.production` dosyasını açın:

```env
VITE_API_BASE_URL=https://nextgent-backend-production.up.railway.app/api/v1
```

**Not**: `nextgent-backend-production.up.railway.app` kısmını kendi Railway URL'nizle değiştirin.

### 3.2. Vercel'e Yeniden Deploy

```powershell
cd c:\Users\icene\Desktop\NEXT-GENT
vercel --prod --yes
```

Deploy tamamlandığında:
```
✅ Production: https://nextgent.co [32s]
```

### 3.3. İlk Test

1. **Frontend**: https://nextgent.co
2. **Login Test**: 
   - Beauty: `BEA-000001` / PIN: `1234`
   - Hotel: `HOS-000001` / PIN: `1234`
   - Medical: `MED-000001` / PIN: `1234`
3. **Network Tab**: API çağrılarının Railway URL'sine gittiğini kontrol edin

## 🌐 Adım 4: Custom Domain Bağlantısı (15 dakika)

### 4.1. Railway'de Custom Domain Ekleme

1. Railway Dashboard → Backend service seçin
2. **Settings** sekmesi → **Networking** bölümü
3. **Custom Domains** altında **Add Custom Domain**
4. Backend subdomain'inizi girin:
   - `api.yourdomain.com` (önerilen)
   - veya `backend.yourdomain.com`
5. **Add Domain** butonuna tıklayın

Railway size DNS kayıtlarını gösterecek.

### 4.2. DNS Yapılandırması

Domain sağlayıcınıza (GoDaddy, Namecheap, Cloudflare, vb.) gidin:

**CNAME Record Ekleme:**

| Tip | İsim | Değer | TTL |
|-----|------|-------|-----|
| CNAME | `api` | `nextgent-backend-production.up.railway.app` | 3600 |

**Alternatif - A Record** (CNAME çalışmazsa):

Railway'de gösterilen IP adresini kullanın:

| Tip | İsim | Değer | TTL |
|-----|------|-------|-----|
| A | `api` | `[Railway IP]` | 3600 |

### 4.3. DNS Doğrulama

**Windows:**
```powershell
nslookup api.yourdomain.com
```

**Başarılı sonuç:**
```
Server:  UnKnown
Address:  192.168.1.1

Non-authoritative answer:
Name:    nextgent-backend-production.up.railway.app
Address:  [IP]
Aliases:  api.yourdomain.com
```

**Not**: DNS propagation 5 dakika - 24 saat sürebilir.

### 4.4. SSL Sertifikası

Railway otomatik olarak Let's Encrypt SSL sertifikası oluşturur (5-10 dakika).

Railway Dashboard'da domain status:
```
✓ api.yourdomain.com - Active
```

### 4.5. CORS Güncelleme

Railway Dashboard → Variables sekmesi → `BACKEND_CORS_ORIGINS` değişkenini güncelleyin:

```env
BACKEND_CORS_ORIGINS=https://next-gent-bbxs21jcs-enesics-projects.vercel.app,https://nextgent.co,https://api.yourdomain.com
```

Save → Service otomatik redeploy olacak (1-2 dakika).

### 4.6. Frontend Custom Domain Kullanımı (Opsiyonel)

Eğer frontend'te custom backend domain kullanmak isterseniz:

`frontend\.env.production`:
```env
VITE_API_BASE_URL=https://api.yourdomain.com/api/v1
```

Vercel'e tekrar deploy:
```powershell
vercel --prod --yes
```

## ✅ Adım 5: Test ve Doğrulama (10 dakika)

### 5.1. Backend Health Check

```powershell
# Railway URL
curl https://nextgent-backend-production.up.railway.app/api/v1/health

# Custom domain
curl https://api.yourdomain.com/api/v1/health
```

### 5.2. Frontend End-to-End Test

1. **https://nextgent.co** adresini açın
2. **Login**:
   - Beauty sector: `BEA-000001` / `1234`
   - Hospitality: `HOS-000001` / `1234`
   - Medical: `MED-000001` / `1234`

3. **Dashboard Kontrolü**:
   - Müşteri sayıları yükleniyor mu?
   - Grafikler görünüyor mu?
   - Anlık bildirimler çalışıyor mu?

4. **API Kontrolü** (Browser DevTools → Network):
   - API endpoint'leri: `https://api.yourdomain.com/api/v1/*`
   - Status: `200 OK`
   - CORS: Hata yok

5. **WebSocket Kontrolü** (Console):
   ```
   🔌 Connecting to WebSocket: wss://api.yourdomain.com/api/v1/ws/...
   ✅ WebSocket Connected
   ```

### 5.3. CRUD Operasyonları Testi

- [ ] Yeni müşteri ekleme
- [ ] Müşteri düzenleme
- [ ] Randevu oluşturma
- [ ] Randevu silme
- [ ] Dashboard filtreleme
- [ ] Arama işlevi

## 💰 Maliyet Breakdown

| Servis | Paket | Aylık Maliyet |
|--------|-------|---------------|
| Vercel Frontend | Hobby | $0 |
| Vercel Postgres | Hobby/Pro | $5-10 |
| Vercel KV | Free | $0 |
| Railway Backend | Hobby | **$5 credit → sonra $5-20** |
| **Toplam** | | **İlk ay: $5-10** |
| | | **Sonraki aylar: $10-30** |

**Railway Pricing Detayları:**
- İlk $5 credit ücretsiz
- Credit bitince: $0.000231/GB-hour (RAM) + $0.000463/vCPU-hour
- Ortalama kullanım: ~$10-20/ay
- Sleep mode yok (7/24 aktif)

## 🔧 Troubleshooting

### Railway Deployment Hatası

**Problem**: Build fail
```
Error: docker build failed
```

**Çözüm**:
1. Railway Dashboard → Deployments → Logs kontrol edin
2. Local'de build test edin:
   ```powershell
   cd backend
   docker build -t test-backend .
   ```
3. Environment variables eksik mi kontrol edin

---

**Problem**: Service başlamıyor
```
Error: Application failed to respond
```

**Çözüm**:
1. Health check path kontrol edin: `/api/v1/health`
2. Port 8000 açık mı kontrol edin (Dockerfile EXPOSE 8000)
3. Logs'da database connection hatasına bakın

### Custom Domain Çalışmıyor

**Problem**: Domain erişilemiyor

**Çözüm**:
1. DNS propagation bekleyin (1-24 saat)
2. DNS test edin: `nslookup api.yourdomain.com`
3. Railway'de domain status kontrol edin
4. SSL sertifikası oluştu mu kontrol edin

---

**Problem**: SSL certificate hatası

**Çözüm**:
1. Railway'de domain "Active" durumunda mı kontrol edin
2. 10 dakika bekleyin (Let's Encrypt provisioning)
3. Domain remove → re-add deneyin

### CORS Hatası

**Problem**: Browser console'da CORS error

```
Access to fetch at 'https://api.yourdomain.com' from origin 'https://nextgent.co' has been blocked by CORS policy
```

**Çözüm**:
1. Railway → Variables → `BACKEND_CORS_ORIGINS` değişkenini kontrol edin
2. Custom domain eklenmiş mi kontrol edin
3. Backend redeploy edin
4. Browser cache temizleyin (Ctrl+Shift+R)

### Database Connection Hatası

**Problem**: Database connection failed

**Çözüm**:
1. Vercel Postgres connection string doğru mu
2. Vercel Postgres → Settings → IP Whitelist kontrol edin (Railway IP'si gerekebilir)
3. `DATABASE_URL` ve diğer POSTGRES_* değişkenlerinin tutarlı olduğunu kontrol edin

## 📊 Monitoring

### Railway Metrics

Railway Dashboard → Service → **Metrics** sekmesi:
- CPU usage
- Memory usage
- Network traffic
- Request count

### Logs

Railway Dashboard → Service → **Deployments** → Latest deployment → **View Logs**

Yararlı log filtreleri:
```
# Sadece error logları
[ERROR]

# Database queries
SELECT

# API requests
GET /api/v1
POST /api/v1
```

### Alerts (Opsiyonel)

Railway Pro plan ile:
- Usage alerts
- Deployment failure alerts
- Downtime alerts

## 🔄 Güncelleme ve Redeploy

### Otomatik Deploy (GitHub)

Railway otomatik olarak GitHub push'larında deploy eder:

```bash
git add .
git commit -m "Backend update"
git push origin main
```

Railway 1-2 dakika içinde yeni versiyonu deploy eder.

### Manuel Redeploy

Railway Dashboard → Service → **Deployments** → **Redeploy**

### Rollback

Railway Dashboard → Service → **Deployments** → Eski deployment → **Redeploy**

## 📚 Ek Kaynaklar

- Railway Documentation: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/
- Vercel Postgres Docs: https://vercel.com/docs/storage/vercel-postgres

## ✅ Deployment Checklist

- [ ] Vercel Postgres oluşturuldu
- [ ] Vercel KV oluşturuldu
- [ ] Database import başarılı
- [ ] Railway hesabı oluşturuldu
- [ ] GitHub repository bağlandı
- [ ] Environment variables eklendi
- [ ] Railway'e deploy başarılı
- [ ] Backend health check çalışıyor
- [ ] Frontend Railway URL'ye bağlandı
- [ ] Frontend Vercel'e redeploy edildi
- [ ] Login test başarılı
- [ ] Custom domain eklendi (opsiyonel)
- [ ] DNS kayıtları güncellendi (opsiyonel)
- [ ] SSL sertifikası aktif (opsiyonel)
- [ ] CORS günceldi (custom domain için)
- [ ] Tüm özellikler test edildi

---

**Başarılar! Railway deployment tamamlandı! 🚂**

*Son güncelleme: 12 Şubat 2026*
