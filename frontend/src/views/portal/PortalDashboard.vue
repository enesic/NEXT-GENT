<template>
  <div class="portal-dashboard">
    <div class="welcome-section">
      <h1>{{ t('welcome_message') }}</h1>
      <p class="subtitle">{{ t('dashboard_subtitle') }}</p>
    </div>

    <!-- MAIN DRAFT: 4-Column Stats Grid (Medical Style) -->
    <div class="stats-grid">
      <div 
        v-for="(stat, index) in displayStats" 
        :key="index"
        class="stat-card"
        :style="{ borderTop: `4px solid ${getColor(stat.color)}` }"
      >
        <div class="stat-header">
            <span class="stat-label">{{ stat.label }}</span>
            <div class="stat-icon" :style="{ color: getColor(stat.color), background: getGlowColor(stat.color) }">
                <component :is="sectorStore.getIcon(stat.icon)" :size="20" />
            </div>
        </div>
        <div class="stat-body">
            <span class="stat-value" >{{ stat.value }}</span>
            <span v-if="stat.change" class="stat-change" :class="stat.change > 0 ? 'positive' : 'negative'">
              {{ stat.change > 0 ? '↑' : '↓' }} {{ Math.abs(stat.change) }}%
            </span>
        </div>
      </div>
    </div>

    <div class="dashboard-grid">
        <!-- MAIN DRAFT: Large Chart Section -->
        <div class="chart-section glass-panel">
            <div class="section-header">
                <h3 >{{ chartConfig?.title || 'Hasta Trafiği' }}</h3>
                <span class="section-subtitle">{{ chartConfig?.subtitle || 'Yıllık Veriler' }}</span>
            </div>
             <LuxuryChart 
                v-if="chartConfig"
                :title="''" 
                :type="'area'"
                :series="chartConfig.datasets"
                :categories="chartConfig.labels"
                :height="350"
                :color="colors.primary"
                :details="{}"
              />
        </div>

        <!-- MAIN DRAFT: Right Side Quick Actions -->
        <div class="side-panel">
            <div class="quick-actions-card">
                <h3 >Hızlı İşlemler</h3>
                <div class="actions-list">
                    <button 
                        v-for="(action, index) in displayActions" 
                        :key="index"
                        class="action-btn"
                        :style="{ '--hover-color': colors.primary }"
                        @click="handleActionClick(action)"
                    >
                        <div class="action-icon" :style="{ background: getGlowColor('primary'), color: colors.primary }">
                             <component :is="sectorStore.getIcon(action.icon)" :size="18" />
                        </div>
                        <span>{{ action.label }}</span>
                        <div class="post-icon">→</div>
                    </button>
                </div>
            </div>

            <!-- MAIN DRAFT: Recent Activity Widget -->
             <div class="activity-card">
                <h3 >Son Aktiviteler</h3>
                <div class="activity-list">
                    <div v-for="i in 3" :key="i" class="activity-row">
                        <div class="dot" :style="{ background: i === 1 ? colors.primary : colors.secondary }"></div>
                        <div class="activity-text">
                            <strong >{{ getDummyActivity(i).title }}</strong>
                            <span class="time">2 saat önce</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Quick Entry Overlay Panel -->
    <Transition name="fade">
      <div v-if="showQuickEntry" class="quick-entry-overlay" @click.self="closeQuickEntry">
        <div class="quick-entry-panel glass-panel">
          <div class="panel-header">
            <h3>{{ entryType === 'appointment' ? 'Hızlı Randevu Ekle' : 'Hızlı Müşteri Kaydı' }}</h3>
            <button class="close-btn" @click="closeQuickEntry">×</button>
          </div>
          
          <div class="panel-body">
            <template v-if="entryType === 'appointment'">
              <div class="form-group">
                <label>Müşteri Adı</label>
                <input v-model="formData.client_name" type="text" placeholder="Ad Soyad" />
              </div>
              <div class="form-group">
                <label>Email</label>
                <input v-model="formData.client_email" type="email" placeholder="ornek@mail.com" />
              </div>
              <div class="form-group">
                <label>Başlık</label>
                <input v-model="formData.title" type="text" placeholder="Randevu Başlığı" />
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label>Başlangıç</label>
                  <input v-model="formData.start_time" type="datetime-local" />
                </div>
                <div class="form-group">
                  <label>Bitiş</label>
                  <input v-model="formData.end_time" type="datetime-local" />
                </div>
              </div>
            </template>

            <template v-else>
              <div class="form-group">
                <label>Ad</label>
                <input v-model="formData.first_name" type="text" placeholder="Ad" />
              </div>
              <div class="form-group">
                <label>Soyad</label>
                <input v-model="formData.last_name" type="text" placeholder="Soyad" />
              </div>
              <div class="form-group">
                <label>Email</label>
                <input v-model="formData.email" type="email" placeholder="ornek@mail.com" />
              </div>
              <div class="form-group">
                <label>Telefon</label>
                <input v-model="formData.phone" type="tel" placeholder="05xx..." />
              </div>
            </template>

            <div v-if="submitError" class="error-msg">{{ submitError }}</div>
          </div>

          <div class="panel-footer">
            <button class="cancel-btn" @click="closeQuickEntry">İptal</button>
            <button class="save-btn" :disabled="submitting" @click="saveEntry">
              {{ submitting ? 'Kaydediliyor...' : 'Kaydet' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, inject, onMounted } from 'vue'
import { useSectorStore } from '../../stores/sector'
import LuxuryChart from '../../components/LuxuryChart.vue'
import dashboardAPI from '../../config/dashboardAPI'

const emit = defineEmits(['navigate'])
const sectorStore = useSectorStore()

// Data state
const loading = ref(true)
const error = ref(null)
const stats = ref([])
const satisfactionData = ref(null)
const quickStatsData = ref(null)

// Quick Entry State
const showQuickEntry = ref(false)
const entryType = ref('appointment') // 'appointment' or 'customer'
const submitting = ref(false)
const submitError = ref(null)
const formData = ref({})

const resetForm = () => {
    formData.value = {
        client_name: '',
        client_email: '',
        title: '',
        start_time: '',
        end_time: '',
        first_name: '',
        last_name: '',
        email: '',
        phone: ''
    }
    submitError.value = null
}

const closeQuickEntry = () => {
    showQuickEntry.value = false
    resetForm()
}

// Dynamic Theme Colors
const colors = computed(() => sectorStore.theme || {
    primary: '#0ea5e9',
    secondary: '#0f766e',
    accent: '#38bdf8',
    text: '#0f172a'
})

// Translation Helper
const t = (key) => {
    if (sectorStore.t) return sectorStore.t(key)
    return key
}

// Helpers
const getColor = (colorName) => {
    const themeColors = sectorStore.theme || {}
    return themeColors[colorName] || themeColors.primary || '#0ea5e9'
}

const getGlowColor = (colorName) => {
    return getColor(colorName) + '1A' // 10% opacity
}

// DEFAULT MEDICAL DATA (Fallback)
const defaultStats = [
    { label: 'Bugünkü Randevular', value: '124', change: 5.2, icon: 'Calendar', color: 'primary' },
    { label: 'Aktif Hastalar', value: '1,284', change: 2.1, icon: 'Users', color: 'accent' },
    { label: 'Acil Durumlar', value: '3', change: -10.5, icon: 'AlertCircle', color: 'red' },
    { label: 'Memnuniyet', value: '98%', change: 1.2, icon: 'Heart', color: 'secondary' }
]

const defaultActions = [
    { label: 'Randevu Ekle', icon: 'CalendarPlus' },
    { label: 'Hasta Kaydı', icon: 'UserPlus' },
    { label: 'Reçete Yaz', icon: 'FileText' },
    { label: 'Lab Sonuçları', icon: 'Activity' }
]

// Fetch dashboard data from API
const fetchDashboardData = async () => {
    try {
        loading.value = true
        error.value = null

        // Fetch data in parallel
        const [kpis, satisfaction, quickStats] = await Promise.all([
            dashboardAPI.getSectoralKPIs().catch(() => null),
            dashboardAPI.getSatisfactionMetrics(30).catch(() => null),
            dashboardAPI.getQuickStats(30).catch(() => null)
        ])

        console.log('✅ Dashboard data loaded:', { kpis, satisfaction, quickStats })

        // Guard: if API returns HTML string instead of JSON, skip it
        const isValidJSON = (data) => data && typeof data !== 'string' && !String(data).startsWith('<!DOCTYPE')

        // Map KPIs to stat cards format
        if (isValidJSON(kpis) && Array.isArray(kpis)) {
            stats.value = kpis.map((kpi, index) => ({
                label: kpi.label,
                value: kpi.value,
                change: parseFloat(kpi.trend) || 0,
                icon: getIconForKPI(index),
                color: kpi.positive ? 'primary' : 'red',
                description: kpi.description
            }))
        } else if (kpis && typeof kpis === 'string') {
            console.warn('⚠️ KPIs returned HTML instead of JSON, using defaults')
        }

        satisfactionData.value = isValidJSON(satisfaction) ? satisfaction : null
        quickStatsData.value = isValidJSON(quickStats) ? quickStats : null

    } catch (err) {
        console.error('❌ Error fetching dashboard data:', err)
        error.value = err.message || 'Veri yüklenirken hata oluştu'
        // Fallback to default data on error
        stats.value = []
    } finally {
        loading.value = false
    }
}

// Get appropriate icon for KPI based on index
const getIconForKPI = (index) => {
    const icons = ['TrendingUp', 'Users', 'AlertCircle', 'Heart', 'Activity', 'CheckCircle']
    return icons[index] || 'BarChart'
}

// OnMounted - Fetch data when component loads
onMounted(() => {
    fetchDashboardData()
})

// Computed Display Data (Merges Defaults if Sector Data Missing)
const displayStats = computed(() => {
    // Priority: 1. API data, 2. Sector store data, 3. Default fallback
    if (stats.value && stats.value.length > 0) {
        return stats.value
    }
    
    if (sectorStore.stats && sectorStore.stats.length > 0) {
        return sectorStore.stats
    }
    
    return defaultStats
})

const displayActions = computed(() => {
    return (sectorStore.quickActions && sectorStore.quickActions.length > 0) ? sectorStore.quickActions : defaultActions
})

const chartConfig = computed(() => sectorStore.chartConfig || {
    title: 'Hasta Trafiği',
    subtitle: 'Haftalık Veriler',
    datasets: [{ name: 'Hasta', data: [30, 40, 35, 50, 49, 60, 70, 91, 125] }],
    labels: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999]
})

