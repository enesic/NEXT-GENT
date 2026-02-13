# NextGent CRM - Production Deployment Kılavuzu

## 🎉 Mevcut Durum

### ✅ Tamamlanan İşlemler

1. ✅ **Frontend Vercel'de CANLI**: https://nextgent.co
2. ✅ **Veritabanı Export Edildi**: `backups\nextgent_backup_20260212_110141.dump` (3.1 MB)
3. ✅ **Tüm Yapılandırma Dosyaları Hazır**
4. ✅ **Docker Image Hazır**: Backend için
5. ✅ **Dokümantasyon Tamamlandı**: 8 detaylı kılavuz

### 🔄 Güncellenmiş Mimari

```
┌─────────────────┐
│  nextgent.co    │ ← Custom Domain
└────────┬────────┘
         │
         v
┌─────────────────┐       ┌──────────────────────┐
│  Vercel         │──────>│  AWS App Runner      │
│  (Frontend)     │  API  │  (Backend - FastAPI) │
│  Vue.js         │       │                      │
└─────────────────┘       └──────────┬───────────┘
                                     │
                            ┌────────┴────────┐
                            │                 │
                     ┌──────v──────┐   ┌─────v─────┐
                     │   Vercel    │   │  Vercel   │
                     │  Postgres   │   │  KV       │
                     └─────────────┘   └───────────┘
```

## 📚 Deployment Kılavuzları

### 🚀 Backend Deployment

| Kılavuz | Platform | Açıklama | Süre | Maliyet |
|---------|----------|----------|------|---------|
| [`RAILWAY_DEPLOYMENT.md`](RAILWAY_DEPLOYMENT.md) | Railway | ⭐ **ÖNERİLEN!** En kolay, $5 credit | 20 dk | $5-20/ay |
| [`AWS_QUICK_START.md`](AWS_QUICK_START.md) | AWS | Production-grade, daha karmaşık | 45 dk | $25-50/ay |
| [`AWS_DEPLOYMENT_GUIDE.md`](AWS_DEPLOYMENT_GUIDE.md) | AWS | Detaylı kılavuz (3 seçenek) | - | Değişken |
| [`DEPLOYMENT_SUCCESS.md`](DEPLOYMENT_SUCCESS.md) | Genel | Frontend başarı + sonraki adımlar | - | - |

### 🎨 Frontend Deployment (Tamamlandı)

| Durum | Detaylar |
|-------|----------|
| ✅ **CANLI** | https://nextgent.co |
| ✅ **Production** | https://next-gent-bbxs21jcs-enesics-projects.vercel.app |
| ✅ **Dashboard** | https://vercel.com/enesics-projects/next-gent |

### 📖 Diğer Kılavuzlar

| Dosya | İçerik |
|-------|--------|
| [`DEPLOYMENT_CHECKLIST.md`](DEPLOYMENT_CHECKLIST.md) | Hiçbir şeyi atlamayın |
| [`VERCEL_DEPLOYMENT_TR.md`](VERCEL_DEPLOYMENT_TR.md) | Genel Türkçe bakış |
| [`VERCEL_DEPLOYMENT_GUIDE.md`](VERCEL_DEPLOYMENT_GUIDE.md) | Detaylı İngilizce kılavuz |
| [`DEPLOYMENT_STEPS_TR.md`](DEPLOYMENT_STEPS_TR.md) | Adım adım Türkçe |

## 🎯 Sonraki 3 Adım

### 1️⃣ Vercel Storage (10 dakika) - MANUEL

**Vercel Postgres:**
1. https://vercel.com/dashboard → Storage → Create Database → Postgres
2. İsim: `nextgent-db`, Bölge: `Frankfurt (fra1)`
3. Connection string'i kopyalayın

**Vercel KV (Redis):**
1. Storage → Create Database → KV
2. İsim: `nextgent-redis`, Aynı bölge
3. Connection details'i kopyalayın

### 2️⃣ Database Import (5 dakika) - MANUEL

```powershell
# PostgreSQL client kurulumu (eğer yoksa)
choco install postgresql

# Import
pg_restore -d "VERCEL_POSTGRES_URL" -v backups\nextgent_backup_20260212_110141.dump
```

### 3️⃣ Backend Deployment - SEÇENEKLERİNİZ

**A) Railway (Önerilen - Basit ve Hızlı)**
- $5 ücretsiz credit/ay
- Kolay kurulum (20 dakika)
- Custom domain desteği
- **Kılavuz**: [`RAILWAY_DEPLOYMENT.md`](RAILWAY_DEPLOYMENT.md) ⭐

**B) AWS App Runner**
- Production-grade
- Daha pahalı ($25-50/ay)
- **Kılavuz**: [`AWS_QUICK_START.md`](AWS_QUICK_START.md)

