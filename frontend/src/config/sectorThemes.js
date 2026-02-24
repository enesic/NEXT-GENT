
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
            primary: '#f472b6',
            secondary: '#fb923c',
            accent: '#e879f9',
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
            { label: 'Memnuniyet', value: '96%', change: 2.1, icon: 'Heart', color: 'primary' },
            { label: 'Aylık Gelir', value: '₺145K', change: 8.7, icon: 'TrendingUp', color: 'green' }
        ],
        quickActions: [
            { label: 'Randevu Ekle', icon: 'CalendarPlus', nav: 'appointments' },
            { label: 'Müşteri Kaydı', icon: 'UserPlus', nav: 'dashboard' },
            { label: 'Hizmet Listesi', icon: 'FileText', nav: 'documents' },
            { label: 'Mesajlar', icon: 'MessageSquare', nav: 'messages' }
        ],
        services: [
            { id: 1, name: 'Cilt Bakımı', price: '₺850', duration: '60 dk', icon: 'Sparkles', description: 'Derinlemesine temizlik ve nemlendirme' },
            { id: 2, name: 'Lazer Epilasyon', price: '₺1.200', duration: '45 dk', icon: 'Zap', description: 'Son teknoloji cihazlar ile kalıcı çözüm' },
            { id: 3, name: 'Saç Bakımı', price: '₺600', duration: '90 dk', icon: 'Scissors', description: 'Keratin bakım ve onarıcı maskeler' },
            { id: 4, name: 'Tırnak Tasarımı', price: '₺450', duration: '60 dk', icon: 'Palette', description: 'Protez tırnak ve nail art uygulamaları' },
            { id: 5, name: 'Medikal Masaj', price: '₺950', duration: '50 dk', icon: 'Heart', description: 'Uzman terapistler eşliğinde gevşeme' }
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
    },
    hospitality: {
        id: 'hospitality',
        label: 'Konaklama',
        colors: {
            primary: '#f59e0b',
            secondary: '#d97706',
            accent: '#fbbf24',
            background: '#030303',
            surface: 'rgba(255, 255, 255, 0.03)',
            text: '#e2e8f0',
            gradient: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
            sidebar: 'linear-gradient(180deg, #030303 0%, #0a0a0a 100%)',
            cardShadow: '0 4px 6px -1px rgba(245, 158, 11, 0.1), 0 2px 4px -1px rgba(245, 158, 11, 0.06)'
        },
        stats: [
            { label: 'Doluluk Oranı', value: '87%', change: 5.2, icon: 'Home', color: 'primary' },
            { label: 'Aktif Rezervasyonlar', value: '142', change: 3.1, icon: 'Calendar', color: 'accent' },
            { label: 'Müşteri Memnuniyeti', value: '94%', change: 1.4, icon: 'Heart', color: 'secondary' },
            { label: 'Aylık Gelir', value: '₺580K', change: 11.2, icon: 'TrendingUp', color: 'green' }
        ],
        quickActions: [
            { label: 'Rezervasyon Ekle', icon: 'CalendarPlus', nav: 'appointments' },
            { label: 'Misafir Kaydı', icon: 'UserPlus', nav: 'dashboard' },
            { label: 'Oda Durumu', icon: 'Home', nav: 'documents' },
            { label: 'Mesajlar', icon: 'MessageSquare', nav: 'messages' }
        ],
        chart: {
            title: 'Doluluk Analizi',
            subtitle: 'Haftalık rezervasyon oranı',
            labels: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
            datasets: [
                { label: 'Rezervasyon', data: [70, 75, 80, 85, 90, 95, 88] },
                { label: 'İptal', data: [5, 3, 4, 2, 6, 3, 4] }
            ]
        }
    },
    automotive: {
        id: 'automotive',
        label: 'Otomotiv',
        colors: {
            primary: '#ef4444',
            secondary: '#f97316',
            accent: '#fb923c',
            background: '#030303',
            surface: 'rgba(255, 255, 255, 0.03)',
            text: '#e2e8f0',
            gradient: 'linear-gradient(135deg, #ef4444 0%, #f97316 100%)',
            sidebar: 'linear-gradient(180deg, #030303 0%, #0a0a0a 100%)',
            cardShadow: '0 4px 6px -1px rgba(239, 68, 68, 0.1), 0 2px 4px -1px rgba(239, 68, 68, 0.06)'
        },
        stats: [
            { label: 'Aktif Servisler', value: '38', change: 4.2, icon: 'Activity', color: 'primary' },
            { label: 'Araç Sayısı', value: '214', change: 2.8, icon: 'Users', color: 'accent' },
            { label: 'Teslim Bekleyen', value: '12', change: -3.5, icon: 'AlertCircle', color: 'red' },
            { label: 'Aylık Ciro', value: '₺320K', change: 9.1, icon: 'TrendingUp', color: 'green' }
        ],
        quickActions: [
            { label: 'Servis Ekle', icon: 'CalendarPlus', nav: 'appointments' },
            { label: 'Müşteri Kaydı', icon: 'UserPlus', nav: 'dashboard' },
            { label: 'İş Emri', icon: 'FileText', nav: 'documents' },
            { label: 'Mesajlar', icon: 'MessageSquare', nav: 'messages' }
        ],
        chart: {
            title: 'Servis Trafiği',
            subtitle: 'Haftalık araç girişi',
            labels: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
            datasets: [
                { label: 'Giriş', data: [12, 15, 10, 18, 20, 8, 3] },
                { label: 'Çıkış', data: [10, 13, 12, 15, 18, 10, 2] }
            ]
        }
    },
    manufacturing: {
        id: 'manufacturing',
        label: 'Üretim',
        colors: {
            primary: '#6366f1',
            secondary: '#8b5cf6',
            accent: '#a78bfa',
            background: '#030303',
            surface: 'rgba(255, 255, 255, 0.03)',
            text: '#e2e8f0',
            gradient: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
            sidebar: 'linear-gradient(180deg, #030303 0%, #0a0a0a 100%)',
            cardShadow: '0 4px 6px -1px rgba(99, 102, 241, 0.1), 0 2px 4px -1px rgba(99, 102, 241, 0.06)'
        },
        stats: [
            { label: 'Üretim Kapasitesi', value: '92%', change: 3.5, icon: 'Activity', color: 'primary' },
            { label: 'Aktif Siparişler', value: '67', change: 8.2, icon: 'Users', color: 'accent' },
            { label: 'Bekleyen Teslimat', value: '14', change: -2.1, icon: 'AlertCircle', color: 'red' },
            { label: 'Aylık Üretim', value: '4,200', change: 6.4, icon: 'TrendingUp', color: 'green' }
        ],
        quickActions: [
            { label: 'Sipariş Ekle', icon: 'CalendarPlus', nav: 'appointments' },
            { label: 'İş Emri', icon: 'FileText', nav: 'documents' },
            { label: 'Stok Kontrol', icon: 'Activity', nav: 'analytics' },
            { label: 'Mesajlar', icon: 'MessageSquare', nav: 'messages' }
        ],
        chart: {
            title: 'Üretim Analizi',
            subtitle: 'Haftalık üretim miktarı',
            labels: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
            datasets: [
                { label: 'Üretilen', data: [800, 850, 900, 780, 950, 600, 200] },
                { label: 'Hedef', data: [800, 800, 800, 800, 800, 600, 200] }
            ]
        }
    },
    education: {
        id: 'education',
        label: 'Eğitim',
        colors: {
            primary: '#3b82f6',
            secondary: '#06b6d4',
            accent: '#38bdf8',
            background: '#030303',
            surface: 'rgba(255, 255, 255, 0.03)',
            text: '#e2e8f0',
            gradient: 'linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%)',
            sidebar: 'linear-gradient(180deg, #030303 0%, #0a0a0a 100%)',
            cardShadow: '0 4px 6px -1px rgba(59, 130, 246, 0.1), 0 2px 4px -1px rgba(59, 130, 246, 0.06)'
        },
        stats: [
            { label: 'Aktif Öğrenciler', value: '1,245', change: 12.3, icon: 'Users', color: 'primary' },
            { label: 'Aktif Kurslar', value: '48', change: 5.1, icon: 'Calendar', color: 'accent' },
            { label: 'Tamamlanan', value: '312', change: 8.7, icon: 'CheckCircle', color: 'green' },
            { label: 'Memnuniyet', value: '97%', change: 1.2, icon: 'Heart', color: 'secondary' }
        ],
        quickActions: [
            { label: 'Ders Ekle', icon: 'CalendarPlus', nav: 'appointments' },
            { label: 'Öğrenci Kaydı', icon: 'UserPlus', nav: 'dashboard' },
            { label: 'Materyal', icon: 'FileText', nav: 'documents' },
            { label: 'Mesajlar', icon: 'MessageSquare', nav: 'messages' }
        ],
        chart: {
            title: 'Katılım Analizi',
            subtitle: 'Haftalık ders katılımı',
            labels: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
            datasets: [
                { label: 'Katılım', data: [220, 250, 230, 280, 260, 100, 50] },
                { label: 'Hedef', data: [250, 250, 250, 250, 250, 150, 50] }
            ]
        }
    },
    retail: {
        id: 'retail',
        label: 'Perakende',
        colors: {
            primary: '#22c55e',
            secondary: '#16a34a',
            accent: '#4ade80',
            background: '#030303',
            surface: 'rgba(255, 255, 255, 0.03)',
            text: '#e2e8f0',
            gradient: 'linear-gradient(135deg, #22c55e 0%, #16a34a 100%)',
            sidebar: 'linear-gradient(180deg, #030303 0%, #0a0a0a 100%)',
            cardShadow: '0 4px 6px -1px rgba(34, 197, 94, 0.1), 0 2px 4px -1px rgba(34, 197, 94, 0.06)'
        },
        stats: [
            { label: 'Günlük Satış', value: '₺85K', change: 7.3, icon: 'TrendingUp', color: 'primary' },
            { label: 'Müşteri Sayısı', value: '324', change: 4.5, icon: 'Users', color: 'accent' },
            { label: 'Sepet Ortalaması', value: '₺262', change: 2.8, icon: 'Activity', color: 'secondary' },
            { label: 'Stok Uyarısı', value: '7', change: -15.0, icon: 'AlertCircle', color: 'red' }
        ],
        quickActions: [
            { label: 'Ürün Ekle', icon: 'PlusCircle', nav: 'documents' },
            { label: 'Sipariş Al', icon: 'CalendarPlus', nav: 'appointments' },
            { label: 'Stok Kontrol', icon: 'FileText', nav: 'documents' },
            { label: 'Mesajlar', icon: 'MessageSquare', nav: 'messages' }
        ],
        chart: {
            title: 'Satış Analizi',
            subtitle: 'Haftalık satış trendi',
            labels: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
            datasets: [
                { label: 'Satış (₺)', data: [60, 75, 65, 80, 95, 120, 85] },
                { label: 'Hedef (₺)', data: [70, 70, 70, 70, 80, 100, 80] }
            ]
        }
    },
    ecommerce: {
        id: 'ecommerce',
        label: 'E-Ticaret',
        colors: {
            primary: '#f97316',
            secondary: '#ea580c',
            accent: '#fb923c',
            background: '#030303',
            surface: 'rgba(255, 255, 255, 0.03)',
            text: '#e2e8f0',
            gradient: 'linear-gradient(135deg, #f97316 0%, #ea580c 100%)',
            sidebar: 'linear-gradient(180deg, #030303 0%, #0a0a0a 100%)',
            cardShadow: '0 4px 6px -1px rgba(249, 115, 22, 0.1), 0 2px 4px -1px rgba(249, 115, 22, 0.06)'
        },
        stats: [
            { label: 'Günlük Sipariş', value: '1,284', change: 18.2, icon: 'TrendingUp', color: 'primary' },
            { label: 'Aktif Müşteri', value: '25.4K', change: 5.3, icon: 'Users', color: 'accent' },
            { label: 'Kargo Bekleyen', value: '342', change: 3.1, icon: 'Activity', color: 'secondary' },
            { label: 'Dönüşüm Oranı', value: '3.2%', change: 0.8, icon: 'Heart', color: 'green' }
        ],
        quickActions: [
            { label: 'Sipariş Oluştur', icon: 'CalendarPlus', nav: 'appointments' },
            { label: 'Ürün Ekle', icon: 'PlusCircle', nav: 'documents' },
            { label: 'Kargo Takip', icon: 'Activity', nav: 'analytics' },
            { label: 'Kampanya', icon: 'Tag', nav: 'messages' }
        ],
        chart: {
            title: 'Sipariş Analizi',
            subtitle: 'Günlük sipariş trendi',
            labels: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
            datasets: [
                { label: 'Siparişler', data: [980, 1100, 1050, 1200, 1350, 1500, 1100] },
                { label: 'İadeler', data: [45, 52, 38, 65, 74, 55, 40] }
            ]
        }
    }
};

export default sectorThemes;
