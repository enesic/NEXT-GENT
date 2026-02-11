<template>
  <DashboardLayout sector="retail" :sector-icon="Store">
    <!-- Stats Overview -->
    <section class="stats-grid">
      <StatCard
        :icon="TrendingUp"
        label="Bugünkü Satışlar"
        :value="`₺${stats.todaySales.toLocaleString('tr-TR')}`"
        change="+16.8%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        :animated="false"
        @click="navigateTo('/sales')"
      />
      <StatCard
        :icon="Users"
        label="Müşteri Trafiği"
        :value="stats.customerTraffic"
        change="+22.3%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/traffic')"
      />
      <StatCard
        :icon="Package"
        label="Stok Durumu"
        :value="`${stats.stockLevel}%`"
        change="+5.2%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        :animated="false"
        @click="navigateTo('/inventory')"
      />
      <StatCard
        :icon="UserCheck"
        label="Personel Performansı"
        :value="`${stats.staffPerformance}%`"
        change="+8.7%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        :animated="false"
        @click="navigateTo('/staff')"
      />
    </section>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- Top Products Chart -->
      <section class="card chart-card">
        <div class="card-header">
          <h3 class="card-title">En Çok Satan Ürünler</h3>
        </div>
        <div class="chart-wrapper">
          <InteractiveChart
            type="bar"
            :data="topProductsData"
            :gradient-colors="['rgba(124, 58, 237, 0.8)', 'rgba(124, 58, 237, 0.3)']"
          />
        </div>
      </section>

      <!-- Customer Traffic Heatmap -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">Müşteri Yoğunluğu</h3>
        </div>
        <div class="heatmap-grid">
          <div 
            v-for="hour in trafficHeatmap" 
            :key="hour.time"
            class="heatmap-cell"
            :class="`intensity-${hour.intensity}`"
            @click="handleHourClick(hour)"
          >
            <span class="hour-label">{{ hour.time }}</span>
            <span class="hour-count">{{ hour.count }}</span>
          </div>
        </div>
      </section>

      <!-- Inventory Status -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">Kategori Bazlı Stok</h3>
        </div>
        <div class="inventory-list">
          <div 
            v-for="category in inventoryByCategory" 
            :key="category.id"
            class="inventory-item"
          >
            <div class="category-info">
              <div class="category-icon" :style="{ background: category.gradient }">
                <component :is="category.icon" :size="20" />
              </div>
              <div>
                <p class="category-name">{{ category.name }}</p>
                <p class="category-items">{{ category.items }} ürün</p>
              </div>
            </div>
            <div class="stock-indicator" :class="category.stockStatus">
              <div class="stock-bar">
                <div class="stock-fill" :style="{ width: `${category.stockPercent}%`, background: category.gradient }"></div>
              </div>
              <span class="stock-label">{{ category.stockPercent }}%</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Staff Performance -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">Personel Performansı</h3>
        </div>
        <div class="staff-list">
          <div 
            v-for="staff in staffPerformance" 
            :key="staff.id"
            class="staff-item"
            @click="handleStaffClick(staff)"
          >
            <div class="staff-rank">{{ staff.rank }}</div>
            <div class="staff-avatar" :style="{ background: staff.avatarColor }">
              {{ staff.name[0] }}
            </div>
            <div class="staff-info">
              <p class="staff-name">{{ staff.name }}</p>
              <p class="staff-role">{{ staff.role }}</p>
            </div>
            <div class="staff-stats">
              <div class="stat-item">
                <ShoppingBag :size="14" />
                <span>{{ staff.sales }}</span>
              </div>
              <div class="stat-item">
                <TrendingUp :size="14" />
                <span>₺{{ staff.revenue.toLocaleString('tr-TR') }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Recent Transactions -->
      <section class="card">
        <ActivityFeed
          title="Son İşlemler"
          :items="recentTransactions"
          @item-click="handleTransactionClick"
          @view-all="navigateTo('/transactions')"
        />
      </section>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Store, TrendingUp, Users, Package, UserCheck,
  ShoppingBag, Shirt, Watch, Smartphone
} from 'lucide-vue-next'
import DashboardLayout from '../../components/dashboard/DashboardLayout.vue'
import StatCard from '../../components/dashboard/StatCard.vue'
import ActivityFeed from '../../components/dashboard/ActivityFeed.vue'
import InteractiveChart from '../../components/dashboard/InteractiveChart.vue'
import { useSectorTheme } from '../../composables/useSectorTheme'

const router = useRouter()
const { theme } = useSectorTheme('retail')

// Stats
const stats = ref({
  todaySales: 28500,
  customerTraffic: 342,
  stockLevel: 87,
  staffPerformance: 94
})

// Top Products Data
const topProductsData = computed(() => ({
  labels: ['Giyim', 'Elektronik', 'Aksesuar', 'Ayakkabı', 'Kozmetik'],
  datasets: [{
    label: 'Satış Adedi',
    data: [145, 98, 87, 76, 54]
  }]
}))

