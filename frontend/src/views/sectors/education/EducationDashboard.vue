<template>
  <DashboardLayout sector="education" :sector-icon="GraduationCap">
    <!-- Stats Overview -->
    <section class="stats-grid">
      <StatCard
        :icon="Users"
        label="Toplam Öğrenci"
        :value="stats.totalStudents"
        change="+5.2%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/students')"
      />
      <StatCard
        :icon="BookOpen"
        label="Aktif Dersler"
        :value="stats.activeCourses"
        change="+3.1%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/courses')"
      />
      <StatCard
        :icon="TrendingUp"
        label="Ortalama Başarı"
        :value="`${stats.averageGrade}%`"
        change="+2.8%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        :animated="false"
        @click="navigateTo('/performance')"
      />
      <StatCard
        :icon="Calendar"
        label="Bugünkü Etkinlikler"
        :value="stats.todayEvents"
        change="+1.5%"
        changeType="positive"
        :gradient="theme.primaryGradient"
        @click="navigateTo('/events')"
      />
    </section>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- Class Schedule -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">Bugünkü Ders Programı</h3>
        </div>
        <div class="schedule-list">
          <div 
            v-for="classItem in todaySchedule" 
            :key="classItem.id"
            class="schedule-item"
            @click="handleClassClick(classItem)"
          >
            <div class="schedule-time">
              <Clock :size="16" />
              <span>{{ classItem.time }}</span>
            </div>
            <div class="schedule-info">
              <p class="class-name">{{ classItem.name }}</p>
              <p class="class-details">{{ classItem.teacher }} • {{ classItem.room }}</p>
            </div>
            <div class="class-attendance">
              <Users :size="14" />
              <span>{{ classItem.attendance }}/{{ classItem.capacity }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Student Performance -->
      <section class="card chart-card">
        <div class="card-header">
          <h3 class="card-title">Öğrenci Performansı</h3>
          <div class="time-filters">
            <button 
              v-for="filter in timeFilters" 
              :key="filter.value"
              class="filter-btn" 
              :class="{ active: selectedTimeFilter === filter.value }"
              @click="selectedTimeFilter = filter.value"
            >
              {{ filter.label }}
            </button>
          </div>
        </div>
        <div class="chart-wrapper">
          <InteractiveChart
            type="line"
            :data="performanceData"
            :gradient-colors="['rgba(245, 158, 11, 0.8)', 'rgba(245, 158, 11, 0.1)']"
          />
        </div>
      </section>

      <!-- Enrollment Stats -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">Kayıt İstatistikleri</h3>
        </div>
        <div class="enrollment-stats">
          <div 
            v-for="dept in departments" 
            :key="dept.id"
            class="dept-item"
          >
            <div class="dept-info">
              <div class="dept-icon" :style="{ background: dept.gradient }">
                <component :is="dept.icon" :size="20" />
              </div>
              <div>
                <p class="dept-name">{{ dept.name }}</p>
                <p class="dept-count">{{ dept.students }} öğrenci</p>
              </div>
            </div>
            <div class="dept-chart">
              <div class="chart-bar">
                <div class="chart-fill" :style="{ width: `${dept.percent}%`, background: dept.gradient }"></div>
              </div>
              <span class="chart-percent">{{ dept.percent }}%</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Teacher Assignments -->
      <section class="card">
        <div class="card-header">
          <h3 class="card-title">Öğretmen Atamaları</h3>
        </div>
        <div class="teachers-list">
          <div 
            v-for="teacher in teachers" 
            :key="teacher.id"
            class="teacher-item"
          >
            <div class="teacher-avatar" :style="{ background: teacher.avatarColor }">
              {{ teacher.name[0] }}
            </div>
            <div class="teacher-info">
              <p class="teacher-name">{{ teacher.name }}</p>
              <p class="teacher-subject">{{ teacher.subject }}</p>
            </div>
            <div class="teacher-stats">
              <div class="stat">
                <BookOpen :size="14" />
                <span>{{ teacher.courses }} ders</span>
              </div>
              <div class="stat">
                <Users :size="14" />
                <span>{{ teacher.students }} öğrenci</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Event Calendar -->
      <section class="card">
        <ActivityFeed
          title="Yaklaşan Etkinlikler"
          :items="upcomingEvents"
          @item-click="handleEventClick"
          @view-all="navigateTo('/events')"
        />
      </section>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { 
  GraduationCap, Users, BookOpen, TrendingUp, Calendar,
  Clock, Beaker, Calculator, Globe
} from 'lucide-vue-next'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import StatCard from '@/components/dashboard/StatCard.vue'
import ActivityFeed from '@/components/dashboard/ActivityFeed.vue'
import InteractiveChart from '@/components/dashboard/InteractiveChart.vue'
import { useSectorTheme } from '@/composables/useSectorTheme'
import { vRipple } from '@/composables/useRipple'

const router = useRouter()
const { theme } = useSectorTheme('education')

// Stats
const stats = ref({
  totalStudents: 1247,
  activeCourses: 42,
  averageGrade: 78,
  todayEvents: 5
})

// Time Filters
const timeFilters = [
  { label: 'Bu Ay', value: '1m' },
  { label: 'Bu Dönem', value: 'semester' },
  { label: 'Bu Yıl', value: '1y' }
]
const selectedTimeFilter = ref('semester')

// Today's Schedule
const todaySchedule = ref([
  {
    id: 1,
    time: '09:00',
    name: 'Matematik 101',
    teacher: 'Dr. Ahmet Yılmaz',
    room: 'A-205',
    attendance: 28,
    capacity: 30
  },
  {
    id: 2,
    time: '11:00',
    name: 'Fizik 201',
    teacher: 'Prof. Ayşe Demir',
    room: 'B-104',
    attendance: 25,
    capacity: 30
  },
  {
    id: 3,
    time: '14:00',
    name: 'Kimya 301',
    teacher: 'Doç. Mehmet Kaya',
    room: 'C-302',
    attendance: 22,
    capacity: 25
  }
])

// Performance Data
const performanceData = computed(() => ({
  labels: ['Eylül', 'Ekim', 'Kasım', 'Aralık', 'Ocak', 'Şubat'],
  datasets: [{
    label: 'Ortalama Not',
    data: [72, 74, 76, 75, 77, 78]
  }]
}))

// Departments
const departments = ref([
  {
    id: 1,
    name: 'Fen Bilimleri',
    icon: Beaker,
    gradient: 'linear-gradient(135deg, #f59e0b, #fbbf24)',
    students: 345,
    percent: 85
  },
  {
    id: 2,
    name: 'Matematik',
    icon: Calculator,
    gradient: 'linear-gradient(135deg, #3b82f6, #60a5fa)',
    students: 298,
    percent: 72
  },
  {
    id: 3,
    name: 'Sosyal Bilimler',
    icon: Globe,
    gradient: 'linear-gradient(135deg, #10b981, #34d399)',
    students: 412,
    percent: 95
  }
])

// Teachers
const teachers = ref([
  {
    id: 1,
    name: 'Dr. Ahmet Yılmaz',
    subject: 'Matematik',
    avatarColor: 'linear-gradient(135deg, #f59e0b, #fbbf24)',
    courses: 4,
    students: 120
  },
  {
    id: 2,
    name: 'Prof. Ayşe Demir',
    subject: 'Fizik',
    avatarColor: 'linear-gradient(135deg, #3b82f6, #60a5fa)',
    courses: 3,
    students: 90
  },
  {
    id: 3,
    name: 'Doç. Mehmet Kaya',
    subject: 'Kimya',
    avatarColor: 'linear-gradient(135deg, #10b981, #34d399)',
    courses: 3,
    students: 75
  }
])

// Upcoming Events
const upcomingEvents = ref([
  {
    id: 1,
    icon: Calendar,
    iconGradient: 'linear-gradient(135deg, #f59e0b, #fbbf24)',
    title: 'Bilim Fuarı',
    subtitle: 'Ana Salon • 15 Şubat',
    time: '4 gün',
    badge: 'Yaklaşıyor',
    badgeType: 'warning'
  },
  {
    id: 2,
    icon: Calendar,
    iconGradient: 'linear-gradient(135deg, #3b82f6, #60a5fa)',
    title: 'Veli Toplantısı',
    subtitle: 'Konferans Salonu • 20 Şubat',
    time: '9 gün',
    badge: 'Planlandı',
    badgeType: 'info'
  }
])

// Methods
const navigateTo = (path) => {
  console.log('Navigate to:', path)
}

const handleClassClick = (classItem) => {
  console.log('Class clicked:', classItem)
}

const handleEventClick = (event) => {
  console.log('Event clicked:', event)
}
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 24px;
}

