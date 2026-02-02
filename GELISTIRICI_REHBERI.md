# NEXT-GENT Geliştirici Başlangıç Rehberi

Hoş geldiniz! 3 kişilik "Task Force" ekibi olarak bu projeyi Pazar gününe kadar yayına alacağız.
Bu rehber, **bilgisayarınıza dokunmadan önce okumanız gereken** tek kaynaktır.

> [!IMPORTANT]
> **PAZAR GÜNÜ PLANLAMASI İÇİN TIKLA:** [SAATLİK PLAN (CRUNCH MODE)](TEAM_ROADMAP.md)
> Lütfen önce yukarıdaki plandan kendinize ait görevi ve saati kontrol edin!


---

## 1. Hazırlık (İlk 5 Dakika)

Projeye başlamadan önce aşağıdaki araçların kurulu olduğundan emin olun:
1.  **Git**: [İndir](https://git-scm.com/downloads)
2.  **Docker Desktop**: [İndir](https://www.docker.com/products/docker-desktop/) (Mutlaka çalışır durumda olsun)
3.  **Antigravity IDE**: Proje geliştirme ortamımız.

---

## 📥 2. Projeyi Bilgisayara İndirme (Clone)

Terminalinizi açın ve aşağıdaki komutları sırasıyla uygulayın.

1.  **Repoyu İndir:**
    ```bash
    git clone https://github.com/enesic/NEXT-GENT.git
    cd NEXT-GENT
    ```

2.  **Kendi Çalışma Dalına (Branch) Geç:**
    Hangi roldeyseniz o dala geçiş yapmalısınız:

    *    **Frontend (Kişi 1)**:
        ```bash
        git checkout feature/visual-polish
        ```
    *    **Backend (Kişi 2)**:
        ```bash
        git checkout feature/backend-fallback
        ```
    *    **DevOps (Kişi 3)**:
        ```bash
        git checkout infrastructure/docker-env
        ```

---

##  3. Ortam Değişkenlerini Ayarlama (.env)

Projenin çalışması için "gizli anahtarlara" ihtiyacı var.

1.  Proje ana dizinindeki örnek dosyayı kopyalayın:
    ```bash
    # Windows (PowerShell)
    cp .env.example .env
    ```

2.  `.env` dosyasını Antigravity editöründe açın.
3.  **ÖNEMLİ**: `OPENAI_API_KEY` kısmına ekibinizin ortak anahtarını yapıştırın. (Bu anahtar Discord/Slack kanalında sabitlenmiş mesajda!)

---

##  4. Projeyi Başlatma (Sihirli Komut)

Bizim takımın kuralı: **"Tek komutla her şey çalışmalı."**

Terminalde (Docker Desktop açıkken):

```powershell
docker-compose up --build
```

Bu komut şunları yapar:
*    **PostgreSQL** veritabanını kurar.
*    **Redis** önbellek sistemini açar.
*   **Backend** API'yi (FastAPI) ayağa kaldırır (`localhost:8000`).
*    **Frontend** arayüzü (Vue) sunar (`localhost:80`).

**Test Etmek İçin:**
Tarayıcınızı açın ve `http://localhost` adresine gidin. Giriş ekranını görüyorsanız başardınız! 🎉

---

##  5. Günlük Çalışma Akışı (Git Flow)

Her sabah ve her kodlamaya başlamadan önce:

1.  **Güncellemeleri Al:**
    ```bash
    git pull origin develop
    ```
    *(Başkalarının yaptığı değişiklikleri kendi bilgisayarına çek)*

2.  **Kodla ve Kaydet:**
    ```bash
    git add .
    git commit -m "Login animasyonu düzeltildi"
    ```

3.  **Gönder:**
    ```bash
    git push origin feature/senin-branch-adın
    ```

---

##  Sorun Giderici (Troubleshooting)

**S: "Port is already allocated" hatası alıyorum.**
C: Bilgisayarınızda 80, 8000 veya 5432 portunu kullanan başka bir şey var (Skype, başka proje, pgAdmin vb.). Onları kapatın veya `docker-compose.yml` dosyasından portları değiştirin.

**S: Veritabanı hatası alıyorum.**
C: Veritabanı ilk kez oluşurken bazen zaman alır. 
```bash
docker-compose down -v
docker-compose up --build
```
komutuyla her şeyi sıfırlayıp temiz bir sayfa açabilirsiniz.

---
**Bol şans Takım! Pazar günü şovu biz yapacağız! **
