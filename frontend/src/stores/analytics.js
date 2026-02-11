import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { analyticsService } from '../services/analytics.service'
import { useNotificationStore } from './notification'
import { indexedDBCache } from '../utils/indexedDB'

export const useAnalyticsStore = defineStore('analytics', () => {
  // State
  const pulse = ref(null)
  const stats = ref(null)
  const kpis = ref([])
  const insights = ref([])
  const satisfaction = ref(null)
  const dashboardSummary = ref(null)
  const quickStats = ref(null)
  const charts = ref({})
  
  // Cache timestamps
  const lastFetch = ref({
    pulse: null,
    stats: null,
    kpis: null,
    insights: null,
    satisfaction: null,
    dashboardSummary: null,
    quickStats: null,
    charts: {}
  })
  
  const CACHE_DURATION = 5 * 60 * 1000 // 5 minutes
  const PERSISTENT_CACHE_DURATION = 30 * 60 * 1000 // 30 minutes for IndexedDB
  
  // Loading states
  const loading = ref({
    pulse: false,
    stats: false,
    kpis: false,
    insights: false,
    satisfaction: false,
    dashboardSummary: false,
    quickStats: false,
    charts: {}
  })
  
  // Error states
  const errors = ref({
    pulse: null,
    stats: null,
    kpis: null,
    insights: null,
    satisfaction: null,
    dashboardSummary: null,
    quickStats: null,
    charts: {}
  })
  
  // Getters
  const isPulseStale = computed(() => {
    return !lastFetch.value.pulse || (Date.now() - lastFetch.value.pulse > CACHE_DURATION)
  })
  
  const isStatsStale = computed(() => {
    return !lastFetch.value.stats || (Date.now() - lastFetch.value.stats > CACHE_DURATION)
  })
  
  const isKPIsStale = computed(() => {
    return !lastFetch.value.kpis || (Date.now() - lastFetch.value.kpis > CACHE_DURATION)
  })
  
  const isInsightsStale = computed(() => {
    return !lastFetch.value.insights || (Date.now() - lastFetch.value.insights > CACHE_DURATION)
  })
  
  const isDataLoading = computed(() => {
    return loading.value.pulse || 
           loading.value.stats || 
           loading.value.kpis || 
           loading.value.insights
  })
  
  const hasErrors = computed(() => {
    return errors.value.pulse ||
           errors.value.stats ||
           errors.value.kpis ||
           errors.value.insights
  })
  
  // Actions
  const fetchPulse = async (force = false) => {
    // Try IndexedDB cache first if not forcing
    if (!force) {
      if (!isPulseStale.value && pulse.value) {
        return pulse.value
      }
      
      // Try persistent cache
      const cached = await indexedDBCache.get('analytics:pulse')
      if (cached) {
        pulse.value = cached
        lastFetch.value.pulse = Date.now()
        // Background refresh if needed
        if (isPulseStale.value) {
          fetchPulse(true).catch(() => {}) // Silent background refresh
        }
        return pulse.value
      }
    }
    
    loading.value.pulse = true
    errors.value.pulse = null
    
    try {
      const response = await analyticsService.getPulse()
      pulse.value = response.data
      lastFetch.value.pulse = Date.now()
      
      // Save to IndexedDB
      await indexedDBCache.set('analytics:pulse', response.data, PERSISTENT_CACHE_DURATION)
      
      return pulse.value
    } catch (error) {
      errors.value.pulse = error
      console.error('Failed to fetch pulse:', error)
      // Don't show notification for pulse errors (too frequent)
      throw error
    } finally {
      loading.value.pulse = false
    }
  }
  
  const fetchStats = async (force = false) => {
    if (!force && !isStatsStale.value && stats.value) {
      return stats.value
    }
    
    loading.value.stats = true
    errors.value.stats = null
    
    try {
      const response = await analyticsService.getStats()
      stats.value = response.data
      lastFetch.value.stats = Date.now()
      return stats.value
    } catch (error) {
      errors.value.stats = error
      console.error('Failed to fetch stats:', error)
      throw error
    } finally {
      loading.value.stats = false
    }
  }
  
  const fetchKPIs = async (force = false) => {
    // Try IndexedDB cache first if not forcing
    if (!force) {
      if (!isKPIsStale.value && kpis.value.length > 0) {
        return kpis.value
      }
      
      // Try persistent cache
      const cached = await indexedDBCache.get('analytics:kpis')
      if (cached) {
        kpis.value = cached
        lastFetch.value.kpis = Date.now()
        // Background refresh if needed
        if (isKPIsStale.value) {
          fetchKPIs(true).catch(() => {}) // Silent background refresh
        }
        return kpis.value
      }
    }
    
    loading.value.kpis = true
    errors.value.kpis = null
    
    try {
      const response = await analyticsService.getKPIs()
      kpis.value = response.data
      lastFetch.value.kpis = Date.now()
      
      // Save to IndexedDB
      await indexedDBCache.set('analytics:kpis', response.data, PERSISTENT_CACHE_DURATION)
      
      return kpis.value
    } catch (error) {
      errors.value.kpis = error
      console.error('Failed to fetch KPIs:', error)
      useNotificationStore().error('Failed to load dashboard metrics')
      throw error
    } finally {
      loading.value.kpis = false
    }
  }
  
  const fetchInsights = async (force = false) => {
    if (!force && !isInsightsStale.value && insights.value.length > 0) {
      return insights.value
    }
    
    loading.value.insights = true
    errors.value.insights = null
    
    try {
      const response = await analyticsService.getInsights()
      insights.value = response.data
      lastFetch.value.insights = Date.now()
      return insights.value
    } catch (error) {
      errors.value.insights = error
      console.error('Failed to fetch insights:', error)
      throw error
    } finally {
      loading.value.insights = false
    }
  }
  
  const fetchSatisfaction = async (force = false) => {
    if (!force && lastFetch.value.satisfaction && 
        (Date.now() - lastFetch.value.satisfaction < CACHE_DURATION) && 
        satisfaction.value) {
      return satisfaction.value
    }
    
    loading.value.satisfaction = true
    errors.value.satisfaction = null
    
    try {
      const response = await analyticsService.getSatisfaction()
      satisfaction.value = response.data
      lastFetch.value.satisfaction = Date.now()
      return satisfaction.value
    } catch (error) {
      errors.value.satisfaction = error
      console.error('Failed to fetch satisfaction:', error)
      throw error
    } finally {
      loading.value.satisfaction = false
    }
  }
  
  const fetchDashboardSummary = async (startDate, endDate, force = false) => {
    const cacheKey = `${startDate}_${endDate}`
    
    if (!force && lastFetch.value.dashboardSummary === cacheKey && dashboardSummary.value) {
      return dashboardSummary.value
    }
    
    loading.value.dashboardSummary = true
    errors.value.dashboardSummary = null
    
    try {
      const response = await analyticsService.getDashboardSummary(startDate, endDate)
      dashboardSummary.value = response.data
      lastFetch.value.dashboardSummary = cacheKey
      return dashboardSummary.value
    } catch (error) {
      errors.value.dashboardSummary = error
      console.error('Failed to fetch dashboard summary:', error)
      throw error
    } finally {
      loading.value.dashboardSummary = false
    }
  }
  
  const fetchQuickStats = async (days = 30, force = false) => {
    const cacheKey = `days_${days}`
    
    if (!force && lastFetch.value.quickStats === cacheKey && quickStats.value) {
      return quickStats.value
    }
    
    loading.value.quickStats = true
    errors.value.quickStats = null
    
    try {
      const response = await analyticsService.getQuickStats(days)
      quickStats.value = response.data
      lastFetch.value.quickStats = cacheKey
      return quickStats.value
    } catch (error) {
      errors.value.quickStats = error
      console.error('Failed to fetch quick stats:', error)
      throw error
    } finally {
      loading.value.quickStats = false
    }
  }
  
  const fetchChart = async (chartType, startDate, endDate, force = false) => {
    const cacheKey = `${chartType}_${startDate}_${endDate}`
    
    if (!force && charts.value[cacheKey] && 
        lastFetch.value.charts[cacheKey] &&
        (Date.now() - lastFetch.value.charts[cacheKey] < CACHE_DURATION)) {
      return charts.value[cacheKey]
    }
    
    if (!loading.value.charts) {
      loading.value.charts = {}
    }
    if (!errors.value.charts) {
      errors.value.charts = {}
    }
    
    loading.value.charts[cacheKey] = true
    errors.value.charts[cacheKey] = null
    
    try {
      const response = await analyticsService.getChartData(chartType, startDate, endDate)
      charts.value[cacheKey] = response.data
      if (!lastFetch.value.charts) {
        lastFetch.value.charts = {}
      }
      lastFetch.value.charts[cacheKey] = Date.now()
      return charts.value[cacheKey]
    } catch (error) {
      errors.value.charts[cacheKey] = error
      console.error(`Failed to fetch chart ${chartType}:`, error)
      throw error
    } finally {
      loading.value.charts[cacheKey] = false
    }
  }
  
  // Cache management
  const clearCache = () => {
    pulse.value = null
    stats.value = null
    kpis.value = []
    insights.value = []
    satisfaction.value = null
    dashboardSummary.value = null
    quickStats.value = null
    charts.value = {}
    lastFetch.value = {
      pulse: null,
      stats: null,
      kpis: null,
      insights: null,
      satisfaction: null,
      dashboardSummary: null,
      quickStats: null,
      charts: {}
    }
    errors.value = {
      pulse: null,
      stats: null,
      kpis: null,
      insights: null,
      satisfaction: null,
      dashboardSummary: null,
      quickStats: null,
      charts: {}
    }
  }
  
  const refreshAll = async () => {
    const results = await Promise.allSettled([
      fetchPulse(true),
      fetchStats(true),
      fetchKPIs(true),
      fetchInsights(true),
      fetchSatisfaction(true)
    ])
    
    return results
  }
  
  const clearErrors = () => {
    errors.value = {
      pulse: null,
      stats: null,
      kpis: null,
      insights: null,
      satisfaction: null,
      dashboardSummary: null,
      quickStats: null,
      charts: {}
    }
  }
  
  return {
    // State
    pulse,
    stats,
    kpis,
    insights,
    satisfaction,
    dashboardSummary,
    quickStats,
    charts,
    loading,
    errors,
    
    // Getters
    isPulseStale,
    isStatsStale,
    isKPIsStale,
    isInsightsStale,
    isDataLoading,
    hasErrors,
    
    // Actions
    fetchPulse,
    fetchStats,
    fetchKPIs,
    fetchInsights,
    fetchSatisfaction,
    fetchDashboardSummary,
    fetchQuickStats,
    fetchChart,
    clearCache,
    refreshAll,
    clearErrors
  }
})