.card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 24px;
  transition: all 0.3s;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  border-color: rgba(255, 255, 255, 0.12);
}

.card:nth-child(1) { grid-column: span 4; }
.card:nth-child(2) { grid-column: span 8; }
.card:nth-child(3) { grid-column: span 4; }
.card:nth-child(4) { grid-column: span 4; }
.card:nth-child(5) { grid-column: span 4; }

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: white;
}

.time-filters {
  display: flex;
  gap: 8px;
}

.filter-btn {
  padding: 6px 14px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: #9ca3af;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  color: white;
}

.filter-btn.active {
  background: var(--sector-gradient);
  color: white;
  border-color: transparent;
}

.chart-wrapper {
  height: 280px;
}

/* Schedule */
.schedule-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.schedule-item {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.schedule-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  transform: translateX(4px);
}

.schedule-time {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--sector-accent);
  font-weight: 600;
  min-width: 80px;
}

.schedule-info {
  flex: 1;
}

.class-name {
  font-size: 14px;
  font-weight: 600;
  color: white;
  margin: 0 0 4px 0;
}

.class-details {
  font-size: 12px;
  color: #9ca3af;
  margin: 0;
}

.class-attendance {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #9ca3af;
  font-weight: 600;
}

/* Enrollment */
.enrollment-stats {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.dept-item {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
}

.dept-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.dept-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.dept-name {
  font-size: 14px;
  font-weight: 600;
  color: white;
  margin: 0 0 4px 0;
}

.dept-count {
  font-size: 12px;
  color: #9ca3af;
  margin: 0;
}

.dept-chart {
  display: flex;
  align-items: center;
  gap: 12px;
}

.chart-bar {
  flex: 1;
  height: 6px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 3px;
  overflow: hidden;
}

.chart-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

.chart-percent {
  font-size: 12px;
  font-weight: 600;
  color: white;
  min-width: 40px;
  text-align: right;
}

/* Teachers */
.teachers-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.teacher-item {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.teacher-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 16px;
}

.teacher-info {
  flex: 1;
}

.teacher-name {
  font-size: 14px;
  font-weight: 600;
  color: white;
  margin: 0 0 4px 0;
}

.teacher-subject {
  font-size: 12px;
  color: #9ca3af;
  margin: 0;
}

.teacher-stats {
  display: flex;
  gap: 16px;
}

.stat {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #9ca3af;
  font-weight: 600;
}

@media (max-width: 1200px) {
  .content-grid > .card {
    grid-column: span 12 !important;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
