
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
            // General
            dashboard: 'Genel Bakış',
            documents: 'Belgeler',
            calendar: 'Takvim',
            settings: 'Ayarlar',
            welcome_message: 'Hoş Geldiniz',
            dashboard_subtitle: 'Hesap özetiniz ve son aktiviteleriniz',
            recent_activity: 'Son Aktiviteler',
            quick_actions: 'Hızlı İşlemler',
            recent_activity_title: 'Son İşlemler',
            client_label: 'Müşteri',
            type_label: 'İşlem',

            // Customer Sidebar
            appointments: 'Randevularım',
            messages: 'Mesajlar',
            calls: 'Aramalar',
            satisfaction: 'Memnuniyet',

            // Admin Sidebar
            admin_dashboard: 'Dashboard',
            users: 'Kullanıcılar',
            cards: 'Kartlar',
            flows: 'Akış Motoru',
            audits: 'Audit Logları',
            analytics: 'Analitik',
            // Settings Overview
            settings_desc: 'Hesap ve uygulama tercihlerini yönetin',
            save_all: 'Tümünü Kaydet',
            profile_settings: 'Profil Ayarları',
            full_name: 'Ad Soyad',
            email_address: 'Email Adresi',
            phone: 'Telefon',
            appearance: 'Görünüm Ayarları',
            dark_mode: 'Koyu Mod',
            dark_mode_desc: 'Göz yorgunluğunu azaltan karanlık arayüz',
            high_contrast: 'Yüksek Karşıtlık',
            high_contrast_desc: 'Daha belirgin metin ve bileşenler',
            compact_view: 'Kompakt Görünüm',
            compact_view_desc: 'Daha fazla veriyi tek ekranda görün',
            notifications: 'Bildirim Ayarları',
            email_notif: 'Email Bildirimleri',
            email_notif_desc: 'Önemli güncellemeleri e-posta ile al',
            sms_notif: 'SMS Bildirimleri',
            sms_notif_desc: 'Randevu hatırlatmalarını SMS ile al',
            security_settings: 'Güvenlik Ayarları',
            two_factor: 'İki Faktörlü Doğrulama',
            two_factor_desc: 'Ekstra güvenlik katmanı ekleyin',
            enable: 'Etkinleştir',
            password_update: 'Şifre Güncelleme',
            password_desc: 'Son güncelleme: 3 ay önce',
            change: 'Değiştir',
            account_recovery: 'Hesap Kurtarma',
            account_recovery_desc: 'Yedek e-posta ve telefon ayarları',
            configure: 'Yapılandır',
            privacy_data: 'Gizlilik ve Veri',
            data_personalization: 'Veri Kişiselleştirme',
            data_pers_desc: 'Deneyiminizi iyileştirmek için verileri kullan',
            download_data: 'Verilerimi İndir',
            download_data_desc: 'Tüm kişisel verilerinizin bir kopyasını alın',
            download: 'İndir',
            storage: 'Depolama Yönetimi',
            used_storage: '6.5 GB / 10 GB Kullanıldı',
            upgrade_plan: 'Plânı Yükselt',
            connected_apps: 'Bağlı Uygulamalar',
            connect: 'Bağla',
            connected: 'Bağlı',
            billing: 'Ödeme ve Faturalandırma',
            current_plan: 'Mevcut Paket',
            lang_region: 'Dil ve Bölge',
            interface_lang: 'Arayüz Dili',
            timezone: 'Saat Dilimi',
            advanced: 'Gelişmiş Ayarlar',
            beta_features: 'Beta Özellikler',
            beta_desc: 'Yeni özellikleri herkesten önce deneyin',
            analytics_sharing: 'Analitik Paylaşımı',
            analytics_desc: 'Hata raporlarını otomatik olarak gönder'
        },
        en: {
            // General
            dashboard: 'Overview',
            documents: 'Documents',
            calendar: 'Calendar',
            settings: 'Settings',
            welcome_message: 'Welcome Back',
            dashboard_subtitle: 'Account summary and recent activity',
            recent_activity: 'Recent Activity',
            quick_actions: 'Quick Actions',
            recent_activity_title: 'Recent Transactions',
            client_label: 'Client',
            type_label: 'Action',

            // Customer Sidebar
            appointments: 'Appointments',
            messages: 'Messages',
            calls: 'Calls',
            satisfaction: 'Satisfaction',

            // Admin Sidebar
            admin_dashboard: 'Dashboard',
            users: 'Users',
            cards: 'Cards',
            flows: 'Flow Engine',
            audits: 'Audit Logs',
            analytics: 'Analytics',

            // Settings Overview
            settings_desc: 'Manage account & application preferences',
            save_all: 'Save All',
            profile_settings: 'Profile Settings',
            full_name: 'Full Name',
            email_address: 'Email Address',
            phone: 'Phone',
            appearance: 'Appearance',
            dark_mode: 'Dark Mode',
            dark_mode_desc: 'Reduce eye strain with dark interface',
            high_contrast: 'High Contrast',
            high_contrast_desc: 'More prominent text and components',
            compact_view: 'Compact View',
            compact_view_desc: 'See more data on a single screen',
            notifications: 'Notifications',
            email_notif: 'Email Notifications',
            email_notif_desc: 'Receive important updates via email',
            sms_notif: 'SMS Notifications',
            sms_notif_desc: 'Receive appointment reminders via SMS',
            security_settings: 'Security Settings',
            two_factor: 'Two-Factor Auth',
            two_factor_desc: 'Add an extra layer of security',
            enable: 'Enable',
            password_update: 'Update Password',
            password_desc: 'Last updated: 3 months ago',
            change: 'Change',
            account_recovery: 'Account Recovery',
            account_recovery_desc: 'Backup email & phone settings',
            configure: 'Configure',
            privacy_data: 'Privacy & Data',
            data_personalization: 'Data Personalization',
            data_pers_desc: 'Use data to improve your experience',
            download_data: 'Download My Data',
            download_data_desc: 'Get a copy of all your personal data',
            download: 'Download',
            storage: 'Storage Management',
            used_storage: '6.5 GB / 10 GB Used',
            upgrade_plan: 'Upgrade Plan',
            connected_apps: 'Connected Apps',
            connect: 'Connect',
            connected: 'Connected',
            billing: 'Billing & Payment',
            current_plan: 'Current Plan',
            lang_region: 'Language & Region',
            interface_lang: 'Interface Language',
            timezone: 'Timezone',
            advanced: 'Advanced Settings',
            beta_features: 'Beta Features',
            beta_desc: 'Try new features before everyone else',
            analytics_sharing: 'Analytics Sharing',
            analytics_desc: 'Automatically send crash reports'
        },
        de: {
            // General
            dashboard: 'Überblick',
            documents: 'Dokumente',
            calendar: 'Kalender',
            settings: 'Einstellungen',
            welcome_message: 'Willkommen zurück',
            dashboard_subtitle: 'Kontozusammenfassung und Aktivitäten',
            recent_activity: 'Letzte Aktivitäten',
            quick_actions: 'Schnellaktionen',
            recent_activity_title: 'Letzte Transaktionen',
            client_label: 'Kunde',
            type_label: 'Aktion',

            // Customer Sidebar
            appointments: 'Termine',
            messages: 'Nachrichten',
            calls: 'Anrufe',
            satisfaction: 'Zufriedenheit',

            // Admin Sidebar
            admin_dashboard: 'Dashboard',
            users: 'Benutzer',
            cards: 'Karten',
            flows: 'Flow-Engine',
            audits: 'Audit-Protokolle',
            analytics: 'Analytik',

            // Settings Overview
            settings_desc: 'Konto- und App-Präferenzen verwalten',
            save_all: 'Alle Speichern',
            profile_settings: 'Profileinstellungen',
            full_name: 'Vollständiger Name',
            email_address: 'E-Mail-Adresse',
            phone: 'Telefon',
            appearance: 'Erscheinungsbild',
            dark_mode: 'Dunkler Modus',
            dark_mode_desc: 'Verringern Sie die Augenbelastung',
            high_contrast: 'Hoher Kontrast',
            high_contrast_desc: 'Markantere Texte und Komponenten',
            compact_view: 'Kompakte Ansicht',
            compact_view_desc: 'Mehr Daten auf einem Bildschirm',
            notifications: 'Benachrichtigungen',
            email_notif: 'E-Mail-Benachrichtigungen',
            email_notif_desc: 'Wichtige Updates per E-Mail erhalten',
            sms_notif: 'SMS-Benachrichtigungen',
            sms_notif_desc: 'Terminerinnerungen per SMS erhalten',
            security_settings: 'Sicherheitseinstellungen',
            two_factor: 'Zweistufige Authentifizierung',
            two_factor_desc: 'Zusätzliche Sicherheitsebene',
            enable: 'Aktivieren',
            password_update: 'Passwort aktualisieren',
            password_desc: 'Zuletzt aktualisiert: vor 3 Monaten',
            change: 'Ändern',
            account_recovery: 'Kontowiederherstellung',
            account_recovery_desc: 'E-Mail & Telefon für Wiederherstellung',
            configure: 'Konfigurieren',
            privacy_data: 'Datenschutz & Daten',
            data_personalization: 'Datenpersonalisierung',
            data_pers_desc: 'Daten zur Verbesserung nutzen',
            download_data: 'Meine Daten herunterladen',
            download_data_desc: 'Kopie aller persönlichen Daten',
            download: 'Herunterladen',
            storage: 'Speicherverwaltung',
            used_storage: '6.5 GB / 10 GB Genutzt',
            upgrade_plan: 'Plan aktualisieren',
            connected_apps: 'Verbundene Apps',
            connect: 'Verbinden',
            connected: 'Verbunden',
            billing: 'Abrechnung & Zahlung',
            current_plan: 'Aktueller Plan',
            lang_region: 'Sprache & Region',
            interface_lang: 'Sprachen',
            timezone: 'Zeitzone',
            advanced: 'Erweiterte Einstellungen',
            beta_features: 'Beta-Funktionen',
            beta_desc: 'Neue Funktionen als Erster testen',
            analytics_sharing: 'Analysefreigabe',
            analytics_desc: 'Fehlerberichte automatisch senden'
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
