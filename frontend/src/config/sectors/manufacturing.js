export const manufacturing = {
    id: 'manufacturing',
    label: { tr: 'Üretim', en: 'Manufacturing', de: 'Produktion' },
    colors: {
        primary: '#64748b', secondary: '#334155', accent: '#94a3b8',
        background: '#0d0d0f', surface: 'rgba(255, 255, 255, 0.03)', text: '#f8fafc',
        gradient: 'linear-gradient(135deg, #64748b 0%, #334155 100%)',
        sidebar: 'linear-gradient(180deg, #0d0d0f 0%, #15151a 100%)',
        cardShadow: '0 4px 6px -1px rgba(100, 116, 139, 0.1), 0 2px 4px -1px rgba(100, 116, 139, 0.06)'
    },
    stats: [
        { label: { tr: 'Kapasite', en: 'Capacity', de: 'Kapazität' }, value: '92%', change: 3.5, icon: 'Activity', color: 'primary' },
        { label: { tr: 'Siparişler', en: 'Orders', de: 'Bestellungen' }, value: '67', change: 8.2, icon: 'Users', color: 'accent' },
        { label: { tr: 'Teslim Bekleyen', en: 'Pending Delivery', de: 'Ausstehende Lieferung' }, value: '14', change: -2.1, icon: 'AlertCircle', color: 'red' },
        { label: { tr: 'Aylık Üretim', en: 'Monthly Prod', de: 'Monatl. Prod' }, value: '4,200', change: 6.4, icon: 'TrendingUp', color: 'green' }
    ],
    quickActions: [
        {
            label: { tr: 'Sipariş Ekle', en: 'Add Order', de: 'Bestellung hinzu' }, icon: 'CalendarPlus', nav: 'appointments',
            fields: [
                { key: 'order_id', label: { tr: 'Sipariş No', en: 'Order ID', de: 'Bestellung ID' }, type: 'text' },
                { key: 'qty', label: { tr: 'Miktar', en: 'Qty', de: 'Menge' }, type: 'number' }
            ]
        },
        {
            label: { tr: 'İş Emri', en: 'Work Order', de: 'Arbeitsauftrag' }, icon: 'FileText', nav: 'documents',
            fields: [
                { key: 'task', label: { tr: 'Görev', en: 'Task', de: 'Aufgabe' }, type: 'text' }
            ]
        },
        { label: { tr: 'Stok Kontrol', en: 'Inv Check', de: 'Bestandsprüfung' }, icon: 'Activity', nav: 'analytics' },
        { label: { tr: 'Mesajlar', en: 'Messages', de: 'Nachrichten' }, icon: 'MessageSquare', nav: 'messages' }
    ],
    chart: {
        title: { tr: 'Üretim Analizi', en: 'Production Analysis', de: 'Produktionsanalyse' },
        subtitle: { tr: 'Haftalık üretim', en: 'Weekly production', de: 'Wöchentliche Produktion' },
        labels: {
            tr: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
            en: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            de: ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
        },
        datasets: [
            { label: { tr: 'Üretilen', en: 'Produced', de: 'Produziert' }, data: [800, 850, 900, 780, 950, 600, 200] },
            { label: { tr: 'Hedef', en: 'Target', de: 'Ziel' }, data: [800, 800, 800, 800, 800, 600, 200] }
        ]
    }
}
