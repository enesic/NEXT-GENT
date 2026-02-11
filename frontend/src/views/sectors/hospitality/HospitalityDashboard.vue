<template>
  <DashboardLayout sector="hospitality" :sector-icon="Hotel">
    <!-- Stats Overview -->
    <section class="stats-grid">
      <StatCard
        :icon="Bed"
        label="Oda Doluluk Oranı"
        :value="`${stats.occupancyRate}%`"
        change="+5.2%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        :animated="false"
        @click="navigateTo('/rooms')"
      />
      <StatCard
        :icon="Users"
        label="Bugünkü Check-in"
        :value="stats.todayCheckins"
        change="+8.1%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/checkins')"
      />
      <StatCard
        :icon="DollarSign"
        label="Günlük Gelir"
        :value="`₺${stats.dailyRevenue.toLocaleString('tr-TR')}`"
        change="+12.4%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        :animated="false"
        @click="navigateTo('/revenue')"
      />
      <StatCard
        :icon="Star"
        label="Misafir Memnuniyeti"
        :value="stats.guestSatisfaction"
        change="+0.4"
        changeType="positive"
        :gradient="theme.primaryGradient"
        :animated="false"
        @click="navigateTo('/reviews')"
      />
    </section>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- Room Status -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">Oda Durumu</h3>
        </div>
        <div class="room-status-grid">
          <div 
            v-for="room in roomStatus" 
            :key="room.id"
            class="room-card"
            :class="room.statusClass"
            @click="handleRoomClick(room)"
          >
            <div class="room-number">{{ room.number }}</div>
            <div class="room-type">{{ room.type }}</div>
            <div class="room-status-badge" :class="room.statusClass">
              {{ room.statusText }}
            </div>
          </div>
        </div>
      </section>

      <!-- Check-ins Today -->
      <section class="card">
        <ActivityFeed
          title="Bugünkü Check-in'ler"
          :items="todayCheckins"
          @item-click="handleCheckinClick"
          @view-all="navigateTo('/checkins')"
        />
      </section>

      <!-- Occupancy Trend -->
      <section class="card chart-card">
        <div class="card-header">
          <h3 class="card-title">Doluluk Trendi</h3>
          <div class="time-filters">
            <button 
              v-for="filter in timeFilters" 
              :key="filter.value"
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
            :data="occupancyData"
            :gradient-colors="['rgba(6, 182, 212, 0.8)', 'rgba(6, 182, 212, 0.1)']"
          />
        </div>
      </section>

      <!-- Guest Requests -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">
            <Bell :size="20" />
            Misafir Talepleri
          </h3>
        </div>
        <div class="requests-list">
          <div 
            v-for="request in guestRequests" 
            :key="request.id"
            class="request-item"
            @click="handleRequestClick(request)"
          >
            <div class="request-icon" :style="{ background: request.iconGradient }">
              <component :is="request.icon" :size="20" />
            </div>
            <div class="request-info">
              <p class="request-title">{{ request.title }}</p>
              <p class="request-details">Oda {{ request.room }} • {{ request.time }}</p>
            </div>
            <div class="request-priority" :class="request.priorityClass">
              {{ request.priority }}
            </div>
          </div>
        </div>
      </section>

      <!-- Revenue Breakdown -->
      <section class="card chart-card">
        <div class="card-header">
          <h3 class="card-title">Gelir Dağılımı</h3>
        </div>
        <div class="chart-wrapper">
          <InteractiveChart
            type="doughnut"
            :data="revenueBreakdownData"
            :gradient-colors="['#06b6d4', '#22d3ee', '#67e8f9', '#a5f3fc']"
          />
        </div>
        <div class="revenue-legend">
          <div 
            v-for="item in revenueBreakdown" 
            :key="item.name"
            class="legend-item"
          >
            <div class="legend-dot" :style="{ background: item.color }"></div>
            <span class="legend-label">{{ item.name }}</span>
            <span class="legend-value">₺{{ item.amount.toLocaleString('tr-TR') }}</span>
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
  Hotel, Bed, Users, DollarSign, Star,
  Bell, Coffee, Utensils, Wifi, Droplet
} from 'lucide-vue-next'
import DashboardLayout from '../../components/dashboard/DashboardLayout.vue'
import StatCard from '../../components/dashboard/StatCard.vue'
import ActivityFeed from '../../components/dashboard/ActivityFeed.vue'
import InteractiveChart from '../../components/dashboard/InteractiveChart.vue'
import { useSectorTheme } from '../../composables/useSectorTheme'

const router = useRouter()
const { theme } = useSectorTheme('hospitality')

// Stats
const stats = ref({
  occupancyRate: 87,
  todayCheckins: 24,
  dailyRevenue: 156000,
  guestSatisfaction: 4.7
})

// Time Filters
const timeFilters = [
  { label: '7 Gün', value: '7d' },
  { label: '30 Gün', value: '30d' },
  { label: '90 Gün', value: '90d' }
]
const selectedTimeFilter = ref('7d')

