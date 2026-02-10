<template>
  <div class="calendar-layout">
    <div class="header-controls">
      <div class="title-group">
        <h2>{{ currentMonthName }} {{ currentYear }}</h2>
        <p class="subtitle">{{ events.length }} randevu/etkinlik</p>
      </div>
      <div class="controls-right">
        <div class="month-selector">
          <button class="nav-btn" @click="changeMonth(-1)">
            <ChevronLeft :size="20" />
          </button>
          <button class="nav-btn" @click="changeMonth(1)">
            <ChevronRight :size="20" />
          </button>
        </div>
        <div class="filters">
          <button class="view-btn active">Ay</button>
          <button class="view-btn">Hafta</button>
          <button class="view-btn">Liste</button>
        </div>
        <button class="add-btn">
          <Plus :size="18" />
          Yeni Randevu
        </button>
      </div>
    </div>

    <div class="calendar-content-grid">
      <div class="calendar-wrapper">
        <div class="calendar-grid">
          <!-- Weekday Headers -->
          <div v-for="day in weekDays" :key="day" class="weekday-header">
            {{ day }}
          </div>
          
          <!-- Calendar Cells -->
          <div 
            v-for="(day, index) in calendarDays" 
            :key="index"
            class="calendar-day"
            :class="{ 'other-month': !day.isCurrentMonth, 'today': day.isToday }"
            :style="{ animationDelay: `${(index % 7) * 0.02 + Math.floor(index / 7) * 0.02}s` }"
            @click="selectDay(day)"
          >
            <div class="day-number">{{ day.date.getDate() }}</div>
            
            <div class="events-list">
              <div 
                v-for="event in getEventsForDay(day.date)" 
                :key="event.id"
                class="event-pill"
                :class="[event.status.toLowerCase(), event.color]"
              >
                <span class="event-time">{{ event.time }}</span>
                <span class="event-title">{{ event.title }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Upcoming Sidebar -->
      <div class="upcoming-sidebar">
          <h3>Yaklaşan Etkinlikler</h3>
          <div class="upcoming-list">
              <div v-for="event in upcomingEvents" :key="event.id" class="upcoming-item">
                  <div class="item-date">
                      <span class="day">{{ new Date(event.start_time).getDate() }}</span>
                      <span class="month">{{ months[new Date(event.start_time).getMonth()].substring(0,3) }}</span>
                  </div>
                  <div class="item-info">
                      <h4>{{ event.title }}</h4>
                      <p>{{ event.time || '10:00' }} • {{ event.status === 'confirmed' ? 'Onaylı' : 'Beklemede' }}</p>
                  </div>
              </div>
          </div>
          <div class="storage-info">
              <div class="storage-labels">
                  <label>Bulut Depolama</label>
                  <span>%65</span>
              </div>
              <div class="storage-bar">
                  <div class="storage-fill" style="width: 65%"></div>
              </div>
          </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue'
import { ChevronLeft, ChevronRight, Plus } from 'lucide-vue-next'
import { useSectorStore } from '../stores/sector'

const axios = inject('axios')
const sectorStore = useSectorStore()

const currentDate = ref(new Date())
const events = ref([])
const upcomingEvents = computed(() => {
    return events.value
        .filter(e => new Date(e.start_time) >= new Date())
        .sort((a,b) => new Date(a.start_time) - new Date(b.start_time))
        .slice(0, 5)
})

const months = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
const weekDays = ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz']

const currentMonthName = computed(() => {
  return currentDate.value.toLocaleString('tr-TR', { month: 'long' })
})

const currentYear = computed(() => currentDate.value.getFullYear())

const calendarDays = computed(() => {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth()
  
  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)
  
  const days = []
  
  // Previous month padding
  const startPadding = (firstDay.getDay() + 6) % 7 // Monday start
  for (let i = startPadding - 1; i >= 0; i--) {
    const d = new Date(year, month, -i)
    days.push({ date: d, isCurrentMonth: false, isToday: isSameDay(d, new Date()) })
  }
  
  // Current month
  for (let i = 1; i <= lastDay.getDate(); i++) {
    const d = new Date(year, month, i)
    days.push({ date: d, isCurrentMonth: true, isToday: isSameDay(d, new Date()) })
  }
  
  // Next month padding
  const remainingCells = 42 - days.length
  for (let i = 1; i <= remainingCells; i++) {
    const d = new Date(year, month + 1, i)
    days.push({ date: d, isCurrentMonth: false, isToday: isSameDay(d, new Date()) })
  }
  
  return days
})

const isSameDay = (d1, d2) => {
  return d1.getDate() === d2.getDate() && 
         d1.getMonth() === d2.getMonth() && 
         d1.getFullYear() === d2.getFullYear()
}

