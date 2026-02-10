
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
            background: '#f0f9ff', // Sky 50
            surface: '#ffffff',
            text: '#0f172a',
            gradient: 'linear-gradient(135deg, #0ea5e9 0%, #0f766e 100%)',
            sidebar: 'linear-gradient(180deg, #f0f9ff 0%, #e0f2fe 100%)',
            cardShadow: '0 4px 6px -1px rgba(14, 165, 233, 0.1), 0 2px 4px -1px rgba(14, 165, 233, 0.06)'
        },
        stats: [
            { label: 'Bugünkü Randevular', value: '124', change: 5.2, icon: 'Calendar', color: 'primary' },
            { label: 'Aktif Hastalar', value: '1,284', change: 2.1, icon: 'Users', color: 'accent' },
            { label: 'Acil Durumlar', value: '3', change: -10.5, icon: 'AlertCircle', color: 'red' },
            { label: 'Müşteri Memnuniyeti', value: '98%', change: 1.2, icon: 'Heart', color: 'secondary' }
        ],
        quickActions: [
            { label: 'Randevu Ekle', icon: 'CalendarPlus' },
            { label: 'Hasta Kaydı', icon: 'UserPlus' },
            { label: 'Reçete Yaz', icon: 'FileText' },
            { label: 'Lab Sonuçları', icon: 'Activity' }
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
            primary: '#1e3a8a', // Blue 900
            secondary: '#b45309', // Amber 700
            accent: '#d97706', // Amber 600
            background: '#f8fafc', // Slate 50
            surface: '#ffffff',
            text: '#1e293b',
            gradient: 'linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%)',
            sidebar: 'linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%)',
            cardShadow: '0 4px 6px -1px rgba(30, 58, 138, 0.1), 0 2px 4px -1px rgba(30, 58, 138, 0.06)'
        },
        stats: [
            { label: 'Aktif Davalar', value: '42', change: 1.5, icon: 'Briefcase', color: 'primary' },
            { label: 'Yaklaşan Duruşmalar', value: '8', change: 0, icon: 'Gavel', color: 'secondary' },
            { label: 'Yeni Müvekkiller', value: '12', change: 8.4, icon: 'UserPlus', color: 'accent' },
            { label: 'Faturalandırılan Saat', value: '145s', change: 12.3, icon: 'Clock', color: 'green' }
        ],
        quickActions: [
            { label: 'Dava Aç', icon: 'Gavel' },
            { label: 'Müvekkil Ekle', icon: 'UserPlus' },
            { label: 'Belge Yükle', icon: 'Upload' },
            { label: 'Zaman Gir', icon: 'Clock' }
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
            primary: '#047857', // Emerald 700
            secondary: '#a16207', // Yellow 700
            accent: '#10b981', // Emerald 500
            background: '#f0fdf4', // Emerald 50
            surface: '#ffffff',
            text: '#064e3b',
            gradient: 'linear-gradient(135deg, #047857 0%, #059669 100%)',
            sidebar: 'linear-gradient(180deg, #f0fdf4 0%, #dcfce7 100%)',
            cardShadow: '0 4px 6px -1px rgba(4, 120, 87, 0.1), 0 2px 4px -1px rgba(4, 120, 87, 0.06)'
        },
        stats: [
            { label: 'Satılık Portföy', value: '156', change: 3.2, icon: 'Home', color: 'primary' },
            { label: 'Kiralık Portföy', value: '89', change: -1.5, icon: 'Key', color: 'accent' },
            { label: 'Bu Ay Satılan', value: '12', change: 24.0, icon: 'DollarSign', color: 'secondary' },
            { label: 'Yeni Talepler', value: '45', change: 15.6, icon: 'MessageCircle', color: 'green' }
        ],
        quickActions: [
            { label: 'İlan Ekle', icon: 'PlusCircle' },
            { label: 'Randevu Oluştur', icon: 'Calendar' },
            { label: 'Sözleşme Hazırla', icon: 'FileText' },
            { label: 'Müşteri Ekle', icon: 'UserPlus' }
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
            primary: '#111827', // Gray 900
            secondary: '#059669', // Emerald 600
            accent: '#34d399', // Emerald 400
            background: '#f9fafb', // Gray 50
            surface: '#ffffff',
            text: '#111827',
            gradient: 'linear-gradient(135deg, #111827 0%, #374151 100%)',
            sidebar: 'linear-gradient(180deg, #f9fafb 0%, #e5e7eb 100%)',
            cardShadow: '0 4px 6px -1px rgba(17, 24, 39, 0.1), 0 2px 4px -1px rgba(17, 24, 39, 0.06)'
        },
        stats: [
            { label: 'Toplam Varlık', value: '₺8.4M', change: 12.5, icon: 'Wallet', color: 'primary' },
            { label: 'Aylık Gelir', value: '₺450K', change: 8.2, icon: 'TrendingUp', color: 'secondary' },
            { label: 'Giderler', value: '₺120K', change: -3.1, icon: 'TrendingDown', color: 'red' },
            { label: 'Net Kar', value: '₺330K', change: 15.4, icon: 'PieChart', color: 'green' }
        ],
        quickActions: [
            { label: 'Transfer Yap', icon: 'ArrowRight' },
            { label: 'Fatura Kes', icon: 'FileText' },
            { label: 'Rapor Al', icon: 'BarChart3' },
            { label: 'Kur Ekle', icon: 'DollarSign' }
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
            primary: '#6366f1', // Indigo 500
            secondary: '#8b5cf6', // Violet 500
            accent: '#a855f7', // Purple 500
            background: '#faf5ff', // Purple 50
            surface: '#ffffff',
            text: '#4c1d95',
            gradient: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
            sidebar: 'linear-gradient(180deg, #faf5ff 0%, #f3e8ff 100%)',
            cardShadow: '0 4px 6px -1px rgba(99, 102, 241, 0.1), 0 2px 4px -1px rgba(99, 102, 241, 0.06)'
        },
        stats: [
            { label: 'Aktif Kullanıcı', value: '25.4K', change: 18.2, icon: 'Users', color: 'primary' },
            { label: 'Sunucu İşlemcisi', value: '45%', change: 5.1, icon: 'Cpu', color: 'secondary' },
            { label: 'API İstekleri', value: '1.2M', change: 24.5, icon: 'Zap', color: 'accent' },
            { label: 'Uptime', value: '99.9%', change: 0, icon: 'Server', color: 'green' }
        ],
        quickActions: [
            { label: 'Dağıtım Yap', icon: 'Rocket' },
            { label: 'Logları İncele', icon: 'FileCode' },
            { label: 'Kullanıcı Yönet', icon: 'UserCog' },
            { label: 'Yedekle', icon: 'Database' }
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
    }
};

export default sectorThemes;
