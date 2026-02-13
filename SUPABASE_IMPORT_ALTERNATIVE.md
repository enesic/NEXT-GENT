# 🚀 Supabase Database Import - Alternatif Yöntem

## DNS Sorunu Nedeniyle

PostgreSQL client Supabase'e bağlanamıyor. İki alternatif yöntem:

---

## ✅ Yöntem 1: Supabase SQL Editor (ÖNERİLEN - 2 dk)

### Adım 1: Backup'ı SQL'e Çevir

Terminal'de:
```powershell
& "C:\Program Files\PostgreSQL\16\bin\pg_restore.exe" --schema-only --no-owner --no-acl "backups\nextgent_backup_20260212_110141.dump" > schema.sql

& "C:\Program Files\PostgreSQL\16\bin\pg_restore.exe" --data-only --no-owner --no-acl "backups\nextgent_backup_20260212_110141.dump" > data.sql
```

### Adım 2: Supabase'e Import

1. https://supabase.com/dashboard → Project → SQL Editor
2. `schema.sql` dosyasını aç, içeriği kopyala
3. SQL Editor'e yapıştır → Run
4. `data.sql` dosyasını aç, içeriği kopyala  
5. SQL Editor'e yapıştır → Run

---

## ✅ Yöntem 2: VPN/Proxy Kapat (30 saniye)

Eğer Cloudflare WARP veya VPN kullanıyorsan:

1. VPN/WARP'ı kapat
2. Ben tekrar import komutu çalıştıracağım
3. Bağlantı başarılı olunca import edilecek

---

## ✅ Yöntem 3: Test Data ile Başla (EN HIZLI)

Eğer test ortamında çalışıyorsan:

- Backend'i Vercel'e deploy et
- Backend otomatik test data oluşturacak
- Daha sonra production data'yı import ederiz

---

## 🎯 Hangisini Tercih Edersin?

**Önerim:** Yöntem 2'yi dene (VPN kapat), çalışmazsa Yöntem 1.

Şimdi ne yapmak istersin? Söyle devam edelim! 🚀
