# NextGent CRM - Docker Compose Rehberi

Bu rehber, NextGent CRM sistemini Docker ile nasıl çalıştıracağınızı açıklar.

## 🚀 Hızlı Başlangıç

### 1. Sistemi Başlatın

```bash
docker-compose up -d
```

Bu komut:
- ✅ PostgreSQL veritabanını başlatır
- ✅ Redis cache'i başlatır
- ✅ Backend API'yi başlatır (port 8001)
- ✅ Frontend'i başlatır (port 80)
- ✅ Veritabanı tablolarını oluşturur
- ✅ **Otomatik olarak tüm sektörler için seed data yükler** (Beauty, Hospitality, Medical, vb.)

### 2. Logları İzleyin

```bash
docker-compose logs -f backend
```

Başlatma sırasında şunu göreceksiniz:
```
🔄 Waiting for database...
✅ Database ready!
🗄️  Initializing database...
🌱 Seeding data (Beauty, Hospitality, Medical, etc.)...
📊 Sample Logins:
  Beauty: BEA-000001 / PIN: 1234
  Hotel: HOS-000001 / PIN: 1234
  Medical: MED-000001 / PIN: 1234
🚀 Starting API server...
```

### 3. Uygulamaya Erişin

**Frontend:** `http://localhost`  
**Backend API:** `http://localhost:8001`  
**API Docs:** `http://localhost:8001/docs`

---

## 🎨 Test Giriş Bilgileri

### Güzellik Merkezi (Beauty)
- **URL:** `http://localhost/sectors/beauty/dashboard`
- **ID:** `BEA-000001` → `BEA-000050` (50 müşteri)
- **PIN:** `1234`

### Otel (Hospitality)
- **URL:** `http://localhost/sectors/hospitality/dashboard`
- **ID:** `HOS-000001` → `HOS-000050` (50 müşteri)
- **PIN:** `1234`

### Tıbbi (Medical)
- **URL:** `http://localhost/sectors/medical/dashboard`
- **ID:** `MED-000001` → `MED-000050`
- **PIN:** `1234`

### Diğer Sektörler
Her sektör için 50 müşteri oluşturulur:
- Legal: `LEG-000001` → `LEG-000050`
- Retail: `RTL-000001` → `RTL-000050`
- Education: `EDU-000001` → `EDU-000050`
- vb...

---

## 🛠️ Docker Komutları

### Sistemi Durdur
```bash
docker-compose down
```

### Sistemi Durdur ve Verileri Sil
```bash
docker-compose down -v
```

### Yeniden Başlat
```bash
docker-compose restart
```

### Sadece Backend'i Yeniden Başlat
```bash
docker-compose restart backend
```

### Logları Görüntüle
```bash
# Tüm servisler
docker-compose logs -f

# Sadece backend
docker-compose logs -f backend

# Sadece frontend
docker-compose logs -f frontend

# Sadece database
docker-compose logs -f db
```

### Container'lara Bağlan
```bash
# Backend container'a bağlan
docker exec -it nextgent_backend sh

# Database'e bağlan
docker exec -it nextgent_db psql -U postgres -d nextgent

# Redis'e bağlan
docker exec -it nextgent_redis redis-cli
```

---

## 🔄 Seed Verilerini Yeniden Yükle

Eğer verileri sıfırlayıp yeniden yüklemek isterseniz:

```bash
# Backend container içinde
docker exec -it nextgent_backend sh
python comprehensive_seed.py
exit
```

Veya container'ı yeniden başlatın (otomatik seed olacak):
```bash
docker-compose restart backend
```

---

## 📦 Servisler ve Portlar

| Servis | Port (Dış) | Port (İç) | Container Adı |
|--------|------------|-----------|---------------|
| Frontend | 80 | 80 | nextgent_frontend |
| Backend | 8001 | 8000 | nextgent_backend |
| PostgreSQL | 5432 | 5432 | nextgent_db |
| Redis | 6379 | 6379 | nextgent_redis |

---

## 🐛 Sorun Giderme

### Veritabanı Bağlantı Hatası
```bash
# Database health check
docker-compose ps

# Database loglarını kontrol et
docker-compose logs db
```

### Backend Başlamıyor
```bash
# Backend loglarını kontrol et
docker-compose logs backend

# Container'ı yeniden başlat
docker-compose restart backend
```

### Port Zaten Kullanımda
Eğer 80 veya 8001 portları kullanılıyorsa, `docker-compose.yml` dosyasındaki portları değiştirebilirsiniz:
```yaml
ports:
  - "8080:80"  # Frontend için 8080 kullan
  - "8002:8000"  # Backend için 8002 kullan
```

### Seed Data Yüklenmiyor
Manuel olarak yükleyin:
```bash
docker exec -it nextgent_backend python comprehensive_seed.py
```

---

## 📊 Oluşturulan Veriler

Her sektör için otomatik olarak oluşturulur:
- ✅ **50 müşteri** (Customer)
- ✅ **100 etkileşim** (Interaction/Appointment)
- ✅ **~80 VAPI araması** (80% call rate)
- ✅ **Token kullanım kayıtları**
- ✅ **~30 memnuniyet anketi** (60% response rate)
- ✅ **Denetim logları** (Audit logs)

**Toplam:** ~3,000+ kayıt tüm sektörler için!

---

## 🔐 Production Notları

Production'a deploy ederken:
1. `ENCRYPTION_KEY` değiştirin
2. `SECRET_KEY` değiştirin
3. `POSTGRES_PASSWORD` değiştirin
4. `DEBUG=false` olduğundan emin olun
5. `ENVIRONMENT=production` ayarlayın

---

## ✅ Başarı Kriterleri

Sistem doğru çalışıyorsa:
- ✅ `docker-compose ps` tüm servisleri "Up (healthy)" gösterir
- ✅ `http://localhost` frontend'i açar
- ✅ `http://localhost:8001/docs` API docs'u gösterir
- ✅ Beauty dashboard `/sectors/beauty/dashboard` çalışır
- ✅ Hotel dashboard `/sectors/hospitality/dashboard` çalışır
- ✅ Login `BEA-000001` / `1234` ile başarılı

---

**🎉 Başarılı kullanımlar!**
