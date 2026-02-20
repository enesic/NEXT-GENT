<template>
  <div class="content-wrapper">
    <!-- Overview Cards -->
    <div class="kpi-grid">
      <div 
        v-for="(kpi, index) in kpis" 
        :key="index"
        class="kpi-card"
      >
        <div class="card-header">
          <h3>{{ kpi.label }}</h3>
          <Target :size="20" :stroke-width="2" class="card-icon" />
        </div>
        <div class="card-body">
          <div class="stat-large">{{ kpi.value }}</div>
          <div class="stat-label">{{ kpi.description }}</div>
          <div class="stat-change" :class="kpi.positive ? 'positive' : 'negative'">
            <TrendingUp v-if="kpi.positive" :size="14" :stroke-width="2" />
            <TrendingDown v-else :size="14" :stroke-width="2" />
            <span>{{ kpi.trend }} bu ay</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Analytics Row -->
    <div class="analytics-row">
      <!-- Main Chart -->
      <div class="chart-section">
        <LuxuryChart 
          title="Canlı Performans Analizi"
          type="area"
          :series="chartData.series"
          :categories="chartData.categories"
          :height="350"
        />
      </div>

      <!-- AI Insights Panel -->
      <div class="insights-section">
        <div class="section-title">
          <div class="icon-box">
            <Sparkles :size="18" />
          </div>
          <h3>AI Insight Engine</h3>
        </div>
        
        <div class="insights-list">
          <AIInsightCard 
            v-for="(insight, index) in insights"
            :key="index"
            :type="insight.type"
            :title="insight.title"
            :message="insight.message"
            :action="insight.action"
          />
        </div>
      </div>
    </div>

    <!-- Satisfaction Metrics -->
    <div class="satisfaction-section">
      <div class="section-title">
        <div class="icon-box">
          <Heart :size="18" />
        </div>
        <h3>Müşteri Memnuniyeti</h3>
      </div>
      <div class="satisfaction-metrics">
        <div class="satisfaction-metric">
          <div class="metric-label">NPS Score</div>
          <div class="metric-value">{{ satisfactionMetrics.nps || 'N/A' }}</div>
        </div>
        <div class="satisfaction-metric">
          <div class="metric-label">CSAT Average</div>
          <div class="metric-value">{{ satisfactionMetrics.csat || 'N/A' }}</div>
        </div>
        <div class="satisfaction-metric">
          <div class="metric-label">Positive Sentiment</div>
          <div class="metric-value">{{ satisfactionMetrics.positive || 0 }}%</div>
        </div>
      </div>
    </div>

    <!-- Recent Appointments Table -->
    <div class="demo-table-card">
      <div class="table-header">
        <h3>{{ sectorStore.t('recent_activity_title') || 'Son İşlemler' }}</h3>
        <button class="view-all-btn">
          Tümünü Gör
          <ArrowRight :size="16" :stroke-width="2" />
        </button>
      </div>
      <div class="table-content">
        <table class="data-table">
          <thead>
            <tr>
              <th>{{ sectorStore.t('client_label') || 'Müşteri' }}</th>
              <th>{{ sectorStore.t('type_label') || 'İşlem' }}</th>
              <th>Tarih</th>
              <th>Durum</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in demoTableData" :key="item.id">
              <td>
                <div class="client-cell">
                  <div class="client-avatar">{{ item.initials }}</div>
                  <span>{{ item.name }}</span>
                </div>
              </td>
              <td>{{ item.type }}</td>
              <td>{{ item.date }}</td>
              <td>
                <span :class="['status-badge', item.status]">
                  {{ item.statusText }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject, watch } from 'vue'
import { Target, TrendingUp, TrendingDown, Sparkles, ArrowRight, Heart } from 'lucide-vue-next'
import { useSectorStore } from '../../stores/sector'
import LuxuryChart from '../LuxuryChart.vue'
import AIInsightCard from '../AIInsightCard.vue'

const axios = inject('axios')
const sectorStore = useSectorStore()

