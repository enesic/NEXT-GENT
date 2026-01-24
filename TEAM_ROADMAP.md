# 🚀 NEXT-GENT: Pazar Günü MVP Lansman Planı (CRUNCH MODE)

> [!IMPORTANT]
> **HEDEF: PAZAR GÜNÜ LANSMAN (MVP)**
> Bu plan, Pazar günü yapılacak demo için **KRİTİK** olan maddeleri içerir. "Olsa güzel olur" özellikleri (Faze 2/3) bu hafta sonu kapsamı dışındadır.

---

## 🎯 MVP Hedefleri (Sunday Launch Goals)
Demo sırasında CEO şunları yapabilmeli:
1.  **Tek Komutla Başlatma**: `docker-compose up` dediğinde her şey çalışmalı.
2.  **Sinematik Giriş**: Login ekranı "WOW" efekti yaratmalı (Animasyonlu geçişler).
3.  **Dayanıklılık (Brave Fallback)**: Backend sunum sırasında çökse bile frontend **ASLA** beyaz erkan vermemeli, mock verilerle akmaya devam etmeli.
4.  **AI Show**: En az bir tane çalışan, etkileyici AI özelliği gösterilmeli (Örn: Sesli asistan veya Chatbot).

---

## 👥 Acil Durum Görev Dağılımı (3 Kişilik Ekip)

### 🧑‍💻 Kişi 1: Frontend & Visual Artist (GÖREV: "WOW" Etkisi)
**Odak**: `SUNDAY_LAUNCH_TEST.md` içindeki Senaryo 1 ve 3.

*   **[ACİL] Sinematik Login**:
    *   `Login.vue`: Giriş animasyonunu (Login -> Dashboard geçişi) pürüzsüz hale getir.
    *   Hatalı şifre girişinde "Shake" (titreme) efektinin çalıştığından emin ol.
*   **[ACİL] 8px Grid Polish**:
    *   Dashboard'daki `gap`, `padding` ve `margin` değerlerini `8px` katları (8, 16, 24, 32) olacak şekilde sabitle.
    *   Yazı tiplerini ve renkleri "Premium" hissettirecek şekilde gözden geçir.
*   **[ACİL] AI Chat UI**:
    *   Chat penceresini daha modern yap (Avatar, yazıyor animasyonu).

### 🧑‍🔬 Kişi 2: Backend & Fallback Architect (GÖREV: "Asla Çökme")
**Odak**: `SUNDAY_LAUNCH_TEST.md` içindeki Senaryo 2 ve AI Entegrasyonu.

*   **[KRİTİK] Brave Fallback İmplementasyonu**:
    *   Frontend'deki API çağrılarına (Axios interceptor) "Backend Yoksa Mock Dön" mantığını ekle.
    *   Backend kapalıyken bile Dashboard'un dolu görünmesini sağla.
*   **[ACİL] AI Endpoint Stabilizasyonu**:
    *   `ai_service.py` içinde demo sırasında hata verirse (OpenAI timeout vs.) hemen "Statik ama mantıklı" bir cevap dönen fallback mekanizmasını kur.
    *   **Demo Güvenliği**: Demo sırasında yapay zekanın saçmalamaması için `temperature=0` ayarlı, güvenli prompt'lar kullan.

### 👷 Kişi 3: DevOps & Environment (GÖREV: "Tek Tuş")
**Odak**: `SUNDAY_LAUNCH_TEST.md` içindeki Senaryo 4.

*   **[KRİTİK] Docker Compose Finalize**:
    *   Docker container içinde `nginx` ayarlarının React/Vue router (history mode) ile uyumlu olduğundan emin ol (Sayfa yenileyince 404 vermesin).
    *   Veritabanının `docker-compose up` sırasında otomatik olarak oluştuğunu (`init_db.py` gerekmeden veya otomatik çalışarak) doğrula.
*   **[ACİL] Demo Data Seeding**:
    *   Veritabanı boş gelmesin! `init_db.py` içine "Demo User", "Demo Appointments", "Demo Analytics Data" ekle. Sistem açıldığında dashboard dolu görünsün.

---

## ⏳ Cumartesi/Pazar Saatlik Plan (Countdown)

### Cumartesi (Hazırlık)
*   **12:00**: Herkes `develop` branchinden güncel hali çeker.
*   **14:00**: Kişi 3, Demo Verilerini (Seeding) hazırlar ve repoya atar.
*   **16:00**: Kişi 2, Backend'i kapatıp Frontend'in çökmediğini (Brave Fallback) test eder.
*   **18:00**: Kişi 1, Login animasyonunu ekibe demo yapar.

### Pazar (Lansman Günü)
*   **10:00**: **CODE FREEZE**. (Yeni özellik yasak, sadece bug fix).
*   **11:00**: "Dry Run". Sunum provası. Sistemi sıfırdan kurup senaryoları test edin.
*   **12:00**: Olası son dakika hataları için hotfix.
*   **13:00**: 🚀 **LAUNCH**.

---

## �️ Kurulum Kontrol Listesi (Lansman Öncesi)
Ekip lideri sunumdan önce şunları kontrol etmeli:
- [ ] `.env` dosyasında `OPENAI_API_KEY` var mı?
- [ ] Docker containerlar ayakta mı? (`docker ps`)
- [ ] Veritabanında demo verileri var mı?
- [ ] "Network" tabını açıp arka planda hata dönen (kırmızı) istek var mı?

---
**Unutmayın**: Pazar günkü hedefimiz *mükemmel kod* değil, **mükemmel görünen ve çalışan bir ürün**.
