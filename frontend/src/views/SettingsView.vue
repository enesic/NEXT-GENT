<template>
  <div class="settings-layout">
    <div class="header">
      <div class="title-group">
        <h2>{{ sectorStore.t('settings') }}</h2>
        <p class="subtitle">{{ sectorStore.t('settings_desc') }}</p>
      </div>
      <button class="save-btn" @click="saveAll">
        <Save :size="18" />
        {{ sectorStore.t('save_all') }}
      </button>
    </div>

    <div class="settings-grid">
      <!-- Profile Section -->
      <div class="settings-card" :style="{ animationDelay: '0.1s' }">
        <div class="card-header">
          <User :size="20" />
          <h3>{{ sectorStore.t('profile_settings') }}</h3>
        </div>
        <div class="card-body">
          <div class="input-group">
            <label>{{ sectorStore.t('full_name') }}</label>
            <input type="text" v-model="settings.profile.fullName" />
          </div>
          <div class="input-group">
            <label>{{ sectorStore.t('email_address') }}</label>
            <input type="email" :value="settings.profile.email" disabled />
          </div>
          <div class="input-group">
            <label>{{ sectorStore.t('phone') }}</label>
            <input type="tel" v-model="settings.profile.phone" />
          </div>
        </div>
      </div>

      <!-- Theme Section -->
      <div class="settings-card" :style="{ animationDelay: '0.2s' }">
        <div class="card-header">
          <Palette :size="20" />
          <h3>{{ sectorStore.t('appearance') }}</h3>
        </div>
        <div class="card-body">
          <div class="toggle-group" @click="toggle('appearance', 'darkMode')">
            <div class="toggle-info">
              <label>{{ sectorStore.t('dark_mode') }}</label>
              <p>{{ sectorStore.t('dark_mode_desc') }}</p>
            </div>
            <div class="toggle" :class="{ active: settings.appearance.darkMode }"></div>
          </div>
          <div class="toggle-group" @click="toggle('appearance', 'highContrast')">
            <div class="toggle-info">
              <label>{{ sectorStore.t('high_contrast') }}</label>
              <p>{{ sectorStore.t('high_contrast_desc') }}</p>
            </div>
            <div class="toggle" :class="{ active: settings.appearance.highContrast }"></div>
          </div>
          <div class="toggle-group" @click="toggle('appearance', 'compactView')">
            <div class="toggle-info">
              <label>{{ sectorStore.t('compact_view') }}</label>
              <p>{{ sectorStore.t('compact_view_desc') }}</p>
            </div>
            <div class="toggle" :class="{ active: settings.appearance.compactView }"></div>
          </div>
        </div>
      </div>

      <!-- Notifications -->
      <div class="settings-card" :style="{ animationDelay: '0.3s' }">
        <div class="card-header">
          <Bell :size="20" />
          <h3>{{ sectorStore.t('notifications') }}</h3>
        </div>
        <div class="card-body">
          <div class="toggle-group" @click="toggle('notifications', 'email')">
            <div class="toggle-info">
              <label>{{ sectorStore.t('email_notif') }}</label>
              <p>{{ sectorStore.t('email_notif_desc') }}</p>
            </div>
            <div class="toggle" :class="{ active: settings.notifications.email }"></div>
          </div>
          <div class="toggle-group" @click="toggle('notifications', 'sms')">
            <div class="toggle-info">
              <label>{{ sectorStore.t('sms_notif') }}</label>
              <p>{{ sectorStore.t('sms_notif_desc') }}</p>
            </div>
            <div class="toggle" :class="{ active: settings.notifications.sms }"></div>
          </div>
        </div>
      </div>

      <!-- Security -->
      <div class="settings-card" :style="{ animationDelay: '0.4s' }">
        <div class="card-header">
          <ShieldCheck :size="20" />
          <h3>{{ sectorStore.t('security_settings') }}</h3>
        </div>
        <div class="card-body">
          <div class="action-row">
            <div class="action-info">
              <label>{{ sectorStore.t('two_factor') }}</label>
              <p>{{ sectorStore.t('two_factor_desc') }}</p>
            </div>
            <button class="outline-btn" @click="openModal('2fa')">{{ sectorStore.t('enable') }}</button>
          </div>
          <div class="action-row">
            <div class="action-info">
              <label>{{ sectorStore.t('password_update') }}</label>
              <p>{{ sectorStore.t('password_desc') }}</p>
            </div>
            <button class="outline-btn" @click="openModal('password')">{{ sectorStore.t('change') }}</button>
          </div>
          <div class="action-row">
            <div class="action-info">
              <label>{{ sectorStore.t('account_recovery') }}</label>
              <p>{{ sectorStore.t('account_recovery_desc') }}</p>
            </div>
            <button class="outline-btn" @click="openModal('recovery')">{{ sectorStore.t('configure') }}</button>
          </div>
        </div>
      </div>

      <!-- Privacy & Data -->
      <div class="settings-card" :style="{ animationDelay: '0.5s' }">
        <div class="card-header">
          <Eye :size="20" />
          <h3>{{ sectorStore.t('privacy_data') }}</h3>
        </div>
        <div class="card-body">
          <div class="toggle-group" @click="toggle('privacy', 'dataPersonalization')">
            <div class="toggle-info">
              <label>{{ sectorStore.t('data_personalization') }}</label>
              <p>{{ sectorStore.t('data_pers_desc') }}</p>
            </div>
            <div class="toggle" :class="{ active: settings.privacy.dataPersonalization }"></div>
          </div>
          <div class="action-row">
            <div class="action-info">
              <label>{{ sectorStore.t('download_data') }}</label>
              <p>{{ sectorStore.t('download_data_desc') }}</p>
            </div>
            <button class="outline-btn" @click="downloadData">{{ sectorStore.t('download') }}</button>
          </div>
        </div>
      </div>

      <!-- Storage Management -->
      <div class="settings-card" :style="{ animationDelay: '0.6s' }">
        <div class="card-header">
          <HardDrive :size="20" />
          <h3>{{ sectorStore.t('storage') }}</h3>
        </div>
        <div class="card-body">
          <div class="storage-usage">
            <div class="usage-stats">
              <span>{{ sectorStore.t('used_storage') }}</span>
              <span class="usage-pct">%65</span>
            </div>
            <div class="usage-bar">
              <div class="bar-fill" style="width: 65%"></div>
            </div>
            <p class="usage-hint">En çok yer kaplayan: PDF Belgeler (%42)</p>
          </div>
          <button class="outline-btn full-width" @click="openModal('billing')">{{ sectorStore.t('upgrade_plan') }}</button>
        </div>
      </div>

      <!-- Connected Apps -->
      <div class="settings-card" :style="{ animationDelay: '0.7s' }">
        <div class="card-header">
          <Link :size="20" />
          <h3>{{ sectorStore.t('connected_apps') }}</h3>
        </div>
        <div class="card-body">
          <div class="app-item">
            <div class="app-icon google">G</div>
            <div class="app-text">
                <label>Google Drive</label>
                <p>Dosyaları otomatik yedekle</p>
            </div>
            <span class="status-badge connected">{{ sectorStore.t('connected') }}</span>
          </div>
          <div class="app-item">
            <div class="app-icon slack">S</div>
            <div class="app-text">
                <label>Slack</label>
                <p>Bildirimleri kanala gönder</p>
            </div>
            <button v-if="!settings.apps.slackConnected" class="link-btn" @click="openModal('slack')">{{ sectorStore.t('connect') }}</button>
            <span v-else class="status-badge connected">{{ sectorStore.t('connected') }}</span>
          </div>
        </div>
      </div>

      <!-- Billing Overview -->
      <div class="settings-card" :style="{ animationDelay: '0.8s' }">
        <div class="card-header">
          <CreditCard :size="20" />
          <h3>{{ sectorStore.t('billing') }}</h3>
        </div>
        <div class="card-body">
          <div class="billing-card-preview">
            <div class="card-brand">VISA</div>
            <div class="card-number">**** **** **** 4242</div>
            <div class="card-exp">12/26</div>
          </div>
          <div class="action-row">
            <div class="action-info">
                <label>{{ sectorStore.t('current_plan') }}</label>
                <p>Kurumsal Pro Plus</p>
            </div>
            <span class="price-tag">49$/Ay</span>
          </div>
        </div>
      </div>

      <!-- Localization -->
      <div class="settings-card" :style="{ animationDelay: '0.9s' }">
        <div class="card-header">
          <Globe :size="20" />
          <h3>{{ sectorStore.t('lang_region') }}</h3>
        </div>
        <div class="card-body">
          <div class="input-group">
            <label>{{ sectorStore.t('interface_lang') }}</label>
            <select class="premium-select" v-model="settings.localization.language">
              <option value="tr">Türkçe</option>
              <option value="en">English</option>
              <option value="de">Deutsch</option>
            </select>
          </div>
          <div class="input-group">
            <label>{{ sectorStore.t('timezone') }}</label>
            <select class="premium-select" v-model="settings.localization.timezone">
              <option value="europe/istanbul">İstanbul (GMT+3)</option>
              <option value="europe/london">London (GMT+0)</option>
              <option value="america/new_york">New York (GMT-5)</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Advanced -->
      <div class="settings-card" :style="{ animationDelay: '0.6s' }">
        <div class="card-header">
          <Cpu :size="20" />
          <h3>{{ sectorStore.t('advanced') }}</h3>
        </div>
        <div class="card-body">
          <div class="toggle-group" @click="toggle('privacy', 'betaFeatures')">
            <div class="toggle-info">
              <label>{{ sectorStore.t('beta_features') }}</label>
              <p>{{ sectorStore.t('beta_desc') }}</p>
            </div>
            <div class="toggle" :class="{ active: settings.privacy.betaFeatures }"></div>
          </div>
          <div class="toggle-group" @click="toggle('privacy', 'analyticsSharing')">
            <div class="toggle-info">
              <label>{{ sectorStore.t('analytics_sharing') }}</label>
              <p>{{ sectorStore.t('analytics_desc') }}</p>
            </div>
            <div class="toggle" :class="{ active: settings.privacy.analyticsSharing }"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Ayarlar Modali -->
    <Transition name="modal-fade">
      <div v-if="activeModal" class="modal-overlay" @click.self="activeModal = null">
        <div class="modal-container" :style="{ '--accent': sectorStore.theme?.primary || '#6366f1' }">
          <div class="modal-header">
            <div class="modal-title-group">
              <div class="modal-icon">
                <component :is="activeModalData.icon" :size="20" />
              </div>
              <h2>{{ activeModalData.title }}</h2>
            </div>
            <button class="close-btn" @click="activeModal = null">
              <X :size="20" />
            </button>
          </div>
          
          <div class="modal-body">
            <template v-if="activeModal === 'password'">
              <div class="input-group">
                <label>Mevcut Şifre</label>
                <input type="password" placeholder="••••••••" />
              </div>
              <div class="input-group">
                <label>Yeni Şifre</label>
                <input type="password" placeholder="••••••••" />
              </div>
              <div class="input-group">
                <label>Yeni Şifre (Tekrar)</label>
                <input type="password" placeholder="••••••••" />
              </div>
            </template>
            
            <template v-else-if="activeModal === '2fa'">
              <p class="modal-desc">Hesabınızı güvence altına almak için Authenticator uygulamanızla aşağıdaki kodu girin.</p>
              <div class="input-group">
                <label>Doğrulama Kodu</label>
                <input type="text" placeholder="123 456" style="text-align: center; font-size: 20px; letter-spacing: 4px;" />
              </div>
            </template>
            
            <template v-else-if="activeModal === 'recovery'">
              <div class="input-group">
                <label>Yedek E-posta Adresi</label>
                <input type="email" placeholder="backup@example.com" />
              </div>
              <div class="input-group">
                <label>Kurtarma Telefonu</label>
                <input type="tel" placeholder="+90 5XX XXX XX XX" />
              </div>
            </template>
            
            <template v-else-if="activeModal === 'billing'">
              <div class="billing-preview">
                <div class="billing-plan active">
                  <h4>Kurumsal Pro Plus</h4>
                  <span class="price">49$/Ay</span>
                  <ul>
                    <li>✓ Sınırsız Randevu</li>
                    <li>✓ 50 GB Bulut Alanı</li>
                    <li>✓ Öncelikli Destek</li>
                  </ul>
                </div>
                <div class="billing-plan upgrade">
                  <h4>Sınırsız Enterprise</h4>
                  <span class="price">99$/Ay</span>
                  <ul>
                    <li>✓ Sınırsız Kullanıcı</li>
                    <li>✓ 500 GB Bulut Alanı</li>
                    <li>✓ Özel Müşteri Temsilcisi</li>
                  </ul>
                </div>
              </div>
            </template>

            <template v-else-if="activeModal === 'slack'">
              <p class="modal-desc">Workspace bilginizi girerek bildirimleri Slack'e bağlayabilirsiniz.</p>
              <div class="input-group">
                <label>Slack Webhook URL</label>
                <input type="url" placeholder="https://hooks.slack.com/services/..." />
              </div>
            </template>
          </div>
          
          <div class="modal-footer">
            <button class="btn-cancel" @click="activeModal = null">İptal</button>
            <button class="btn-submit" @click="submitModal">Kaydet</button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { 
  User, Palette, Bell, ShieldCheck, Globe, Cpu, Eye, 
  HardDrive, Link, CreditCard, Save, Download, Shield,
  Lock, RefreshCw, Smartphone, Key
} from 'lucide-vue-next'
import { useSectorStore } from '../stores/sector'
import { useNotificationStore } from '../stores/notification'
import { useAuthStore } from '../stores/auth'

