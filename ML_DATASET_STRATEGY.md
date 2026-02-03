# 🤖 NextGent ML Chatbot - Dataset Stratejisi ve Uygulama Planı

## Genel Bakış

NextGent AI Chatbot için kapsamlı bir dataset oluşturma stratejisi. Hedef: Sektöre özel (Sağlık, Hukuk, Gayrimenkul), context-aware, Türkçe destekli bir chatbot.

---

## 📊 Dataset Gereksinimleri

### Minimum Gereksinimler
- **Toplam Soru-Cevap Çifti**: 1000+
- **Sektör Başına**: 300+ örnek
- **Dil**: Türkçe (öncelik), İngilizce (destek)
- **Format**: JSON, JSONL veya CSV

### Kalite Kriterleri
- ✅ Gerçekçi kullanıcı soruları
- ✅ Profesyonel ve doğru cevaplar
- ✅ Sektörel terminoloji
- ✅ Çeşitli soru tipleri (bilgi, yönlendirme, troubleshooting)
- ✅ Context-aware yanıtlar

---

## 🗂️ Dataset Kategorileri

### 1. Genel NextGent Bilgileri (200 örnek)

**Alt Kategoriler**:
- Ürün tanıtımı (50)
- Özellikler ve yetenekler (50)
- Fiyatlandırma (30)
- Teknik gereksinimler (30)
- Destek ve iletişim (40)

**Örnek**:
```json
{
  "category": "product_info",
  "sector": "general",
  "question": "NextGent nedir?",
  "answer": "NextGent, sağlık, hukuk ve gayrimenkul sektörlerine özel geliştirilmiş yapay zeka destekli operasyon yönetim platformudur. Randevu yönetimi, müşteri takibi, AI sesli asistan ve gerçek zamanlı analitik özellikleri sunar.",
  "intent": "product_overview",
  "keywords": ["nextgent", "platform", "yapay zeka", "operasyon yönetimi"]
}
```

### 2. Sağlık Sektörü (300 örnek)

**Alt Kategoriler**:
- Randevu yönetimi (80)
- Hasta takibi (60)
- Doktor özellikleri (40)
- Klinik operasyonları (60)
- KVKK ve güvenlik (30)
- Entegrasyonlar (e-Nabız) (30)

**Örnek**:
```json
{
  "category": "appointment",
  "sector": "medical",
  "question": "Randevu nasıl oluşturabilirim?",
  "answer": "Dashboard'da 'Randevular' menüsüne tıklayın, 'Yeni Randevu' butonuna basın. Hasta bilgilerini seçin, tarih ve saat belirleyin, randevu notlarını ekleyin ve kaydedin. Sistem otomatik olarak hastaya SMS/email bildirimi gönderecektir.",
  "intent": "how_to",
  "keywords": ["randevu", "oluşturma", "hasta", "bildirim"],
  "context": {
    "user_role": "doctor",
    "page": "appointments"
  }
}
```

### 3. Hukuk Sektörü (300 örnek)

**Alt Kategoriler**:
- Dava yönetimi (80)
- Müvekkil takibi (60)
- Duruşma takvimi (50)
- Belge yönetimi (60)
- Faturalandırma (30)
- UYAP entegrasyonu (20)

**Örnek**:
```json
{
  "category": "case_management",
  "sector": "legal",
  "question": "Yeni dava dosyası nasıl açarım?",
  "answer": "Ana menüden 'Dosyalar' bölümüne gidin, 'Yeni Dosya' butonuna tıklayın. Müvekkil bilgilerini seçin, dava türünü belirleyin, mahkeme ve dosya numarasını girin. İlgili belgeleri yükleyebilir ve duruşma tarihlerini ekleyebilirsiniz.",
  "intent": "how_to",
  "keywords": ["dava", "dosya", "müvekkil", "mahkeme"]
}
```

### 4. Gayrimenkul Sektörü (300 örnek)

**Alt Kategoriler**:
- Portföy yönetimi (80)
- Müşteri talepleri (70)
- İlan yönetimi (50)
- Görüşme takibi (50)
- Satış/Kiralama süreçleri (50)

**Örnek**:
```json
{
  "category": "portfolio",
  "sector": "real_estate",
  "question": "Yeni portföy nasıl eklerim?",
  "answer": "Dashboard'da 'Portföy' menüsüne tıklayın, 'Yeni İlan' butonuna basın. Gayrimenkul tipini seçin (satılık/kiralık), konum, fiyat, metrekare gibi detayları girin. Fotoğrafları yükleyin ve ilan açıklamasını yazın. Kaydettiğinizde otomatik olarak web sitenizde yayınlanacaktır.",
  "intent": "how_to",
  "keywords": ["portföy", "ilan", "gayrimenkul", "satılık", "kiralık"]
}
```

