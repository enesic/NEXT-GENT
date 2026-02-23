<template>
  <DashboardLayout sector="beauty" :sector-icon="Sparkles">
  <div class="beauty-dashboard">
    <!-- Decorative Welcome - Her zaman görünür -->
    <div class="beauty-welcome">
      <span class="beauty-divider"></span>
      <p class="beauty-tagline">Bakım ve güzellik yönetiminizin merkezi</p>
      <span class="beauty-divider"></span>
    </div>

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
      <section class="stats-grid beauty-stats">
        <SkeletonStatCard v-for="i in 4" :key="i" />
      </section>
    </template>

    <!-- Data Loaded -->
    <template v-else>
    <!-- Quick Action Bar -->
    <div class="quick-actions">
      <button class="quick-btn appointment-btn" @click="showAppointmentModal = true">
        <CalendarPlus :size="18" :stroke-width="2" />
        Yeni Randevu Oluştur
      </button>
      <div class="quick-stats">
        <span class="quick-stat">
          <span class="qs-dot confirmed"></span>
          {{ stats.todayAppointments }} randevu bugün
        </span>
      </div>
    </div>
    <!-- Stats Overview -->
    <section class="stats-grid beauty-stats">
      <StatCard
        :icon="Calendar"
        label="Bugünkü Randevular"
        :value="stats.todayAppointments"
        change="+12%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/appointments')"
      />
      <StatCard
        :icon="DollarSign"
        label="Toplam Gelir"
        :value="`₺${stats.totalRevenue.toLocaleString('tr-TR')}`"
        change="+23%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        :animated="false"
        @click="navigateTo('/revenue')"
      />
      <StatCard
        :icon="Users"
        label="Aktif Müşteriler"
        :value="stats.activeClients"
        change="+8%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/clients')"
      />
      <StatCard
        :icon="Star"
        label="Ortalama Memnuniyet"
        :value="stats.averageRating"
        change="+0.3"
        changeType="positive"
        :gradient="theme.primaryGradient"
        :animated="false"
        @click="navigateTo('/reviews')"
      />
    </section>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- Today's Appointments -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">Bugünün Randevuları</h3>
          <button v-ripple class="btn-link" @click="navigateTo('/appointments')" aria-label="View all appointments">Tümünü Gör</button>
        </div>
        <div class="appointments-list">
          <div 
            v-for="apt in todayAppointments" 
            :key="apt.id"
            v-ripple
            class="appointment-item"
            @click="handleAppointmentClick(apt)"
            role="button"
            tabindex="0"
            :aria-label="`View appointment for ${apt.client}`"
            @keydown.enter="handleAppointmentClick(apt)"
            @keydown.space.prevent="handleAppointmentClick(apt)"
          >
            <div class="appointment-time">
              <Clock :size="16" />
              <span>{{ apt.time }}</span>
            </div>
            <div class="appointment-details">
              <p class="client-name">{{ apt.client }}</p>
              <p class="service-name">{{ apt.service }}</p>
            </div>
            <div class="appointment-staff">
              <div class="staff-avatar" :style="{ background: apt.staffGradient }">
                {{ apt.staff[0] }}
              </div>
            </div>
            <div class="appointment-status" :class="apt.statusClass">
              {{ apt.statusText }}
            </div>
          </div>
        </div>
      </section>

      <!-- Popular Services -->
      <section class="card chart-card">
        <div class="card-header">
          <h3 class="card-title">Popüler Hizmetler</h3>
        </div>
        <div class="chart-wrapper">
          <InteractiveChart
            type="doughnut"
            :data="servicesData"
            :gradient-colors="['#ec4899', '#a855f7', '#f59e0b', '#22c55e']"
          />
        </div>
        <div class="services-legend">
          <div 
            v-for="service in topServices" 
            :key="service.name"
            class="legend-item"
            @click="handleServiceClick(service)"
          >
            <div class="legend-dot" :style="{ background: service.color }"></div>
            <span class="legend-label">{{ service.name }}</span>
            <span class="legend-value">{{ service.count }}</span>
          </div>
        </div>
      </section>

      <!-- Revenue Trend -->
      <section class="card chart-card">
        <div class="card-header">
          <h3 class="card-title">Gelir Trendi</h3>
          <div class="time-filters">
            <button 
              v-for="filter in timeFilters" 
              :key="filter.value"
              v-ripple
              class="filter-btn" 
              :class="{ active: selectedTimeFilter === filter.value }"
              @click="selectedTimeFilter = filter.value"
            >
              {{ filter.label }}
            </button>
          </div>
        </div>
        <div class="chart-wrapper">
          <SkeletonChart v-if="revenueChartLoading || !revenueChartData" type="line" />
          <InteractiveChart
            v-else
            type="line"
            :data="revenueChartData"
            :gradient-colors="['rgba(236, 72, 153, 0.8)', 'rgba(236, 72, 153, 0.1)']"
          />
        </div>
      </section>

      <!-- Staff Performance -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">
            <Trophy :size="20" />
            Personel Performansı
          </h3>
        </div>
        <div class="staff-list">
          <div 
            v-for="staff in staffPerformance" 
            :key="staff.id"
            class="staff-item"
            @click="handleStaffClick(staff)"
          >
            <div class="staff-info">
              <div class="staff-avatar" :style="{ background: staff.gradient }">
                {{ staff.name[0] }}
              </div>
              <div>
                <p class="staff-name">{{ staff.name }}</p>
                <p class="staff-role">{{ staff.role }}</p>
              </div>
            </div>
            <div class="staff-metrics">
              <div class="metric">
                <Users :size="14" />
                <span>{{ staff.clients }}</span>
              </div>
              <div class="metric">
                <Star :size="14" :fill="'#f59e0b'" :stroke="'#f59e0b'" />
                <span>{{ staff.rating }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- Appointment Modal -->
    <AppointmentModal
      v-model="showAppointmentModal"
      :service-options="beautyServices"
    />
    </template>
  </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Sparkles, Calendar, DollarSign, Users, Star,
  Clock, Trophy, CalendarPlus
} from 'lucide-vue-next'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import StatCard from '@/components/dashboard/StatCard.vue'
import InteractiveChart from '@/components/dashboard/InteractiveChart.vue'
import SkeletonStatCard from '@/components/common/SkeletonStatCard.vue'
import SkeletonChart from '@/components/common/SkeletonChart.vue'
import ErrorState from '@/components/common/ErrorState.vue'
import { useSectorTheme } from '@/composables/useSectorTheme'
import { useDashboardData } from '@/composables/useDashboardData'
import { useAnalyticsStore } from '@/stores/analytics'
import { vRipple } from '@/composables/useRipple'
import AppointmentModal from '@/components/common/AppointmentModal.vue'

