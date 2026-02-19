<template>
  <DashboardLayout sector="ecommerce" :sector-icon="ShoppingCart">
    <!-- Stats Overview -->
    <section class="stats-grid">
      <StatCard
        :icon="ShoppingBag"
        label="Bugünkü Siparişler"
        :value="stats.todayOrders"
        change="+18.2%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/orders')"
      />
      <StatCard
        :icon="TrendingUp"
        label="Günlük Gelir"
        :value="`₺${stats.dailyRevenue.toLocaleString('tr-TR')}`"
        change="+24.5%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        :animated="false"
        @click="navigateTo('/revenue')"
      />
      <StatCard
        :icon="Users"
        label="Aktif Müşteriler"
        :value="stats.activeCustomers"
        change="+12.3%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/customers')"
      />
      <StatCard
        :icon="AlertCircle"
        label="Düşük Stok Uyarısı"
        :value="stats.lowStockItems"
        change="-5.2%"
        changeType="positive"
        :gradient="'linear-gradient(135deg, #f59e0b, #fbbf24)'"
        @click="navigateTo('/inventory')"
      />
    </section>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- Recent Orders -->
      <section class="card">
        <ActivityFeed
          title="Son Siparişler"
          :items="recentOrders"
          @item-click="handleOrderClick"
          @view-all="navigateTo('/orders')"
        />
      </section>

      <!-- Sales Chart -->
      <section class="card chart-card">
        <div class="card-header">
          <h3 class="card-title">Satış Trendi</h3>
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
            :data="salesData"
            :gradient-colors="['rgba(139, 92, 246, 0.8)', 'rgba(139, 92, 246, 0.1)']"
          />
        </div>
      </section>

      <!-- Top Products -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">En Çok Satan Ürünler</h3>
        </div>
        <div class="products-list">
          <div 
            v-for="product in topProducts" 
            :key="product.id"
            class="product-item"
            @click="handleProductClick(product)"
          >
            <div class="product-rank">{{ product.rank }}</div>
            <div class="product-image" :style="{ background: product.imageGradient }">
              <Package :size="20" />
            </div>
            <div class="product-info">
              <p class="product-name">{{ product.name }}</p>
              <p class="product-category">{{ product.category }}</p>
            </div>
            <div class="product-stats">
              <p class="product-sales">{{ product.sales }} satış</p>
              <p class="product-revenue">₺{{ product.revenue.toLocaleString('tr-TR') }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Customer Metrics -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">Müşteri Metrikleri</h3>
        </div>
        <div class="metrics-grid">
          <div class="metric-card">
            <div class="metric-icon" style="background: linear-gradient(135deg, #10b981, #34d399)">
              <UserPlus :size="20" />
            </div>
            <div>
              <p class="metric-label">Yeni Müşteriler</p>
              <p class="metric-value">{{ stats.newCustomers }}</p>
              <p class="metric-change positive">+15.3%</p>
            </div>
          </div>
          <div class="metric-card">
            <div class="metric-icon" style="background: linear-gradient(135deg, #3b82f6, #60a5fa)">
              <RefreshCw :size="20" />
            </div>
            <div>
              <p class="metric-label">Tekrar Müşteriler</p>
              <p class="metric-value">{{ stats.returningCustomers }}</p>
              <p class="metric-change positive">+8.7%</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Shipping Status -->
      <section class="card shipping-card">
        <div class="card-header">
          <h3 class="card-title">
            <Truck :size="20" />
            Kargo Durumu
          </h3>
        </div>
        <div class="shipping-stats">
          <div class="shipping-stat">
            <div class="stat-bar">
              <div class="stat-fill" style="width: 65%; background: linear-gradient(135deg, #10b981, #34d399)"></div>
            </div>
            <div class="stat-info">
              <span class="stat-label">Teslim Edildi</span>
              <span class="stat-value">156</span>
            </div>
          </div>
          <div class="shipping-stat">
            <div class="stat-bar">
              <div class="stat-fill" style="width: 25%; background: linear-gradient(135deg, #3b82f6, #60a5fa)"></div>
            </div>
            <div class="stat-info">
              <span class="stat-label">Yolda</span>
              <span class="stat-value">62</span>
            </div>
          </div>
          <div class="shipping-stat">
            <div class="stat-bar">
              <div class="stat-fill" style="width: 10%; background: linear-gradient(135deg, #f59e0b, #fbbf24)"></div>
            </div>
            <div class="stat-info">
              <span class="stat-label">Hazırlanıyor</span>
              <span class="stat-value">24</span>
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
  ShoppingCart, ShoppingBag, TrendingUp, Users, AlertCircle,
  Package, UserPlus, RefreshCw, Truck
} from 'lucide-vue-next'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import StatCard from '@/components/dashboard/StatCard.vue'
import ActivityFeed from '@/components/dashboard/ActivityFeed.vue'
import InteractiveChart from '@/components/dashboard/InteractiveChart.vue'
import { useSectorTheme } from '@/composables/useSectorTheme'
import { vRipple } from '@/composables/useRipple'

