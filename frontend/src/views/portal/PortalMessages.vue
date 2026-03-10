<template>
  <div class="portal-page">
    <div class="page-header">
      <h1 :style="{ color: colors.primary }">{{ t('messages_title') }}</h1>
      <p class="subtitle">{{ t('messages_subtitle') }} <span v-if="totalMessages > 0" class="msg-count">({{ totalMessages }} {{ t('messages_title').toLowerCase() }})</span></p>
    </div>

    <div class="content-card">
      <div v-if="loading" class="loading-state">
        <div class="spinner" :style="{ borderTopColor: colors.primary }"></div>
        <span>{{ t('loading_messages') }}</span>
      </div>
      
      <div v-else-if="errorMsg" class="empty-state">
        <component :is="sectorStore.getIcon('AlertCircle')" :size="48" color="#ef4444" />
        <p>{{ errorMsg }}</p>
        <button class="retry-btn" :style="{ borderColor: colors.primary, color: colors.primary }" @click="loadMessages">{{ t('retry') }}</button>
      </div>

      <div v-else-if="messages.length === 0" class="empty-state">
        <component :is="sectorStore.getIcon('MessageSquare')" :size="48" :color="colors.primary" />
        <p>{{ t('no_messages') }}</p>
      </div>

      <div v-else class="list-container">
        <div 
            v-for="message in messages" 
            :key="message.id" 
            class="list-item"
            :style="{ borderLeft: `4px solid ${colors.primary}` }"
        >
            <div class="item-icon" :style="{ background: getGlowColor('primary'), color: colors.primary }">
                <component :is="sectorStore.getIcon('MessageSquare')" :size="20" />
            </div>
            <div class="item-content">
                <div class="item-header">
                    <span class="item-title">{{ cleanName(message.customer_name) }}</span>
                    <span class="item-badge" :class="message.status">{{ statusLabel(message.status) }}</span>
                    <span class="item-date">{{ formatTime(message.created_at) }}</span>
                </div>
                <p class="item-desc">{{ message.message }}</p>
                <span v-if="message.channel" class="item-channel">{{ message.channel }}</span>
            </div>
        </div>

        <!-- Pagination -->
        <div v-if="totalMessages > pageSize" class="pagination">
          <button :disabled="currentPage <= 1" @click="goToPage(currentPage - 1)" class="page-btn" :style="{ '--page-accent': colors.primary }">← {{ t('previous') }}</button>
          <span class="page-info" :style="{ color: colors.primary }">{{ t('page') }} {{ currentPage }} / {{ totalPages }}</span>
          <button :disabled="currentPage >= totalPages" @click="goToPage(currentPage + 1)" class="page-btn" :style="{ '--page-accent': colors.primary }">{{ t('next') }} →</button>
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

const t = (key) => sectorStore.t(key)

const messages = ref([])
const loading = ref(true)
const errorMsg = ref(null)
const currentPage = ref(1)
const totalMessages = ref(0)
const pageSize = 10
const isFetching = ref(false)  // Prevent concurrent fetch spam
let destroyed = false           // Prevent state updates after unmount

const totalPages = computed(() => Math.ceil(totalMessages.value / pageSize))

const colors = computed(() => sectorStore.theme || {
    primary: '#0ea5e9',
    secondary: '#0f766e',
    text: '#e2e8f0'
})

const getColor = (name) => (sectorStore.theme || {})[name] || colors.value.primary
const getGlowColor = (name) => getColor(name) + '1A'

// Filter out 'Sistem' and similar system names
const cleanName = (name) => {
    if (!name) return t('customer_fallback')
    const lower = name.trim().toLowerCase()
    if (['sistem', 'system', 'admin', 'test', ''].includes(lower)) return t('customer_fallback')
    return name.trim()
}

const statusLabel = (status) => {
    const labels = { 
        read: t('status_read'), 
        unread: t('status_unread'), 
        replied: t('status_replied') 
    }
    return labels[status] || status
}

const formatTime = (d) => {
    if (!d) return ''
    const locale = sectorStore.currentLocale === 'tr' ? 'tr-TR' : (sectorStore.currentLocale === 'de' ? 'de-DE' : 'en-US')
    return new Date(d).toLocaleDateString(locale, { day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit' })
}

const loadMessages = async () => {
    if (isFetching.value || destroyed) return  // guard against spam & stale updates
    isFetching.value = true
    try {
        loading.value = true
        errorMsg.value = null
        // ✅ Correct endpoint: /portal/messages (not /messages)
        const res = await axios.get(`/portal/messages?limit=${pageSize}&page=${currentPage.value}`)
        if (destroyed) return   // component was unmounted while awaiting
        
        // Handle paginated response from backend
        if (res.data && res.data.data) {
            messages.value = res.data.data
            totalMessages.value = res.data.pagination?.total ?? res.data.data.length
        } else if (Array.isArray(res.data)) {
            messages.value = res.data
            totalMessages.value = res.data.length
        } else {
            messages.value = []
            totalMessages.value = 0
        }
    } catch (e) {
        if (!destroyed) {
            console.error('Failed to load messages', e)
            errorMsg.value = 'Mesajlar yüklenirken bir hata oluştu.'
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
    loadMessages()
}

onMounted(() => { loadMessages() })
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

.msg-count {
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
    justify-content: space-between;
    margin-bottom: 4px;
}

.item-title {
    font-weight: 600;
    color: var(--text-primary);
}

.item-date {
    font-size: 12px;
    color: var(--text-muted);
}

.item-desc {
    font-size: 14px;
    color: var(--text-secondary);
    line-height: 1.5;
}

.item-badge {
    font-size: 10px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 4px;
    text-transform: uppercase;
}
.item-badge.unread { background: rgba(59, 130, 246, 0.25); color: #93bbfd; font-weight: 700; box-shadow: 0 0 8px rgba(59, 130, 246, 0.3); }
.item-badge.read { background: rgba(16, 185, 129, 0.15); color: #34d399; }
.item-badge.replied { background: rgba(168, 85, 247, 0.2); color: #c084fc; }

.item-channel {
    font-size: 11px;
    color: var(--text-muted);
    text-transform: capitalize;
    margin-top: 4px;
    display: inline-block;
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
