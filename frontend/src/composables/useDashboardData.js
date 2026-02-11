import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useAnalyticsStore } from '../stores/analytics'
import { useWebSocket } from './useWebSocket'

/**
 * Dashboard Data Composable
 * Reusable composable for fetching dashboard data with WebSocket support
 * 
 * @param {Object} options - Configuration options
 * @param {Boolean} options.autoFetch - Auto-fetch data on mount (default: true)
 * @param {Boolean} options.fetchPulse - Fetch pulse data (default: true)
 * @param {Boolean} options.fetchStats - Fetch stats data (default: true)
 * @param {Boolean} options.fetchKPIs - Fetch KPIs (default: true)
 * @param {Boolean} options.fetchInsights - Fetch insights (default: true)
 * @param {Boolean} options.fetchSatisfaction - Fetch satisfaction metrics (default: false)
 * @param {Boolean} options.enableWebSocket - Enable WebSocket updates (default: true)
 * @returns {Object} Dashboard data and methods
 */
export function useDashboardData(options = {}) {
  const {
    autoFetch = true,
    fetchPulse = true,
    fetchStats = true,
    fetchKPIs = true,
    fetchInsights = true,
    fetchSatisfaction = false,
    enableWebSocket = true
  } = options
  
  const analyticsStore = useAnalyticsStore()
  const ws = enableWebSocket ? useWebSocket() : null
  
  // WebSocket event handlers
  const wsHandlers = []
  
  // Computed properties
  const isLoading = computed(() => {
    return analyticsStore.loading.pulse || 
           analyticsStore.loading.stats ||
           analyticsStore.loading.kpis ||
           analyticsStore.loading.insights
  })
  
  const hasError = computed(() => {
    return !!(analyticsStore.errors.pulse ||
           analyticsStore.errors.stats ||
           analyticsStore.errors.kpis ||
           analyticsStore.errors.insights)
  })
  
  const firstError = computed(() => {
    return analyticsStore.errors.pulse ||
           analyticsStore.errors.stats ||
           analyticsStore.errors.kpis ||
           analyticsStore.errors.insights ||
           null
  })
  
  // Data computed properties
  const pulse = computed(() => analyticsStore.pulse)
  const stats = computed(() => analyticsStore.stats)
  const kpis = computed(() => analyticsStore.kpis)
  const insights = computed(() => analyticsStore.insights)
  const satisfaction = computed(() => analyticsStore.satisfaction)
  
  /**
   * Fetch all configured data
   */
  const fetchData = async () => {
    const promises = []
    
    if (fetchPulse) {
      promises.push(analyticsStore.fetchPulse().catch(err => {
        console.error('Failed to fetch pulse:', err)
        return null
      }))
    }
    
    if (fetchStats) {
      promises.push(analyticsStore.fetchStats().catch(err => {
        console.error('Failed to fetch stats:', err)
        return null
      }))
    }
    
    if (fetchKPIs) {
      promises.push(analyticsStore.fetchKPIs().catch(err => {
        console.error('Failed to fetch KPIs:', err)
        return null
      }))
    }
    
    if (fetchInsights) {
      promises.push(analyticsStore.fetchInsights().catch(err => {
        console.error('Failed to fetch insights:', err)
        return null
      }))
    }
    
    if (fetchSatisfaction) {
      promises.push(analyticsStore.fetchSatisfaction().catch(err => {
        console.error('Failed to fetch satisfaction:', err)
        return null
      }))
    }
    
    const results = await Promise.allSettled(promises)
    return results
  }
  
  /**
   * Retry fetching data (clears errors first)
   */
  const retry = async () => {
    analyticsStore.clearErrors()
    return await fetchData()
  }
  
  /**
   * Refresh all data (force fetch)
   */
  const refresh = async () => {
    const promises = []
    
    if (fetchPulse) {
      promises.push(analyticsStore.fetchPulse(true).catch(err => null))
    }
    
    if (fetchStats) {
      promises.push(analyticsStore.fetchStats(true).catch(err => null))
    }
    
    if (fetchKPIs) {
      promises.push(analyticsStore.fetchKPIs(true).catch(err => null))
    }
    
    if (fetchInsights) {
      promises.push(analyticsStore.fetchInsights(true).catch(err => null))
    }
    
    if (fetchSatisfaction) {
      promises.push(analyticsStore.fetchSatisfaction(true).catch(err => null))
    }
    
    const results = await Promise.allSettled(promises)
    return results
  }
  
  // Setup WebSocket listeners if enabled
  if (ws) {
    // Pulse updates
    const handlePulseUpdate = (data) => {
      if (data.payload) {
        analyticsStore.pulse = data.payload
      }
    }
    
    // Stats updates
    const handleStatsUpdate = (data) => {
      if (data.payload) {
        analyticsStore.stats = data.payload
      }
    }
    
    // KPI updates
    const handleKPIUpdate = (data) => {
      if (data.payload) {
        analyticsStore.kpis = data.payload
      }
    }
    
    // Insight updates
    const handleInsightUpdate = (data) => {
      if (data.payload) {
        analyticsStore.insights = data.payload
      }
    }
    
    // Store handlers for cleanup
    wsHandlers.push(
      { event: 'pulse_update', handler: handlePulseUpdate },
      { event: 'stats_update', handler: handleStatsUpdate },
      { event: 'kpi_update', handler: handleKPIUpdate },
      { event: 'insight_update', handler: handleInsightUpdate }
    )
  }
  
  // Lifecycle hooks
  onMounted(() => {
    // Register WebSocket handlers
    if (ws && wsHandlers.length > 0) {
      wsHandlers.forEach(({ event, handler }) => {
        ws.on(event, handler)
      })
    }
    
    // Auto-fetch data
    if (autoFetch) {
      fetchData()
    }
  })
  
  onUnmounted(() => {
    // Cleanup WebSocket handlers
    if (ws && wsHandlers.length > 0) {
      wsHandlers.forEach(({ event, handler }) => {
        ws.off(event, handler)
      })
    }
  })
  
  return {
    // Data
    pulse,
    stats,
    kpis,
    insights,
    satisfaction,
    
    // State
    isLoading,
    hasError,
    firstError,
    
    // Methods
    fetchData,
    retry,
    refresh,
    
    // WebSocket
    isConnected: ws ? ws.isConnected : ref(false),
    wsError: ws ? ws.error : ref(null)
  }
}