### 5. Teknik Destek ve Troubleshooting (200 örnek)

**Alt Kategoriler**:
- Login sorunları (40)
- Performans sorunları (30)
- Bildirim ayarları (30)
- Veri export/import (30)
- Entegrasyon sorunları (40)
- Mobil uygulama (30)

**Örnek**:
```json
{
  "category": "troubleshooting",
  "sector": "general",
  "question": "Giriş yapamıyorum, ne yapmalıyım?",
  "answer": "Öncelikle kullanıcı ID ve PIN kodunuzu kontrol edin. Caps Lock kapalı olmalı. Sorun devam ederse 'Şifremi Unuttum' linkine tıklayarak PIN kodunuzu sıfırlayabilirsiniz. Hala giriş yapamıyorsanız support@nextgent.com adresinden bizimle iletişime geçin.",
  "intent": "troubleshooting",
  "keywords": ["giriş", "login", "şifre", "pin"]
}
```

---

## 🛠️ Dataset Oluşturma Yöntemleri

### Yöntem 1: Manuel Oluşturma (Önerilen - Yüksek Kalite)

**Görev Dağılımı**:
- **Lider**: Genel bilgiler, teknik destek (200 örnek)
- **Doğukan**: Sağlık sektörü (300 örnek)
- **Musa**: Hukuk + Gayrimenkul (600 örnek toplam)

**Süreç**:
1. Template JSON dosyası kullan
2. Gerçek kullanıcı senaryolarını düşün
3. Profesyonel dil kullan
4. Çeşitli soru formları dene (nasıl, neden, ne zaman, vb.)
5. Quality check yap

**Timeline**: 2 hafta (günde 50-70 örnek)

### Yöntem 2: AI-Assisted Generation (Hızlı - Orta Kalite)

**Araçlar**: ChatGPT, Claude, GPT-4

**Prompt Örneği**:
```
Sen NextGent platformu için dataset oluşturan bir AI asistanısın. 
Sağlık sektörü için randevu yönetimi hakkında 20 soru-cevap çifti oluştur.
Format: JSON
Dil: Türkçe
Ton: Profesyonel, yardımsever
```

**Avantajlar**: Hızlı, çeşitli
**Dezavantajlar**: Manuel review gerekli, bazen generic cevaplar

### Yöntem 3: Web Scraping (Tamamlayıcı)

**Kaynaklar**:
- Rakip ürünlerin FAQ sayfaları
- Sektörel forumlar
- Stack Overflow (teknik sorular için)

**Dikkat**: Telif hakkı, veri gizliliği

### Yöntem 4: Gerçek Kullanıcı Verisi (Gelecek)

Production'a geçtikten sonra:
- Gerçek chatbot konuşmalarını logla
- User feedback topla
- Başarısız yanıtları tespit et
- Dataset'i sürekli iyileştir

---

## 📁 Dataset Format ve Yapısı

### Önerilen Format: JSONL (JSON Lines)

**Avantajlar**:
- Streaming-friendly
- Kolay append
- Büyük dosyalar için uygun

**Örnek Dosya Yapısı**:
```
ml-service/datasets/
├── raw/
│   ├── general_qa.jsonl
│   ├── medical_qa.jsonl
│   ├── legal_qa.jsonl
│   └── real_estate_qa.jsonl
├── processed/
│   ├── train.jsonl (80%)
│   ├── validation.jsonl (10%)
│   └── test.jsonl (10%)
└── metadata.json
```

### JSON Schema

```json
{
  "id": "unique_id_001",
  "category": "appointment|case_management|portfolio|troubleshooting|product_info",
  "sector": "general|medical|legal|real_estate",
  "question": "Kullanıcı sorusu",
  "answer": "Chatbot cevabı",
  "intent": "how_to|what_is|troubleshooting|pricing|feature_request",
  "keywords": ["keyword1", "keyword2"],
  "context": {
    "user_role": "doctor|lawyer|agent|admin",
    "page": "dashboard|appointments|cases|portfolio",
    "required_data": ["customer_id", "appointment_id"]
  },
  "metadata": {
    "created_by": "dogukan",
    "created_at": "2026-01-28",
    "reviewed": true,
    "quality_score": 4.5
  }
}
```

