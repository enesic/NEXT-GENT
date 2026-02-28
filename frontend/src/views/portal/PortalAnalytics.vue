<template>
  <div class="portal-page">
    <div class="page-header">
      <h1 :style="{ color: colors.primary }">Performans Analizi</h1>
      <p class="subtitle">Detaylı istatistik ve raporlar</p>
    </div>

    <div class="content-card">
       <div class="analytics-grid">
            <div class="chart-container large">
                <h3>Aylık Performans</h3>
                <LuxuryChart 
                    type="area" 
                    :series="[{ name: 'Etkileşim', data: [30, 40, 45, 50, 49, 60, 70, 91] }]" 
                    :categories="['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz', 'Tem', 'Ağu']" 
                    height="300"
                    :color="colors.primary"
                />
            </div>
            
            <div class="chart-container">
                 <h3>Dağılım</h3>
                 <LuxuryChart 
                    type="donut" 
                    :series="[44, 55, 41, 17]" 
                    :labels="['Randevu', 'Bilgi', 'Şikayet', 'Diğer']" 
                    height="300" 
                    :color="colors.primary"
                />
            </div>

            <div class="chart-container">
                 <h3>Dönüşüm</h3>
                 <LuxuryChart 
                    type="bar" 
                    :series="[{ name: 'Oran', data: [20, 30, 40, 80, 20, 80] }]" 
                    :categories="['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt']" 
                    height="300"
                    :color="colors.accent"
                />
            </div>
       </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useSectorStore } from '../../stores/sector'
import LuxuryChart from '../../components/LuxuryChart.vue'

const sectorStore = useSectorStore()

const colors = computed(() => sectorStore.theme || {
    primary: '#0ea5e9',
    secondary: '#0f766e',
    text: '#0f172a'
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

.analytics-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
}

.chart-container {
    padding: 16px;
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
}

.chart-container h3 {
    margin-bottom: 16px;
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
}

.chart-container.large {
    grid-column: span 2;
}

@media (max-width: 768px) {
    .analytics-grid {
        grid-template-columns: 1fr;
    }
    .chart-container.large {
        grid-column: span 1;
    }
}
</style>
