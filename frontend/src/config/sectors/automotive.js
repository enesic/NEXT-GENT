export const automotive = {
    id: 'automotive',
    label: { tr: 'Otomotiv', en: 'Automotive', de: 'Automobil' },
    colors: {
        primary: '#dc2626', secondary: '#991b1b', accent: '#ef4444',
        background: '#080202', surface: 'rgba(255, 255, 255, 0.03)', text: '#fef2f2',
        gradient: 'linear-gradient(135deg, #dc2626 0%, #991b1b 100%)',
        sidebar: 'linear-gradient(180deg, #080202 0%, #140505 100%)',
        cardShadow: '0 4px 6px -1px rgba(220, 38, 38, 0.1), 0 2px 4px -1px rgba(220, 38, 38, 0.06)'
    },
    stats: [
        { label: { tr: 'Aktif Servisler', en: 'Active Services', de: 'Aktive Dienste' }, value: '38', change: 4.2, icon: 'Activity', color: 'primary' },
        { label: { tr: 'Araç Sayısı', en: 'Vehicle Count', de: 'Fahrzeuganzahl' }, value: '214', change: 2.8, icon: 'Users', color: 'accent' },
        { label: { tr: 'Teslim Bekleyen', en: 'Pending Delivery', de: 'Ausstehende Lieferung' }, value: '12', change: -3.5, icon: 'AlertCircle', color: 'red' },
        { label: { tr: 'Aylık Ciro', en: 'Monthly Rev', de: 'Monatlicher Umsatz' }, value: '₺320K', change: 9.1, icon: 'TrendingUp', color: 'green' }
    ],
    quickActions: [
        {
            label: { tr: 'Servis Ekle', en: 'Add Service', de: 'Service hinzufügen' }, icon: 'CalendarPlus', nav: 'appointments',
            fields: [
                { key: 'plate', label: { tr: 'Plaka', en: 'Plate', de: 'Kennzeichen' }, type: 'text' },
                { key: 'type', label: { tr: 'Servis Türü', en: 'Service Type', de: 'Serviceart' }, type: 'text' }
            ]
        },
        {
            label: { tr: 'Müşteri Kaydı', en: 'New Client', de: 'Neuer Kunde' }, icon: 'UserPlus', nav: 'dashboard',
            fields: [
                { key: 'name', label: { tr: 'Ad Soyad', en: 'Name', de: 'Name' }, type: 'text' },
                { key: 'phone', label: { tr: 'Telefon', en: 'Phone', de: 'Telefon' }, type: 'tel' }
            ]
        },
        {
            label: { tr: 'İş Emri', en: 'Work Order', de: 'Arbeitsauftrag' }, icon: 'FileText', nav: 'documents',
            fields: [
                { key: 'desc', label: { tr: 'Açıklama', en: 'Description', de: 'Beschreibung' }, type: 'textarea' }
            ]
        },
        { label: { tr: 'Mesajlar', en: 'Messages', de: 'Nachrichten' }, icon: 'MessageSquare', nav: 'messages' }
    ],
    chart: {
        title: { tr: 'Servis Trafiği', en: 'Service Traffic', de: 'Serviceverkehr' },
        subtitle: { tr: 'Haftalık araç girişi', en: 'Weekly vehicle entry', de: 'Wöchentlicher Fahrzeugeingang' },
        labels: {
            tr: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
            en: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            de: ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
        },
        datasets: [
            { label: { tr: 'Giriş', en: 'Entry', de: 'Eingang' }, data: [12, 15, 10, 18, 20, 8, 3] },
            { label: { tr: 'Çıkış', en: 'Exit', de: 'Ausgang' }, data: [10, 13, 12, 15, 18, 10, 2] }
        ]
    }
}
