<template>
  <DashboardLayout sector="ecommerce" :sector-icon="ShoppingBag">
    <!-- Stats Overview -->
    <section class="stats-grid">
      <StatCard
        :icon="TrendingUp"
        label="Günlük Sipariş"
        :value="stats.dailyOrders"
        change="+18.2%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/orders')"
      />
      <StatCard
        :icon="Users"
        label="Aktif Müşteri"
        :value="stats.activeCustomers"
        change="+5.3%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/customers')"
      />
      <StatCard
        :icon="Package"
        label="Kargo Bekleyen"
        :value="stats.pendingShipments"
        change="+3.1%"
        changeType="neutral"
        :gradient="theme.primaryGradient"
        :animated="false"
        @click="navigateTo('/shipments')"
      />
      <StatCard
        :icon="BarChart2"
        label="Dönüşüm Oranı"
        :value="`${stats.conversionRate}%`"
        change="+0.8%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        :animated="false"
        @click="navigateTo('/analytics')"
      />
    </section>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- Order Trend Chart -->
      <section class="card chart-card">
        <div class="card-header">
          <h3 class="card-title">Sipariş Trendi</h3>
          <div class="period-pills">
            <button
              v-for="p in periods"
              :key="p"
              :class="['pill', { active: selectedPeriod === p }]"
              @click="selectedPeriod = p"
            >{{ p }}</button>
          </div>
        </div>
        <div class="chart-wrapper">
          <InteractiveChart
            type="area"
            :data="orderTrendData"
            :gradient-colors="['rgba(249, 115, 22, 0.8)', 'rgba(249, 115, 22, 0.1)']"
          />
        </div>
      </section>

      <!-- Category Breakdown Donut -->
      <section class="card donut-card">
        <div class="card-header">
          <h3 class="card-title">Kategori Dağılımı</h3>
        </div>
        <div class="category-list">
          <div
            v-for="cat in categoryBreakdown"
            :key="cat.name"
            class="category-row"
          >
            <div class="cat-dot" :style="{ background: cat.color }"></div>
            <span class="cat-name">{{ cat.name }}</span>
            <div class="cat-bar-wrap">
              <div class="cat-bar" :style="{ width: cat.percent + '%', background: cat.color }"></div>
            </div>
            <span class="cat-percent">{{ cat.percent }}%</span>
          </div>
        </div>
      </section>

      <!-- Top Products -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">En Çok Satan Ürünler</h3>
        </div>
        <div class="product-list">
          <div
            v-for="(product, i) in topProducts"
            :key="product.id"
            class="product-row"
          >
            <span class="product-rank" :style="{ color: theme.primary }">#{{ i + 1 }}</span>
            <div class="product-icon" :style="{ background: theme.primary + '22' }">
              <component :is="product.icon" :size="18" :style="{ color: theme.primary }" />
            </div>
            <div class="product-info">
              <p class="product-name">{{ product.name }}</p>
              <p class="product-stats">{{ product.sold }} adet • ₺{{ product.revenue.toLocaleString('tr-TR') }}</p>
            </div>
            <div class="product-trend" :class="product.trend > 0 ? 'up' : 'down'">
              {{ product.trend > 0 ? '+' : '' }}{{ product.trend }}%
            </div>
          </div>
        </div>
      </section>

      <!-- Pending Orders -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">Bekleyen Siparişler</h3>
          <span class="badge-count" :style="{ background: theme.primary + '22', color: theme.primary }">
            {{ pendingOrders.length }}
          </span>
        </div>
        <div class="order-list">
          <div
            v-for="order in pendingOrders"
            :key="order.id"
            class="order-row"
            @click="handleOrderClick(order)"
          >
            <div class="order-id" :style="{ color: theme.primary }">
              #{{ order.id }}
            </div>
            <div class="order-info">
              <p class="order-customer">{{ order.customer }}</p>
              <p class="order-items">{{ order.items }} ürün</p>
            </div>
            <div class="order-amount">₺{{ order.amount.toLocaleString('tr-TR') }}</div>
            <div class="order-status" :class="`status-${order.status}`">
              {{ statusLabel(order.status) }}
            </div>
          </div>
        </div>
      </section>

      <!-- Recent Activity Feed -->
      <section class="card">
        <ActivityFeed
          title="Son Aktiviteler"
          :items="recentActivity"
          @item-click="handleActivityClick"
          @view-all="navigateTo('/activity')"
        />
      </section>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import {
  ShoppingBag, TrendingUp, Users, Package, BarChart2,
  Shirt, Smartphone, Watch, Tag, Box
} from 'lucide-vue-next'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import StatCard from '@/components/dashboard/StatCard.vue'
import ActivityFeed from '@/components/dashboard/ActivityFeed.vue'
import InteractiveChart from '@/components/dashboard/InteractiveChart.vue'
import { useSectorTheme } from '@/composables/useSectorTheme'

