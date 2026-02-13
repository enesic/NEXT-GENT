# Supabase + Railway Deployment Kılavuzu

## ✅ Mevcut Durum

- ✅ Frontend Vercel'de: https://nextgent.co
- ✅ **Supabase Postgres** seçildi (HARIKA SEÇİM!)
- ✅ Database backup hazır: `backups\nextgent_backup_20260212_110141.dump`
- ⏳ PostgreSQL client tools kuruluyor...

## 🎯 Supabase Connection String

Sizin connection string'iniz:
```
postgresql://postgres:[YOUR-PASSWORD]@db.kmuwxpyaqpkwfewnsijy.supabase.co:5432/postgres
```

**ÖNEMLİ**: `[YOUR-PASSWORD]` kısmını Supabase'den aldığınız gerçek şifre ile değiştirin!

## 📋 Adım 1: Redis Database Seçimi

Supabase sadece Postgres sağlıyor. Redis için ayrı bir servis seçmelisiniz:

### Seçenek 1: Upstash Redis (Önerilen)

Vercel Dashboard → Storage → **Upstash** seçin

**Neden Upstash:**
- ✅ **Ücretsiz tier**: 10,000 komut/gün
- ✅ Serverless Redis
- ✅ Supabase ile uyumlu
- ✅ Global regions

**Kurulum:**
1. Vercel Storage → Marketplace → **Upstash**
2. Connect butonuna tıklayın
3. Upstash hesabı oluşturun
4. Redis database oluşturun:
   - Name: `nextgent-redis`
   - Region: **EU-West-1** (Avrupa)
   - Type: **Redis** (Vector/Queue değil!)
5. Connection string'i kopyalayın:
   ```
   redis://default:password@xyz.upstash.io:6379
   ```

### Seçenek 2: Redis Cloud (Alternatif)

Marketplace'te "Redis" seçeneğini kullanın (ama ücretli olabilir).

## 📦 Adım 2: Database Import

PostgreSQL kurulumu tamamlandıktan sonra:

### 2.1. Şifrenizi Connection String'e Ekleyin

Supabase dashboard'da şifrenizi bulun ve connection string'e ekleyin:

```
postgresql://postgres:GERÇEK_ŞİFRE_BURAYA@db.kmuwxpyaqpkwfewnsijy.supabase.co:5432/postgres
```

### 2.2. Import Komutunu Çalıştırın

```powershell
# PostgreSQL kurulumu tamamlandıktan sonra terminal'i yeniden açın veya:
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Import işlemi (şifrenizi yerleştirin!)
pg_restore -d "postgresql://postgres:GERÇEK_ŞİFRE@db.kmuwxpyaqpkwfewnsijy.supabase.co:5432/postgres" -v backups\nextgent_backup_20260212_110141.dump
```

**Beklenen çıktı:**
```
pg_restore: processing data for table "public.tenants"
pg_restore: processing data for table "public.customers"
...
pg_restore: creating CONSTRAINT "public.tenants tenants_pkey"
```

**Not**: Permission uyarıları normal, önemli olan ERROR olmadan bitmesi.

### 2.3. Import Doğrulama

Supabase Dashboard → SQL Editor → Query çalıştırın:
```sql
SELECT COUNT(*) FROM tenants;
SELECT COUNT(*) FROM customers;
```

Veriler görünüyorsa başarılı!

## 🚂 Adım 3: Railway Deployment

### 3.1. Railway Hesabı

1. https://railway.app → Login with GitHub
2. Repository erişim izni verin

### 3.2. Backend Deploy

1. **New Project** → **Deploy from GitHub repo**
2. **NextGent** repository seçin
3. **Settings** → Root Directory: `backend`

### 3.3. Environment Variables (Railway)

**Güvenlik Anahtarları Oluşturun:**
```powershell
# SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# ENCRYPTION_KEY
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

**Railway Variables sekmesinde ekleyin:**

```env
# Uygulama
PROJECT_NAME=NextGent
API_V1_STR=/api/v1
ENVIRONMENT=production
DEBUG=false

