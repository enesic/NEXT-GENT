<template>
  <div class="satisfaction-dashboard">
    <!-- Header -->
    <div class="dashboard-header">
      <h2>Müşteri Memnuniyet Analizi</h2>
      <div class="period-selector">
        <button 
          v-for="period in periods" 
          :key="period.value"
          :class="['period-btn', { active: selectedPeriod === period.value }]"
          @click="selectedPeriod = period.value; fetchData()"
        >
          {{ period.label }}
        </button>
      </div>
    </div>

    <!-- Key Metrics Cards -->
    <div class="metrics-grid">
      <div class="metric-card nps">
        <div class="metric-header">
          <h3>NPS Score</h3>
          <TrendingUp :size="20" :stroke-width="2" />
        </div>
        <div class="metric-value">{{ npsScore }}</div>
        <div class="metric-details">
          <span>Promoters: {{ promoters }}</span>
          <span>Detractors: {{ detractors }}</span>
        </div>
      </div>

      <div class="metric-card csat">
        <div class="metric-header">
          <h3>CSAT Average</h3>
          <Star :size="20" :stroke-width="2" />
        </div>
        <div class="metric-value">{{ csatAverage }}</div>
        <div class="metric-details">
          <span>{{ totalResponses }} responses</span>
        </div>
      </div>

      <div class="metric-card sentiment">
        <div class="metric-header">
          <h3>Sentiment</h3>
          <Heart :size="20" :stroke-width="2" />
        </div>
        <div class="sentiment-distribution">
          <div class="sentiment-item positive">
            <span class="label">Positive</span>
            <span class="value">{{ sentimentDist.positive }}</span>
          </div>
          <div class="sentiment-item neutral">
            <span class="label">Neutral</span>
            <span class="value">{{ sentimentDist.neutral }}</span>
          </div>
          <div class="sentiment-item negative">
            <span class="label">Negative</span>
            <span class="value">{{ sentimentDist.negative }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts -->
    <div class="charts-grid">
      <!-- Satisfaction Trends -->
      <div class="chart-card">
        <h3>Satisfaction Trends</h3>
        <apexchart
          type="line"
          height="350"
          :options="trendChartOptions"
          :series="trendSeries"
        />
      </div>

      <!-- Sentiment Distribution -->
      <div class="chart-card">
        <h3>Sentiment Distribution</h3>
        <apexchart
          type="pie"
          height="350"
          :options="sentimentChartOptions"
          :series="sentimentSeries"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { TrendingUp, Star, Heart } from 'lucide-vue-next'
import { inject } from 'vue'

const axios = inject('axios')

// State
const selectedPeriod = ref(30)
const npsScore = ref(0)
const csatAverage = ref(0)
const promoters = ref(0)
const detractors = ref(0)
const totalResponses = ref(0)
const sentimentDist = ref({
  positive: 0,
  neutral: 0,
  negative: 0
})
const trends = ref({
  series: [],
  categories: []
})

// Periods
const periods = [
  { label: '7 Days', value: 7 },
  { label: '30 Days', value: 30 },
  { label: '90 Days', value: 90 },
  { label: '1 Year', value: 365 }
]

// Chart Options
const trendChartOptions = computed(() => ({
  chart: {
    type: 'line',
    toolbar: { show: false },
    zoom: { enabled: false }
  },
  colors: ['#6366f1', '#10b981'],
  stroke: {
    curve: 'smooth',
    width: 3
  },
  xaxis: {
    categories: trends.value.categories,
    labels: {
      style: { colors: '#a1a1aa' }
    }
  },
  yaxis: {
    labels: {
      style: { colors: '#a1a1aa' }
    }
  },
  legend: {
    labels: {
      colors: '#ffffff'
    }
  },
  grid: {
    borderColor: 'rgba(255, 255, 255, 0.1)'
  },
  theme: {
    mode: 'dark'
  }
}))

const trendSeries = computed(() => trends.value.series || [])

const sentimentChartOptions = computed(() => ({
  chart: {
    type: 'pie',
    toolbar: { show: false }
  },
  colors: ['#10b981', '#f59e0b', '#ef4444'],
  labels: ['Positive', 'Neutral', 'Negative'],
  legend: {
    labels: {
      colors: '#ffffff'
    }
  },
  theme: {
    mode: 'dark'
  }
}))

const sentimentSeries = computed(() => [
  sentimentDist.value.positive,
  sentimentDist.value.neutral,
  sentimentDist.value.negative
])

// Methods
const fetchData = async () => {
  try {
    // Fetch metrics
    const metricsRes = await axios.get('/satisfaction/metrics', {
      params: {
        days: selectedPeriod.value
      }
    })
    
    const metrics = metricsRes.data
    npsScore.value = metrics.nps?.score || 0
    promoters.value = metrics.nps?.promoters || 0
    detractors.value = metrics.nps?.detractors || 0
    csatAverage.value = metrics.csat?.average || 0
    totalResponses.value = metrics.csat?.total_responses || 0
    sentimentDist.value = metrics.sentiment || { positive: 0, neutral: 0, negative: 0 }
    
    // Fetch trends
    const trendsRes = await axios.get('/satisfaction/trends', {
      params: {
        days: selectedPeriod.value
      }
    })
    
    trends.value = trendsRes.data || { series: [], categories: [] }
    
  } catch (error) {
    console.error('Satisfaction data fetch error:', error)
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.satisfaction-dashboard {
  display: flex;
  flex-direction: column;
  gap: 32px;
  padding: 32px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dashboard-header h2 {
  font-size: 24px;
  font-weight: 700;
}

.period-selector {
  display: flex;
  gap: 8px;
}

.period-btn {
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #a1a1aa;
  cursor: pointer;
  transition: all 0.2s;
}

.period-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.period-btn.active {
  background: #6366f1;
  border-color: #6366f1;
  color: white;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.metric-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 24px;
}

.metric-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.metric-header h3 {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
}

.metric-value {
  font-size: 36px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.metric-details {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: var(--text-muted);
}

.sentiment-distribution {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.sentiment-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 12px;
  border-radius: 8px;
}

.sentiment-item.positive {
  background: rgba(16, 185, 129, 0.1);
}

.sentiment-item.neutral {
  background: rgba(245, 158, 11, 0.1);
}

.sentiment-item.negative {
  background: rgba(239, 68, 68, 0.1);
}

.charts-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

.chart-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 24px;
}

.chart-card h3 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 24px;
}

@media (max-width: 1024px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
}
</style>
