<template>
  <div class="portal-page">
    <div class="page-header">
      <h1 :style="{ color: colors.primary }">Memnuniyet</h1>
      <p class="subtitle">Geri bildirimleriniz bizim için değerli</p>
    </div>

    <div class="content-card">
       <div class="satisfaction-content">
            <div class="score-card" :style="{ background: getGlowColor('primary') }">
                <h3>Genel Memnuniyet</h3>
                <div class="score" :style="{ color: colors.primary }">4.8/5.0</div>
                <div class="stars">
                    <component :is="sectorStore.getIcon('Star')" v-for="i in 5" :key="i" :size="20" :fill="i <= 4 ? colors.primary : 'none'" :color="colors.primary" />
                </div>
            </div>

            <div class="feedback-list">
                 <h3>Son Geri Bildirimleriniz</h3>
                 <div v-for="i in 3" :key="i" class="feedback-item">
                    <div class="feedback-icon" :style="{ background: colors.background }">
                        <component :is="sectorStore.getIcon('MessageCircle')" :size="18" :color="colors.text" />
                    </div>
                    <div class="feedback-text">
                        <strong>Hizmet Kalitesi</strong>
                        <p>"Çok hızlı ve ilgili bir hizmet aldım, teşekkürler."</p>
                    </div>
                    <span class="feedback-date">2 gün önce</span>
                 </div>
            </div>

            <button class="action-btn-primary" :style="{ background: colors.primary }">
                Yeni Geri Bildirim Gönder
            </button>
       </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useSectorStore } from '../../stores/sector'

const sectorStore = useSectorStore()

const colors = computed(() => sectorStore.theme || {
    primary: '#0ea5e9',
    secondary: '#0f766e',
    text: '#0f172a',
    background: '#f0f9ff'
})

const getColor = (name) => (sectorStore.theme || {})[name] || colors.value.primary
const getGlowColor = (name) => getColor(name) + '1A'
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
    padding: 32px;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
}

.satisfaction-content {
    display: flex;
    flex-direction: column;
    gap: 32px;
    align-items: center;
}

.score-card {
    padding: 32px;
    border-radius: 16px;
    text-align: center;
    width: 100%;
    max-width: 400px;
}

.score-card h3 {
    margin-bottom: 16px;
    font-weight: 600;
    color: var(--text-primary);
}

.score {
    font-size: 48px;
    font-weight: 800;
    margin-bottom: 16px;
}

.stars {
    display: flex;
    justify-content: center;
    gap: 8px;
}

.feedback-list {
    width: 100%;
}

.feedback-list h3 {
    margin-bottom: 16px;
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
}

.feedback-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px;
    border-bottom: 1px solid var(--border-subtle);
}

.feedback-icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.feedback-text {
    flex: 1;
}

.feedback-text strong {
    display: block;
    font-size: 14px;
    color: var(--text-primary);
}

.feedback-text p {
    font-size: 13px;
    color: var(--text-secondary);
    margin-top: 4px;
}

.feedback-date {
    font-size: 12px;
    color: var(--text-muted);
}

.action-btn-primary {
    padding: 12px 24px;
    border-radius: 8px;
    color: white;
    font-weight: 600;
    border: none;
    cursor: pointer;
    transition: opacity 0.2s;
}

.action-btn-primary:hover {
    opacity: 0.9;
}
</style>
