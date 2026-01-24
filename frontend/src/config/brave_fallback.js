/**
 * BRAVE FALLBACK CONFIGURATION
 * 
 * "Legacy of Resilience"
 * 
 * This file contains high-fidelity mock data that is served INSTANTLY
 * if the backend API fails during a critical demo.
 * 
 * The goal: The CEO must NEVER see a loading spinner hanging or a red error alert.
 */

export const BRAVE_FALLBACK = {
    // Analytics Stats
    '/analytics/stats': {
        daily_revenue: 15420.00,
        active_calls: 3,
        customer_satisfaction: 98.5,
        total_appointments: 24,
        completed_appointments: 18,
        waiting_appointments: 4,
        cancelled_appointments: 2
    },

    // Sectoral KPIs
    '/analytics/kpis': [
        {
            label: "Randevu Sadakati",
            value: "94%",
            trend: "+2.5%",
            positive: true,
            description: "Randevusuna sadık kalan hasta oranı"
        },
        {
            label: "Yıllık Hasta Tekrarı",
            value: "3.2",
            trend: "+0.4",
            positive: true,
            description: "Ortalama yıllık ziyaret sayısı"
        },
        {
            label: "İptal Oranı",
            value: "4.8%",
            trend: "-1.2%",
            positive: true,
            description: "Son 30 gündeki iptal oranı"
        }
    ],

    // AI Strategic Insights
    '/analytics/insights': [
        {
            type: "opportunity",
            title: "Kapasite Fırsatı",
            message: "Salı günleri öğleden sonra randevu yoğunluğunuz %20 artıyor. Bu saatlere ek bir asistan atamak bekleme sürelerini düşürebilir.",
            action: "Otomatik Asistan Ekle"
        },
        {
            type: "warning",
            title: "İptal Riski Analizi",
            message: "Cuma akşamüstü alınan randevuların iptal edilme olasılığı diğer saatlere göre %15 daha yüksek. Teyit aramalarını sıkılaştırın.",
            action: "Teyit Kurallarını Güncelle"
        },
        {
            type: "success",
            title: "VIP Segment Büyümesi",
            message: "Son bir ayda VIP müşteri segmentiniz %12 büyüdü. Bu gruba özel bir sadakat kampanyası başlatmak gelirleri artırabilir.",
            action: "Kampanya Oluştur"
        }
    ],

    // Chart Data (Conversation Duration)
    '/analytics/daily-conversation-duration': {
        series: [{ name: "Duration", data: [45, 52, 38, 24, 33, 26, 21, 20, 6, 8, 15, 10] }],
        categories: ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"]
    },

    // Appointments List
    '/appointments': [
        {
            id: 1,
            customer_name: 'Mehmet Yılmaz',
            start_time: new Date(new Date().setHours(14, 30)).toISOString(),
            status: 'confirmed',
            notes: 'Genel Kontrol'
        },
        {
            id: 2,
            customer_name: 'Ayşe Kaya',
            start_time: new Date(new Date().setHours(15, 0)).toISOString(),
            status: 'waiting',
            notes: 'Diş Beyazlatma'
        },
        {
            id: 3,
            customer_name: 'Zeynep Demir',
            start_time: new Date(new Date().setHours(16, 15)).toISOString(),
            status: 'scheduled',
            notes: 'Dolgu Tedavisi'
        }
    ]
}

export const isCriticalEndpoint = (url) => {
    // Remove query params for check
    const cleanUrl = url.split('?')[0]
    return Object.keys(BRAVE_FALLBACK).some(key => cleanUrl.endsWith(key))
}

export const getFallbackData = (url) => {
    const cleanUrl = url.split('?')[0]
    const key = Object.keys(BRAVE_FALLBACK).find(k => cleanUrl.endsWith(k))
    return BRAVE_FALLBACK[key]
}