# Güvenlik (yukarıda oluşturduğunuz)
SECRET_KEY=<yeni-oluşturduğunuz>
ENCRYPTION_KEY=<yeni-oluşturduğunuz>

# Supabase Postgres (şifrenizi ekleyin!)
DATABASE_URL=postgresql://postgres:ŞİFRE@db.kmuwxpyaqpkwfewnsijy.supabase.co:5432/postgres
POSTGRES_SERVER=db.kmuwxpyaqpkwfewnsijy.supabase.co
POSTGRES_USER=postgres
POSTGRES_PASSWORD=ŞİFRE
POSTGRES_DB=postgres
POSTGRES_PORT=5432

# Upstash Redis (Upstash'ten kopyalayın)
REDIS_URL=redis://default:password@xyz.upstash.io:6379
REDIS_HOST=xyz.upstash.io
REDIS_PORT=6379
REDIS_PASSWORD=password

# CORS
BACKEND_CORS_ORIGINS=https://next-gent-bbxs21jcs-enesics-projects.vercel.app,https://nextgent.co

# OpenAI (opsiyonel)
OPENAI_API_KEY=sk-proj-your-key
AI_MODEL=gpt-4o-mini
AI_ENABLED=true
```

### 3.4. Deploy

**Deploy** butonuna tıklayın → 3-5 dakika bekleyin

Railway URL'yi alın:
```
https://nextgent-backend-production.up.railway.app
```

## 🔄 Adım 4: Frontend Güncelleme

### 4.1. Environment Variable

`frontend\.env.production` dosyasını düzenleyin:
```env
VITE_API_BASE_URL=https://nextgent-backend-production.up.railway.app/api/v1
```

### 4.2. Vercel Redeploy

```powershell
vercel --prod --yes
```

## ✅ Adım 5: Test

### 5.1. Backend Health Check

```powershell
curl https://nextgent-backend-production.up.railway.app/api/v1/health
```

### 5.2. Frontend Test

https://nextgent.co → Login:
- Beauty: `BEA-000001` / `1234`
- Hotel: `HOS-000001` / `1234`

## 🌐 Bonus: Custom Domain (Backend)

### Railway'de Custom Domain

1. Railway → Backend service → **Settings** → **Domains**
2. **Add Custom Domain**: `api.yourdomain.com`
3. DNS kayıtlarını ekleyin:
   ```
   Type: CNAME
   Name: api
   Value: nextgent-backend-production.up.railway.app
   TTL: 3600
   ```

4. CORS güncelleyin:
   ```env
   BACKEND_CORS_ORIGINS=https://nextgent.co,https://api.yourdomain.com
   ```

## 💰 Maliyet

| Servis | Tier | Aylık |
|--------|------|-------|
| Vercel Frontend | Hobby | $0 |
| Supabase Postgres | Free | **$0** (500MB) |
| Upstash Redis | Free | **$0** (10K cmd/day) |
| Railway Backend | Hobby | **$5 credit** → $5-20 |
| **TOPLAM** | | **İlk ay $0-5!** |

**Mükemmel!** En ucuz kombinasyon!

## 🆘 Troubleshooting

### pg_restore bulunamıyor

PostgreSQL kurulumu tamamlandıktan sonra terminal'i kapatıp yeniden açın:

```powershell
# PATH'i yenileyin
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Tekrar deneyin
pg_restore --version
```

### Supabase şifre hatası

Supabase Dashboard → Settings → Database → Password → Reset password

Yeni şifreyi connection string'e ekleyin.

### Railway build hatası

Railway logs kontrol edin, environment variables eksik olabilir.

## ✅ Checklist

- [ ] Supabase Postgres oluşturuldu
- [ ] Upstash Redis oluşturuldu
- [ ] PostgreSQL client kuruldu
- [ ] Supabase şifresi connection string'e eklendi
- [ ] Database import başarılı
- [ ] Railway hesabı açıldı
- [ ] Environment variables eklendi
- [ ] Railway'e deploy edildi
- [ ] Frontend .env.production güncellendi
- [ ] Vercel'e redeploy edildi
- [ ] Test başarılı

---

**Başarılar! Supabase + Upstash + Railway = Tamamen ücretsiz başlangıç! 🎉**