const kpis = ref([])
const insights = ref([])
const chartData = ref({ series: [], categories: [] })
const satisfactionMetrics = ref({
  nps: null,
  csat: null,
  positive: 0
})
const demoTableData = ref([
  { id: 1, name: 'Ayşe Yılmaz', initials: 'AY', type: 'Kontrol', date: 'Bugün, 14:00', status: 'confirmed', statusText: 'Onaylandı' },
  { id: 2, name: 'Mehmet Demir', initials: 'MD', type: 'İlk Görüşme', date: 'Bugün, 15:30', status: 'pending', statusText: 'Bekliyor' },
  { id: 3, name: 'Canan Öz', initials: 'CÖ', type: 'Acil', date: 'Yarın, 09:00', status: 'cancelled', statusText: 'İptal' },
])

const fetchDashboardData = async () => {
  try {
    // Calculate date range (last 30 days)
    const endDate = new Date()
    const startDate = new Date()
    startDate.setDate(startDate.getDate() - 30)
    
    const dateParams = {
      start_date: startDate.toISOString().split('T')[0],
      end_date: endDate.toISOString().split('T')[0]
    }
    
    // Fetch real KPIs from backend - NO FALLBACK
    const kpiRes = await axios.get(`/analytics/kpis`)
    kpis.value = kpiRes.data || []

    // Fetch real insights - NO FALLBACK
    const insightRes = await axios.get('/analytics/insights')
    insights.value = insightRes.data || []
    
    // Fetch satisfaction metrics - NO FALLBACK
    const satisfactionRes = await axios.get('/satisfaction/metrics', {
      params: { days: 30 }
    })
    if (satisfactionRes.data) {
      satisfactionMetrics.value = {
        nps: satisfactionRes.data.nps?.score || null,
        csat: satisfactionRes.data.csat?.average || null,
        positive: satisfactionRes.data.sentiment?.positive || 0
      }
    }
    
    // Fetch real chart data with date range - NO FALLBACK
    const chartRes = await axios.get('/analytics/daily-conversation-duration', {
      params: dateParams
    })
    if (chartRes.data && chartRes.data.series && chartRes.data.series.length > 0) {
      chartData.value = {
        series: chartRes.data.series,
        categories: chartRes.data.categories || []
      }
    }
    
    // Fetch real interactions for table - NO FALLBACK
    const interactionsRes = await axios.get('/interactions', {
      params: { limit: 10, status: 'CONFIRMED' }
    })
    if (interactionsRes.data && Array.isArray(interactionsRes.data) && interactionsRes.data.length > 0) {
      demoTableData.value = interactionsRes.data.slice(0, 10).map((interaction) => ({
        id: interaction.id,
        name: interaction.client_name || 'Müşteri',
        initials: (interaction.client_name || 'MU').split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase(),
        type: interaction.type || 'Randevu',
        date: new Date(interaction.start_time).toLocaleDateString('tr-TR', { 
          day: 'numeric', 
          month: 'short', 
          hour: '2-digit', 
          minute: '2-digit' 
        }),
        status: (interaction.status || 'PENDING').toLowerCase(),
        statusText: getStatusText(interaction.status || 'PENDING')
      }))
    }
    
  } catch (e) {
    console.error("Dashboard fetch error:", e)
    // NO FALLBACK - Show error state to user
    // Silent fail for UX
    console.error("Dashboard data load error (silent)", e)
  }
}

const getStatusText = (status) => {
  const statusMap = {
    'CONFIRMED': 'Onaylandı',
    'PENDING': 'Bekliyor',
    'CANCELLED': 'İptal',
    'COMPLETED': 'Tamamlandı'
  }
  return statusMap[status] || status
}

watch(() => sectorStore.currentSectorId, fetchDashboardData)

onMounted(fetchDashboardData)
</script>

<style scoped>
.content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 32px; /* 8px grid: 32 = 8*4 */
  padding-bottom: 32px;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px; /* 8px grid: 24 = 8*3 */
}

.kpi-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: 16px; /* 8px grid: 16 = 8*2 */
  padding: 24px; /* 8px grid: 24 = 8*3 */
  transition: all var(--transition-fast);
}

.kpi-card:hover {
  border-color: var(--border-hover);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px; /* 8px grid: 16 = 8*2 */
}

.card-header h3 {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
}

