<template>
  <DashboardLayout sector="legal" :sector-icon="Scale">
    <!-- Stats Overview -->
    <section class="stats-grid">
      <StatCard
        :icon="Briefcase"
        label="Aktif Davalar"
        :value="stats.activeCases"
        change="+5.2%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/cases')"
      />
      <StatCard
        :icon="Calendar"
        label="Bugünkü Görüşmeler"
        :value="stats.todayMeetings"
        change="+3.1%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/meetings')"
      />
      <StatCard
        :icon="FileText"
        label="Bekleyen Belgeler"
        :value="stats.pendingDocuments"
        change="-8.5%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/documents')"
      />
      <StatCard
        :icon="DollarSign"
        label="Aylık Gelir"
        :value="`₺${stats.monthlyRevenue.toLocaleString('tr-TR')}`"
        change="+12.7%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        :animated="false"
        @click="navigateTo('/billing')"
      />
    </section>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- Today's Appointments -->
      <section class="card">
        <ActivityFeed
          title="Bugünkü Görüşmeler"
          :items="todayMeetings"
          @item-click="handleMeetingClick"
          @view-all="navigateTo('/meetings')"
        />
      </section>

      <!-- Case Status Chart -->
      <section class="card chart-card">
        <div class="card-header">
          <h3 class="card-title">Dava Durumları</h3>
        </div>
        <div class="chart-wrapper">
          <InteractiveChart
            type="doughnut"
            :data="caseStatusData"
            :gradient="false"
          />
        </div>
        <div class="chart-legend">
          <div v-for="(item, index) in caseStatusLegend" :key="index" class="legend-item">
            <div class="legend-dot" :style="{ background: item.color }"></div>
            <span class="legend-label">{{ item.label }}</span>
            <span class="legend-value">{{ item.value }}</span>
          </div>
        </div>
      </section>

      <!-- Active Cases -->
      <section class="card cases-card">
        <div class="card-header">
          <h3 class="card-title">Aktif Davalar</h3>
          <button class="btn-link" @click="navigateTo('/cases')">Tümünü Gör</button>
        </div>
        <div class="cases-list">
          <div 
            v-for="caseItem in activeCases" 
            :key="caseItem.id"
            class="case-item"
            @click="handleCaseClick(caseItem)"
          >
            <div class="case-header">
              <div class="case-number">{{ caseItem.caseNumber }}</div>
              <div class="case-status" :class="caseItem.statusClass">
                {{ caseItem.status }}
              </div>
            </div>
            <p class="case-title">{{ caseItem.title }}</p>
            <p class="case-client">{{ caseItem.client }}</p>
            <div class="case-footer">
              <div class="case-date">
                <Clock :size="14" />
                <span>{{ caseItem.nextHearing }}</span>
              </div>
              <div class="case-lawyer">{{ caseItem.lawyer }}</div>
            </div>
          </div>
        </div>
      </section>

      <!-- Court Calendar -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">
            <CalendarDays :size="20" />
            Mahkeme Takvimi
          </h3>
        </div>
        <div class="court-calendar">
          <div 
            v-for="hearing in courtHearings" 
            :key="hearing.id"
            class="hearing-item"
          >
            <div class="hearing-date">
              <div class="date-day">{{ hearing.day }}</div>
              <div class="date-month">{{ hearing.month }}</div>
            </div>
            <div class="hearing-info">
              <p class="hearing-case">{{ hearing.caseNumber }}</p>
              <p class="hearing-court">{{ hearing.court }}</p>
              <p class="hearing-time">{{ hearing.time }}</p>
            </div>
            <button class="btn-reminder" @click="setReminder(hearing)">
              <Bell :size="16" />
            </button>
          </div>
        </div>
      </section>

      <!-- Billing Overview -->
      <section class="card billing-card">
        <div class="card-header">
          <h3 class="card-title">Faturalandırma</h3>
        </div>
        <div class="billing-stats">
          <div class="billing-stat">
            <div class="stat-icon" style="background: linear-gradient(135deg, #10b981, #34d399)">
              <TrendingUp :size="20" />
            </div>
            <div>
              <p class="stat-label">Tahsil Edilen</p>
              <p class="stat-value">₺{{ stats.collected.toLocaleString('tr-TR') }}</p>
            </div>
          </div>
          <div class="billing-stat">
            <div class="stat-icon" style="background: linear-gradient(135deg, #f59e0b, #fbbf24)">
              <Clock :size="20" />
            </div>
            <div>
              <p class="stat-label">Bekleyen</p>
              <p class="stat-value">₺{{ stats.pending.toLocaleString('tr-TR') }}</p>
            </div>
          </div>
          <div class="billing-stat">
            <div class="stat-icon" style="background: linear-gradient(135deg, #ef4444, #f87171)">
              <AlertCircle :size="20" />
            </div>
            <div>
              <p class="stat-label">Gecikmiş</p>
              <p class="stat-value">₺{{ stats.overdue.toLocaleString('tr-TR') }}</p>
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
  Scale, Briefcase, Calendar, FileText, DollarSign, Clock,
  CalendarDays, Bell, TrendingUp, AlertCircle
} from 'lucide-vue-next'
import DashboardLayout from '../../components/dashboard/DashboardLayout.vue'
import StatCard from '../../components/dashboard/StatCard.vue'
import ActivityFeed from '../../components/dashboard/ActivityFeed.vue'
import InteractiveChart from '../../components/dashboard/InteractiveChart.vue'
import { useSectorTheme } from '../../composables/useSectorTheme'

