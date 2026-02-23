<template>
  <DashboardLayout sector="ecommerce" :sector-icon="ShoppingCart">
  <div class="ecommerce-settings">
    <div class="sector-welcome">
      <span class="welcome-divider"></span>
      <p class="welcome-tagline">E-ticaret Ayarları</p>
      <span class="welcome-divider"></span>
    </div>

    <div class="settings-grid">
      <!-- Ödeme Ayarları -->
      <section class="settings-card">
        <div class="card-header">
          <h3 class="card-title">
            <CreditCard :size="20" />
            Ödeme Ayarları
          </h3>
        </div>
        <div class="settings-form">
          <div class="form-row">
            <label class="setting-label">Varsayılan Para Birimi</label>
            <select v-model="settings.currency" class="setting-input">
              <option value="TRY">TRY (₺)</option>
              <option value="USD">USD ($)</option>
              <option value="EUR">EUR (€)</option>
            </select>
          </div>
          <div class="form-row">
            <label class="setting-label">KDV Oranı (%)</label>
            <input v-model.number="settings.vatRate" type="number" class="setting-input" min="0" max="100" step="0.01" />
          </div>
          <div class="form-row toggle-row">
            <label class="setting-label">Taksit Seçeneği</label>
            <label class="toggle">
              <input v-model="settings.installmentEnabled" type="checkbox" />
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>
      </section>

      <!-- Kargo Ayarları -->
      <section class="settings-card">
        <div class="card-header">
          <h3 class="card-title">
            <Truck :size="20" />
            Kargo Ayarları
          </h3>
        </div>
        <div class="settings-form">
          <div class="form-row">
            <label class="setting-label">Ücretsiz Kargo Limiti (₺)</label>
            <input v-model.number="settings.freeShippingThreshold" type="number" class="setting-input" min="0" />
          </div>
          <div class="form-row">
            <label class="setting-label">Varsayılan Kargo Ücreti (₺)</label>
            <input v-model.number="settings.defaultShippingCost" type="number" class="setting-input" min="0" step="0.01" />
          </div>
          <div class="form-row toggle-row">
            <label class="setting-label">Hızlı Teslimat Seçeneği</label>
            <label class="toggle">
              <input v-model="settings.expressShippingEnabled" type="checkbox" />
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>
      </section>

      <!-- Bildirim Ayarları -->
      <section class="settings-card">
        <div class="card-header">
          <h3 class="card-title">
            <Bell :size="20" />
            Bildirim Ayarları
          </h3>
        </div>
        <div class="settings-form">
          <div class="form-row toggle-row">
            <label class="setting-label">Sipariş Bildirimleri</label>
            <label class="toggle">
              <input v-model="settings.orderNotifications" type="checkbox" />
              <span class="toggle-slider"></span>
            </label>
          </div>
          <div class="form-row toggle-row">
            <label class="setting-label">Düşük Stok Uyarıları</label>
            <label class="toggle">
              <input v-model="settings.lowStockAlerts" type="checkbox" />
              <span class="toggle-slider"></span>
            </label>
          </div>
          <div class="form-row">
            <label class="setting-label">Stok Uyarı Eşiği</label>
            <input v-model.number="settings.lowStockThreshold" type="number" class="setting-input" min="0" />
          </div>
        </div>
      </section>
    </div>

    <div class="settings-actions">
      <button class="btn-cancel" @click="router.push('/sectors/ecommerce/dashboard')">
        İptal
      </button>
      <button class="btn-save" @click="saveSettings">
        <Check :size="18" />
        Kaydet
      </button>
    </div>
  </div>
  </DashboardLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ShoppingCart, CreditCard, Truck, Bell, Check } from 'lucide-vue-next'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import { useNotificationStore } from '@/stores/notification'

const router = useRouter()
const notificationStore = useNotificationStore()

const settings = ref({
  currency: 'TRY',
  vatRate: 18,
  installmentEnabled: true,
  freeShippingThreshold: 299,
  defaultShippingCost: 29.99,
  expressShippingEnabled: true,
  orderNotifications: true,
  lowStockAlerts: true,
  lowStockThreshold: 5
})

const saveSettings = () => {
  notificationStore.success('Ayarlar kaydedildi', 'E-ticaret')
  router.push('/sectors/ecommerce/dashboard')
}
</script>

<style scoped>
.ecommerce-settings {
  font-family: 'Cormorant Garamond', 'Inter', serif;
  min-height: 100%;
  margin: -32px;
  padding: 32px;
  background: 
    radial-gradient(ellipse 80% 50% at 50% -10%, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
    linear-gradient(180deg, #0c0a0a 0%, #0a0808 100%);
}

.sector-welcome {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 40px;
  padding: 0 16px;
}

.welcome-divider {
  flex: 1;
  max-width: 120px;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.5), transparent);
  opacity: 0.8;
}

.welcome-tagline {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: #c4b5fd;
  margin: 0;
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.settings-card {
  background: linear-gradient(160deg, rgba(26, 22, 24, 0.9) 0%, rgba(12, 10, 10, 0.95) 100%);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(139, 92, 246, 0.12);
  border-radius: 24px;
  padding: 28px;
  transition: all 0.3s;
}

.settings-card:hover {
  border-color: rgba(139, 92, 246, 0.25);
}

.card-header {
  margin-bottom: 24px;
}

.card-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 19px;
  font-weight: 600;
  margin: 0;
  color: #fdf2f8;
  display: flex;
  align-items: center;
  gap: 10px;
}

.settings-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.toggle-row {
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}

.setting-label {
  font-size: 13px;
  font-weight: 600;
  color: rgba(253, 242, 248, 0.8);
}

.setting-input {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 12px;
  padding: 12px 16px;
  color: #fdf2f8;
  font-size: 14px;
  outline: none;
}

.setting-input:focus {
  border-color: rgba(139, 92, 246, 0.5);
}

.toggle {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 26px;
}

.toggle input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 26px;
  transition: 0.3s;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 3px;
  bottom: 3px;
  background: #6b7280;
  border-radius: 50%;
  transition: 0.3s;
}

.toggle input:checked + .toggle-slider {
  background: rgba(139, 92, 246, 0.4);
}

.toggle input:checked + .toggle-slider:before {
  transform: translateX(22px);
  background: #a78bfa;
}

.settings-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.btn-cancel {
  padding: 12px 24px;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: #9ca3af;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel:hover {
  background: rgba(255, 255, 255, 0.05);
  color: white;
}

.btn-save {
  padding: 12px 28px;
  background: linear-gradient(135deg, #8b5cf6, #a78bfa);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.35);
}

.btn-save:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(139, 92, 246, 0.45);
}

@media (max-width: 768px) {
  .ecommerce-settings {
    margin: -20px -16px;
    padding: 20px 16px;
  }
}
</style>
