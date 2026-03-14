export const legal = {
    id: 'legal',
    label: { tr: 'Hukuk', en: 'Legal', de: 'Recht' },
    colors: {
        primary: '#b45309', secondary: '#78350f', accent: '#d97706',
        background: '#0a0806', surface: 'rgba(255, 255, 255, 0.03)', text: '#fffbeb',
        gradient: 'linear-gradient(135deg, #b45309 0%, #78350f 100%)',
        sidebar: 'linear-gradient(180deg, #0a0806 0%, #15100b 100%)',
        cardShadow: '0 4px 6px -1px rgba(180, 83, 9, 0.1), 0 2px 4px -1px rgba(180, 83, 9, 0.06)'
    },
    stats: [
        { label: { tr: 'Aktif Davalar', en: 'Active Cases', de: 'Aktive Fälle' }, value: '42', change: 1.5, icon: 'Briefcase', color: 'primary' },
        { label: { tr: 'Duruşmalar', en: 'Hearings', de: 'Anhörungen' }, value: '8', change: 0, icon: 'Gavel', color: 'secondary' },
        { label: { tr: 'Müvekkiller', en: 'Clients', de: 'Klienten' }, value: '12', change: 8.4, icon: 'UserPlus', color: 'accent' },
        { label: { tr: 'Fatura Saati', en: 'Billed Hrs', de: 'Abgerechnete Std' }, value: '145s', change: 12.3, icon: 'Clock', color: 'green' }
    ],
    quickActions: [
        {
            label: { tr: 'Dava Aç', en: 'New Case', de: 'Neuer Fall' }, icon: 'Gavel', nav: 'documents',
            fields: [
                { key: 'title', label: { tr: 'Dava Başlığı', en: 'Case Title', de: 'Falltitel' }, type: 'text' },
                { key: 'client', label: { tr: 'Müvekkil', en: 'Client', de: 'Klient' }, type: 'text' },
                {
                    key: 'type', label: { tr: 'Tür', en: 'Type', de: 'Typ' }, type: 'select', options: [
                        { value: 'civil', label: { tr: 'Hukuk', en: 'Civil', de: 'Zivil' } },
                        { value: 'criminal', label: { tr: 'Ceza', en: 'Criminal', de: 'Strafrecht' } }
                    ]
                }
            ]
        },
        {
            label: { tr: 'Müvekkil Ekle', en: 'Add Client', de: 'Klient hinzufügen' }, icon: 'UserPlus', nav: 'dashboard',
            fields: [
                { key: 'name', label: { tr: 'Ad Soyad', en: 'Full Name', de: 'Vor- und Nachname' }, type: 'text' },
                { key: 'phone', label: { tr: 'Telefon', en: 'Phone', de: 'Telefon' }, type: 'tel' }
            ]
        },
        {
            label: { tr: 'Belge Yükle', en: 'Upload Doc', de: 'Dokument hochladen' }, icon: 'Upload', nav: 'documents',
            fields: [
                { key: 'file', label: { tr: 'Dosya Seç', en: 'Choose File', de: 'Datei wählen' }, type: 'text' }
            ]
        },
        {
            label: { tr: 'Zaman Gir', en: 'Log Time', de: 'Zeit erfassen' }, icon: 'Clock', nav: 'calendar',
            fields: [
                { key: 'hours', label: { tr: 'Saat', en: 'Hours', de: 'Stunden' }, type: 'number' },
                { key: 'note', label: { tr: 'Açıklama', en: 'Note', de: 'Notiz' }, type: 'textarea' }
            ]
        }
    ],
    chart: {
        title: { tr: 'Dava Yükü', en: 'Case Load', de: 'Falllast' },
        subtitle: { tr: 'Tamamlanan vs Devam Eden', en: 'Completed vs Ongoing', de: 'Abgeschlossen vs Laufend' },
        labels: {
            tr: ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz'],
            en: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            de: ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun']
        },
        datasets: [
            { label: { tr: 'Tamamlanan', en: 'Completed', de: 'Abgeschlossen' }, data: [10, 15, 12, 18, 20, 25] },
            { label: { tr: 'Yeni Açılan', en: 'New Opened', de: 'Neu eröffnet' }, data: [12, 18, 15, 22, 24, 20] }
        ]
    }
}