const sectorStore = useSectorStore()
const notificationStore = useNotificationStore()
const authStore = useAuthStore()

// 1. Reactive State
const settings = reactive({
  profile: {
    fullName: authStore.user?.name || 'Ahmet Yılmaz',
    email: authStore.user?.email || 'info@nextgent.co',
    phone: '+90 555 123 4567'
  },
  appearance: {
    darkMode: true,
    highContrast: false,
    compactView: false
  },
  notifications: {
    email: true,
    sms: true,
    push: false
  },
  privacy: {
    dataPersonalization: true,
    betaFeatures: false,
    analyticsSharing: true
  },
  localization: {
    language: 'tr',
    timezone: 'europe/istanbul'
  },
  apps: {
    slackConnected: false
  }
})

// 1.5. Modal State
const activeModal = ref(null)
const activeModalData = ref({
  title: '',
  icon: 'Settings'
})

const getModalConfig = (modalType) => {
  const configs = {
    password: { title: 'Şifre Değiştir', icon: 'Key' },
    '2fa': { title: 'İki Faktörlü Doğrulama', icon: 'ShieldCheck' },
    recovery: { title: 'Hesap Kurtarma Ayarları', icon: 'RefreshCw' },
    billing: { title: 'Paket Yükseltme', icon: 'CreditCard' },
    slack: { title: 'Slack Entegrasyonu', icon: 'Link' }
  }
  return configs[modalType] || { title: 'Ayarlar', icon: 'Settings' }
}

