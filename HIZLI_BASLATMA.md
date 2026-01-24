# ⚡ Hızlı Başlatma - 3 Adımda Sistemi Görün

## 🚀 ADIM 1: Başlat (1 Komut)

```powershell
# Proje ana dizininde
docker-compose up --build
```

**Bekle**: 2-3 dakika (ilk seferde image'ler indirilecek)

---

## 🌐 ADIM 2: Tarayıcıda Aç

**Frontend:**
```
http://localhost
```

**Backend API Docs:**
```
http://localhost:8000/docs
```

**Health Check:**
```
http://localhost:8000/api/v1/health
```

---

## ✅ ADIM 3: Test Et

### Frontend Testi
1. Login sayfasında herhangi bir email/şifre gir
2. "Sign In" butonuna tıkla
3. Dashboard'u gör!

### Backend Testi
1. `/docs` sayfasında "Try it out" butonuna tıkla
2. `/health` endpoint'ini test et
3. Response'u gör!

---

## 🎯 Ne Göreceksiniz?

### Frontend
- ✅ Modern, lüks dashboard
- ✅ Animasyonlu geçişler
- ✅ KPI kartları ve grafikler
- ✅ Sektör switcher

### Backend
- ✅ Swagger UI (API documentation)
- ✅ Health check response
- ✅ Tüm endpoint'ler

---

**Detaylı Test**: `GORSELLE_TEST_REHBERI.md` dosyasına bakın

**Süre**: 5 dakika  
**Sonuç**: Sistemi gözlerinizle göreceksiniz! 👁️