const getEventsForDay = (date) => {
  return events.value.filter(e => isSameDay(new Date(e.start_time), date)).map(e => ({
    ...e,
    time: new Date(e.start_time).toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })
  }))
}

const fetchEvents = async () => {
  try {
    // Check if user is customer (crudely via sectorStore or let api handle it)
    // Better: Helper to check role
    const isCustomer = !localStorage.getItem('user')?.includes('admin') // Simple check
    
    const endpoint = isCustomer ? '/portal/appointments' : '/interactions'
    
    const response = await axios.get(endpoint, { params: { limit: 100 } })
    
    // Normalize data structure or use rich dummy data if empty
    if (response.data.length === 0) {
      const today = new Date()
      const y = today.getFullYear()
      const m = today.getMonth()
      const d = today.getDate()
      
      events.value = [
        { id: 1, title: 'Haftalık Senkronizasyon', start_time: new Date(y, m, d, 10, 0), status: 'confirmed', color: 'primary', time: '10:00' },
        { id: 2, title: 'Müşteri Sunumu: Teknik Altyapı', start_time: new Date(y, m, d + 1, 14, 30), status: 'pending', color: 'accent', time: '14:30' },
        { id: 3, title: 'Sistem Bakım Çalışması', start_time: new Date(y, m, d - 2, 22, 0), status: 'confirmed', color: 'red', time: '22:00' },
        { id: 4, title: 'KVKK Danışmanlık Görüşmesi', start_time: new Date(y, m, d + 2, 9, 0), status: 'pending', color: 'secondary', time: '09:00' },
        { id: 5, title: 'Yeni Özellik Tanıtımı', start_time: new Date(y, m, d + 3, 11, 0), status: 'confirmed', color: 'primary', time: '11:00' },
        { id: 6, title: 'İptal Edilen Proje Toplantısı', start_time: new Date(y, m, d - 1, 15, 0), status: 'cancelled', color: 'red', time: '15:00' },
        { id: 7, title: 'Aylık Strateji Planlama', start_time: new Date(y, m, d + 5, 13, 0), status: 'pending', color: 'accent', time: '13:00' },
        { id: 8, title: 'Eğitim: Portal Kullanımı', start_time: new Date(y, m, d + 1, 16, 0), status: 'confirmed', color: 'secondary', time: '16:00' },
        { id: 9, title: 'Yıllık Bütçe Onayı', start_time: new Date(y, m, 5, 10, 0), status: 'confirmed', color: 'primary', time: '10:00' },
        { id: 10, title: 'Freelancer Görüşmesi', start_time: new Date(y, m, 12, 14, 0), status: 'pending', color: 'accent', time: '14:00' },
        { id: 11, title: 'Siber Güvenlik Denetimi', start_time: new Date(y, m, 18, 9, 0), status: 'confirmed', color: 'red', time: '09:00' },
        { id: 12, title: 'Pazarlama Kampanyası Review', start_time: new Date(y, m, 22, 11, 30), status: 'pending', color: 'secondary', time: '11:30' },
        { id: 13, title: 'Ofis Partisi', start_time: new Date(y, m, 28, 17, 0), status: 'confirmed', color: 'accent', time: '17:00' },
        { id: 14, title: 'Performans Değerlendirmeleri', start_time: new Date(y, m, 3, 9, 0), status: 'confirmed', color: 'primary', time: '09:00' },
        { id: 15, title: 'Yatırımcı Toplantısı', start_time: new Date(y, m, 15, 11, 0), status: 'pending', color: 'secondary', time: '11:00' }
      ]
    } else {
      events.value = response.data.map(e => ({
          ...e,
          start_time: e.date || e.start_time,
          title: e.title || e.type || 'Randevu'
      }))
    }
  } catch (e) {
    console.error("Calendar events fetch error:", e)
  }
}

const changeMonth = (delta) => {
  const d = new Date(currentDate.value)
  d.setMonth(d.getMonth() + delta)
  currentDate.value = d
}

const selectDay = (day) => {
  console.log("Selected:", day.date)
}

const getColor = (colorName) => {
    const themeColors = sectorStore.theme || {}
    return themeColors[colorName] || themeColors.primary || '#0ea5e9'
}

onMounted(fetchEvents)
</script>

<style scoped>
.calendar-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 32px;
  color: var(--text-primary);
}