const router = useRouter()
const { theme } = useSectorTheme('beauty')
const analyticsStore = useAnalyticsStore()
const showAppointmentModal = ref(false)

const beautyServices = [
  'Cilt Bakımı',
  'Saç Kesim',
  'Saç Boyama',
  'Masaj Terapisi',
  'Manikür & Pedikür',
  'Kalıcı Makyaj',
  'Kaş & Kirpik',
  'Epilasyon',
  'Dolgu & Botoks Danışma',
  'Diğer'
]

// Fetch dashboard data with WebSocket support
const { kpis, pulse, satisfaction, isLoading, hasError, retry } = useDashboardData({
  enableWebSocket: true,
  fetchSatisfaction: true
})

// Transform backend KPIs to stats (Beauty sector)
const stats = computed(() => {
  const defaultStats = {
    todayAppointments: 28,
    totalRevenue: 45680,
    activeClients: 156,
    averageRating: '4.8'
  }

  if (!kpis.value || kpis.value.length === 0) {
    return {
      ...defaultStats,
      todayAppointments: pulse.value?.pendingAppointments ?? defaultStats.todayAppointments,
      totalRevenue: pulse.value?.totalRevenue ?? defaultStats.totalRevenue,
      activeClients: pulse.value?.todayClients ?? defaultStats.activeClients,
      averageRating: String(satisfaction?.value?.average ?? defaultStats.averageRating)
    }
  }

  return {
    todayAppointments: pulse.value?.pendingAppointments ?? defaultStats.todayAppointments,
    totalRevenue: kpis.value[1]?.value ?? defaultStats.totalRevenue,
    activeClients: pulse.value?.todayClients ?? kpis.value[2]?.value ?? defaultStats.activeClients,
    averageRating: String(kpis.value[3]?.value ?? satisfaction?.value?.average ?? defaultStats.averageRating)
  }
})

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
    time: '09:00',
    client: 'Ayşe Yılmaz',
    service: 'Cilt Bakımı',
    staff: 'Zeynep K.',
    staffGradient: 'linear-gradient(135deg, #ec4899, #a855f7)',
    statusClass: 'confirmed',
    statusText: 'Onaylı'
  },
  {
    id: 2,
    time: '10:30',
    client: 'Elif Demir',
    service: 'Saç Kesim & Boyama',
    staff: 'Merve A.',
    staffGradient: 'linear-gradient(135deg, #a855f7, #ec4899)',
    statusClass: 'confirmed',
    statusText: 'Onaylı'
  },
  {
    id: 3,
    time: '11:00',
    client: 'Selin Kaya',
    service: 'Manikür & Pedikür',
    staff: 'Aylin S.',
    staffGradient: 'linear-gradient(135deg, #f59e0b, #ec4899)',
    statusClass: 'in-progress',
    statusText: 'Devam Ediyor'
  },
  {
    id: 4,
    time: '13:00',
    client: 'Deniz Çelik',
    service: 'Masaj Terapisi',
    staff: 'Zeynep K.',
    staffGradient: 'linear-gradient(135deg, #ec4899, #a855f7)',
    statusClass: 'confirmed',
    statusText: 'Onaylı'
  },
  {
    id: 5,
    time: '14:30',
    client: 'Burcu Arslan',
    service: 'Kalıcı Makyaj',
    staff: 'Seda T.',
    staffGradient: 'linear-gradient(135deg, #0891b2, #22c55e)',
    statusClass: 'pending',
    statusText: 'Bekliyor'
  }
])

