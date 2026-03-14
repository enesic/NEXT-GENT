<template>
  <div class="calendar-layout">
    <div class="header-controls">
      <div class="title-group">
        <h2>{{ route.name === 'Appointments' ? sectorStore.t('appointments_title') : sectorStore.t('calendar_title') }}</h2>
        <p class="subtitle">{{ events.length }} {{ sectorStore.t('events_count') }}</p>
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
          <button 
            class="view-btn" 
            :class="{ active: currentView === 'month' }"
            @click="currentView = 'month'"
          >
            {{ sectorStore.t('month_view') }}
          </button>
          <button 
            class="view-btn" 
            :class="{ active: currentView === 'week' }"
            @click="currentView = 'week'"
          >
            {{ sectorStore.t('week_view') }}
          </button>
          <button 
            class="view-btn" 
            :class="{ active: currentView === 'list' }"
            @click="currentView = 'list'"
          >
            {{ sectorStore.t('list_view') }}
          </button>
        </div>
        <button class="add-btn" @click="showAppointmentModal = true">
          <Plus :size="18" />
          {{ sectorStore.t('new_appointment') }}
        </button>
      </div>
    </div>

    <div class="calendar-content-grid">
      <div class="calendar-wrapper">
        <!-- Month View -->
        <div v-if="currentView === 'month'" class="calendar-grid">
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

        <!-- Week View -->
        <div v-else-if="currentView === 'week'" class="week-view">
          <div class="week-header">
            <div class="time-spacer"></div>
            <div v-for="day in currentWeekDays" :key="day.date" class="week-col-header" :class="{ today: day.isToday }">
              <span class="day-name">{{ day.dayName }}</span>
              <span class="day-num">{{ day.date.getDate() }}</span>
            </div>
          </div>
          <div class="week-body">
            <div class="time-column">
              <div v-for="hour in 13" :key="hour" class="hour-label">
                {{ hour + 7 }}:00
              </div>
            </div>
            <div class="week-grid">
              <div v-for="day in currentWeekDays" :key="day.date" class="week-col">
                <div v-for="hour in 13" :key="hour" class="hour-slot"></div>
                <div 
                  v-for="event in getEventsForDay(day.date)" 
                  :key="event.id"
                  class="week-event-pill"
                  :style="getEventStyle(event)"
                  :class="[event.status.toLowerCase(), event.color]"
                >
                  <span class="time">{{ event.time }}</span>
                  <span class="title">{{ event.title }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- List View -->
        <div v-else-if="currentView === 'list'" class="list-view">
          <div v-if="listEvents.length === 0" class="empty-list">
            {{ sectorStore.t('no_scheduled_events') }}
          </div>
          <div v-for="event in listEvents" :key="event.id" class="list-item" :class="event.color">
            <div class="item-date">
              <span class="day">{{ new Date(event.start_time).getDate() }}</span>
              <span class="month">{{ months[new Date(event.start_time).getMonth()] }}</span>
            </div>
            <div class="item-details">
              <h4>{{ event.title }}</h4>
              <div class="meta">
                <span>{{ new Date(event.start_time).toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }) }}</span>
                <span class="dot">•</span>
                <span class="status-badge" :class="event.status.toLowerCase()">{{ event.status }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Upcoming Sidebar -->
      <div class="upcoming-sidebar" v-if="route.name !== 'Appointments'">
          <h3>{{ sectorStore.t('upcoming_events') }}</h3>
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

  <!-- Appointment Modal -->
  <AppointmentModal
    v-model="showAppointmentModal"
    @created="fetchEvents"
  />
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ChevronLeft, ChevronRight, Plus } from 'lucide-vue-next'
import { useSectorStore } from '../stores/sector'
import { useRoute } from 'vue-router'
import AppointmentModal from '../components/common/AppointmentModal.vue'
import api from '@/config/api'

const sectorStore = useSectorStore()
const route = useRoute()

// State
const currentDate = ref(new Date())
const currentView = ref(route.name === 'Appointments' ? 'list' : 'month') // 'month', 'week', 'list'
const events = ref([])
const showAppointmentModal = ref(false)

const upcomingEvents = computed(() => {
    return events.value
        .filter(e => new Date(e.start_time) >= new Date())
        .sort((a,b) => new Date(a.start_time) - new Date(b.start_time))
        .slice(0, 5)
})

const currentWeekDays = computed(() => {
  const curr = new Date(currentDate.value)
  const first = curr.getDate() - ((curr.getDay() + 6) % 7) // Monday start
  
  return Array.from({ length: 7 }, (_, i) => {
    const d = new Date(curr.setDate(first + i))
    return {
      date: d,
      isToday: isSameDay(d, new Date()),
      dayName: weekDays[i]
    }
  })
})

const listEvents = computed(() => {
  return [...events.value].sort((a, b) => new Date(a.date) - new Date(b.date))
})

// Force list view if we are on appointments route
watch(
  () => route.name,
  (newName) => {
    if (newName === 'Appointments') {
      currentView.value = 'list'
    } else {
      currentView.value = 'month'
    }
  }
)

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

function toEventsArray(raw) {
  if (Array.isArray(raw)) return raw
  if (raw && Array.isArray(raw.data)) return raw.data
  if (raw && Array.isArray(raw.events)) return raw.events
  if (raw && Array.isArray(raw.appointments)) return raw.appointments
  if (raw && Array.isArray(raw.items)) return raw.items
  if (raw && Array.isArray(raw.results)) return raw.results
  return []
}

