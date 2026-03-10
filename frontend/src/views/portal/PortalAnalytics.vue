<template>
  <div class="portal-page">
    <div class="page-header">
      <div>
        <h1 :style="{ color: colors.primary }">{{ t('performance_analysis') }}</h1>
        <p class="subtitle">{{ t('analytics_subtitle') }}</p>
      </div>
      <!-- Date Range Picker -->
      <div class="date-picker">
        <button
          v-for="range in dateRanges"
          :key="range.label"
          class="picker-btn"
          :class="{ active: selectedRange === range.label.tr }"
          @click="selectRange(range)"
        >
          {{ tLoc(range.label) }}
        </button>
      </div>
    </div>

    <!-- KPI Summary Cards -->
    <div class="kpi-row" v-if="!loadingSummary">
      <div class="kpi-card" v-for="kpi in kpiCards" :key="tLoc(kpi.label)">
        <span class="kpi-label">{{ tLoc(kpi.label) }}</span>
        <span class="kpi-value" :style="{ color: colors.primary }">{{ kpi.value }}</span>
        <span class="kpi-sub">{{ tLoc(kpi.sub) }}</span>
      </div>
    </div>
    <div class="kpi-row" v-else>
      <div class="kpi-card skeleton" v-for="i in 4" :key="i"></div>
    </div>

    <div class="content-card">
      <div class="analytics-grid">
        <!-- Aylık Etkileşim Grafiği -->
        <div class="chart-container large">
          <h3>{{ t('monthly_interaction') }}</h3>
          <div v-if="loadingConversation" class="chart-loading">
            <div class="spinner" :style="{ borderTopColor: colors.primary }"></div>
            <span>{{ t('data_loading') }}</span>
          </div>
          <LuxuryChart
            v-else
            type="area"
            :series="conversationData.series"
            :categories="conversationData.categories"
            height="300"
            :color="colors.primary"
          />
        </div>

        <!-- Dağılım / Durum Pie -->
        <div class="chart-container">
          <h3>{{ t('appointment_distribution') }}</h3>
          <div v-if="loadingStatus" class="chart-loading">
            <div class="spinner" :style="{ borderTopColor: colors.primary }"></div>
            <span>{{ t('data_loading') }}</span>
          </div>
          <LuxuryChart
            v-else
            type="donut"
            :series="statusData.series"
            :labels="statusData.labels"
            height="300"
            :color="colors.primary"
          />
        </div>

        <!-- Dönüşüm Oranı Bar -->
        <div class="chart-container">
          <h3>{{ t('conversion_rate') }}</h3>
          <div v-if="loadingConversion" class="chart-loading">
            <div class="spinner" :style="{ borderTopColor: colors.accent || colors.primary }"></div>
            <span>{{ t('data_loading') }}</span>
          </div>
          <LuxuryChart
            v-else
            type="bar"
            :series="conversionData.series"
            :categories="conversionData.categories"
            height="300"
            :color="colors.accent || colors.primary"
          />
        </div>
      </div>
    </div>

    <!-- Error State -->
    <div v-if="error" class="error-banner">
      <span>⚠️ {{ error }}</span>
      <button @click="fetchAll">{{ t('retry') }}</button>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useSectorStore } from '../../stores/sector'
import LuxuryChart from '../../components/LuxuryChart.vue'
import api from '@/config/api'

const t = (key) => sectorStore.t(key)
const tLoc = (obj) => sectorStore.tLoc(obj)

const colors = computed(() => sectorStore.theme || {
  primary: '#0ea5e9',
  secondary: '#0f766e',
  accent: '#38bdf8',
  text: '#e2e8f0'
})

// ── Date Range ──────────────────────────────────────────────────────────────
const dateRanges = [
  { label: { tr: 'Son 7 Gün', en: 'Last 7 Days', de: 'Letzte 7 Tage' },  days: 7 },
  { label: { tr: 'Son 30 Gün', en: 'Last 30 Days', de: 'Letzte 30 Tage' }, days: 30 },
  { label: { tr: 'Son 90 Gün', en: 'Last 90 Days', de: 'Letzte 90 Tage' }, days: 90 },
]
const selectedRange = ref('Son 30 Gün')

const getDateRange = (days) => {
  const end = new Date()
  const start = new Date()
  start.setDate(start.getDate() - days)
  const fmt = (d) => d.toISOString().split('T')[0]
  return { start_date: fmt(start), end_date: fmt(end) }
}

const selectRange = (range) => {
  selectedRange.value = range.label.tr
  fetchAll(range.days)
}

// ── State ──────────────────────────────────────────────────────────────────
const loadingConversation = ref(true)
const loadingConversion   = ref(true)
const loadingStatus       = ref(true)
const loadingSummary      = ref(true)
const error               = ref(null)

const conversationData = ref({ series: [], categories: [] })
const conversionData   = ref({ series: [], categories: [] })
const statusData       = ref({ series: [], labels: [] })
const summaryData      = ref(null)

