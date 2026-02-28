<template>
  <div class="portal-page">
    <div class="page-header">
      <h1 :style="{ color: colors.primary }">Aramalar</h1>
      <p class="subtitle">Çağrı geçmişi ve detayları <span v-if="totalCalls > 0" class="call-count">({{ totalCalls }} arama)</span></p>
    </div>

    <div class="content-card">
      <div v-if="loading" class="loading-state">
        <div class="spinner" :style="{ borderTopColor: colors.primary }"></div>
        <span>Aramalar yükleniyor...</span>
      </div>
      
      <div v-else-if="errorMsg" class="empty-state">
        <component :is="sectorStore.getIcon('AlertCircle')" :size="48" color="#ef4444" />
        <p>{{ errorMsg }}</p>
        <button class="retry-btn" :style="{ borderColor: colors.primary, color: colors.primary }" @click="loadCalls">Tekrar Dene</button>
      </div>

      <div v-else-if="calls.length === 0" class="empty-state">
        <component :is="sectorStore.getIcon('Phone')" :size="48" :color="colors.primary" />
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
                    <span class="item-title">{{ cleanName(call.customer_name) }}</span>
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
          <button :disabled="currentPage <= 1" @click="goToPage(currentPage - 1)" class="page-btn" :style="{ '--page-accent': colors.primary }">← Önceki</button>
          <span class="page-info" :style="{ color: colors.primary }">Sayfa {{ currentPage }} / {{ totalPages }}</span>
          <button :disabled="currentPage >= totalPages" @click="goToPage(currentPage + 1)" class="page-btn" :style="{ '--page-accent': colors.primary }">Sonraki →</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, inject } from 'vue'
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
const isFetching = ref(false)  // Prevent concurrent fetch spam
let destroyed = false           // Prevent state updates after unmount

const totalPages = computed(() => Math.ceil(totalCalls.value / pageSize))

const colors = computed(() => sectorStore.theme || {
    primary: '#0ea5e9',
    secondary: '#0f766e',
    accent: '#38bdf8',
    text: '#e2e8f0'
})

const getColor = (name) => (sectorStore.theme || {})[name] || colors.value.primary
const getGlowColor = (name) => getColor(name) + '1A'

// Filter out 'Sistem' and similar system names
const cleanName = (name) => {
    if (!name) return 'Müşteri'
    const lower = name.trim().toLowerCase()
    if (['sistem', 'system', 'admin', 'test', ''].includes(lower)) return 'Müşteri'
    return name.trim()
}

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
    if (isFetching.value || destroyed) return  // guard against spam & stale updates
    isFetching.value = true
    try {
        loading.value = true
        errorMsg.value = null
        // ✅ Correct endpoint: /portal/calls (not /calls)
        const res = await axios.get(`/portal/calls?limit=${pageSize}&page=${currentPage.value}`)
        if (destroyed) return   // component was unmounted while awaiting

        if (res.data && res.data.data) {
            calls.value = res.data.data
            totalCalls.value = res.data.pagination?.total ?? res.data.data.length
        } else if (Array.isArray(res.data)) {
            calls.value = res.data
            totalCalls.value = res.data.length
        } else {
            calls.value = []
            totalCalls.value = 0
        }
    } catch (e) {
        if (!destroyed) {
            console.error('Failed to load calls', e)
            errorMsg.value = 'Aramalar yüklenirken bir hata oluştu.'
        }
    } finally {
        if (!destroyed) {
            loading.value = false
            isFetching.value = false
        }
    }
}

const goToPage = (page) => {
    if (page < 1 || page > totalPages.value) return
    currentPage.value = page
    loadCalls()
}

onMounted(() => { loadCalls() })
onUnmounted(() => { destroyed = true; isFetching.value = false })
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

.call-count {
    color: var(--text-muted);
    font-weight: 400;
    font-size: 13px;
}

.loading-state, .empty-state {
    text-align: center;
    padding: 48px;
    color: var(--text-secondary);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
}

.spinner {
    width: 36px;
    height: 36px;
    border: 3px solid var(--border-subtle);
    border-top-color: var(--text-primary); /* overridden by inline :style */
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.empty-state {
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
.status-badge.success { background: rgba(16, 185, 129, 0.2); color: #34d399; }
.status-badge.danger { background: rgba(239, 68, 68, 0.2); color: #f87171; font-weight: 700; box-shadow: 0 0 6px rgba(239, 68, 68, 0.25); }
.status-badge.warning { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }

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
    border-color: var(--page-accent, var(--border-hover));
    color: var(--page-accent, var(--text-primary));
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
    background: transparent;
    border: 1px solid;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s;
}
.retry-btn:hover {
    opacity: 0.8;
    transform: translateY(-1px);
}
</style>
