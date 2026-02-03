<template>
  <div class="portal-dashboard">
    <div class="welcome-section">
      <h1>Hoş Geldiniz</h1>
      <p class="subtitle">Hesap özetiniz ve son aktiviteleriniz</p>
    </div>

    <!-- Quick Stats -->
    <div class="quick-stats">
      <div class="stat-card">
        <div class="stat-icon appointments">
          <Calendar :size="24" />
        </div>
        <div class="stat-info">
          <span class="stat-label">Aktif Randevular</span>
          <span class="stat-value">{{ stats.appointments }}</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon messages">
          <MessageSquare :size="24" />
        </div>
        <div class="stat-info">
          <span class="stat-label">Mesajlar</span>
          <span class="stat-value">{{ stats.messages }}</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon calls">
          <Phone :size="24" />
        </div>
        <div class="stat-info">
          <span class="stat-label">Aramalar</span>
          <span class="stat-value">{{ stats.calls }}</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon subscription">
          <CreditCard :size="24" />
        </div>
        <div class="stat-info">
          <span class="stat-label">Abonelik</span>
          <span class="stat-value">{{ subscription?.card_name || 'Yok' }}</span>
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="activity-section">
      <h2>Son Aktiviteler</h2>
      <div class="activity-list">
        <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
          <div class="activity-icon" :class="activity.type">
            <component :is="getActivityIcon(activity.type)" :size="20" />
          </div>
          <div class="activity-content">
            <p class="activity-title">{{ activity.title }}</p>
            <span class="activity-time">{{ formatTime(activity.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="quick-actions">
      <h2>Hızlı Erişim</h2>
      <div class="actions-grid">
        <button class="action-btn" @click="$router.push('/portal/appointments')">
          <Calendar :size="24" />
          <span>Randevularım</span>
        </button>
        <button class="action-btn" @click="$router.push('/portal/messages')">
          <MessageSquare :size="24" />
          <span>Mesajlar</span>
        </button>
        <button class="action-btn" @click="$router.push('/portal/calls')">
          <Phone :size="24" />
          <span>Aramalar</span>
        </button>
        <button class="action-btn" @click="$router.push('/portal/subscription')">
          <CreditCard :size="24" />
          <span>Abonelik</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Calendar, MessageSquare, Phone, CreditCard, Clock } from 'lucide-vue-next'
import api from '@/config/api'

const stats = ref({
  appointments: 0,
  messages: 0,
  calls: 0
})

const subscription = ref(null)
const recentActivities = ref([])

const loadDashboardData = async () => {
  try {
    // Load appointments count
    const appointmentsRes = await api.get('/portal/appointments?limit=100')
    stats.value.appointments = appointmentsRes.data.length

    // Load messages count
    const messagesRes = await api.get('/portal/messages?limit=100')
    stats.value.messages = messagesRes.data.length

    // Load calls count
    const callsRes = await api.get('/portal/calls?limit=100')
    stats.value.calls = callsRes.data.length

    // Load subscription
    const subRes = await api.get('/portal/subscription')
    subscription.value = subRes.data

    // Combine recent activities
    recentActivities.value = [
      ...appointmentsRes.data.slice(0, 3).map(a => ({
        id: a.id,
        type: 'appointment',
        title: a.title,
        created_at: a.date
      })),
      ...messagesRes.data.slice(0, 3).map(m => ({
        id: m.id,
        type: 'message',
        title: m.message.substring(0, 50) + '...',
        created_at: m.created_at
      })),
      ...callsRes.data.slice(0, 3).map(c => ({
        id: c.id,
        type: 'call',
        title: `Arama - ${c.duration}s`,
        created_at: c.created_at
      }))
    ].sort((a, b) => new Date(b.created_at) - new Date(a.created_at)).slice(0, 10)

  } catch (error) {
    console.error('Dashboard verileri yüklenemedi:', error)
  }
}

const getActivityIcon = (type) => {
  const icons = {
    appointment: Calendar,
    message: MessageSquare,
    call: Phone
  }
  return icons[type] || Clock
}

const formatTime = (date) => {
  const d = new Date(date)
  const now = new Date()
  const diff = now - d
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)

  if (days > 0) return `${days} gün önce`
  if (hours > 0) return `${hours} saat önce`
  if (minutes > 0) return `${minutes} dakika önce`
  return 'Az önce'
}

onMounted(() => {
  loadDashboardData()
})
</script>

<style scoped>
.portal-dashboard {
  padding: 32px;
  max-width: 1400px;
  margin: 0 auto;
}

.welcome-section {
  margin-bottom: 32px;
}

.welcome-section h1 {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
  letter-spacing: var(--letter-spacing-tight);
}

.subtitle {
  color: var(--text-secondary);
  font-size: 14px;
}

.quick-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all var(--transition-base);
}

.stat-card:hover {
  border-color: var(--border-hover);
  transform: translateY(-2px);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon.appointments {
  background: rgba(99, 102, 241, 0.1);
  color: var(--indigo-primary);
}

.stat-icon.messages {
  background: rgba(16, 185, 129, 0.1);
  color: var(--emerald-primary);
}

.stat-icon.calls {
  background: rgba(245, 158, 11, 0.1);
  color: var(--gold-primary);
}

.stat-icon.subscription {
  background: rgba(168, 85, 247, 0.1);
  color: #a855f7;
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
}

.activity-section,
.quick-actions {
  margin-bottom: 32px;
}

.activity-section h2,
.quick-actions h2 {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 16px;
}

.activity-list {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 24px;
  border-bottom: 1px solid var(--border-subtle);
  transition: background var(--transition-base);
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-item:hover {
  background: var(--surface-hover);
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.activity-icon.appointment {
  background: rgba(99, 102, 241, 0.1);
  color: var(--indigo-primary);
}

.activity-icon.message {
  background: rgba(16, 185, 129, 0.1);
  color: var(--emerald-primary);
}

.activity-icon.call {
  background: rgba(245, 158, 11, 0.1);
  color: var(--gold-primary);
}

.activity-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.activity-title {
  font-size: 14px;
  color: var(--text-primary);
  font-weight: 500;
}

.activity-time {
  font-size: 12px;
  color: var(--text-secondary);
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 24px;
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  color: var(--text-primary);
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
}

.action-btn:hover {
  background: var(--surface-hover);
  border-color: var(--border-hover);
  transform: translateY(-2px);
}

.action-btn svg {
  color: var(--indigo-primary);
}

@media (max-width: 768px) {
  .portal-dashboard {
    padding: 16px;
  }

  .quick-stats {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
