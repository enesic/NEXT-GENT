# ✅ Otomatik Deployment Adımları

## Tamamlanan İşlemler

1. ✅ **Tüm yapılandırma dosyaları oluşturuldu**
2. ✅ **Veritabanı dışa aktarıldı**: `backups\nextgent_backup_20260212_110141.dump`
3. ✅ **Vercel CLI kuruldu**

## 📋 Şimdi Yapmanız Gerekenler

### Adım 1: Vercel'e Giriş Yapın (2 dakika)

Terminal'de şu komutu çalıştırın:

```bash
vercel login
```

Tarayıcınız açılacak ve Vercel'e giriş yapmanız istenecek:
1. Email adresinizi girin
2. Doğrulama linkine tıklayın
3. Terminal'de "Success!" mesajını bekleyin

### Adım 2: Vercel Storage Oluşturun (10 dakika)

1. **Vercel Postgres Oluşturun**:
   - https://vercel.com/dashboard adresine gidin
   - Storage → Create Database → Postgres
   - İsim: `nextgent-db`
   - Bölge: `Frankfurt (fra1)`
   - Create butonuna tıklayın
   - Connection bilgilerini kopyalayın (aşağıdaki gibi):
     ```
     POSTGRES_URL="postgres://default:abc123@ep-xxx.vercel-storage.com:5432/verceldb"
     ```

2. **Vercel KV (Redis) Oluşturun**:
   - Storage → Create Database → KV
   - İsim: `nextgent-redis`
   - Aynı bölge: `Frankfurt (fra1)`
   - Create butonuna tıklayın
   - Connection bilgilerini kopyalayın:
     ```
     KV_URL="redis://default:abc123@xxx.vercel-storage.com:6379"
     ```

### Adım 3: Veritabanını Import Edin (5 dakika)

Terminal'de şu komutu çalıştırın (Vercel Postgres URL'nizi kullanın):

```powershell
# PostgreSQL client tools kurulu değilse:
choco install postgresql
# veya: winget install PostgreSQL.PostgreSQL

# Import işlemi:
pg_restore -d "POSTGRES_URL_BURAYA" -v backups\nextgent_backup_20260212_110141.dump
```

**Örnek**:
```powershell
pg_restore -d "postgres://default:abc123@ep-xxx.vercel-storage.com:5432/verceldb" -v backups\nextgent_backup_20260212_110141.dump
```

### Adım 4: Railway'de Backend Hesabı Oluşturun (15 dakika)

1. **Railway Hesabı**:
   - https://railway.app adresine gidin
   - GitHub ile giriş yapın

2. **Backend Deploy**:
   - New Project → Deploy from GitHub repo
   - NextGent repository'nizi seçin
   - Root Directory: `backend` yazın
   - Variables sekmesine geçin

3. **Environment Variables Ekleyin**:

```env
# Uygulama
PROJECT_NAME=NextGent
API_V1_STR=/api/v1
ENVIRONMENT=production
DEBUG=false

# Güvenlik - YENİ ANAHTARLAR OLUŞTURUN!
# Terminal'de şunları çalıştırın:
# python -c "import secrets; print(secrets.token_urlsafe(32))"
# python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
SECRET_KEY=buraya-yeni-secret-key
ENCRYPTION_KEY=buraya-yeni-encryption-key

# Vercel Postgres (Adım 2'den)
POSTGRES_URL=postgres://default:abc123@ep-xxx.vercel-storage.com:5432/verceldb
POSTGRES_SERVER=ep-xxx.vercel-storage.com
POSTGRES_USER=default
POSTGRES_PASSWORD=abc123
POSTGRES_DB=verceldb
POSTGRES_PORT=5432

# Vercel KV / Redis (Adım 2'den)
KV_URL=redis://default:abc123@xxx.vercel-storage.com:6379
REDIS_HOST=xxx.vercel-storage.com
REDIS_PORT=6379
REDIS_PASSWORD=abc123

# CORS (şimdilik localhost, sonra güncellenecek)
BACKEND_CORS_ORIGINS=http://localhost:5173

# OpenAI (opsiyonel)
OPENAI_API_KEY=your-openai-key
AI_MODEL=gpt-4o-mini
AI_ENABLED=true
```

4. **Deploy Edin**:
   - Deploy butonuna tıklayın
   - Deployment loglarını izleyin
   - Public URL'yi kopyalayın (örn: `https://nextgent-backend-production.up.railway.app`)

### Adım 5: Frontend .env Dosyasını Güncelleyin (1 dakika)

`frontend\.env.production` dosyasını açın ve Backend URL'nizi yazın:

```env
VITE_API_BASE_URL=https://nextgent-backend-production.up.railway.app/api/v1
```

### Adım 6: Frontend'i Vercel'e Deploy Edin (5 dakika)

Terminal'de:

```bash
vercel --prod
```

Sorulara şöyle cevap verin:
- Set up and deploy? **Yes**
- Which scope? **Your account**
- Link to existing project? **No**
- Project name? **nextgent** (veya istediğiniz isim)
- In which directory is your code? **./**
- Override settings? **No**

Deploy tamamlandığında size bir URL verilecek:
```
https://nextgent-abc123.vercel.app
```

### Adım 7: CORS Güncelleyin (3 dakika)

1. Railway dashboard'a gidin
2. Backend servisinize tıklayın
3. Variables sekmesinde `BACKEND_CORS_ORIGINS` değişkenini bulun
4. Vercel URL'nizi ekleyin:
   ```
   https://nextgent-abc123.vercel.app
   ```
5. Redeploy edin

### Adım 8: Test Edin! (5 dakika)

1. Vercel URL'nize gidin: `https://nextgent-abc123.vercel.app`
2. Test hesaplarıyla giriş yapın:
   - Beauty: `BEA-000001` / PIN: `1234`
   - Hotel: `HOS-000001` / PIN: `1234`
   - Medical: `MED-000001` / PIN: `1234`
3. Dashboard'un çalıştığını kontrol edin
4. Browser DevTools → Network sekmesinde API çağrılarını kontrol edin
5. WebSocket bağlantısını kontrol edin (sağ alt köşe)

## 🎉 Tamamlandı!

Deployment başarılı! Artık sisteminiz Vercel'de çalışıyor.

### Önemli URL'ler

- Frontend: `https://nextgent-abc123.vercel.app`
- Backend: `https://nextgent-backend-production.up.railway.app`
- Vercel Dashboard: https://vercel.com/dashboard
- Railway Dashboard: https://railway.app/dashboard

### Sonraki Adımlar (Opsiyonel)

- **Custom Domain**: Vercel Dashboard → Domains → Add domain
- **Monitoring**: Vercel Analytics'i etkinleştirin
- **Backups**: Otomatik veritabanı backup stratejisi kurun

## 🆘 Yardım

Sorun yaşarsanız:
- `VERCEL_DEPLOYMENT_TR.md` dosyasına bakın
- `VERCEL_DEPLOYMENT_GUIDE.md` dosyasına bakın (detaylı İngilizce kılavuz)

---

**Başarılar! 🚀**
