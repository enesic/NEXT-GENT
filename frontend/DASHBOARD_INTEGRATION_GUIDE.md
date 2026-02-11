# Dashboard Backend Integration Guide

## Quick Reference for Integrating Remaining Dashboards

This guide shows how to apply the same backend integration pattern used in Medical Dashboard to all other sector dashboards.

## Pattern Overview

Each dashboard follows this structure:
1. Import necessary composables and components
2. Use `useDashboardData()` to fetch backend data
3. Transform backend KPIs to dashboard stats
4. Fetch chart data in onMounted
5. Add loading, error, and success states in template

## Step-by-Step Integration

### Step 1: Update Script Imports

**Add these imports** to the `<script setup>` section:

```javascript
import { useDashboardData } from '../../composables/useDashboardData'
import { useAnalyticsStore } from '../../stores/analytics'
import SkeletonStatCard from '../../components/common/SkeletonStatCard.vue'
import SkeletonChart from '../../components/common/SkeletonChart.vue'
import ErrorState from '../../components/common/ErrorState.vue'
```

### Step 2: Replace Mock Data with Backend Integration

**Replace the mock stats ref** with:

```javascript
const analyticsStore = useAnalyticsStore()

// Fetch dashboard data with WebSocket support
const { kpis, pulse, isLoading, hasError, retry } = useDashboardData({
  enableWebSocket: true
})

// Transform backend KPIs to stats (customize per sector)
const stats = computed(() => {
  if (!kpis.value || kpis.value.length === 0) {
    return {
      stat1: 0,
      stat2: 0,
      stat3: 0,
      stat4: 0
    }
  }
  
  // Map KPIs to your specific stats
  return {
    stat1: pulse.value?.todayClients || 0,
    stat2: pulse.value?.pendingAppointments || 0,
    stat3: kpis.value[2]?.value || 0,
    stat4: kpis.value[3]?.value || 0
  }
})
```

### Step 3: Update Chart Data Fetching

**Replace mock chart data** with backend fetching:

```javascript
// Chart data states
const chartData = ref(null)
const chartLoading = ref(false)

// Fetch chart data
const fetchChartData = async () => {
  chartLoading.value = true
  try {
    const endDate = new Date().toISOString()
    const startDate = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString()
    
    const response = await analyticsStore.fetchChart(
      'unique-person-count',  // or other chart type
      startDate, 
      endDate
    )
    chartData.value = response
  } catch (error) {
    console.error('Failed to load chart:', error)
    // Fallback to empty data or keep existing
  } finally {
    chartLoading.value = false
  }
}

onMounted(() => {
  fetchChartData()
})
```

**Remove old computed chart data** (if any):

```javascript
// DELETE THIS:
const chartData = computed(() => ({
  labels: [...],
  datasets: [...]
}))
```

### Step 4: Update Template with Loading/Error States

**Wrap your stats grid** with conditional rendering:

```vue
<template>
  <DashboardLayout sector="your-sector" :sector-icon="YourIcon">
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
      <section class="stats-grid">
        <SkeletonStatCard v-for="i in 4" :key="i" />
      </section>
    </template>
    
    <!-- Data Loaded -->
    <template v-else>
      <!-- Your existing stats-grid here -->
      <section class="stats-grid">
        <StatCard ... />
      </section>
      
      <!-- Your existing content-grid here -->
      <div class="content-grid">
        <!-- Charts with loading -->
        <section class="card">
          <SkeletonChart v-if="chartLoading || !chartData" type="line" />
          <InteractiveChart v-else :data="chartData" />
        </section>
        
        <!-- Other sections -->
      </div>
    </template>
  </DashboardLayout>
</template>
```

**Important**: Add closing `</template>` tag before `</DashboardLayout>`!

## Chart Type Mapping

Choose the appropriate chart type for your data:

| Chart Type | Backend Endpoint | Use Case |
|------------|------------------|----------|
| `unique-person-count` | unique-person-count | Daily customer/patient flow |
| `conversion-rate` | conversion-rate | Conversion percentage over time |
| `daily-conversation-duration` | daily-conversation-duration | Call duration trends |
| `appointment-status-breakdown` | appointment-status-breakdown | Status distribution (pie) |
| `customer-segment-distribution` | customer-segment-distribution | Segment breakdown (pie) |
| `revenue-by-segment` | revenue-by-segment | Revenue by category (bar) |
| `hourly-distribution` | hourly-distribution | Hourly heatmap |

## Sector-Specific Stat Mapping

Backend returns KPIs based on sector. Map them to your stats:

### Medical Sector
```javascript
{
  todayPatients: pulse.value?.todayClients || 0,
  activeAppointments: pulse.value?.pendingAppointments || 0,
  weeklyRevenue: kpis.value[2]?.value || 0,
  emergencies: kpis.value[3]?.value || 0
}
```

### Legal Sector
```javascript
{
  activeCases: kpis.value[0]?.value || 0,
  todayMeetings: pulse.value?.todayClients || 0,
  pendingDocuments: kpis.value[2]?.value || 0,
  monthlyRevenue: kpis.value[3]?.value || 0
}
```

