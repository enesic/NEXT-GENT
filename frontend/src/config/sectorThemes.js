// Sector-Specific Theme and Data Configuration
// This file defines the look, feel, and default data for each industry sector, including multi-language support.

export const sectorThemes = {
    medical: {
        id: 'medical',
        label: { tr: 'Sağlık', en: 'Medical', de: 'Medizin' },
        colors: {
            primary: '#0ea5e9', secondary: '#0f766e', accent: '#38bdf8',
            background: '#030303', surface: 'rgba(255, 255, 255, 0.03)', text: '#e2e8f0',
            gradient: 'linear-gradient(135deg, #0ea5e9 0%, #0f766e 100%)',
            sidebar: 'linear-gradient(180deg, #030303 0%, #0a0a0a 100%)',
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
    },
    legal: {
        id: 'legal',
        label: { tr: 'Hukuk', en: 'Legal', de: 'Recht' },
        colors: {
            primary: '#818cf8', secondary: '#fbbf24', accent: '#d97706',
            background: '#030303', surface: 'rgba(255, 255, 255, 0.03)', text: '#e2e8f0',
            gradient: 'linear-gradient(135deg, #818cf8 0%, #6366f1 100%)',
            sidebar: 'linear-gradient(180deg, #030303 0%, #0a0a0a 100%)',
            cardShadow: '0 4px 6px -1px rgba(129, 140, 248, 0.1), 0 2px 4px -1px rgba(129, 140, 248, 0.06)'
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
    },
    real_estate: {
        id: 'real_estate',
        label: { tr: 'Emlak', en: 'Real Estate', de: 'Immobilien' },
        colors: {
            primary: '#10b981', secondary: '#fbbf24', accent: '#34d399',
            background: '#030303', surface: 'rgba(255, 255, 255, 0.03)', text: '#e2e8f0',
            gradient: 'linear-gradient(135deg, #047857 0%, #059669 100%)',
            sidebar: 'linear-gradient(180deg, #030303 0%, #0a0a0a 100%)',
            cardShadow: '0 4px 6px -1px rgba(4, 120, 87, 0.1), 0 2px 4px -1px rgba(4, 120, 87, 0.06)'
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
    },
    finance: {
        id: 'finance',
        label: { tr: 'Finans', en: 'Finance', de: 'Finanzen' },
        colors: {
            primary: '#a78bfa', secondary: '#34d399', accent: '#6ee7b7',
            background: '#030303', surface: 'rgba(255, 255, 255, 0.03)', text: '#e2e8f0',
            gradient: 'linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%)',
            sidebar: 'linear-gradient(180deg, #030303 0%, #0a0a0a 100%)',
            cardShadow: '0 4px 6px -1px rgba(167, 139, 250, 0.1), 0 2px 4px -1px rgba(167, 139, 250, 0.06)'
        },
        stats: [
            { label: { tr: 'Toplam Varlık', en: 'Total Assets', de: 'Gesamtvermögen' }, value: '₺8.4M', change: 12.5, icon: 'Wallet', color: 'primary' },
            { label: { tr: 'Aylık Gelir', en: 'Monthly Income', de: 'Monatliches Einkommen' }, value: '₺450K', change: 8.2, icon: 'TrendingUp', color: 'secondary' },
            { label: { tr: 'Giderler', en: 'Expenses', de: 'Ausgaben' }, value: '₺120K', change: -3.1, icon: 'TrendingDown', color: 'red' },
            { label: { tr: 'Net Kar', en: 'Net Profit', de: 'Nettogewinn' }, value: '₺330K', change: 15.4, icon: 'PieChart', color: 'green' }
        ],
        quickActions: [
            {
                label: { tr: 'Transfer Yap', en: 'Transfer', de: 'Überweisung' }, icon: 'ArrowRight', nav: 'documents',
                fields: [
                    { key: 'to', label: { tr: 'Alıcı', en: 'To', de: 'Empfänger' }, type: 'text' },
                    { key: 'amount', label: { tr: 'Tutar', en: 'Amount', de: 'Betrag' }, type: 'number' },
                    { key: 'desc', label: { tr: 'Açıklama', en: 'Description', de: 'Verwendungszweck' }, type: 'text' }
                ]
            },
            {
                label: { tr: 'Fatura Kes', en: 'Invoice', de: 'Rechnung' }, icon: 'FileText', nav: 'documents',
                fields: [
                    { key: 'client', label: { tr: 'Müşteri', en: 'Client', de: 'Kunde' }, type: 'text' },
                    { key: 'amount', label: { tr: 'Tutar', en: 'Amount', de: 'Betrag' }, type: 'number' }
                ]
            },
            { label: { tr: 'Rapor Al', en: 'Report', de: 'Bericht' }, icon: 'BarChart3', nav: 'analytics' },
            {
                label: { tr: 'Kur Ekle', en: 'Exchange Rate', de: 'Wechselkurs' }, icon: 'DollarSign', nav: 'dashboard',
                fields: [
                    { key: 'currency', label: { tr: 'Döviz', en: 'Currency', de: 'Währung' }, type: 'text', placeholder: 'USD' },
                    { key: 'rate', label: { tr: 'Kur', en: 'Rate', de: 'Kurs' }, type: 'number' }
                ]
            }
        ],
        chart: {
            title: { tr: 'Nakit Akışı', en: 'Cash Flow', de: 'Cashflow' },
            subtitle: { tr: 'Gelir ve Gider Dengesi', en: 'Income and Exp Balance', de: 'Einnahmen und Ausgaben' },
            labels: {
                tr: ['Q1', 'Q2', 'Q3', 'Q4'],
                en: ['Q1', 'Q2', 'Q3', 'Q4'],
                de: ['Q1', 'Q2', 'Q3', 'Q4']
            },
            datasets: [
                { label: { tr: 'Gelir', en: 'Income', de: 'Einnahmen' }, data: [300, 450, 400, 500] },
                { label: { tr: 'Gider', en: 'Expense', de: 'Ausgaben' }, data: [100, 120, 150, 130] }
            ]
        }
    },
    technology: {
        id: 'technology',
        label: { tr: 'Teknoloji', en: 'Technology', de: 'Technologie' },
        colors: {
            primary: '#818cf8', secondary: '#a78bfa', accent: '#c084fc',
            background: '#030303', surface: 'rgba(255, 255, 255, 0.03)', text: '#e2e8f0',
            gradient: 'linear-gradient(135deg, #818cf8 0%, #a78bfa 100%)',
            sidebar: 'linear-gradient(180deg, #030303 0%, #0a0a0a 100%)',
            cardShadow: '0 4px 6px -1px rgba(129, 140, 248, 0.1), 0 2px 4px -1px rgba(129, 140, 248, 0.06)'
        },
        stats: [
            { label: { tr: 'Aktif Kullanıcı', en: 'Active Users', de: 'Aktive Benutzer' }, value: '25.4K', change: 18.2, icon: 'Users', color: 'primary' },
            { label: { tr: 'Sunucu Yükü', en: 'Server Load', de: 'Serverauslastung' }, value: '45%', change: 5.1, icon: 'Cpu', color: 'secondary' },
            { label: { tr: 'API İstekleri', en: 'API Requests', de: 'API-Anfragen' }, value: '1.2M', change: 24.5, icon: 'Zap', color: 'accent' },
            { label: { tr: 'Uptime', en: 'Uptime', de: 'Betriebszeit' }, value: '99.9%', change: 0, icon: 'Server', color: 'green' }
        ],
        quickActions: [
            {
                label: { tr: 'Dağıtım Yap', en: 'Deploy', de: 'Bereitstellen' }, icon: 'Rocket', nav: 'dashboard',
                fields: [
                    {
                        key: 'env', label: { tr: 'Ortam', en: 'Env', de: 'Umgebung' }, type: 'select', options: [
                            { value: 'prod', label: 'Production' },
                            { value: 'stg', label: 'Staging' }
                        ]
                    },
                    { key: 'version', label: { tr: 'Versiyon', en: 'Version', de: 'Version' }, type: 'text' }
                ]
            },
            { label: { tr: 'Loglar', en: 'Logs', de: 'Protokolle' }, icon: 'FileCode', nav: 'documents' },
            { label: { tr: 'Kullanıcılar', en: 'Users', de: 'Benutzer' }, icon: 'UserCog', nav: 'settings' },
            {
                label: { tr: 'Yedekle', en: 'Backup', de: 'Sichern' }, icon: 'Database', nav: 'settings',
                fields: [
                    { key: 'db', label: { tr: 'Veritabanı', en: 'DB', de: 'Datenbank' }, type: 'text' }
                ]
            }
        ],
        chart: {
            title: { tr: 'Sistem Yükü', en: 'System Load', de: 'Systemauslastung' },
            subtitle: { tr: 'Sunucu Kaynak Kullanımı', en: 'Server resources', de: 'Serverressourcen' },
            labels: {
                tr: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
                en: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
                de: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00']
            },
            datasets: [
                { label: { tr: 'CPU', en: 'CPU', de: 'CPU' }, data: [20, 25, 45, 60, 55, 30] },
                { label: { tr: 'Bellek', en: 'Memory', de: 'Speicher' }, data: [40, 42, 45, 50, 48, 45] }
            ]
        }
    },
    beauty: {
        id: 'beauty',
        label: { tr: 'Güzellik', en: 'Beauty', de: 'Schönheit' },
        colors: {
            primary: '#f472b6', secondary: '#fb923c', accent: '#e879f9',
            background: '#030303', surface: 'rgba(255, 255, 255, 0.03)', text: '#e2e8f0',
            gradient: 'linear-gradient(135deg, #f472b6 0%, #e879f9 100%)',
            sidebar: 'linear-gradient(180deg, #030303 0%, #0a0a0a 100%)',
            cardShadow: '0 4px 6px -1px rgba(244, 114, 182, 0.1), 0 2px 4px -1px rgba(244, 114, 182, 0.06)'
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
    },
    hospitality: {
        id: 'hospitality',
        label: { tr: 'Konaklama', en: 'Hospitality', de: 'Gastgewerbe' },
        colors: {
            primary: '#f59e0b', secondary: '#d97706', accent: '#fbbf24',
            background: '#030303', surface: 'rgba(255, 255, 255, 0.03)', text: '#e2e8f0',
            gradient: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
            sidebar: 'linear-gradient(180deg, #030303 0%, #0a0a0a 100%)',
            cardShadow: '0 4px 6px -1px rgba(245, 158, 11, 0.1), 0 2px 4px -1px rgba(245, 158, 11, 0.06)'
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
    },
    automotive: {
        id: 'automotive',
        label: { tr: 'Otomotiv', en: 'Automotive', de: 'Automobil' },
        colors: {
            primary: '#ef4444', secondary: '#f97316', accent: '#fb923c',
            background: '#030303', surface: 'rgba(255, 255, 255, 0.03)', text: '#e2e8f0',
            gradient: 'linear-gradient(135deg, #ef4444 0%, #f97316 100%)',
            sidebar: 'linear-gradient(180deg, #030303 0%, #0a0a0a 100%)',
            cardShadow: '0 4px 6px -1px rgba(239, 68, 68, 0.1), 0 2px 4px -1px rgba(239, 68, 68, 0.06)'
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
    },
    manufacturing: {
        id: 'manufacturing',
        label: { tr: 'Üretim', en: 'Manufacturing', de: 'Produktion' },
        colors: {
            primary: '#6366f1', secondary: '#8b5cf6', accent: '#a78bfa',
            background: '#030303', surface: 'rgba(255, 255, 255, 0.03)', text: '#e2e8f0',
            gradient: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
            sidebar: 'linear-gradient(180deg, #030303 0%, #0a0a0a 100%)',
            cardShadow: '0 4px 6px -1px rgba(99, 102, 241, 0.1), 0 2px 4px -1px rgba(99, 102, 241, 0.06)'
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
    },
    education: {
        id: 'education',
        label: { tr: 'Eğitim', en: 'Education', de: 'Ausbildung' },
        colors: {
            primary: '#3b82f6', secondary: '#06b6d4', accent: '#38bdf8',
            background: '#030303', surface: 'rgba(255, 255, 255, 0.03)', text: '#e2e8f0',
            gradient: 'linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%)',
            sidebar: 'linear-gradient(180deg, #030303 0%, #0a0a0a 100%)',
            cardShadow: '0 4px 6px -1px rgba(59, 130, 246, 0.1), 0 2px 4px -1px rgba(59, 130, 246, 0.06)'
        },
        stats: [
            { label: { tr: 'Öğrenciler', en: 'Students', de: 'Studenten' }, value: '1,245', change: 12.3, icon: 'Users', color: 'primary' },
            { label: { tr: 'Aktif Kurslar', en: 'Active Courses', de: 'Aktive Kurse' }, value: '48', change: 5.1, icon: 'Calendar', color: 'accent' },
            { label: { tr: 'Tamamlanan', en: 'Completed', de: 'Abgeschlossen' }, value: '312', change: 8.7, icon: 'CheckCircle', color: 'green' },
            { label: { tr: 'Memnuniyet', en: 'Satisfaction', de: 'Zufriedenheit' }, value: '97%', change: 1.2, icon: 'Heart', color: 'secondary' }
        ],
        quickActions: [
            {
                label: { tr: 'Ders Ekle', en: 'Add Class', de: 'Klasse hinzu' }, icon: 'CalendarPlus', nav: 'appointments',
                fields: [
                    { key: 'course', label: { tr: 'Ders', en: 'Course', de: 'Kurs' }, type: 'text' },
                    { key: 'teacher', label: { tr: 'Öğretmen', en: 'Teacher', de: 'Lehrer' }, type: 'text' }
                ]
            },
            {
                label: { tr: 'Öğrenci Kaydı', en: 'New Student', de: 'Neuer Student' }, icon: 'UserPlus', nav: 'dashboard',
                fields: [
                    { key: 'name', label: { tr: 'Ad Soyad', en: 'Name', de: 'Name' }, type: 'text' },
                    { key: 'grade', label: { tr: 'Sınıf', en: 'Grade', de: 'Klasse' }, type: 'text' }
                ]
            },
            { label: { tr: 'Materyal', en: 'Material', de: 'Material' }, icon: 'FileText', nav: 'documents' },
            { label: { tr: 'Mesajlar', en: 'Messages', de: 'Nachrichten' }, icon: 'MessageSquare', nav: 'messages' }
        ],
        chart: {
            title: { tr: 'Katılım Analizi', en: 'Attendance Analysis', de: 'Teilnahmeanalyse' },
            subtitle: { tr: 'Haftalık katılım', en: 'Weekly attendance', de: 'Wöchentliche Teilnahme' },
            labels: {
                tr: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
                en: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                de: ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
            },
            datasets: [
                { label: { tr: 'Katılım', en: 'Attendance', de: 'Teilnahme' }, data: [220, 250, 230, 280, 260, 100, 50] },
                { label: { tr: 'Hedef', en: 'Target', de: 'Ziel' }, data: [250, 250, 250, 250, 250, 150, 50] }
            ]
        }
    },
    retail: {
        id: 'retail',
        label: { tr: 'Perakende', en: 'Retail', de: 'Einzelhandel' },
        colors: {
            primary: '#22c55e', secondary: '#16a34a', accent: '#4ade80',
            background: '#030303', surface: 'rgba(255, 255, 255, 0.03)', text: '#e2e8f0',
            gradient: 'linear-gradient(135deg, #22c55e 0%, #16a34a 100%)',
            sidebar: 'linear-gradient(180deg, #030303 0%, #0a0a0a 100%)',
            cardShadow: '0 4px 6px -1px rgba(34, 197, 94, 0.1), 0 2px 4px -1px rgba(34, 197, 94, 0.06)'
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
    },
    ecommerce: {
        id: 'ecommerce',
        label: { tr: 'E-Ticaret', en: 'E-Commerce', de: 'E-Commerce' },
        colors: {
            primary: '#f97316', secondary: '#ea580c', accent: '#fb923c',
            background: '#030303', surface: 'rgba(255, 255, 255, 0.03)', text: '#e2e8f0',
            gradient: 'linear-gradient(135deg, #f97316 0%, #ea580c 100%)',
            sidebar: 'linear-gradient(180deg, #030303 0%, #0a0a0a 100%)',
            cardShadow: '0 4px 6px -1px rgba(249, 115, 22, 0.1), 0 2px 4px -1px rgba(249, 115, 22, 0.06)'
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
};

export default sectorThemes;
