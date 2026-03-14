export const retail = {
    id: 'retail',
    label: { tr: 'Perakende', en: 'Retail', de: 'Einzelhandel' },
    colors: {
        primary: '#8b5cf6', secondary: '#5b21b6', accent: '#a78bfa',
        background: '#08050a', surface: 'rgba(255, 255, 255, 0.03)', text: '#f5f3ff',
        gradient: 'linear-gradient(135deg, #8b5cf6 0%, #5b21b6 100%)',
        sidebar: 'linear-gradient(180deg, #08050a 0%, #14081c 100%)',
        cardShadow: '0 4px 6px -1px rgba(139, 92, 246, 0.1), 0 2px 4px -1px rgba(139, 92, 246, 0.06)'
    },
    stats: [
        { label: { tr: 'Günlük Satış', en: 'Daily Sales', de: 'Tagesumsatz' }, value: '₺85K', change: 7.3, icon: 'TrendingUp', color: 'primary' },
        { label: { tr: 'Müşteri Sayısı', en: 'Customers', de: 'Kunden' }, value: '324', change: 4.5, icon: 'Users', color: 'accent' },
        { label: { tr: 'Sepet Ortalaması', en: 'Avg Basket', de: 'Durchschn. Korb' }, value: '₺262', change: 2.8, icon: 'Activity', color: 'secondary' },
        { label: { tr: 'Stok Uyarısı', en: 'Stock Alert', de: 'Lagerwarnung' }, value: '7', change: -15.0, icon: 'AlertCircle', color: 'red' }
    ],
    quickActions: [
        {
            label: { tr: 'Ürün Ekle', en: 'Add Product', de: 'Produkt hinzu' }, icon: 'PlusCircle', nav: 'documents',
            fields: [
                { key: 'name', label: { tr: 'Ürün', en: 'Product', de: 'Produkt' }, type: 'text' },
                { key: 'stock', label: { tr: 'Stok', en: 'Stock', de: 'Bestand' }, type: 'number' }
            ]
        },
        {
            label: { tr: 'Sipariş Al', en: 'Take Order', de: 'Bestellung aufnehmen' }, icon: 'CalendarPlus', nav: 'appointments',
            fields: [
                { key: 'customer', label: { tr: 'Müşteri', en: 'Customer', de: 'Kunde' }, type: 'text' },
                { key: 'total', label: { tr: 'Toplam', en: 'Total', de: 'Gesamt' }, type: 'number' }
            ]
        },
        { label: { tr: 'Stok Kontrol', en: 'Stock Check', de: 'Bestandsprüfung' }, icon: 'FileText', nav: 'documents' },
        { label: { tr: 'Mesajlar', en: 'Messages', de: 'Nachrichten' }, icon: 'MessageSquare', nav: 'messages' }
    ],
    chart: {
        title: { tr: 'Satış Analizi', en: 'Sales Analysis', de: 'Verkaufsanalyse' },
        subtitle: { tr: 'Haftalık trend', en: 'Weekly trend', de: 'Wöchentlicher Trend' },
        labels: {
            tr: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
            en: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            de: ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
        },
        datasets: [
            { label: { tr: 'Satış', en: 'Sales', de: 'Verkäufe' }, data: [60, 75, 65, 80, 95, 120, 85] },
            { label: { tr: 'Hedef', en: 'Target', de: 'Ziel' }, data: [70, 70, 70, 70, 80, 100, 80] }
        ]
    }
}
