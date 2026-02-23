<template>
  <DashboardLayout sector="ecommerce" :sector-icon="ShoppingCart">
  <div class="ecommerce-dashboard">
    <!-- Decorative Welcome - Her zaman görünür -->
    <div class="sector-welcome">
      <span class="welcome-divider"></span>
      <p class="welcome-tagline">E-ticaret yönetiminizin merkezi</p>
      <span class="welcome-divider"></span>
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
      <section class="stats-grid sector-stats">
        <SkeletonStatCard v-for="i in 4" :key="i" />
      </section>
    </template>

    <!-- Data Loaded -->
    <template v-else>
    <!-- Quick Action Bar -->
    <div class="quick-actions">
      <div class="quick-buttons">
        <button class="quick-btn primary-btn" @click="showOrderModal = true">
          <Package :size="18" :stroke-width="2" />
          Yeni Sipariş Oluştur
        </button>
        <button class="quick-btn secondary-btn" @click="handleInventory">
          <AlertCircle :size="18" :stroke-width="2" />
          Stok Yönetimi
        </button>
        <button class="quick-btn secondary-btn" @click="router.push('/sectors/ecommerce/settings')">
          <Settings :size="18" :stroke-width="2" />
          Ayarlar
        </button>
      </div>
      <div class="quick-stats">
        <span class="quick-stat">
          <span class="qs-dot confirmed"></span>
          {{ stats.todayOrders }} sipariş bugün
        </span>
      </div>
    </div>
    <!-- Stats Overview -->
    <section class="stats-grid sector-stats">
      <StatCard
        :icon="ShoppingBag"
        label="Bugünkü Siparişler"
        :value="stats.todayOrders"
        change="+18%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/orders')"
      />
      <StatCard
        :icon="TrendingUp"
        label="Günlük Gelir"
        :value="`₺${Number(stats.dailyRevenue || 0).toLocaleString('tr-TR')}`"
        change="+24%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        :animated="false"
        @click="navigateTo('/revenue')"
      />
      <StatCard
        :icon="Users"
        label="Aktif Müşteriler"
        :value="stats.activeCustomers"
        change="+12%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/customers')"
      />
      <StatCard
        :icon="AlertCircle"
        label="Düşük Stok"
        :value="stats.lowStockItems"
        change="-5%"
        changeType="positive"
        :gradient="'linear-gradient(135deg, #f59e0b, #fbbf24)'"
        @click="navigateTo('/inventory')"
      />
    </section>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- Son Siparişler -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">Son Siparişler</h3>
          <button v-ripple class="btn-link" @click="navigateTo('/orders')" aria-label="Tüm siparişleri gör">Tümünü Gör</button>
        </div>
        <div class="orders-list">
          <div 
            v-for="order in recentOrders" 
            :key="order.id"
            v-ripple
            class="order-item"
            @click="handleOrderClick(order)"
            role="button"
            tabindex="0"
            :aria-label="`Sipariş ${order.title} detayı`"
            @keydown.enter="handleOrderClick(order)"
            @keydown.space.prevent="handleOrderClick(order)"
          >
            <div class="order-id">
              <Package :size="16" />
              <span>{{ order.title }}</span>
            </div>
            <div class="order-details">
              <p class="order-customer">{{ order.subtitle }}</p>
            </div>
            <div class="order-status" :class="order.statusClass">
              {{ order.badge }}
            </div>
          </div>
        </div>
      </section>

      <!-- Popüler Ürünler -->
      <section class="card chart-card">
        <div class="card-header">
          <h3 class="card-title">Popüler Ürünler</h3>
        </div>
        <div class="chart-wrapper">
          <InteractiveChart
            type="doughnut"
            :data="productsChartData"
            :gradient-colors="['#8b5cf6', '#a78bfa', '#3b82f6', '#10b981']"
          />
        </div>
        <div class="products-legend">
          <div 
            v-for="product in topProducts" 
            :key="product.id"
            class="legend-item"
            @click="handleProductClick(product)"
          >
            <div class="legend-dot" :style="{ background: product.color }"></div>
            <span class="legend-label">{{ product.name }}</span>
            <span class="legend-value">{{ product.sales }}</span>
          </div>
        </div>
      </section>

      <!-- Satış Trendi -->
      <section class="card chart-card">
        <div class="card-header">
          <h3 class="card-title">Satış Trendi</h3>
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
          <SkeletonChart v-if="salesChartLoading || !salesChartData" type="line" />
          <InteractiveChart
            v-else
            type="line"
            :data="salesChartData"
            :gradient-colors="['rgba(139, 92, 246, 0.8)', 'rgba(139, 92, 246, 0.1)']"
          />
        </div>
      </section>

      <!-- Kargo Durumu -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">
            <Truck :size="20" />
            Kargo Durumu
          </h3>
        </div>
        <div class="shipping-list">
          <div 
            v-for="ship in shippingStats" 
            :key="ship.label"
            class="shipping-item"
          >
            <div class="shipping-info">
              <div class="shipping-bar">
                <div class="bar-fill" :style="{ width: ship.percent + '%', background: ship.gradient }"></div>
              </div>
              <div class="shipping-meta">
                <span class="shipping-label">{{ ship.label }}</span>
                <span class="shipping-value">{{ ship.value }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- E-ticaret Metrikleri -->
      <section class="card metrics-card">
        <div class="card-header">
          <h3 class="card-title">E-ticaret Metrikleri</h3>
          <button v-ripple class="btn-link" @click="navigateTo('/analytics')" aria-label="Detaylı analitik">Detay</button>
        </div>
        <div class="ecommerce-metrics">
          <div class="metric-box">
            <div class="metric-icon-wrap" style="background: linear-gradient(135deg, #8b5cf6, #a78bfa)">
              <TrendingUp :size="20" />
            </div>
            <div class="metric-content">
              <span class="metric-label">Dönüşüm Oranı</span>
              <span class="metric-value">{{ ecommerceMetrics.conversionRate }}%</span>
              <span class="metric-trend positive">+2.1%</span>
            </div>
          </div>
          <div class="metric-box">
            <div class="metric-icon-wrap" style="background: linear-gradient(135deg, #10b981, #34d399)">
              <ShoppingCart :size="20" />
            </div>
            <div class="metric-content">
              <span class="metric-label">Sepet Terk Oranı</span>
              <span class="metric-value">{{ ecommerceMetrics.cartAbandonRate }}%</span>
              <span class="metric-trend negative">-1.3%</span>
            </div>
          </div>
          <div class="metric-box">
            <div class="metric-icon-wrap" style="background: linear-gradient(135deg, #3b82f6, #60a5fa)">
              <Users :size="20" />
            </div>
            <div class="metric-content">
              <span class="metric-label">Ort. Sipariş Değeri</span>
              <span class="metric-value">₺{{ ecommerceMetrics.avgOrderValue.toLocaleString('tr-TR') }}</span>
              <span class="metric-trend positive">+5%</span>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- Order Modal -->
    <OrderModal
      v-model="showOrderModal"
      :product-options="productOptions"
      @created="onOrderCreated"
    />
    </template>
  </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { 
  ShoppingCart, ShoppingBag, TrendingUp, Users, AlertCircle,
  Package, Truck, Settings
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
import { useNotificationStore } from '@/stores/notification'
import { vRipple } from '@/composables/useRipple'
import OrderModal from '@/components/common/OrderModal.vue'

const router = useRouter()
const notificationStore = useNotificationStore()
const { theme } = useSectorTheme('ecommerce')
const analyticsStore = useAnalyticsStore()
const showOrderModal = ref(false)

const productOptions = [
  'Premium Kulaklık',
  'Akıllı Saat',
  'Kablosuz Mouse',
  'Mekanik Klavye',
  'USB Hub',
  'Webcam',
  'Diğer'
]

// E-ticaret metrikleri
const ecommerceMetrics = ref({
  conversionRate: 3.2,
  cartAbandonRate: 68.5,
  avgOrderValue: 1250
})

// Fetch dashboard data with WebSocket support
const { kpis, pulse, satisfaction, isLoading, hasError, retry } = useDashboardData({
  enableWebSocket: true,
  fetchSatisfaction: true
})

// Transform backend KPIs to stats (E-commerce sector)
const stats = computed(() => {
  const defaultStats = {
    todayOrders: 127,
    dailyRevenue: 45800,
    activeCustomers: 1234,
    lowStockItems: 8
  }

  if (!kpis.value || kpis.value.length === 0) {
    return {
      ...defaultStats,
      todayOrders: pulse.value?.pendingAppointments ?? defaultStats.todayOrders,
      dailyRevenue: pulse.value?.totalRevenue ?? defaultStats.dailyRevenue,
      activeCustomers: pulse.value?.todayClients ?? defaultStats.activeCustomers,
      lowStockItems: kpis.value?.[3]?.value ?? defaultStats.lowStockItems
    }
  }

  return {
    todayOrders: pulse.value?.pendingAppointments ?? kpis.value[0]?.value ?? defaultStats.todayOrders,
    dailyRevenue: kpis.value[1]?.value ?? defaultStats.dailyRevenue,
    activeCustomers: pulse.value?.todayClients ?? kpis.value[2]?.value ?? defaultStats.activeCustomers,
    lowStockItems: kpis.value[3]?.value ?? defaultStats.lowStockItems
  }
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
    title: 'Sipariş #12345',
    subtitle: 'Ahmet Yılmaz • ₺450',
    badge: 'Hazırlanıyor',
    statusClass: 'processing'
  },
  {
    id: 2,
    title: 'Sipariş #12344',
    subtitle: 'Ayşe Demir • ₺1,250',
    badge: 'Kargoda',
    statusClass: 'shipping'
  },
  {
    id: 3,
    title: 'Sipariş #12343',
    subtitle: 'Mehmet Kaya • ₺780',
    badge: 'Teslim Edildi',
    statusClass: 'delivered'
  },
  {
    id: 4,
    title: 'Sipariş #12342',
    subtitle: 'Zeynep Arslan • ₺2,100',
    badge: 'Onay Bekliyor',
    statusClass: 'pending'
  },
  {
    id: 5,
    title: 'Sipariş #12341',
    subtitle: 'Can Öztürk • ₺540',
    badge: 'Hazırlanıyor',
    statusClass: 'processing'
  }
])

// Top Products
const topProducts = ref([
  { id: 1, name: 'Premium Kulaklık', sales: 145, color: '#8b5cf6' },
  { id: 2, name: 'Akıllı Saat', sales: 98, color: '#a78bfa' },
  { id: 3, name: 'Kablosuz Mouse', sales: 87, color: '#3b82f6' },
  { id: 4, name: 'Mekanik Klavye', sales: 62, color: '#10b981' }
])

// Products Chart Data
const productsChartData = computed(() => ({
  labels: topProducts.value.map(p => p.name),
  datasets: [{
    data: topProducts.value.map(p => p.sales),
    backgroundColor: topProducts.value.map(p => p.color)
  }]
}))

// Sales Chart (fetched from backend)
const salesChartData = ref(null)
const salesChartLoading = ref(false)

// Shipping Stats
const shippingStats = ref([
  { label: 'Teslim Edildi', value: 156, percent: 65, gradient: 'linear-gradient(135deg, #10b981, #34d399)' },
  { label: 'Yolda', value: 62, percent: 25, gradient: 'linear-gradient(135deg, #3b82f6, #60a5fa)' },
  { label: 'Hazırlanıyor', value: 24, percent: 10, gradient: 'linear-gradient(135deg, #f59e0b, #fbbf24)' }
])

// Methods
const navigateTo = (path) => {
  console.log('Navigate to:', path)
}

const handleOrderClick = (order) => {
  console.log('Order clicked:', order)
}

const handleProductClick = (product) => {
  console.log('Product clicked:', product)
}

const handleInventory = () => {
  navigateTo('/inventory')
}

const onOrderCreated = () => {
  notificationStore.success('Sipariş başarıyla oluşturuldu', 'E-ticaret')
  // Listeye yeni sipariş ekle (mock)
  const newId = Math.max(...recentOrders.value.map(o => o.id), 0) + 1
  recentOrders.value.unshift({
    id: newId,
    title: `Sipariş #${12345 + newId}`,
    subtitle: 'Yeni sipariş • İşleniyor',
    badge: 'Onay Bekliyor',
    statusClass: 'pending'
  })
}

// Fetch sales chart data from backend
const fetchSalesChartData = async () => {
  salesChartLoading.value = true
  try {
    const endDate = new Date().toISOString()
    const days = selectedTimeFilter.value === '7d' ? 7 : selectedTimeFilter.value === '30d' ? 30 : 90
    const startDate = new Date(Date.now() - days * 24 * 60 * 60 * 1000).toISOString()

    const response = await analyticsStore.fetchChart('revenue-by-segment', startDate, endDate)
    if (response && (response.labels || response.datasets)) {
      salesChartData.value = response
    } else {
      salesChartData.value = {
        labels: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
        datasets: [{
          label: 'Satış (₺)',
          data: [38000, 42000, 45000, 48000, 52000, 35000, 30000]
        }]
      }
    }
  } catch (error) {
    console.error('Failed to load sales chart:', error)
    salesChartData.value = {
      labels: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
      datasets: [{
        label: 'Satış (₺)',
        data: [38000, 42000, 45000, 48000, 52000, 35000, 30000]
      }]
    }
  } finally {
    salesChartLoading.value = false
  }
}

watch(selectedTimeFilter, () => {
  fetchSalesChartData()
})

onMounted(() => {
  fetchSalesChartData()
})
</script>

<style scoped>
/* ═══════════════════════════════════════════════════════════════
   E-TİCARET – Güzellik Merkezi ile Aynı Lüks Dashboard Yapısı
   ═══════════════════════════════════════════════════════════════ */

.ecommerce-dashboard {
  font-family: 'Cormorant Garamond', 'Inter', serif;
  min-height: 100%;
  position: relative;
  margin: -32px;
  padding: 32px;
  background: 
    radial-gradient(ellipse 80% 50% at 50% -10%, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
    radial-gradient(ellipse 60% 40% at 100% 50%, rgba(167, 139, 250, 0.05) 0%, transparent 50%),
    radial-gradient(ellipse 50% 30% at 0% 80%, rgba(99, 102, 241, 0.03) 0%, transparent 50%),
    linear-gradient(180deg, #0c0a0a 0%, #0a0808 100%);
}

/* Quick Actions */
.quick-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28px;
  padding: 18px 24px;
  background: rgba(139, 92, 246, 0.04);
  border: 1px solid rgba(139, 92, 246, 0.15);
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

.primary-btn {
  background: linear-gradient(135deg, #8b5cf6, #a78bfa);
  color: white;
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.35);
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(139, 92, 246, 0.45);
}

.quick-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.secondary-btn {
  background: transparent;
  border: 1px solid rgba(139, 92, 246, 0.5);
  color: #c4b5fd;
}

.secondary-btn:hover {
  background: rgba(139, 92, 246, 0.15);
  border-color: rgba(139, 92, 246, 0.7);
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
.sector-welcome {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 32px;
  padding: 0 16px;
}

.welcome-divider {
  flex: 1;
  max-width: 120px;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.5), transparent);
  opacity: 0.8;
}

.welcome-tagline {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: #c4b5fd;
  margin: 0;
  text-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
}

/* Stats Grid */
.stats-grid.sector-stats {
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

/* Cards */
.card {
  background: linear-gradient(160deg, rgba(26, 22, 24, 0.9) 0%, rgba(12, 10, 10, 0.95) 100%);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(139, 92, 246, 0.12);
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
  background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.3), transparent);
  opacity: 0.6;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.35), 0 0 0 1px rgba(139, 92, 246, 0.15);
  border-color: rgba(139, 92, 246, 0.25);
}