const openModal = (modalType) => {
  activeModalData.value = getModalConfig(modalType)
  activeModal.value = modalType
}

const submitModal = () => {
  if (activeModal.value === 'slack') {
    settings.apps.slackConnected = true
    notificationStore.success('Slack başarıyla bağlandı!', 'Entegrasyon')
  } else if (activeModal.value === 'billing') {
    notificationStore.success('Yeni pakete geçiş işleminiz alındı.', 'Ödeme')
  } else {
    notificationStore.success(`${activeModalData.value.title} işleminiz kaydedildi.`, 'Başarılı')
  }
  // save globally
  saveAll()
  activeModal.value = null
}

// 2. Load from LocalStorage on mount
const applyAppearance = (appearance) => {
    document.body.classList.toggle('light-mode', !appearance.darkMode)
    document.body.classList.toggle('high-contrast', !!appearance.highContrast)
    document.body.classList.toggle('compact-view', !!appearance.compactView)
}

onMounted(() => {
    const savedSettings = localStorage.getItem('user_settings')
    if (savedSettings) {
        try {
            const parsed = JSON.parse(savedSettings)
            // Deep merge nested objects instead of shallow Object.assign
            if (parsed.profile)      Object.assign(settings.profile, parsed.profile)
            if (parsed.appearance)   Object.assign(settings.appearance, parsed.appearance)
            if (parsed.notifications) Object.assign(settings.notifications, parsed.notifications)
            if (parsed.privacy)      Object.assign(settings.privacy, parsed.privacy)
            if (parsed.localization) Object.assign(settings.localization, parsed.localization)
            if (parsed.apps)         Object.assign(settings.apps, parsed.apps)
            // Re-apply appearance immediately after loading
            applyAppearance(settings.appearance)
        } catch (e) {
            console.error('Failed to parse settings:', e)
        }
    }
})

