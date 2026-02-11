<template>
  <DashboardLayout sector="finance" :sector-icon="DollarSign">
    <!-- Stats Overview -->
    <section class="stats-grid">
      <StatCard
        :icon="Wallet"
        label="Toplam Varlıklar"
        :value="`₺${stats.totalAssets.toLocaleString('tr-TR')}`"
        change="+8.4%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        :animated="false"
        @click="navigateTo('/assets')"
      />
      <StatCard
        :icon="TrendingUp"
        label="Yatırım Getirisi"
        :value="`%${stats.investmentReturn}`"
        change="+2.3%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        :animated="false"
        @click="navigateTo('/investments')"
      />
      <StatCard
        :icon="CreditCard"
        label="Aktif Krediler"
        :value="stats.activeLoans"
        change="-3.2%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/loans')"
      />
      <StatCard
        :icon="PieChart"
        label="Bütçe Kullanımı"
        :value="`%${stats.budgetUsage}`"
        change="+5.1%"
        changeType="neutral"
        :gradient="theme.primaryGradient"
        :animated="false"
        @click="navigateTo('/budget')"
      />
    </section>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- Account Overview -->
      <section class="card accounts-card">
        <div class="card-header">
          <h3 class="card-title">Hesap Özeti</h3>
        </div>
        <div class="accounts-list">
          <div 
            v-for="account in accounts" 
            :key="account.id"
            class="account-item"
            @click="handleAccountClick(account)"
          >
            <div class="account-icon" :style="{ background: account.gradient }">
              <component :is="account.icon" :size="20" />
            </div>
            <div class="account-info">
              <p class="account-name">{{ account.name }}</p>
              <p class="account-number">{{ account.number }}</p>
            </div>
            <div class="account-balance">
              <p class="balance-amount">₺{{ account.balance.toLocaleString('tr-TR') }}</p>
              <p class="balance-change" :class="account.changeType">{{ account.change }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Investment Performance -->
      <section class="card chart-card">
        <div class="card-header">
          <h3 class="card-title">Yatırım Performansı</h3>
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
            :data="investmentData"
            :gradient-colors="['rgba(6, 182, 212, 0.8)', 'rgba(6, 182, 212, 0.1)']"
          />
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

      <!-- Budget Tracking -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">Bütçe Takibi</h3>
        </div>
        <div class="budget-list">
          <div 
            v-for="category in budgetCategories" 
            :key="category.id"
            class="budget-item"
          >
            <div class="budget-header">
              <span class="budget-name">{{ category.name }}</span>
              <span class="budget-amount">₺{{ category.spent.toLocaleString('tr-TR') }} / ₺{{ category.limit.toLocaleString('tr-TR') }}</span>
            </div>
            <div class="budget-bar">
              <div 
                class="budget-fill" 
                :style="{ 
                  width: `${(category.spent / category.limit) * 100}%`,
                  background: category.percent > 90 ? '#ef4444' : category.percent > 70 ? '#f59e0b' : '#10b981'
                }"
              ></div>
            </div>
            <span class="budget-percent">{{ category.percent }}%</span>
          </div>
        </div>
      </section>

      <!-- Loan Status -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">Kredi Durumu</h3>
        </div>
        <div class="loans-list">
          <div 
            v-for="loan in loans" 
            :key="loan.id"
            class="loan-item"
          >
            <div class="loan-info">
              <p class="loan-type">{{ loan.type }}</p>
              <p class="loan-bank">{{ loan.bank }}</p>
            </div>
            <div class="loan-details">
              <div class="detail-item">
                <span class="detail-label">Kalan</span>
                <span class="detail-value">₺{{ loan.remaining.toLocaleString('tr-TR') }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Aylık Taksit</span>
                <span class="detail-value">₺{{ loan.monthly.toLocaleString('tr-TR') }}</span>
              </div>
            </div>
            <div class="loan-progress">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: `${loan.progress}%`, background: theme.primaryGradient }"></div>
              </div>
              <span class="progress-label">%{{ loan.progress }} ödendi</span>
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
  DollarSign, Wallet, TrendingUp, CreditCard, PieChart,
  Landmark, ArrowUpRight, ArrowDownRight
} from 'lucide-vue-next'
import DashboardLayout from '../../components/dashboard/DashboardLayout.vue'
import StatCard from '../../components/dashboard/StatCard.vue'
import ActivityFeed from '../../components/dashboard/ActivityFeed.vue'
import InteractiveChart from '../../components/dashboard/InteractiveChart.vue'
import { useSectorTheme } from '../../composables/useSectorTheme'

const router = useRouter()
const { theme } = useSectorTheme('finance')

// Stats
const stats = ref({
  totalAssets: 1250000,
  investmentReturn: 12.4,
  activeLoans: 3,
  budgetUsage: 68
})

