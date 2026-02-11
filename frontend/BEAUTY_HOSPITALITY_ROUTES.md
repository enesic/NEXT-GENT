# Güzellik Merkezi ve Otel Router Ayarları

## ✅ Güncelleme Tamamlandı

Beauty (Güzellik Merkezi) ve Hospitality (Otel Yönetimi) sektörleri için detaylı route yapısı eklendi.

## 🏨 Güzellik Merkezi (Beauty) - Routes

### 1. Ana Dashboard
```javascript
Path: '/sectors/beauty/dashboard'
Name: 'BeautyDashboard'
Component: BeautyDashboard.vue
Meta: {
    requiresAuth: true,
    sector: 'beauty',
    title: 'Güzellik Merkezi Dashboard',
    description: 'Beauty salon management dashboard'
}
```

**Erişim**: http://localhost/sectors/beauty/dashboard  
**Giriş Bilgileri**: `BEA-000001` / PIN: `1234`

### 2. Randevular (Appointments)
```javascript
Path: '/sectors/beauty/appointments'
Name: 'BeautyAppointments'
Meta: {
    requiresAuth: true,
    sector: 'beauty',
    title: 'Randevular'
}
```

**Özellikler**:
- Randevu listesi
- Yeni randevu oluşturma
- Randevu düzenleme/iptal
- Randevu filtreleme (tarih, durum, hizmet)

### 3. Hizmetler (Services)
```javascript
Path: '/sectors/beauty/services'
Name: 'BeautyServices'
Meta: {
    requiresAuth: true,
    sector: 'beauty',
    title: 'Hizmetler'
}
```

**Özellikler**:
- Saç kesimi, boyama, manikür, pedikür
- Cilt bakımı, makyaj
- Hizmet fiyatları
- Hizmet süreleri

### 4. Müşteriler (Customers)
```javascript
Path: '/sectors/beauty/customers'
Name: 'BeautyCustomers'
Meta: {
    requiresAuth: true,
    sector: 'beauty',
    title: 'Müşteriler'
}
```

**Özellikler**:
- Müşteri listesi ve arama
- Müşteri detayları
- Geçmiş randevular
- Müşteri segmentasyonu (VIP, GOLD, SILVER, REGULAR)

---

## 🏨 Otel Yönetimi (Hospitality) - Routes

### 1. Ana Dashboard
```javascript
Path: '/sectors/hospitality/dashboard'
Name: 'HospitalityDashboard'
Component: HospitalityDashboard.vue
Meta: {
    requiresAuth: true,
    sector: 'hospitality',
    title: 'Otel Yönetimi Dashboard',
    description: 'Hotel management dashboard'
}
```

**Erişim**: http://localhost/sectors/hospitality/dashboard  
**Giriş Bilgileri**: `HOS-000001` / PIN: `1234`

### 2. Rezervasyonlar (Reservations)
```javascript
Path: '/sectors/hospitality/reservations'
Name: 'HospitalityReservations'
Meta: {
    requiresAuth: true,
    sector: 'hospitality',
    title: 'Rezervasyonlar'
}
```

**Özellikler**:
- Rezervasyon listesi
- Yeni rezervasyon oluşturma
- Check-in / Check-out işlemleri
- Rezervasyon durumu (PENDING, CONFIRMED, COMPLETED, CANCELLED)

### 3. Oda Yönetimi (Rooms)
```javascript
Path: '/sectors/hospitality/rooms'
Name: 'HospitalityRooms'
Meta: {
    requiresAuth: true,
    sector: 'hospitality',
    title: 'Oda Yönetimi'
}
```

**Özellikler**:
- Oda tipi yönetimi (Standart, Deluxe, Suite)
- Oda durumu (Boş, Dolu, Temizlik, Bakım)
- Oda fiyatlandırma
- Oda özellikleri

### 4. Misafirler (Guests)
```javascript
Path: '/sectors/hospitality/guests'
Name: 'HospitalityGuests'
Meta: {
    requiresAuth: true,
    sector: 'hospitality',
    title: 'Misafirler'
}
```

**Özellikler**:
- Misafir listesi
- Misafir profilleri
- Konaklama geçmişi
- Sadakat programı (VIP misafirler)

---

## 🚀 Kullanım

### Frontend Navigation
```javascript
// Programmatic navigation
import { useRouter } from 'vue-router'

const router = useRouter()

// Güzellik Merkezi'ne git
router.push({ name: 'BeautyDashboard' })
router.push('/sectors/beauty/dashboard')

// Otel Yönetimi'ne git
router.push({ name: 'HospitalityDashboard' })
router.push('/sectors/hospitality/dashboard')

// Alt sayfalara git
router.push({ name: 'BeautyAppointments' })
router.push({ name: 'HospitalityReservations' })
```

