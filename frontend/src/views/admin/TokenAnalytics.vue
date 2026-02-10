<template>
  <div class="token-analytics">
    <div class="page-header">
      <div>
        <h1>Token Tüketimi Analitikleri</h1>
        <p class="subtitle">AI model kullanımı ve maliyetlerini izleyin</p>
      </div>
      <select v-model="selectedPeriod" class="period-selector">
        <option :value="7">Son 7 Gün</option>
        <option :value="30">Son 30 Gün</option>
        <option :value="90">Son 90 Gün</option>
      </select>
    </div>

    <!-- Summary Cards -->
    <div class="stats-grid">
      <div class="stat-card total">
        <div class="stat-icon">
          <Cpu :size="24" />
        </div>
        <div>
          <p class="stat-label">Toplam Token</p>
          <h3 class="stat-value">{{ formatNumber(summary.total_tokens) }}</h3>
        </div>
      </div>
      <div class="stat-card cost">
        <div class="stat-icon">
          <DollarSign :size="24" />
        </div>
        <div>
          <p class="stat-label">Toplam Maliyet</p>
          <h3 class="stat-value">${{ summary.total_cost_usd }}</h3>
        </div>
      </div>
      <div class="stat-card calls">
        <div class="stat-icon">
          <Phone :size="24" />
        </div>
        <div>
          <p class="stat-label">Toplam Çağrı</p>
          <h3 class="stat-value">{{ formatNumber(summary.total_calls) }}</h3>
        </div>
      </div>
      <div class="stat-card average">
        <div class="stat-icon">
          <TrendingUp :size="24" />
        </div>
        <div>
          <p class="stat-label">Ortalama Token/Çağrı</p>
          <h3 class="stat-value">{{ formatNumber(summary.average_tokens_per_call) }}</h3>
        </div>
      </div>
    </div>

    <!-- Charts Grid -->
    <div class="charts-grid">
      <!-- Daily Usage Chart -->
      <div class="chart-card glass-effect">
        <h3>Günlük Token Tüketimi</h3>
        <div class="chart-container">
          <canvas ref="dailyChart"></canvas>
        </div>
      </div>

      <!-- Model Breakdown Chart -->
      <div class="chart-card glass-effect">
        <h3>Model Bazlı Dağılım</h3>
        <div class="chart-container">
          <canvas ref="modelChart"></canvas>
        </div>
      </div>
    </div>

    <!-- Model Breakdown Table -->
    <div class="table-container glass-effect">
      <h3>Detaylı Model İstatistikleri</h3>
      <table class="model-table">
        <thead>
          <tr>
            <th>Model</th>
            <th>Toplam Token</th>
            <th>Çağrı Sayısı</th>
            <th>Maliyet (USD)</th>
            <th>Ortalama Token</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="model in modelBreakdown" :key="model.model">
            <td>
              <span class="model-name">{{ model.model }}</span>
            </td>
            <td>{{ formatNumber(model.total_tokens) }}</td>
            <td>{{ formatNumber(model.call_count) }}</td>
            <td>
              <span class="cost-value">${{ model.total_cost.toFixed(4) }}</span>
            </td>
            <td>{{ formatNumber(Math.round(model.total_tokens / model.call_count)) }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Empty State -->
      <div v-if="modelBreakdown.length === 0 && !isLoading" class="empty-state">
        <BarChart3 :size="48" />
        <p>Token kullanım verisi bulunamadı</p>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="loading-state">
        <Loader2 :size="32" class="spin" />
        <p>Veriler yükleniyor...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, nextTick } from 'vue'
import { Cpu, DollarSign, Phone, TrendingUp, BarChart3, Loader2 } from 'lucide-vue-next'
import { useAdminStore } from '@/stores/admin'
import { Chart, registerables } from 'chart.js'
import api from '@/config/api'

Chart.register(...registerables)

const adminStore = useAdminStore()

// State
const selectedPeriod = ref(30)
const isLoading = ref(false)
const summary = ref({
  total_tokens: 0,
  total_cost_usd: 0,
  total_calls: 0,
  average_tokens_per_call: 0,
  period_days: 30
})
const dailyUsage = ref([])
const modelBreakdown = ref([])

// Chart refs
const dailyChart = ref(null)
const modelChart = ref(null)
let dailyChartInstance = null
let modelChartInstance = null

// Methods
async function loadAnalytics() {
  isLoading.value = true
  
  try {
    const response = await api.get('/admin/token-analytics', {
      params: { days: selectedPeriod.value },
      headers: {
        Authorization: `Bearer ${adminStore.accessToken}`
      }
    })
    
    summary.value = response.data.summary
    dailyUsage.value = response.data.daily_usage
    modelBreakdown.value = response.data.model_breakdown
    
    await nextTick()
    renderCharts()
  } catch (error) {
    console.error('Failed to load analytics:', error)
    alert('Analitik verileri yüklenemedi')
  } finally {
    isLoading.value = false
  }
}

function renderCharts() {
  renderDailyChart()
  renderModelChart()
}

