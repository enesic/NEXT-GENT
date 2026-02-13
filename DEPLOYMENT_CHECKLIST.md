# ✅ Deployment Kontrol Listesi

Deployment sürecini takip etmek için bu kontrol listesini kullanın.

## 🎯 Otomatik Tamamlanan İşler

- [x] Tüm yapılandırma dosyaları oluşturuldu
- [x] Backend CORS güncellemesi yapıldı
- [x] Frontend WebSocket yapılandırması güncellendi
- [x] Veritabanı backup'ı alındı: `backups\nextgent_backup_20260212_110141.dump`
- [x] Vercel CLI kuruldu
- [x] `.vercelignore` dosyası oluşturuldu
- [x] Deployment scriptleri hazırlandı
- [x] Türkçe dokümantasyon oluşturuldu

## 📋 Manuel Adımlar (Sırayla)

### 1️⃣ Vercel Authentication
- [ ] `vercel login` komutu çalıştırıldı
- [ ] Tarayıcıda https://vercel.com/oauth/device?user_code=BSCG-CQCK adresine gidildi
- [ ] Email ile giriş yapıldı
- [ ] Terminal'de "Success!" mesajı görüldü

### 2️⃣ Vercel Storage Kurulumu
- [ ] https://vercel.com/dashboard adresine gidildi
- [ ] Storage → Create Database → Postgres seçildi
- [ ] Database adı: `nextgent-db`, Bölge: `Frankfurt (fra1)`
- [ ] Postgres connection string kopyalandı
- [ ] Storage → Create Database → KV seçildi
- [ ] KV adı: `nextgent-redis`, Aynı bölge
- [ ] Redis connection details kopyalandı

### 3️⃣ Database Import
- [ ] PostgreSQL client tools kuruldu (eğer yoksa): `choco install postgresql`
- [ ] Vercel Postgres connection string hazır
- [ ] Import komutu çalıştırıldı:
  ```
  pg_restore -d "<postgres-url>" -v backups\nextgent_backup_20260212_110141.dump
  ```
- [ ] Import başarılı mesajı alındı
- [ ] Vercel Postgres dashboard'da tablolar görüldü

### 4️⃣ Güvenlik Anahtarları Oluşturma
- [ ] SECRET_KEY oluşturuldu:
  ```
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```
- [ ] ENCRYPTION_KEY oluşturuldu:
  ```
  python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
  ```
- [ ] Anahtarlar güvenli bir yere kaydedildi

