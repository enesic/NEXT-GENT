<template>
  <DashboardLayout sector="automotive" :sector-icon="Car">
    <!-- Stats Overview -->
    <section class="stats-grid">
      <StatCard
        :icon="Wrench"
        label="Bugünkü Servisler"
        :value="stats.todayServices"
        change="+8.5%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/services')"
      />
      <StatCard
        :icon="Car"
        label="Envanterdeki Araçlar"
        :value="stats.inventoryVehicles"
        change="+12.3%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/inventory')"
      />
      <StatCard
        :icon="Calendar"
        label="Test Sürüşleri"
        :value="stats.testDrives"
        change="+15.7%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/test-drives')"
      />
      <StatCard
        :icon="TrendingUp"
        label="Aylık Satışlar"
        :value="stats.monthlySales"
        change="+22.1%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/sales')"
      />
    </section>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- Service Appointments -->
      <section class="card">
        <ActivityFeed
          title="Bugünkü Servis Randevuları"
          :items="serviceAppointments"
          @item-click="handleServiceClick"
          @view-all="navigateTo('/services')"
        />
      </section>

      <!-- Vehicle Inventory -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">Araç Envanteri</h3>
          <button class="btn-link" @click="navigateTo('/inventory')">Tümünü Gör</button>
        </div>
        <div class="vehicles-grid">
          <div 
            v-for="vehicle in inventoryVehicles" 
            :key="vehicle.id"
            class="vehicle-card"
            @click="handleVehicleClick(vehicle)"
          >
            <div class="vehicle-image" :style="{ background: vehicle.imageGradient }">
              <div class="vehicle-badge" :class="vehicle.condition">{{ vehicle.conditionLabel }}</div>
            </div>
            <div class="vehicle-info">
              <p class="vehicle-name">{{ vehicle.name }}</p>
              <p class="vehicle-specs">{{ vehicle.year }} • {{ vehicle.mileage }} km</p>
              <p class="vehicle-price">₺{{ vehicle.price.toLocaleString('tr-TR') }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Sales Performance -->
      <section class="card chart-card">
        <div class="card-header">
          <h3 class="card-title">Satış Performansı</h3>
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
            type="bar"
            :data="salesData"
            :gradient-colors="['rgba(220, 38, 38, 0.8)', 'rgba(220, 38, 38, 0.3)']"
          />
        </div>
      </section>

      <!-- Test Drive Schedule -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">Test Sürüş Programı</h3>
        </div>
        <div class="test-drives-list">
          <div 
            v-for="drive in testDrives" 
            :key="drive.id"
            class="drive-item"
          >
            <div class="drive-time">
              <Clock :size="16" />
              <span>{{ drive.time }}</span>
            </div>
            <div class="drive-info">
              <p class="drive-customer">{{ drive.customer }}</p>
              <p class="drive-vehicle">{{ drive.vehicle }}</p>
            </div>
            <div class="drive-status" :class="drive.statusClass">
              {{ drive.status }}
            </div>
          </div>
        </div>
      </section>

      <!-- Parts Inventory -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">
            <Package :size="20" />
            Yedek Parça Envanteri
          </h3>
        </div>
        <div class="parts-list">
          <div 
            v-for="part in partsInventory" 
            :key="part.id"
            class="part-item"
          >
            <div class="part-info">
              <p class="part-name">{{ part.name }}</p>
              <p class="part-code">{{ part.code }}</p>
            </div>
            <div class="part-stock" :class="part.stockClass">
              <div class="stock-bar">
                <div class="stock-fill" :style="{ width: `${part.stockPercent}%`, background: part.gradient }"></div>
              </div>
              <span class="stock-text">{{ part.quantity }} adet</span>
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
  Car, Wrench, Calendar, TrendingUp,
  Clock, Package
} from 'lucide-vue-next'
import DashboardLayout from '../../components/dashboard/DashboardLayout.vue'
import StatCard from '../../components/dashboard/StatCard.vue'
import ActivityFeed from '../../components/dashboard/ActivityFeed.vue'
import InteractiveChart from '../../components/dashboard/InteractiveChart.vue'
import { useSectorTheme } from '../../composables/useSectorTheme'

const router = useRouter()
const { theme } = useSectorTheme('automotive')

// Stats
const stats = ref({
  todayServices: 18,
  inventoryVehicles: 47,
  testDrives: 12,
  monthlySales: 23
})

// Time Filters
const timeFilters = [
  { label: '7 Gün', value: '7d' },
  { label: '30 Gün', value: '30d' },
  { label: '90 Gün', value: '90d' }
]
const selectedTimeFilter = ref('30d')

// Service Appointments
const serviceAppointments = ref([
  {
    id: 1,
    icon: Wrench,
    iconGradient: 'linear-gradient(135deg, #dc2626, #ef4444)',
    title: 'Periyodik Bakım',
    subtitle: 'Ahmet Yılmaz • Toyota Corolla',
    time: '30 dk',
    badge: 'Devam Ediyor',
    badgeType: 'warning'
  },
  {
    id: 2,
    icon: Wrench,
    iconGradient: 'linear-gradient(135deg, #3b82f6, #60a5fa)',
    title: 'Fren Değişimi',
    subtitle: 'Ayşe Demir • Honda Civic',
    time: '2 saat',
    badge: 'Bekliyor',
    badgeType: 'info'
  },
  {
    id: 3,
    icon: Wrench,
    iconGradient: 'linear-gradient(135deg, #10b981, #34d399)',
    title: 'Yağ Değişimi',
    subtitle: 'Mehmet Kaya • Ford Focus',
    time: '4 saat',
    badge: 'Tamamlandı',
    badgeType: 'success'
  }
])

