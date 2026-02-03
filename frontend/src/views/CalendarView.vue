<template>
  <div class="calendar-layout">
    <div class="header-controls">
      <div class="month-selector">
        <button class="nav-btn" @click="changeMonth(-1)">
          <ChevronLeft :size="20" />
        </button>
        <h2>{{ currentMonthName }} {{ currentYear }}</h2>
        <button class="nav-btn" @click="changeMonth(1)">
          <ChevronRight :size="20" />
        </button>
      </div>
      <div class="filters">
        <button class="view-btn active">Ay</button>
        <button class="view-btn">Hafta</button>
        <button class="view-btn">Liste</button>
      </div>
    </div>

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
        @click="selectDay(day)"
      >
        <div class="day-number">{{ day.date.getDate() }}</div>
        
        <div class="events-list">
          <div 
            v-for="event in getEventsForDay(day.date)" 
            :key="event.id"
            class="event-pill"
            :class="event.status.toLowerCase()"
          >
            {{ event.time }} {{ event.title }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue'
import { ChevronLeft, ChevronRight } from 'lucide-vue-next'
import { useSectorStore } from '../stores/sector'

const axios = inject('axios')
const sectorStore = useSectorStore()

const currentDate = ref(new Date())
const events = ref([])
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
    const res = await axios.get('/interactions', { params: { limit: 100 } })
    events.value = res.data
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

onMounted(fetchEvents)
</script>

<style scoped>
.calendar-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
  color: var(--text-primary);
}

.header-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.month-selector {
  display: flex;
  align-items: center;
  gap: 16px;
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
  background: var(--surface-hover);
  color: var(--text-primary);
  font-weight: 600;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1px;
  background: var(--border-subtle);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  overflow: hidden;
  flex: 1;
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
  min-height: 100px;
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  cursor: pointer;
  transition: background 0.2s;
}

.calendar-day:hover {
  background: var(--surface-hover);
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
  font-size: 10px;
  padding: 2px 4px;
  border-radius: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  background: var(--surface-elevated);
  border-left: 2px solid var(--text-muted);
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
</style>
