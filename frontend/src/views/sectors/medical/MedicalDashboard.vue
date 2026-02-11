<template>
  <DashboardLayout sector="medical" :sector-icon="Activity">
    <!-- Error State -->
    <ErrorState
      v-if="hasError && !isLoading"
      variant="network"
      title="Dashboard Yüklenemedi"
      message="Sunucuya bağlanılamadı. Lütfen internet bağlantınızı kontrol edin."
      @action="retry"
    />
    
    <!-- Loading State -->
    <template v-else-if="isLoading && !kpis">
      <section class="stats-grid">
        <SkeletonStatCard v-for="i in 4" :key="i" />
      </section>
    </template>
    
    <!-- Data Loaded -->
    <template v-else>
      <!-- Stats Overview -->
      <section class="stats-grid">
        <StatCard
          :icon="Users"
          label="Bugünkü Hastalar"
          :value="stats.todayPatients"
          change="+12.5%"
          changeType="positive"
          :gradient="theme.primaryGradient"
          @click="navigateTo('/patients/today')"
        />
        <StatCard
          :icon="Calendar"
          label="Aktif Randevular"
          :value="stats.activeAppointments"
          change="+8.3%"
          changeType="positive"
          :gradient="theme.primaryGradient"
          @click="navigateTo('/appointments')"
        />
        <StatCard
          :icon="TrendingUp"
          label="Haftalık Gelir"
          :value="`₺${stats.weeklyRevenue.toLocaleString('tr-TR')}`"
          change="+15.2%"
          changeType="positive"
          :gradient="theme.primaryGradient"
          :animated="false"
          @click="navigateTo('/revenue')"
        />
        <StatCard
          :icon="AlertCircle"
          label="Acil Durumlar"
          :value="stats.emergencies"
          change="-5.1%"
          changeType="positive"
          :gradient="'linear-gradient(135deg, #10b981, #34d399)'"
          @click="navigateTo('/emergencies')"
        />
      </section>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- Today's Appointments -->
      <section class="card">
        <ActivityFeed
          title="Bugünkü Randevular"
          :items="todayAppointments"
          @item-click="handleAppointmentClick"
          @view-all="navigateTo('/appointments')"
        />
      </section>

      <!-- Patient Flow Chart -->
      <section class="card chart-card">
        <div class="card-header">
          <h3 class="card-title">Hasta Akışı</h3>
          <div class="time-filters">
            <button 
              v-for="filter in timeFilters" 
              :key="filter.value"
              v-ripple
              class="filter-btn" 
              :class="{ active: selectedTimeFilter === filter.value }"
              @click="selectedTimeFilter = filter.value"
              :aria-pressed="selectedTimeFilter === filter.value"
              :aria-label="`Filter by ${filter.label}`"
            >
              {{ filter.label }}
            </button>
          </div>
        </div>
        <div class="chart-wrapper">
          <SkeletonChart v-if="patientFlowLoading || !patientFlowData" type="line" />
          <InteractiveChart
            v-else
            type="line"
            :data="patientFlowData"
            :gradient-colors="['rgba(239, 68, 68, 0.8)', 'rgba(239, 68, 68, 0.1)']"
          />
        </div>
      </section>

      <!-- Department Performance -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">Departman Performansı</h3>
        </div>
        <div class="department-list">
          <div 
            v-for="dept in departments" 
            :key="dept.id"
            v-ripple
            class="department-item"
            @click="handleDepartmentClick(dept)"
            role="button"
            tabindex="0"
            :aria-label="`View ${dept.name} department details`"
            @keydown.enter="handleDepartmentClick(dept)"
            @keydown.space.prevent="handleDepartmentClick(dept)"
          >
            <div class="dept-info">
              <div class="dept-icon" :style="{ background: dept.gradient }">
                <component :is="dept.icon" :size="20" />
              </div>
              <div>
                <p class="dept-name">{{ dept.name }}</p>
                <p class="dept-stats">{{ dept.patients }} hasta • {{ dept.doctors }} doktor</p>
              </div>
            </div>
            <div class="dept-progress">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: `${dept.efficiency}%`, background: dept.gradient }"></div>
              </div>
              <span class="progress-label">{{ dept.efficiency }}% verimlilik</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Emergency Alerts -->
      <section class="card emergency-card">
        <div class="card-header">
          <h3 class="card-title">
            <AlertCircle :size="20" :stroke-width="2" />
            Acil Durumlar
          </h3>
        </div>
        <div class="emergency-list">
          <div 
            v-for="emergency in emergencies" 
            :key="emergency.id"
            class="emergency-item"
            :class="`priority-${emergency.priority}`"
          >
            <div class="emergency-indicator"></div>
            <div class="emergency-content">
              <p class="emergency-patient">{{ emergency.patient }}</p>
              <p class="emergency-condition">{{ emergency.condition }}</p>
              <p class="emergency-time">{{ emergency.time }}</p>
            </div>
            <button 
              v-ripple
              class="btn-action" 
              @click="handleEmergency(emergency)"
              :aria-label="`View emergency details for ${emergency.patient}`"
            >
              Detay
            </button>
          </div>
        </div>
      </section>

      <!-- Staff Schedule -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">Doktor Programı</h3>
        </div>
        <div class="staff-schedule">
          <div 
            v-for="doctor in staffSchedule" 
            :key="doctor.id"
            class="staff-item"
          >
            <div class="staff-avatar" :style="{ background: doctor.avatarColor }">
              {{ doctor.name[0] }}
            </div>
            <div class="staff-info">
              <p class="staff-name">{{ doctor.name }}</p>
              <p class="staff-specialty">{{ doctor.specialty }}</p>
            </div>
            <div class="staff-status" :class="doctor.status">
              {{ doctor.statusText }}
            </div>
            <div class="staff-patients">
              <Users :size="14" />
              <span>{{ doctor.patientsToday }}</span>
            </div>
          </div>
        </div>
      </section>
    </div>
    </template>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Activity, Users, Calendar, TrendingUp, AlertCircle, 
  Heart, Brain, Stethoscope, Syringe, Clock
} from 'lucide-vue-next'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import StatCard from '@/components/dashboard/StatCard.vue'
import ActivityFeed from '@/components/dashboard/ActivityFeed.vue'
import InteractiveChart from '@/components/dashboard/InteractiveChart.vue'
import SkeletonStatCard from '@/components/common/SkeletonStatCard.vue'
import SkeletonChart from '@/components/common/SkeletonChart.vue'
import ErrorState from '@/components/common/ErrorState.vue'
import { useSectorTheme } from '@/composables/useSectorTheme'
import { useDashboardData } from '@/composables/useDashboardData'
import { useAnalyticsStore } from '@/stores/analytics'
import { vRipple } from '@/composables/useRipple'