const router = useRouter()
const { theme } = useSectorTheme('legal')

// Stats
const stats = ref({
  activeCases: 34,
  todayMeetings: 8,
  pendingDocuments: 12,
  monthlyRevenue: 285000,
  collected: 185000,
  pending: 75000,
  overdue: 25000
})

// Today's Meetings
const todayMeetings = ref([
  {
    id: 1,
    icon: Calendar,
    iconGradient: 'linear-gradient(135deg, #3b82f6, #60a5fa)',
    title: 'Müvekkil Görüşmesi',
    subtitle: 'Ahmet Yılmaz • Boşanma Davası',
    time: '10:00',
    badge: 'Yaklaşıyor',
    badgeType: 'warning'
  },
  {
    id: 2,
    icon: Calendar,
    iconGradient: 'linear-gradient(135deg, #10b981, #34d399)',
    title: 'Mahkeme Duruşması',
    subtitle: 'Ticari Alacak Davası',
    time: '14:30',
    badge: 'Planlandı',
    badgeType: 'info'
  }
])

// Case Status Data
const caseStatusData = computed(() => ({
  labels: ['Devam Eden', 'Kazanılan', 'Kaybedilen', 'Beklemede'],
  datasets: [{
    data: [18, 12, 3, 1],
    backgroundColor: [
      '#3b82f6',
      '#10b981',
      '#ef4444',
      '#f59e0b'
    ],
    borderWidth: 0
  }]
}))

const caseStatusLegend = [
  { label: 'Devam Eden', value: 18, color: '#3b82f6' },
  { label: 'Kazanılan', value: 12, color: '#10b981' },
  { label: 'Kaybedilen', value: 3, color: '#ef4444' },
  { label: 'Beklemede', value: 1, color: '#f59e0b' }
]

// Active Cases
const activeCases = ref([
  {
    id: 1,
    caseNumber: '2024/123',
    title: 'Ticari Alacak Davası',
    client: 'ABC Şirketi',
    status: 'Duruşma',
    statusClass: 'status-hearing',
    nextHearing: '15 Şubat 2026',
    lawyer: 'Av. Mehmet Demir'
  },
  {
    id: 2,
    caseNumber: '2024/089',
    title: 'İş Hukuku Uyuşmazlığı',
    client: 'Ayşe Kaya',
    status: 'Tahkikat',
    statusClass: 'status-investigation',
    nextHearing: '22 Şubat 2026',
    lawyer: 'Av. Zeynep Arslan'
  },
  {
    id: 3,
    caseNumber: '2023/456',
    title: 'Gayrimenkul Uyuşmazlığı',
    client: 'Can Öztürk',
    status: 'Karar',
    statusClass: 'status-decision',
    nextHearing: '28 Şubat 2026',
    lawyer: 'Av. Ali Çelik'
  }
])