// 3. Auto-save preference (optional, but good for UX)
watch(settings, (newSettings) => {
  localStorage.setItem('user_settings', JSON.stringify(newSettings))
}, { deep: true })

// 4. Watch for Visual Changes and apply to Body
watch(() => settings.appearance.darkMode, (isDark) => {
  document.body.classList.toggle('light-mode', !isDark)
}, { immediate: true })

watch(() => settings.appearance.highContrast, (isHigh) => {
  document.body.classList.toggle('high-contrast', isHigh)
}, { immediate: true })

watch(() => settings.appearance.compactView, (isCompact) => {
  document.body.classList.toggle('compact-view', isCompact)
}, { immediate: true })

// 5. Watch for Locale Change
watch(() => settings.localization.language, (newLang) => {
  sectorStore.setLocale(newLang)
})

// 6. Action Handlers
const saveAll = () => {
    localStorage.setItem('user_settings', JSON.stringify(settings))
    applyAppearance(settings.appearance)
    notificationStore.success('Ayarlarınız başarıyla kaydedildi.', 'Güncellendi')
}

const toggle = (category, key) => {
  settings[category][key] = !settings[category][key]
}

const handleAction = (title, message = 'Bu işlem başarıyla başlatıldı.') => {
  notificationStore.info(message, title)
}