const router = useRouter()
const { theme } = useSectorTheme('medical')
const analyticsStore = useAnalyticsStore()

// Fetch dashboard data with WebSocket support
const { kpis, pulse, isLoading, hasError, retry } = useDashboardData({
  enableWebSocket: true
})

// Transform backend KPIs to stats
const stats = computed(() => {
  if (!kpis.value || kpis.value.length === 0) {
    return {
      todayPatients: 0,
      activeAppointments: 0,
      weeklyRevenue: 0,
      emergencies: 0
    }
  }
  
  // Map KPIs to stat cards (backend returns sector-specific KPIs)
  return {
    todayPatients: pulse.value?.todayClients || 47,
    activeAppointments: pulse.value?.pendingAppointments || 23,
    weeklyRevenue: 125000, // TODO: Get from KPIs when available
    emergencies: 3 // TODO: Get from KPIs when available
  }
})

// Chart data states
const patientFlowData = ref(null)
const patientFlowLoading = ref(false)

// Time Filters
const timeFilters = [
  { label: '7 Gün', value: '7d' },
  { label: '30 Gün', value: '30d' },
  { label: '90 Gün', value: '90d' }
]
const selectedTimeFilter = ref('7d')

// Today's Appointments
const todayAppointments = ref([
  {
    id: 1,
    icon: Calendar,
    iconGradient: 'linear-gradient(135deg, #ef4444, #f87171)',
    title: 'Ahmet Yılmaz',
    subtitle: 'Kardiyoloji Kontrolü • 09:00',
    time: '30 dk',
    badge: 'Bekliyor',
    badgeType: 'warning'
  },
  {
    id: 2,
    icon: Calendar,
    iconGradient: 'linear-gradient(135deg, #10b981, #34d399)',
    title: 'Ayşe Demir',
    subtitle: 'Radyoloji Taraması • 10:30',
    time: '1 saat',
    badge: 'Tamamlandı',
    badgeType: 'success'
  },
  {
    id: 3,
    icon: Calendar,
    iconGradient: 'linear-gradient(135deg, #3b82f6, #60a5fa)',
    title: 'Mehmet Kaya',
    subtitle: 'Nöroloji Muayenesi • 14:00',
    time: '3 saat',
    badge: 'Planlandı',
    badgeType: 'info'
  }
])

