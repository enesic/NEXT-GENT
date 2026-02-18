
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { sectorThemes } from '../config/sectorThemes'
import * as LucideIcons from 'lucide-vue-next'

/**
 * Sector Store
 * Manages current sector state and provides theme data
 */
export const useSectorStore = defineStore('sector', () => {
    // State
    const currentSectorId = ref(sessionStorage.getItem('current_sector') || 'medical')

    // Actions
    const setSector = (sectorId) => {
        if (sectorThemes[sectorId]) {
            currentSectorId.value = sectorId
            sessionStorage.setItem('current_sector', sectorId)
        }
    }

    // Getters
    const currentSector = computed(() => {
        return sectorThemes[currentSectorId.value] || sectorThemes.medical
    })

    const theme = computed(() => currentSector.value.colors)

    // Helper to resolve string icon names to components
    const getIcon = (iconName) => {
        return LucideIcons[iconName] || LucideIcons.HelpCircle
    }

    // Simple translation/text helper to prevent crashes
    const t = (key) => {
        const defaults = {
            dashboard: 'Dashboard',
            documents: 'Belgeler',
            calendar: 'Takvim',
            settings: 'Ayarlar',
            welcome_message: 'Hoş Geldiniz',
            dashboard_subtitle: 'Hesap özetiniz ve son aktiviteleriniz',
            recent_activity: 'Son Aktiviteler',
            quick_actions: 'Hızlı İşlemler',
            recent_activity_title: 'Son İşlemler',
            client_label: 'Müşteri',
            type_label: 'İşlem'
        }
        return defaults[key] || key
    }

    // Computed Data exposure
    const stats = computed(() => currentSector.value.stats)
    const quickActions = computed(() => currentSector.value.quickActions)
    const chartConfig = computed(() => currentSector.value.chartConfig)

    return {
        currentSectorId,
        currentSector,
        theme,
        stats,
        quickActions,
        chartConfig,
        setSector,
        getIcon,
        t
    }
})
