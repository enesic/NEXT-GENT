export const ecommerce = {
    id: 'ecommerce',
    label: { tr: 'E-Ticaret', en: 'E-Commerce', de: 'E-Commerce' },
    colors: {
        primary: '#f59e0b', secondary: '#c2410c', accent: '#fbbf24',
        background: '#0a0a05', surface: 'rgba(255, 255, 255, 0.03)', text: '#fef3c7',
        gradient: 'linear-gradient(135deg, #f59e0b 0%, #c2410c 100%)',
        sidebar: 'linear-gradient(180deg, #0a0a05 0%, #171708 100%)',
        cardShadow: '0 4px 6px -1px rgba(245, 158, 11, 0.1), 0 2px 4px -1px rgba(245, 158, 11, 0.06)'
    },
    stats: [
        { label: { tr: 'Günlük Sipariş', en: 'Daily Orders', de: 'Tagesbestellungen' }, value: '1,284', change: 18.2, icon: 'TrendingUp', color: 'primary' },
        { label: { tr: 'Aktif Müşteri', en: 'Active Customers', de: 'Aktive Kunden' }, value: '25.4K', change: 5.3, icon: 'Users', color: 'accent' },
        { label: { tr: 'Kargo Bekleyen', en: 'Pending Shipments', de: 'Ausstehende Sendungen' }, value: '342', change: 3.1, icon: 'Activity', color: 'secondary' },
        { label: { tr: 'Dönüşüm Oranı', en: 'Conversion Rate', de: 'Konversionsrate' }, value: '3.2%', change: 0.8, icon: 'Heart', color: 'green' }
    ],
    quickActions: [
        {
            label: { tr: 'Sipariş Oluştur', en: 'Create Order', de: 'Bestellung anlegen' }, icon: 'CalendarPlus', nav: 'appointments',
            fields: [
                { key: 'customer', label: { tr: 'Müşteri', en: 'Customer', de: 'Kunde' }, type: 'text' },
                { key: 'product', label: { tr: 'Ürün', en: 'Product', de: 'Produkt' }, type: 'text' },
                { key: 'amount', label: { tr: 'Adet', en: 'Quantity', de: 'Menge' }, type: 'number' }
            ]
        },
        {
            label: { tr: 'Ürün Ekle', en: 'Add Product', de: 'Produkt hinzu' }, icon: 'PlusCircle', nav: 'documents',
            fields: [
                { key: 'name', label: { tr: 'Ürün Adı', en: 'Product Name', de: 'Produktname' }, type: 'text' },
                { key: 'price', label: { tr: 'Fiyat', en: 'Price', de: 'Preis' }, type: 'number' }
            ]
        },
        {
            label: { tr: 'Kargo Takip', en: 'Track Shipment', de: 'Sendung verfolgen' }, icon: 'Activity', nav: 'analytics',
            fields: [
                { key: 'track_no', label: { tr: 'Takip No', en: 'Tracking No', de: 'Tracking-Nummer' }, type: 'text' }
            ]
        },
        {
            label: { tr: 'Kampanya', en: 'Campaign', de: 'Kampagne' }, icon: 'Tag', nav: 'messages',
            fields: [
                { key: 'title', label: { tr: 'Kampanya Adı', en: 'Campaign Name', de: 'Kampagnenname' }, type: 'text' },
                { key: 'discount', label: { tr: 'İndirim %', en: 'Discount %', de: 'Rabatt %' }, type: 'number' }
            ]
        }
    ],
    chart: {
        title: { tr: 'Sipariş Analizi', en: 'Order Analysis', de: 'Bestellanalyse' },
        subtitle: { tr: 'Günlük sipariş trendi', en: 'Daily order trend', de: 'Täglicher Bestelltrend' },
        labels: {
            tr: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
            en: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            de: ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
        },
        datasets: [
            { label: { tr: 'Siparişler', en: 'Orders', de: 'Bestellungen' }, data: [980, 1100, 1050, 1200, 1350, 1500, 1100] },
            { label: { tr: 'İadeler', en: 'Returns', de: 'Rücksendungen' }, data: [45, 52, 38, 65, 74, 55, 40] }
        ]
    }
}