### 5️⃣ Railway Backend Deployment
- [ ] https://railway.app adresine gidildi
- [ ] GitHub ile giriş yapıldı
- [ ] New Project → Deploy from GitHub repo seçildi
- [ ] NextGent repository seçildi
- [ ] Root Directory: `backend` yazıldı
- [ ] Variables sekmesine geçildi
- [ ] Tüm environment variables eklendi:
  - [ ] PROJECT_NAME=NextGent
  - [ ] API_V1_STR=/api/v1
  - [ ] ENVIRONMENT=production
  - [ ] DEBUG=false
  - [ ] SECRET_KEY (yeni oluşturulan)
  - [ ] ENCRYPTION_KEY (yeni oluşturulan)
  - [ ] POSTGRES_URL (Vercel'den)
  - [ ] POSTGRES_SERVER
  - [ ] POSTGRES_USER
  - [ ] POSTGRES_PASSWORD
  - [ ] POSTGRES_DB
  - [ ] POSTGRES_PORT=5432
  - [ ] REDIS_URL (Vercel KV'den)
  - [ ] REDIS_HOST
  - [ ] REDIS_PORT=6379
  - [ ] REDIS_PASSWORD
  - [ ] BACKEND_CORS_ORIGINS=http://localhost:5173
  - [ ] OPENAI_API_KEY (opsiyonel)
- [ ] Deploy butonu tıklandı
- [ ] Deployment logları kontrol edildi
- [ ] Public URL kopyalandı (örn: https://nextgent-backend.up.railway.app)

### 6️⃣ Frontend Environment Update
- [ ] `frontend\.env.production` dosyası açıldı
- [ ] `VITE_API_BASE_URL` değeri Railway URL ile güncellendi:
  ```
  VITE_API_BASE_URL=https://nextgent-backend.up.railway.app/api/v1
  ```
- [ ] Dosya kaydedildi

### 7️⃣ Frontend Vercel Deployment
**Otomatik Script ile:**
- [ ] `.\deploy-automation.ps1` komutu çalıştırıldı
- [ ] Frontend build başarılı
- [ ] Vercel'e deploy edildi

**Ya da Manuel:**
- [ ] `vercel --prod` komutu çalıştırıldı
- [ ] Deployment tamamlandı
- [ ] Vercel URL kopyalandı (örn: https://nextgent.vercel.app)

### 8️⃣ CORS Configuration Update
- [ ] Railway dashboard açıldı
- [ ] Backend servis seçildi
- [ ] Variables sekmesine gidildi
- [ ] `BACKEND_CORS_ORIGINS` bulundu
- [ ] Vercel URL eklendi:
  ```
  https://nextgent.vercel.app
  ```
- [ ] Backend redeploy edildi
- [ ] Deployment tamamlandı

### 9️⃣ Testing & Verification
- [ ] Vercel frontend URL'si açıldı
- [ ] Login sayfası göründü
- [ ] Test hesapları denendi:
  - [ ] Beauty: `BEA-000001` / PIN: `1234`
  - [ ] Hotel: `HOS-000001` / PIN: `1234`
  - [ ] Medical: `MED-000001` / PIN: `1234`
- [ ] Dashboard yüklendi
- [ ] Browser DevTools açıldı
- [ ] Network tab kontrol edildi:
  - [ ] API çağrıları backend URL'sine gidiyor
  - [ ] CORS hataları yok
  - [ ] 200 OK response'lar alınıyor
- [ ] WebSocket bağlantısı kontrol edildi:
  - [ ] Sağ alt köşede bağlantı göstergesi var
  - [ ] Console'da WebSocket bağlantı mesajı görüldü
- [ ] Temel özellikler test edildi:
  - [ ] Müşteri listesi yüklendi
  - [ ] Dashboard grafikleri göründü
  - [ ] Yeni müşteri eklenebildi

### 🔟 Custom Domain (Opsiyonel)
- [ ] Vercel Dashboard → Project → Settings → Domains
- [ ] Domain eklendi
- [ ] DNS kayıtları güncellendi:
  - [ ] A Record: `@` → `76.76.21.21`
  - [ ] veya CNAME: `www` → `cname.vercel-dns.com`
- [ ] SSL sertifikası beklendi (~10 dakika)
- [ ] Custom domain çalışıyor
- [ ] Backend CORS'a custom domain eklendi
- [ ] Backend redeploy edildi

## 🎉 Deployment Tamamlandı!

Tüm checkboxlar işaretliyse, tebrikler! NextGent CRM sisteminiz artık Vercel'de çalışıyor.

### 📊 Final Checklist

- [ ] Frontend çalışıyor: https://nextgent.vercel.app
- [ ] Backend çalışıyor: https://nextgent-backend.up.railway.app
- [ ] Database import edildi ve çalışıyor
- [ ] Redis bağlantısı çalışıyor
- [ ] Login başarılı
- [ ] Dashboard yükleniyor
- [ ] API çağrıları çalışıyor
- [ ] WebSocket bağlantısı aktif
- [ ] CORS yapılandırması doğru

### 🔐 Güvenlik Son Kontrol

- [ ] Yeni SECRET_KEY kullanılıyor
- [ ] Yeni ENCRYPTION_KEY kullanılıyor
- [ ] DEBUG=false production'da
- [ ] CORS sadece belirli domain'lere izin veriyor
- [ ] Backup dosyaları güvende saklanıyor
- [ ] .env dosyaları Git'e commit edilmemiş

### 📚 Dokümantasyon

Deployment hakkında daha fazla bilgi:
- **Hızlı Başlangıç**: `AFTER_VERCEL_LOGIN.md`
- **Detaylı Adımlar**: `DEPLOYMENT_STEPS_TR.md`
- **Genel Bakış**: `VERCEL_DEPLOYMENT_TR.md`
- **İngilizce Kılavuz**: `VERCEL_DEPLOYMENT_GUIDE.md`

### 🆘 Sorun Giderme

Sorun yaşıyorsanız:
1. Browser console loglarını kontrol edin
2. Vercel deployment loglarını kontrol edin
3. Railway backend loglarını kontrol edin
4. CORS yapılandırmasını tekrar kontrol edin
5. Database bağlantı string'lerini doğrulayın

---

**Başarılar! 🚀**

*Son güncelleme: 12 Şubat 2026*
