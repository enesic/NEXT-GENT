# 🧪 Manuel Test Rehberi - NextGent Randevu Sistemi

## 📋 Ön Hazırlık

### 1. Docker Servislerini Başlat

```bash
docker-compose up -d
```

**Beklenen Çıktı:**
```
✅ postgres container başlatıldı
✅ redis container başlatıldı
```

### 2. Veritabanını Hazırla

```bash
# Veritabanı tablolarını oluştur
python init_db.py
```

**Beklenen Çıktı:**
```
✅ Tüm tablolar oluşturuldu
```

### 3. Uygulamayı Başlat

```bash
uvicorn app.main:app --reload --port 8000
```

**Beklenen Çıktı:**
```
INFO: Uvicorn running on http://127.0.0.1:8000
INFO: Application startup complete
```

---

## 🏢 Test 1: Tenant (Şirket) Oluşturma

### API İsteği

```bash
curl -X POST "http://localhost:8000/api/v1/tenants/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Medipol Hastanesi",
    "slug": "medipol",
    "domain": "medipol.com.tr",
    "webhook_url": "https://webhook.site/unique-id-buraya"
  }'
```

### Beklenen Sonuç

```json
{
  "id": "abc-123-def-456",
  "name": "Medipol Hastanesi",
  "slug": "medipol",
  "is_active": true,
  "webhook_url": "https://webhook.site/unique-id-buraya"
}
```

**✅ Başarı Kriteri:** HTTP 200 ve tenant ID döndü

**📝 Not:** `id` değerini kaydet, sonraki testlerde kullanacaksın!

---

## 👤 Test 2: Müşteri Oluşturma

### API İsteği

```bash
curl -X POST "http://localhost:8000/api/v1/customers/" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: abc-123-def-456" \
  -d '{
    "first_name": "Ahmet",
    "last_name": "Yılmaz",
    "email": "ahmet@example.com",
    "phone": "+905551234567",
    "segment": "gold",
    "status": "active",
    "total_orders": 10,
    "total_spent": 5000.0
  }'
```

### Beklenen Sonuç

```json
{
  "id": "customer-id-123",
  "first_name": "Ahmet",
  "last_name": "Yılmaz",
  "phone": "+905551234567",
  "segment": "gold"
}
```

**✅ Başarı Kriteri:** HTTP 200 ve müşteri oluşturuldu

---

## 📅 Test 3: Randevu Oluşturma (İlk Randevu)

### API İsteği

```bash
curl -X POST "http://localhost:8000/api/v1/appointments/" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: abc-123-def-456" \
  -d '{
    "title": "Kardiyoloji Muayenesi",
    "description": "Rutin kontrol",
    "start_time": "2026-01-22T10:00:00",
    "end_time": "2026-01-22T10:30:00",
    "client_name": "Ahmet Yılmaz",
    "client_email": "ahmet@example.com",
    "client_phone": "+905551234567"
  }'
```

### Beklenen Sonuç

```json
{
  "id": "appointment-id-123",
  "title": "Kardiyoloji Muayenesi",
  "start_time": "2026-01-22T10:00:00",
  "status": "pending"
}
```

**✅ Başarı Kriteri:** HTTP 200 ve randevu oluşturuldu

**🔔 Webhook Kontrolü:** webhook.site'ta bildirim geldi mi?

---

## 🔒 Test 4: Çift Rezervasyon Önleme (Race Condition)

### Senaryo
Aynı saate 2 randevu oluşturmaya çalış.

### 1. İlk Randevu (Başarılı Olmalı)

```bash
curl -X POST "http://localhost:8000/api/v1/appointments/" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: abc-123-def-456" \
  -d '{
    "title": "İlk Randevu",
    "start_time": "2026-01-22T14:00:00",
    "end_time": "2026-01-22T14:30:00",
    "client_name": "Test User 1",
    "client_email": "test1@example.com"
  }'
```

**Beklenen:** ✅ HTTP 200

### 2. İkinci Randevu (Başarısız Olmalı)

```bash
curl -X POST "http://localhost:8000/api/v1/appointments/" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: abc-123-def-456" \
  -d '{
    "title": "İkinci Randevu",
    "start_time": "2026-01-22T14:00:00",
    "end_time": "2026-01-22T14:30:00",
    "client_name": "Test User 2",
    "client_email": "test2@example.com"
  }'
```

