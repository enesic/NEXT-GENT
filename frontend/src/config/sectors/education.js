export const education = {
    id: 'education',
    label: { tr: 'Eğitim', en: 'Education', de: 'Ausbildung' },
    colors: {
        primary: '#8b5cf6', secondary: '#4c1d95', accent: '#a78bfa',
        background: '#06040a', surface: 'rgba(255, 255, 255, 0.03)', text: '#f5f3ff',
        gradient: 'linear-gradient(135deg, #8b5cf6 0%, #4c1d95 100%)',
        sidebar: 'linear-gradient(180deg, #06040a 0%, #0c0817 100%)',
        cardShadow: '0 4px 6px -1px rgba(139, 92, 246, 0.1), 0 2px 4px -1px rgba(139, 92, 246, 0.06)'
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
}