---

## 🧠 ML Model Stratejisi

### Seçenek 1: OpenAI Fine-Tuning (Önerilen - Kolay)

**Model**: GPT-3.5-turbo veya GPT-4
**Maliyet**: ~$0.008/1K tokens (training), ~$0.012/1K tokens (usage)

**Avantajlar**:
- Kolay implementasyon
- Yüksek kalite
- Türkçe desteği mükemmel
- Bakım gerektirmiyor

**Dezavantajlar**:
- Aylık maliyet (~$100-300)
- External dependency
- Veri OpenAI'a gidiyor (KVKK riski)

**Uygulama**:
```python
import openai

# Dataset hazırla (JSONL format)
# Her satır: {"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}

# Fine-tuning başlat
openai.FineTuningJob.create(
    training_file="file-abc123",
    model="gpt-3.5-turbo"
)

# Inference
response = openai.ChatCompletion.create(
    model="ft:gpt-3.5-turbo:nextgent:...",
    messages=[{"role": "user", "content": "NextGent nedir?"}]
)
```

### Seçenek 2: RAG (Retrieval-Augmented Generation) (Önerilen - Esnek)

**Yaklaşım**: Vector database + LLM

**Bileşenler**:
1. **Embedding Model**: sentence-transformers (multilingual)
2. **Vector DB**: Pinecone, Weaviate, veya ChromaDB
3. **LLM**: OpenAI GPT-4 veya local model

**Avantajlar**:
- Dataset güncellemesi kolay
- Kaynak gösterebilir (transparency)
- Maliyet düşük (sadece embedding + inference)
- KVKK uyumlu (veriler kendi sunucumuzda)

**Dezavantajlar**:
- Biraz daha kompleks
- Vector DB kurulumu gerekli

