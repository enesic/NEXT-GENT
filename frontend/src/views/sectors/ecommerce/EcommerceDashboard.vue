<template>
  <DashboardLayout sector="ecommerce" :sector-icon="ShoppingCart">
  <div class="ecommerce-dashboard">
    <!-- Decorative Welcome - Her zaman görünür -->
    <div class="ecommerce-welcome">
      <span class="ecommerce-divider"></span>
      <p class="ecommerce-tagline">E-ticaret yönetiminizin merkezi</p>
      <span class="ecommerce-divider"></span>
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
      <section class="stats-grid ecommerce-stats">
        <SkeletonStatCard v-for="i in 4" :key="i" />
      </section>
    </template>

    <!-- Data Loaded -->
    <template v-else>
    <!-- Quick Action Bar -->
    <div class="quick-actions">
      <button class="quick-btn primary-btn" @click="navigateTo('/orders')">
        <Package :size="18" :stroke-width="2" />
        Yeni Sipariş Oluştur
      </button>
      <div class="quick-stats">
        <span class="quick-stat">
          <span class="qs-dot confirmed"></span>
          {{ stats.todayOrders }} sipariş bugün
        </span>
      </div>
    </div>
    <!-- Stats Overview -->
    <section class="stats-grid ecommerce-stats">
      <StatCard
        :icon="Package"
        label="Bugünkü Siparişler"
        :value="stats.todayOrders"
        change="+12%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/orders')"
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
      <!-- Today's Orders -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">Bugünün Siparişleri</h3>
          <button v-ripple class="btn-link" @click="navigateTo('/orders')" aria-label="Tüm siparişleri gör">Tümünü Gör</button>
        </div>
        <div class="orders-list">
          <div 
            v-for="order in todayOrders" 
            :key="order.id"
            v-ripple
            class="order-item"
            @click="handleOrderClick(order)"
            role="button"
            tabindex="0"
            :aria-label="`Sipariş ${order.customer}`"
            @keydown.enter="handleOrderClick(order)"
            @keydown.space.prevent="handleOrderClick(order)"
          >
            <div class="order-time">
              <Clock :size="16" />
              <span>{{ order.time }}</span>
            </div>
            <div class="order-details">
              <p class="customer-name">{{ order.customer }}</p>
              <p class="product-name">{{ order.product }}</p>
            </div>
            <div class="order-status" :class="order.statusClass">
              {{ order.statusText }}
            </div>
          </div>
        </div>
      </section>

      <!-- Popular Products -->
      <section class="card chart-card">
        <div class="card-header">
          <h3 class="card-title">Popüler Ürünler</h3>
        </div>
        <div class="chart-wrapper">
          <InteractiveChart
            type="doughnut"
            :data="productsData"
            :gradient-colors="['#f97316', '#ea580c', '#f59e0b', '#22c55e']"
          />
        </div>
        <div class="products-legend">
          <div 
            v-for="product in topProducts" 
            :key="product.name"
            class="legend-item"
            @click="handleProductClick(product)"
          >
            <div class="legend-dot" :style="{ background: product.color }"></div>
            <span class="legend-label">{{ product.name }}</span>
            <span class="legend-value">{{ product.count }}</span>
          </div>
        </div>
      </section>

      <!-- Revenue Trend -->
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
          <SkeletonChart v-if="revenueChartLoading || !revenueChartData" type="line" />
          <InteractiveChart
            v-else
            type="line"
            :data="revenueChartData"
            :gradient-colors="['rgba(249, 115, 22, 0.8)', 'rgba(249, 115, 22, 0.1)']"
          />
        </div>
      </section>

      <!-- Top Sellers -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">
            <Trophy :size="20" />
            En Çok Satanlar
          </h3>
        </div>
        <div class="sellers-list">
          <div 
            v-for="item in topSellers" 
            :key="item.id"
            class="seller-item"
            @click="handleSellerClick(item)"
          >
            <div class="seller-info">
              <div class="seller-avatar" :style="{ background: item.gradient }">
                {{ item.name[0] }}
              </div>
              <div>
                <p class="seller-name">{{ item.name }}</p>
                <p class="seller-category">{{ item.category }}</p>
              </div>
            </div>
            <div class="seller-metrics">
              <div class="metric">
                <Package :size="14" />
                <span>{{ item.sales }}</span>
              </div>
              <div class="metric">
                <Star :size="14" :fill="'#f59e0b'" :stroke="'#f59e0b'" />
                <span>{{ item.rating }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
    </template>
  </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { 
  ShoppingCart, Package, DollarSign, Users, Star,
  Clock, Trophy
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

const router = useRouter()
const { theme } = useSectorTheme('ecommerce')
const analyticsStore = useAnalyticsStore()

// Fetch dashboard data with WebSocket support
const { kpis, pulse, satisfaction, isLoading, hasError, retry } = useDashboardData({
  enableWebSocket: true,
  fetchSatisfaction: true
})

// Transform backend KPIs to stats (E-commerce sector)
const stats = computed(() => {
  const defaultStats = {
    todayOrders: 28,
    totalRevenue: 45680,
    activeClients: 156,
    averageRating: '4.8'
  }

  if (!kpis.value || kpis.value.length === 0) {
    return {
      ...defaultStats,
      todayOrders: pulse.value?.pendingAppointments ?? defaultStats.todayOrders,
      totalRevenue: pulse.value?.totalRevenue ?? defaultStats.totalRevenue,
      activeClients: pulse.value?.todayClients ?? defaultStats.activeClients,
      averageRating: String(satisfaction?.value?.average ?? defaultStats.averageRating)
    }
  }

  return {
    todayOrders: pulse.value?.pendingAppointments ?? defaultStats.todayOrders,
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

// Today's Orders
const todayOrders = ref([
  { id: 1, time: '09:00', customer: 'Ayşe Yılmaz', product: 'Premium Kulaklık', statusClass: 'confirmed', statusText: 'Onaylı' },
  { id: 2, time: '10:30', customer: 'Elif Demir', product: 'Akıllı Saat', statusClass: 'confirmed', statusText: 'Onaylı' },
  { id: 3, time: '11:00', customer: 'Selin Kaya', product: 'Kablosuz Mouse', statusClass: 'in-progress', statusText: 'Hazırlanıyor' },
  { id: 4, time: '13:00', customer: 'Deniz Çelik', product: 'Mekanik Klavye', statusClass: 'confirmed', statusText: 'Onaylı' },
  { id: 5, time: '14:30', customer: 'Burcu Arslan', product: 'USB Hub', statusClass: 'pending', statusText: 'Bekliyor' }
])

// Top Products
const topProducts = ref([
  { name: 'Premium Kulaklık', count: 45, color: '#f97316' },
  { name: 'Akıllı Saat', count: 38, color: '#ea580c' },
  { name: 'Kablosuz Mouse', count: 32, color: '#f59e0b' },
  { name: 'Mekanik Klavye', count: 28, color: '#22c55e' }
])

// Products Data for Chart
const productsData = computed(() => ({
  labels: topProducts.value.map(p => p.name),
  datasets: [{
    data: topProducts.value.map(p => p.count),
    backgroundColor: topProducts.value.map(p => p.color)
  }]
}))

// Revenue Chart (fetched from backend)
const revenueChartData = ref(null)
const revenueChartLoading = ref(false)

// Top Sellers
const topSellers = ref([
  { id: 1, name: 'Electronics', category: 'Elektronik', sales: 142, rating: 4.9, gradient: 'linear-gradient(135deg, #f97316, #ea580c)' },
  { id: 2, name: 'Accessories', category: 'Aksesuar', sales: 98, rating: 4.8, gradient: 'linear-gradient(135deg, #ea580c, #f97316)' },
  { id: 3, name: 'Computers', category: 'Bilgisayar', sales: 85, rating: 4.7, gradient: 'linear-gradient(135deg, #f59e0b, #f97316)' },
  { id: 4, name: 'Phones', category: 'Telefon', sales: 72, rating: 4.9, gradient: 'linear-gradient(135deg, #0891b2, #22c55e)' }
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

const handleSellerClick = (item) => {
  console.log('Seller clicked:', item)
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
          label: 'Satış (₺)',
          data: [5200, 6800, 5900, 7200, 8100, 9500, 6800]
        }]
      }
    }
  } catch (error) {
    console.error('Failed to load revenue chart:', error)
    revenueChartData.value = {
      labels: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
      datasets: [{
        label: 'Satış (₺)',
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
   E-TİCARET – Güzellik Merkezi Dashboard Kopyası
   ═══════════════════════════════════════════════════════════════ */

.ecommerce-dashboard {
  font-family: 'Cormorant Garamond', 'Inter', serif;
  min-height: 100%;
  position: relative;
  margin: -32px;
  padding: 32px;
  background: 
    radial-gradient(ellipse 80% 50% at 50% -10%, rgba(249, 115, 22, 0.08) 0%, transparent 50%),
    radial-gradient(ellipse 60% 40% at 100% 50%, rgba(234, 88, 12, 0.05) 0%, transparent 50%),
    radial-gradient(ellipse 50% 30% at 0% 80%, rgba(251, 146, 60, 0.03) 0%, transparent 50%),
    linear-gradient(180deg, #0c0a0a 0%, #0a0808 100%);
}

.quick-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28px;
  padding: 18px 24px;
  background: rgba(249, 115, 22, 0.04);
  border: 1px solid rgba(249, 115, 22, 0.15);
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
  background: linear-gradient(135deg, #f97316, #ea580c);
  color: white;
  box-shadow: 0 4px 16px rgba(249, 115, 22, 0.35);
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(249, 115, 22, 0.45);
}

.quick-stats { display: flex; align-items: center; gap: 16px; }
.quick-stat { display: flex; align-items: center; gap: 8px; font-size: 14px; color: rgba(253, 242, 248, 0.7); font-weight: 500; }
.qs-dot { width: 8px; height: 8px; border-radius: 50%; }
.qs-dot.confirmed { background: #34d399; box-shadow: 0 0 8px rgba(52, 211, 153, 0.5); }

.ecommerce-welcome {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 32px;
  padding: 0 16px;
}

.ecommerce-divider {
  flex: 1;
  max-width: 120px;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(249, 115, 22, 0.5), transparent);
  opacity: 0.8;
}

.ecommerce-tagline {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: #fdba74;
  margin: 0;
  text-shadow: 0 0 20px rgba(249, 115, 22, 0.3);
}

.stats-grid.ecommerce-stats {
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

.card {
  background: linear-gradient(160deg, rgba(26, 22, 24, 0.9) 0%, rgba(12, 10, 10, 0.95) 100%);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(249, 115, 22, 0.12);
  border-radius: 24px;
  padding: 28px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(249, 115, 22, 0.3), transparent);
  opacity: 0.6;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.35), 0 0 0 1px rgba(249, 115, 22, 0.15);
  border-color: rgba(249, 115, 22, 0.25);
}

.card:nth-child(1) { grid-column: span 6; }
.card:nth-child(2) { grid-column: span 6; }
.card:nth-child(3) { grid-column: span 8; }
.card:nth-child(4) { grid-column: span 4; }

.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.card-title { font-family: 'Playfair Display', Georgia, serif; font-size: 19px; font-weight: 600; letter-spacing: 0.02em; margin: 0; color: #fdf2f8; display: flex; align-items: center; gap: 10px; }

.btn-link {
  background: transparent;
  border: 1px solid rgba(249, 115, 22, 0.4);
  color: #fdba74;
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
  background: rgba(249, 115, 22, 0.15);
  color: #fdf2f8;
  border-color: rgba(249, 115, 22, 0.6);
}

.time-filters { display: flex; gap: 8px; }
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

.filter-btn:hover { background: rgba(249, 115, 22, 0.1); color: #fdf2f8; border-color: rgba(249, 115, 22, 0.3); }
.filter-btn.active { background: linear-gradient(135deg, #f97316, #ea580c); color: white; border-color: transparent; box-shadow: 0 4px 16px rgba(249, 115, 22, 0.35); }
.chart-wrapper { height: 280px; }

.orders-list { display: flex; flex-direction: column; gap: 14px; }
.order-item {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.02) 0%, rgba(255, 255, 255, 0.01) 100%);
  border: 1px solid rgba(249, 115, 22, 0.08);
  border-radius: 16px;
  padding: 18px 20px;
  display: flex;
  align-items: center;
  gap: 18px;
  cursor: pointer;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.order-item:hover {
  background: rgba(249, 115, 22, 0.06);
  border-color: rgba(249, 115, 22, 0.2);
  transform: translateX(6px);
  box-shadow: 0 4px 20px rgba(249, 115, 22, 0.08);
}

.order-time { display: flex; align-items: center; gap: 8px; font-size: 14px; color: #fdba74; font-weight: 600; min-width: 72px; }
.order-details { flex: 1; }
.customer-name { font-family: 'Playfair Display', Georgia, serif; font-size: 15px; font-weight: 600; color: #fdf2f8; margin: 0 0 4px 0; }
.product-name { font-size: 13px; color: rgba(253, 242, 248, 0.6); margin: 0; }

.order-status { padding: 8px 14px; border-radius: 24px; font-size: 11px; font-weight: 600; letter-spacing: 0.04em; }
.order-status.confirmed { background: rgba(52, 211, 153, 0.12); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.25); }
.order-status.in-progress { background: rgba(251, 191, 36, 0.12); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.25); }
.order-status.pending { background: rgba(168, 85, 247, 0.12); color: #c4b5fd; border: 1px solid rgba(168, 85, 247, 0.25); }

.products-legend { display: flex; flex-direction: column; gap: 14px; margin-top: 24px; }
.legend-item { display: flex; align-items: center; gap: 14px; padding: 12px 14px; border-radius: 14px; cursor: pointer; transition: all 0.3s; border: 1px solid transparent; }
.legend-item:hover { background: rgba(249, 115, 22, 0.06); border-color: rgba(249, 115, 22, 0.15); }
.legend-dot { width: 14px; height: 14px; border-radius: 50%; box-shadow: 0 0 12px currentColor; }
.legend-label { flex: 1; font-family: 'Cormorant Garamond', serif; font-size: 15px; font-weight: 500; color: #fdf2f8; }
.legend-value { font-family: 'Playfair Display', Georgia, serif; font-size: 16px; font-weight: 600; color: #fdba74; }

.sellers-list { display: flex; flex-direction: column; gap: 14px; }
.seller-item {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.02) 0%, transparent 100%);
  border: 1px solid rgba(249, 115, 22, 0.08);
  border-radius: 18px;
  padding: 18px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.seller-item:hover { background: rgba(249, 115, 22, 0.06); border-color: rgba(249, 115, 22, 0.2); transform: translateX(4px); box-shadow: 0 4px 24px rgba(249, 115, 22, 0.08); }
.seller-info { display: flex; align-items: center; gap: 14px; }
.seller-info .seller-avatar { width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 18px; border: 2px solid rgba(249, 115, 22, 0.25); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); }
.seller-name { font-family: 'Playfair Display', Georgia, serif; font-size: 15px; font-weight: 600; color: #fdf2f8; margin: 0 0 4px 0; }
.seller-category { font-size: 13px; color: rgba(253, 242, 248, 0.6); margin: 0; }
.seller-metrics { display: flex; gap: 20px; }
.metric { display: flex; align-items: center; gap: 8px; font-size: 14px; color: #fdf2f8; font-weight: 600; }

@media (max-width: 1200px) { .content-grid > .card { grid-column: span 12 !important; } }
@media (max-width: 768px) {
  .ecommerce-dashboard { margin: -20px -16px; padding: 20px 16px; }
  .stats-grid.ecommerce-stats { grid-template-columns: 1fr; }
  .ecommerce-welcome { flex-direction: column; gap: 12px; }
  .ecommerce-divider { max-width: 80px; }
  .ecommerce-tagline { font-size: 13px; letter-spacing: 0.15em; }
  .card { padding: 20px; border-radius: 20px; }
}
</style>
