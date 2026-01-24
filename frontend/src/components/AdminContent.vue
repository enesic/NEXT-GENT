<template>
  <section class="admin-content">
    <div class="content-grid">
      <!-- Financial Metrics -->
      <div class="metric-card revenue">
        <div class="metric-header">
          <div class="metric-icon">
            <TrendingUp :size="24" :stroke-width="2" />
          </div>
          <span class="metric-badge positive">+12.5%</span>
        </div>
        <h3 class="metric-title">Toplam Gelir</h3>
        <p class="metric-value">
          <span v-if="!isLoading">{{ formatCurrency(stats.daily_revenue) }}</span>
          <SkeletonLoader v-else width="140px" height="40px" />
        </p>
        <p class="metric-subtitle">Bugün</p>
      </div>

      <div class="metric-card profit">
        <div class="metric-header">
          <div class="metric-icon">
            <DollarSign :size="24" :stroke-width="2" />
          </div>
          <span class="metric-badge positive">+8.2%</span>
        </div>
        <h3 class="metric-title">Kar Marjı</h3>
        <p class="metric-value">42.3%</p>
        <p class="metric-subtitle">Hedef: 40%</p>
      </div>

      <div class="metric-card growth">
        <div class="metric-header">
          <div class="metric-icon">
            <BarChart3 :size="24" :stroke-width="2" />
          </div>
          <span class="metric-badge positive">+15.8%</span>
        </div>
        <h3 class="metric-title">Büyüme Oranı</h3>
        <p class="metric-value">YoY 24%</p>
        <p class="metric-subtitle">Yıllık bazda</p>
      </div>

      <!-- AI Performance Heatmap -->
      <div class="heatmap-card">
        <div class="card-header">
          <h3 class="card-title">
            <Cpu :size="20" :stroke-width="2" class="title-icon" />
            AI Model Performansı
          </h3>
        </div>
        <div class="heatmap-grid">
          <div 
            v-for="(cell, index) in heatmapData" 
            :key="index"
            class="heatmap-cell"
            :style="{ backgroundColor: getHeatmapColor(cell.value) }"
            :title="`${cell.label}: ${cell.value}%`"
          >
            <span class="cell-value">{{ cell.value }}</span>
          </div>
        </div>
        <div class="heatmap-legend">
          <span class="legend-label">Düşük</span>
          <div class="legend-gradient"></div>
          <span class="legend-label">Yüksek</span>
        </div>
      </div>

      <!-- Strategic Reports -->
      <div class="report-card">
        <div class="card-header">
          <h3 class="card-title">
            <FileText :size="20" :stroke-width="2" class="title-icon" />
            Stratejik Raporlar
          </h3>
        </div>
        <div class="report-list">
          <div 
            v-for="report in reports" 
            :key="report.id"
            class="report-item"
          >
            <div class="report-info">
              <component :is="report.icon" :size="18" :stroke-width="2" class="report-icon" />
              <div class="report-details">
                <span class="report-name">{{ report.name }}</span>
                <span class="report-date">{{ report.date }}</span>
              </div>
            </div>
            <button class="report-action">
              <Download :size="16" :stroke-width="2" />
            </button>
          </div>
        </div>
      </div>

      <!-- Executive Summary -->
      <div class="summary-card">
        <div class="card-header">
          <h3 class="card-title">
            <Target :size="20" :stroke-width="2" class="title-icon" />
            Yönetici Özeti
          </h3>
        </div>
        <div class="summary-content">
          <div class="summary-item">
            <div class="summary-label">Aktif Projeler</div>
            <div class="summary-value">24</div>
          </div>
          <div class="summary-item">
            <div class="summary-label">Tamamlanan</div>
            <div class="summary-value">156</div>
          </div>
          <div class="summary-item">
            <div class="summary-label">Ekip Üyeleri</div>
            <div class="summary-value">48</div>
          </div>
          <div class="summary-item">
            <div class="summary-label">Müşteri Memnuniyeti</div>
            <div class="summary-value">
              <span v-if="!isLoading">{{ stats.customer_satisfaction }}%</span>
              <SkeletonLoader v-else width="60px" height="32px" />
            </div>
          </div>
          <div class="summary-item">
            <div class="summary-label">Aktif Çağrılar</div>
            <div class="summary-value">
              <span v-if="!isLoading">{{ stats.active_calls }}</span>
              <SkeletonLoader v-else width="60px" height="32px" />
            </div>
          </div>
        </div>
      </div>

      <!-- Data Art Charts -->
      <CallVolumeChart />
      <ConversionChart />
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted, inject } from 'vue'
import { 
  TrendingUp, 
  DollarSign, 
  BarChart3, 
  Cpu, 
  FileText, 
  Download,
  Target,
  PieChart,
  Activity,
  Briefcase
} from 'lucide-vue-next'
import CallVolumeChart from './CallVolumeChart.vue'
import ConversionChart from './ConversionChart.vue'
import SkeletonLoader from './SkeletonLoader.vue'

const axios = inject('axios')

const isLoading = ref(true)
const stats = ref({
  daily_revenue: 0,
  active_calls: 0,
  customer_satisfaction: 0
})

