<template>
  <section class="secretary-content">
    <div class="content-grid">
      <!-- Quick Actions -->
      <div class="quick-actions-card">
        <div class="card-header">
          <h3 class="card-title">
            <Zap :size="20" :stroke-width="2" class="title-icon" />
            Hızlı İşlemler
          </h3>
        </div>
        <div class="actions-grid">
          <button 
            v-for="action in quickActions" 
            :key="action.id"
            class="action-button"
            :style="{ '--action-color': action.color }"
          >
            <component :is="action.icon" :size="24" :stroke-width="2" />
            <span class="action-label">{{ action.label }}</span>
          </button>
        </div>
      </div>

      <!-- Live Appointment Stream -->
      <div class="appointment-stream-card">
        <div class="card-header">
          <h3 class="card-title">
            <Clock :size="20" :stroke-width="2" class="title-icon" />
            Bugünkü Randevular
          </h3>
          <span class="live-badge">
            <span class="live-dot"></span>
            Canlı
          </span>
        </div>
        
        <div v-if="isLoading" class="appointment-timeline">
           <div v-for="i in 5" :key="i" class="appointment-item">
             <SkeletonLoader width="60px" height="20px" />
             <div class="appointment-indicator">
               <div class="indicator-dot"></div>
             </div>
             <div class="appointment-details" style="width: 100%">
               <SkeletonLoader width="150px" height="20px" style="margin-bottom: 8px" />
               <SkeletonLoader width="100px" height="16px" />
             </div>
           </div>
        </div>

        <div v-else class="appointment-timeline">
          <div 
            v-for="appointment in appointments" 
            :key="appointment.id"
            class="appointment-item"
            :class="appointment.status"
          >
            <div class="appointment-time">{{ formatTime(appointment.start_time) }}</div>
            <div class="appointment-indicator">
              <div class="indicator-dot"></div>
              <div class="indicator-line"></div>
            </div>
            <div class="appointment-details">
              <div class="appointment-patient">{{ appointment.customer_name || 'Misafir' }}</div>
              <div class="appointment-type">{{ appointment.notes || 'Genel Muayene' }}</div>
              <div class="appointment-status-badge" :class="appointment.status.toLowerCase()">
                {{ getStatusLabel(appointment.status) }}
              </div>
            </div>
          </div>
          <div v-if="appointments.length === 0" class="empty-state">
            <p>Bugün için randevu bulunamadı.</p>
          </div>
        </div>
      </div>

      <!-- Pending Approvals -->
      <div class="approvals-card">
        <div class="card-header">
          <h3 class="card-title">
            <AlertCircle :size="20" :stroke-width="2" class="title-icon" />
            Bekleyen Onaylar
          </h3>
          <span class="count-badge">{{ pendingApprovals.length }}</span>
        </div>
        <div class="approvals-list">
          <div 
            v-for="approval in pendingApprovals" 
            :key="approval.id"
            class="approval-item"
          >
            <div class="approval-info">
              <component :is="approval.icon" :size="18" :stroke-width="2" class="approval-icon" />
              <div class="approval-details">
                <span class="approval-title">{{ approval.title }}</span>
                <span class="approval-meta">{{ approval.submittedBy }} • {{ approval.time }}</span>
              </div>
            </div>
            <div class="approval-actions">
              <button class="approve-btn" title="Onayla">
                <Check :size="16" :stroke-width="2.5" />
              </button>
              <button class="reject-btn" title="Reddet">
                <X :size="16" :stroke-width="2.5" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Today's Stats -->
      <div class="stats-card">
        <div class="card-header">
          <h3 class="card-title">
            <BarChart3 :size="20" :stroke-width="2" class="title-icon" />
            Bugünkü Özet
          </h3>
        </div>
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-icon">
              <Users :size="20" :stroke-width="2" />
            </div>
            <div class="stat-value">
               <span v-if="!isLoading">{{ stats.total_appointments }}</span>
               <SkeletonLoader v-else width="40px" height="32px" />
            </div>
            <div class="stat-label">Toplam Randevu</div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">
              <CheckCircle2 :size="20" :stroke-width="2" />
            </div>
            <div class="stat-value">
               <span v-if="!isLoading">{{ stats.completed_appointments }}</span>
               <SkeletonLoader v-else width="40px" height="32px" />
            </div>
            <div class="stat-label">Tamamlanan</div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">
              <Clock :size="20" :stroke-width="2" />
            </div>
            <div class="stat-value">
               <span v-if="!isLoading">{{ stats.waiting_appointments }}</span>
               <SkeletonLoader v-else width="40px" height="32px" />
            </div>
            <div class="stat-label">Bekliyor</div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">
              <XCircle :size="20" :stroke-width="2" />
            </div>
            <div class="stat-value">
               <span v-if="!isLoading">{{ stats.cancelled_appointments }}</span>
               <SkeletonLoader v-else width="40px" height="32px" />
            </div>
            <div class="stat-label">İptal</div>
          </div>
        </div>
      </div>

      <!-- Recent Registrations -->
      <div class="registrations-card">
        <div class="card-header">
          <h3 class="card-title">
            <UserPlus :size="20" :stroke-width="2" class="title-icon" />
            Son Kayıtlar
          </h3>
        </div>
        <div class="registrations-list">
          <div 
            v-for="registration in recentRegistrations" 
            :key="registration.id"
            class="registration-item"
          >
            <div class="registration-avatar">{{ registration.initials }}</div>
            <div class="registration-info">
              <span class="registration-name">{{ registration.name }}</span>
              <span class="registration-time">{{ registration.time }}</span>
            </div>
            <span class="registration-type">{{ registration.type }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted, inject } from 'vue'
