export const finance = {
    id: 'finance',
    label: { tr: 'Finans', en: 'Finance', de: 'Finanzen' },
    colors: {
        primary: '#10b981', secondary: '#047857', accent: '#34d399',
        background: '#030805', surface: 'rgba(255, 255, 255, 0.03)', text: '#ecfdf5',
        gradient: 'linear-gradient(135deg, #10b981 0%, #047857 100%)',
        sidebar: 'linear-gradient(180deg, #030805 0%, #06140b 100%)',
        cardShadow: '0 4px 6px -1px rgba(16, 185, 129, 0.1), 0 2px 4px -1px rgba(16, 185, 129, 0.06)'
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
}
