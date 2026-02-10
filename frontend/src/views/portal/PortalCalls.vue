<template>
  <div class="portal-page">
    <div class="page-header">
      <h1 :style="{ color: colors.primary }">Aramalar</h1>
      <p class="subtitle">Çağrı geçmişi ve detayları</p>
    </div>

    <div class="content-card">
      <div v-if="loading" class="loading-state">
        Yükleniyor...
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
                    <span class="item-title">{{ call.caller_number || 'Bilinmiyor' }}</span>
                    <span class="item-date">{{ formatTime(call.created_at) }}</span>
                </div>
                <p class="item-desc">
                    <span class="status-badge" :style="{ background: call.status === 'missed' ? '#fee2e2' : '#dcfce7', color: call.status === 'missed' ? '#991b1b' : '#166534' }">
                        {{ call.status === 'missed' ? 'Cevapsız' : 'Tamamlandı' }}
                    </span>
                    {{ call.duration ? ` • ${call.duration} sn` : '' }}
                </p>
            </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, inject } from 'vue'
import { useSectorStore } from '../../stores/sector'

const sectorStore = useSectorStore()
const axios = inject('axios')

const calls = ref([])
const loading = ref(true)

const colors = computed(() => sectorStore.theme || {
    primary: '#0ea5e9',
    secondary: '#0f766e',
    accent: '#38bdf8',
    text: '#0f172a'
})

const getColor = (name) => (sectorStore.theme || {})[name] || colors.value.primary
const getGlowColor = (name) => getColor(name) + '1A'

const formatTime = (d) => {
    if (!d) return ''
    return new Date(d).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit' })
}

onMounted(async () => {
    try {
        const res = await axios.get('/portal/calls?limit=50')
        calls.value = res.data || []
    } catch (e) {
        console.error('Failed to load calls', e)
    } finally {
        loading.value = false
    }
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
    display: flex;
    align-items: center;
    gap: 8px;
}

.status-badge {
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
}
</style>