const downloadData = () => {
  const dataToExport = {
    settings,
    exportedAt: new Date().toISOString(),
    user: authStore.user
  }
  const data = JSON.stringify(dataToExport, null, 2)
  const blob = new Blob([data], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `nextgent-account-data-${new Date().toISOString().split('T')[0]}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  notificationStore.success('Hesap verileriniz dışa aktarıldı.', 'Veri İndirme')
}

const toggleApp = (app) => {
  handleAction(`${app} Bağlantısı`, `${app} bağlantı ayarları güncelleniyor...`)
}
</script>

<style scoped>
.settings-layout {
  display: flex;
  flex-direction: column;
  gap: 32px;
  color: var(--text-primary);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.title-group h2 {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 4px;
}

.subtitle {
  color: var(--text-secondary);
  font-size: 14px;
}

.save-btn {
  background: var(--current-accent);
  color: white;
  border: none;
  padding: 0 24px;
  height: 44px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 12px var(--current-glow);
  display: flex;
  align-items: center;
  gap: 8px;
}

.save-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px var(--current-glow-strong);
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.settings-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  padding: 0;
  overflow: hidden;
  transition: all 0.3s;
  animation: appear 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
}

.settings-card:hover {
  border-color: var(--current-accent);
  box-shadow: 0 12px 24px -12px var(--current-glow-strong);
}

.card-header {
  padding: 20px 24px;
  background: rgba(255, 255, 255, 0.02);
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--current-accent);
}

.card-header h3 {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: var(--text-primary);
}

.card-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-group label {
  font-size: 12px;
  color: var(--text-muted);
}

.input-group input {
  background: var(--bg-sidebar);
  border: 1px solid var(--border-subtle);
  padding: 12px 16px;
  border-radius: 10px;
  color: var(--text-primary);
  transition: all 0.3s;
}

.input-group input:focus {
  outline: none;
  border-color: var(--current-accent);
  box-shadow: 0 0 0 2px var(--current-glow);
}

.input-group input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: var(--surface-hover);
}

.input-group select {
  background: var(--bg-sidebar);
  border: 1px solid var(--border-subtle);
  padding: 12px 16px;
  border-radius: 10px;
  color: var(--text-primary);
  transition: all 0.3s;
  cursor: pointer;
}

.input-group select:focus {
  outline: none;
  border-color: var(--current-accent);
  box-shadow: 0 0 0 2px var(--current-glow);
}

.premium-select option {
  background: var(--surface-elevated);
  padding: 10px;
}

.toggle-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.toggle-info label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 2px;
}

.toggle-info p {
  font-size: 12px;
  color: var(--text-muted);
}

.toggle {
  width: 44px;
  height: 24px;
  background: var(--bg-main);
  border: 1px solid var(--border-subtle);
  border-radius: 99px;
  position: relative;
  cursor: pointer;
  transition: all 0.3s;
}

.toggle::after {
  content: '';
  position: absolute;
  left: 3px;
  top: 3px;
  width: 16px;
  height: 16px;
  background: var(--text-muted);
  border-radius: 50%;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.toggle.active {
  background: var(--current-accent);
  border-color: var(--current-accent);
}

.toggle.active::after {
  transform: translateX(18px);
  background: white;
}

.action-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.action-info label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 2px;
}

.action-info p {
  font-size: 12px;
  color: var(--text-muted);
}

.outline-btn {
  background: transparent;
  border: 1px solid var(--border-subtle);
  color: var(--text-primary);
  padding: 8px 16px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.outline-btn:hover {
  border-color: var(--current-accent);
  color: var(--current-accent);
  background: var(--current-glow);
}

.outline-btn.full-width {
    width: 100%;
}

/* Storage Usage */
.storage-usage {
    margin-bottom: 8px;
}

.usage-stats {
    display: flex;
    justify-content: space-between;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 10px;
}

.usage-pct {
    color: var(--current-accent);
}

.usage-bar {
    height: 8px;
    background: var(--bg-main);
    border-radius: 4px;
    margin-bottom: 8px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    background: var(--current-accent);
    box-shadow: 0 0 10px var(--current-glow);
}

.usage-hint {
    font-size: 11px;
    color: var(--text-muted);
}

/* App Item */
.app-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 12px;
    background: var(--bg-main);
    border-radius: 12px;
    border: 1px solid var(--border-subtle);
}

.app-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 18px;
}

.app-icon.google { background: #4285F4; color: white; }
.app-icon.slack { background: #4A154B; color: white; }

.app-text {
    flex: 1;
}

.app-text label {
    display: block;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 2px;
}

.app-text p {
    font-size: 11px;
    color: var(--text-muted);
}

.status-badge.connected {
    font-size: 10px;
    font-weight: 700;
    color: #22c55e;
    background: rgba(34, 197, 94, 0.1);
    padding: 4px 8px;
    border-radius: 6px;
}

.link-btn {
    background: transparent;
    border: none;
    color: var(--current-accent);
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
}

/* Billing Card */
.billing-card-preview {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 12px;
}

.card-brand {
    font-weight: 800;
    font-style: italic;
    font-size: 18px;
    color: white;
}

.card-number {
    font-family: monospace;
    font-size: 18px;
    letter-spacing: 2px;
    color: white;
    opacity: 0.9;
}

.card-exp {
    font-size: 12px;
    color: white;
    opacity: 0.6;
}

.price-tag {
    font-size: 16px;
    font-weight: 700;
    color: var(--current-accent);
}

/* Settings Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-container {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 24px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.4);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 24px;
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.02);
}

.modal-title-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.modal-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: var(--current-glow);
  color: var(--current-accent);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-title-group h2 {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.close-btn {
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: all 0.2s;
}

.close-btn:hover {
  background: var(--surface-hover);
  color: var(--text-primary);
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.modal-desc {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.5;
  margin: 0;
}

.modal-footer {
  padding: 20px 24px;
  border-top: 1px solid var(--border-subtle);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  background: rgba(0, 0, 0, 0.2);
}

.btn-cancel {
  padding: 10px 20px;
  border: 1px solid var(--border-subtle);
  background: transparent;
  color: var(--text-primary);
  border-radius: 10px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel:hover {
  background: var(--surface-hover);
}

.btn-submit {
  padding: 10px 24px;
  border: none;
  background: var(--current-accent);
  color: white;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 12px var(--current-glow);
}

.btn-submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px var(--current-glow-strong);
}

.billing-preview {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.billing-plan {
  padding: 20px;
  border-radius: 16px;
  border: 1px solid var(--border-subtle);
  background: var(--surface-hover);
  position: relative;
  transition: all 0.2s;
}

.billing-plan.active {
  border-color: var(--current-accent);
  background: var(--current-glow);
}

.billing-plan.active::after {
  content: 'Mevcut';
  position: absolute;
  top: 16px;
  right: 16px;
  font-size: 11px;
  font-weight: 700;
  background: var(--current-accent);
  color: white;
  padding: 4px 8px;
  border-radius: 6px;
}

.billing-plan h4 {
  margin: 0 0 8px 0;
  color: var(--text-primary);
  font-size: 16px;
}

.billing-plan .price {
  font-size: 24px;
  font-weight: 700;
  color: white;
  display: block;
  margin-bottom: 16px;
}

.billing-plan ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.billing-plan li {
  font-size: 13px;
  color: var(--text-secondary);
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-active .modal-container,
.modal-fade-leave-active .modal-container {
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-fade-enter-from .modal-container,
.modal-fade-leave-to .modal-container {
  transform: scale(0.95) translateY(20px);
}

@keyframes appear {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