const fetchEvents = async () => {
  try {
    const isCustomer = !sessionStorage.getItem('user')?.includes('admin')
    const endpoint = isCustomer ? '/portal/appointments' : '/interactions'

    const response = await api.get(endpoint, { params: { limit: 100 } })
    const arr = toEventsArray(response?.data ?? {})

    if (arr.length === 0) {
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
      events.value = arr.map(e => ({
        ...e,
        start_time: e.date || e.start_time || e.created_at,
        title: e.title || e.summary || e.type || 'Randevu'
      }))
    }
  } catch {
    events.value = []
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

const getEventStyle = (event) => {
  const date = new Date(event.start_time)
  const hours = date.getHours()
  const minutes = date.getMinutes()
  
  if (hours < 8 || hours > 20) return { display: 'none' }
  
  const top = (hours - 8) * 60 + minutes
  return {
    top: `${top}px`,
    height: '50px' // Default fixed height for demo
  }
}

const getColor = (colorName) => {
    const themeColors = sectorStore.theme || {}
    return themeColors[colorName] || themeColors.primary || '#0ea5e9'
}

onMounted(fetchEvents)
</script>

<style scoped>
.calendar-layout {
  width: 100%;
  min-height: 100%;
  display: flex;
  flex-direction: column;
  gap: 28px;
  padding: 24px;
  box-sizing: border-box;
  color: var(--text-primary);
  overflow-x: hidden;
  min-width: 0;
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
  grid-template-columns: 1fr 300px;
  gap: 24px;
  flex: 1;
  min-width: 0;
  min-height: 600px;
}

.calendar-wrapper {
  background: var(--surface-elevated);
  border-radius: 24px;
  padding: 24px;
  border: 1px solid var(--border-subtle);
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
  overflow: hidden;  /* prevent today's events from overflowing */
  min-width: 0;      /* allow grid cell to shrink */
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
  background: var(--bg-main);
  min-height: 120px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s;
  animation: appear 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
  overflow: hidden;  /* prevent event pills from expanding the cell */
  min-width: 0;
  max-width: 100%;
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
    background: var(--bg-main);
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
    background: var(--bg-main);
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

/* Week View Styles */
.week-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.week-header {
  display: flex;
  border-bottom: 1px solid var(--border-subtle);
  background: var(--surface-elevated);
}

.time-spacer {
  width: 60px;
  flex-shrink: 0;
}

.week-col-header {
  flex: 1;
  padding: 12px;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 4px;
  border-left: 1px solid var(--border-subtle);
}

.week-col-header.today .day-name {
  color: var(--current-accent);
}

.week-col-header.today .day-num {
  background: var(--current-accent);
  color: white;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  margin: 0 auto;
}

.day-name {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
}

.day-num {
  font-size: 18px;
  font-weight: 700;
}

.week-body {
  display: flex;
  flex: 1;
  overflow-y: auto;
  position: relative;
}

.time-column {
  width: 60px;
  flex-shrink: 0;
  border-right: 1px solid var(--border-subtle);
}

.hour-label {
  height: 60px;
  font-size: 11px;
  color: var(--text-muted);
  text-align: center;
  padding-top: 4px;
}

.week-grid {
  flex: 1;
  display: flex;
  position: relative;
}

.week-col {
  flex: 1;
  position: relative;
  border-left: 1px solid var(--border-subtle);
}

.hour-slot {
  height: 60px;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}

.week-event-pill {
  position: absolute;
  left: 4px;
  right: 4px;
  padding: 6px;
  border-radius: 6px;
  font-size: 11px;
  z-index: 10;
  border-left: 3px solid var(--current-accent);
  display: flex;
  flex-direction: column;
  gap: 2px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.week-event-pill .time {
  font-weight: 800;
  font-size: 10px;
}

/* List View Styles */
.list-view {
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow-y: auto;
  height: 100%;
}

.list-item {
  display: flex;
  gap: 20px;
  padding: 16px;
  background: var(--bg-main);
  border-radius: 16px;
  border: 1px solid var(--border-subtle);
  transition: all 0.3s;
}

.list-item:hover {
  border-color: var(--current-accent);
  background: rgba(var(--current-rgb), 0.05);
  transform: translateX(4px);
}

.list-item .item-date {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 60px;
  height: 60px;
  background: var(--surface-elevated);
  border-radius: 12px;
}

.list-item.primary .item-date .day { color: var(--current-accent); }
.list-item.accent .item-date .day { color: #8b5cf6; }
.list-item.secondary .item-date .day { color: #06b6d4; }
.list-item.red .item-date .day { color: #ef4444; }

.item-details h4 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
}

.meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-muted);
}

.status-badge {
  text-transform: capitalize;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 20px;
  font-size: 11px;
}

.status-badge.confirmed { color: #10b981; background: rgba(16, 185, 129, 0.1); }
.status-badge.pending { color: #f59e0b; background: rgba(245, 158, 11, 0.1); }
.status-badge.cancelled { color: #ef4444; background: rgba(239, 68, 68, 0.1); }

.empty-list {
  text-align: center;
  padding: 40px;
  color: var(--text-muted);
  font-style: italic;
}

@media (max-width: 1024px) {
  .calendar-content-grid {
    grid-template-columns: 1fr;
    min-height: auto;
  }
}
</style>
