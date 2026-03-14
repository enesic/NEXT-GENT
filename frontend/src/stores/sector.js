
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { sectorThemes } from '../config/sectorThemes'
// import * as LucideIcons from 'lucide-vue-next'

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
        // Temporarily returning null or a placeholder to test build
        return iconName
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
            analytics_desc: 'Hata raporlarını otomatik olarak gönder',

            // Messages & Calls
            messages_title: 'Mesajlar',
            messages_subtitle: 'Gelen kutusu ve mesaj geçmişiniz',
            calls_title: 'Aramalar',
            calls_subtitle: 'Çağrı geçmişi ve detayları',
            loading_messages: 'Mesajlar yükleniyor...',
            loading_calls: 'Aramalar yükleniyor...',
            no_messages: 'Henüz bir mesajınız bulunmuyor.',
            no_calls: 'Henüz bir arama kaydı bulunmuyor.',
            previous: 'Önceki',
            next: 'Sonraki',
            page: 'Sayfa',
            total_items: 'toplam',

            // Documents View
            documents_title: 'Belgeler',
            documents_loading: 'Belgeler yükleniyor...',
            documents_empty: 'Belge bulunamadı',
            documents_clear_filters: 'Filtreleri Temizle',
            documents_upload: 'Yükle',
            documents_found: 'belge bulundu',
            documents_search_placeholder: 'Belge ara...',
            documents_size: 'Boyut',
            documents_type: 'Tür',

            // Calendar & Appointments
            calendar_title: 'Takvim',
            appointments_title: 'Randevular',
            upcoming_events: 'Yaklaşan Etkinlikler',
            new_appointment: 'Yeni Randevu',
            events_count: 'randevu/etkinlik',
            no_scheduled_events: 'Yakın zamanda planlanmış bir randevu bulunmuyor.',
            month_view: 'Ay',
            week_view: 'Hafta',
            list_view: 'Liste',

            // Statuses
            status_read: 'Okundu',
            status_unread: 'Okunmadı',
            status_replied: 'Yanıtlandı',
            status_answered: 'Cevaplandı',
            status_missed: 'Kaçırıldı',
            status_busy: 'Meşgul',
            status_resolved: 'Çözüldü',
            status_closed: 'Kapatıldı',
            status_open: 'Açık',
            customer_fallback: 'Müşteri',
            cancel: 'İptal',
            save: 'Kaydet',
            processing: 'İşleniyor...',
            success_saved: 'İşlem başarıyla kaydedildi!',
            complete_action: 'İşlemi Tamamla',

            // Analytics View
            performance_analysis: 'Performans Analizi',
            analytics_subtitle: 'Detaylı istatistik ve raporlar',
            monthly_interaction: 'Aylık Etkileşim Hacmi',
            appointment_distribution: 'Randevu Dağılımı',
            conversion_rate: 'Dönüşüm Oranı',
            data_loading: 'Veri yükleniyor...',
            retry: 'Tekrar Dene',

            // Satisfaction View
            satisfaction_title: 'Memnuniyet',
            satisfaction_subtitle: 'Geri bildirimleriniz bizim için değerli',
            overall_satisfaction: 'Genel Memnuniyet',
            recent_feedbacks: 'Son Geri Bildirimleriniz',
            send_new_feedback: 'Yeni Geri Bildirim Gönder',
            new_feedback_title: 'Yeni Geri Bildirim',
            rate_service: 'Hizmetimizi puanlayın',
            your_thoughts: 'Düşünceleriniz',
            feedback_placeholder: 'Hizmetimiz hakkında her türlü görüş, öneri veya şikayetinizi yazabilirsiniz...',
            cancel: 'İptal',
            send: 'Gönder',
            sending: 'Gönderiliyor...',
            feedback_success: 'Geri bildiriminiz başarıyla iletildi. Teşekkür ederiz!',
            feedback_success_title: 'Geri Bildirim Alındı',
            system_error: 'Sistem Hatası',
            feedback_error: 'Geri bildirim gönderilirken bir hata oluştu'
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
            analytics_desc: 'Automatically send crash reports',

            // Messages & Calls
            messages_title: 'Messages',
            messages_subtitle: 'Inbox and message history',
            calls_title: 'Calls',
            calls_subtitle: 'Call history and details',
            loading_messages: 'Loading messages...',
            loading_calls: 'Loading calls...',
            no_messages: 'You don\'t have any messages yet.',
            no_calls: 'No call records found yet.',
            previous: 'Previous',
            next: 'Next',
            page: 'Page',
            total_items: 'total',

            // Documents View
            documents_title: 'Documents',
            documents_loading: 'Loading documents...',
            documents_empty: 'No documents found',
            documents_clear_filters: 'Clear Filters',
            documents_upload: 'Upload',
            documents_found: 'documents found',
            documents_search_placeholder: 'Search documents...',
            documents_size: 'Size',
            documents_type: 'Type',

            // Calendar & Appointments
            calendar_title: 'Calendar',
            appointments_title: 'Appointments',
            upcoming_events: 'Upcoming Events',
            new_appointment: 'New Appointment',
            events_count: 'appointments/events',
            no_scheduled_events: 'No upcoming scheduled appointments.',
            month_view: 'Month',
            week_view: 'Week',
            list_view: 'List',

            // Statuses
            status_read: 'Read',
            status_unread: 'Unread',
            status_replied: 'Replied',
            status_answered: 'Answered',
            status_missed: 'Missed',
            status_busy: 'Busy',
            status_resolved: 'Resolved',
            status_closed: 'Closed',
            status_open: 'Open',
            customer_fallback: 'Customer',
            cancel: 'Cancel',
            save: 'Save',
            processing: 'Processing...',
            success_saved: 'Action saved successfully!',
            complete_action: 'Complete Action',

            // Analytics View
            performance_analysis: 'Performance Analysis',
            analytics_subtitle: 'Detailed statistics and reports',
            monthly_interaction: 'Monthly Interaction Volume',
            appointment_distribution: 'Appointment Distribution',
            conversion_rate: 'Conversion Rate',
            data_loading: 'Loading data...',
            retry: 'Try Again',

            // Satisfaction View
            satisfaction_title: 'Satisfaction',
            satisfaction_subtitle: 'Your feedback is valuable to us',
            overall_satisfaction: 'Overall Satisfaction',
            recent_feedbacks: 'Your Recent Feedbacks',
            send_new_feedback: 'Send New Feedback',
            new_feedback_title: 'New Feedback',
            rate_service: 'Rate our service',
            your_thoughts: 'Your thoughts',
            feedback_placeholder: 'You can write any opinions, suggestions or complaints about our service...',
            cancel: 'Cancel',
            send: 'Send',
            sending: 'Sending...',
            feedback_success: 'Your feedback has been successfully delivered. Thank you!',
            feedback_success_title: 'Feedback Received',
            system_error: 'System Error',
            feedback_error: 'An error occurred while sending feedback'
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
            analytics_desc: 'Fehlerberichte automatisch senden',

            // Messages & Calls
            messages_title: 'Nachrichten',
            messages_subtitle: 'Posteingang und Nachrichtenverlauf',
            calls_title: 'Anrufe',
            calls_subtitle: 'Anrufverlauf und Details',
            loading_messages: 'Nachrichten werden geladen...',
            loading_calls: 'Anrufe werden geladen...',
            no_messages: 'Sie haben noch keine Nachrichten.',
            no_calls: 'Noch keine Anrufprotokolle gefunden.',
            previous: 'Zurück',
            next: 'Weiter',
            page: 'Seite',
            total_items: 'insgesamt',

            // Documents View
            documents_title: 'Dokumente',
            documents_loading: 'Dokumente werden geladen...',
            documents_empty: 'Keine Dokumente gefunden',
            documents_clear_filters: 'Filter löschen',
            documents_upload: 'Hochladen',
            documents_found: 'Dokumente gefunden',
            documents_search_placeholder: 'Dokumente suchen...',
            documents_size: 'Größe',
            documents_type: 'Typ',

            // Calendar & Appointments
            calendar_title: 'Kalender',
            appointments_title: 'Termine',
            upcoming_events: 'Kommende Termine',
            new_appointment: 'Neuer Termin',
            events_count: 'Termine/Ereignisse',
            no_scheduled_events: 'Keine anstehenden Termine geplant.',
            month_view: 'Monat',
            week_view: 'Woche',
            list_view: 'Liste',

            // Statuses
            status_read: 'Gelesen',
            status_unread: 'Ungelesen',
            status_replied: 'Beantwortet',
            status_answered: 'Angenommen',
            status_missed: 'Verpasst',
            status_busy: 'Besetzt',
            status_resolved: 'Gelöst',
            status_closed: 'Geschlossen',
            status_open: 'Offen',
            customer_fallback: 'Kunde',
            cancel: 'Abbrechen',
            save: 'Speichern',
            processing: 'Wird verarbeitet...',
            success_saved: 'Vorgang erfolgreich gespeichert!',
            complete_action: 'Vorgang abschließen',

            // Analytics View
            performance_analysis: 'Leistungsanalyse',
            analytics_subtitle: 'Detaillierte Statistiken und Berichte',
            monthly_interaction: 'Monatliches Interaktionsvolumen',
            appointment_distribution: 'Terminverteilung',
            conversion_rate: 'Konversionsrate',
            data_loading: 'Daten werden geladen...',
            retry: 'Erneut versuchen',

            // Satisfaction View
            satisfaction_title: 'Zufriedenheit',
            satisfaction_subtitle: 'Ihr Feedback ist uns wichtig',
            overall_satisfaction: 'Gesamtzufriedenheit',
            recent_feedbacks: 'Ihre letzten Rückmeldungen',
            send_new_feedback: 'Neues Feedback senden',
            new_feedback_title: 'Neues Feedback',
            rate_service: 'Bewerten Sie unseren Service',
            your_thoughts: 'Ihre Gedanken',
            feedback_placeholder: 'Sie können Meinungen, Vorschläge oder Beschwerden zu unserem Service schreiben...',
            cancel: 'Abbrechen',
            send: 'Senden',
            sending: 'Senden...',
            feedback_success: 'Ihr Feedback wurde erfolgreich übermittelt. Vielen Dank!',
            feedback_success_title: 'Feedback erhalten',
            system_error: 'Systemfehler',
            feedback_error: 'Beim Senden des Feedbacks ist ein Fehler aufgetreten'
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

    /**
     * Localized string getter
     * Handles both single localization objects {tr: '', en: ''} 
     * and arrays of such objects (useful for chart labels)
     */
    const tLoc = (obj) => {
        if (!obj) return ''
        if (typeof obj === 'string') return obj
        if (Array.isArray(obj)) return obj.map(item => tLoc(item))
        return obj[currentLocale.value] || obj['tr'] || ''
    }

    // Computed Data exposure
    const stats = computed(() => currentSector.value.stats)
    const quickActions = computed(() => currentSector.value.quickActions)
    const chartConfig = computed(() => {
        const raw = currentSector.value.chartConfig || currentSector.value.chart
        if (!raw) return null
        return {
            ...raw,
            title: tLoc(raw.title),
            subtitle: tLoc(raw.subtitle),
            labels: tLoc(raw.labels) || []
        }
    })

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
        tLoc,
        currentLocale,
        setLocale
    }
})