.header-controls {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.title-group h2 {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 4px;
}

.subtitle {
  color: var(--text-secondary);
  font-size: 14px;
}

.controls-right {
  display: flex;
  gap: 16px;
  align-items: center;
}

.month-selector {
  display: flex;
  align-items: center;
  gap: 8px;
}

.month-selector h2 {
  font-size: 20px;
  font-weight: 600;
  min-width: 200px;
  text-align: center;
}

.nav-btn {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 8px;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
}

.nav-btn:hover {
  background: var(--surface-hover);
  color: var(--text-primary);
}

.filters {
  display: flex;
  background: var(--surface-elevated);
  border-radius: 8px;
  padding: 4px;
  border: 1px solid var(--border-subtle);
}

.view-btn {
  padding: 6px 12px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-size: 13px;
  cursor: pointer;
  border-radius: 6px;
}

.view-btn.active {
  background: var(--current-accent);
  color: white;
  font-weight: 600;
}

.add-btn {
  background: var(--current-accent);
  color: white;
  border: none;
  padding: 0 20px;
  height: 44px;
  border-radius: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 12px var(--current-glow);
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px var(--current-glow-strong);
}

.calendar-content-grid {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 32px;
  flex: 1;
}

.calendar-wrapper {
  background: var(--surface-elevated);
  border-radius: 24px;
  padding: 24px;
  border: 1px solid var(--border-subtle);
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1px;
  background: var(--border-subtle);
  border: 1px solid var(--border-subtle);
  border-radius: 16px;
  overflow: hidden;
}

.weekday-header {
  background: var(--surface-elevated);
  padding: 12px;
  text-align: center;
  font-weight: 600;
  color: var(--text-muted);
  font-size: 13px;
}

.calendar-day {
  background: var(--obsidian-black);
  min-height: 120px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s;
  animation: appear 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
}

.calendar-day:hover {
  background: var(--surface-elevated);
}

.calendar-day.other-month {
  background: rgba(255, 255, 255, 0.02);
  color: var(--text-muted);
}

.calendar-day.today {
  background: rgba(var(--current-rgb), 0.1);
}

.day-number {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 4px;
}

.calendar-day.today .day-number {
  color: var(--current-accent);
}

.events-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
  overflow-y: auto;
  flex: 1;
}

.event-pill {
  font-size: 11px;
  padding: 4px 8px;
  border-radius: 6px;
  background: var(--surface-elevated);
  border-left: 3px solid var(--current-accent);
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: flex;
  gap: 6px;
}

.event-pill.primary { border-left-color: var(--current-accent); }
.event-pill.accent { border-left-color: #8b5cf6; }
.event-pill.secondary { border-left-color: #06b6d4; }
.event-pill.red { border-left-color: #ef4444; }

.event-time {
    font-weight: 700;
    opacity: 0.7;
}

.event-title {
    font-weight: 500;
}

.event-pill.pending {
  opacity: 0.7;
  border-left-style: dashed;
}

/* Sidebar Styles */
.upcoming-sidebar {
    background: var(--surface-elevated);
    border-radius: 24px;
    padding: 24px;
    border: 1px solid var(--border-subtle);
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.upcoming-sidebar h3 {
    font-size: 18px;
    font-weight: 700;
}

.upcoming-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.upcoming-item {
    display: flex;
    gap: 16px;
    align-items: center;
    padding: 12px;
    background: var(--obsidian-black);
    border-radius: 16px;
    border: 1px solid var(--border-subtle);
    transition: all 0.3s;
}

.upcoming-item:hover {
    border-color: var(--current-accent);
    transform: translateX(4px);
}

.item-date {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-width: 50px;
    height: 50px;
    background: var(--surface-elevated);
    border-radius: 12px;
    border: 1px solid var(--border-subtle);
}

.item-date .day {
    font-size: 18px;
    font-weight: 800;
    color: var(--current-accent);
    line-height: 1;
}

.item-date .month {
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    opacity: 0.6;
}

.item-info h4 {
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 2px;
}

.item-info p {
    font-size: 12px;
    color: var(--text-muted);
}

.storage-info {
    margin-top: auto;
    padding-top: 24px;
    border-top: 1px solid var(--border-subtle);
}

.storage-labels {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 8px;
}

.storage-bar {
    height: 6px;
    background: var(--obsidian-black);
    border-radius: 3px;
    overflow: hidden;
}

.storage-fill {
    height: 100%;
    background: var(--current-accent);
    border-radius: 3px;
    box-shadow: 0 0 10px var(--current-glow);
}

.event-pill.confirmed {
  background: rgba(16, 185, 129, 0.1);
  border-left-color: #10b981;
  color: #10b981;
}

.event-pill.pending {
  background: rgba(245, 158, 11, 0.1);
  border-left-color: #f59e0b;
  color: #f59e0b;
}

.event-pill.cancelled {
  background: rgba(239, 68, 68, 0.1);
  border-left-color: #ef4444;
  color: #ef4444;
}

@keyframes appear {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}
</style>
