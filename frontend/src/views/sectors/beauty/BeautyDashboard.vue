<template>
  <DashboardLayout sector="beauty" :sector-icon="Sparkles">
    <!-- Stats Overview -->
    <section class="stats-grid">
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
          <InteractiveChart
            type="line"
            :data="revenueData"
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
  </DashboardLayout>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Sparkles, Calendar, DollarSign, Users, Star,
  Clock, Trophy
} from 'lucide-vue-next'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import StatCard from '@/components/dashboard/StatCard.vue'
import InteractiveChart from '@/components/dashboard/InteractiveChart.vue'
import { useSectorTheme } from '@/composables/useSectorTheme'
import { vRipple } from '@/composables/useRipple'

const router = useRouter()
const { theme } = useSectorTheme('beauty')

// Stats
const stats = ref({
  todayAppointments: 28,
  totalRevenue: 45680,
  activeClients: 156,
  averageRating: 4.8
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

// Revenue Data
const revenueData = computed(() => ({
  labels: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
  datasets: [{
    label: 'Gelir (₺)',
    data: [5200, 6800, 5900, 7200, 8100, 9500, 6800]
  }]
}))

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

.card:nth-child(1) { grid-column: span 6; }
.card:nth-child(2) { grid-column: span 6; }
.card:nth-child(3) { grid-column: span 8; }
.card:nth-child(4) { grid-column: span 4; }

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

.btn-link {
  background: none;
  border: none;
  color: var(--sector-accent);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  padding: 6px 12px;
  border-radius: 8px;
}

.btn-link:hover {
  background: rgba(255, 255, 255, 0.05);
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
  height: 280px;
}

/* Appointments */
.appointments-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.appointment-item {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.appointment-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  transform: translateX(4px);
}

.appointment-time {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--sector-accent);
  font-weight: 600;
  min-width: 80px;
}

.appointment-details {
  flex: 1;
}

.client-name {
  font-size: 14px;
  font-weight: 600;
  color: white;
  margin: 0 0 4px 0;
}

.service-name {
  font-size: 12px;
  color: #9ca3af;
  margin: 0;
}

.appointment-staff {
  display: flex;
  align-items: center;
}

.staff-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 14px;
}

.appointment-status {
  padding: 6px 12px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 600;
}

.appointment-status.confirmed {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.appointment-status.in-progress {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.appointment-status.pending {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

/* Services Legend */
.services-legend {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 20px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.legend-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.legend-label {
  flex: 1;
  font-size: 13px;
  color: white;
  font-weight: 500;
}

.legend-value {
  font-size: 14px;
  font-weight: 700;
  color: var(--sector-accent);
}

/* Staff */
.staff-list {
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
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s;
}

.staff-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

.staff-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.staff-info .staff-avatar {
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

.staff-name {
  font-size: 14px;
  font-weight: 600;
  color: white;
  margin: 0 0 4px 0;
}

.staff-role {
  font-size: 12px;
  color: #9ca3af;
  margin: 0;
}

.staff-metrics {
  display: flex;
  gap: 16px;
}

.metric {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: white;
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
