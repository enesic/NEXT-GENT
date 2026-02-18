
// Sector-Specific Theme and Data Configuration
// This file defines the look, feel, and default data for each industry sector.

export const sectorThemes = {
    medical: {
        id: 'medical',
        label: 'Sağlık',
        colors: {
            primary: '#0ea5e9', // Sky 500
            secondary: '#0f766e', // Teal 700
            accent: '#38bdf8', // Sky 400
            background: '#030303',
            surface: 'rgba(255, 255, 255, 0.03)',
            text: '#e2e8f0', // Light slate for dark bg
            gradient: 'linear-gradient(135deg, #0ea5e9 0%, #0f766e 100%)',
            sidebar: 'linear-gradient(180deg, #030303 0%, #0a0a0a 100%)',
            cardShadow: '0 4px 6px -1px rgba(14, 165, 233, 0.1), 0 2px 4px -1px rgba(14, 165, 233, 0.06)'
        },
        stats: [
            { label: 'Bugünkü Randevular', value: '124', change: 5.2, icon: 'Calendar', color: 'primary' },
            { label: 'Aktif Hastalar', value: '1,284', change: 2.1, icon: 'Users', color: 'accent' },
            { label: 'Acil Durumlar', value: '3', change: -10.5, icon: 'AlertCircle', color: 'red' },
            { label: 'Müşteri Memnuniyeti', value: '98%', change: 1.2, icon: 'Heart', color: 'secondary' }
        ],
        quickActions: [
            { label: 'Randevu Ekle', icon: 'CalendarPlus', nav: 'appointments' },
            { label: 'Hasta Kaydı', icon: 'UserPlus', nav: 'dashboard' },
            { label: 'Reçete Yaz', icon: 'FileText', nav: 'documents' },
            { label: 'Lab Sonuçları', icon: 'Activity', nav: 'documents' }
        ],
        chart: {
            title: 'Hasta Trafiği',
            subtitle: 'Poliklinik yoğunluğu',
            labels: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
            datasets: [
                { label: 'Muayene', data: [45, 52, 38, 65, 74, 55, 20] },
                { label: 'Acil', data: [12, 15, 8, 22, 18, 25, 35] }
            ]
        }
    },
    legal: {
        id: 'legal',
        label: 'Hukuk',
        colors: {
            primary: '#818cf8', // Indigo 400 (lighter for dark bg)
            secondary: '#fbbf24', // Amber 400
            accent: '#d97706', // Amber 600
            background: '#030303',
            surface: 'rgba(255, 255, 255, 0.03)',
            text: '#e2e8f0', // Light slate for dark bg
            gradient: 'linear-gradient(135deg, #818cf8 0%, #6366f1 100%)',
            sidebar: 'linear-gradient(180deg, #030303 0%, #0a0a0a 100%)',
            cardShadow: '0 4px 6px -1px rgba(129, 140, 248, 0.1), 0 2px 4px -1px rgba(129, 140, 248, 0.06)'
        },
        stats: [
            { label: 'Aktif Davalar', value: '42', change: 1.5, icon: 'Briefcase', color: 'primary' },
            { label: 'Yaklaşan Duruşmalar', value: '8', change: 0, icon: 'Gavel', color: 'secondary' },
            { label: 'Yeni Müvekkiller', value: '12', change: 8.4, icon: 'UserPlus', color: 'accent' },
            { label: 'Faturalandırılan Saat', value: '145s', change: 12.3, icon: 'Clock', color: 'green' }
        ],
        quickActions: [
            { label: 'Dava Aç', icon: 'Gavel', nav: 'documents' },
            { label: 'Müvekkil Ekle', icon: 'UserPlus', nav: 'dashboard' },
            { label: 'Belge Yükle', icon: 'Upload', nav: 'documents' },
            { label: 'Zaman Gir', icon: 'Clock', nav: 'calendar' }
        ],
        chart: {
            title: 'Dava Yükü',
            subtitle: 'Tamamlanan vs Devam Eden',
            labels: ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz'],
            datasets: [
                { label: 'Tamamlanan', data: [10, 15, 12, 18, 20, 25] },
                { label: 'Yeni Açılan', data: [12, 18, 15, 22, 24, 20] }
            ]
        }
    },
    real_estate: {
        id: 'real_estate',
        label: 'Emlak',
        colors: {
            primary: '#10b981', // Emerald 500
            secondary: '#fbbf24', // Yellow 400
            accent: '#34d399', // Emerald 400
            background: '#030303',
            surface: 'rgba(255, 255, 255, 0.03)',
            text: '#e2e8f0', // Light slate for dark bg
            gradient: 'linear-gradient(135deg, #047857 0%, #059669 100%)',
            sidebar: 'linear-gradient(180deg, #030303 0%, #0a0a0a 100%)',
            cardShadow: '0 4px 6px -1px rgba(4, 120, 87, 0.1), 0 2px 4px -1px rgba(4, 120, 87, 0.06)'
        },
        stats: [
            { label: 'Satılık Portföy', value: '156', change: 3.2, icon: 'Home', color: 'primary' },
            { label: 'Kiralık Portföy', value: '89', change: -1.5, icon: 'Key', color: 'accent' },
            { label: 'Bu Ay Satılan', value: '12', change: 24.0, icon: 'DollarSign', color: 'secondary' },
            { label: 'Yeni Talepler', value: '45', change: 15.6, icon: 'MessageCircle', color: 'green' }
        ],
        quickActions: [
            { label: 'İlan Ekle', icon: 'PlusCircle', nav: 'documents' },
            { label: 'Randevu Oluştur', icon: 'Calendar', nav: 'appointments' },
            { label: 'Sözleşme Hazırla', icon: 'FileText', nav: 'documents' },
            { label: 'Müşteri Ekle', icon: 'UserPlus', nav: 'dashboard' }
        ],
        chart: {
            title: 'Satış Performansı',
            subtitle: 'Aylık işlem hacmi',
            labels: ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz'],
            datasets: [
                { label: 'Satış', data: [5, 8, 12, 10, 15, 18] },
                { label: 'Kiralama', data: [20, 25, 30, 28, 35, 40] }
            ]
        }
    },
    finance: {
        id: 'finance',
        label: 'Finans',
        colors: {
            primary: '#a78bfa', // Violet 400
            secondary: '#34d399', // Emerald 400
            accent: '#6ee7b7', // Emerald 300
            background: '#030303',
            surface: 'rgba(255, 255, 255, 0.03)',
            text: '#e2e8f0', // Light slate for dark bg
            gradient: 'linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%)',
            sidebar: 'linear-gradient(180deg, #030303 0%, #0a0a0a 100%)',
            cardShadow: '0 4px 6px -1px rgba(167, 139, 250, 0.1), 0 2px 4px -1px rgba(167, 139, 250, 0.06)'
        },
        stats: [
            { label: 'Toplam Varlık', value: '₺8.4M', change: 12.5, icon: 'Wallet', color: 'primary' },
            { label: 'Aylık Gelir', value: '₺450K', change: 8.2, icon: 'TrendingUp', color: 'secondary' },
            { label: 'Giderler', value: '₺120K', change: -3.1, icon: 'TrendingDown', color: 'red' },
            { label: 'Net Kar', value: '₺330K', change: 15.4, icon: 'PieChart', color: 'green' }
        ],
        quickActions: [
            { label: 'Transfer Yap', icon: 'ArrowRight', nav: 'documents' },
            { label: 'Fatura Kes', icon: 'FileText', nav: 'documents' },
            { label: 'Rapor Al', icon: 'BarChart3', nav: 'analytics' },
            { label: 'Kur Ekle', icon: 'DollarSign', nav: 'dashboard' }
        ],
        chart: {
            title: 'Nakit Akışı',
            subtitle: 'Gelir ve Gider Dengesi',
            labels: ['Q1', 'Q2', 'Q3', 'Q4'],
            datasets: [
                { label: 'Gelir', data: [300, 450, 400, 500] },
                { label: 'Gider', data: [100, 120, 150, 130] }
            ]
        }
    },
    technology: {
        id: 'technology',
        label: 'Teknoloji',
        colors: {
            primary: '#818cf8', // Indigo 400
            secondary: '#a78bfa', // Violet 400
            accent: '#c084fc', // Purple 400
            background: '#030303',
            surface: 'rgba(255, 255, 255, 0.03)',
            text: '#e2e8f0', // Light slate for dark bg
            gradient: 'linear-gradient(135deg, #818cf8 0%, #a78bfa 100%)',
            sidebar: 'linear-gradient(180deg, #030303 0%, #0a0a0a 100%)',
            cardShadow: '0 4px 6px -1px rgba(129, 140, 248, 0.1), 0 2px 4px -1px rgba(129, 140, 248, 0.06)'
        },
        stats: [
            { label: 'Aktif Kullanıcı', value: '25.4K', change: 18.2, icon: 'Users', color: 'primary' },
            { label: 'Sunucu İşlemcisi', value: '45%', change: 5.1, icon: 'Cpu', color: 'secondary' },
            { label: 'API İstekleri', value: '1.2M', change: 24.5, icon: 'Zap', color: 'accent' },
            { label: 'Uptime', value: '99.9%', change: 0, icon: 'Server', color: 'green' }
        ],
        quickActions: [
            { label: 'Dağıtım Yap', icon: 'Rocket', nav: 'dashboard' },
            { label: 'Logları İncele', icon: 'FileCode', nav: 'documents' },
            { label: 'Kullanıcı Yönet', icon: 'UserCog', nav: 'settings' },
            { label: 'Yedekle', icon: 'Database', nav: 'settings' }
        ],
        chart: {
            title: 'Sistem Yükü',
            subtitle: 'Sunucu Kaynak Kullanımı',
            labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
            datasets: [
                { label: 'CPU', data: [20, 25, 45, 60, 55, 30] },
                { label: 'Memory', data: [40, 42, 45, 50, 48, 45] }
            ]
        }
    },
    beauty: {
        id: 'beauty',
        label: 'Güzellik',
        colors: {
            primary: '#f472b6', // Pink 400
            secondary: '#fb923c', // Orange 400
            accent: '#e879f9', // Fuchsia 400
            background: '#030303',
            surface: 'rgba(255, 255, 255, 0.03)',
            text: '#e2e8f0',
            gradient: 'linear-gradient(135deg, #f472b6 0%, #e879f9 100%)',
            sidebar: 'linear-gradient(180deg, #030303 0%, #0a0a0a 100%)',
            cardShadow: '0 4px 6px -1px rgba(244, 114, 182, 0.1), 0 2px 4px -1px rgba(244, 114, 182, 0.06)'
        },
        stats: [
            { label: 'Bugünkü Randevular', value: '28', change: 12.5, icon: 'Calendar', color: 'primary' },
            { label: 'Aktif Müşteriler', value: '856', change: 5.3, icon: 'Users', color: 'accent' },
            { label: 'Memnuniyet', value: '96%', change: 2.1, icon: 'Heart', color: 'secondary' },
            { label: 'Aylık Gelir', value: '₺145K', change: 8.7, icon: 'TrendingUp', color: 'green' }
        ],
        quickActions: [
            { label: 'Randevu Ekle', icon: 'CalendarPlus', nav: 'appointments' },
            { label: 'Müşteri Kaydı', icon: 'UserPlus', nav: 'dashboard' },
            { label: 'Hizmet Listesi', icon: 'FileText', nav: 'documents' },
            { label: 'Mesajlar', icon: 'MessageSquare', nav: 'messages' }
        ],
        chart: {
            title: 'Randevu Trafiği',
            subtitle: 'Haftalık doluluk oranı',
            labels: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
            datasets: [
                { label: 'Randevu', data: [18, 22, 25, 30, 35, 40, 10] },
                { label: 'İptal', data: [2, 3, 1, 4, 2, 5, 1] }
            ]
        }
    }
};

export default sectorThemes;
