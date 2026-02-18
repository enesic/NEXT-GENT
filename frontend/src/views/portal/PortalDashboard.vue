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

        // Map KPIs to stat cards format
        if (kpis && Array.isArray(kpis)) {
            stats.value = kpis.map((kpi, index) => ({
                label: kpi.label,
                value: kpi.value,
                change: parseFloat(kpi.trend) || 0,
                icon: getIconForKPI(index),
                color: kpi.positive ? 'primary' : 'red',
                description: kpi.description
            }))
        }

        satisfactionData.value = satisfaction
        quickStatsData.value = quickStats

        console.log('✅ Dashboard data loaded:', { kpis, satisfaction, quickStats })
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
    // Use nav property from sectorThemes quickActions
    const target = action.nav || 'dashboard'
    emit('navigate', target)
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
