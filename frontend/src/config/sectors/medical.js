export const medical = {
    id: 'medical',
    label: { tr: 'Sağlık', en: 'Medical', de: 'Medizin' },
    colors: {
        primary: '#0ea5e9', secondary: '#0f766e', accent: '#38bdf8',
        background: '#020408', surface: 'rgba(255, 255, 255, 0.03)', text: '#e2e8f0',
        gradient: 'linear-gradient(135deg, #0ea5e9 0%, #0f766e 100%)',
        sidebar: 'linear-gradient(180deg, #020408 0%, #050a14 100%)',
        cardShadow: '0 4px 6px -1px rgba(14, 165, 233, 0.1), 0 2px 4px -1px rgba(14, 165, 233, 0.06)'
    },
    stats: [
        { label: { tr: 'Bugünkü Randevular', en: 'Today Appts', de: 'Heute Termine' }, value: '124', change: 5.2, icon: 'Calendar', color: 'primary' },
        { label: { tr: 'Aktif Hastalar', en: 'Active Patients', de: 'Aktive Patienten' }, value: '1,284', change: 2.1, icon: 'Users', color: 'accent' },
        { label: { tr: 'Acil Durumlar', en: 'Emergencies', de: 'Notfälle' }, value: '3', change: -10.5, icon: 'AlertCircle', color: 'red' },
        { label: { tr: 'Müşteri Memnuniyeti', en: 'Satisfaction', de: 'Zufriedenheit' }, value: '98%', change: 1.2, icon: 'Heart', color: 'secondary' }
    ],
    quickActions: [
        {
            label: { tr: 'Randevu Ekle', en: 'Add Appt', de: 'Termin hinzufügen' }, icon: 'CalendarPlus', nav: 'appointments',
            fields: [
                { key: 'patient', label: { tr: 'Hasta Adı', en: 'Patient Name', de: 'Patientenname' }, type: 'text', placeholder: { tr: 'Ad Soyad', en: 'Full Name', de: 'Vor- und Nachname' } },
                {
                    key: 'dept', label: { tr: 'Poliklinik', en: 'Department', de: 'Abteilung' }, type: 'select', placeholder: { tr: 'Bölüm Seçin', en: 'Select Dept', de: 'Abt. wählen' }, options: [
                        { value: 'cardiology', label: { tr: 'Kardiyoloji', en: 'Cardiology', de: 'Kardiologie' } },
                        { value: 'dermatology', label: { tr: 'Dermatoloji', en: 'Dermatology', de: 'Dermatologie' } }
                    ]
                },
                { key: 'date', label: { tr: 'Tarih', en: 'Date', de: 'Datum' }, type: 'datetime-local' }
            ]
        },
        {
            label: { tr: 'Hasta Kaydı', en: 'New Patient', de: 'Neuer Patient' }, icon: 'UserPlus', nav: 'dashboard',
            fields: [
                { key: 'name', label: { tr: 'Ad Soyad', en: 'Full Name', de: 'Vor- und Nachname' }, type: 'text' },
                { key: 'phone', label: { tr: 'Telefon', en: 'Phone', de: 'Telefon' }, type: 'tel' },
                { key: 'tc', label: { tr: 'T.C. No / ID', en: 'ID Number', de: 'Ausweisnummer' }, type: 'text' }
            ]
        },
        {
            label: { tr: 'Reçete', en: 'Prescription', de: 'Rezept' }, icon: 'FileText', nav: 'documents',
            fields: [
                { key: 'patient', label: { tr: 'Hasta', en: 'Patient', de: 'Patient' }, type: 'text' },
                { key: 'meds', label: { tr: 'İlaçlar', en: 'Medications', de: 'Medikamente' }, type: 'textarea' }
            ]
        },
        {
            label: { tr: 'Sonuçlar', en: 'Lab Results', de: 'Ergebnisse' }, icon: 'Activity', nav: 'documents',
            fields: [
                { key: 'patient', label: { tr: 'Hasta', en: 'Patient', de: 'Patient' }, type: 'text' },
                { key: 'type', label: { tr: 'Test Türü', en: 'Test Type', de: 'Testart' }, type: 'text' }
            ]
        }
    ],
    chart: {
        title: { tr: 'Hasta Trafiği', en: 'Patient Traffic', de: 'Patientenverkehr' },
        subtitle: { tr: 'Poliklinik yoğunluğu', en: 'Clinic density', de: 'Klinikdichte' },
        labels: {
            tr: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
            en: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            de: ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
        },
        datasets: [
            { label: { tr: 'Muayene', en: 'Examination', de: 'Untersuchung' }, data: [45, 52, 38, 65, 74, 55, 20] },
            { label: { tr: 'Acil', en: 'Emergency', de: 'Notfall' }, data: [12, 15, 8, 22, 18, 25, 35] }
        ]
    }
}