const getDummyActivity = (i) => {
    const sector = sectorStore.currentSector || 'medical'
    const messages = {
        medical: ['Yeni randevu oluşturuldu', 'Lab sonuçları onaylandı', 'Acil servis girişi'],
        legal: ['Dava dosyası güncellendi', 'Müvekkil araması', 'Duruşma hatırlatması'],
        technology: ['Server yedeklemesi tamamlandı', 'Yeni deployment', 'CPU kullanımı arttı'],
        finance: ['Para transferi geldi', 'Fatura kesildi', 'Kur güncellemesi'],
        real_estate: ['Yeni ilan yayında', 'Müşteri randevusu', 'Tapu işlemleri başlatıldı']
    }
    return { title: (messages[sector] || messages.medical)[i-1] || 'İşlem tamamlandı' }
}

// Button click handler - navigate via parent shell
const handleActionClick = (action) => {
    if (action.label === 'Randevu Ekle') {
        entryType.value = 'appointment'
        resetForm()
        showQuickEntry.value = true
        return
    }
    if (action.label === 'Hasta Kaydı' || action.label === 'Müşteri Kaydı') {
        entryType.value = 'customer'
        resetForm()
        showQuickEntry.value = true
        return
    }
    
    // Use nav property from sectorThemes quickActions
    const target = action.nav || 'dashboard'
    emit('navigate', target)
}

