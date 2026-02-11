<template>
  <div class="hotel-dashboard">
    <!-- Header -->
    <header class="dashboard-header">
      <div class="header-content">
        <div>
          <h1 class="title">Otel Yönetim Sistemi</h1>
          <p class="subtitle">Premium Hospitality Management</p>
        </div>
        <div class="header-actions">
          <button class="btn-icon" title="Notifications">
            <Bell :size="20" />
          </button>
          <button class="btn-icon" title="Settings">
            <Settings :size="20" />
          </button>
        </div>
      </div>
    </header>

    <!-- Stats Overview -->
    <section class="stats-grid">
      <div class="stat-card" v-for="(stat, index) in stats" :key="index">
        <div class="stat-icon-wrapper" :style="{ background: stat.gradient }">
          <component :is="stat.icon" :size="24" />
        </div>
        <div class="stat-content">
          <p class="stat-label">{{ stat.label }}</p>
          <h3 class="stat-value">{{ stat.value }}</h3>
          <div class="stat-change" :class="stat.changeType">
            <component :is="stat.changeType === 'positive' ? TrendingUp : TrendingDown" :size="16" />
            <span>{{ stat.change }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- Check-ins Today -->
      <section class="card checkins-card">
        <div class="card-header">
          <h2 class="card-title">Bugünkü Check-in'ler</h2>
          <button class="btn-link">Tümünü Gör</button>
        </div>
        <div class="checkins-list">
          <div class="checkin-item" v-for="checkin in todayCheckins" :key="checkin.id">
            <div class="checkin-time">
              <Clock :size="16" />
              <span>{{ checkin.time }}</span>
            </div>
            <div class="guest-details">
              <p class="guest-name">{{ checkin.guest }}</p>
              <p class="room-info">Oda {{ checkin.room }} • {{ checkin.nights }} gece</p>
            </div>
            <div class="checkin-type" :class="checkin.type">
              {{ checkin.typeText }}
            </div>
            <div class="checkin-status" :class="checkin.status">
              {{ checkin.statusText }}
            </div>
          </div>
        </div>
      </section>

      <!-- Room Occupancy -->
      <section class="card occupancy-card">
        <div class="card-header">
          <h2 class="card-title">Oda Doluluk Oranı</h2>
        </div>
        <div class="occupancy-visual">
          <div class="occupancy-circle">
            <svg viewBox="0 0 200 200">
              <circle cx="100" cy="100" r="90" fill="none" stroke="rgba(234, 88, 12, 0.1)" stroke-width="20"/>
              <circle cx="100" cy="100" r="90" fill="none" stroke="url(#gradient)" stroke-width="20" 
                      :stroke-dasharray="occupancyDasharray" stroke-linecap="round" transform="rotate(-90 100 100)"/>
              <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style="stop-color:#ea580c;stop-opacity:1" />
                  <stop offset="100%" style="stop-color:#0891b2;stop-opacity:1" />
                </linearGradient>
              </defs>
            </svg>
            <div class="occupancy-text">
              <span class="occupancy-percent">{{ occupancyRate }}%</span>
              <span class="occupancy-label">Doluluk</span>
            </div>
          </div>
        </div>
        <div class="room-stats">
          <div class="room-stat">
            <div class="stat-dot occupied"></div>
            <span>Dolu: {{ roomsOccupied }}</span>
          </div>
          <div class="room-stat">
            <div class="stat-dot available"></div>
            <span>Boş: {{ roomsAvailable }}</span>
          </div>
          <div class="room-stat">
            <div class="stat-dot maintenance"></div>
            <span>Bakım: {{ roomsMaintenance }}</span>
          </div>
        </div>
      </section>

      <!-- Revenue Chart -->
      <section class="card revenue-card">
        <div class="card-header">
          <h2 class="card-title">Gelir Analizi</h2>
          <div class="time-filters">
            <button class="filter-btn" :class="{ active: timeFilter === '7d' }" @click="timeFilter = '7d'">7 Gün</button>
            <button class="filter-btn" :class="{ active: timeFilter === '30d' }" @click="timeFilter = '30d'">30 Gün</button>
            <button class="filter-btn" :class="{ active: timeFilter === '90d' }" @click="timeFilter = '90d'">90 Gün</button>
          </div>
        </div>
        <div class="revenue-chart">
          <canvas ref="revenueChartEl"></canvas>
        </div>
      </section>

      <!-- Guest Requests -->
      <section class="card requests-card">
        <div class="card-header">
          <h2 class="card-title">Misafir Talepleri</h2>
        </div>
        <div class="requests-list">
          <div class="request-item" v-for="request in guestRequests" :key="request.id">
            <div class="request-icon" :class="request.priority">
              <component :is="request.icon" :size="18" />
            </div>
            <div class="request-details">
              <p class="request-title">{{ request.title }}</p>
              <p class="request-meta">Oda {{ request.room }} • {{ request.time }}</p>
            </div>
            <div class="request-priority" :class="request.priority">
              {{ request.priorityText }}
            </div>
          </div>
        </div>
      </section>

      <!-- Recent Feedback -->
      <section class="card feedback-card">
        <div class="card-header">
          <h2 class="card-title">Son Değerlendirmeler</h2>
        </div>
        <div class="feedback-list">
          <div class="feedback-item" v-for="feedback in recentFeedback" :key="feedback.id">
            <div class="feedback-header">
              <div class="guest-info">
                <div class="guest-avatar" :style="{ background: feedback.color }">
                  {{ feedback.guest[0] }}
                </div>
                <div>
                  <p class="guest-name">{{ feedback.guest }}</p>
                  <p class="feedback-time">{{ feedback.time }}</p>
                </div>
              </div>
              <div class="rating">
                <Star :size="16" v-for="i in 5" :key="i" 
                      :fill="i <= feedback.rating ? '#facc15' : 'none'" 
                      :stroke="i <= feedback.rating ? '#facc15' : '#a8a29e'" />
              </div>
            </div>
            <p class="feedback-text">{{ feedback.comment }}</p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Chart, registerables } from 'chart.js'