// Top Services
const topServices = ref([
  { name: 'Cilt Bakımı', count: 45, color: '#ec4899' },
  { name: 'Saç Kesim', count: 38, color: '#a855f7' },
  { name: 'Masaj', count: 32, color: '#f59e0b' },
  { name: 'Manikür', count: 28, color: '#22c55e' }
])

// Services Data for Chart
const servicesData = computed(() => ({
  labels: topServices.value.map(s => s.name),
  datasets: [{
    data: topServices.value.map(s => s.count),
    backgroundColor: topServices.value.map(s => s.color)
  }]
}))

// Revenue Chart (fetched from backend)
const revenueChartData = ref(null)
const revenueChartLoading = ref(false)

// Staff Performance
const staffPerformance = ref([
  {
    id: 1,
    name: 'Zeynep Karaca',
    role: 'Kıdemli Estetisyen',
    clients: 42,
    rating: 4.9,
    gradient: 'linear-gradient(135deg, #ec4899, #a855f7)'
  },
  {
    id: 2,
    name: 'Merve Aydın',
    role: 'Kuaför',
    clients: 38,
    rating: 4.8,
    gradient: 'linear-gradient(135deg, #a855f7, #ec4899)'
  },
  {
    id: 3,
    name: 'Aylin Şahin',
    role: 'Tırnak Uzmanı',
    clients: 35,
    rating: 4.7,
    gradient: 'linear-gradient(135deg, #f59e0b, #ec4899)'
  },
  {
    id: 4,
    name: 'Seda Tekin',
    role: 'Makyaj Uzmanı',
    clients: 30,
    rating: 4.9,
    gradient: 'linear-gradient(135deg, #0891b2, #22c55e)'
  }
])

// Methods
const navigateTo = (path) => {
  console.log('Navigate to:', path)
}

const handleAppointmentClick = (appointment) => {
  console.log('Appointment clicked:', appointment)
}

const handleServiceClick = (service) => {
  console.log('Service clicked:', service)
}

const handleStaffClick = (staff) => {
  console.log('Staff clicked:', staff)
}

// Fetch revenue chart data from backend
const fetchRevenueChartData = async () => {
  revenueChartLoading.value = true
  try {
    const endDate = new Date().toISOString()
    const days = selectedTimeFilter.value === '7d' ? 7 : selectedTimeFilter.value === '30d' ? 30 : 90
    const startDate = new Date(Date.now() - days * 24 * 60 * 60 * 1000).toISOString()

    const response = await analyticsStore.fetchChart('revenue-by-segment', startDate, endDate)
    if (response && (response.labels || response.datasets)) {
      revenueChartData.value = response
    } else {
      revenueChartData.value = {
        labels: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
        datasets: [{
          label: 'Gelir (₺)',
          data: [5200, 6800, 5900, 7200, 8100, 9500, 6800]
        }]
      }
    }
  } catch (error) {
    console.error('Failed to load revenue chart:', error)
    revenueChartData.value = {
      labels: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
      datasets: [{
        label: 'Gelir (₺)',
        data: [5200, 6800, 5900, 7200, 8100, 9500, 6800]
      }]
    }
  } finally {
    revenueChartLoading.value = false
  }
}