.card:nth-child(1) { grid-column: span 6; }
.card:nth-child(2) { grid-column: span 6; }
.card:nth-child(3) { grid-column: span 8; }
.card:nth-child(4) { grid-column: span 4; }
.card.metrics-card { grid-column: span 12; }

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
  border: 1px solid rgba(139, 92, 246, 0.4);
  color: #c4b5fd;
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
  background: rgba(139, 92, 246, 0.15);
  color: #fdf2f8;
  border-color: rgba(139, 92, 246, 0.6);
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
  background: rgba(139, 92, 246, 0.1);
  color: #fdf2f8;
  border-color: rgba(139, 92, 246, 0.3);
}

.filter-btn.active {
  background: linear-gradient(135deg, #8b5cf6, #a78bfa);
  color: white;
  border-color: transparent;
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.35);
}

.chart-wrapper {
  height: 280px;
}

/* Orders List */
.orders-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.order-item {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.02) 0%, rgba(255, 255, 255, 0.01) 100%);
  border: 1px solid rgba(139, 92, 246, 0.08);
  border-radius: 16px;
  padding: 18px 20px;
  display: flex;
  align-items: center;
  gap: 18px;
  cursor: pointer;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.order-item:hover {
  background: rgba(139, 92, 246, 0.06);
  border-color: rgba(139, 92, 246, 0.2);
  transform: translateX(6px);
  box-shadow: 0 4px 20px rgba(139, 92, 246, 0.08);
}