import { Bell, Settings, TrendingUp, TrendingDown, Home, Users, DollarSign, Percent, Clock, Star, Coffee, Utensils, Wind } from 'lucide-vue-next'

Chart.register(...registerables)

const revenueChartEl = ref(null)
const timeFilter = ref('7d')

const stats = [
  {
    label: 'Toplam Odalar',
    value: '150',
    change: 'Kapasite',
    changeType: 'positive',
    icon: Home,
    gradient: 'linear-gradient(135deg, #ea580c 0%, #0891b2 100%)'
  },
  {
    label: 'Bugünkü Gelir',
    value: '₺128,400',
    change: '+18%',
    changeType: 'positive',
    icon: DollarSign,
    gradient: 'linear-gradient(135deg, #facc15 0%, #ea580c 100%)'
  },
  {
    label: 'Aktif Misafirler',
    value: '112',
    change: '+5%',
    changeType: 'positive',
    icon: Users,
    gradient: 'linear-gradient(135deg, #0891b2 0%, #ea580c 100%)'
  },
  {
    label: 'Doluluk Oranı',
    value: '85%',
    change: '+12%',
    changeType: 'positive',
    icon: Percent,
    gradient: 'linear-gradient(135deg, #ea580c 0%, #facc15 100%)'
  }
]

const todayCheckins = [
  { id: 1, time: '14:00', guest: 'Ahmet Yılmaz', room: '201', nights: 3, type: 'vip', typeText: 'VIP', status: 'pending', statusText: 'Bekliyor' },
  { id: 2, time: '15:30', guest: 'Sarah Johnson', room: '305', nights: 2, type: 'standard', typeText: 'Standart', status: 'ready', statusText: 'Hazır' },
  { id: 3, time: '16:00', guest: 'Mehmet Demir', room: '412', nights: 5, type: 'suite', typeText: 'Suite', status: 'ready', statusText: 'Hazır' },
  { id: 4, time: '17:30', guest: 'Emma Wilson', room: '208', nights: 1, type: 'standard', typeText: 'Standart', status: 'pending', statusText: 'Bekliyor' },
]

const roomsOccupied = 128
const roomsAvailable = 18
const roomsMaintenance = 4
const totalRooms = roomsOccupied + roomsAvailable + roomsMaintenance

const occupancyRate = computed(() => Math.round((roomsOccupied / totalRooms) * 100))
const occupancyDasharray = computed(() => {
  const circumference = 2 * Math.PI * 90
  const filled = (occupancyRate.value / 100) * circumference
  return `${filled} ${circumference}`
})

