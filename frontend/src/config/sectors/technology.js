export const technology = {
    id: 'technology',
    label: { tr: 'Teknoloji', en: 'Technology', de: 'Technologie' },
    colors: {
        primary: '#3b82f6', secondary: '#8b5cf6', accent: '#60a5fa',
        background: '#04050a', surface: 'rgba(255, 255, 255, 0.03)', text: '#f1f5f9',
        gradient: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
        sidebar: 'linear-gradient(180deg, #04050a 0%, #080a18 100%)',
        cardShadow: '0 4px 6px -1px rgba(59, 130, 246, 0.1), 0 2px 4px -1px rgba(59, 130, 246, 0.06)'
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
}
