<template>
  <div class="portal-page">
    <div class="page-header">
      <h1>Aramalar</h1>
      <p class="subtitle">Çağrı geçmişi ve detayları</p>
    </div>

    <div class="content-card">
      <div v-if="loading" class="loading-state">
        Yükleniyor...
      </div>
      
      <div v-else-if="errorMsg" class="empty-state">
        <component :is="sectorStore.getIcon('AlertCircle')" :size="48" color="#ef4444" />
        <p>{{ errorMsg }}</p>
        <button class="retry-btn" @click="loadCalls">Tekrar Dene</button>
      </div>

      <div v-else-if="calls.length === 0" class="empty-state">
        <component :is="sectorStore.getIcon('Phone')" :size="48" :color="colors.secondary" />
        <p>Henüz bir arama kaydı bulunmuyor.</p>
      </div>

      <div v-else class="list-container">
        <div 
            v-for="call in calls" 
            :key="call.id" 
            class="list-item"
            :style="{ borderLeft: `4px solid ${colors.accent}` }"
        >
            <div class="item-icon" :style="{ background: getGlowColor('accent'), color: colors.accent }">
                <component :is="sectorStore.getIcon('Phone')" :size="20" />
            </div>
            <div class="item-content">
                <div class="item-header">
                    <span class="item-title">{{ call.customer_name || 'Müşteri' }}</span>
                    <span class="item-phone" v-if="call.phone">{{ call.phone }}</span>
                    <span class="item-date">{{ formatTime(call.timestamp || call.created_at) }}</span>
                </div>
                <p class="item-desc">
                    <span class="status-badge" :class="statusClass(call.status)">
                        {{ statusLabel(call.status) }}
                    </span>
                    <span v-if="call.duration" class="call-duration">{{ call.duration }}</span>
                    <span v-if="call.agent" class="call-agent">{{ call.agent }}</span>
                </p>
                <p v-if="call.summary" class="item-summary">{{ call.summary }}</p>
            </div>
        </div>

        <!-- Pagination -->
        <div v-if="totalCalls > pageSize" class="pagination">
          <button :disabled="currentPage <= 1" @click="goToPage(currentPage - 1)" class="page-btn">← Önceki</button>
          <span class="page-info">Sayfa {{ currentPage }} / {{ totalPages }}</span>
          <button :disabled="currentPage >= totalPages" @click="goToPage(currentPage + 1)" class="page-btn">Sonraki →</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, inject } from 'vue'
import { useSectorStore } from '../../stores/sector'
import { useAuthStore } from '../../stores/auth'

const sectorStore = useSectorStore()
const authStore = useAuthStore()
const axios = inject('axios')

const calls = ref([])
const loading = ref(true)
const errorMsg = ref(null)
const currentPage = ref(1)
const totalCalls = ref(0)
const pageSize = 10

const totalPages = computed(() => Math.ceil(totalCalls.value / pageSize))

const colors = computed(() => sectorStore.theme || {
    primary: '#0ea5e9',
    secondary: '#0f766e',
    accent: '#38bdf8',
    text: '#e2e8f0'
})

const getColor = (name) => (sectorStore.theme || {})[name] || colors.value.primary
const getGlowColor = (name) => getColor(name) + '1A'

const statusLabel = (status) => {
    const labels = {
        resolved: 'Çözüldü',
        closed: 'Kapatıldı',
        pending: 'Beklemede',
        missed: 'Cevapsız',
        completed: 'Tamamlandı',
        open: 'Açık'
    }
    return labels[status] || status || 'Tamamlandı'
}

const statusClass = (status) => {
    if (['resolved', 'closed', 'completed'].includes(status)) return 'success'
    if (['missed', 'open'].includes(status)) return 'danger'
    return 'warning'
}

const formatTime = (d) => {
    if (!d) return ''
    return new Date(d).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit' })
}

const loadCalls = async () => {
    // Guard against concurrent fetches
    if (loading.value && calls.value.length > 0) return
    try {
        loading.value = true
        errorMsg.value = null
        const tenant = sectorStore.currentSectorId || 'beauty'
        const res = await axios.get(`/calls?tenant=${tenant}&limit=${pageSize}&page=${currentPage.value}`)
        
        // Handle paginated response from backend
        if (res.data && res.data.data) {
            calls.value = res.data.data
            totalCalls.value = res.data.pagination?.total || res.data.total || res.data.data.length
        } else if (Array.isArray(res.data)) {
            calls.value = res.data
            totalCalls.value = res.data.length
        } else {
            calls.value = []
            totalCalls.value = 0
        }
    } catch (e) {
        console.error('Failed to load calls', e)
        errorMsg.value = 'Aramalar yüklenirken bir hata oluştu.'
    } finally {
        loading.value = false
    }
}

const goToPage = (page) => {
    currentPage.value = page
    loadCalls()
}

onMounted(() => {
    loadCalls()
})
</script>

<style scoped>
.portal-page {
    width: 100%;
    margin: 0;
    padding: 24px;
}

.page-header {
    margin-bottom: 32px;
}

.page-header h1 {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 4px;
    color: var(--text-primary);
}

.subtitle {
    color: var(--text-secondary);
    font-size: 14px;
}

.content-card {
    background: var(--surface-elevated);
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
}

.loading-state, .empty-state {
    text-align: center;
    padding: 48px;
    color: var(--text-secondary);
}

.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
}

.list-container {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.list-item {
    display: flex;
    gap: 16px;
    padding: 16px;
    background: var(--surface-hover);
    border-radius: 8px;
    transition: transform 0.2s;
}

.list-item:hover {
    transform: translateX(4px);
    background: var(--surface-elevated);
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.item-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.item-content {
    flex: 1;
}

.item-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 4px;
}

.item-title {
    font-weight: 600;
    color: var(--text-primary);
}

.item-phone {
    font-size: 12px;
    color: var(--text-muted);
    font-family: monospace;
}

.item-date {
    font-size: 12px;
    color: var(--text-muted);
    margin-left: auto;
}

.item-desc {
    font-size: 14px;
    color: var(--text-secondary);
    line-height: 1.5;
    display: flex;
    align-items: center;
    gap: 8px;
}

.item-summary {
    font-size: 13px;
    color: var(--text-muted);
    margin-top: 4px;
}

.status-badge {
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
}
.status-badge.success { background: rgba(16, 185, 129, 0.15); color: #34d399; }
.status-badge.danger { background: rgba(239, 68, 68, 0.15); color: #f87171; }
.status-badge.warning { background: rgba(245, 158, 11, 0.15); color: #fbbf24; }

.call-duration {
    font-size: 12px;
    color: var(--text-secondary);
}

.call-agent {
    font-size: 12px;
    color: var(--text-muted);
}

.pagination {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    margin-top: 24px;
    padding-top: 16px;
    border-top: 1px solid var(--border-subtle);
}

.page-btn {
    padding: 8px 16px;
    background: var(--surface-elevated);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    color: var(--text-primary);
    cursor: pointer;
    transition: all 0.2s;
    font-size: 13px;
}
.page-btn:hover:not(:disabled) {
    background: var(--surface-hover);
    border-color: var(--border-hover);
}
.page-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

.page-info {
    font-size: 13px;
    color: var(--text-secondary);
}

.retry-btn {
    padding: 8px 20px;
    background: var(--surface-elevated);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    color: var(--text-primary);
    cursor: pointer;
    transition: all 0.2s;
}
.retry-btn:hover {
    background: var(--surface-hover);
}
</style>