// Patient Flow Data is now fetched from backend in onMounted

// Departments
const departments = ref([
  {
    id: 1,
    name: 'Kardiyoloji',
    icon: Heart,
    gradient: 'linear-gradient(135deg, #ef4444, #f87171)',
    patients: 18,
    doctors: 3,
    efficiency: 92
  },
  {
    id: 2,
    name: 'Nöroloji',
    icon: Brain,
    gradient: 'linear-gradient(135deg, #8b5cf6, #a78bfa)',
    patients: 12,
    doctors: 2,
    efficiency: 87
  },
  {
    id: 3,
    name: 'Genel Cerrahi',
    icon: Stethoscope,
    gradient: 'linear-gradient(135deg, #10b981, #34d399)',
    patients: 15,
    doctors: 4,
    efficiency: 95
  },
  {
    id: 4,
    name: 'Radyoloji',
    icon: Syringe,
    gradient: 'linear-gradient(135deg, #3b82f6, #60a5fa)',
    patients: 22,
    doctors: 2,
    efficiency: 89
  }
])

// Emergencies
const emergencies = ref([
  {
    id: 1,
    patient: 'Can Öztürk',
    condition: 'Kalp krizi şüphesi',
    time: '5 dakika önce',
    priority: 'high'
  },
  {
    id: 2,
    patient: 'Zeynep Arslan',
    condition: 'Solunum güçlüğü',
    time: '12 dakika önce',
    priority: 'medium'
  },
  {
    id: 3,
    patient: 'Ali Çelik',
    condition: 'Kırık şüphesi',
    time: '25 dakika önce',
    priority: 'low'
  }
])

// Staff Schedule
const staffSchedule = ref([
  {
    id: 1,
    name: 'Dr. Elif Yıldız',
    specialty: 'Kardiyolog',
    avatarColor: 'linear-gradient(135deg, #ef4444, #f87171)',
    status: 'available',
    statusText: 'Müsait',
    patientsToday: 8
  },
  {
    id: 2,
    name: 'Dr. Murat Aydın',
    specialty: 'Nörolog',
    avatarColor: 'linear-gradient(135deg, #8b5cf6, #a78bfa)',
    status: 'busy',
    statusText: 'Meşgul',
    patientsToday: 6
  },
  {
    id: 3,
    name: 'Dr. Selin Kara',
    specialty: 'Cerrah',
    avatarColor: 'linear-gradient(135deg, #10b981, #34d399)',
    status: 'surgery',
    statusText: 'Ameliyatta',
    patientsToday: 4
  }
])

// Methods
const navigateTo = (path) => {
  console.log('Navigate to:', path)
}

const handleAppointmentClick = (appointment) => {
  console.log('Appointment clicked:', appointment)
}

const handleDepartmentClick = (dept) => {
  console.log('Department clicked:', dept)
}

const handleEmergency = (emergency) => {
  console.log('Emergency:', emergency)
}