**Beklenen:** ❌ HTTP 409 Conflict

**Hata Mesajı:**
```json
{
  "detail": {
    "message": "Bu saat dilimi az önce doldu. Lütfen başka bir saat seçin.",
    "error_code": "TIME_SLOT_JUST_TAKEN"
  }
}
```

**✅ Başarı Kriteri:** İkinci randevu reddedildi, çift rezervasyon önlendi!

---

## ⚡ Test 5: Redis Cache Hızı (Antigravity Speed)

### 1. İlk Sorgu (Cache MISS - Yavaş)

```bash
curl "http://localhost:8000/api/v1/customers/by-phone/+905551234567" \
  -H "X-Tenant-ID: abc-123-def-456"
```

**Terminal Çıktısı:**
```
❌ CACHE MISS: +905551234567 | 45.2ms | Querying database...
```

### 2. İkinci Sorgu (Cache HIT - Hızlı!)

```bash
curl "http://localhost:8000/api/v1/customers/by-phone/+905551234567" \
  -H "X-Tenant-ID: abc-123-def-456"
```

**Terminal Çıktısı:**
```
⚡ CACHE HIT: +905551234567 | 8.5ms | Antigravity speed!
```

**✅ Başarı Kriteri:** İkinci sorgu < 20ms

---

## 🛡️ Test 6: Tenant İzolasyonu (Güvenlik)

### Senaryo
Farklı tenant'lar birbirinin verilerini görememeli.

### 1. İkinci Tenant Oluştur

```bash
curl -X POST "http://localhost:8000/api/v1/tenants/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acıbadem Hastanesi",
    "slug": "acibadem",
    "domain": "acibadem.com.tr"
  }'
```

**Tenant ID'yi kaydet:** `tenant-2-id`

### 2. Medipol'ün Randevularını Acıbadem ile Sorgula

```bash
curl "http://localhost:8000/api/v1/appointments/" \
  -H "X-Tenant-ID: tenant-2-id"
```

**Beklenen Sonuç:**
```json
{
  "appointments": []
}
```

**✅ Başarı Kriteri:** Acıbadem, Medipol'ün randevularını göremiyor!

---

## 🔄 Test 7: Webhook Retry Mekanizması

### Senaryo
Webhook URL çalışmıyorsa, sistem 3 kez tekrar denemeli.

### 1. Geçersiz Webhook URL'li Tenant Oluştur

```bash
curl -X POST "http://localhost:8000/api/v1/tenants/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Hastanesi",
    "slug": "test-hospital",
    "domain": "test.com",
    "webhook_url": "http://192.0.2.1:9999/webhook"
  }'
```

### 2. Randevu Oluştur

```bash
curl -X POST "http://localhost:8000/api/v1/appointments/" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: test-hospital-tenant-id" \
  -d '{
    "title": "Test Randevu",
    "start_time": "2026-01-22T16:00:00",
    "end_time": "2026-01-22T16:30:00",
    "client_name": "Test User",
    "client_email": "test@example.com"
  }'
```

**Terminal Çıktısı (Beklenen):**
```
⏱️  Webhook timeout (attempt 1/3)
🔄 Retrying in 1s...
⏱️  Webhook timeout (attempt 2/3)
🔄 Retrying in 2s...
⏱️  Webhook timeout (attempt 3/3)
❌ Webhook failed after 3 retries
💾 Failed webhook saved to database
```

**✅ Başarı Kriteri:** 
- 3 retry denemesi yapıldı
- Toplam süre ~7 saniye
- Failed webhook veritabanına kaydedildi

---

## 📊 Test 8: Randevu Güncelleme (Optimistic Locking)

### 1. Randevu Sorgula

```bash
curl "http://localhost:8000/api/v1/appointments/appointment-id-123" \
  -H "X-Tenant-ID: abc-123-def-456"
```

**Version değerini kaydet:** `"version": 1`

### 2. Randevu Güncelle

```bash
curl -X PUT "http://localhost:8000/api/v1/appointments/appointment-id-123" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: abc-123-def-456" \
  -d '{
    "status": "confirmed",
    "version": 1
  }'
```

**Beklenen:** ✅ HTTP 200

### 3. Eski Version ile Tekrar Güncelle (Başarısız Olmalı)

