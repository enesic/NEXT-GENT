# 🚀 Supabase + Railway - Hızlı Başlangıç

## ✅ Durum

- ✅ Frontend: https://nextgent.co (CANLI)
- ✅ Supabase Postgres: Seçildi ✨
- ✅ Database backup: Hazır
- ⏳ PostgreSQL client: Kuruluyor...

## 📋 Supabase Connection String'iniz

```
postgresql://postgres:[YOUR-PASSWORD]@db.kmuwxpyaqpkwfewnsijy.supabase.co:5432/postgres
```

## 🔐 ADIM 1: ŞİFRENİZİ ALIN

Supabase Dashboard'a gidin ve şifrenizi bulun:

1. https://supabase.com/dashboard
2. Projeniz → **Settings** → **Database**
3. **Connection String** bölümünde:
   - **Password** yazan yerde şifrenizi görebilirsiniz
   - Veya **Reset Database Password** ile yeni şifre oluşturun

**Şifrenizi kopyalayın!** (örn: `abc123xyz789`)

## 🔑 ADIM 2: UPSTASH REDIS

Vercel Marketplace'te **Upstash** seçin:

1. Vercel Dashboard → Storage → Marketplace → **Upstash**
2. Connect butonuna tıklayın
3. Upstash hesabı oluşturun (ücretsiz)
4. **Redis** database oluşturun:
   - Name: `nextgent-redis`
   - Region: **EU-West-1** (Europe)
   - Type: **Redis**
5. Connection string'i kopyalayın:
   ```
   redis://default:password@xyz.upstash.io:6379
   ```

## 📦 ADIM 3: DATABASE IMPORT

PostgreSQL kurulumu tamamlandıktan sonra (şu anda kuruluyor...):

### 3.1. Terminal'i Yeniden Açın

**ÖNEMLİ**: PostgreSQL kurulumu bitince terminal'i kapatıp yeniden açın!

### 3.2. Import Komutu

```powershell
# ŞİFRENİZİ yerleştirin!
pg_restore -d "postgresql://postgres:ŞİFRENİZ_BURAYA@db.kmuwxpyaqpkwfewnsijy.supabase.co:5432/postgres" -v backups\nextgent_backup_20260212_110141.dump
```

**Örnek** (şifre abc123xyz789 ise):
```powershell
pg_restore -d "postgresql://postgres:abc123xyz789@db.kmuwxpyaqpkwfewnsijy.supabase.co:5432/postgres" -v backups\nextgent_backup_20260212_110141.dump
```

## 🚂 ADIM 4: RAILWAY DEPLOYMENT

### 4.1. Güvenlik Anahtarları Oluşturun

```powershell
# SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# ENCRYPTION_KEY
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

**Çıktıları kopyalayın!**

### 4.2. Railway Deploy

1. https://railway.app → Login with GitHub
2. **New Project** → **Deploy from GitHub repo** → NextGent seçin
3. **Settings** → Root Directory: `backend`
4. **Variables** sekmesine gidin
5. Aşağıdaki değişkenleri ekleyin:

```env
# Uygulama
PROJECT_NAME=NextGent
API_V1_STR=/api/v1
ENVIRONMENT=production
DEBUG=false

# Güvenlik (Adım 4.1'den)
SECRET_KEY=<kopyaladığınız>
ENCRYPTION_KEY=<kopyaladığınız>

# Supabase Postgres (ŞİFRENİZİ ekleyin!)
DATABASE_URL=postgresql://postgres:ŞİFRENİZ@db.kmuwxpyaqpkwfewnsijy.supabase.co:5432/postgres
POSTGRES_SERVER=db.kmuwxpyaqpkwfewnsijy.supabase.co
POSTGRES_USER=postgres
POSTGRES_PASSWORD=ŞİFRENİZ
POSTGRES_DB=postgres
POSTGRES_PORT=5432

# Upstash Redis (Adım 2'den kopyalayın)
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

6. **Deploy** butonuna tıklayın
7. Railway URL'yi kopyalayın: `https://nextgent-backend-production.up.railway.app`

## 🔄 ADIM 5: FRONTEND GÜNCELLE

### 5.1. Environment Variable

`frontend\.env.production` dosyasını düzenleyin:
```env
VITE_API_BASE_URL=https://nextgent-backend-production.up.railway.app/api/v1
```

### 5.2. Vercel Redeploy

```powershell
vercel --prod --yes
```

## ✅ ADIM 6: TEST

### Backend Test:
```powershell
curl https://nextgent-backend-production.up.railway.app/api/v1/health
```

### Frontend Test:
```
https://nextgent.co → Login: BEA-000001 / 1234
```

## 💰 Maliyet (TAMAMEN ÜCRETSIZ BAŞLANGIÇ!)

| Servis | Tier | Maliyet |
|--------|------|---------|
| Vercel Frontend | Hobby | **$0** |
| Supabase Postgres | Free | **$0** (500MB) |
| Upstash Redis | Free | **$0** (10K cmd/day) |
| Railway Backend | Hobby | **$5 credit** (ilk ay ücretsiz!) |
| **TOPLAM** | | **İLK AY: $0!** 🎉 |

**Sonraki aylar**: ~$5-20 (Railway kullanımına göre)

## 🌐 Custom Domain (Backend)

Railway'de custom domain eklemek için:

1. Railway → Backend service → **Settings** → **Domains**
2. **Add Custom Domain**: `api.yourdomain.com`
3. DNS sağlayıcınızda CNAME ekleyin:
   ```
   Type: CNAME
   Name: api
   Value: nextgent-backend-production.up.railway.app
   ```
4. CORS güncelleyin:
   ```env
   BACKEND_CORS_ORIGINS=https://nextgent.co,https://api.yourdomain.com
   ```

## ⏰ Zaman Çizelgesi

| Adım | Süre | Durum |
|------|------|-------|
| PostgreSQL kurulumu | ~5 dk | ⏳ Şu anda |
| Upstash Redis | 3 dk | Sonraki |
| Database import | 2 dk | Sonraki |
| Railway deployment | 10 dk | Sonraki |
| Frontend güncelleme | 3 dk | Sonraki |
| Test | 5 dk | Son |
| **TOPLAM** | **~30 dk** | |

## 🆘 Sorun Giderme

### pg_restore hala bulunamıyor

Terminal'i kapatıp yeniden açın:
```powershell
# Yeni terminal'de
pg_restore --version
```

### Supabase şifre hatası

Supabase Dashboard → Settings → Database → Reset password

### Import hatası

Bazı uyarılar normal:
```
WARNING: errors ignored on restore
```

Önemli olan:
```
pg_restore: creating TABLE "public.tenants"  ← BU OLMALI
```

---

**PostgreSQL kurulumu bitince bu adımları takip edin! 🚀**

**ŞU ANDA YAPMANIZ GEREKEN:**
1. ⏳ PostgreSQL kurulumunun bitmesini bekleyin (~5 dk)
2. 🔐 Supabase'den şifrenizi alın
3. 📦 Upstash Redis oluşturun
4. ✅ Database import edin
5. 🚂 Railway'e deploy edin

**Başarılar! Tamamen ücretsiz başlangıç! 💰**
