# ⚡ Vercel Login Sonrası Hızlı Deployment

Vercel'e giriş yaptıktan sonra bu adımları takip edin.

## 🚀 Hızlı Deployment

### Otomatik Script ile (Önerilen)

Terminal'de bu komutu çalıştırın:

```powershell
.\deploy-automation.ps1
```

Bu script otomatik olarak:
- ✅ Frontend'i build eder
- ✅ Vercel'e deploy eder
- ✅ Size sonraki adımları gösterir

### Manuel Deployment

Ya da manuel olarak:

```bash
# Frontend deploy
vercel --prod
```

Sorulara cevaplar:
- Set up and deploy? **Yes**
- Which scope? **Your account**
- Link to existing project? **No**
- Project name? **nextgent**
- In which directory is your code? **./**
- Override settings? **No**

## 📝 Deployment Sonrası

Vercel size bir URL verecek:
```
https://nextgent-abc123.vercel.app
```

### Hemen Yapmanız Gerekenler

1. **Vercel Storage Oluşturun** (10 dakika):
   - https://vercel.com/dashboard → Storage
   - Postgres: `nextgent-db`
   - KV: `nextgent-redis`

2. **Database Import** (5 dakika):
   ```powershell
   pg_restore -d "<postgres-url>" -v backups\nextgent_backup_20260212_110141.dump
   ```

3. **Backend Deploy** (15 dakika):
   - https://railway.app
   - Deploy backend folder
   - Environment variables ekle

4. **CORS Güncelle** (2 dakika):
   - Railway'de `BACKEND_CORS_ORIGINS` değişkenine Vercel URL'nizi ekleyin

5. **Test!**
   - Vercel URL'nize gidin
   - Login test edin

## 📚 Detaylı Kılavuz

Tüm detaylar için: **DEPLOYMENT_STEPS_TR.md**

---

**Başarılar! 🎉**
