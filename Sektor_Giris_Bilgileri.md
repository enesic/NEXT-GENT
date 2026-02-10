# 🏢 Sektörler ve Giriş Bilgileri Raporu

Bu dosya, NEXT-GENT sisteminde tanımlı olan sektörleri ve bu sektörlere erişim için kullanılabilecek test giriş bilgilerini içermektedir.

---

## 🔑 Yönetici (Admin) Giriş Bilgileri

Sistem geneline erişim için kullanılan yönetici hesabı bilgileridir.

- **URL:** `http://localhost/admin/login` veya `http://localhost:5173/admin/login`
- **Kullanıcı Adı:** `admin`
- **Şifre:** `admin123`

---

## 📊 Müşteri Sektörleri ve Giriş Örnekleri

Sistemde 10 farklı sektör için özelleştirilmiş dashboardlar bulunmaktadır. **Tüm test hesapları için PIN kodu standarttır.**

**Standart PIN:** `1234`

| Sektör | Sektör Kodu | Örnek Müşteri ID | Segment |
| :--- | :--- | :--- | :--- |
| **Sağlık (Medical)** | `MED` | `MED-000001` | VIP |
| **Hukuk (Legal)** | `LEG` | `LEG-000001` | VIP |
| **Emlak (Real Estate)** | `EST` | `EST-000001` | VIP |
| **Sanayi (Manufacturing)** | `MFG` | `MFG-000001` | VIP |
| **E-Ticaret (E-Commerce)** | `ECM` | `ECM-000001` | VIP |
| **Eğitim (Education)** | `EDU` | `EDU-000001` | VIP |
| **Finans (Finance)** | `FIN` | `FIN-000001` | VIP |
| **Otelcilik (Hospitality)** | `HTL` | `HTL-000001` | VIP |
| **Otomotiv (Automotive)** | `AUTO` | `AUTO-000001` | VIP |
| **Perakende (Retail)** | `RTL` | `RTL-000001` | VIP |

---

## 👥 Müşteri Segment Aralıkları

Her sektörde Müşteri ID numarasına göre farklı segmentler tanımlanmıştır:

*   **VIP:** `SECTOR-000001` ile `000002` arası
*   **GOLD:** `SECTOR-000003` ile `000005` arası
*   **SILVER:** `SECTOR-000006` ile `000010` arası
*   **REGULAR:** `SECTOR-000011` ile `000020` arası

---

## 💡 Önemli Notlar

1.  **Format:** Müşteri ID girerken daima büyük harf ve 6 haneli numara (örn: `MED-000001`) kullanınız.
2.  **Özellikler:** Her sektörün girişi sonrası dashboard; o sektöre özel ikonlar, grafikler ve menülerle yüklenir.
3.  **Sorun Giderme:** Eğer giriş başarısız olursa, veritabanının seed edildiğinden emin olun (`docker-compose exec backend python comprehensive_seed.py`).

---
*Hazırlanma Tarihi: 10 Şubat 2026*
