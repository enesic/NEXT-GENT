# 🚂 Railway Hızlı Başlangıç - 3 Adımda Backend Deployment

## ✅ Hazır Olanlar

- ✅ Frontend Vercel'de CANLI: https://nextgent.co  
- ✅ Database backup: `backups\nextgent_backup_20260212_110141.dump`
- ✅ Docker container hazır
- ✅ Tüm dokümantasyon hazır

## 🎯 3 Basit Adım (Toplam ~35 dakika)

### Adım 1: Vercel Storage + Database Import (15 dakika)

**1.1. Vercel Postgres:**
```
https://vercel.com/dashboard → Storage → Create Database → Postgres
Name: nextgent-db
Region: Frankfurt (fra1)
→ Connection string'i kopyala
```

**1.2. Vercel KV (Redis):**
```
Storage → Create Database → KV
Name: nextgent-redis
→ Connection details'i kopyala
```

**1.3. Database Import:**
```powershell
choco install postgresql
pg_restore -d "POSTGRES_URL_BURAYA" -v backups\nextgent_backup_20260212_110141.dump
```

### Adım 2: Railway Deployment (10 dakika)

**2.1. Railway Hesabı:**
```
https://railway.app → Login with GitHub
```

**2.2. Deploy:**
```
New Project → Deploy from GitHub repo → NextGent
Settings → Root Directory: "backend"
```

**2.3. Environment Variables Ekle:**

Güvenlik anahtarları oluştur:
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Railway Variables sekmesinde ekle:
```env
PROJECT_NAME=NextGent
API_V1_STR=/api/v1
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=<yeni-oluşturduğunuz>
ENCRYPTION_KEY=<yeni-oluşturduğunuz>
POSTGRES_URL=<Vercel'den kopyaladığınız>
POSTGRES_SERVER=<Vercel'den>
POSTGRES_USER=default
POSTGRES_PASSWORD=<Vercel'den>
POSTGRES_DB=verceldb
POSTGRES_PORT=5432
REDIS_URL=<Vercel KV'den>
REDIS_HOST=<Vercel'den>
REDIS_PORT=6379
REDIS_PASSWORD=<Vercel'den>
BACKEND_CORS_ORIGINS=https://nextgent.co
```

Deploy butonuna tıkla → Railway URL'yi kopyala!

### Adım 3: Frontend Güncelle + Test (10 dakika)

**3.1. Frontend .env.production güncelle:**
```env
VITE_API_BASE_URL=https://nextgent-backend-production.up.railway.app/api/v1
```

**3.2. Vercel'e deploy:**
```powershell
vercel --prod --yes
```

**3.3. Test:**
```
https://nextgent.co → Login: BEA-000001 / 1234
```

## 🌐 Bonus: Custom Domain (Opsiyonel, +15 dakika)

**Railway'de:**
```
Settings → Domains → Add Custom Domain → api.yourdomain.com
```

**DNS Sağlayıcınızda:**
```
Type: CNAME
Name: api
Value: nextgent-backend-production.up.railway.app
```

Bekleyin (5-60 dakika) → SSL otomatik!

## 💰 Maliyet

- Vercel: $0-10/ay
- Railway: $5 credit (ilk ay ücretsiz), sonra $5-20/ay
- **Toplam: ~$10-30/ay**

## 📚 Detaylı Kılavuz

Sorun yaşarsanız: [`RAILWAY_DEPLOYMENT.md`](RAILWAY_DEPLOYMENT.md)

---

**3 adımda hazır! 🎉**