// Traffic Heatmap
const trafficHeatmap = ref([
  { time: '09:00', count: 12, intensity: 'low' },
  { time: '10:00', count: 28, intensity: 'medium' },
  { time: '11:00', count: 45, intensity: 'high' },
  { time: '12:00', count: 62, intensity: 'very-high' },
  { time: '13:00', count: 58, intensity: 'high' },
  { time: '14:00', count: 41, intensity: 'high' },
  { time: '15:00', count: 52, intensity: 'high' },
  { time: '16:00', count: 67, intensity: 'very-high' },
  { time: '17:00', count: 71, intensity: 'very-high' },
  { time: '18:00', count: 84, intensity: 'very-high' },
  { time: '19:00', count: 56, intensity: 'high' },
  { time: '20:00', count: 32, intensity: 'medium' }
])

// Inventory by Category
const inventoryByCategory = ref([
  {
    id: 1,
    name: 'Giyim',
    icon: Shirt,
    gradient: 'linear-gradient(135deg, #7c3aed, #8b5cf6)',
    items: 245,
    stockPercent: 92,
    stockStatus: 'good'
  },
  {
    id: 2,
    name: 'Elektronik',
    icon: Smartphone,
    gradient: 'linear-gradient(135deg, #3b82f6, #60a5fa)',
    items: 87,
    stockPercent: 45,
    stockStatus: 'low'
  },
  {
    id: 3,
    name: 'Aksesuar',
    icon: Watch,
    gradient: 'linear-gradient(135deg, #10b981, #34d399)',
    items: 156,
    stockPercent: 78,
    stockStatus: 'good'
  }
])

// Staff Performance
const staffPerformance = ref([
  {
    id: 1,
    rank: 1,
    name: 'Ayşe Yılmaz',
    role: 'Satış Danışmanı',
    avatarColor: 'linear-gradient(135deg, #7c3aed, #8b5cf6)',
    sales: 45,
    revenue: 12500
  },
  {
    id: 2,
    rank: 2,
    name: 'Mehmet Demir',
    role: 'Satış Danışmanı',
    avatarColor: 'linear-gradient(135deg, #3b82f6, #60a5fa)',
    sales: 38,
    revenue: 9800
  },
  {
    id: 3,
    rank: 3,
    name: 'Zeynep Kaya',
    role: 'Kıdemli Danışman',
    avatarColor: 'linear-gradient(135deg, #10b981, #34d399)',
    sales: 32,
    revenue: 8200
  }
])

// Recent Transactions
const recentTransactions = ref([
  {
    id: 1,
    icon: ShoppingBag,
    iconGradient: 'linear-gradient(135deg, #7c3aed, #8b5cf6)',
    title: 'Satış #5678',
    subtitle: 'Giyim • ₺450',
    time: '2 dk',
    badge: 'Tamamlandı',
    badgeType: 'success'
  },
  {
    id: 2,
    icon: ShoppingBag,
    iconGradient: 'linear-gradient(135deg, #3b82f6, #60a5fa)',
    title: 'İade #5677',
    subtitle: 'Elektronik • ₺1,200',
    time: '15 dk',
    badge: 'İşlemde',
    badgeType: 'warning'
  }
])

// Methods
const navigateTo = (path) => {
  console.log('Navigate to:', path)
}

const handleHourClick = (hour) => {
  console.log('Hour clicked:', hour)
}

const handleStaffClick = (staff) => {
  console.log('Staff clicked:', staff)
}

const handleTransactionClick = (transaction) => {
  console.log('Transaction clicked:', transaction)
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

.card:nth-child(1) { grid-column: span 6; }
.card:nth-child(2) { grid-column: span 6; }
.card:nth-child(3) { grid-column: span 4; }
.card:nth-child(4) { grid-column: span 4; }
.card:nth-child(5) { grid-column: span 4; }

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
}

.chart-wrapper {
  height: 280px;
}

/* Heatmap */
.heatmap-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
  gap: 12px;
}

.heatmap-cell {
  aspect-ratio: 1;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.heatmap-cell.intensity-low {
  background: rgba(124, 58, 237, 0.1);
}

.heatmap-cell.intensity-medium {
  background: rgba(124, 58, 237, 0.3);
}

.heatmap-cell.intensity-high {
  background: rgba(124, 58, 237, 0.5);
}

.heatmap-cell.intensity-very-high {
  background: rgba(124, 58, 237, 0.7);
}

.heatmap-cell:hover {
  transform: scale(1.05);
  border-color: rgba(124, 58, 237, 0.5);
}

.hour-label {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 4px;
}

.hour-count {
  font-size: 18px;
  font-weight: 700;
  color: white;
}

/* Inventory */
.inventory-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.inventory-item {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.category-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.category-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.category-name {
  font-size: 14px;
  font-weight: 600;
  color: white;
  margin: 0 0 4px 0;
}

.category-items {
  font-size: 12px;
  color: #9ca3af;
  margin: 0;
}

.stock-indicator {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 150px;
}

.stock-bar {
  flex: 1;
  height: 6px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 3px;
  overflow: hidden;
}

.stock-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

.stock-label {
  font-size: 12px;
  font-weight: 600;
  color: white;
  min-width: 40px;
  text-align: right;
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
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.staff-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  transform: translateX(4px);
}

.staff-rank {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: var(--sector-gradient);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  color: white;
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

.staff-role {
  font-size: 12px;
  color: #9ca3af;
  margin: 0;
}

.staff-stats {
  display: flex;
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #9ca3af;
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
  
  .heatmap-grid {
    grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
  }
}
</style>
