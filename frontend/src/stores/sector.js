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
            real_estate: 'Real Estate',
            retail: 'Retail',
            manufacturing: 'Manufacturing',
            education: 'Education',
            automotive: 'Automotive',
            finance: 'Finance',
            hospitality: 'Hospitality',
            ecommerce: 'E-Commerce'
        }
        return names[currentSector.value] || 'Medical'
    })

    const sectorIcon = computed(() => {
        const icons = {
            medical: 'stethoscope',
            legal: 'scale',
            real_estate: 'home',
            retail: 'shopping-bag',
            manufacturing: 'hammer',
            education: 'graduation-cap',
            automotive: 'car',
            finance: 'landmark',
            hospitality: 'coffee',
            ecommerce: 'shopping-cart'
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
            },
            retail: {
                displayName: 'Retail',
                primaryColor: '#ec4899',
                accentColor: '#be185d'
            },
            manufacturing: {
                displayName: 'Sanayi',
                primaryColor: '#64748b',
                accentColor: '#475569'
            },
            education: {
                displayName: 'Eğitim',
                primaryColor: '#8b5cf6',
                accentColor: '#7c3aed'
            },
            automotive: {
                displayName: 'Otomotiv',
                primaryColor: '#ef4444',
                accentColor: '#dc2626'
            },
            finance: {
                displayName: 'Finance',
                primaryColor: '#14b8a6',
                accentColor: '#0d9488'
            },
            hospitality: {
                displayName: 'Hospitality',
                primaryColor: '#f97316',
                accentColor: '#ea580c'
            },
            ecommerce: {
                displayName: 'E-Commerce',
                primaryColor: '#ec4899',
                accentColor: '#be185d'
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

        // Sector specific terms
        const sectorTerms = {
            medical: {
                recent_activity_title: 'Son Randevular',
                client_label: 'Hasta',
                type_label: 'İşlem Türü'
            },
            legal: {
                recent_activity_title: 'Son Dosyalar',
                client_label: 'Müvekkil',
                type_label: 'Dava Türü'
            },
            real_estate: {
                recent_activity_title: 'Son Emlak Gösterimleri',
                client_label: 'Müşteri',
                type_label: 'İşlem'
            },
            retail: {
                recent_activity_title: 'Son Siparişler',
                client_label: 'Müşteri',
                type_label: 'Sipariş'
            },
            ecommerce: {
                recent_activity_title: 'Son Siparişler',
                client_label: 'Müşteri',
                type_label: 'Sepet'
            },
            automotive: {
                recent_activity_title: 'Son Servis Randevuları',
                client_label: 'Araç Sahibi',
                type_label: 'Servis'
            },
            finance: {
                recent_activity_title: 'Son İşlemler',
                client_label: 'Müşteri',
                type_label: 'İşlem'
            },
            education: {
                recent_activity_title: 'Son Görüşmeler',
                client_label: 'Veli/Öğrenci',
                type_label: 'Konu'
            },
            hospitality: {
                recent_activity_title: 'Son Rezervasyonlar',
                client_label: 'Misafir',
                type_label: 'Oda Tipi'
            },
            manufacturing: {
                recent_activity_title: 'Son Üretim Emirleri',
                client_label: 'Müşteri',
                type_label: 'Sipariş'
            }
        }

        // Check if it's a sector specific term request
        const term = sectorTerms[currentSector.value]?.[key]
        if (term) return term

        // Fallback or general translation
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
