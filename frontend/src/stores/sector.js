
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
        return sectorThemes[currentSectorId.value] || {
            label: 'Genel',
            colors: {
                primary: '#0ea5e9',
                secondary: '#0f766e',
                accent: '#38bdf8',
                text: '#e2e8f0'
            },
            stats: [],
            quickActions: []
        }
    })

    const theme = computed(() => currentSector.value.colors)

    // Helper to resolve string icon names to components
    const getIcon = (iconName) => {
        return LucideIcons[iconName] || LucideIcons.HelpCircle
    }

    // Reactive translations
    const currentLocale = ref(localStorage.getItem('user_language') || 'tr')

    const translations = {
        tr: {
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
        },
        en: {
            dashboard: 'Dashboard',
            documents: 'Documents',
            calendar: 'Calendar',
            settings: 'Settings',
            welcome_message: 'Welcome Back',
            dashboard_subtitle: 'Account summary and recent activity',
            recent_activity: 'Recent Activity',
            quick_actions: 'Quick Actions',
            recent_activity_title: 'Recent Transactions',
            client_label: 'Client',
            type_label: 'Action'
        },
        de: {
            dashboard: 'Armaturenbrett',
            documents: 'Dokumente',
            calendar: 'Kalender',
            settings: 'Einstellungen',
            welcome_message: 'Willkommen zurück',
            dashboard_subtitle: 'Kontozusammenfassung und Aktivitäten',
            recent_activity: 'Letzte Aktivitäten',
            quick_actions: 'Schnellaktionen',
            recent_activity_title: 'Letzte Transaktionen',
            client_label: 'Kunde',
            type_label: 'Aktion'
        }
    }

    const t = (key) => {
        return translations[currentLocale.value]?.[key] || translations['tr'][key] || key
    }

    const setLocale = (lang) => {
        if (translations[lang]) {
            currentLocale.value = lang
            localStorage.setItem('user_language', lang)
        }
    }

    // Computed Data exposure
    const stats = computed(() => currentSector.value.stats)
    const quickActions = computed(() => currentSector.value.quickActions)
    const chartConfig = computed(() => currentSector.value.chartConfig || currentSector.value.chart)

    return {
        currentSectorId,
        currentSector,
        theme,
        stats,
        quickActions,
        chartConfig,
        setSector,
        getIcon,
        t,
        currentLocale,
        setLocale
    }
})
