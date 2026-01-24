# 🚀 Sunday Launch - Manual Test Protocol

Lead Architect olarak sistemi "Pazar Lansmanı" için onaylamanız adına aşağıdaki test senaryolarını hazırladım.

Bu adımları sırasıyla uygulayarak sistemin **Sinematik**, **Dayanıklı** ve **Piksel Mükemmel** olduğunu doğrulayabilirsiniz.

---

## ⚡ Başlangıç Rehberi (Startup Commands)

Sistemi ayağa kaldırmak için aşağıdaki iki yöntemden birini seçebilirsiniz.

### Seçenek 1: Docker ile (Önerilen - One Command)
Tüm sistemi (Backend, Frontend, Database) tek komutla, izole bir şekilde başlatır. Pazar günü sunumda bunu kullanacağız.

```powershell
# Proje ana dizininde (NEXT-GENT klasörü) terminal açın ve şu komutu yapıştırın:
docker-compose up --build
```
*Durdurmak için:* `CTRL+C`

### Seçenek 2: Manuel Geliştirme Modu (Development)
Docker kullanmıyorsanız parçaları ayrı ayrı başlatabilirsiniz. İki ayrı terminal açmanız gerekir.

**Terminal 1: Backend**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python init_db.py  # Veritabanını hazırlamak için (sadece ilk seferde)
uvicorn app.main:app --reload
```

**Terminal 2: Frontend**
```powershell
cd frontend
npm install
npm run dev
```

---

## 🎭 Senaryo 1: Sinematik Giriş Deneyimi (The "Wow" Factor)
**Amaç:** Giriş ekranının "büyüleyici" geçişini doğrulamak.

1.  Tarayıcıda uygulamayı açın (Development modunda `localhost:3000` veya Docker ile `localhost:80`).
2.  Giriş ekranı yüklendiğinde arka plandaki "Orb" animasyonlarının süzüldüğünü görün.
3.  Formu doldurun (İsterseniz yanlış şifre girip "Shake" efektini test edin).
4.  Doğru şifre ile **Sign In** butonuna basın.
5.  **GÖZLEM:**
    *   Form kartı **küçülerek kaybolmalı** (Fade-out & Scale-down).
    *   Ekranda yeşil bir **"Authentication Verified"** loader'ı belirmeli.
    *   Loader tamamlanınca Dashboard yumuşak bir şekilde ekrana gelmeli.

---

## 🛡️ Senaryo 2: Brave Fallback (Çökmezlik Testi)
**Amaç:** Backend çökse bile demonun devam edebildiğini kanıtlamak.

1.  Dashboard açıkken ve veriler (Grafikler, KPI'lar) görünüyorken terminali açın.
2.  Backend servisini "öldürün" (CTRL+C veya Docker kullanıyorsanız `docker stop nextgent_backend`).
3.  Tarayıcıya dönüp sayfayı **YENİLEYİN** (F5).
4.  **KRİTİK GÖZLEM:**
    *   Sayfa **BEYAZA DÜŞMEMELİ**.
    *   Kırmızı bir "Network Error" hatası **GÖRÜNMEMELİ**.
    *   Grafikler ve KPI'lar (Mock verilerle) **gelmeye devam etmeli**.
    *   Console'u (F12) açarsanız `🛡️ Brave Fallback Activated` uyarısını görmelisiniz.
    *   *CEO sunum yaparken Backend patlasa bile kimse anlamayacak.*

---

## 💎 Senaryo 3: 8px Grid Denetimi (Visual Polish)
**Amaç:** Arayüzün matematiksel nizamını kontrol etmek.

1.  Dashboard'daki KPI kartlarına ve grafiklere dikkatlice bakın.
2.  Kartlar arasındaki boşlukların (gap) eşit ve **24px** olduğunu gözlemleyin.
3.  Kart içindeki padding'lerin **24px** olduğunu hissedin.
4.  Başlık-İkon arası boşlukların **16px** olduğunu görün.
5.  Hiçbir öğe diğerine "çok yakın" veya "çok uzak" hissettirmemeli. Everything should feel "Solid".

---

## 🐳 Senaryo 4: One-Command Deploy
**Amaç:** Tüm sistemi tek komutla "Sıfırdan" ayağa kaldırmak.

1.  Tüm çalışan terminalleri kapatın.
2.  Proje ana dizininde terminali açın (`c:\Users\icene\Desktop\NEXT-GENT`).
3.  Şu komutu çalıştırın:
    ```bash
    docker-compose up --build
    ```
4.  **GÖZLEM:**
    *   PostgreSQL veritabanı başlatılacak (`nextgent_db`).
    *   Backend API Docker içinde derlenip `8000` portundan açılacak.
    *   Frontend Nginx içinde derlenip `80` portundan açılacak.
5.  Tarayıcıda `http://localhost` adresine gidin. Sistem çalışıyor olmalı.

---

**Onay Durumu:** [ ] Ready for Sunday Launch
