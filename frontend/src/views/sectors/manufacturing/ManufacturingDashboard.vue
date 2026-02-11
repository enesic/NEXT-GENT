<template>
  <DashboardLayout sector="manufacturing" :sector-icon="Factory">
    <!-- Stats Overview -->
    <section class="stats-grid">
      <StatCard
        :icon="Activity"
        label="Üretim Hattı Durumu"
        :value="`${stats.productionStatus}%`"
        change="+4.2%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        :animated="false"
        @click="navigateTo('/production')"
      />
      <StatCard
        :icon="CheckCircle"
        label="Kalite Skoru"
        :value="`${stats.qualityScore}%`"
        change="+2.8%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        :animated="false"
        @click="navigateTo('/quality')"
      />
      <StatCard
        :icon="Package"
        label="Stok Seviyesi"
        :value="`${stats.inventoryLevel}%`"
        change="-3.5%"
        changeType="negative"
        :gradient="theme.primaryGradient"
        :animated="false"
        @click="navigateTo('/inventory')"
      />
      <StatCard
        :icon="TrendingUp"
        label="Sipariş Karşılama"
        :value="`${stats.orderFulfillment}%`"
        change="+6.1%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        :animated="false"
        @click="navigateTo('/orders')"
      />
    </section>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- Production Lines -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">Üretim Hatları</h3>
        </div>
        <div class="production-lines">
          <div 
            v-for="line in productionLines" 
            :key="line.id"
            class="production-line"
            @click="handleLineClick(line)"
          >
            <div class="line-header">
              <div class="line-name">
                <component :is="line.icon" :size="20" />
                <span>{{ line.name }}</span>
              </div>
              <div class="line-status" :class="line.statusClass">
                {{ line.status }}
              </div>
            </div>
            <div class="line-metrics">
              <div class="metric">
                <span class="metric-label">Üretim</span>
                <span class="metric-value">{{ line.production }}/{{ line.target }}</span>
              </div>
              <div class="metric">
                <span class="metric-label">Verimlilik</span>
                <span class="metric-value">{{ line.efficiency }}%</span>
              </div>
            </div>
            <div class="line-progress">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: `${line.progress}%`, background: line.gradient }"></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Quality Metrics -->
      <section class="card chart-card">
        <div class="card-header">
          <h3 class="card-title">Kalite Metrikleri</h3>
        </div>
        <div class="chart-wrapper">
          <InteractiveChart
            type="line"
            :data="qualityData"
            :gradient-colors="['rgba(100, 116, 139, 0.8)', 'rgba(100, 116, 139, 0.1)']"
          />
        </div>
      </section>

      <!-- Inventory Levels -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">Envanter Seviyeleri</h3>
        </div>
        <div class="inventory-items">
          <div 
            v-for="item in inventoryItems" 
            :key="item.id"
            class="inventory-item"
          >
            <div class="item-info">
              <p class="item-name">{{ item.name }}</p>
              <p class="item-code">{{ item.code }}</p>
            </div>
            <div class="item-level" :class="item.levelClass">
              <div class="level-bar">
                <div class="level-fill" :style="{ width: `${item.level}%`, background: item.gradient }"></div>
              </div>
              <span class="level-text">{{ item.quantity }} / {{ item.max }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Order Fulfillment -->
      <section class="card">
        <ActivityFeed
          title="Sipariş Durumu"
          :items="orderStatus"
          @item-click="handleOrderClick"
          @view-all="navigateTo('/orders')"
        />
      </section>

      <!-- Equipment Status -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">
            <Settings :size="20" />
            Ekipman Durumu
          </h3>
        </div>
        <div class="equipment-grid">
          <div 
            v-for="equipment in equipmentStatus" 
            :key="equipment.id"
            class="equipment-card"
            :class="equipment.statusClass"
            @click="handleEquipmentClick(equipment)"
          >
            <div class="equipment-icon" :style="{ background: equipment.gradient }">
              <component :is="equipment.icon" :size="24" />
            </div>
            <p class="equipment-name">{{ equipment.name }}</p>
            <p class="equipment-status">{{ equipment.status }}</p>
            <div class="equipment-uptime">
              <Clock :size="14" />
              <span>{{ equipment.uptime }}% çalışma</span>
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
  Factory, Activity, CheckCircle, Package, TrendingUp,
  Settings, Clock, Cpu, Zap, Cog
} from 'lucide-vue-next'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import StatCard from '@/components/dashboard/StatCard.vue'
import ActivityFeed from '@/components/dashboard/ActivityFeed.vue'
import InteractiveChart from '@/components/dashboard/InteractiveChart.vue'
import { useSectorTheme } from '@/composables/useSectorTheme'
import { vRipple } from '@/composables/useRipple'

const router = useRouter()
const { theme } = useSectorTheme('manufacturing')

// Stats
const stats = ref({
  productionStatus: 92,
  qualityScore: 96,
  inventoryLevel: 78,
  orderFulfillment: 94
})

// Production Lines
const productionLines = ref([
  {
    id: 1,
    name: 'Hat A - Montaj',
    icon: Cpu,
    status: 'Aktif',
    statusClass: 'active',
    production: 245,
    target: 300,
    efficiency: 92,
    progress: 82,
    gradient: 'linear-gradient(135deg, #64748b, #94a3b8)'
  },
  {
    id: 2,
    name: 'Hat B - Paketleme',
    icon: Package,
    status: 'Aktif',
    statusClass: 'active',
    production: 180,
    target: 200,
    efficiency: 95,
    progress: 90,
    gradient: 'linear-gradient(135deg, #10b981, #34d399)'
  },
  {
    id: 3,
    name: 'Hat C - Kalite Kontrol',
    icon: CheckCircle,
    status: 'Bakımda',
    statusClass: 'maintenance',
    production: 0,
    target: 150,
    efficiency: 0,
    progress: 0,
    gradient: 'linear-gradient(135deg, #f59e0b, #fbbf24)'
  }
])