const formatCurrency = (value) => {
  return new Intl.NumberFormat('tr-TR', { style: 'currency', currency: 'TRY' }).format(value)
}

const fetchData = async () => {
  try {
    const response = await axios.get('/analytics/stats')
    stats.value = response.data
  } catch (error) {
    console.error('Failed to fetch admin stats:', error)
  } finally {
    isLoading.value = false
  }
}

let pollInterval

onMounted(() => {
  fetchData()
  pollInterval = setInterval(fetchData, 30000)
})

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval)
})

const heatmapData = ref([
  { label: 'Accuracy', value: 94 },
  { label: 'Precision', value: 89 },
  { label: 'Recall', value: 92 },
  { label: 'F1-Score', value: 90 },
  { label: 'Latency', value: 78 },
  { label: 'Throughput', value: 85 },
  { label: 'Error Rate', value: 12 },
  { label: 'Uptime', value: 99 }
])

const reports = ref([
  { id: 1, name: 'Q1 Finansal Rapor', date: '15 Ocak 2026', icon: PieChart },
  { id: 2, name: 'Performans Analizi', date: '12 Ocak 2026', icon: Activity },
  { id: 3, name: 'Stratejik Plan 2026', date: '8 Ocak 2026', icon: Briefcase }
])

const getHeatmapColor = (value) => {
  if (value >= 90) return 'rgba(34, 197, 94, 0.8)'  // Green
  if (value >= 70) return 'rgba(234, 179, 8, 0.8)'  // Yellow
  if (value >= 50) return 'rgba(249, 115, 22, 0.8)' // Orange
  return 'rgba(239, 68, 68, 0.8)' // Red
}
</script>

<style scoped>
.admin-content {
  flex: 1;
  overflow-y: auto;
  padding: 32px;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
  max-width: 1400px;
}

/* Metric Cards */
.metric-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 24px;
  transition: all var(--transition-base);
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--indigo-primary), #8b5cf6);
  opacity: 0;
  transition: opacity var(--transition-base);
}

.metric-card:hover {
  background: var(--surface-hover);
  border-color: var(--border-hover);
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4),
              0 0 48px var(--indigo-glow);
}

.metric-card:hover::before {
  opacity: 1;
}

.metric-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.metric-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, var(--indigo-primary), #8b5cf6);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 0 24px var(--indigo-glow);
}

.metric-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: var(--letter-spacing-normal);
}

.metric-badge.positive {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}

.metric-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  letter-spacing: var(--letter-spacing-normal);
  margin-bottom: 8px;
}

.metric-value {
  font-size: 32px;
  font-weight: 700;
  letter-spacing: var(--letter-spacing-tight);
  line-height: var(--line-height-tight);
  margin-bottom: 4px;
}

.metric-subtitle {
  font-size: 12px;
  color: var(--text-muted);
  letter-spacing: var(--letter-spacing-normal);
}

/* Heatmap Card */
.heatmap-card {
  grid-column: span 2;
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 24px;
}

.card-header {
  margin-bottom: 20px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  letter-spacing: var(--letter-spacing-tight);
  display: flex;
  align-items: center;
  gap: 8px;
}

.title-icon {
  color: var(--indigo-primary);
}

.heatmap-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.heatmap-cell {
  aspect-ratio: 1;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 18px;
  color: white;
  cursor: pointer;
  transition: all var(--transition-fast);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.heatmap-cell:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
}

.heatmap-legend {
  display: flex;
  align-items: center;
  gap: 12px;
  justify-content: center;
}

.legend-label {
  font-size: 12px;
  color: var(--text-muted);
  font-weight: 500;
}

.legend-gradient {
  width: 200px;
  height: 8px;
  border-radius: 4px;
  background: linear-gradient(90deg, 
    rgba(239, 68, 68, 0.8), 
    rgba(249, 115, 22, 0.8), 
    rgba(234, 179, 8, 0.8), 
    rgba(34, 197, 94, 0.8)
  );
}

/* Report Card */
.report-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 24px;
}

.report-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.report-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  background: var(--surface-hover);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  transition: all var(--transition-fast);
}

.report-item:hover {
  border-color: var(--border-hover);
  box-shadow: 0 0 16px var(--indigo-glow);
}

.report-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.report-icon {
  color: var(--indigo-primary);
}

.report-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.report-name {
  font-size: 14px;
  font-weight: 500;
  letter-spacing: var(--letter-spacing-normal);
}

.report-date {
  font-size: 12px;
  color: var(--text-muted);
}

.report-action {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.report-action:hover {
  background: var(--indigo-primary);
  border-color: var(--indigo-primary);
  color: white;
  box-shadow: 0 0 16px var(--indigo-glow);
}

/* Summary Card */
.summary-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 24px;
}

.summary-content {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.summary-item {
  text-align: center;
}

.summary-label {
  font-size: 12px;
  color: var(--text-muted);
  margin-bottom: 8px;
  letter-spacing: var(--letter-spacing-normal);
}

.summary-value {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: var(--letter-spacing-tight);
  background: linear-gradient(135deg, var(--indigo-primary), #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>