const guestRequests = [
  { id: 1, title: 'Ekstra havlu talebi', room: '305', time: '10 dk önce', priority: 'normal', priorityText: 'Normal', icon: Wind },
  { id: 2, title: 'Oda servisi - Kahvaltı', room: '412', time: '25 dk önce', priority: 'high', priorityText: 'Acil', icon: Utensils },
  { id: 3, title: 'Kahve makinesi arızası', room: '201', time: '1 saat önce', priority: 'high', priorityText: 'Acil', icon: Coffee },
  { id: 4, title: 'Geç çıkış talebi', room: '108', time: '2 saat önce', priority: 'normal', priorityText: 'Normal', icon: Clock },
]

const recentFeedback = [
  { id: 1, guest: 'Ali Kaya', rating: 5, time: '2 saat önce', comment: 'Mükemmel hizmet, personel çok ilgili. Kesinlikle tekrar geleceğim!', color: '#ea580c' },
  { id: 2, guest: 'Laura Smith', rating: 4, time: '5 saat önce', comment: 'Great location and clean rooms. Breakfast could be better.', color: '#0891b2' },
  { id: 3, guest: 'Zeynep Arslan', rating: 5, time: '1 gün önce', comment: 'Harika bir deneyim. Özellikle spa merkezi çok başarılı.', color: '#facc15' },
]