const router = useRouter()
const { theme } = useSectorTheme('ecommerce')

// ── Stats ──────────────────────────────────────────────────────────────────
const stats = ref({
  dailyOrders:      '1,284',
  activeCustomers:  '25.4K',
  pendingShipments: '342',
  conversionRate:   3.2
})

// ── Period Selector ────────────────────────────────────────────────────────
const periods = ['7G', '30G', '90G']
const selectedPeriod = ref('30G')

// ── Order Trend Chart ──────────────────────────────────────────────────────
const orderTrendData = computed(() => ({
  labels: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
  datasets: [{
    label: 'Siparişler',
    data: [980, 1100, 1050, 1200, 1350, 1500, 1100]
  }]
}))

// ── Category Breakdown ─────────────────────────────────────────────────────
const categoryBreakdown = ref([
  { name: 'Elektronik',  percent: 35, color: '#f97316' },
  { name: 'Giyim',       percent: 28, color: '#fb923c' },
  { name: 'Ev & Yaşam',  percent: 18, color: '#fed7aa' },
  { name: 'Spor',        percent: 12, color: '#fde68a' },
  { name: 'Diğer',       percent:  7, color: '#9ca3af' },
])

// ── Top Products ───────────────────────────────────────────────────────────
const topProducts = ref([
  { id: 1, name: 'Akıllı Saat Pro',    icon: Watch,       sold: 284,  revenue: 420000, trend: +22.5 },
  { id: 2, name: 'Kablosuz Kulaklık',  icon: Smartphone,  sold: 215,  revenue: 215000, trend: +14.2 },
  { id: 3, name: 'Spor Ayakkabı',      icon: Tag,         sold: 198,  revenue: 148500, trend: +8.7  },
  { id: 4, name: 'Yazlık Elbise',      icon: Shirt,       sold: 176,  revenue:  88000, trend: +31.3 },
  { id: 5, name: 'Kargolu Kutu Set',   icon: Box,         sold: 142,  revenue:  71000, trend: -3.2  },
])

// ── Pending Orders ─────────────────────────────────────────────────────────
const pendingOrders = ref([
  { id: 10582, customer: 'Ahmet Yılmaz',  items: 3, amount: 1240, status: 'processing' },
  { id: 10581, customer: 'Fatma Demir',   items: 1, amount:  450, status: 'pending'    },
  { id: 10580, customer: 'Mehmet Kaya',   items: 5, amount: 2800, status: 'shipping'   },
  { id: 10579, customer: 'Zeynep Çelik',  items: 2, amount:  890, status: 'pending'    },
  { id: 10578, customer: 'Ali Özkan',     items: 4, amount: 1680, status: 'processing' },
])

const STATUS_LABELS = {
  pending:    'Beklemede',
  processing: 'Hazırlanıyor',
  shipping:   'Kargoda',
  delivered:  'Teslim Edildi',
}
const statusLabel = (s) => STATUS_LABELS[s] || s

// ── Recent Activity ────────────────────────────────────────────────────────
const recentActivity = ref([
  { id: 1, icon: ShoppingBag, iconGradient: 'linear-gradient(135deg,#f97316,#ea580c)', title: 'Yeni Sipariş #10582', subtitle: 'Ahmet Yılmaz • ₺1,240', time: '2 dk önce',   badge: 'Yeni',       badgeType: 'info'    },
  { id: 2, icon: TrendingUp,  iconGradient: 'linear-gradient(135deg,#10b981,#059669)', title: 'Ödeme Onaylandı',    subtitle: 'Sipariş #10578 • ₺1,680',  time: '8 dk önce',   badge: 'Onaylandı',  badgeType: 'success' },
  { id: 3, icon: Package,     iconGradient: 'linear-gradient(135deg,#3b82f6,#2563eb)', title: 'Kargo Gönderildi',  subtitle: 'Sipariş #10576 • Yurtiçi',  time: '25 dk önce',  badge: 'Kargoda',    badgeType: 'warning' },
  { id: 4, icon: Users,       iconGradient: 'linear-gradient(135deg,#8b5cf6,#7c3aed)', title: 'Yeni Kayıt',        subtitle: 'Zeynep Çelik',               time: '1 saat önce', badge: 'Müşteri',    badgeType: 'info'    },
])