.order-id {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #c4b5fd;
  font-weight: 600;
  min-width: 140px;
}

.order-details {
  flex: 1;
}

.order-customer {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 15px;
  font-weight: 600;
  color: #fdf2f8;
  margin: 0;
}

.order-status {
  padding: 8px 14px;
  border-radius: 24px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.04em;
}

.order-status.delivered {
  background: rgba(52, 211, 153, 0.12);
  color: #34d399;
  border: 1px solid rgba(52, 211, 153, 0.25);
}

.order-status.shipping {
  background: rgba(59, 130, 246, 0.12);
  color: #60a5fa;
  border: 1px solid rgba(59, 130, 246, 0.25);
}

.order-status.processing {
  background: rgba(251, 191, 36, 0.12);
  color: #fbbf24;
  border: 1px solid rgba(251, 191, 36, 0.25);
}

.order-status.pending {
  background: rgba(168, 85, 247, 0.12);
  color: #c4b5fd;
  border: 1px solid rgba(168, 85, 247, 0.25);
}

/* Products Legend */
.products-legend {
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
  background: rgba(139, 92, 246, 0.06);
  border-color: rgba(139, 92, 246, 0.15);
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
  color: #c4b5fd;
}

/* Shipping */
.shipping-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.shipping-item {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.02) 0%, transparent 100%);
  border: 1px solid rgba(139, 92, 246, 0.08);
  border-radius: 16px;
  padding: 16px 20px;
  transition: all 0.35s;
}