const saveEntry = async () => {
    try {
        submitting.value = true
        submitError.value = null
        
        let endpoint = entryType.value === 'appointment' ? '/portal/appointments' : '/portal/customers'
        
        // Basic validation
        if (entryType.value === 'appointment') {
            if (!formData.value.client_name || !formData.value.start_time || !formData.value.end_time) {
                throw new Error('Lütfen zorunlu alanları doldurun.')
            }
        } else {
            if (!formData.value.first_name || !formData.value.last_name || !formData.value.phone || !formData.value.email) {
                throw new Error('Lütfen zorunlu alanları doldurun.')
            }
        }

        const axios = inject('axios')
        const response = await axios.post(endpoint, formData.value)
        
        if (response.data.status === 'success') {
            closeQuickEntry()
            // Optional: trigger a success message or refresh
            fetchDashboardData()
        }
    } catch (err) {
        console.error('Save error:', err)
        submitError.value = err.response?.data?.detail || err.message || 'Kayıt sırasında bir hata oluştu.'
    } finally {
        submitting.value = false
    }
}

</script>

<style scoped>
.portal-dashboard {
  padding: 32px;
  width: 100%;
  margin: 0;
  box-sizing: border-box;
}

.welcome-section {
  margin-bottom: 32px;
}

.welcome-section h1 {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 4px;
}