### Template Navigation
```vue
<template>
  <!-- Router Link ile -->
  <router-link :to="{ name: 'BeautyDashboard' }">
    Güzellik Merkezi
  </router-link>
  
  <router-link to="/sectors/hospitality/dashboard">
    Otel Yönetimi
  </router-link>
  
  <!-- Button ile -->
  <button @click="$router.push({ name: 'BeautyAppointments' })">
    Randevular
  </button>
</template>
```

---

## 🔐 Authentication Guard

Tüm route'lar `requiresAuth: true` ile korunmaktadır:

```javascript
router.beforeEach((to, from, next) => {
    if (to.meta.requiresAuth) {
        const authStore = useAuthStore()
        if (!authStore.isAuthenticated) {
            return next('/login')
        }
    }
    next()
})
```

---

## 📊 Meta Bilgileri

Her route için eklenen meta bilgileri:

```javascript
meta: {
    requiresAuth: true,      // Kimlik doğrulama gerekli
    sector: 'beauty',        // Sektör kodu
    title: 'Sayfa Başlığı',  // Sayfa başlığı
    description: '...'       // Açıklama (SEO için)
}
```

Bu bilgiler şu amaçlarla kullanılabilir:
- **Breadcrumb**: Sayfa yolu gösterimi
- **Page Title**: `document.title` ayarlama
- **SEO**: Meta tag'ler için
- **Analytics**: Sayfa izleme

---

## 🎨 Sektör Temaları

Her sektör için özel renk temaları (`useSectorTheme` composable):

### Beauty (Güzellik Merkezi)
```javascript
{
    name: 'Güzellik Merkezi',
    primaryGradient: 'linear-gradient(135deg, #ec4899, #f472b6)',
    accentColor: '#f9a8d4',
    iconColor: '#ec4899',
    glowColor: 'rgba(236, 72, 153, 0.3)',
    backgroundColor: 'rgba(236, 72, 153, 0.05)'
}
```

### Hospitality (Otel Yönetimi)
```javascript
{
    name: 'Otel Yönetimi',
    primaryGradient: 'linear-gradient(135deg, #ea580c, #0891b2)',
    accentColor: '#fb923c',
    iconColor: '#ea580c',
    glowColor: 'rgba(234, 88, 12, 0.3)',
    backgroundColor: 'rgba(234, 88, 12, 0.05)'
}
```

---

## ✅ Test Adımları

### 1. Güzellik Merkezi Test
```bash
# Giriş yap
URL: http://localhost/login
ID: BEA-000001
PIN: 1234

# Dashboard'a eriş
http://localhost/sectors/beauty/dashboard

# Alt sayfalara eriş
http://localhost/sectors/beauty/appointments
http://localhost/sectors/beauty/services
http://localhost/sectors/beauty/customers
```

### 2. Otel Yönetimi Test
```bash
# Giriş yap
URL: http://localhost/login
ID: HOS-000001
PIN: 1234

# Dashboard'a eriş
http://localhost/sectors/hospitality/dashboard

# Alt sayfalara eriş
http://localhost/sectors/hospitality/reservations
http://localhost/sectors/hospitality/rooms
http://localhost/sectors/hospitality/guests
```

---

## 📝 Sonraki Adımlar

### Önerilen Geliştirmeler

1. **Alt Sayfa Component'leri**:
   - `BeautyAppointments.vue` oluştur
   - `BeautyServices.vue` oluştur
   - `HospitalityReservations.vue` oluştur
   - `HospitalityRooms.vue` oluştur

2. **Tab Navigation**:
   - Dashboard içinde tab yapısı ile alt sayfalar
   - Smooth geçişler

3. **Breadcrumb Component**:
   - Sayfa yolu gösterimi
   - Kolay navigasyon

4. **URL Query Parameters**:
   ```javascript
   // Filtreleme için
   /sectors/beauty/appointments?date=2024-02-11&status=confirmed
   ```

5. **Route Guards**:
   - Sektöre özel yetki kontrolü
   - VIP müşteri kontrolleri

---

## 🎉 Tamamlandı!

✅ Beauty ve Hospitality route'ları başarıyla yapılandırıldı  
✅ Alt sayfalar eklendi  
✅ Meta bilgileri tanımlandı  
✅ Authentication guard aktif  
✅ Docker'da çalışıyor

**Erişim**: http://localhost
