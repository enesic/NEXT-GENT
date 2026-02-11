<template>
  <DashboardLayout sector="real_estate" :sector-icon="Home">
    <!-- Stats Overview -->
    <section class="stats-grid">
      <StatCard
        :icon="Building"
        label="Aktif İlanlar"
        :value="stats.activeListings"
        change="+8.2%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/listings')"
      />
      <StatCard
        :icon="Calendar"
        label="Bugünkü Geziler"
        :value="stats.todayViewings"
        change="+12.5%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/viewings')"
      />
      <StatCard
        :icon="TrendingUp"
        label="Aylık Satışlar"
        :value="stats.monthlySales"
        change="+18.3%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/sales')"
      />
      <StatCard
        :icon="DollarSign"
        label="Toplam Komisyon"
        :value="`₺${stats.totalCommission.toLocaleString('tr-TR')}`"
        change="+22.7%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        :animated="false"
        @click="navigateTo('/commission')"
      />
    </section>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- Property Listings -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">Öne Çıkan İlanlar</h3>
          <button class="btn-link" @click="navigateTo('/listings')">Tümünü Gör</button>
        </div>
        <div class="properties-grid">
          <div 
            v-for="property in featuredProperties" 
            :key="property.id"
            class="property-card"
            @click="handlePropertyClick(property)"
          >
            <div class="property-image" :style="{ background: property.imageGradient }">
              <div class="property-badge" :class="property.type">{{ property.typeLabel }}</div>
            </div>
            <div class="property-info">
              <p class="property-title">{{ property.title }}</p>
              <p class="property-location">
                <MapPin :size="14" />
                {{ property.location }}
              </p>
              <div class="property-details">
                <span><Bed :size="14" /> {{ property.bedrooms }}</span>
                <span><Bath :size="14" /> {{ property.bathrooms }}</span>
                <span><Maximize :size="14" /> {{ property.area }}m²</span>
              </div>
              <p class="property-price">₺{{ property.price.toLocaleString('tr-TR') }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Sales Pipeline -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">Satış Hunisi</h3>
        </div>
        <div class="pipeline-stages">
          <div 
            v-for="stage in pipelineStages" 
            :key="stage.id"
            class="pipeline-stage"
            @click="handleStageClick(stage)"
          >
            <div class="stage-header">
              <span class="stage-name">{{ stage.name }}</span>
              <span class="stage-count">{{ stage.count }}</span>
            </div>
            <div class="stage-bar">
              <div class="stage-fill" :style="{ width: `${stage.percent}%`, background: stage.gradient }"></div>
            </div>
            <p class="stage-value">₺{{ stage.value.toLocaleString('tr-TR') }}</p>
          </div>
        </div>
      </section>

      <!-- Viewing Schedule -->
      <section class="card">
        <ActivityFeed
          title="Gezi Programı"
          :items="viewingSchedule"
          @item-click="handleViewingClick"
          @view-all="navigateTo('/viewings')"
        />
      </section>

      <!-- Market Trends -->
      <section class="card chart-card">
        <div class="card-header">
          <h3 class="card-title">Piyasa Trendleri</h3>
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
            :data="marketTrendsData"
            :gradient-colors="['rgba(16, 185, 129, 0.8)', 'rgba(16, 185, 129, 0.1)']"
          />
        </div>
      </section>

      <!-- Agent Performance -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">
            <Trophy :size="20" />
            Danışman Performansı
          </h3>
        </div>
        <div class="agents-list">
          <div 
            v-for="agent in topAgents" 
            :key="agent.id"
            class="agent-item"
          >
            <div class="agent-rank">{{ agent.rank }}</div>
            <div class="agent-avatar" :style="{ background: agent.avatarColor }">
              {{ agent.name[0] }}
            </div>
            <div class="agent-info">
              <p class="agent-name">{{ agent.name }}</p>
              <p class="agent-stats">{{ agent.sales }} satış • ₺{{ agent.commission.toLocaleString('tr-TR') }}</p>
            </div>
            <div class="agent-rating">
              <Star :size="14" :fill="'#f59e0b'" :stroke="'#f59e0b'" />
              <span>{{ agent.rating }}</span>
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
  Home, Building, Calendar, TrendingUp, DollarSign,
  MapPin, Bed, Bath, Maximize, Trophy, Star
} from 'lucide-vue-next'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import StatCard from '@/components/dashboard/StatCard.vue'
import ActivityFeed from '@/components/dashboard/ActivityFeed.vue'
import InteractiveChart from '@/components/dashboard/InteractiveChart.vue'
import { useSectorTheme } from '@/composables/useSectorTheme'
import { vRipple } from '@/composables/useRipple'

const router = useRouter()
const { theme } = useSectorTheme('real_estate')

// Stats
const stats = ref({
  activeListings: 47,
  todayViewings: 12,
  monthlySales: 8,
  totalCommission: 285000
})

// Time Filters
const timeFilters = [
  { label: '3 Ay', value: '3m' },
  { label: '6 Ay', value: '6m' },
  { label: '1 Yıl', value: '1y' }
]
const selectedTimeFilter = ref('3m')

// Featured Properties
const featuredProperties = ref([
  {
    id: 1,
    title: '3+1 Lüks Daire',
    location: 'Çankaya, Ankara',
    imageGradient: 'linear-gradient(135deg, #10b981, #34d399)',
    type: 'sale',
    typeLabel: 'Satılık',
    bedrooms: 3,
    bathrooms: 2,
    area: 145,
    price: 2500000
  },
  {
    id: 2,
    title: '2+1 Merkezi Ofis',
    location: 'Kızılay, Ankara',
    imageGradient: 'linear-gradient(135deg, #3b82f6, #60a5fa)',
    type: 'rent',
    typeLabel: 'Kiralık',
    bedrooms: 2,
    bathrooms: 1,
    area: 95,
    price: 15000
  }
])