**Uygulama**:
```python
from sentence_transformers import SentenceTransformer
import chromadb

# Embedding model
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

# Vector DB
client = chromadb.Client()
collection = client.create_collection("nextgent_qa")

# Dataset'i embed et ve kaydet
for qa in dataset:
    embedding = model.encode(qa['question'])
    collection.add(
        embeddings=[embedding],
        documents=[qa['answer']],
        metadatas=[{"category": qa['category']}],
        ids=[qa['id']]
    )

# Query
def answer_question(question):
    query_embedding = model.encode(question)
    results = collection.query(query_embeddings=[query_embedding], n_results=3)
    
    # En iyi 3 sonucu GPT'ye context olarak ver
    context = "\n".join(results['documents'][0])
    prompt = f"Context: {context}\n\nSoru: {question}\n\nCevap:"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

### Seçenek 3: Self-Hosted Model (İleri Seviye - Tam Kontrol)

**Model**: Llama 2, Mistral, veya Türkçe fine-tuned BERT

**Avantajlar**:
- Tam kontrol
- Sıfır external dependency
- KVKK tam uyumlu
- Uzun vadede maliyet düşük

**Dezavantajlar**:
- GPU gerekli (NVIDIA A100 veya benzeri)
- Kompleks setup
- Bakım gerektirir
- Türkçe kalitesi düşük olabilir

**Önerim**: İlk aşamada kullanma, production'da büyük ölçeğe ulaşınca düşün.

---

## 🎯 Önerilen Strateji (Hibrit Yaklaşım)

### Faz 1: MVP (Hafta 1-4)
- **Dataset**: Manuel + AI-assisted (500 örnek)
- **Model**: OpenAI GPT-3.5-turbo (fine-tuning yok, direkt API)
- **Maliyet**: ~$50/ay
- **Hedef**: Temel soruları cevaplayabilen chatbot

### Faz 2: Beta (Hafta 5-7)
- **Dataset**: 1000+ örnek (manuel review edilmiş)
- **Model**: RAG (ChromaDB + OpenAI GPT-4)
- **Maliyet**: ~$150/ay
- **Hedef**: Context-aware, kaynak gösterebilen chatbot

### Faz 3: Production (Hafta 8-10)
- **Dataset**: 1500+ örnek + gerçek kullanıcı verileri
- **Model**: RAG + Fine-tuned GPT-3.5-turbo
- **Maliyet**: ~$300/ay
- **Hedef**: %85+ accuracy, <2s response time

### Faz 4: Scale (3+ ay sonra)
- **Dataset**: 3000+ örnek (sürekli güncellenen)
- **Model**: Self-hosted Llama 2 (opsiyonel)
- **Maliyet**: GPU sunucu (~$500/ay) veya OpenAI (~$500/ay)
- **Hedef**: %90+ accuracy, multi-language, voice support

---

## 📋 Aksiyon Planı

### Hafta 1-2: Dataset Oluşturma Kickoff

**Lider (İceneşik)**:
- [ ] Dataset template JSON oluştur
- [ ] Quality guidelines yaz
- [ ] Genel bilgiler kategorisi (200 örnek)
- [ ] Review process kur

**Doğukan**:
- [ ] Sağlık sektörü research yap
- [ ] Sağlık kategorisi (300 örnek)
- [ ] Frontend'de dataset upload arayüzü

**Musa**:
- [ ] Hukuk sektörü research yap
- [ ] Hukuk kategorisi (300 örnek)
- [ ] Gayrimenkul kategorisi (300 örnek)
- [ ] Dataset validation script

### Hafta 3-4: Dataset Review ve ML Setup

**Tüm Ekip**:
- [ ] Cross-review (herkes birbirinin dataset'ini review eder)
- [ ] Quality score ver (1-5)
- [ ] Düşük kaliteli örnekleri düzelt

**Lider**:
- [ ] ML servis mimarisi kur
- [ ] OpenAI API entegrasyonu
- [ ] RAG prototype (ChromaDB)

**Musa**:
- [ ] Dataset processing pipeline
- [ ] Train/validation/test split
- [ ] ML servis API endpoints

### Hafta 5-7: Model Training ve Testing

**Lider + Musa**:
- [ ] Model training (RAG veya fine-tuning)
- [ ] Inference API test
- [ ] Performance benchmarking
- [ ] A/B testing (farklı modeller)

**Doğukan**:
- [ ] Chatbot frontend entegrasyonu
- [ ] User feedback sistemi
- [ ] Analytics dashboard

---

## 🔍 Kalite Kontrol

### Dataset Quality Metrics

- **Completeness**: Tüm alanlar dolu mu?
- **Accuracy**: Cevaplar doğru mu?
- **Relevance**: Soru-cevap uyumlu mu?
- **Diversity**: Çeşitli soru tipleri var mı?
- **Language**: Türkçe doğal ve akıcı mı?

### Review Checklist

- [ ] Yazım hataları yok
- [ ] Profesyonel dil kullanılmış
- [ ] Sektörel terminoloji doğru
- [ ] Cevap actionable (uygulanabilir)
- [ ] Context bilgileri eksiksiz
- [ ] Keywords anlamlı

### Automated Validation

```python
def validate_qa_pair(qa):
    errors = []
    
    # Required fields
    required = ['question', 'answer', 'category', 'sector']
    for field in required:
        if field not in qa or not qa[field]:
            errors.append(f"Missing {field}")
    
    # Length checks
    if len(qa.get('question', '')) < 10:
        errors.append("Question too short")
    if len(qa.get('answer', '')) < 20:
        errors.append("Answer too short")
    
    # Language check (basic)
    if not any(char in 'çğıöşüÇĞİÖŞÜ' for char in qa.get('answer', '')):
        errors.append("Answer might not be in Turkish")
    
    return errors
```

---

## 💡 Best Practices

1. **Gerçek Senaryolar**: Gerçek kullanıcıların sorabileceği soruları düşün
2. **Çeşitlilik**: Aynı soruyu farklı şekillerde sor
3. **Kısa ve Net**: Cevaplar 2-3 cümle olmalı (çok uzun değil)
4. **Actionable**: Kullanıcıya ne yapması gerektiğini söyle
5. **Empati**: Kullanıcının duygusunu anla (frustrated, confused, curious)
6. **Tutarlılık**: Aynı terminolojiyi kullan
7. **Update**: Dataset'i sürekli güncelle

---

## 📊 Başarı Metrikleri

- **Coverage**: Dataset kaç farklı intent'i kapsıyor? (Hedef: 50+)
- **Accuracy**: Model test set'inde kaç doğru cevap veriyor? (Hedef: %85+)
- **Response Time**: Ortalama yanıt süresi (Hedef: <2s)
- **User Satisfaction**: Kullanıcı feedback skoru (Hedef: 4/5+)
- **Deflection Rate**: Chatbot kaç soruyu insan desteğe yönlendirmeden çözüyor? (Hedef: %70+)

---

**Hadi başlayalım! 🚀**