.shipping-bar {
  height: 8px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 10px;
}

.bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.shipping-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.shipping-label {
  font-size: 13px;
  color: rgba(253, 242, 248, 0.7);
}

.shipping-value {
  font-size: 16px;
  font-weight: 700;
  color: #fdf2f8;
}

/* E-ticaret Metrikleri */
.ecommerce-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.metric-box {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.02) 0%, transparent 100%);
  border: 1px solid rgba(139, 92, 246, 0.08);
  border-radius: 16px;
  transition: all 0.3s;
}

.metric-box:hover {
  background: rgba(139, 92, 246, 0.06);
  border-color: rgba(139, 92, 246, 0.15);
}

.metric-icon-wrap {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.metric-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.metric-label {
  font-size: 12px;
  color: rgba(253, 242, 248, 0.6);
  font-weight: 500;
}

.metric-value {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 20px;
  font-weight: 700;
  color: #fdf2f8;
}

.metric-trend {
  font-size: 12px;
  font-weight: 600;
}

.metric-trend.positive {
  color: #34d399;
}

.metric-trend.negative {
  color: #f87171;
}

/* Responsive */
@media (max-width: 1200px) {
  .content-grid > .card {
    grid-column: span 12 !important;
  }
}

@media (max-width: 768px) {
  .ecommerce-dashboard {
    margin: -20px -16px;
    padding: 20px 16px;
  }

  .stats-grid.sector-stats {
    grid-template-columns: 1fr;
  }

  .sector-welcome {
    flex-direction: column;
    gap: 12px;
  }

  .welcome-divider {
    max-width: 80px;
  }

  .welcome-tagline {
    font-size: 13px;
    letter-spacing: 0.15em;
  }

  .card {
    padding: 20px;
    border-radius: 20px;
  }
}
</style>
