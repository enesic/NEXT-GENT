# 📖 Müşteri Kullanım Rehberi - NextGent

**Versiyon**: 2.0.0  
**Tarih**: 2024

---

## 🎯 ANA ÖZELLİKLER

### 1. 🤖 Yapay Zeka Destekli Callcenter ve Helpdesk

#### Callcenter (Sesli Asistan)
**Nasıl Kullanılır:**

1. **Vapi.ai Entegrasyonu:**
   - Vapi.ai dashboard'unda telefon numaranızı ayarlayın
   - Webhook URL'i yapılandırın: `https://your-api.com/api/v1/webhooks/voice/vapi`
   - Header ekleyin: `X-Tenant-ID: your-tenant-id`

2. **Dashboard'da İzleme:**
   - Dashboard → "Call Center" menüsüne tıklayın
   - Aktif çağrıları gerçek zamanlı görüntüleyin
   - Call metrics (süre, sentiment) takip edin
   - Call history'yi inceleyin

3. **Otomatik Özellikler:**
   - Müşteri segmentine göre otomatik prompt özelleştirme
   - VIP müşteriler premium hizmet alır
   - Müşteri geçmişi otomatik olarak AI'ya aktarılır

**Kullanım Senaryosu:**
```
Müşteri → Telefonu açar → Vapi.ai → NextGent API'ye webhook gönderir
→ AI müşteri segmentini tespit eder → Özelleştirilmiş prompt döner
→ Vapi.ai müşteriyle konuşur → Dashboard'da görüntülenir
```

---

#### Helpdesk (Chatbot)
**Nasıl Kullanılır:**

1. **Ana Sayfada:**
   - Sağ alt köşedeki chat butonuna tıklayın
   - Mesajınızı yazın
   - AI otomatik olarak yanıt verir

2. **Otomatik İşlem Yapma:**
   - AI mesajınızı analiz eder
   - Intent'i tespit eder (randevu oluştur, iptal et, bilgi al)
   - Yüksek güvenle (>80%) otomatik işlem yapar
   - Sonucu size bildirir

**Örnek Kullanım:**
```
Kullanıcı: "Yarın saat 14:00'te randevu almak istiyorum"
AI: Intent tespit edildi → create_appointment() çağrıldı
AI: "Randevunuz 2026-01-24 tarihinde 14:00 saatinde oluşturuldu."
```

**Desteklenen İşlemler:**
- ✅ Randevu oluşturma
- ✅ Randevu iptal etme
- ✅ Müşteri bilgisi sorgulama
- ✅ Genel sorulara yanıt verme

---

### 2. 📊 Yapay Zeka Destekli Müşteri Memnuniyet Oranı ve Grafikleri

#### Memnuniyet Anketi Sistemi
**Nasıl Çalışır:**

1. **Otomatik Survey Gönderimi:**
   - Call sonrası otomatik survey gönderilir
   - Interaction sonrası survey gönderilir
   - Admin manuel olarak da gönderebilir

2. **Survey Tipleri:**
   - **NPS (Net Promoter Score)**: 0-10 puan
   - **CSAT (Customer Satisfaction)**: 1-5 yıldız
   - **Custom Rating**: Özel ölçek

3. **AI Sentiment Analysis:**
   - Feedback text'i otomatik analiz edilir
   - Sentiment tespit edilir (positive/neutral/negative)
   - Score hesaplanır (0.0 - 1.0)
   - AI summary oluşturulur

**Dashboard'da Görüntüleme:**

1. **Dashboard → "Memnuniyet" Menüsü:**
   - NPS Score görüntüleme
   - CSAT Average görüntüleme
   - Sentiment distribution (pie chart)
   - Satisfaction trends (line chart)

2. **Grafikler:**
   - **Trend Chart**: Zaman içinde memnuniyet değişimi
   - **Sentiment Pie Chart**: Positive/Neutral/Negative dağılımı
   - **Segment Bazlı**: Müşteri segmentine göre memnuniyet

**API Kullanımı:**
```bash
# Survey oluştur
POST /api/v1/satisfaction/
{
  "customer_id": "uuid",
  "interaction_id": "uuid",
  "survey_type": "csat"
}

# Yanıt gönder
POST /api/v1/satisfaction/{survey_id}/submit
{
  "csat_score": 5,
  "feedback_text": "Çok memnun kaldım!"
}

# Metrikleri görüntüle
GET /api/v1/satisfaction/metrics?days=30
```

---

### 3. 🧠 Yapay Zeka Destekli Otomatik Sorun Çözücü

#### Intent Detection ve Function Calling
**Nasıl Çalışır:**

