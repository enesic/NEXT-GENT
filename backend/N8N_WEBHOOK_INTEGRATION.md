# n8n Webhook Entegrasyonu - Randevu Sistemi

## Genel Bakış

Randevu sistemi artık **webhook desteği** ile n8n, Zapier ve diğer automation platformlarıyla entegre çalışabilir.

## Webhook Olayları

Sistem aşağıdaki olaylar için webhook bildirimleri gönderir:

### 1. `appointment.created`
Yeni randevu oluşturulduğunda tetiklenir.

**Payload Örneği:**
```json
{
  "event": "appointment.created",
  "timestamp": "2026-01-21T03:00:00",
  "data": {
    "appointment_id": "uuid",
    "tenant_id": "uuid",
    "title": "Müşteri Görüşmesi",
    "description": "Proje görüşmesi",
    "start_time": "2026-01-22T10:00:00",
    "end_time": "2026-01-22T11:00:00",
    "client_name": "Ahmet Yılmaz",
    "client_email": "ahmet@example.com",
    "client_phone": "+905551234567",
    "status": "pending",
    "created_at": "2026-01-21T03:00:00",
    "updated_at": "2026-01-21T03:00:00"
  }
}
```

### 2. `appointment.updated`
Randevu güncellendiğinde tetiklenir.

**Payload Örneği:**
```json
{
  "event": "appointment.updated",
  "timestamp": "2026-01-21T03:15:00",
  "data": {
    "appointment_id": "uuid",
    "tenant_id": "uuid",
    "title": "Müşteri Görüşmesi",
    "status": "confirmed",
    "changes": {
      "status": "confirmed"
    },
    ...
  }
}
```

### 3. `appointment.cancelled`
Randevu iptal edildiğinde tetiklenir.

**Payload Örneği:**
```json
{
  "event": "appointment.cancelled",
  "timestamp": "2026-01-21T03:30:00",
  "data": {
    "appointment_id": "uuid",
    "tenant_id": "uuid",
    "status": "cancelled",
    ...
  }
}
```

### 4. `appointment.conflict`
Randevu oluşturma sırasında çakışma tespit edildiğinde tetiklenir.

**Payload Örneği:**
```json
{
  "event": "appointment.conflict",
  "timestamp": "2026-01-21T03:45:00",
  "data": {
    "requested_appointment": {
      "title": "Yeni Randevu",
      "start_time": "2026-01-22T10:30:00",
      "end_time": "2026-01-22T11:30:00",
      ...
    },
    "conflicts": [
      {
        "conflicting_appointment_id": "uuid",
        "start_time": "2026-01-22T10:00:00",
        "end_time": "2026-01-22T11:00:00",
        "title": "Mevcut Randevu"
      }
    ]
  }
}
```

## n8n Kurulumu

### Adım 1: n8n Workflow Oluşturma

1. n8n'de yeni bir workflow oluşturun
2. **Webhook** node'u ekleyin
3. Webhook URL'ini kopyalayın (örn: `https://your-n8n.com/webhook/randevu`)

### Adım 2: Tenant'a Webhook URL Ekleme

```bash
# Tenant oluştururken webhook URL ekleyin
curl -X POST "http://localhost:8000/api/v1/tenants/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Şirketi",
    "slug": "test-sirketi",
    "domain": "test.com",
    "webhook_url": "https://your-n8n.com/webhook/randevu"
  }'

# Veya mevcut tenant'ı güncelleyin
curl -X PUT "http://localhost:8000/api/v1/tenants/{tenant_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "webhook_url": "https://your-n8n.com/webhook/randevu"
  }'
```

### Adım 3: n8n Workflow Tasarlama

#### Örnek Workflow 1: Email Bildirimi

```
Webhook (Trigger)
  ↓
Switch (Event Type)
  ↓
├─ appointment.created → Send Email (Müşteriye onay maili)
├─ appointment.updated → Send Email (Güncelleme bildirimi)
├─ appointment.cancelled → Send Email (İptal bildirimi)
└─ appointment.conflict → Send Email (Admin'e uyarı)
```

**n8n Node Yapılandırması:**

1. **Webhook Node:**
   - HTTP Method: POST
   - Path: `/webhook/randevu`
   - Response Mode: "Respond Immediately"

2. **Switch Node:**
   - Mode: "Rules"
   - Rules:
     - `{{ $json.event }} === "appointment.created"`
     - `{{ $json.event }} === "appointment.updated"`
     - `{{ $json.event }} === "appointment.cancelled"`
     - `{{ $json.event }} === "appointment.conflict"`

3. **Send Email Node (appointment.created):**
   ```
   To: {{ $json.data.client_email }}
   Subject: Randevu Onayı
   Body:
   Sayın {{ $json.data.client_name }},
   
   Randevunuz oluşturuldu:
   Tarih: {{ $json.data.start_time }}
   Konu: {{ $json.data.title }}
   
   Teşekkürler!
   ```

#### Örnek Workflow 2: Google Calendar Senkronizasyonu

```
Webhook (Trigger)
  ↓
Switch (Event Type)
  ↓
├─ appointment.created → Google Calendar (Create Event)
├─ appointment.updated → Google Calendar (Update Event)
└─ appointment.cancelled → Google Calendar (Delete Event)
```

**Google Calendar Node Yapılandırması:**

1. **Create Event:**
   - Calendar: Primary
   - Start: `{{ $json.data.start_time }}`
   - End: `{{ $json.data.end_time }}`
   - Summary: `{{ $json.data.title }}`
   - Description: `{{ $json.data.description }}`
   - Attendees: `{{ $json.data.client_email }}`