function renderDailyChart() {
  if (!dailyChart.value) return
  
  // Destroy previous instance
  if (dailyChartInstance) {
    dailyChartInstance.destroy()
  }
  
  const ctx = dailyChart.value.getContext('2d')
  
  dailyChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: dailyUsage.value.map(d => new Date(d.date).toLocaleDateString('tr-TR', { month: 'short', day: 'numeric' })),
      datasets: [
        {
          label: 'Token Tüketimi',
          data: dailyUsage.value.map(d => d.tokens),
          borderColor: '#6366f1',
          backgroundColor: 'rgba(99, 102, 241, 0.1)',
          tension: 0.4,
          fill: true,
          pointBackgroundColor: '#6366f1',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: { color: '#9ca3af' }
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: '#fff',
          bodyColor: '#fff',
          padding: 12,
          cornerRadius: 8
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { color: '#9ca3af' },
          grid: { color: 'rgba(255, 255, 255, 0.05)' }
        },
        x: {
          ticks: { color: '#9ca3af' },
          grid: { color: 'rgba(255, 255, 255, 0.05)' }
        }
      }
    }
  })
}

function renderModelChart() {
  if (!modelChart.value || modelBreakdown.value.length === 0) return
  
  // Destroy previous instance
  if (modelChartInstance) {
    modelChartInstance.destroy()
  }
  
  const ctx = modelChart.value.getContext('2d')
  
  const colors = [
    '#6366f1',
    '#8b5cf6',
    '#10b981',
    '#f59e0b',
    '#ef4444'
  ]
  
  modelChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: modelBreakdown.value.map(m => m.model),
      datasets: [{
        data: modelBreakdown.value.map(m => m.total_tokens),
        backgroundColor: colors.slice(0, modelBreakdown.value.length),
        borderColor: '#030712',
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: { 
            color: '#9ca3af',
            padding: 16,
            usePointStyle: true
          }
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: '#fff',
          bodyColor: '#fff',
          padding: 12,
          cornerRadius: 8,
          callbacks: {
            label: function(context) {
              const label = context.label || ''
              const value = context.parsed || 0
              const total = context.dataset.data.reduce((a, b) => a + b, 0)
              const percentage = ((value / total) * 100).toFixed(1)
              return `${label}: ${formatNumber(value)} (${percentage}%)`
            }
          }
        }
      }
    }
  })
}

function formatNumber(num) {
  if (!num) return '0'
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`
  return num.toFixed(0)
}

// Watch period changes
watch(selectedPeriod, () => {
  loadAnalytics()
})

onMounted(() => {
  loadAnalytics()
})
</script>

<style scoped>
.token-analytics {
  padding: 24px;
  width: 100%;
  box-sizing: border-box;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 8px;
  animation: appear 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.subtitle {
  color: var(--text-secondary);
  font-size: 14px;
  animation: appear 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  animation-delay: 0.1s;
  opacity: 0;
}

.period-selector {
  padding: 12px 20px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
  margin-bottom: 32px;
}

.stat-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.3s;
  animation: appear 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
}

.stat-card:nth-child(1) { animation-delay: 0.2s; }
.stat-card:nth-child(2) { animation-delay: 0.3s; }
.stat-card:nth-child(3) { animation-delay: 0.4s; }
.stat-card:nth-child(4) { animation-delay: 0.5s; }

.stat-card:hover {
  transform: translateY(-2px);
  border-color: var(--border-hover);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-card.total .stat-icon {
  background: rgba(99, 102, 241, 0.1);
  color: #6366f1;
}

.stat-card.cost .stat-icon {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.stat-card.calls .stat-icon {
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
}

.stat-card.average .stat-icon {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
}

.stat-label {
  color: var(--text-secondary);
  font-size: 13px;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
}

/* Charts Grid */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.chart-card {
  padding: 24px;
  border-radius: 16px;
}

.chart-card h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 24px;
  color: var(--text-primary);
}

.chart-container {
  height: 300px;
  position: relative;
  animation: appear 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  animation-delay: 0.6s;
  opacity: 0;
}

/* Table */
.table-container {
  padding: 24px;
  border-radius: 16px;
  animation: appear 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  animation-delay: 0.7s;
  opacity: 0;
}

.table-container h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 20px;
  color: var(--text-primary);
}

.model-table {
  width: 100%;
  border-collapse: collapse;
}

.model-table thead {
  background: rgba(255, 255, 255, 0.03);
}

.model-table th {
  text-align: left;
  padding: 16px;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.025em;
  border-bottom: 1px solid var(--border-subtle);
}

.model-table td {
  padding: 16px;
  border-bottom: 1px solid var(--border-subtle);
  font-size: 14px;
  color: var(--text-primary);
}

.model-table tbody tr {
  transition: background 0.2s;
}

.model-table tbody tr:hover {
  background: rgba(255, 255, 255, 0.02);
}

.model-name {
  font-family: 'Courier New', monospace;
  padding: 4px 10px;
  background: rgba(99, 102, 241, 0.1);
  border-radius: 6px;
  color: #6366f1;
  font-weight: 600;
}

.cost-value {
  color: #10b981;
  font-weight: 600;
}

.empty-state,
.loading-state {
  padding: 80px;
  text-align: center;
  color: var(--text-secondary);
}

.empty-state p,
.loading-state p {
  margin-top: 16px;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
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

/* Responsive */
@media (max-width: 1024px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .token-analytics {
    padding: 16px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
