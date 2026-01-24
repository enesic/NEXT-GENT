<template>
  <div class="callcenter-dashboard">
    <!-- Header -->
    <div class="dashboard-header">
      <h2>Call Center Dashboard</h2>
      <div class="refresh-controls">
        <button class="refresh-btn" @click="fetchData">
          <RefreshCw :size="16" :stroke-width="2" :class="{ spinning: isRefreshing }" />
          Refresh
        </button>
        <span class="last-update">Last update: {{ lastUpdate }}</span>
      </div>
    </div>

    <!-- Key Metrics -->
    <div class="metrics-grid">
      <div class="metric-card">
        <div class="metric-header">
          <h3>Active Calls</h3>
          <Phone :size="20" :stroke-width="2" />
        </div>
        <div class="metric-value">{{ activeCallsCount }}</div>
      </div>

      <div class="metric-card">
        <div class="metric-header">
          <h3>Total Calls (30d)</h3>
          <TrendingUp :size="20" :stroke-width="2" />
        </div>
        <div class="metric-value">{{ callMetrics.total_calls }}</div>
      </div>

      <div class="metric-card">
        <div class="metric-header">
          <h3>Avg Duration</h3>
          <Clock :size="20" :stroke-width="2" />
        </div>
        <div class="metric-value">{{ formatDuration(callMetrics.average_duration_seconds) }}</div>
      </div>

      <div class="metric-card">
        <div class="metric-header">
          <h3>Positive Sentiment</h3>
          <Smile :size="20" :stroke-width="2" />
        </div>
        <div class="metric-value">{{ callMetrics.positive_sentiment_percentage }}%</div>
      </div>
    </div>

    <!-- Active Calls List -->
    <div class="active-calls-section">
      <h3>Active Calls</h3>
      <div v-if="activeCalls.length === 0" class="empty-state">
        <PhoneOff :size="48" :stroke-width="2" />
        <p>No active calls</p>
      </div>
      <div v-else class="calls-list">
        <div 
          v-for="call in activeCalls" 
          :key="call.call_id"
          class="call-card"
        >
          <div class="call-info">
            <div class="call-header">
              <div class="caller-info">
                <div class="caller-avatar">{{ getInitials(call.customer_name) }}</div>
                <div>
                  <div class="caller-name">{{ call.customer_name }}</div>
                  <div class="caller-phone">{{ call.customer_phone }}</div>
                </div>
              </div>
              <div class="call-status">
                <div class="status-dot active"></div>
                <span>Active</span>
              </div>
            </div>
            <div class="call-details">
              <div class="detail-item">
                <Clock :size="14" :stroke-width="2" />
                <span>{{ formatDuration(call.duration_seconds) }}</span>
              </div>
              <div class="detail-item" v-if="call.sentiment">
                <Smile :size="14" :stroke-width="2" />
                <span>{{ call.sentiment }}</span>
              </div>
            </div>
            <div v-if="call.transcript" class="call-transcript">
              <p>{{ call.transcript }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Call History -->
    <div class="call-history-section">
      <h3>Recent Calls</h3>
      <div class="history-table">
        <table>
          <thead>
            <tr>
              <th>Customer</th>
              <th>Duration</th>
              <th>Sentiment</th>
              <th>Status</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="call in callHistory" :key="call.call_id">
              <td>
                <div class="customer-cell">
                  <div class="customer-avatar">{{ getInitials(call.customer_name) }}</div>
                  <div>
                    <div class="customer-name">{{ call.customer_name }}</div>
                    <div class="customer-phone">{{ call.customer_phone }}</div>
                  </div>
                </div>
              </td>
              <td>{{ formatDuration(call.duration_seconds) }}</td>
              <td>
                <span :class="['sentiment-badge', call.sentiment]">
                  {{ call.sentiment || 'N/A' }}
                </span>
              </td>
              <td>
                <span :class="['status-badge', call.status]">
                  {{ call.status }}
                </span>
              </td>
              <td>{{ formatTime(call.started_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Phone, PhoneOff, Clock, TrendingUp, Smile, RefreshCw } from 'lucide-vue-next'
import { inject } from 'vue'

const axios = inject('axios')

// State
const activeCalls = ref([])
const activeCallsCount = ref(0)
const callHistory = ref([])
const callMetrics = ref({
  total_calls: 0,
  average_duration_seconds: 0,
  positive_sentiment_percentage: 0
})
const isRefreshing = ref(false)
const lastUpdate = ref('Never')
let refreshInterval = null

// Methods
const fetchData = async () => {
  isRefreshing.value = true
  try {
    // Fetch active calls
    const activeRes = await axios.get('/callcenter/active-calls')
    activeCalls.value = activeRes.data.active_calls || []
    activeCallsCount.value = activeRes.data.count || 0
    
    // Fetch call history
    const historyRes = await axios.get('/callcenter/call-history', {
      params: { limit: 20 }
    })
    callHistory.value = historyRes.data.calls || []
    
    // Fetch metrics
    const metricsRes = await axios.get('/callcenter/call-metrics', {
      params: { days: 30 }
    })
    callMetrics.value = metricsRes.data || {}
    
    lastUpdate.value = new Date().toLocaleTimeString('tr-TR')
  } catch (error) {
    console.error('Callcenter data fetch error:', error)
  } finally {
    isRefreshing.value = false
  }
}

const formatDuration = (seconds) => {
  if (!seconds) return '0:00'
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

const formatTime = (isoString) => {
  if (!isoString) return 'N/A'
  const date = new Date(isoString)
  return date.toLocaleString('tr-TR', {
    day: '2-digit',
    month: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getInitials = (name) => {
  if (!name) return '??'
  return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
}

onMounted(() => {
  fetchData()
  // Auto-refresh every 5 seconds
  refreshInterval = setInterval(fetchData, 5000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>

<style scoped>
.callcenter-dashboard {
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

.refresh-controls {
  display: flex;
  align-items: center;
  gap: 16px;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.3);
  border-radius: 8px;
  color: #818cf8;
  cursor: pointer;
  transition: all 0.2s;
}

.refresh-btn:hover {
  background: rgba(99, 102, 241, 0.2);
}

.refresh-btn .spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.last-update {
  font-size: 12px;
  color: var(--text-muted);
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
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
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
}

.active-calls-section,
.call-history-section {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 24px;
}

.active-calls-section h3,
.call-history-section h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 20px;
}

.empty-state {
  text-align: center;
  padding: 48px;
  color: var(--text-muted);
}

.empty-state p {
  margin-top: 16px;
  font-size: 14px;
}

.calls-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.call-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  padding: 20px;
}

.call-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.caller-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.caller-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  color: white;
}

.caller-name {
  font-weight: 600;
  font-size: 14px;
}

.caller-phone {
  font-size: 12px;
  color: var(--text-muted);
}

.call-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #10b981;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
  animation: pulse 2s infinite;
}

.status-dot.active {
  background: #10b981;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.call-details {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text-muted);
}

.call-transcript {
  margin-top: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 8px;
  font-size: 12px;
  color: var(--text-secondary);
  max-height: 100px;
  overflow-y: auto;
}

.history-table {
  overflow-x: auto;
}

.history-table table {
  width: 100%;
  border-collapse: collapse;
}

.history-table th,
.history-table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid var(--border-subtle);
}

.history-table th {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
}

.customer-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.customer-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(99, 102, 241, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 12px;
  color: #818cf8;
}

.sentiment-badge {
  padding: 4px 10px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 600;
}

.sentiment-badge.positive {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.sentiment-badge.neutral {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
}

.sentiment-badge.negative {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.status-badge {
  padding: 4px 10px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 600;
  text-transform: capitalize;
}

.status-badge.active {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.status-badge.completed {
  background: rgba(99, 102, 241, 0.1);
  color: #6366f1;
}

.status-badge.failed {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
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
  
  .history-table {
    font-size: 12px;
  }
}
</style>