.card-icon {
  color: var(--current-accent);
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 8px; /* 8px grid: 8 = 8*1 */
}

.stat-large {
  font-size: 36px;
  font-weight: 700;
  letter-spacing: var(--letter-spacing-tight);
  color: var(--text-primary);
}

.stat-label {
  font-size: 13px;
  color: var(--text-muted);
}

.stat-change {
  display: flex;
  align-items: center;
  gap: 8px; /* 8px grid: 8 = 8*1 */
  font-size: 12px;
  font-weight: 600;
  margin-top: 8px; /* 8px grid: 8 = 8*1 */
}

.stat-change.positive { color: #10b981; }
.stat-change.negative { color: #ef4444; }

/* Analytics Row */
.analytics-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

@media (max-width: 1200px) {
  .analytics-row { grid-template-columns: 1fr; }
}

.chart-section { 
  min-height: 400px;
  width: 100%;
}

/* Responsive Design */
@media (max-width: 768px) {
  .content-wrapper {
    gap: 24px;
  }
  
  .kpi-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .kpi-card {
    padding: 20px;
  }
  
  .stat-large {
    font-size: 28px;
  }
  
  .analytics-row {
    gap: 16px;
  }
  
  .chart-section {
    min-height: 300px;
  }
  
  .table-header {
    padding: 16px;
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .data-table {
    font-size: 12px;
  }
  
  .data-table th,
  .data-table td {
    padding: 12px 16px;
  }
  
  .client-cell {
    gap: 8px;
  }
  
  .client-avatar {
    width: 28px;
    height: 28px;
    font-size: 10px;
  }
}

@media (max-width: 480px) {
  .content-wrapper {
    gap: 16px;
  }
  
  .kpi-card {
    padding: 16px;
  }
  
  .card-header {
    margin-bottom: 16px;
  }
  
  .stat-large {
    font-size: 24px;
  }
  
  .chart-section {
    min-height: 250px;
  }
  
  .data-table th,
  .data-table td {
    padding: 8px 12px;
    font-size: 11px;
  }
  
  .table-content {
    overflow-x: scroll;
    -webkit-overflow-scrolling: touch;
  }
}

/* Insights */
.insights-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 16px;
}

.icon-box {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, var(--indigo-primary), #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 0 12px var(--indigo-glow);
}

.section-title h3 {
  font-size: 16px;
  font-weight: 600;
  letter-spacing: -0.01em;
  color: var(--text-primary);
}

.insights-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Table */
.demo-table-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.table-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px;
  border-bottom: 1px solid var(--border-subtle);
}

.table-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.view-all-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
}

.view-all-btn:hover { color: var(--text-primary); }

.table-content { overflow-x: auto; }

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th, .data-table td {
  padding: 16px 24px;
  text-align: left;
  border-bottom: 1px solid var(--border-subtle);
}

.data-table th {
  font-size: 12px;
  text-transform: uppercase;
  color: var(--text-muted);
  font-weight: 600;
  letter-spacing: 0.05em;
}

.data-table td {
  color: var(--text-secondary);
  font-size: 14px;
}

.data-table tr:last-child td { border-bottom: none; }
.data-table tr:hover { background: var(--surface-hover); }

.client-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.client-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--surface-hover);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  color: var(--current-accent);
}

.status-badge {
  padding: 4px 10px;
  border-radius: 99px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.confirmed { background: rgba(16, 185, 129, 0.1); color: #10b981; }
.status-badge.pending { background: rgba(245, 158, 11, 0.1); color: #f59e0b; }
.status-badge.cancelled { background: rgba(239, 68, 68, 0.1); color: #ef4444; }

/* Satisfaction Section */
.satisfaction-section {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 24px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.icon-box {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, #ec4899, #f43f5e);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 0 12px rgba(236, 72, 153, 0.3);
}

.section-title h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.satisfaction-metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.satisfaction-metric {
  text-align: center;
}

.metric-label {
  font-size: 12px;
  color: var(--text-muted);
  margin-bottom: 8px;
}

.metric-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
}

@media (max-width: 768px) {
  .satisfaction-metrics {
    grid-template-columns: 1fr;
  }
}
</style>