// Pipeline Stages
const pipelineStages = ref([
  {
    id: 1,
    name: 'İlk Görüşme',
    count: 24,
    percent: 100,
    value: 12000000,
    gradient: 'linear-gradient(135deg, #10b981, #34d399)'
  },
  {
    id: 2,
    name: 'Gezi Planlandı',
    count: 18,
    percent: 75,
    value: 9000000,
    gradient: 'linear-gradient(135deg, #3b82f6, #60a5fa)'
  },
  {
    id: 3,
    name: 'Teklif Verildi',
    count: 12,
    percent: 50,
    value: 6000000,
    gradient: 'linear-gradient(135deg, #f59e0b, #fbbf24)'
  },
  {
    id: 4,
    name: 'Anlaşma',
    count: 8,
    percent: 33,
    value: 4000000,
    gradient: 'linear-gradient(135deg, #10b981, #34d399)'
  }
])

// Viewing Schedule
const viewingSchedule = ref([
  {
    id: 1,
    icon: Calendar,
    iconGradient: 'linear-gradient(135deg, #10b981, #34d399)',
    title: '3+1 Lüks Daire Gezisi',
    subtitle: 'Ahmet Yılmaz • 14:00',
    time: '2 saat',
    badge: 'Planlandı',
    badgeType: 'info'
  },
  {
    id: 2,
    icon: Calendar,
    iconGradient: 'linear-gradient(135deg, #3b82f6, #60a5fa)',
    title: 'Villa Gezisi',
    subtitle: 'Ayşe Demir • 16:30',
    time: '4 saat',
    badge: 'Onaylandı',
    badgeType: 'success'
  }
])

// Market Trends Data
const marketTrendsData = computed(() => ({
  labels: ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz'],
  datasets: [{
    label: 'Ortalama Fiyat (₺)',
    data: [2200000, 2300000, 2350000, 2400000, 2450000, 2500000]
  }]
}))

// Top Agents
const topAgents = ref([
  {
    id: 1,
    rank: 1,
    name: 'Mehmet Kaya',
    avatarColor: 'linear-gradient(135deg, #10b981, #34d399)',
    sales: 12,
    commission: 145000,
    rating: 4.9
  },
  {
    id: 2,
    rank: 2,
    name: 'Zeynep Arslan',
    avatarColor: 'linear-gradient(135deg, #3b82f6, #60a5fa)',
    sales: 9,
    commission: 98000,
    rating: 4.8
  },
  {
    id: 3,
    rank: 3,
    name: 'Can Öztürk',
    avatarColor: 'linear-gradient(135deg, #f59e0b, #fbbf24)',
    sales: 7,
    commission: 72000,
    rating: 4.7
  }
])

// Methods
const navigateTo = (path) => {
  console.log('Navigate to:', path)
}

const handlePropertyClick = (property) => {
  console.log('Property clicked:', property)
}

const handleStageClick = (stage) => {
  console.log('Stage clicked:', stage)
}

const handleViewingClick = (viewing) => {
  console.log('Viewing clicked:', viewing)
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

.card:nth-child(1) { grid-column: span 8; }
.card:nth-child(2) { grid-column: span 4; }
.card:nth-child(3) { grid-column: span 4; }
.card:nth-child(4) { grid-column: span 8; }
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

/* Properties */
.properties-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.property-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s;
}

.property-card:hover {
  transform: translateY(-4px);
  border-color: rgba(255, 255, 255, 0.1);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
}

.property-image {
  height: 140px;
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
  padding: 12px;
}

.property-badge {
  padding: 6px 12px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 600;
  backdrop-filter: blur(10px);
}

.property-badge.sale {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.property-badge.rent {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.property-info {
  padding: 16px;
}

.property-title {
  font-size: 14px;
  font-weight: 600;
  color: white;
  margin: 0 0 8px 0;
}

.property-location {
  font-size: 12px;
  color: #9ca3af;
  margin: 0 0 12px 0;
  display: flex;
  align-items: center;
  gap: 4px;
}

.property-details {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.property-details span {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #9ca3af;
}

.property-price {
  font-size: 16px;
  font-weight: 700;
  color: var(--sector-accent);
  margin: 0;
}

/* Pipeline */
.pipeline-stages {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.pipeline-stage {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.pipeline-stage:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

.stage-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.stage-name {
  font-size: 13px;
  color: white;
  font-weight: 600;
}

.stage-count {
  font-size: 14px;
  font-weight: 700;
  color: var(--sector-accent);
}

.stage-bar {
  height: 8px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.stage-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.stage-value {
  font-size: 12px;
  color: #9ca3af;
  margin: 0;
  text-align: right;
}

/* Agents */
.agents-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.agent-item {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.agent-rank {
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

.agent-avatar {
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

.agent-info {
  flex: 1;
}

.agent-name {
  font-size: 14px;
  font-weight: 600;
  color: white;
  margin: 0 0 4px 0;
}

.agent-stats {
  font-size: 12px;
  color: #9ca3af;
  margin: 0;
}

.agent-rating {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  font-weight: 600;
  color: #f59e0b;
}

@media (max-width: 1200px) {
  .content-grid > .card {
    grid-column: span 12 !important;
  }
  
  .properties-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .properties-grid {
    grid-template-columns: 1fr;
  }
}
</style>
