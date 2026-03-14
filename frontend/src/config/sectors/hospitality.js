export const hospitality = {
    id: 'hospitality',
    label: { tr: 'Konaklama', en: 'Hospitality', de: 'Gastgewerbe' },
    colors: {
        primary: '#be185d', secondary: '#831843', accent: '#f472b6',
        background: '#0a0306', surface: 'rgba(255, 255, 255, 0.03)', text: '#fdf2f8',
        gradient: 'linear-gradient(135deg, #be185d 0%, #831843 100%)',
        sidebar: 'linear-gradient(180deg, #0a0306 0%, #170810 100%)',
        cardShadow: '0 4px 6px -1px rgba(190, 24, 93, 0.1), 0 2px 4px -1px rgba(190, 24, 93, 0.06)'
    },
    stats: [
        { label: { tr: 'Doluluk Oranı', en: 'Occupancy Rate', de: 'Belegungsrate' }, value: '87%', change: 5.2, icon: 'Home', color: 'primary' },
        { label: { tr: 'Rezervasyonlar', en: 'Reservations', de: 'Reservierungen' }, value: '142', change: 3.1, icon: 'Calendar', color: 'accent' },
        { label: { tr: 'Memnuniyet', en: 'Satisfaction', de: 'Zufriedenheit' }, value: '94%', change: 1.4, icon: 'Heart', color: 'secondary' },
        { label: { tr: 'Aylık Gelir', en: 'Monthly Income', de: 'Monatliches Einkommen' }, value: '₺580K', change: 11.2, icon: 'TrendingUp', color: 'green' }
    ],
    quickActions: [
        {
            label: { tr: 'Rezv. Ekle', en: 'Add Resv.', de: 'Resv. hinzufügen' }, icon: 'CalendarPlus', nav: 'appointments',
            fields: [
                { key: 'guest', label: { tr: 'Misafir', en: 'Guest', de: 'Gast' }, type: 'text' },
                { key: 'room', label: { tr: 'Oda No', en: 'Room No', de: 'Zimmernr' }, type: 'text' },
                { key: 'dates', label: { tr: 'Tarihler', en: 'Dates', de: 'Daten' }, type: 'text' }
            ]
        },
        {
            label: { tr: 'Misafir Kaydı', en: 'Guest Reg.', de: 'Gastregistrierung' }, icon: 'UserPlus', nav: 'dashboard',
            fields: [
                { key: 'name', label: { tr: 'Ad Soyad', en: 'Name', de: 'Name' }, type: 'text' },
                { key: 'passport', label: { tr: 'Pasaport / Kimlik', en: 'Passport/ID', de: 'Ausweis' }, type: 'text' }
            ]
        },
        { label: { tr: 'Oda Durumu', en: 'Room Status', de: 'Zimmerstatus' }, icon: 'Home', nav: 'documents' },
        { label: { tr: 'Mesajlar', en: 'Messages', de: 'Nachrichten' }, icon: 'MessageSquare', nav: 'messages' }
    ],
    chart: {
        title: { tr: 'Doluluk Analizi', en: 'Occupancy Analysis', de: 'Belegungsanalyse' },
        subtitle: { tr: 'Haftalık rezervasyon oranı', en: 'Weekly resv rate', de: 'Wöchentliche Resv-Rate' },
        labels: {
            tr: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
            en: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            de: ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
        },
        datasets: [
            { label: { tr: 'Rezervasyon', en: 'Reservation', de: 'Reservierung' }, data: [70, 75, 80, 85, 90, 95, 88] },
            { label: { tr: 'İptal', en: 'Canceled', de: 'Abgesagt' }, data: [5, 3, 4, 2, 6, 3, 4] }
        ]
    }
}
