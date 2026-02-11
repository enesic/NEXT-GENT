/**
 * Premium Sector Theme Configuration
 * World-class UI/UX design system for NextGent CRM
 * 
 * Each sector has a carefully curated color palette designed by
 * professional UI/UX designers to evoke the right emotions and
 * maintain brand consistency.
 */

export const sectorThemes = {
    medical: {
        name: 'Medical & Healthcare',
        displayName: 'Sağlık',
        colors: {
            primary: '#2563eb',      // Deep Blue - Trust & Professionalism
            secondary: '#7c3aed',    // Royal Purple - Premium Care
            accent: '#0ea5e9',       // Sky Blue - Modern Medicine
            success: '#10b981',      // Emerald - Health & Vitality
            warning: '#f59e0b',      // Amber - Attention
            danger: '#ef4444',       // Red - Urgency
            background: '#0f172a',   // Slate 900 - Professional Dark
            surface: '#1e293b',      // Slate 800
            surfaceLight: '#334155', // Slate 700
            text: '#f1f5f9',         // Slate 100
            textMuted: '#94a3b8',    // Slate 400
        },
        gradients: {
            primary: 'linear-gradient(135deg, #2563eb 0%, #7c3aed 100%)',
            hero: 'linear-gradient(135deg, #1e3a8a 0%, #581c87 100%)',
            card: 'linear-gradient(145deg, #1e293b 0%, #0f172a 100%)',
        },
        shadows: {
            sm: '0 1px 2px 0 rgb(37 99 235 / 0.1)',
            md: '0 4px 6px -1px rgb(37 99 235 / 0.15)',
            lg: '0 10px 15px -3px rgb(37 99 235 / 0.2)',
            glow: '0 0 20px rgb(37 99 235 / 0.3)',
        },
        fonts: {
            heading: "'Inter', -apple-system, sans-serif",
            body: "'Inter', -apple-system, sans-serif",
            mono: "'JetBrains Mono', monospace",
        }
    },

    beauty: {
        name: 'Beauty & Wellness',
        displayName: 'Güzellik Merkezi',
        colors: {
            primary: '#ec4899',      // Pink - Elegance & Beauty
            secondary: '#f59e0b',    // Amber - Luxury & Warmth
            accent: '#a855f7',       // Purple - Premium & Sophistication
            success: '#22c55e',      // Green - Wellness
            warning: '#fb923c',      // Orange - Energy
            danger: '#f43f5e',       // Rose - Attention
            background: '#0a0a0b',   // Pure Black - Luxury
            surface: '#1a1a1d',      // Near Black
            surfaceLight: '#2d2d30', // Dark Gray
            text: '#fef3f2',         // Rose 50
            textMuted: '#fda4af',    // Rose 300
        },
        gradients: {
            primary: 'linear-gradient(135deg, #ec4899 0%, #a855f7 100%)',
            hero: 'linear-gradient(135deg, #be185d 0%, #7e22ce 100%)',
            card: 'linear-gradient(145deg, #1a1a1d 0%, #0a0a0b 100%)',
            luxury: 'linear-gradient(135deg, #f59e0b 0%, #ec4899 50%, #a855f7 100%)',
        },
        shadows: {
            sm: '0 1px 2px 0 rgb(236 72 153 / 0.1)',
            md: '0 4px 6px -1px rgb(236 72 153 / 0.15)',
            lg: '0 10px 15px -3px rgb(236 72 153 / 0.2)',
            glow: '0 0 25px rgb(236 72 153 / 0.4)',
        },
        fonts: {
            heading: "'Playfair Display', serif",
            body: "'Inter', -apple-system, sans-serif",
            mono: "'JetBrains Mono', monospace",
        }
    },

    hospitality: {
        name: 'Hospitality & Hotels',
        displayName: 'Otelcilik',
        colors: {
            primary: '#ea580c',      // Orange - Warmth & Welcome
            secondary: '#0891b2',    // Cyan - Tranquility & Relaxation
            accent: '#facc15',       // Yellow - Hospitality & Service
            success: '#16a34a',      // Green - Comfort
            warning: '#f59e0b',      // Amber - Attention
            danger: '#dc2626',       // Red - Urgency
            background: '#0c0a09',   // Stone 950 - Sophisticated Dark
            surface: '#1c1917',      // Stone 900
            surfaceLight: '#292524', // Stone 800
            text: '#fafaf9',         // Stone 50
            textMuted: '#a8a29e',    // Stone 400
        },
        gradients: {
            primary: 'linear-gradient(135deg, #ea580c 0%, #0891b2 100%)',
            hero: 'linear-gradient(135deg, #c2410c 0%, #155e75 100%)',
            card: 'linear-gradient(145deg, #1c1917 0%, #0c0a09 100%)',
            welcome: 'linear-gradient(135deg, #facc15 0%, #ea580c 50%, #0891b2 100%)',
        },
        shadows: {
            sm: '0 1px 2px 0 rgb(234 88 12 / 0.1)',
            md: '0 4px 6px -1px rgb(234 88 12 / 0.15)',
            lg: '0 10px 15px -3px rgb(234 88 12 / 0.2)',
            glow: '0 0 20px rgb(234 88 12 / 0.3)',
        },
        fonts: {
            heading: "'Cormorant Garamond', serif",
            body: "'Inter', -apple-system, sans-serif",
            mono: "'JetBrains Mono', monospace",
        }
    },

    legal: {
        name: 'Legal Services',
        displayName: 'Hukuk',
        colors: {
            primary: '#1e40af',      // Deep Blue - Authority & Trust
            secondary: '#713f12',    // Brown - Tradition & Stability
            accent: '#0369a1',       // Sky - Clarity & Justice
            success: '#15803d',      // Green
            warning: '#ca8a04',      // Yellow
            danger: '#b91c1c',       // Red
            background: '#0f172a',   // Slate 900
            surface: '#1e293b',      // Slate 800
            surfaceLight: '#334155', // Slate 700
            text: '#f8fafc',         // Slate 50
            textMuted: '#94a3b8',    // Slate 400
        },
        gradients: {
            primary: 'linear-gradient(135deg, #1e40af 0%, #713f12 100%)',
            hero: 'linear-gradient(135deg, #1e3a8a 0%, #451a03 100%)',
            card: 'linear-gradient(145deg, #1e293b 0%, #0f172a 100%)',
        },
        shadows: {
            sm: '0 1px 2px 0 rgb(30 64 175 / 0.1)',
            md: '0 4px 6px -1px rgb(30 64 175 / 0.15)',
            lg: '0 10px 15px -3px rgb(30 64 175 / 0.2)',
            glow: '0 0 20px rgb(30 64 175 / 0.25)',
        },
        fonts: {
            heading: "'Merriweather', serif",
            body: "'Inter', -apple-system, sans-serif",
            mono: "'JetBrains Mono', monospace",
        }
    },

    retail: {
        name: 'Retail & Commerce',
        displayName: 'Perakende',
        colors: {
            primary: '#db2777',      // Pink - Energy & Engagement
            secondary: '#9333ea',    // Purple - Premium Shopping
            accent: '#0284c7',       // Blue - Trust
            success: '#059669',      // Green - Purchase Success
            warning: '#d97706',      // Amber
            danger: '#dc2626',       // Red
            background: '#0c0a09',   // Stone 950
            surface: '#1c1917',      // Stone 900
            surfaceLight: '#292524', // Stone 800
            text: '#fafaf9',         // Stone 50
            textMuted: '#a8a29e',    // Stone 400
        },
        gradients: {
            primary: 'linear-gradient(135deg, #db2777 0%, #9333ea 100%)',
            hero: 'linear-gradient(135deg, #be185d 0%, #7e22ce 100%)',
            card: 'linear-gradient(145deg, #1c1917 0%, #0c0a09 100%)',
        },
        shadows: {
            sm: '0 1px 2px 0 rgb(219 39 119 / 0.1)',
            md: '0 4px 6px -1px rgb(219 39 119 / 0.15)',
            lg: '0 10px 15px -3px rgb(219 39 119 / 0.2)',
            glow: '0 0 20px rgb(219 39 119 / 0.3)',
        },
        fonts: {
            heading: "'Montserrat', sans-serif",
            body: "'Inter', -apple-system, sans-serif",
            mono: "'JetBrains Mono', monospace",
        }
    },

    // Add more sectors as needed...
    default: {
        name: 'Default Theme',
        displayName: 'Varsayılan',
        colors: {
            primary: '#3b82f6',
            secondary: '#8b5cf6',
            accent: '#06b6d4',
            success: '#10b981',
            warning: '#f59e0b',
            danger: '#ef4444',
            background: '#0f172a',
            surface: '#1e293b',
            surfaceLight: '#334155',
            text: '#f1f5f9',
            textMuted: '#94a3b8',
        },
        gradients: {
            primary: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
            hero: 'linear-gradient(135deg, #1e40af 0%, #6d28d9 100%)',
            card: 'linear-gradient(145deg, #1e293b 0%, #0f172a 100%)',
        },
        shadows: {
            sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
            md: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
            lg: '0 10px 15px -3px rgb(0 0 0 / 0.15)',
            glow: '0 0 20px rgb(59 130 246 / 0.3)',
        },
        fonts: {
            heading: "'Inter', -apple-system, sans-serif",
            body: "'Inter', -apple-system, sans-serif",
            mono: "'JetBrains Mono', monospace",
        }
    }
}