// Quality Data
const qualityData = computed(() => ({
  labels: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
  datasets: [{
    label: 'Kalite Skoru (%)',
    data: [94, 95, 96, 95, 97, 96, 96]
  }]
}))

// Inventory Items
const inventoryItems = ref([
  {
    id: 1,
    name: 'Hammadde A',
    code: 'HM-001',
    quantity: 850,
    max: 1000,
    level: 85,
    levelClass: 'good',
    gradient: 'linear-gradient(135deg, #10b981, #34d399)'
  },
  {
    id: 2,
    name: 'Komponent B',
    code: 'KM-045',
    quantity: 320,
    max: 500,
    level: 64,
    levelClass: 'medium',
    gradient: 'linear-gradient(135deg, #f59e0b, #fbbf24)'
  },
  {
    id: 3,
    name: 'Paketleme Malzemesi',
    code: 'PK-012',
    quantity: 150,
    max: 1000,
    level: 15,
    levelClass: 'low',
    gradient: 'linear-gradient(135deg, #ef4444, #f87171)'
  }
])

// Order Status
const orderStatus = ref([
  {
    id: 1,
    icon: Package,
    iconGradient: 'linear-gradient(135deg, #10b981, #34d399)',
    title: 'Sipariş #5678',
    subtitle: 'ABC Şirketi • 500 adet',
    time: '2 gün',
    badge: 'Üretimde',
    badgeType: 'info'
  },
  {
    id: 2,
    icon: CheckCircle,
    iconGradient: 'linear-gradient(135deg, #64748b, #94a3b8)',
    title: 'Sipariş #5677',
    subtitle: 'XYZ Ltd. • 300 adet',
    time: '1 gün',
    badge: 'Tamamlandı',
    badgeType: 'success'
  }
])

// Equipment Status
const equipmentStatus = ref([
  {
    id: 1,
    name: 'CNC Torna',
    icon: Cog,
    status: 'Çalışıyor',
    statusClass: 'operational',
    uptime: 98,
    gradient: 'linear-gradient(135deg, #10b981, #34d399)'
  },
  {
    id: 2,
    name: 'Pres Makinesi',
    icon: Zap,
    status: 'Çalışıyor',
    statusClass: 'operational',
    uptime: 95,
    gradient: 'linear-gradient(135deg, #3b82f6, #60a5fa)'
  },
  {
    id: 3,
    name: 'Paketleme Ünitesi',
    icon: Package,
    status: 'Bakımda',
    statusClass: 'maintenance',
    uptime: 0,
    gradient: 'linear-gradient(135deg, #f59e0b, #fbbf24)'
  },
  {
    id: 4,
    name: 'Kalite Test Cihazı',
    icon: CheckCircle,
    status: 'Çalışıyor',
    statusClass: 'operational',
    uptime: 100,
    gradient: 'linear-gradient(135deg, #64748b, #94a3b8)'
  }
])

// Methods
const navigateTo = (path) => {
  console.log('Navigate to:', path)
}

const handleLineClick = (line) => {
  console.log('Line clicked:', line)
}

const handleOrderClick = (order) => {
  console.log('Order clicked:', order)
}

const handleEquipmentClick = (equipment) => {
  console.log('Equipment clicked:', equipment)
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
  display: flex;
  align-items: center;
  gap: 8px;
}

.chart-wrapper {
  height: 280px;
}

/* Production Lines */
.production-lines {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.production-line {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.production-line:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

.line-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.line-name {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: white;
}

.line-status {
  padding: 4px 10px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 600;
}

.line-status.active {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.line-status.maintenance {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.line-metrics {
  display: flex;
  gap: 24px;
  margin-bottom: 12px;
}

.metric {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.metric-label {
  font-size: 11px;
  color: #6b7280;
}

.metric-value {
  font-size: 14px;
  font-weight: 700;
  color: white;
}

.line-progress {
  margin-top: 12px;
}

.progress-bar {
  height: 6px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

/* Inventory */
.inventory-items {
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

.item-info {
  flex: 1;
}

.item-name {
  font-size: 14px;
  font-weight: 600;
  color: white;
  margin: 0 0 4px 0;
}

.item-code {
  font-size: 11px;
  color: #6b7280;
  margin: 0;
  font-family: 'JetBrains Mono', monospace;
}

.item-level {
  min-width: 200px;
}

.level-bar {
  height: 6px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 6px;
}

.level-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

.level-text {
  font-size: 12px;
  color: #9ca3af;
}

/* Equipment */
.equipment-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 16px;
}

.equipment-card {
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

.equipment-card:hover {
  transform: translateY(-4px);
  border-color: rgba(255, 255, 255, 0.1);
}

.equipment-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-bottom: 12px;
}

.equipment-name {
  font-size: 13px;
  font-weight: 600;
  color: white;
  margin: 0 0 6px 0;
}

.equipment-status {
  font-size: 11px;
  color: #9ca3af;
  margin: 0 0 8px 0;
}

.equipment-uptime {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: #6b7280;
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
  
  .equipment-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  }
}
</style>