## 💰 Maliyet Tahmini

| Servis | Paket | Aylık Maliyet |
|--------|-------|---------------|
| **Vercel** | | |
| - Frontend | Hobby | $0 |
| - Postgres | Pro | $5-10 |
| - KV (Redis) | Free | $0 |
| **Railway (Önerilen)** | | |
| - Backend | Hobby | $5-20 |
| **TOPLAM (Railway)** | | **$10-30/ay** |
| **AWS (Alternatif)** | | |
| - App Runner | 1vCPU 2GB | $25-50 |
| **TOPLAM (AWS)** | | **$30-70/ay** |

**Not:** 
- AWS Free Tier ile ilk 12 ay daha ucuz
- Production-ready, güvenli ve ölçeklenebilir

## 🔐 Güvenlik Kontrol Listesi

Deployment öncesi:

- [ ] Yeni `SECRET_KEY` oluşturuldu
- [ ] Yeni `ENCRYPTION_KEY` oluşturuldu
- [ ] `DEBUG=false` production'da
- [ ] CORS sadece belirli domain'lere izin veriyor
- [ ] Database backup alındı ve güvende
- [ ] `.env` dosyaları Git'e commit edilmedi
- [ ] AWS IAM en az yetki prensibi uygulandı
- [ ] SSL/HTTPS aktif (otomatik)

## 📊 Deployment Durumu

| Bileşen | Durum | URL/Konum |
|---------|-------|-----------|
| Frontend | ✅ CANLI | https://nextgent.co |
| Database Export | ✅ Tamamlandı | backups/ klasörü |
| Vercel Postgres | ⏳ Bekliyor | Manuel kurulum |
| Vercel KV | ⏳ Bekliyor | Manuel kurulum |
| AWS Backend | ⏳ Bekliyor | AWS_QUICK_START.md |
| Testing | ⏳ Bekliyor | Deployment sonrası |

## 🚀 Hızlı Başlangıç

```powershell
# 1. Vercel Storage oluşturun
#    https://vercel.com/dashboard → Storage

# 2. Database import edin
choco install postgresql
pg_restore -d "POSTGRES_URL" -v backups\nextgent_backup_20260212_110141.dump

# 3. AWS deployment başlatın
code AWS_QUICK_START.md
```

## 📱 Test Hesapları

Deployment sonrası test için:

| Sektör | Kullanıcı ID | PIN |
|--------|--------------|-----|
| Beauty | `BEA-000001` | `1234` |
| Hospitality | `HOS-000001` | `1234` |
| Medical | `MED-000001` | `1234` |

## 🆘 Yardım ve Destek

### Sorun Yaşıyorsanız

1. **Frontend Açılmıyor**: Vercel logs kontrol edin
2. **Backend Bağlanamıyor**: AWS CloudWatch logs kontrol edin
3. **Database Hatası**: Connection string'i doğrulayın
4. **CORS Hatası**: BACKEND_CORS_ORIGINS değişkenini kontrol edin

### Dokümantasyon

Her adım için detaylı dokümantasyon hazır:

```
NEXT-GENT/
├── AWS_QUICK_START.md           ⭐ BURADAN BAŞLAYIN
├── AWS_DEPLOYMENT_GUIDE.md      📖 Detaylı AWS kılavuzu
├── DEPLOYMENT_SUCCESS.md        ✅ Frontend başarı + sonraki adımlar
├── DEPLOYMENT_CHECKLIST.md      ✓ Kontrol listesi
├── VERCEL_DEPLOYMENT_TR.md      🇹🇷 Türkçe genel bakış
└── backups/                     💾 Database backup
    └── nextgent_backup_*.dump
```

## 🎉 Özet

**Yapıldı:**
- ✅ 8 kılavuz dosyası oluşturuldu
- ✅ Frontend Vercel'de canli
- ✅ Database export edildi
- ✅ Tüm yapılandırmalar hazır
- ✅ AWS seçeneği eklendi

**Kalan:**
- ⏳ Vercel Storage (10 dk)
- ⏳ Database import (5 dk)
- ⏳ AWS backend (45 dk)
- ⏳ Test (5 dk)

**Toplam Süre:** ~65 dakika

---

## 🔗 Önemli Linkler

- **Frontend**: https://nextgent.co
- **Vercel Dashboard**: https://vercel.com/dashboard
- **AWS Console**: https://console.aws.amazon.com
- **AWS App Runner**: https://console.aws.amazon.com/apprunner

---

**Başarılar! Her şey hazır, sadece 3 adım kaldı! 🚀**

*Son güncelleme: 12 Şubat 2026*
*Backend: Railway → AWS App Runner'a güncellendi*