import SkeletonLoader from './SkeletonLoader.vue'
import { 
  Zap,
  Clock,
  AlertCircle,
  BarChart3,
  Users,
  CheckCircle2,
  XCircle,
  UserPlus,
  UserCircle,
  Calendar,
  CreditCard,
  FileText,
  Check,
  X
} from 'lucide-vue-next'

// Inject axios (or use import)
const axios = inject('axios')

const isLoading = ref(true)
const appointments = ref([])
const stats = ref({
  total_appointments: 0,
  completed_appointments: 0,
  waiting_appointments: 0,
  cancelled_appointments: 0
})

const quickActions = ref([
  { id: 1, label: 'Yeni Hasta', icon: UserCircle, color: '#6366f1' },
  { id: 2, label: 'Randevu Oluştur', icon: Calendar, color: '#8b5cf6' },
  { id: 3, label: 'Ödeme Kaydet', icon: CreditCard, color: '#a855f7' },
  { id: 4, label: 'Rapor Yazdır', icon: FileText, color: '#c084fc' }
])

const pendingApprovals = ref([
  { id: 1, title: 'Hasta Dosyası Güncelleme', submittedBy: 'Dr. Ahmet', time: '5 dk önce', icon: FileText },
  { id: 2, title: 'İlaç Reçetesi Onayı', submittedBy: 'Dr. Zeynep', time: '12 dk önce', icon: FileText },
  { id: 3, title: 'Randevu Değişikliği', submittedBy: 'Resepsiyon', time: '25 dk önce', icon: Calendar }
])

const recentRegistrations = ref([
  { id: 1, name: 'Elif Yıldız', initials: 'EY', time: '10 dk önce', type: 'Yeni Hasta' },
  { id: 2, name: 'Burak Öztürk', initials: 'BÖ', time: '25 dk önce', type: 'Randevu' },
  { id: 3, name: 'Selin Aydın', initials: 'SA', time: '1 saat önce', type: 'Ödeme' }
])

const getStatusLabel = (status) => {
  if (!status) return ''
  // Handle backend enum values
  const labels = {
    'PENDING': 'Bekliyor',
    'CONFIRMED': 'Onaylandı',
    'COMPLETED': 'Tamamlandı',
    'CANCELLED': 'İptal',
    'completed': 'Tamamlandı',
    'in-progress': 'Devam Ediyor',
    'waiting': 'Bekliyor',
    'scheduled': 'Planlandı'
  }
  return labels[status.toUpperCase()] || labels[status] || status
}

const formatTime = (isoString) => {
  if (!isoString) return '--:--'
  try {
    return new Date(isoString).toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })
  } catch (e) {
    return isoString
  }
}

const fetchData = async () => {
  try {
    const today = new Date().toISOString().split('T')[0]
    
    const [apptRes, statsRes] = await Promise.all([
      axios.get('/appointments', {
        params: {
          start_date: today,
          limit: 10
        }
      }),
      axios.get('/analytics/stats')
    ])
    
    appointments.value = apptRes.data
    stats.value = statsRes.data
    
  } catch (error) {
    console.error('Failed to fetch dashboard data:', error)
  } finally {
    isLoading.value = false
  }
}

let pollInterval

onMounted(() => {
  fetchData()
  // Poll every 30 seconds
  pollInterval = setInterval(fetchData, 30000)
})

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval)
})
</script>

<style scoped>
.secretary-content {
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

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
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

/* Quick Actions Card */
.quick-actions-card {
  grid-column: span 2;
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 24px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 16px;
}

.action-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 24px 16px;
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);
  color: var(--text-primary);
  font-family: var(--font-family);
}

.action-button:hover {
  background: var(--surface-hover);
  border-color: var(--action-color);
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3),
              0 0 32px var(--indigo-glow);
}

.action-button svg {
  color: var(--action-color);
}

.action-label {
  font-size: 14px;
  font-weight: 500;
  letter-spacing: var(--letter-spacing-normal);
}

/* Appointment Stream Card */
.appointment-stream-card {
  grid-column: span 2;
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 24px;
}