// Court Hearings
const courtHearings = ref([
  {
    id: 1,
    day: '15',
    month: 'ŞUB',
    caseNumber: '2024/123',
    court: 'Ankara 5. Asliye Ticaret Mahkemesi',
    time: '10:00'
  },
  {
    id: 2,
    day: '22',
    month: 'ŞUB',
    caseNumber: '2024/089',
    court: 'İstanbul 12. İş Mahkemesi',
    time: '14:30'
  },
  {
    id: 3,
    day: '28',
    month: 'ŞUB',
    caseNumber: '2023/456',
    court: 'İzmir 3. Asliye Hukuk Mahkemesi',
    time: '11:00'
  }
])

// Methods
const navigateTo = (path) => {
  console.log('Navigate to:', path)
}

const handleMeetingClick = (meeting) => {
  console.log('Meeting clicked:', meeting)
}

const handleCaseClick = (caseItem) => {
  console.log('Case clicked:', caseItem)
}

const setReminder = (hearing) => {
  console.log('Set reminder for:', hearing)
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
.card:nth-child(2) { grid-column: span 4; }
.card:nth-child(3) { grid-column: span 4; }
.card:nth-child(4) { grid-column: span 6; }
.card:nth-child(5) { grid-column: span 6; }

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

.chart-wrapper {
  height: 250px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-legend {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.legend-label {
  flex: 1;
  font-size: 13px;
  color: #9ca3af;
}

.legend-value {
  font-size: 14px;
  font-weight: 600;
  color: white;
}

/* Cases */
.cases-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.case-item {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.case-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.case-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.case-number {
  font-size: 12px;
  font-weight: 700;
  color: var(--sector-accent);
  font-family: 'JetBrains Mono', monospace;
}

.case-status {
  padding: 4px 10px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 600;
}

.status-hearing {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.status-investigation {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.status-decision {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.case-title {
  font-size: 14px;
  font-weight: 600;
  color: white;
  margin: 0 0 8px 0;
}

.case-client {
  font-size: 13px;
  color: #9ca3af;
  margin: 0 0 12px 0;
}

.case-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.case-date {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #6b7280;
}

.case-lawyer {
  font-size: 12px;
  color: #9ca3af;
  font-weight: 600;
}

/* Court Calendar */
.court-calendar {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.hearing-item {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.hearing-date {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  background: var(--sector-gradient);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.date-day {
  font-size: 24px;
  font-weight: 700;
  color: white;
  line-height: 1;
}

.date-month {
  font-size: 11px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
  margin-top: 4px;
}

.hearing-info {
  flex: 1;
}

.hearing-case {
  font-size: 12px;
  font-weight: 700;
  color: var(--sector-accent);
  margin: 0 0 6px 0;
  font-family: 'JetBrains Mono', monospace;
}

.hearing-court {
  font-size: 13px;
  color: white;
  margin: 0 0 4px 0;
}

.hearing-time {
  font-size: 12px;
  color: #9ca3af;
  margin: 0;
}

.btn-reminder {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: #9ca3af;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-reminder:hover {
  background: var(--sector-gradient);
  color: white;
  border-color: transparent;
}

/* Billing */
.billing-stats {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.billing-stat {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.billing-stat .stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.billing-stat .stat-label {
  font-size: 12px;
  color: #9ca3af;
  margin: 0 0 6px 0;
}

.billing-stat .stat-value {
  font-size: 18px;
  font-weight: 700;
  color: white;
  margin: 0;
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
