# Randevu Yönetim Sistemi - Dokümantasyon

## Genel Bakış

Görseldeki akış diyagramına göre tasarlanmış, asenkron randevu yönetim sistemi. Multi-tenant desteği ve concurrency kontrolü ile.

## Oluşturulan Dosyalar

### 1. Model: `app/models/appointment.py`
- **Appointment** modeli: Randevu veritabanı tablosu
- **AppointmentStatus** enum: pending, confirmed, cancelled, completed
- **Özellikler**:
  - Tenant izolasyonu (tenant_id)
  - Zaman aralığı (start_time, end_time)
  - Müşteri bilgileri (client_name, email, phone)
  - Google Calendar entegrasyonu için alan (google_calendar_event_id)
  - **Optimistic Locking**: `version` field ile concurrency kontrolü

### 2. Şemalar: `app/schemas/appointment.py`
- **AppointmentCreate**: Yeni randevu oluşturma
  - Validation: end_time > start_time kontrolü
- **AppointmentUpdate**: Randevu güncelleme
- **AppointmentResponse**: API yanıtı
- **AppointmentConflict**: Çakışma bilgisi

### 3. Servis: `app/services/appointment_service.py`

#### Ana Metodlar:

**`check_time_slot_availability()`**
- Zaman aralığında çakışma kontrolü
- Mevcut pending/confirmed randevuları kontrol eder
- 3 tip çakışma senaryosu:
  1. Yeni randevu mevcut randevunun içinde başlıyor
  2. Yeni randevu mevcut randevunun içinde bitiyor
  3. Yeni randevu mevcut randevuyu tamamen kapsıyor

**`create_appointment()`**
Akış:
1. ✅ Zaman aralığı müsaitlik kontrolü
2. ❌ Çakışma varsa → HTTP 409 Conflict + çakışan randevular
3. ✅ Veritabanına kaydet
4. 🔄 (Opsiyonel) Google Calendar senkronizasyonu

**`update_appointment()`**
- **Optimistic Locking** ile concurrency kontrolü
- Version numarası kontrolü
- Version mismatch → HTTP 409 Conflict
- Zaman değişiyorsa yeniden çakışma kontrolü

**`get_conflicting_appointments()`**
- Çakışan randevuların listesini döner
- Kullanıcıya hangi randevularla çakıştığını gösterir

**`cancel_appointment()`**
- Randevu iptali
- Status → CANCELLED

### 4. API Endpoints: `app/api/v1/endpoints/appointments.py`

#### Endpoint'ler:

**POST `/api/v1/appointments/`**
- Yeni randevu oluştur
- Otomatik çakışma kontrolü
- Header: `X-Tenant-ID` (zorunlu)

**GET `/api/v1/appointments/`**
- Randevuları listele
- Filtreler:
  - `start_date`: Başlangıç tarihi
  - `end_date`: Bitiş tarihi
  - `status`: Durum filtresi
  - `skip`, `limit`: Pagination

**GET `/api/v1/appointments/{appointment_id}`**
- Tek randevu detayı

**PUT `/api/v1/appointments/{appointment_id}?version={version}`**
- Randevu güncelle
- **Zorunlu**: `version` query parametresi (optimistic locking)
- Version uyuşmazlığı → 409 Conflict

**POST `/api/v1/appointments/{appointment_id}/cancel`**
- Randevu iptal et

**GET `/api/v1/appointments/check-availability/`**
- Zaman aralığı müsaitlik kontrolü
- Query params: `start_time`, `end_time`
- Response:
  ```json
  {
    "available": true/false,
    "conflicts": [...]
  }
  ```

## Concurrency Kontrolü

### Optimistic Locking Stratejisi:
1. Her randevunun bir `version` numarası var
2. Güncelleme yaparken client mevcut version'ı gönderir
3. Server version'ı kontrol eder:
   - ✅ Eşleşirse → Güncelle ve version++
   - ❌ Eşleşmezse → 409 Conflict (başkası güncellemiş)

### Çakışma Önleme:
- Database seviyesinde zaman aralığı kontrolü
- 3 farklı overlap senaryosu kontrol edilir
- Atomik transaction ile race condition önlenir

## Kullanım Örnekleri

### 1. Randevu Oluşturma
```bash
curl -X POST "http://localhost:8000/api/v1/appointments/" \
  -H "X-Tenant-ID: <tenant-uuid>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Müşteri Görüşmesi",
    "description": "Proje görüşmesi",
    "start_time": "2026-01-21T10:00:00",
    "end_time": "2026-01-21T11:00:00",
    "client_name": "Ahmet Yılmaz",
    "client_email": "ahmet@example.com",
    "client_phone": "+905551234567"
  }'
```

### 2. Müsaitlik Kontrolü
```bash
curl -X GET "http://localhost:8000/api/v1/appointments/check-availability/?start_time=2026-01-21T10:00:00&end_time=2026-01-21T11:00:00" \
  -H "X-Tenant-ID: <tenant-uuid>"
```

### 3. Randevu Güncelleme (Optimistic Locking)
```bash
curl -X PUT "http://localhost:8000/api/v1/appointments/<appointment-id>?version=1" \
  -H "X-Tenant-ID: <tenant-uuid>" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "confirmed"
  }'
```

## Veritabanı Migration

Alembic ile migration oluşturmak için:

```bash
# Migration oluştur
alembic revision --autogenerate -m "Add appointment model"

# Migration uygula
alembic upgrade head
```

## Google Calendar Entegrasyonu (Opsiyonel)

`AppointmentService.sync_to_google_calendar()` metodu placeholder olarak bırakıldı.

Entegrasyon için:
1. Google Calendar API credentials al
2. `google-api-python-client` kütüphanesini yükle
3. Metodu implement et
4. `google_calendar_event_id` field'ını kullan

## Hata Yönetimi

- **409 Conflict**: Zaman çakışması veya version mismatch
- **404 Not Found**: Randevu bulunamadı
- **400 Bad Request**: Geçersiz veri
- **403 Forbidden**: Geçersiz tenant

## Güvenlik

- ✅ Tenant izolasyonu (her sorgu tenant_id ile filtrelenir)
- ✅ Optimistic locking (concurrent update koruması)
- ✅ Input validation (Pydantic)
- ✅ SQL injection koruması (SQLAlchemy ORM)
