import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

/**
 * Sector Store
 * Manages current sector state for adaptive UI
 */
export const useSectorStore = defineStore('sector', () => {
    // State
    const currentSector = ref(localStorage.getItem('current_sector') || 'medical')

    // Getters
    const sectorName = computed(() => {
        const names = {
            medical: 'Medical',
            legal: 'Legal',
            real_estate: 'Real Estate'
        }
        return names[currentSector.value] || 'Medical'
    })

    const sectorIcon = computed(() => {
        const icons = {
            medical: 'stethoscope',
            legal: 'scale',
            real_estate: 'home'
        }
        return icons[currentSector.value] || 'activity'
    })

    const config = computed(() => {
        const configs = {
            medical: {
                displayName: 'Medical',
                primaryColor: '#10b981',
                accentColor: '#059669'
            },
            legal: {
                displayName: 'Legal',
                primaryColor: '#3b82f6',
                accentColor: '#2563eb'
            },
            real_estate: {
                displayName: 'Real Estate',
                primaryColor: '#f59e0b',
                accentColor: '#d97706'
            }
        }
        return configs[currentSector.value] || configs.medical
    })

    // Translation helper
    const t = (key) => {
        const translations = {
            dashboard: 'Dashboard',
            documents: 'Belgeler',
            calendar: 'Takvim',
            settings: 'Ayarlar',
            analytics: 'Analitik'
        }
        return translations[key] || key
    }

    // Actions
    const setSector = (sector) => {
        currentSector.value = sector
        localStorage.setItem('current_sector', sector)
    }

    const clearSector = () => {
        currentSector.value = 'medical'
        localStorage.removeItem('current_sector')
    }

    return {
        // State
        currentSector,

        // Getters
        sectorName,
        sectorIcon,
        config,

        // Methods
        t,
        setSector,
        clearSector
    }
})