/**
 * Apply theme to document root
 * @param {string} sector - Sector key (e.g., 'medical', 'beauty')
 */
export function applyTheme(sector) {
    const theme = sectorThemes[sector] || sectorThemes.default
    const root = document.documentElement

    // Apply CSS custom properties
    Object.entries(theme.colors).forEach(([key, value]) => {
        root.style.setProperty(`--color-${key}`, value)
    })

    // Apply gradients
    Object.entries(theme.gradients).forEach(([key, value]) => {
        root.style.setProperty(`--gradient-${key}`, value)
    })

    // Apply shadows
    Object.entries(theme.shadows).forEach(([key, value]) => {
        root.style.setProperty(`--shadow-${key}`, value)
    })

    // Apply fonts
    Object.entries(theme.fonts).forEach(([key, value]) => {
        root.style.setProperty(`--font-${key}`, value)
    })

    // Store current sector
    root.setAttribute('data-sector', sector)
}

/**
 * Get theme for a specific sector
 * @param {string} sector - Sector key
 * @returns {Object} Theme configuration
 */
export function getTheme(sector) {
    return sectorThemes[sector] || sectorThemes.default
}

/**
 * Get all available sectors
 * @returns {Array<string>} Sector keys
 */
export function getAvailableSectors() {
    return Object.keys(sectorThemes).filter(key => key !== 'default')
}