// Room Status
const roomStatus = ref([
  { id: 1, number: '101', type: 'Standart', statusClass: 'occupied', statusText: 'Dolu' },
  { id: 2, number: '102', type: 'Deluxe', statusClass: 'occupied', statusText: 'Dolu' },
  { id: 3, number: '103', type: 'Suite', statusClass: 'available', statusText: 'Boş' },
  { id: 4, number: '104', type: 'Standart', statusClass: 'cleaning', statusText: 'Temizlik' },
  { id: 5, number: '201', type: 'Deluxe', statusClass: 'occupied', statusText: 'Dolu' },
  { id: 6, number: '202', type: 'Suite', statusClass: 'available', statusText: 'Boş' },
  { id: 7, number: '203', type: 'Standart', statusClass: 'occupied', statusText: 'Dolu' },
  { id: 8, number: '204', type: 'Deluxe', statusClass: 'maintenance', statusText: 'Bakım' }
])

// Today's Check-ins
const todayCheckins = ref([
  {
    id: 1,
    icon: Users,
    iconGradient: 'linear-gradient(135deg, #06b6d4, #22d3ee)',
    title: 'Ahmet & Ayşe Yılmaz',
    subtitle: 'Oda 301 • Deluxe Suite',
    time: '2 saat',
    badge: 'Bekleniyor',
    badgeType: 'info'
  },
  {
    id: 2,
    icon: Users,
    iconGradient: 'linear-gradient(135deg, #22d3ee, #67e8f9)',
    title: 'John Smith',
    subtitle: 'Oda 205 • Standart',
    time: '4 saat',
    badge: 'Onaylandı',
    badgeType: 'success'
  }
])

// Occupancy Data
const occupancyData = computed(() => ({
  labels: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
  datasets: [{
    label: 'Doluluk Oranı (%)',
    data: [82, 85, 83, 88, 92, 95, 87]
  }]
}))

// Guest Requests
const guestRequests = ref([
  {
    id: 1,
    icon: Coffee,
    iconGradient: 'linear-gradient(135deg, #06b6d4, #22d3ee)',
    title: 'Kahvaltı Servisi',
    room: '205',
    time: '10 dk önce',
    priority: 'Yüksek',
    priorityClass: 'high'
  },
  {
    id: 2,
    icon: Utensils,
    iconGradient: 'linear-gradient(135deg, #22d3ee, #67e8f9)',
    title: 'Oda Servisi',
    room: '301',
    time: '25 dk önce',
    priority: 'Orta',
    priorityClass: 'medium'
  },
  {
    id: 3,
    icon: Wifi,
    iconGradient: 'linear-gradient(135deg, #67e8f9, #a5f3fc)',
    title: 'WiFi Sorunu',
    room: '102',
    time: '1 saat önce',
    priority: 'Düşük',
    priorityClass: 'low'
  },
  {
    id: 4,
    icon: Droplet,
    iconGradient: 'linear-gradient(135deg, #06b6d4, #22d3ee)',
    title: 'Havlu Talebi',
    room: '203',
    time: '2 saat önce',
    priority: 'Orta',
    priorityClass: 'medium'
  }
])

// Revenue Breakdown
const revenueBreakdown = ref([
  { name: 'Oda Gelirleri', amount: 98000, color: '#06b6d4' },
  { name: 'Restoran', amount: 32000, color: '#22d3ee' },
  { name: 'Spa & Wellness', amount: 18000, color: '#67e8f9' },
  { name: 'Diğer', amount: 8000, color: '#a5f3fc' }
])

// Revenue Breakdown Data for Chart
const revenueBreakdownData = computed(() => ({
  labels: revenueBreakdown.value.map(r => r.name),
  datasets: [{
    data: revenueBreakdown.value.map(r => r.amount),
    backgroundColor: revenueBreakdown.value.map(r => r.color)
  }]
}))

// Methods
const navigateTo = (path) => {
  console.log('Navigate to:', path)
}

const handleRoomClick = (room) => {
  console.log('Room clicked:', room)
}

const handleCheckinClick = (checkin) => {
  console.log('Check-in clicked:', checkin)
}

const handleRequestClick = (request) => {
  console.log('Request clicked:', request)
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
}

.card:nth-child(1) { grid-column: span 8; }
.card:nth-child(2) { grid-column: span 4; }
.card:nth-child(3) { grid-column: span 8; }
.card:nth-child(4) { grid-column: span 4; }
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
  height: 280px;
}

/* Room Status */
.room-status-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 12px;
}

.room-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}

.room-card:hover {
  transform: translateY(-4px);
  border-color: rgba(255, 255, 255, 0.1);
}

.room-number {
  font-size: 18px;
  font-weight: 700;
  color: white;
  margin-bottom: 6px;
}

.room-type {
  font-size: 11px;
  color: #9ca3af;
  margin-bottom: 8px;
}

.room-status-badge {
  padding: 4px 10px;
  border-radius: 99px;
  font-size: 10px;
  font-weight: 600;
}

.room-status-badge.occupied {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.room-status-badge.available {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.room-status-badge.cleaning {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.room-status-badge.maintenance {
  background: rgba(107, 114, 128, 0.15);
  color: #6b7280;
}

/* Guest Requests */
.requests-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.request-item {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.request-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

.request-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.request-info {
  flex: 1;
}

.request-title {
  font-size: 14px;
  font-weight: 600;
  color: white;
  margin: 0 0 4px 0;
}

.request-details {
  font-size: 12px;
  color: #9ca3af;
  margin: 0;
}

.request-priority {
  padding: 6px 12px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 600;
}

.request-priority.high {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.request-priority.medium {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.request-priority.low {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

/* Revenue Legend */
.revenue-legend {
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

@media (max-width: 1200px) {
  .content-grid > .card {
    grid-column: span 12 !important;
  }
  
  .room-status-grid {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .room-status-grid {
    grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
  }
}
</style>
