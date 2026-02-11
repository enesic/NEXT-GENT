import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAnalyticsStore } from '@/stores/analytics'

// Mock analytics service
vi.mock('@/services/analytics.service', () => ({
  analyticsService: {
    getPulse: vi.fn(() => Promise.resolve({ data: { active_calls: 10, queue_size: 5 } })),
    getStats: vi.fn(() => Promise.resolve({ data: { total_calls: 100 } })),
    getKPIs: vi.fn(() => Promise.resolve({ data: [{ label: 'KPI1', value: 100 }] })),
    getInsights: vi.fn(() => Promise.resolve({ data: [] })),
    getSatisfaction: vi.fn(() => Promise.resolve({ data: { score: 4.5 } }))
  }
}))

// Mock IndexedDB
vi.mock('@/utils/indexedDB', () => ({
  indexedDBCache: {
    get: vi.fn(() => Promise.resolve(null)),
    set: vi.fn(() => Promise.resolve()),
    delete: vi.fn(() => Promise.resolve()),
    keys: vi.fn(() => Promise.resolve([]))
  }
}))

describe('Analytics Store', () => {
  let store

  beforeEach(() => {
    setActivePinia(createPinia())
    store = useAnalyticsStore()
  })

  it('should initialize with empty state', () => {
    expect(store.pulse).toBeNull()
    expect(store.stats).toBeNull()
    expect(store.kpis).toEqual([])
    expect(store.insights).toEqual([])
  })

  it('should fetch pulse data', async () => {
    await store.fetchPulse()

    expect(store.pulse).toBeDefined()
    expect(store.pulse.active_calls).toBe(10)
    expect(store.pulse.queue_size).toBe(5)
  })

  it('should fetch KPIs data', async () => {
    await store.fetchKPIs()

    expect(store.kpis).toHaveLength(1)
    expect(store.kpis[0].label).toBe('KPI1')
  })

  it('should track loading state during fetch', async () => {
    const promise = store.fetchPulse()
    expect(store.loading.pulse).toBe(true)

    await promise
    expect(store.loading.pulse).toBe(false)
  })

  it('should check if pulse is stale', () => {
    expect(store.isPulseStale).toBe(true)
    
    store.lastFetch.pulse = Date.now()
    expect(store.isPulseStale).toBe(false)
  })

  it('should check if KPIs are stale', () => {
    expect(store.isKPIsStale).toBe(true)
    
    store.lastFetch.kpis = Date.now()
    expect(store.isKPIsStale).toBe(false)
  })

  it('should clear all cache', async () => {
    store.pulse = { active_calls: 10 }
    store.kpis = [{ label: 'KPI1' }]

    await store.clearCache()

    expect(store.pulse).toBeNull()
    expect(store.kpis).toEqual([])
  })
})