// Inventory Vehicles
const inventoryVehicles = ref([
  {
    id: 1,
    name: 'Toyota Corolla 1.6',
    year: 2023,
    mileage: 15000,
    price: 850000,
    imageGradient: 'linear-gradient(135deg, #dc2626, #ef4444)',
    condition: 'new',
    conditionLabel: 'Sıfır'
  },
  {
    id: 2,
    name: 'Honda Civic 1.5 Turbo',
    year: 2022,
    mileage: 28000,
    price: 720000,
    imageGradient: 'linear-gradient(135deg, #3b82f6, #60a5fa)',
    condition: 'used',
    conditionLabel: '2.El'
  }
])

// Sales Data
const salesData = computed(() => ({
  labels: ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz'],
  datasets: [{
    label: 'Satış Adedi',
    data: [18, 22, 19, 25, 21, 23]
  }]
}))

// Test Drives
const testDrives = ref([
  {
    id: 1,
    time: '10:00',
    customer: 'Can Öztürk',
    vehicle: 'BMW 3.20i',
    status: 'Onaylandı',
    statusClass: 'confirmed'
  },
  {
    id: 2,
    time: '14:00',
    customer: 'Zeynep Arslan',
    vehicle: 'Mercedes C180',
    status: 'Bekliyor',
    statusClass: 'pending'
  },
  {
    id: 3,
    time: '16:30',
    customer: 'Ali Çelik',
    vehicle: 'Audi A4',
    status: 'Planlandı',
    statusClass: 'scheduled'
  }
])

// Parts Inventory
const partsInventory = ref([
  {
    id: 1,
    name: 'Fren Balatası',
    code: 'FB-2024',
    quantity: 45,
    stockPercent: 90,
    stockClass: 'good',
    gradient: 'linear-gradient(135deg, #10b981, #34d399)'
  },
  {
    id: 2,
    name: 'Motor Yağı 5W-30',
    code: 'MY-5030',
    quantity: 28,
    stockPercent: 56,
    stockClass: 'medium',
    gradient: 'linear-gradient(135deg, #f59e0b, #fbbf24)'
  },
  {
    id: 3,
    name: 'Hava Filtresi',
    code: 'HF-1001',
    quantity: 8,
    stockPercent: 16,
    stockClass: 'low',
    gradient: 'linear-gradient(135deg, #ef4444, #f87171)'
  }
])

// Methods
const navigateTo = (path) => {
  console.log('Navigate to:', path)
}

const handleServiceClick = (service) => {
  console.log('Service clicked:', service)
}

const handleVehicleClick = (vehicle) => {
  console.log('Vehicle clicked:', vehicle)
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

.card:nth-child(1) { grid-column: span 4; }
.card:nth-child(2) { grid-column: span 8; }
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

/* Vehicles */
.vehicles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.vehicle-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s;
}

.vehicle-card:hover {
  transform: translateY(-4px);
  border-color: rgba(255, 255, 255, 0.1);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
}

.vehicle-image {
  height: 140px;
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
  padding: 12px;
}

.vehicle-badge {
  padding: 6px 12px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 600;
  backdrop-filter: blur(10px);
}

.vehicle-badge.new {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.vehicle-badge.used {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.vehicle-info {
  padding: 16px;
}

.vehicle-name {
  font-size: 14px;
  font-weight: 600;
  color: white;
  margin: 0 0 8px 0;
}

.vehicle-specs {
  font-size: 12px;
  color: #9ca3af;
  margin: 0 0 12px 0;
}

.vehicle-price {
  font-size: 16px;
  font-weight: 700;
  color: var(--sector-accent);
  margin: 0;
}

/* Test Drives */
.test-drives-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.drive-item {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.drive-time {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--sector-accent);
  font-weight: 600;
  min-width: 80px;
}

.drive-info {
  flex: 1;
}

.drive-customer {
  font-size: 14px;
  font-weight: 600;
  color: white;
  margin: 0 0 4px 0;
}

.drive-vehicle {
  font-size: 12px;
  color: #9ca3af;
  margin: 0;
}

.drive-status {
  padding: 6px 12px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 600;
}

.drive-status.confirmed {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.drive-status.pending {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.drive-status.scheduled {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

/* Parts */
.parts-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.part-item {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.part-info {
  flex: 1;
}

.part-name {
  font-size: 14px;
  font-weight: 600;
  color: white;
  margin: 0 0 4px 0;
}

.part-code {
  font-size: 11px;
  color: #6b7280;
  margin: 0;
  font-family: 'JetBrains Mono', monospace;
}

.part-stock {
  min-width: 180px;
}

.stock-bar {
  height: 6px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 6px;
}

.stock-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

.stock-text {
  font-size: 12px;
  color: #9ca3af;
}

@media (max-width: 1200px) {
  .content-grid > .card {
    grid-column: span 12 !important;
  }
  
  .vehicles-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .vehicles-grid {
    grid-template-columns: 1fr;
  }
}
</style>
