export const real_estate = {
    id: 'real_estate',
    label: { tr: 'Emlak', en: 'Real Estate', de: 'Immobilien' },
    colors: {
        primary: '#3b82f6', secondary: '#1e40af', accent: '#60a5fa',
        background: '#04070a', surface: 'rgba(255, 255, 255, 0.03)', text: '#eff6ff',
        gradient: 'linear-gradient(135deg, #3b82f6 0%, #1e40af 100%)',
        sidebar: 'linear-gradient(180deg, #04070a 0%, #08101a 100%)',
        cardShadow: '0 4px 6px -1px rgba(59, 130, 246, 0.1), 0 2px 4px -1px rgba(59, 130, 246, 0.06)'
    },
    stats: [
        { label: { tr: 'Satılık Portföy', en: 'For Sale', de: 'Zum Verkauf' }, value: '156', change: 3.2, icon: 'Home', color: 'primary' },
        { label: { tr: 'Kiralık Portföy', en: 'For Rent', de: 'Zur Miete' }, value: '89', change: -1.5, icon: 'Key', color: 'accent' },
        { label: { tr: 'Bu Ay Satılan', en: 'Sold This Month', de: 'Diesen Monat verkauft' }, value: '12', change: 24.0, icon: 'DollarSign', color: 'secondary' },
        { label: { tr: 'Yeni Talepler', en: 'New Requests', de: 'Neue Anfragen' }, value: '45', change: 15.6, icon: 'MessageCircle', color: 'green' }
    ],
    quickActions: [
        {
            label: { tr: 'İlan Ekle', en: 'Add Listing', de: 'Inserat hinzufügen' }, icon: 'PlusCircle', nav: 'documents',
            fields: [
                { key: 'title', label: { tr: 'İlan Başlığı', en: 'Listing Title', de: 'Anzeigentitel' }, type: 'text' },
                {
                    key: 'type', label: { tr: 'Tür', en: 'Type', de: 'Typ' }, type: 'select', options: [
                        { value: 'sale', label: { tr: 'Satılık', en: 'For Sale', de: 'Verkauf' } },
                        { value: 'rent', label: { tr: 'Kiralık', en: 'For Rent', de: 'Miete' } }
                    ]
                },
                { key: 'price', label: { tr: 'Fiyat', en: 'Price', de: 'Preis' }, type: 'number' }
            ]
        },
        {
            label: { tr: 'Randevu', en: 'Appointment', de: 'Termin' }, icon: 'Calendar', nav: 'appointments',
            fields: [
                { key: 'client', label: { tr: 'Müşteri', en: 'Client', de: 'Kunde' }, type: 'text' },
                { key: 'date', label: { tr: 'Tarih', en: 'Date', de: 'Datum' }, type: 'datetime-local' }
            ]
        },
        {
            label: { tr: 'Sözleşme', en: 'Contract', de: 'Vertrag' }, icon: 'FileText', nav: 'documents',
            fields: [
                { key: 'client', label: { tr: 'Müşteri', en: 'Client', de: 'Kunde' }, type: 'text' },
                { key: 'type', label: { tr: 'Tür', en: 'Type', de: 'Vertragstyp' }, type: 'text' }
            ]
        },
        {
            label: { tr: 'Müşteri Ekle', en: 'Add Client', de: 'Klient hinzufügen' }, icon: 'UserPlus', nav: 'dashboard',
            fields: [
                { key: 'name', label: { tr: 'Ad Soyad', en: 'Name', de: 'Name' }, type: 'text' },
                { key: 'phone', label: { tr: 'Telefon', en: 'Phone', de: 'Telefon' }, type: 'tel' }
            ]
        }
    ],
    chart: {
        title: { tr: 'Satış Performansı', en: 'Sales Performance', de: 'Verkaufsleistung' },
        subtitle: { tr: 'Aylık işlem hacmi', en: 'Monthly tx volume', de: 'Monatliches Volumen' },
        labels: {
            tr: ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz'],
            en: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            de: ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun']
        },
        datasets: [
            { label: { tr: 'Satış', en: 'Sales', de: 'Verkäufe' }, data: [5, 8, 12, 10, 15, 18] },
            { label: { tr: 'Kiralama', en: 'Rentals', de: 'Vermietungen' }, data: [20, 25, 30, 28, 35, 40] }
        ]
    }
}