1. **AI Intent Detection:**
   - Kullanıcı mesajını AI analiz eder
   - Intent tespit edilir (appointment_create, appointment_cancel, customer_info, vb.)
   - Confidence score hesaplanır (0.0 - 1.0)
   - Entity extraction (tarih, saat, müşteri bilgisi)

2. **Otomatik İşlem Yapma:**
   - Confidence > 80% ise otomatik işlem yapılır
   - AI system function'ları çağırır
   - İşlem sonucu kullanıcıya bildirilir

**Desteklenen Fonksiyonlar:**

| Fonksiyon | Açıklama | Örnek |
|-----------|----------|-------|
| `create_appointment` | Randevu oluştur | "Yarın saat 14:00'te randevu al" |
| `cancel_appointment` | Randevu iptal et | "Randevumu iptal et" |
| `get_customer_info` | Müşteri bilgisi | "Müşteri bilgilerimi göster" |
| `send_satisfaction_survey` | Memnuniyet anketi gönder | Otomatik |

**Kullanım Örnekleri:**

**Örnek 1: Randevu Oluşturma**
```
Kullanıcı: "24 Ocak saat 14:00'te randevu almak istiyorum"
AI: Intent detected: appointment_create (confidence: 0.95)
AI: Entities extracted: date=2026-01-24, time=14:00
AI: Function called: create_appointment()
AI: "Randevunuz 24 Ocak 2026 tarihinde saat 14:00'te oluşturuldu."
```

**Örnek 2: Müşteri Bilgisi**
```
Kullanıcı: "Telefon numaram +905551234567, bilgilerimi göster"
AI: Intent detected: customer_info (confidence: 0.90)
AI: Function called: get_customer_info(phone="+905551234567")
AI: "Müşteri bilgileriniz: Ahmet Yılmaz, Segment: VIP, Durum: Active"
```

**Örnek 3: Otomatik Memnuniyet Anketi**
```
Call tamamlandı → Sistem otomatik survey gönderir
Müşteri yanıt verir → AI sentiment analizi yapar
Dashboard'da görüntülenir
```

---

## 🎨 DASHBOARD KULLANIMI

### Ana Dashboard
1. **Login:** Email ve şifre girin (sektör otomatik tespit edilir)
2. **Dashboard:** Ana sayfada KPI'lar, grafikler ve insights görüntülenir
3. **Sektör Badge:** Üst sağda sektörünüz görünür

### Call Center Dashboard
1. **Menü:** Sol sidebar'dan "Call Center" seçin
2. **Aktif Çağrılar:** Gerçek zamanlı aktif çağrıları görüntüleyin
3. **Call History:** Son çağrıları ve sentiment analizlerini görün
4. **Metrics:** Toplam çağrı, ortalama süre, positive sentiment %

### Satisfaction Dashboard
1. **Menü:** Sol sidebar'dan "Memnuniyet" seçin
2. **Metrikler:** NPS, CSAT, Sentiment distribution
3. **Grafikler:** Trend chart ve sentiment pie chart
4. **Period Selector:** 7 gün, 30 gün, 90 gün, 1 yıl

---

## 🔧 KURULUM VE YAPILANDIRMA

### 1. OpenAI API Key
```bash
# .env dosyasına ekleyin
OPENAI_API_KEY=sk-...
```

### 2. Vapi.ai Entegrasyonu
1. Vapi.ai hesabı oluşturun
2. Webhook URL: `https://your-api.com/api/v1/webhooks/voice/vapi`
3. Header: `X-Tenant-ID: your-tenant-id`

### 3. Survey Otomatik Gönderimi
- Call/interaction sonrası otomatik çalışır
- Manuel göndermek için API kullanın

---

## 📈 METRİKLER VE RAPORLAR

### Callcenter Metrikleri
- **Active Calls**: Şu anda aktif çağrı sayısı
- **Total Calls**: Son 30 gündeki toplam çağrı
- **Average Duration**: Ortalama çağrı süresi
- **Positive Sentiment %**: Pozitif sentiment yüzdesi

### Satisfaction Metrikleri
- **NPS Score**: -100 ile +100 arası
- **CSAT Average**: 1-5 arası ortalama
- **Sentiment Distribution**: Positive/Neutral/Negative sayıları
- **Trends**: Zaman içinde değişim

---

## ✅ ÖZET

**Tüm Ana Özellikler Eklendi:**

1. ✅ **AI Callcenter & Helpdesk**
   - Vapi.ai entegrasyonu
   - Real-time monitoring dashboard
   - AI-powered responses

2. ✅ **AI Müşteri Memnuniyet Sistemi**
   - Satisfaction survey model
   - AI sentiment analysis
   - Dashboard ve grafikler

3. ✅ **AI Otomatik Sorun Çözücü**
   - Advanced intent detection
   - Function calling sistemi
   - Otomatik işlem yapma

**Sistem Production'a Hazır! 🚀**