// Time Filters
const timeFilters = [
  { label: '1 Ay', value: '1m' },
  { label: '3 Ay', value: '3m' },
  { label: '1 Yıl', value: '1y' }
]
const selectedTimeFilter = ref('3m')

// Accounts
const accounts = ref([
  {
    id: 1,
    name: 'Vadesiz Hesap',
    number: '****1234',
    icon: Wallet,
    gradient: 'linear-gradient(135deg, #06b6d4, #22d3ee)',
    balance: 45000,
    change: '+₺2,500',
    changeType: 'positive'
  },
  {
    id: 2,
    name: 'Yatırım Hesabı',
    number: '****5678',
    icon: TrendingUp,
    gradient: 'linear-gradient(135deg, #10b981, #34d399)',
    balance: 125000,
    change: '+₺8,200',
    changeType: 'positive'
  },
  {
    id: 3,
    name: 'Tasarruf Hesabı',
    number: '****9012',
    icon: Landmark,
    gradient: 'linear-gradient(135deg, #3b82f6, #60a5fa)',
    balance: 78000,
    change: '+₺1,100',
    changeType: 'positive'
  }
])

// Investment Data
const investmentData = computed(() => ({
  labels: ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz'],
  datasets: [{
    label: 'Portföy Değeri (₺)',
    data: [115000, 118000, 122000, 120000, 125000, 128000]
  }]
}))

// Recent Transactions
const recentTransactions = ref([
  {
    id: 1,
    icon: ArrowUpRight,
    iconGradient: 'linear-gradient(135deg, #10b981, #34d399)',
    title: 'Maaş Yatırımı',
    subtitle: 'İşveren • ₺15,000',
    time: '2 gün',
    badge: 'Gelir',
    badgeType: 'success'
  },
  {
    id: 2,
    icon: ArrowDownRight,
    iconGradient: 'linear-gradient(135deg, #ef4444, #f87171)',
    title: 'Kira Ödemesi',
    subtitle: 'Otomatik Ödeme • ₺5,000',
    time: '5 gün',
    badge: 'Gider',
    badgeType: 'error'
  }
])

// Budget Categories
const budgetCategories = ref([
  { id: 1, name: 'Kira & Faturalar', spent: 8500, limit: 10000, percent: 85 },
  { id: 2, name: 'Yemek & Market', spent: 3200, limit: 5000, percent: 64 },
  { id: 3, name: 'Ulaşım', spent: 1800, limit: 2000, percent: 90 },
  { id: 4, name: 'Eğlence', spent: 1200, limit: 3000, percent: 40 }
])

// Loans
const loans = ref([
  {
    id: 1,
    type: 'Konut Kredisi',
    bank: 'ABC Bankası',
    remaining: 450000,
    monthly: 5200,
    progress: 35
  },
  {
    id: 2,
    type: 'Taşıt Kredisi',
    bank: 'XYZ Bankası',
    remaining: 85000,
    monthly: 2800,
    progress: 62
  }
])

// Methods
const navigateTo = (path) => {
  console.log('Navigate to:', path)
}

const handleAccountClick = (account) => {
  console.log('Account clicked:', account)
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

.card:nth-child(1) { grid-column: span 4; }
.card:nth-child(2) { grid-column: span 8; }
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

/* Accounts */
.accounts-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.account-item {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.account-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  transform: translateX(4px);
}

.account-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.account-info {
  flex: 1;
}

.account-name {
  font-size: 14px;
  font-weight: 600;
  color: white;
  margin: 0 0 4px 0;
}

.account-number {
  font-size: 12px;
  color: #9ca3af;
  margin: 0;
  font-family: 'JetBrains Mono', monospace;
}

.account-balance {
  text-align: right;
}

.balance-amount {
  font-size: 18px;
  font-weight: 700;
  color: white;
  margin: 0 0 4px 0;
}

.balance-change {
  font-size: 12px;
  font-weight: 600;
}

.balance-change.positive {
  color: #10b981;
}

/* Budget */
.budget-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.budget-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.budget-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.budget-name {
  font-size: 13px;
  color: white;
  font-weight: 600;
}

.budget-amount {
  font-size: 12px;
  color: #9ca3af;
}

.budget-bar {
  height: 8px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
  overflow: hidden;
}

.budget-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.budget-percent {
  font-size: 11px;
  color: #6b7280;
  align-self: flex-end;
}

/* Loans */
.loans-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.loan-item {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.loan-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.loan-type {
  font-size: 14px;
  font-weight: 600;
  color: white;
  margin: 0;
}

.loan-bank {
  font-size: 12px;
  color: #9ca3af;
  margin: 0;
}

.loan-details {
  display: flex;
  gap: 24px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-label {
  font-size: 11px;
  color: #6b7280;
}

.detail-value {
  font-size: 14px;
  font-weight: 700;
  color: white;
}

.loan-progress {
  display: flex;
  flex-direction: column;
  gap: 6px;
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

.progress-label {
  font-size: 11px;
  color: #9ca3af;
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
