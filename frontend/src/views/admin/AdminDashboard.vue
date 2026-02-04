<template>
  <div class="dashboard-wrapper">
    <!-- Stats Grid -->
    <div class="stats-grid">
      <div class="stat-card" v-for="stat in stats" :key="stat.label">
        <div class="stat-icon" :style="{ background: stat.color }">
          <component :is="stat.icon" :size="24" :stroke-width="2" />
        </div>
        <div class="stat-content">
          <p class="stat-label">{{ stat.label }}</p>
          <h3 class="stat-value">{{ stat.value }}</h3>
          <div class="stat-footer">
            <span class="stat-change" :class="{ positive: stat.change > 0, negative: stat.change < 0 }">
              <TrendingUp v-if="stat.change > 0" :size="14" />
              <TrendingDown v-else :size="14" />
              {{ Math.abs(stat.change) }}%
            </span>
            <span class="stat-period">vs geçen ay</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Row -->
    <div class="charts-row">
      <!-- Traffic Chart -->
      <div class="chart-card">
        <div class="chart-header">
          <div>
            <h3 class="chart-title">Haftalık Trafik</h3>
            <p class="chart-subtitle">Son 7 günlük aktivite</p>
          </div>
          <select class="chart-select">
            <option>Son 7 Gün</option>
            <option>Son 30 Gün</option>
            <option>Son 90 Gün</option>
          </select>
        </div>
        <div class="chart-container">
          <canvas ref="trafficChart"></canvas>
        </div>
      </div>

      <!-- Performance Chart -->
      <div class="chart-card">
        <div class="chart-header">
          <div>
            <h3 class="chart-title">Sistem Performansı</h3>
            <p class="chart-subtitle">Başarı oranları</p>
          </div>
        </div>
        <div class="chart-container">
          <canvas ref="performanceChart"></canvas>
        </div>
      </div>
    </div>

    <!-- Activity & Quick Actions -->
    <div class="bottom-row">
      <!-- Recent Activity -->
      <div class="activity-card">
        <div class="card-header">
          <h3 class="card-title">
            <Activity :size="20" :stroke-width="2" />
            Son Aktiviteler
          </h3>
          <button class="view-all-btn">Tümünü Gör</button>
        </div>
        <div class="activity-list">
          <div class="activity-item" v-for="activity in recentActivities" :key="activity.id">
            <div class="activity-icon" :class="activity.type">
              <component :is="activity.icon" :size="16" :stroke-width="2" />
            </div>
            <div class="activity-content">
              <p class="activity-text">{{ activity.text }}</p>
              <span class="activity-time">{{ activity.time }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="quick-actions-card">
        <div class="card-header">
          <h3 class="card-title">
            <Zap :size="20" :stroke-width="2" />
            Hızlı İşlemler
          </h3>
        </div>
        <div class="actions-grid">
          <button class="action-btn" v-for="action in quickActions" :key="action.label">
            <component :is="action.icon" :size="20" :stroke-width="2" />
            <span>{{ action.label }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Chart, registerables } from 'chart.js'
import {
  Users,
  DollarSign,
  Phone,
  TrendingUp,
  TrendingDown,
  Activity,
  Zap,
  UserPlus,
  FileText,
  Settings,
  Download,
  Upload,
  RefreshCw,
  BarChart3
} from 'lucide-vue-next'

Chart.register(...registerables)

const stats = ref([
  {
    label: 'Toplam Kullanıcı',
    value: '2,543',
    change: 12.5,
    icon: Users,
    color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  {
    label: 'Aylık Gelir',
    value: '₺45,231',
    change: 8.2,
    icon: DollarSign,
    color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
  },
  {
    label: 'Aktif Çağrılar',
    value: '1,234',
    change: -3.1,
    icon: Phone,
    color: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
  },
  {
    label: 'Başarı Oranı',
    value: '94.2%',
    change: 2.4,
    icon: TrendingUp,
    color: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
  }
])

const recentActivities = ref([
  {
    id: 1,
    text: 'Yeni kullanıcı kaydı: Ahmet Yılmaz',
    time: '2 dakika önce',
    type: 'user',
    icon: UserPlus
  },
  {
    id: 2,
    text: 'Sistem güncellemesi tamamlandı',
    time: '15 dakika önce',
    type: 'system',
    icon: RefreshCw
  },
  {
    id: 3,
    text: 'Yeni rapor oluşturuldu',
    time: '1 saat önce',
    type: 'report',
    icon: FileText
  },
  {
    id: 4,
    text: 'Ayarlar güncellendi',
    time: '2 saat önce',
    type: 'settings',
    icon: Settings
  }
])

const quickActions = ref([
  { label: 'Kullanıcı Ekle', icon: UserPlus },
  { label: 'Rapor Oluştur', icon: FileText },
  { label: 'Veri İndir', icon: Download },
  { label: 'Veri Yükle', icon: Upload },
  { label: 'Ayarlar', icon: Settings },
  { label: 'Analitik', icon: BarChart3 }
])

const trafficChart = ref(null)
const performanceChart = ref(null)

const renderCharts = () => {
  // Traffic Chart
  if (trafficChart.value) {
    new Chart(trafficChart.value, {
      type: 'line',
      data: {
        labels: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
        datasets: [
          {
            label: 'Çağrılar',
            data: [65, 78, 90, 81, 56, 55, 40],
            borderColor: '#667eea',
            backgroundColor: 'rgba(102, 126, 234, 0.1)',
            tension: 0.4,
            fill: true,
            borderWidth: 2
          },
          {
            label: 'Mesajlar',
            data: [45, 52, 65, 59, 48, 42, 35],
            borderColor: '#f093fb',
            backgroundColor: 'rgba(240, 147, 251, 0.1)',
            tension: 0.4,
            fill: true,
            borderWidth: 2
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'bottom',
            labels: {
              color: '#9ca3af',
              usePointStyle: true,
              padding: 15
            }
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
            grid: { display: false }
          }
        }
      }
    })
  }

  // Performance Chart (Doughnut)
  if (performanceChart.value) {
    new Chart(performanceChart.value, {
      type: 'doughnut',
      data: {
        labels: ['Başarılı', 'Beklemede', 'Başarısız'],
        datasets: [
          {
            data: [85, 10, 5],
            backgroundColor: [
              '#43e97b',
              '#f093fb',
              '#f5576c'
            ],
            borderWidth: 0
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'bottom',
            labels: {
              color: '#9ca3af',
              usePointStyle: true,
              padding: 15
            }
          }
        }
      }
    })
  }
}

onMounted(() => {
  renderCharts()
})
</script>

<style scoped>
/* Main Wrapper - Full Width */
.dashboard-wrapper {
  width: 100%;
  padding: 24px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Stats Grid - 4 Columns */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  width: 100%;
}

.stat-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  gap: 20px;
  align-items: flex-start;
  transition: all 0.3s;
  width: 100%;
  box-sizing: border-box;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
  border-color: var(--border-hover);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.stat-content {
  flex: 1;
  min-width: 0;
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 8px;
  font-weight: 500;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  margin-bottom: 12px;
}

.stat-footer {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stat-change {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
}

.stat-change.positive {
  background: rgba(67, 233, 123, 0.15);
  color: #43e97b;
}

.stat-change.negative {
  background: rgba(245, 87, 108, 0.15);
  color: #f5576c;
}

.stat-period {
  font-size: 12px;
  color: var(--text-muted);
}

/* Charts Row - 2 Columns */
.charts-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  width: 100%;
}

.chart-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: 16px;
  padding: 24px;
  width: 100%;
  box-sizing: border-box;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.chart-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.chart-subtitle {
  font-size: 13px;
  color: var(--text-secondary);
}

.chart-select {
  padding: 8px 12px;
  background: var(--surface-hover);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  color: var(--text-primary);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.chart-select:hover {
  border-color: var(--border-hover);
}

.chart-container {
  height: 300px;
  position: relative;
}

/* Bottom Row */
.bottom-row {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 20px;
  width: 100%;
}

.activity-card,
.quick-actions-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: 16px;
  padding: 24px;
  width: 100%;
  box-sizing: border-box;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 10px;
}

.view-all-btn {
  padding: 6px 14px;
  background: transparent;
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.view-all-btn:hover {
  background: var(--surface-hover);
  border-color: var(--border-hover);
  color: var(--text-primary);
}

/* Activity List */
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.activity-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  background: var(--surface-hover);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  transition: all 0.2s;
}

.activity-item:hover {
  border-color: var(--border-hover);
}

.activity-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.activity-icon.user {
  background: rgba(102, 126, 234, 0.15);
  color: #667eea;
}

.activity-icon.system {
  background: rgba(67, 233, 123, 0.15);
  color: #43e97b;
}

.activity-icon.report {
  background: rgba(240, 147, 251, 0.15);
  color: #f093fb;
}

.activity-icon.settings {
  background: rgba(79, 172, 254, 0.15);
  color: #4facfe;
}

.activity-content {
  flex: 1;
  min-width: 0;
}

.activity-text {
  font-size: 14px;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.activity-time {
  font-size: 12px;
  color: var(--text-muted);
}

/* Quick Actions */
.actions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.action-btn {
  padding: 16px;
  background: var(--surface-hover);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 10px;
}

.action-btn:hover {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
  border-color: #667eea;
  color: #667eea;
  transform: translateY(-2px);
}

/* Responsive Design */
@media (max-width: 1600px) {
  .stats-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .charts-row {
    grid-template-columns: 1fr;
  }
  
  .bottom-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .dashboard-wrapper {
    padding: 16px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }
}
</style>