onMounted(() => {
  // Revenue Line Chart
  if (revenueChartEl.value) {
    new Chart(revenueChartEl.value, {
      type: 'line',
      data: {
        labels: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
        datasets: [
          {
            label: 'Oda Geliri',
            data: [85000, 92000, 88000, 95000, 102000, 128000, 115000],
            borderColor: '#ea580c',
            backgroundColor: 'rgba(234, 88, 12, 0.1)',
            tension: 0.4,
            fill: true,
            borderWidth: 2,
            pointBackgroundColor: '#ea580c',
            pointRadius: 4,
            pointHoverRadius: 6,
          },
          {
            label: 'Hizmet Geliri',
            data: [15000, 18000, 16000, 22000, 19000, 24000, 21000],
            borderColor: '#0891b2',
            backgroundColor: 'rgba(8, 145, 178, 0.1)',
            tension: 0.4,
            fill: true,
            borderWidth: 2,
            pointBackgroundColor: '#0891b2',
            pointRadius: 4,
            pointHoverRadius: 6,
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { 
            display: true,
            labels: { color: '#a8a29e' }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: { color: 'rgba(255,255,255,0.05)' },
            ticks: { color: '#a8a29e' }
          },
          x: {
            grid: { color: 'rgba(255,255,255,0.05)' },
            ticks: { color: '#a8a29e' }
          }
        }
      }
    })
  }
})
</script>

<style scoped>
.hotel-dashboard {
  padding: 2rem;
  background: #0c0a09;
  min-height: 100vh;
  color: #ffffff;
  font-family: 'Inter', -apple-system, sans-serif;
}

/* Header */
.dashboard-header {
  margin-bottom: 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #ea580c 0%, #0891b2 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.25rem;
}

.subtitle {
  color: #d6d3d1;
  font-size: 0.875rem;
  font-weight: 500;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

.btn-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: #1c1917;
  border: 1px solid #292524;
  color: #d6d3d1;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-icon:hover {
  background: #292524;
  border-color: #ea580c;
  transform: translateY(-2px);
  box-shadow: 0 0 20px rgba(234, 88, 12, 0.3);
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: linear-gradient(145deg, #1c1917 0%, #0c0a09 100%);
  border: 1px solid #292524;
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  gap: 1rem;
  transition: all 0.3s ease;
}

.stat-card:hover {
  border-color: #ea580c;
  transform: translateY(-4px);
  box-shadow: 0 10px 30px rgba(234, 88, 12, 0.2);
}

.stat-icon-wrapper {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 0.75rem;
  color: #d6d3d1;
  margin-bottom: 0.25rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: #ffffff;
}

.stat-change {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.875rem;
}

.stat-change.positive {
  color: #16a34a;
}

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

.card {
  background: linear-gradient(145deg, #1c1917 0%, #0c0a09 100%);
  border: 1px solid #292524;
  border-radius: 16px;
  padding: 1.5rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
}

.btn-link {
  background: none;
  border: none;
  color: #ea580c;
  cursor: pointer;
  font-size: 0.875rem;
  transition: color 0.3s ease;
}

.btn-link:hover {
  color: #0891b2;
}

/* Check-ins */
.checkins-card {
  grid-column: span 2;
}

.checkins-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.checkin-item {
  display: grid;
  grid-template-columns: 100px 1fr auto auto;
  gap: 1rem;
  align-items: center;
  padding: 1rem;
  background: rgba(234, 88, 12, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(234, 88, 12, 0.1);
  transition: all 0.3s ease;
}

.checkin-item:hover {
  border-color: #ea580c;
  background: rgba(234, 88, 12, 0.1);
}

.checkin-time {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #d6d3d1;
  font-size: 0.875rem;
  font-weight: 500;
}

.guest-name {
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: #ffffff;
}

.room-info {
  font-size: 0.875rem;
  color: #d6d3d1;
  font-weight: 500;
}

.checkin-type, .checkin-status {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 600;
}

.checkin-type.vip {
  background: rgba(250, 204, 21, 0.1);
  color: #facc15;
}

.checkin-type.suite {
  background: rgba(8, 145, 178, 0.1);
  color: #0891b2;
}

.checkin-type.standard {
  background: rgba(168, 162, 158, 0.1);
  color: #a8a29e;
}

.checkin-status.ready {
  background: rgba(22, 163, 74, 0.1);
  color: #16a34a;
}

.checkin-status.pending {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
}

/* Occupancy */
.occupancy-visual {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.occupancy-circle {
  position: relative;
  width: 200px;
  height: 200px;
}

.occupancy-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.occupancy-percent {
  display: block;
  font-size: 2.5rem;
  font-weight: 700;
  color: #ea580c;
}

.occupancy-label {
  display: block;
  font-size: 0.875rem;
  color: #d6d3d1;
  font-weight: 500;
}

.room-stats {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.room-stat {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.875rem;
}

.stat-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.stat-dot.occupied {
  background: #ea580c;
}

.stat-dot.available {
  background: #16a34a;
}

.stat-dot.maintenance {
  background: #f59e0b;
}

/* Revenue */
.time-filters {
  display: flex;
  gap: 0.5rem;
}

.filter-btn {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  background: transparent;
  border: 1px solid #292524;
  color: #d6d3d1;
  font-weight: 500;
  cursor: pointer;
  font-size: 0.75rem;
  transition: all 0.3s ease;
}

.filter-btn.active {
  background: #ea580c;
  color: white;
  border-color: #ea580c;
}

.revenue-chart {
  height: 250px;
}

/* Guest Requests */
.requests-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.request-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(234, 88, 12, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(234, 88, 12, 0.1);
  transition: all 0.3s ease;
}

.request-item:hover {
  border-color: #ea580c;
  background: rgba(234, 88, 12, 0.1);
}

.request-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.request-icon.high {
  background: rgba(220, 38, 38, 0.1);
  color: #dc2626;
}

.request-icon.normal {
  background: rgba(8, 145, 178, 0.1);
  color: #0891b2;
}

.request-details {
  flex: 1;
}

.request-title {
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: #ffffff;
}

.request-meta {
  font-size: 0.75rem;
  color: #d6d3d1;
  font-weight: 500;
}

.request-priority {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 600;
}

.request-priority.high {
  background: rgba(220, 38, 38, 0.1);
  color: #dc2626;
}

.request-priority.normal {
  background: rgba(8, 145, 178, 0.1);
  color: #0891b2;
}

/* Feedback */
.feedback-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.feedback-item {
  padding: 1rem;
  background: rgba(234, 88, 12, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(234, 88, 12, 0.1);
}

.feedback-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.guest-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.guest-avatar {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 0.875rem;
}

.guest-name {
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: #ffffff;
}

.feedback-time {
  font-size: 0.75rem;
  color: #d6d3d1;
  font-weight: 500;
}

.rating {
  display: flex;
  gap: 0.25rem;
}

.feedback-text {
  font-size: 0.875rem;
  color: #d6d3d1;
  line-height: 1.5;
  font-weight: 400;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .checkins-card {
    grid-column: span 1;
  }
  
  .checkin-item {
    grid-template-columns: 1fr;
  }
}
</style>
