import { ref, computed } from 'vue'

/**
 * Sector Theme Composable
 * Provides sector-specific theming (colors, gradients, icons)
 */

const SECTOR_THEMES = {
    medical: {
        name: 'Sağlık & Klinik',
        primaryGradient: 'linear-gradient(135deg, #ef4444, #f87171)',
        accentColor: '#fca5a5',
        iconColor: '#ef4444',
        glowColor: 'rgba(239, 68, 68, 0.3)',
        backgroundColor: 'rgba(239, 68, 68, 0.05)'
    },
    beauty: {
        name: 'Güzellik Merkezi',
        primaryGradient: 'linear-gradient(135deg, #ec4899, #f472b6)',
        accentColor: '#f9a8d4',
        iconColor: '#ec4899',
        glowColor: 'rgba(236, 72, 153, 0.3)',
        backgroundColor: 'rgba(236, 72, 153, 0.05)'
    },
    hospitality: {
        name: 'Otel Yönetimi',
        primaryGradient: 'linear-gradient(135deg, #ea580c, #0891b2)',
        accentColor: '#fb923c',
        iconColor: '#ea580c',
        glowColor: 'rgba(234, 88, 12, 0.3)',
        backgroundColor: 'rgba(234, 88, 12, 0.05)'
    },
    legal: {
        name: 'Hukuk & Danışmanlık',
        primaryGradient: 'linear-gradient(135deg, #3b82f6, #60a5fa)',
        accentColor: '#93c5fd',
        iconColor: '#3b82f6',
        glowColor: 'rgba(59, 130, 246, 0.3)',
        backgroundColor: 'rgba(59, 130, 246, 0.05)'
    },
    real_estate: {
        name: 'Gayrimenkul',
        primaryGradient: 'linear-gradient(135deg, #10b981, #34d399)',
        accentColor: '#6ee7b7',
        iconColor: '#10b981',
        glowColor: 'rgba(16, 185, 129, 0.3)',
        backgroundColor: 'rgba(16, 185, 129, 0.05)'
    },
    manufacturing: {
        name: 'Üretim & Sanayi',
        primaryGradient: 'linear-gradient(135deg, #64748b, #94a3b8)',
        accentColor: '#cbd5e1',
        iconColor: '#64748b',
        glowColor: 'rgba(100, 116, 139, 0.3)',
        backgroundColor: 'rgba(100, 116, 139, 0.05)'
    },
    ecommerce: {
        name: 'E-Ticaret',
        primaryGradient: 'linear-gradient(135deg, #8b5cf6, #a78bfa)',
        accentColor: '#c4b5fd',
        iconColor: '#8b5cf6',
        glowColor: 'rgba(139, 92, 246, 0.3)',
        backgroundColor: 'rgba(139, 92, 246, 0.05)'
    },
    education: {
        name: 'Eğitim',
        primaryGradient: 'linear-gradient(135deg, #f59e0b, #fbbf24)',
        accentColor: '#fcd34d',
        iconColor: '#f59e0b',
        glowColor: 'rgba(245, 158, 11, 0.3)',
        backgroundColor: 'rgba(245, 158, 11, 0.05)'
    },
    finance: {
        name: 'Finans',
        primaryGradient: 'linear-gradient(135deg, #06b6d4, #22d3ee)',
        accentColor: '#67e8f9',
        iconColor: '#06b6d4',
        glowColor: 'rgba(6, 182, 212, 0.3)',
        backgroundColor: 'rgba(6, 182, 212, 0.05)'
    },
    automotive: {
        name: 'Otomotiv',
        primaryGradient: 'linear-gradient(135deg, #dc2626, #ef4444)',
        accentColor: '#f87171',
        iconColor: '#dc2626',
        glowColor: 'rgba(220, 38, 38, 0.3)',
        backgroundColor: 'rgba(220, 38, 38, 0.05)'
    },
    retail: {
        name: 'Perakende',
        primaryGradient: 'linear-gradient(135deg, #7c3aed, #8b5cf6)',
        accentColor: '#a78bfa',
        iconColor: '#7c3aed',
        glowColor: 'rgba(124, 58, 237, 0.3)',
        backgroundColor: 'rgba(124, 58, 237, 0.05)'
    }
}

export function useSectorTheme(sectorKey) {
    const theme = computed(() => SECTOR_THEMES[sectorKey] || SECTOR_THEMES.medical)

    const applyTheme = () => {
        if (typeof document !== 'undefined') {
            const root = document.documentElement
            root.style.setProperty('--sector-gradient', theme.value.primaryGradient)
            root.style.setProperty('--sector-accent', theme.value.accentColor)
            root.style.setProperty('--sector-icon', theme.value.iconColor)
            root.style.setProperty('--sector-glow', theme.value.glowColor)
            root.style.setProperty('--sector-bg', theme.value.backgroundColor)
        }
    }

    return {
        theme,
        applyTheme
    }
}
