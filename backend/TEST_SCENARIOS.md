# Test Senaryoları - Randevu Sistemi

Bu dosya, randevu sistemini test etmek için örnek senaryolar içerir.

## Ön Hazırlık

1. PostgreSQL ve Redis'in çalıştığından emin olun
2. `.env` dosyasını oluşturun (`.env.example`'dan kopyalayın)
3. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

4. Veritabanı migration'ları çalıştırın:
```bash
alembic revision --autogenerate -m "Initial migration with tenant and appointment"
alembic upgrade head
```

5. Sunucuyu başlatın:
```bash
uvicorn app.main:app --reload
```

## Test Senaryoları

### Senaryo 1: Tenant ve İlk Randevu Oluşturma

```bash
# 1. Tenant oluştur
TENANT_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/tenants/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Şirketi",
    "slug": "test-sirketi",
    "domain": "test.com"
  }')

echo $TENANT_RESPONSE

# Tenant ID'yi al (jq kullanarak)
TENANT_ID=$(echo $TENANT_RESPONSE | jq -r '.id')
echo "Tenant ID: $TENANT_ID"

# 2. İlk randevuyu oluştur
curl -X POST "http://localhost:8000/api/v1/appointments/" \
  -H "X-Tenant-ID: $TENANT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Müşteri Görüşmesi",
    "description": "Yeni proje görüşmesi",
    "start_time": "2026-01-22T10:00:00",
    "end_time": "2026-01-22T11:00:00",
    "client_name": "Ahmet Yılmaz",
    "client_email": "ahmet@example.com",
    "client_phone": "+905551234567"
  }'
```

### Senaryo 2: Çakışma Testi

```bash
# Aynı zaman aralığında ikinci randevu oluşturmayı dene (BAŞARISIZ olmalı)
curl -X POST "http://localhost:8000/api/v1/appointments/" \
  -H "X-Tenant-ID: $TENANT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Başka Görüşme",
    "description": "Bu çakışmalı",
    "start_time": "2026-01-22T10:30:00",
    "end_time": "2026-01-22T11:30:00",
    "client_name": "Mehmet Demir",
    "client_email": "mehmet@example.com"
  }'

# Beklenen yanıt: 409 Conflict
# {
#   "detail": {
#     "message": "Time slot is not available",
#     "conflicts": [...]
#   }
# }
```

### Senaryo 3: Müsaitlik Kontrolü

```bash
# Çakışan zaman aralığını kontrol et
curl -X GET "http://localhost:8000/api/v1/appointments/check-availability/?start_time=2026-01-22T10:30:00&end_time=2026-01-22T11:30:00" \
  -H "X-Tenant-ID: $TENANT_ID"

# Beklenen yanıt:
# {
#   "available": false,
#   "conflicts": [
#     {
#       "conflicting_appointment_id": "...",
#       "start_time": "2026-01-22T10:00:00",
#       "end_time": "2026-01-22T11:00:00",
#       "title": "Müşteri Görüşmesi"
#     }
#   ]
# }

# Müsait zaman aralığını kontrol et
curl -X GET "http://localhost:8000/api/v1/appointments/check-availability/?start_time=2026-01-22T14:00:00&end_time=2026-01-22T15:00:00" \
  -H "X-Tenant-ID: $TENANT_ID"

# Beklenen yanıt:
# {
#   "available": true,
#   "conflicts": []
# }
```

### Senaryo 4: Randevu Listeleme

```bash
# Tüm randevuları listele
curl -X GET "http://localhost:8000/api/v1/appointments/" \
  -H "X-Tenant-ID: $TENANT_ID"

# Tarih filtreli listeleme
curl -X GET "http://localhost:8000/api/v1/appointments/?start_date=2026-01-22T00:00:00&end_date=2026-01-23T00:00:00" \
  -H "X-Tenant-ID: $TENANT_ID"

# Status filtreli listeleme
curl -X GET "http://localhost:8000/api/v1/appointments/?status=pending" \
  -H "X-Tenant-ID: $TENANT_ID"
```

### Senaryo 5: Optimistic Locking Testi

```bash
# 1. Randevu detayını al
APPOINTMENT_RESPONSE=$(curl -s -X GET "http://localhost:8000/api/v1/appointments/" \
  -H "X-Tenant-ID: $TENANT_ID")

# İlk randevunun ID ve version'ını al
APPOINTMENT_ID=$(echo $APPOINTMENT_RESPONSE | jq -r '.[0].id')
VERSION=$(echo $APPOINTMENT_RESPONSE | jq -r '.[0].version')

echo "Appointment ID: $APPOINTMENT_ID"
echo "Current Version: $VERSION"

# 2. Randevuyu güncelle (doğru version ile)
curl -X PUT "http://localhost:8000/api/v1/appointments/$APPOINTMENT_ID?version=$VERSION" \
  -H "X-Tenant-ID: $TENANT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "confirmed"
  }'

# Başarılı olmalı, version artmış olmalı (version: 2)

# 3. Eski version ile güncellemeyi dene (BAŞARISIZ olmalı)
curl -X PUT "http://localhost:8000/api/v1/appointments/$APPOINTMENT_ID?version=$VERSION" \
  -H "X-Tenant-ID: $TENANT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Güncellenmiş açıklama"
  }'

# Beklenen yanıt: 409 Conflict
# {
#   "detail": "Appointment was modified by another user. Please refresh and try again."
# }
```

### Senaryo 6: Randevu Güncelleme ile Çakışma Testi

```bash
# 1. İkinci bir randevu oluştur
SECOND_APPOINTMENT=$(curl -s -X POST "http://localhost:8000/api/v1/appointments/" \
  -H "X-Tenant-ID: $TENANT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Öğleden Sonra Toplantısı",
    "start_time": "2026-01-22T14:00:00",
    "end_time": "2026-01-22T15:00:00",
    "client_name": "Ayşe Kaya",
    "client_email": "ayse@example.com"
  }')

SECOND_ID=$(echo $SECOND_APPOINTMENT | jq -r '.id')
SECOND_VERSION=$(echo $SECOND_APPOINTMENT | jq -r '.version')

# 2. İkinci randevunun saatini ilk randevuyla çakışacak şekilde değiştirmeyi dene
curl -X PUT "http://localhost:8000/api/v1/appointments/$SECOND_ID?version=$SECOND_VERSION" \
  -H "X-Tenant-ID: $TENANT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "start_time": "2026-01-22T10:30:00",
    "end_time": "2026-01-22T11:30:00"
  }'

# Beklenen yanıt: 409 Conflict (zaman çakışması)
```

### Senaryo 7: Randevu İptali

```bash
# Randevuyu iptal et
curl -X POST "http://localhost:8000/api/v1/appointments/$APPOINTMENT_ID/cancel" \
  -H "X-Tenant-ID: $TENANT_ID"

# Başarılı olmalı, status: "cancelled" olmalı

# İptal edilmiş randevuyu tekrar iptal etmeyi dene
curl -X POST "http://localhost:8000/api/v1/appointments/$APPOINTMENT_ID/cancel" \
  -H "X-Tenant-ID: $TENANT_ID"

# Beklenen yanıt: 400 Bad Request
# {
#   "detail": "Appointment is already cancelled"
# }
```

### Senaryo 8: Multi-Tenant İzolasyon Testi

```bash
# 1. İkinci bir tenant oluştur
TENANT2_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/tenants/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "İkinci Şirket",
    "slug": "ikinci-sirket",
    "domain": "ikinci.com"
  }')

TENANT2_ID=$(echo $TENANT2_RESPONSE | jq -r '.id')

# 2. İkinci tenant'ın randevularını listele (boş olmalı)
curl -X GET "http://localhost:8000/api/v1/appointments/" \
  -H "X-Tenant-ID: $TENANT2_ID"

# Beklenen yanıt: [] (boş array)

# 3. İkinci tenant ile ilk tenant'ın randevusuna erişmeyi dene
curl -X GET "http://localhost:8000/api/v1/appointments/$APPOINTMENT_ID" \
  -H "X-Tenant-ID: $TENANT2_ID"

# Beklenen yanıt: 404 Not Found (tenant izolasyonu çalışıyor)
```

## Swagger UI ile Test

Tarayıcıda `http://localhost:8000/docs` adresine giderek Swagger UI üzerinden de test edebilirsiniz.

1. Önce bir tenant oluşturun
2. Tenant ID'yi kopyalayın
3. Her endpoint için "X-Tenant-ID" header'ını ekleyin
4. Endpoint'leri test edin

## Python ile Test

```python
import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api/v1"

# Tenant oluştur
tenant_response = requests.post(
    f"{BASE_URL}/tenants/",
    json={
        "name": "Test Şirketi",
        "slug": "test-sirketi",
        "domain": "test.com"
    }
)
tenant_id = tenant_response.json()["id"]
headers = {"X-Tenant-ID": tenant_id}

# Randevu oluştur
appointment_data = {
    "title": "Müşteri Görüşmesi",
    "description": "Test randevusu",
    "start_time": (datetime.now() + timedelta(days=1)).isoformat(),
    "end_time": (datetime.now() + timedelta(days=1, hours=1)).isoformat(),
    "client_name": "Test Kullanıcı",
    "client_email": "test@example.com"
}

response = requests.post(
    f"{BASE_URL}/appointments/",
    headers=headers,
    json=appointment_data
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

## Beklenen Sonuçlar

✅ **Başarılı Senaryolar:**
- Müsait zaman aralığında randevu oluşturma
- Randevu listeleme ve filtreleme
- Doğru version ile güncelleme
- Randevu iptali
- Tenant izolasyonu

❌ **Başarısız Olması Gereken Senaryolar:**
- Çakışan zaman aralığında randevu oluşturma → 409 Conflict
- Yanlış version ile güncelleme → 409 Conflict
- Başka tenant'ın randevusuna erişim → 404 Not Found
- İptal edilmiş randevuyu tekrar iptal etme → 400 Bad Request
