<template>
  <div class="portal-page">
    <div class="page-header">
      <h1 :style="{ color: colors.primary }">{{ pageTitle }}</h1>
      <p class="subtitle">{{ pageSubtitle }}</p>
    </div>

    <!-- Generic List Layout for "Sector Specific" Items -->
    <div class="content-card">
         <div v-if="items.length === 0" class="empty-state">
            <component :is="sectorStore.getIcon(pageIcon)" :size="48" :color="colors.secondary" />
            <p>Henüz kayıt bulunamadı.</p>
         </div>

         <div v-else class="generic-list">
            <div v-for="(item, i) in items" :key="i" class="list-row">
                 <div class="row-icon" :style="{ background: getGlowColor('primary'), color: colors.primary }">
                    <component :is="sectorStore.getIcon(pageIcon)" :size="20" />
                 </div>
                 <div class="row-content">
                    <strong>{{ item.title }}</strong>
                    <span>{{ item.desc }}</span>
                 </div>
                 <div class="row-status" :style="{ color: colors.secondary }">
                    {{ item.status }}
                 </div>
            </div>
         </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useSectorStore } from '../../stores/sector'

const props = defineProps(['type'])
const sectorStore = useSectorStore()

const colors = computed(() => sectorStore.theme || {
    primary: '#0ea5e9',
    secondary: '#0f766e',
    text: '#0f172a'
})

const getColor = (name) => (sectorStore.theme || {})[name] || colors.value.primary
const getGlowColor = (name) => getColor(name) + '1A'

// Dynamic Content Configuration
const pageConfig = computed(() => {
    const sector = sectorStore.currentSectorId || 'medical'
    const type = props.type

    const configs = {
        medical: { title: 'Tıbbi Raporlar', subtitle: 'Lab ve Görüntüleme Sonuçları', icon: 'FileText' },
        legal: { title: 'Dava Dosyaları', subtitle: 'Aktif ve Arşivlenmiş Dosyalar', icon: 'Briefcase' },
        real_estate: { title: 'Portföy Yönetimi', subtitle: 'İlan ve Müşteri Kayıtları', icon: 'Home' },
        technology: { title: 'Sistem Durumu', subtitle: 'Server Hizmet Raporları', icon: 'Server' },
        finance: { title: 'Bütçe Raporları', subtitle: 'Aylık Gelir/Gider Tabloları', icon: 'PieChart' },
        education: { title: 'Ders Programı', subtitle: 'Haftalık Ders Çizelgesi', icon: 'Calendar' }
    }
    
    // Override if 'analytic' was requested specifically (though standard medical analytics uses PortalAnalytics)
    return configs[sector] || { title: 'Özel Sayfa', subtitle: 'Sektör Detayları', icon: 'FileText' }
})

const pageTitle = computed(() => pageConfig.value.title)
const pageSubtitle = computed(() => pageConfig.value.subtitle)
const pageIcon = computed(() => pageConfig.value.icon)

// Dummy Data Generator
const items = ref([])

onMounted(() => {
    // Simulate fetching data appropriate for the sector page
    items.value = [
        { title: 'Örnek Kayıt 1', desc: 'Detaylar buraya gelecek...', status: 'Aktif' },
        { title: 'Örnek Kayıt 2', desc: 'Sistem tarafından oluşturuldu.', status: 'Tamamlandı' },
        { title: 'Örnek Kayıt 3', desc: 'İşlem bekleniyor.', status: 'Beklemede' },
        { title: 'Örnek Kayıt 4', desc: 'Arşivlendi.', status: 'Pasif' }
    ]
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

.generic-list {
    display: flex;
    flex-direction: column;
    gap: 0;
}

.list-row {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px;
    border-bottom: 1px solid var(--border-subtle);
}

.list-row:last-child {
    border-bottom: none;
}

.row-icon {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.row-content {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.row-content strong {
    font-size: 14px;
    color: var(--text-primary);
}

.row-content span {
    font-size: 12px;
    color: var(--text-secondary);
}

.row-status {
    font-size: 13px;
    font-weight: 600;
}

.empty-state {
    text-align: center;
    padding: 40px;
    color: var(--text-secondary);
}
</style>