#### Örnek Workflow 3: SMS Bildirimi (Twilio)

```
Webhook (Trigger)
  ↓
Filter (appointment.created veya appointment.updated)
  ↓
Twilio (Send SMS)
```

**Twilio Node:**
```
To: {{ $json.data.client_phone }}
Message: 
Randevunuz: {{ $json.data.title }}
Tarih: {{ $json.data.start_time }}
```

#### Örnek Workflow 4: Slack Bildirimi

```
Webhook (Trigger)
  ↓
Slack (Send Message)
```

**Slack Node:**
```
Channel: #randevular
Message:
🆕 Yeni Randevu: {{ $json.data.title }}
👤 Müşteri: {{ $json.data.client_name }}
📅 Tarih: {{ $json.data.start_time }}
```

## Test Etme

### 1. Webhook URL'ini Test Edin

```bash
# n8n webhook'unuzu manuel test edin
curl -X POST "https://your-n8n.com/webhook/randevu" \
  -H "Content-Type: application/json" \
  -d '{
    "event": "appointment.created",
    "timestamp": "2026-01-21T03:00:00",
    "data": {
      "appointment_id": "test-uuid",
      "title": "Test Randevu",
      "client_email": "test@example.com"
    }
  }'
```

### 2. Gerçek Randevu Oluşturun

```bash
# Webhook URL'li tenant ile randevu oluşturun
curl -X POST "http://localhost:8000/api/v1/appointments/" \
  -H "X-Tenant-ID: {tenant_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Randevu",
    "start_time": "2026-01-22T10:00:00",
    "end_time": "2026-01-22T11:00:00",
    "client_name": "Test User",
    "client_email": "test@example.com"
  }'
```

n8n workflow'unuzda webhook tetiklenmelidir!

## Gelişmiş Kullanım

### Conditional Logic (Koşullu Mantık)

n8n'de koşullu akışlar oluşturabilirsiniz:

```
Webhook
  ↓
IF Node (Status === "confirmed")
  ↓
├─ True → Send Confirmation Email
└─ False → Do Nothing
```

### Data Transformation

n8n'de veriyi dönüştürebilirsiniz:

```
Webhook
  ↓
Function Node
  ↓
Database (Save to external DB)
```

**Function Node Örneği:**
```javascript
// Tarihi formatla
const startTime = new Date($json.data.start_time);
const formattedDate = startTime.toLocaleDateString('tr-TR');
const formattedTime = startTime.toLocaleTimeString('tr-TR');

return {
  ...item,
  formatted_date: formattedDate,
  formatted_time: formattedTime
};
```

### Error Handling

n8n'de hata yönetimi:

```
Webhook
  ↓
Try/Catch
  ↓
├─ Success → Process normally
└─ Error → Send Error Notification to Admin
```

## Güvenlik

### Webhook Güvenliği

1. **HTTPS Kullanın:** Webhook URL'niz HTTPS olmalı
2. **Secret Token:** n8n'de webhook için secret token ekleyin
3. **IP Whitelist:** Sadece sunucunuzun IP'sinden gelen istekleri kabul edin

### Örnek: Secret Token Doğrulama

n8n'de Function Node ile:

```javascript
const secret = 'your-secret-token';
const receivedSecret = $json.headers['x-webhook-secret'];

if (receivedSecret !== secret) {
  throw new Error('Unauthorized');
}

return items;
```

## Sorun Giderme

### Webhook Çalışmıyor

1. **n8n Workflow Aktif mi?** Workflow'un aktif olduğundan emin olun
2. **URL Doğru mu?** Tenant'taki webhook_url'i kontrol edin
3. **n8n Erişilebilir mi?** n8n sunucunuzun internetten erişilebilir olduğundan emin olun
4. **Logları Kontrol Edin:** FastAPI loglarında webhook hatalarını kontrol edin

### Debug Modu

Webhook servisinde debug için:

```python
# app/services/webhook_service.py içinde
print(f"Sending webhook to: {webhook_url}")
print(f"Payload: {payload}")
```

## Örnek n8n Workflow JSON

Aşağıdaki JSON'u n8n'e import edebilirsiniz:

```json
{
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "randevu",
        "responseMode": "responseNode",
        "options": {}
      },
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [250, 300]
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{$json.event}}",
              "value2": "appointment.created"
            }
          ]
        }
      },
      "name": "IF Created",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [450, 300]
    },
    {
      "parameters": {
        "fromEmail": "noreply@example.com",
        "toEmail": "={{$json.data.client_email}}",
        "subject": "Randevu Onayı",
        "text": "=Sayın {{$json.data.client_name}},\n\nRandevunuz oluşturuldu:\nTarih: {{$json.data.start_time}}\nKonu: {{$json.data.title}}"
      },
      "name": "Send Email",
      "type": "n8n-nodes-base.emailSend",
      "typeVersion": 1,
      "position": [650, 300]
    }
  ],
  "connections": {
    "Webhook": {
      "main": [[{"node": "IF Created", "type": "main", "index": 0}]]
    },
    "IF Created": {
      "main": [[{"node": "Send Email", "type": "main", "index": 0}]]
    }
  }
}
```

## Sonuç

Webhook entegrasyonu ile randevu sisteminiz artık:
- ✅ Email bildirimleri gönderebilir
- ✅ SMS bildirimleri gönderebilir
- ✅ Google Calendar'a senkronize edebilir
- ✅ Slack/Teams'e bildirim gönderebilir
- ✅ Harici veritabanlarına kayıt yapabilir
- ✅ Custom logic çalıştırabilir

Tüm bunları **kod yazmadan** n8n ile yapabilirsiniz! 🚀