### E-commerce Sector
```javascript
{
  todayOrders: pulse.value?.todayClients || 0,
  activeOrders: pulse.value?.pendingAppointments || 0,
  revenue: kpis.value[2]?.value || 0,
  conversionRate: pulse.value?.conversionRate || 0
}
```

*Adjust mapping based on what KPIs your backend returns for each sector.*

## Common Issues & Solutions

### Issue 1: "Cannot read property 'value' of undefined"

**Solution**: Add null checks:
```javascript
const stats = computed(() => {
  if (!kpis.value || kpis.value.length === 0) {
    return defaultStats
  }
  return { /* mapped stats */ }
})
```

### Issue 2: Chart doesn't display

**Solution**: Ensure data format matches Chart.js:
```javascript
// Correct format
{
  labels: ['Mon', 'Tue', 'Wed'],
  datasets: [{
    label: 'Metric',
    data: [10, 20, 30]
  }]
}
```

### Issue 3: Skeleton loader shows forever

**Solution**: Check loading state logic:
```vue
<SkeletonChart v-if="chartLoading || !chartData" />
<InteractiveChart v-else :data="chartData" />
```

### Issue 4: WebSocket not connecting

**Solution**: Check tenant_id in localStorage:
```javascript
console.log(localStorage.getItem('tenant_id'))
```

### Issue 5: API returns 401 Unauthorized

**Solution**: Check token in localStorage:
```javascript
console.log(localStorage.getItem('access_token'))
```

The axios interceptor should automatically add it.

## Testing Checklist per Dashboard

For each dashboard you integrate:

- [ ] Imports added correctly
- [ ] `useDashboardData()` called
- [ ] Stats computed from KPIs
- [ ] Chart data fetched in onMounted
- [ ] ErrorState shows when backend is down
- [ ] SkeletonLoader shows during fetch
- [ ] Real data displays when loaded
- [ ] Stats cards clickable with ripple effect
- [ ] Charts animate on load
- [ ] No console errors
- [ ] WebSocket connects (check DevTools)
- [ ] Real-time updates work (if backend emits)

## Quick Copy-Paste Template

```vue
<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
// ... existing icon imports ...
import DashboardLayout from '../../components/dashboard/DashboardLayout.vue'
import StatCard from '../../components/dashboard/StatCard.vue'
import InteractiveChart from '../../components/dashboard/InteractiveChart.vue'
import SkeletonStatCard from '../../components/common/SkeletonStatCard.vue'
import SkeletonChart from '../../components/common/SkeletonChart.vue'
import ErrorState from '../../components/common/ErrorState.vue'
import { useSectorTheme } from '../../composables/useSectorTheme'
import { useDashboardData } from '../../composables/useDashboardData'
import { useAnalyticsStore } from '../../stores/analytics'
import { vRipple } from '../../composables/useRipple'

const router = useRouter()
const { theme } = useSectorTheme('YOUR_SECTOR')
const analyticsStore = useAnalyticsStore()

// Fetch dashboard data
const { kpis, pulse, isLoading, hasError, retry } = useDashboardData({
  enableWebSocket: true
})

// Transform KPIs to stats
const stats = computed(() => {
  if (!kpis.value || kpis.value.length === 0) {
    return { /* defaults */ }
  }
  return {
    stat1: pulse.value?.todayClients || 0,
    stat2: pulse.value?.pendingAppointments || 0,
    // ... map other stats
  }
})

// Chart data
const chartData = ref(null)
const chartLoading = ref(false)

const fetchChartData = async () => {
  chartLoading.value = true
  try {
    const endDate = new Date().toISOString()
    const startDate = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString()
    const response = await analyticsStore.fetchChart('unique-person-count', startDate, endDate)
    chartData.value = response
  } catch (error) {
    console.error('Chart load failed:', error)
  } finally {
    chartLoading.value = false
  }
}

onMounted(() => {
  fetchChartData()
})

// ... rest of your dashboard code ...
</script>

<template>
  <DashboardLayout sector="YOUR_SECTOR" :sector-icon="YourIcon">
    <ErrorState v-if="hasError && !isLoading" @action="retry" />
    
    <template v-else-if="isLoading && !kpis">
      <section class="stats-grid">
        <SkeletonStatCard v-for="i in 4" :key="i" />
      </section>
    </template>
    
    <template v-else>
      <!-- Your existing dashboard content here -->
    </template>
  </DashboardLayout>
</template>
```

## Backend Requirements

Ensure your backend is running:

```bash
# Start backend (from backend directory)
uvicorn app.main:app --reload --port 8001

# Verify analytics endpoints
curl http://localhost:8001/api/v1/analytics/pulse
curl http://localhost:8001/api/v1/analytics/kpis

# Verify WebSocket
# Open browser DevTools -> Network -> WS tab
```

## Summary

All infrastructure is ready. Each dashboard can now:
1. Fetch real data from 14 analytics endpoints
2. Cache data for 5 minutes
3. Show loading skeletons during fetch
4. Show error states with retry
5. Receive real-time WebSocket updates
6. Perform optimistic UI updates
7. Display live connection status

Apply the pattern above to each dashboard for full Phase 4 integration!