// ── Methods ────────────────────────────────────────────────────────────────
const navigateTo = (path) => router.push(path).catch(() => {})
const handleOrderClick    = (order)    => console.log('Order clicked:', order)
const handleActivityClick = (activity) => console.log('Activity clicked:', activity)
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
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

.chart-card    { grid-column: span 8; }
.donut-card    { grid-column: span 4; }
.card:nth-child(3) { grid-column: span 6; }
.card:nth-child(4) { grid-column: span 6; }
.card:nth-child(5) { grid-column: span 12; }

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 8px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: white;
}

/* Period Pills */
.period-pills { display: flex; gap: 4px; }

.pill {
  padding: 4px 12px;
  border-radius: 99px;
  font-size: 12px;
  font-weight: 600;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
  color: rgba(255,255,255,0.5);
  cursor: pointer;
  transition: all 0.2s;
}

.pill.active {
  background: rgba(249, 115, 22, 0.2);
  border-color: rgba(249, 115, 22, 0.4);
  color: #fb923c;
}

.chart-wrapper { height: 260px; }

/* Badge Count */
.badge-count {
  padding: 4px 10px;
  border-radius: 99px;
  font-size: 12px;
  font-weight: 700;
}

/* Category List */
.category-list { display: flex; flex-direction: column; gap: 14px; }

.category-row {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
}

.cat-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.cat-name { color: rgba(255,255,255,0.7); min-width: 80px; }

.cat-bar-wrap {
  flex: 1;
  height: 6px;
  background: rgba(255,255,255,0.06);
  border-radius: 3px;
  overflow: hidden;
}

.cat-bar { height: 100%; border-radius: 3px; transition: width 0.6s ease; }
.cat-percent { color: white; font-weight: 600; min-width: 36px; text-align: right; }

/* Products */
.product-list { display: flex; flex-direction: column; gap: 12px; }

.product-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px;
  border-radius: 12px;
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.04);
  transition: all 0.2s;
  cursor: default;
}

.product-row:hover {
  background: rgba(255,255,255,0.05);
  border-color: rgba(249,115,22,0.2);
}

.product-rank { font-size: 13px; font-weight: 700; min-width: 24px; }

.product-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.product-info { flex: 1; }
.product-name  { font-size: 13px; font-weight: 600; color: white;        margin: 0 0 3px 0; }
.product-stats { font-size: 11px; color: rgba(255,255,255,0.5); margin: 0; }

.product-trend { font-size: 12px; font-weight: 700; }
.product-trend.up   { color: #10b981; }
.product-trend.down { color: #ef4444; }

/* Orders */
.order-list { display: flex; flex-direction: column; gap: 10px; }

.order-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 12px;
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.04);
  cursor: pointer;
  transition: all 0.2s;
}

.order-row:hover {
  background: rgba(255,255,255,0.05);
  border-color: rgba(249,115,22,0.2);
  transform: translateX(4px);
}

.order-id        { font-size: 13px; font-weight: 700; min-width: 56px; }
.order-info      { flex: 1; }
.order-customer  { font-size: 13px; font-weight: 600; color: white; margin: 0 0 2px 0; }
.order-items     { font-size: 11px; color: rgba(255,255,255,0.5); margin: 0; }
.order-amount    { font-size: 13px; font-weight: 700; color: white; }

.order-status {
  padding: 4px 10px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
}

.status-pending    { background: rgba(245,158,11,0.15);  color: #f59e0b; }
.status-processing { background: rgba(59,130,246,0.15);  color: #60a5fa; }
.status-shipping   { background: rgba(16,185,129,0.15);  color: #34d399; }
.status-delivered  { background: rgba(156,163,175,0.15); color: #9ca3af; }

@media (max-width: 1200px) {
  .content-grid > .card { grid-column: span 12 !important; }
}

@media (max-width: 768px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .period-pills { flex-wrap: wrap; }
}
</style>