watch(selectedTimeFilter, () => {
  fetchRevenueChartData()
})

onMounted(() => {
  fetchRevenueChartData()
})
</script>

<style scoped>
/* ═══════════════════════════════════════════════════════════════
   GÜZELLİK MERKEZİ – Özel Lüks Salon Estetiği
   ═══════════════════════════════════════════════════════════════ */

.beauty-dashboard {
  font-family: 'Cormorant Garamond', 'Inter', serif;
  min-height: 100%;
  position: relative;
  margin: -32px;
  padding: 32px;
  background: 
    radial-gradient(ellipse 80% 50% at 50% -10%, rgba(236, 72, 153, 0.08) 0%, transparent 50%),
    radial-gradient(ellipse 60% 40% at 100% 50%, rgba(168, 85, 247, 0.05) 0%, transparent 50%),
    radial-gradient(ellipse 50% 30% at 0% 80%, rgba(212, 165, 116, 0.03) 0%, transparent 50%),
    linear-gradient(180deg, #0c0a0a 0%, #0a0808 100%);
}

/* Quick Actions – Beauty style */
.quick-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28px;
  padding: 18px 24px;
  background: rgba(236, 72, 153, 0.04);
  border: 1px solid rgba(236, 72, 153, 0.15);
  border-radius: 20px;
  gap: 16px;
  flex-wrap: wrap;
}

.quick-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 24px;
  border: none;
  border-radius: 16px;
  font-family: 'Cormorant Garamond', serif;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.appointment-btn {
  background: linear-gradient(135deg, #ec4899, #a855f7);
  color: white;
  box-shadow: 0 4px 16px rgba(236, 72, 153, 0.35);
}

.appointment-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(236, 72, 153, 0.45);
}

.quick-stats {
  display: flex;
  align-items: center;
  gap: 16px;
}

.quick-stat {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: rgba(253, 242, 248, 0.7);
  font-weight: 500;
}

.qs-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.qs-dot.confirmed { background: #34d399; box-shadow: 0 0 8px rgba(52, 211, 153, 0.5); }

/* Decorative Welcome */
.beauty-welcome {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 32px;
  padding: 0 16px;
}

.beauty-divider {
  flex: 1;
  max-width: 120px;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(236, 72, 153, 0.5), transparent);
  opacity: 0.8;
}

.beauty-tagline {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: #f9a8d4;
  margin: 0;
  text-shadow: 0 0 20px rgba(236, 72, 153, 0.3);
}

/* Stats Grid – Elegant spacing */
.stats-grid.beauty-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 28px;
}

/* Cards – Lüks cam efekti, yumuşak köşeler */
.card {
  background: linear-gradient(160deg, rgba(26, 22, 24, 0.9) 0%, rgba(12, 10, 10, 0.95) 100%);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(236, 72, 153, 0.12);
  border-radius: 24px;
  padding: 28px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(236, 72, 153, 0.3), transparent);
  opacity: 0.6;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.35), 0 0 0 1px rgba(236, 72, 153, 0.15);
  border-color: rgba(236, 72, 153, 0.25);
}

.card:nth-child(1) { grid-column: span 6; }
.card:nth-child(2) { grid-column: span 6; }
.card:nth-child(3) { grid-column: span 8; }
.card:nth-child(4) { grid-column: span 4; }

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.card-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 19px;
  font-weight: 600;
  letter-spacing: 0.02em;
  margin: 0;
  color: #fdf2f8;
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn-link {
  background: transparent;
  border: 1px solid rgba(236, 72, 153, 0.4);
  color: #f9a8d4;
  font-family: 'Cormorant Garamond', serif;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: all 0.3s;
  padding: 8px 16px;
  border-radius: 20px;
}

.btn-link:hover {
  background: rgba(236, 72, 153, 0.15);
  color: #fdf2f8;
  border-color: rgba(236, 72, 153, 0.6);
}

.time-filters {
  display: flex;
  gap: 8px;
}

.filter-btn {
  padding: 8px 16px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  color: rgba(253, 242, 248, 0.6);
  font-family: 'Cormorant Garamond', serif;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.03em;
  cursor: pointer;
  transition: all 0.3s;
}