const router = useRouter()
const { theme } = useSectorTheme('ecommerce')

// Stats
const stats = ref({
  todayOrders: 127,
  dailyRevenue: 45800,
  activeCustomers: 1234,
  lowStockItems: 8,
  newCustomers: 45,
  returningCustomers: 82
})

// Time Filters
const timeFilters = [
  { label: '7 Gün', value: '7d' },
  { label: '30 Gün', value: '30d' },
  { label: '90 Gün', value: '90d' }
]
const selectedTimeFilter = ref('7d')

// Recent Orders
const recentOrders = ref([
  {
    id: 1,
    icon: ShoppingBag,
    iconGradient: 'linear-gradient(135deg, #8b5cf6, #a78bfa)',
    title: 'Sipariş #12345',
    subtitle: 'Ahmet Yılmaz • ₺450',
    time: '5 dk',
    badge: 'Hazırlanıyor',
    badgeType: 'warning'
  },
  {
    id: 2,
    icon: ShoppingBag,
    iconGradient: 'linear-gradient(135deg, #10b981, #34d399)',
    title: 'Sipariş #12344',
    subtitle: 'Ayşe Demir • ₺1,250',
    time: '15 dk',
    badge: 'Kargoda',
    badgeType: 'info'
  },
  {
    id: 3,
    icon: ShoppingBag,
    iconGradient: 'linear-gradient(135deg, #3b82f6, #60a5fa)',
    title: 'Sipariş #12343',
    subtitle: 'Mehmet Kaya • ₺780',
    time: '1 saat',
    badge: 'Teslim Edildi',
    badgeType: 'success'
  }
])

// Sales Data
const salesData = computed(() => ({
  labels: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
  datasets: [{
    label: 'Satış (₺)',
    data: [38000, 42000, 45000, 48000, 52000, 35000, 30000]
  }]
}))

// Top Products
const topProducts = ref([
  {
    id: 1,
    rank: 1,
    name: 'Premium Kulaklık',
    category: 'Elektronik',
    imageGradient: 'linear-gradient(135deg, #8b5cf6, #a78bfa)',
    sales: 145,
    revenue: 72500
  },
  {
    id: 2,
    rank: 2,
    name: 'Akıllı Saat',
    category: 'Aksesuar',
    imageGradient: 'linear-gradient(135deg, #3b82f6, #60a5fa)',
    sales: 98,
    revenue: 49000
  },
  {
    id: 3,
    rank: 3,
    name: 'Kablosuz Mouse',
    category: 'Bilgisayar',
    imageGradient: 'linear-gradient(135deg, #10b981, #34d399)',
    sales: 87,
    revenue: 26100
  }
])

// Methods
const navigateTo = (path) => {
  // Navigation within the SPA — use notification since no router pages exist yet
  console.log('Navigate to:', path)
}

const handleOrderClick = (order) => {
  console.log('Order clicked:', order)
}

const handleProductClick = (product) => {
  console.log('Product clicked:', product)
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

.card:nth-child(1) { grid-column: span 4; }
.card:nth-child(2) { grid-column: span 8; }
.card:nth-child(3) { grid-column: span 6; }
.card:nth-child(4) { grid-column: span 3; }
.card:nth-child(5) { grid-column: span 3; }

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

/* Products */
.products-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.product-item {
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

.product-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  transform: translateX(4px);
}

.product-rank {
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

.product-image {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.product-info {
  flex: 1;
}

.product-name {
  font-size: 14px;
  font-weight: 600;
  color: white;
  margin: 0 0 4px 0;
}

.product-category {
  font-size: 12px;
  color: #9ca3af;
  margin: 0;
}

.product-stats {
  text-align: right;
}

.product-sales {
  font-size: 12px;
  color: #9ca3af;
  margin: 0 0 4px 0;
}

.product-revenue {
  font-size: 14px;
  font-weight: 700;
  color: white;
  margin: 0;
}

/* Metrics */
.metrics-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.metric-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.metric-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.metric-label {
  font-size: 12px;
  color: #9ca3af;
  margin: 0 0 6px 0;
}

.metric-value {
  font-size: 24px;
  font-weight: 700;
  color: white;
  margin: 0 0 4px 0;
}

.metric-change {
  font-size: 12px;
  font-weight: 600;
}

.metric-change.positive {
  color: #10b981;
}

/* Shipping */
.shipping-stats {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.shipping-stat {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-bar {
  height: 8px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
  overflow: hidden;
}

.stat-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.stat-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-label {
  font-size: 13px;
  color: #9ca3af;
}

.stat-value {
  font-size: 16px;
  font-weight: 700;
  color: white;
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