.subtitle {
  color: var(--text-secondary);
  font-size: 14px;
}

/* Stats Grid - Fixed 4 Cols */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: var(--surface-elevated);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  transition: transform 0.2s;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 140px;
}

.stat-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.stat-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}

.stat-label {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-secondary);
}

.stat-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.stat-body {
    margin-top: auto;
}

.stat-value {
    font-size: 28px;
    font-weight: 700;
    display: block;
}

.stat-change {
    font-size: 12px;
    font-weight: 600;
    margin-top: 4px;
    display: inline-block;
}

.stat-change.positive { color: #10b981; }
.stat-change.negative { color: #ef4444; }

/* Dashboard Grid */
.dashboard-grid {
    display: grid;
    grid-template-columns: 3fr 1fr;
    gap: 24px;
}

/* Chart Section */
.chart-section {
    background: var(--surface-elevated);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.section-header {
    margin-bottom: 20px;
}

.section-header h3 {
    font-size: 18px;
    font-weight: 600;
    margin: 0;
}

.section-subtitle {
    font-size: 12px;
    color: var(--text-secondary);
}

/* Side Panel */
.side-panel {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.quick-actions-card, .activity-card {
    background: var(--surface-elevated);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.quick-actions-card h3, .activity-card h3 {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 16px;
}

.actions-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.action-btn {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    background: var(--surface-hover);
    border: 1px solid transparent;
    border-radius: 10px;
    font-weight: 500;
    font-size: 14px;
    color: var(--text-primary);
    cursor: pointer;
    transition: all 0.2s;
}

.action-btn:hover {
    background: var(--bg-secondary);
    border-color: var(--hover-color);
    transform: translateX(4px);
}

.action-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.post-icon {
    margin-left: auto;
    font-size: 16px;
    color: var(--text-secondary);
    opacity: 0;
    transition: opacity 0.2s;
}

.action-btn:hover .post-icon {
    opacity: 1;
}

/* Activity List */
.activity-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.activity-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border-subtle);
}

.activity-row:last-child {
    border-bottom: none;
    padding-bottom: 0;
}

.dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

.activity-text {
    display: flex;
    flex-direction: column;
}

.activity-text strong {
    font-size: 13px;
    font-weight: 500;
}

.time {
    font-size: 11px;
    color: var(--text-secondary);
}

/* Quick Entry Styles */
.quick-entry-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(8px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.quick-entry-panel {
    width: 100%;
    max-width: 500px;
    background: var(--surface-elevated);
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
    border: 1px solid var(--border-subtle);
}

.panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}

.panel-header h3 {
    font-size: 20px;
    font-weight: 700;
    margin: 0;
}

.close-btn {
    background: transparent;
    border: none;
    color: var(--text-secondary);
    font-size: 28px;
    cursor: pointer;
    line-height: 1;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 20px;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}

.form-group label {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-secondary);
}

.form-group input {
    background: var(--bg-primary);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 12px 16px;
    color: var(--text-primary);
    font-size: 14px;
    transition: all 0.2s;
}

.form-group input:focus {
    outline: none;
    border-color: var(--current-accent, #0ea5e9);
    box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.1);
}

.error-msg {
    color: #ef4444;
    font-size: 13px;
    margin-top: -8px;
    margin-bottom: 16px;
}

.panel-footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    margin-top: 8px;
}

.cancel-btn {
    padding: 10px 20px;
    background: transparent;
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    color: var(--text-primary);
    font-weight: 600;
    cursor: pointer;
}

.save-btn {
    padding: 10px 24px;
    background: var(--current-accent, #0ea5e9);
    border: none;
    border-radius: 10px;
    color: white;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
}

.save-btn:hover {
    filter: brightness(1.1);
    transform: translateY(-1px);
}

.save-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.fade-enter-active, .fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
    opacity: 0;
}

@media (max-width: 1200px) {
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    .dashboard-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 600px) {
    .stats-grid {
        grid-template-columns: 1fr;
    }
}
</style>