```bash
curl -X PUT "http://localhost:8000/api/v1/appointments/appointment-id-123" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: abc-123-def-456" \
  -d '{
    "status": "cancelled",
    "version": 1
  }'
```

**Beklenen:** ❌ HTTP 409 Conflict

**Hata Mesajı:**
```json
{
  "detail": "Appointment was modified by another user"
}
```

**✅ Başarı Kriteri:** Eski version ile güncelleme reddedildi!

---

## 🗑️ Test 9: Cache Invalidation (Önbellek Temizleme)

### 1. Müşteri Bilgisini Sorgula (Cache'e al)

```bash
curl "http://localhost:8000/api/v1/customers/by-phone/+905551234567" \
  -H "X-Tenant-ID: abc-123-def-456"
```

**Terminal:** `⚡ CACHE HIT: 8.5ms`

### 2. Müşteri Bilgisini Güncelle

```bash
curl -X PUT "http://localhost:8000/api/v1/customers/customer-id-123" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: abc-123-def-456" \
  -d '{
    "total_orders": 20,
    "total_spent": 10000.0
  }'
```

**Terminal:** `🗑️ Cache invalidated for +905551234567`

### 3. Tekrar Sorgula (Cache MISS olmalı)

```bash
curl "http://localhost:8000/api/v1/customers/by-phone/+905551234567" \
  -H "X-Tenant-ID: abc-123-def-456"
```

**Terminal:** `❌ CACHE MISS: 45.2ms`

**✅ Başarı Kriteri:** Cache güncelleme sonrası temizlendi, stale data yok!

---

## 📈 Test 10: Analytics API

### Günlük Randevu İstatistikleri

```bash
curl "http://localhost:8000/api/v1/analytics/dashboard-summary?start_date=2026-01-01&end_date=2026-01-31" \
  -H "X-Tenant-ID: abc-123-def-456"
```

**Beklenen Sonuç:**
```json
{
  "total_appointments": 10,
  "confirmed_appointments": 7,
  "cancelled_appointments": 2,
  "pending_appointments": 1,
  "total_revenue": 15000.0
}
```

**✅ Başarı Kriteri:** İstatistikler doğru hesaplandı

---

## ✅ Test Sonuçları Kontrol Listesi

| Test | Durum | Notlar |
|------|-------|--------|
| 1. Tenant Oluşturma | ⬜ | |
| 2. Müşteri Oluşturma | ⬜ | |
| 3. Randevu Oluşturma | ⬜ | |
| 4. Çift Rezervasyon Önleme | ⬜ | 409 Conflict dönmeli |
| 5. Redis Cache Hızı | ⬜ | < 20ms olmalı |
| 6. Tenant İzolasyonu | ⬜ | Veri sızıntısı yok |
| 7. Webhook Retry | ⬜ | 3 deneme yapmalı |
| 8. Optimistic Locking | ⬜ | Eski version reddedilmeli |
| 9. Cache Invalidation | ⬜ | Güncelleme sonrası temizlenmeli |
| 10. Analytics API | ⬜ | İstatistikler doğru |

---

## 🐛 Sorun Giderme

### Docker Çalışmıyor

```bash
# Docker servislerini yeniden başlat
docker-compose down
docker-compose up -d
```

### Veritabanı Bağlantı Hatası

```bash
# PostgreSQL container'ını kontrol et
docker ps
docker logs outer-granule-postgres-1
```

### Redis Bağlantı Hatası

```bash
# Redis container'ını kontrol et
docker logs outer-granule-redis-1
```

### Port Zaten Kullanımda

```bash
# 8000 portunu kullanan process'i bul
netstat -ano | findstr :8000

# Process'i kapat (Windows)
taskkill /PID <process-id> /F
```

---

## 📝 Notlar

- **Tenant ID:** Her istekte `X-Tenant-ID` header'ı zorunlu
- **Webhook Test:** webhook.site kullanarak gerçek webhook testi yapabilirsin
- **Zaman Formatı:** ISO 8601 format kullan: `2026-01-22T10:00:00`
- **Telefon Formatı:** Uluslararası format: `+905551234567`

---

## 🎉 Başarı Kriterleri

Tüm testler geçerse:
- ✅ Sistem production'a hazır
- ✅ Medipol ölçeğinde çalışabilir
- ✅ Güvenlik testlerini geçti
- ✅ Performans hedeflerine ulaştı

**İyi testler! 🚀**
