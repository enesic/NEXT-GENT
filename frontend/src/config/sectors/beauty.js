export const beauty = {
    id: 'beauty',
    label: { tr: 'Güzellik', en: 'Beauty', de: 'Schönheit' },
    colors: {
        primary: '#ec4899', secondary: '#be185d', accent: '#f472b6',
        background: '#0f050a', surface: 'rgba(255, 255, 255, 0.03)', text: '#fdf2f8',
        gradient: 'linear-gradient(135deg, #ec4899 0%, #be185d 100%)',
        sidebar: 'linear-gradient(180deg, #0f050a 0%, #180812 100%)',
        cardShadow: '0 4px 6px -1px rgba(236, 72, 153, 0.1), 0 2px 4px -1px rgba(236, 72, 153, 0.06)'
    },
    stats: [
        { label: { tr: 'Bugünkü Randevular', en: 'Today Appts', de: 'Heute Termine' }, value: '28', change: 12.5, icon: 'Calendar', color: 'primary' },
        { label: { tr: 'Aktif Müşteriler', en: 'Active Clients', de: 'Aktive Kunden' }, value: '856', change: 5.3, icon: 'Users', color: 'accent' },
        { label: { tr: 'Memnuniyet', en: 'Satisfaction', de: 'Zufriedenheit' }, value: '96%', change: 2.1, icon: 'Heart', color: 'primary' },
        { label: { tr: 'Aylık Gelir', en: 'Monthly Income', de: 'Monatliches Einkommen' }, value: '₺145K', change: 8.7, icon: 'TrendingUp', color: 'green' }
    ],
    quickActions: [
        {
            label: { tr: 'Randevu Ekle', en: 'Add Appt', de: 'Termin hinzufügen' }, icon: 'CalendarPlus', nav: 'appointments',
            fields: [
                { key: 'customer', label: { tr: 'Müşteri', en: 'Customer', de: 'Kunde' }, type: 'text' },
                {
                    key: 'service', label: { tr: 'Hizmet', en: 'Service', de: 'Dienstleistung' }, type: 'select', options: [
                        { value: 'skin', label: { tr: 'Cilt Bakımı', en: 'Skin Care', de: 'Hautpflege' } },
                        { value: 'hair', label: { tr: 'Saç Kesimi', en: 'Haircut', de: 'Haarschnitt' } }
                    ]
                },
                { key: 'date', label: { tr: 'Zaman', en: 'Time', de: 'Zeit' }, type: 'datetime-local' }
            ]
        },
        {
            label: { tr: 'Müşteri Kaydı', en: 'New Client', de: 'Neuer Kunde' }, icon: 'UserPlus', nav: 'dashboard',
            fields: [
                { key: 'name', label: { tr: 'Ad Soyad', en: 'Name', de: 'Name' }, type: 'text' },
                { key: 'phone', label: { tr: 'Telefon', en: 'Phone', de: 'Telefon' }, type: 'tel' }
            ]
        },
        { label: { tr: 'Hizmetler', en: 'Services', de: 'Dienstleistungen' }, icon: 'FileText', nav: 'documents' },
        { label: { tr: 'Mesajlar', en: 'Messages', de: 'Nachrichten' }, icon: 'MessageSquare', nav: 'messages' }
    ],
    chart: {
        title: { tr: 'Randevu Trafiği', en: 'Appointment Traffic', de: 'Terminverkehr' },
        subtitle: { tr: 'Haftalık doluluk oranı', en: 'Weekly occupancy rate', de: 'Wöchentliche Auslastung' },
        labels: {
            tr: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
            en: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            de: ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
        },
        datasets: [
            { label: { tr: 'Randevu', en: 'Appts', de: 'Termine' }, data: [18, 22, 25, 30, 35, 40, 10] },
            { label: { tr: 'İptal', en: 'Canceled', de: 'Abgesagt' }, data: [2, 3, 1, 4, 2, 5, 1] }
        ]
    }
}