// ── KPI Cards ──────────────────────────────────────────────────────────────
const kpiCards = computed(() => {
  if (!summaryData.value) return []
  const s = summaryData.value
  return [
    { label: { tr: 'Toplam Randevu', en: 'Total Appts', de: 'Gesamte Termine' },  value: s.total_appointments ?? '-',  sub: { tr: 'dönem içinde', en: 'in period', de: 'im Zeitraum' } },
    { label: { tr: 'Onaylanan', en: 'Confirmed', de: 'Bestätigt' },       value: s.confirmed_appointments ?? '-', sub: { tr: 'randevu', en: 'appt', de: 'termin' } },
    { label: { tr: 'Müşteri', en: 'Customer', de: 'Kunde' },         value: s.total_customers ?? '-',  sub: { tr: 'benzersiz kişi', en: 'unique people', de: 'einzigartige Personen' } },
    { label: { tr: 'Dönüşüm Oranı', en: 'Conv Rate', de: 'Konv. Rate' },  value: s.conversion_rate != null ? `${s.conversion_rate}%` : '-', sub: { tr: 'onay/toplam', en: 'conf/total', de: 'best/ges' } },
  ]
})

// ── Fetch Functions ─────────────────────────────────────────────────────────
const fetchConversation = async (days = 30) => {
  loadingConversation.value = true
  try {
    const res = await api.get('/analytics/daily-conversation-duration')
    conversationData.value = res.data
  } catch (e) {
    console.error('Conversation analytics error:', e)
  } finally {
    loadingConversation.value = false
  }
}

const fetchConversion = async (days = 30) => {
  loadingConversion.value = true
  try {
    const { start_date, end_date } = getDateRange(days)
    const res = await api.get('/analytics/conversion-rate', { params: { start_date, end_date } })
    conversionData.value = res.data
  } catch (e) {
    console.error('Conversion analytics error:', e)
    conversionData.value = { series: [], categories: [] }
  } finally {
    loadingConversion.value = false
  }
}

const fetchStatus = async (days = 30) => {
  loadingStatus.value = true
  try {
    const { start_date, end_date } = getDateRange(days)
    const res = await api.get('/analytics/appointment-status-breakdown', { params: { start_date, end_date } })
    statusData.value = res.data
  } catch (e) {
    console.error('Status analytics error:', e)
    statusData.value = { series: [], labels: [] }
  } finally {
    loadingStatus.value = false
  }
}

const fetchSummary = async (days = 30) => {
  loadingSummary.value = true
  try {
    const { start_date, end_date } = getDateRange(days)
    const res = await api.get('/analytics/dashboard-summary', { params: { start_date, end_date } })
    summaryData.value = res.data
  } catch (e) {
    console.error('Summary analytics error:', e)
  } finally {
    loadingSummary.value = false
  }
}

const fetchAll = async (days = 30) => {
  error.value = null
  try {
    await Promise.all([
      fetchConversation(days),
      fetchConversion(days),
      fetchStatus(days),
      fetchSummary(days),
    ])
  } catch (e) {
    error.value = 'Veriler yüklenirken hata oluştu. Lütfen tekrar deneyin.'
  }
}

onMounted(() => fetchAll(30))
</script>

<style scoped>
.portal-page {
  width: 100%;
  margin: 0;
  padding: 24px;
  box-sizing: border-box;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 4px;
}

.subtitle {
  color: var(--text-secondary);
  font-size: 14px;
}

/* Date Picker */
.date-picker {
  display: flex;
  gap: 6px;
  background: var(--surface-elevated);
  padding: 4px;
  border-radius: 8px;
  border: 1px solid var(--border-subtle);
}

.picker-btn {
  padding: 6px 14px;
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  border-radius: 6px;
  font-size: 13px;
  transition: all 0.2s;
}

.picker-btn.active,
.picker-btn:hover {
  background: var(--surface-hover);
  color: var(--text-primary);
  font-weight: 600;
}

/* KPI Row */
.kpi-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.kpi-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  padding: 20px 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.kpi-card.skeleton {
  min-height: 90px;
  animation: pulse 1.5s ease-in-out infinite;
  background: var(--surface-hover);
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.5; }
}

.kpi-label {
  font-size: 12px;
  color: var(--text-secondary);
}

.kpi-value {
  font-size: 28px;
  font-weight: 700;
  line-height: 1.2;
}

.kpi-sub {
  font-size: 11px;
  color: var(--text-secondary);
}

/* Content Card */
.content-card {
  background: var(--surface-elevated);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
}

.analytics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.chart-container {
  padding: 16px;
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
}

.chart-container.large {
  grid-column: span 2;
}

.chart-container h3 {
  margin-bottom: 16px;
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
}

/* Loading */
.chart-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  height: 200px;
  color: var(--text-secondary);
  font-size: 13px;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--border-subtle);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Error Banner */
.error-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-top: 16px;
  padding: 12px 16px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  color: #ef4444;
  font-size: 14px;
}

.error-banner button {
  padding: 6px 16px;
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 6px;
  color: #ef4444;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  transition: background 0.2s;
}

.error-banner button:hover {
  background: rgba(239, 68, 68, 0.25);
}

@media (max-width: 768px) {
  .analytics-grid { grid-template-columns: 1fr; }
  .chart-container.large { grid-column: span 1; }
  .kpi-row { grid-template-columns: repeat(2, 1fr); }
  .page-header { flex-direction: column; }
}
</style>