.live-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  background: rgba(34, 197, 94, 0.15);
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  color: #22c55e;
}

.live-dot {
  width: 6px;
  height: 6px;
  background: #22c55e;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.2); }
}

.appointment-timeline {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.appointment-item {
  display: grid;
  grid-template-columns: 60px 40px 1fr;
  gap: 16px;
  padding: 16px 0;
  border-bottom: 1px solid var(--border-subtle);
}

.appointment-item:last-child {
  border-bottom: none;
}

.appointment-time {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  letter-spacing: var(--letter-spacing-normal);
}

.appointment-indicator {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.indicator-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--border-subtle);
  border: 2px solid var(--obsidian-black);
  z-index: 1;
}

.appointment-item.completed .indicator-dot {
  background: #22c55e;
  box-shadow: 0 0 12px rgba(34, 197, 94, 0.5);
}

.appointment-item.in-progress .indicator-dot {
  background: #f59e0b;
  box-shadow: 0 0 12px rgba(245, 158, 11, 0.5);
  animation: pulse 2s ease-in-out infinite;
}

.appointment-item.waiting .indicator-dot {
  background: var(--indigo-primary);
  box-shadow: 0 0 12px var(--indigo-glow);
}

.indicator-line {
  flex: 1;
  width: 2px;
  background: var(--border-subtle);
  margin-top: 4px;
}

.appointment-item:last-child .indicator-line {
  display: none;
}

.appointment-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.appointment-patient {
  font-size: 15px;
  font-weight: 600;
  letter-spacing: var(--letter-spacing-normal);
}

.appointment-type {
  font-size: 13px;
  color: var(--text-secondary);
}

.appointment-status-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 600;
  width: fit-content;
  margin-top: 4px;
}

.appointment-status-badge.completed {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}

.appointment-status-badge.in-progress {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.appointment-status-badge.waiting {
  background: var(--indigo-glow);
  color: var(--indigo-primary);
}

.appointment-status-badge.scheduled {
  background: var(--surface-hover);
  color: var(--text-secondary);
}

/* Approvals Card */
.approvals-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 24px;
}

.count-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  height: 24px;
  padding: 0 8px;
  background: rgba(239, 68, 68, 0.15);
  border-radius: 12px;
  font-size: 12px;
  font-weight: 700;
  color: #ef4444;
}

.approvals-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.approval-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  background: var(--surface-hover);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  transition: all var(--transition-fast);
}

.approval-item:hover {
  border-color: var(--border-hover);
  box-shadow: 0 0 16px var(--indigo-glow);
}

.approval-info {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.approval-icon {
  color: var(--indigo-primary);
  flex-shrink: 0;
}

.approval-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.approval-title {
  font-size: 14px;
  font-weight: 500;
  letter-spacing: var(--letter-spacing-normal);
}

.approval-meta {
  font-size: 12px;
  color: var(--text-muted);
}

.approval-actions {
  display: flex;
  gap: 8px;
}

.approve-btn,
.reject-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.approve-btn {
  background: transparent;
  color: var(--text-secondary);
}

.approve-btn:hover {
  background: #22c55e;
  border-color: #22c55e;
  color: white;
  box-shadow: 0 0 16px rgba(34, 197, 94, 0.4);
}

.reject-btn {
  background: transparent;
  color: var(--text-secondary);
}

.reject-btn:hover {
  background: #ef4444;
  border-color: #ef4444;
  color: white;
  box-shadow: 0 0 16px rgba(239, 68, 68, 0.4);
}

/* Stats Card */
.stats-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 24px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px;
  background: var(--surface-hover);
  border-radius: var(--radius-sm);
}

.stat-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--indigo-primary), #8b5cf6);
  border-radius: var(--radius-sm);
  color: white;
  box-shadow: 0 0 16px var(--indigo-glow);
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  letter-spacing: var(--letter-spacing-tight);
}

.stat-label {
  font-size: 12px;
  color: var(--text-muted);
  text-align: center;
}

/* Registrations Card */
.registrations-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 24px;
}

.registrations-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.registration-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--surface-hover);
  border-radius: var(--radius-sm);
  transition: all var(--transition-fast);
}

.registration-item:hover {
  background: var(--surface-elevated);
  box-shadow: 0 0 16px var(--indigo-glow);
}

.registration-avatar {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--indigo-primary), #8b5cf6);
  border-radius: 50%;
  font-weight: 600;
  font-size: 14px;
  color: white;
  box-shadow: 0 0 12px var(--indigo-glow);
}

.registration-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.registration-name {
  font-size: 14px;
  font-weight: 500;
  letter-spacing: var(--letter-spacing-normal);
}

.registration-time {
  font-size: 12px;
  color: var(--text-muted);
}

.registration-type {
  font-size: 12px;
  padding: 4px 8px;
  background: var(--indigo-glow);
  color: var(--indigo-primary);
  border-radius: 8px;
  font-weight: 600;
}
</style>
