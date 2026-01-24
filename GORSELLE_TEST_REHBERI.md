# 👁️ Görsel Test Rehberi - NEXT-GENT

**Hedef**: Sistemi gözlerinizle görmek ve test etmek  
**Süre**: ~15 dakika  
**Zorluk**: Kolay

---

## 🚀 ADIM 1: Sistemi Başlatma

### Seçenek A: Docker ile (Önerilen - Tek Komut)

```powershell
# Proje ana dizininde (NEXT-GENT klasörü)
docker-compose up --build
```

**Ne Olacak?**
1. PostgreSQL veritabanı başlayacak (port 5432)
2. Redis cache başlayacak (port 6379)
3. Backend API başlayacak (port 8000)
4. Frontend başlayacak (port 80)

**Bekleme Süresi**: İlk seferde 2-3 dakika (image'ler indirilecek)

**Başarı İşareti**: Terminal'de şunları göreceksiniz:
```
✅ nextgent_db started
✅ nextgent_redis started
✅ nextgent_backend started
✅ nextgent_frontend started
```

---

### Seçenek B: Manuel Başlatma (Development)

**Terminal 1 - Backend:**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python init_db.py  # İlk seferde
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```powershell

npm install  # İlk seferde
npm run dev
```

**Terminal 3 - Redis (Eğer yoksa):**
```powershell
# Redis'i ayrı başlatmanız gerekebilir
# Docker kullanıyorsanız: docker run -d -p 6379:6379 redis:7-alpine
```

---

## 🌐 ADIM 2: Tarayıcıda Açma

### Frontend'i Aç
1. Tarayıcınızı açın (Chrome, Edge, Firefox)
2. Şu adrese gidin:
   - **Docker ile**: `http://localhost`
   - **Manuel ile**: `http://localhost:5173`

**Ne Göreceksiniz?**
- İlk açılışta **Landing Page** veya **Login** sayfası
- Modern, lüks bir arayüz
- Animasyonlu geçişler

---

## 🎨 ADIM 3: Görsel İnceleme - Frontend

### 3.1 Landing Page / Login Sayfası

**Kontrol Edilecekler:**
- [ ] Sayfa yüklendi mi? (Beyaz ekran yok mu?)
- [ ] Animasyonlar çalışıyor mu? (Orb animasyonları)
- [ ] Form görünüyor mu?
- [ ] Butonlar tıklanabilir mi?

**Göreceğiniz:**
- Modern login formu
- Arka planda animasyonlu "Orb" efektleri
- "Sign In" butonu

---

### 3.2 Login İşlemi

**Test Senaryosu:**
1. Herhangi bir email girin: `demo@nextgent.com`
2. Herhangi bir şifre girin: `demo123`
3. **Sign In** butonuna tıklayın

**Ne Olacak?**
- Form küçülerek kaybolacak (animasyon)
- Yeşil bir loader görünecek: "Authentication Verified"
- Dashboard'a geçiş yapılacak

**Göreceğiniz:**
- Sinematik geçiş animasyonu
- Dashboard ekranı

---

### 3.3 Dashboard (Executive Shell)

**Göreceğiniz Bileşenler:**

#### Sol Sidebar
- [ ] **Logo**: NextGent logosu + ikon
- [ ] **Ana Menü**: Dashboard, Müşteriler, Randevular, vb.
- [ ] **Çalışma Alanı**: Sektör bazlı menüler
- [ ] **Kullanıcı Profili**: Alt kısımda (Ahmet Yılmaz)

#### Üst Topbar
- [ ] **Sayfa Başlığı**: "Dashboard" veya aktif sayfa
- [ ] **Sektör Badge**: Medical, Legal, Real Estate switcher
- [ ] **Bildirim İkonu**: Bell ikonu
- [ ] **Arama İkonu**: Search ikonu

#### Ana İçerik Alanı
- [ ] **KPI Kartları**: 4-6 adet metrik kartı
- [ ] **Grafikler**: ApexCharts ile çizilmiş grafikler
- [ ] **AI Insight Cards**: AI önerileri
- [ ] **Call Volume Chart**: Çağrı hacmi grafiği

**Kontrol Edilecekler:**
- [ ] Tüm kartlar görünüyor mu?
- [ ] Grafikler render edildi mi?
- [ ] Animasyonlar smooth mu?
- [ ] Responsive mi? (Ekranı küçültüp büyütün)

---

## 🔍 ADIM 4: Sektör Değiştirme Testi

**Test Senaryosu:**
1. Üst sağdaki sektör switcher'a tıklayın
2. **Medical** → **Legal** → **Real Estate** arasında geçiş yapın

**Ne Olacak?**
- Sidebar ikonları değişecek
- Menü öğeleri sektöre göre güncellenecek
- Dashboard metrikleri değişecek

**Göreceğiniz:**
- Smooth fade-slide animasyonu
- Sektöre özel içerik

---

## 🧪 ADIM 5: API Testleri (Backend)

### 5.1 Health Check

**Tarayıcıda Aç:**
```
http://localhost:8000/api/v1/health
```

**Göreceğiniz:**
```json
{
  "status": "healthy",
  "service": "NextGent",
  "environment": "production",
  "checks": {
    "database": {
      "status": "healthy",
      "message": "PostgreSQL connection successful"
    },
    "redis": {
      "status": "healthy",
      "message": "Redis connection successful"
    }
  }
}
```

**Kontrol:**
- [ ] Status "healthy" mi?
- [ ] Database check "healthy" mi?
- [ ] Redis check "healthy" mi?

---

### 5.2 API Documentation (Swagger)

**Tarayıcıda Aç:**
```
http://localhost:8000/docs
```

**Göreceğiniz:**
- **Swagger UI**: Tüm API endpoint'leri
- **Try it out**: Her endpoint'i test edebilirsiniz
- **Request/Response**: Örnekler

**Test Edilecek Endpoint'ler:**
1. `GET /api/v1/health` - Health check
2. `GET /api/v1/tenants/me` - Current tenant (X-Tenant-ID header gerekli)
3. `GET /api/v1/metrics` - Metrics (X-Tenant-ID header gerekli)

---

### 5.3 Rate Limiting Testi

**Terminal'de Çalıştır:**
```powershell
# 110 request gönder (limit: 100/dakika)
for ($i=1; $i -le 110; $i++) {
    Invoke-WebRequest -Uri "http://localhost:8000/api/v1/health" -Headers @{"X-Tenant-ID"="test-tenant-id"}
    Write-Host "Request $i"
}
```

**Ne Olacak?**
- İlk 100 request: `200 OK`
- 101. request'ten itibaren: `429 Too Many Requests`
- Response header'da: `Retry-After: 60`

**Göreceğiniz:**
```
Request 1: 200 OK
Request 2: 200 OK
...
Request 100: 200 OK
Request 101: 429 Too Many Requests
Request 102: 429 Too Many Requests
```

---

## 🎯 ADIM 6: Brave Fallback Testi

**Test Senaryosu:**
1. Dashboard açıkken backend'i durdurun
2. Sayfayı yenileyin (F5)

**Ne Olacak?**
- ❌ Sayfa **BEYAZA DÜŞMEMELİ**
- ❌ Kırmızı hata mesajı **GÖRÜNMEMELİ**
- ✅ Grafikler ve KPI'lar **MOCK VERİLERLE** gelmeye devam etmeli
- ✅ Console'da: `🛡️ Brave Fallback Activated`

**Göreceğiniz:**
- Dashboard normal görünmeye devam eder
- Mock verilerle çalışır
- Kullanıcı deneyimi bozulmaz

---

## 📊 ADIM 7: Metrics Endpoint Testi

**Tarayıcıda Aç (Header ile):**
```
http://localhost:8000/api/v1/metrics
```

**Header Ekle:**
- `X-Tenant-ID`: Herhangi bir UUID (örn: `550e8400-e29b-41d4-a716-446655440000`)

**Göreceğiniz:**
```json
{
  "tenant_id": "550e8400-e29b-41d4-a716-446655440000",
  "metrics": {
    "api_requests_count": 45,
    "db_query_timing_avg": 12.5,
    "cache_hit_count": 120
  },
  "timestamp": "2024-01-20T10:30:00"
}
```

---

## 🔒 ADIM 8: Security Headers Testi

**Terminal'de Çalıştır:**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/health" | Select-Object -ExpandProperty Headers
```

**Göreceğiniz Header'lar:**
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
X-Request-ID: 550e8400-e29b-41d4-a716-446655440000
X-Response-Time-Ms: 12.34
```

**Kontrol:**
- [ ] Tüm security header'lar var mı?
- [ ] X-Request-ID her request'te farklı mı?
- [ ] X-Response-Time-Ms görünüyor mu?

---

## 🎨 ADIM 9: UI/UX Detay Kontrolü

### 9.1 8px Grid Sistemi

**Kontrol:**
- [ ] Kartlar arası boşluk: **24px** (eşit mi?)
- [ ] Kart içi padding: **24px** (eşit mi?)
- [ ] İkon-başlık arası: **16px** (eşit mi?)
- [ ] Her şey "matematiksel nizam"da mı?

### 9.2 Animasyonlar

**Kontrol:**
- [ ] Sayfa geçişleri smooth mu?
- [ ] Hover efektleri çalışıyor mu?
- [ ] Loading animasyonları var mı?
- [ ] Form animasyonları (shake, fade) çalışıyor mu?

### 9.3 Responsive Design

**Test:**
1. Tarayıcı penceresini küçültün (mobile boyut)
2. Büyütün (desktop boyut)
3. Farklı ekran boyutlarında test edin

**Kontrol:**
- [ ] Mobile'da düzgün görünüyor mu?
- [ ] Tablet'te düzgün görünüyor mu?
- [ ] Desktop'ta düzgün görünüyor mu?

---

## 🐛 ADIM 10: Hata Senaryoları Testi

### 10.1 Geçersiz Tenant ID

**Test:**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/tenants/me" -Headers @{"X-Tenant-ID"="invalid-uuid"}
```

**Göreceğiniz:**
```json
{
  "detail": "Invalid Tenant ID format"
}
```
**Status Code**: `403 Forbidden`

---

### 10.2 Olmayan Endpoint

**Test:**
```
http://localhost:8000/api/v1/nonexistent
```

**Göreceğiniz:**
```json
{
  "detail": "Not Found"
}
```
**Status Code**: `404 Not Found`

---

### 10.3 Database Bağlantı Hatası

**Test:**
1. PostgreSQL container'ını durdurun: `docker stop nextgent_db`
2. Health check yapın: `http://localhost:8000/api/v1/health`

**Göreceğiniz:**
```json
{
  "status": "degraded",
  "checks": {
    "database": {
      "status": "unhealthy",
      "message": "Database connection failed: ..."
    }
  }
}
```
**Status Code**: `503 Service Unavailable`

---

## 📸 ADIM 11: Görsel Ekran Görüntüleri Alın

**Alınacak Ekran Görüntüleri:**
1. ✅ Login sayfası
2. ✅ Dashboard (tam ekran)
3. ✅ Sektör switcher (açık menü)
4. ✅ API Documentation (Swagger)
5. ✅ Health check response
6. ✅ Metrics endpoint response
7. ✅ Security headers (browser dev tools)

---

## ✅ TEST CHECKLIST

### Frontend
- [ ] Login sayfası açılıyor
- [ ] Login işlemi çalışıyor
- [ ] Dashboard yükleniyor
- [ ] KPI kartları görünüyor
- [ ] Grafikler render ediliyor
- [ ] Sektör değiştirme çalışıyor
- [ ] Animasyonlar smooth
- [ ] Responsive design çalışıyor
- [ ] Brave fallback çalışıyor

### Backend
- [ ] Health check: `200 OK`
- [ ] Database: `healthy`
- [ ] Redis: `healthy`
- [ ] API docs açılıyor (`/docs`)
- [ ] Rate limiting çalışıyor
- [ ] Security headers var
- [ ] Request ID tracking çalışıyor
- [ ] Metrics endpoint çalışıyor

### Güvenlik
- [ ] Rate limiting aktif
- [ ] Security headers var
- [ ] CORS yapılandırması doğru
- [ ] Error messages güvenli (PII sızıntısı yok)

---

## 🎯 SONUÇ

**Başarı Kriterleri:**
- ✅ Tüm sayfalar yükleniyor
- ✅ Animasyonlar çalışıyor
- ✅ API'ler response veriyor
- ✅ Güvenlik özellikleri aktif
- ✅ Hata durumları düzgün handle ediliyor

**Sistem Durumu**: ✅ **Production'a Hazır**

---

## 🆘 SORUN GİDERME

### Frontend açılmıyor
- Docker loglarını kontrol edin: `docker-compose logs frontend`
- Port 80 kullanımda mı? Başka bir servis çalışıyor olabilir

### Backend hata veriyor
- Database bağlantısını kontrol edin: `docker-compose logs db`
- Redis bağlantısını kontrol edin: `docker-compose logs redis`
- Environment variable'ları kontrol edin

### Rate limiting çalışmıyor
- Redis çalışıyor mu? `docker-compose ps redis`
- Redis loglarını kontrol edin: `docker-compose logs redis`

---

**Test Süresi**: ~15-20 dakika  
**Sonuç**: Sistemin görsel ve fonksiyonel olarak mükemmel çalıştığını doğrulayacaksınız! 🎉