// Fetch chart data
const fetchChartData = async () => {
  patientFlowLoading.value = true
  try {
    const endDate = new Date().toISOString()
    const startDate = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString()
    
    const response = await analyticsStore.fetchChart('unique-person-count', startDate, endDate)
    patientFlowData.value = response
  } catch (error) {
    console.error('Failed to load patient flow chart:', error)
    patientFlowData.value = {
      labels: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
      datasets: [{
        label: 'Hasta Sayısı',
        data: [42, 38, 51, 47, 55, 32, 28]
      }]
    }
  } finally {
    patientFlowLoading.value = false
  }
}

onMounted(() => {
  fetchChartData()
})
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 24px;
}

.card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 24px;
  transition: all 0.3s;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  border-color: rgba(255, 255, 255, 0.12);
}

.card:nth-child(1) { grid-column: span 4; }
.card:nth-child(2) { grid-column: span 8; }
.card:nth-child(3) { grid-column: span 6; }
.card:nth-child(4) { grid-column: span 6; }
.card:nth-child(5) { grid-column: span 12; }

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: white;
  display: flex;
  align-items: center;
  gap: 8px;
}

.time-filters {
  display: flex;
  gap: 8px;
}

.filter-btn {
  padding: 6px 14px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: #9ca3af;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  color: white;
}

.filter-btn.active {
  background: var(--sector-gradient);
  color: white;
  border-color: transparent;
}

.chart-wrapper {
  height: 300px;
}

/* Department List */
.department-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.department-item {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.department-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  transform: translateX(4px);
}

.dept-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.dept-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.dept-name {
  font-size: 14px;
  font-weight: 600;
  color: white;
  margin: 0 0 4px 0;
}

.dept-stats {
  font-size: 12px;
  color: #9ca3af;
  margin: 0;
}

.dept-progress {
  display: flex;
  align-items: center;
  gap: 12px;
}

.progress-bar {
  flex: 1;
  height: 6px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

.progress-label {
  font-size: 12px;
  color: #9ca3af;
  font-weight: 600;
  min-width: 90px;
  text-align: right;
}

/* Emergency List */
.emergency-card {
  border-color: rgba(239, 68, 68, 0.2);
}

.emergency-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.emergency-item {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
  overflow: hidden;
}

.emergency-indicator {
  width: 4px;
  height: 100%;
  position: absolute;
  left: 0;
  top: 0;
  border-radius: 2px 0 0 2px;
}

.emergency-item.priority-high .emergency-indicator {
  background: #ef4444;
  box-shadow: 0 0 12px rgba(239, 68, 68, 0.5);
}

.emergency-item.priority-medium .emergency-indicator {
  background: #f59e0b;
}

.emergency-item.priority-low .emergency-indicator {
  background: #10b981;
}

.emergency-content {
  flex: 1;
  padding-left: 8px;
}

.emergency-patient {
  font-size: 14px;
  font-weight: 600;
  color: white;
  margin: 0 0 4px 0;
}

.emergency-condition {
  font-size: 13px;
  color: #9ca3af;
  margin: 0 0 4px 0;
}

.emergency-time {
  font-size: 11px;
  color: #6b7280;
  margin: 0;
}

.btn-action {
  padding: 8px 16px;
  border-radius: 8px;
  background: var(--sector-gradient);
  border: none;
  color: white;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-action:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(239, 68, 68, 0.3);
}

/* Staff Schedule */
.staff-schedule {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.staff-item {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.staff-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 16px;
}

.staff-info {
  flex: 1;
}

.staff-name {
  font-size: 14px;
  font-weight: 600;
  color: white;
  margin: 0 0 4px 0;
}

.staff-specialty {
  font-size: 12px;
  color: #9ca3af;
  margin: 0;
}

.staff-status {
  padding: 6px 12px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 600;
}

.staff-status.available {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.staff-status.busy {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.staff-status.surgery {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.staff-patients {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #9ca3af;
  font-size: 13px;
  font-weight: 600;
}

@media (max-width: 1200px) {
  .content-grid > .card {
    grid-column: span 12 !important;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