.filter-btn:hover {
  background: rgba(236, 72, 153, 0.1);
  color: #fdf2f8;
  border-color: rgba(236, 72, 153, 0.3);
}

.filter-btn.active {
  background: linear-gradient(135deg, #ec4899 0%, #a855f7 100%);
  color: white;
  border-color: transparent;
  box-shadow: 0 4px 16px rgba(236, 72, 153, 0.35);
}

.chart-wrapper {
  height: 280px;
}

/* Appointments – Salon tarzı listeler */
.appointments-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.appointment-item {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.02) 0%, rgba(255, 255, 255, 0.01) 100%);
  border: 1px solid rgba(236, 72, 153, 0.08);
  border-radius: 16px;
  padding: 18px 20px;
  display: flex;
  align-items: center;
  gap: 18px;
  cursor: pointer;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.appointment-item:hover {
  background: rgba(236, 72, 153, 0.06);
  border-color: rgba(236, 72, 153, 0.2);
  transform: translateX(6px);
  box-shadow: 0 4px 20px rgba(236, 72, 153, 0.08);
}

.appointment-time {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #f9a8d4;
  font-weight: 600;
  min-width: 72px;
}

.appointment-details {
  flex: 1;
}

.client-name {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 15px;
  font-weight: 600;
  color: #fdf2f8;
  margin: 0 0 4px 0;
}

.service-name {
  font-size: 13px;
  color: rgba(253, 242, 248, 0.6);
  margin: 0;
}

.appointment-staff .staff-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 15px;
  border: 2px solid rgba(236, 72, 153, 0.2);
}

.appointment-status {
  padding: 8px 14px;
  border-radius: 24px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.04em;
}

.appointment-status.confirmed {
  background: rgba(52, 211, 153, 0.12);
  color: #34d399;
  border: 1px solid rgba(52, 211, 153, 0.25);
}

.appointment-status.in-progress {
  background: rgba(251, 191, 36, 0.12);
  color: #fbbf24;
  border: 1px solid rgba(251, 191, 36, 0.25);
}

.appointment-status.pending {
  background: rgba(168, 85, 247, 0.12);
  color: #c4b5fd;
  border: 1px solid rgba(168, 85, 247, 0.25);
}

/* Services Legend */
.services-legend {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-top: 24px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 14px;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid transparent;
}

.legend-item:hover {
  background: rgba(236, 72, 153, 0.06);
  border-color: rgba(236, 72, 153, 0.15);
}

.legend-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  box-shadow: 0 0 12px currentColor;
}

.legend-label {
  flex: 1;
  font-family: 'Cormorant Garamond', serif;
  font-size: 15px;
  font-weight: 500;
  color: #fdf2f8;
}

.legend-value {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 16px;
  font-weight: 600;
  color: #f9a8d4;
}

/* Staff – Personel kartları */
.staff-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.staff-item {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.02) 0%, transparent 100%);
  border: 1px solid rgba(236, 72, 153, 0.08);
  border-radius: 18px;
  padding: 18px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.staff-item:hover {
  background: rgba(236, 72, 153, 0.06);
  border-color: rgba(236, 72, 153, 0.2);
  transform: translateX(4px);
  box-shadow: 0 4px 24px rgba(236, 72, 153, 0.08);
}

.staff-info {
  display: flex;
  align-items: center;
  gap: 14px;
}

.staff-info .staff-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 18px;
  border: 2px solid rgba(236, 72, 153, 0.25);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.staff-name {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 15px;
  font-weight: 600;
  color: #fdf2f8;
  margin: 0 0 4px 0;
}

.staff-role {
  font-size: 13px;
  color: rgba(253, 242, 248, 0.6);
  margin: 0;
}

.staff-metrics {
  display: flex;
  gap: 20px;
}

.metric {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #fdf2f8;
  font-weight: 600;
}

/* Responsive */
@media (max-width: 1200px) {
  .content-grid > .card {
    grid-column: span 12 !important;
  }
}

@media (max-width: 768px) {
  .beauty-dashboard {
    margin: -20px -16px;
    padding: 20px 16px;
  }

  .stats-grid.beauty-stats {
    grid-template-columns: 1fr;
  }

  .beauty-welcome {
    flex-direction: column;
    gap: 12px;
  }

  .beauty-divider {
    max-width: 80px;
  }

  .beauty-tagline {
    font-size: 13px;
    letter-spacing: 0.15em;
  }

  .card {
    padding: 20px;
    border-radius: 20px;
  }
}
</style>
