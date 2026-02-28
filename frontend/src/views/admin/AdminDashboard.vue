<template>
  <div class="classic-dashboard">


    <!-- Top Stats Row (4 Columns to spread everywhere) -->
    <div class="top-stats">
      <!-- Total Users -->
      <div class="stat-card">
        <div class="stat-icon-wrapper purple">
            <Users :size="24" color="#a855f7" />
        </div>
        <div class="stat-info">
            <span class="label">TOPLAM KULLANICI</span>
            <span class="value">2,543</span>
            <div class="stat-meta">
                 <span class="change positive">
                    <TrendingUp :size="14" /> 12.5%
                </span>
                <span class="muted">vs geçen ay</span>
            </div>
        </div>
      </div>

      <!-- Monthly Income -->
      <div class="stat-card">
        <div class="stat-icon-wrapper pink">
            <DollarSign :size="24" color="#ec4899" />
        </div>
        <div class="stat-info">
            <span class="label">AYLIK GELİR</span>
            <span class="value">₺45,231</span>
            <div class="stat-meta">
                <span class="change positive">
                    <TrendingUp :size="14" /> 8.2%
                </span>
                <span class="muted">vs geçen ay</span>
            </div>
        </div>
      </div>

      <!-- Active Calls -->
      <div class="stat-card">
        <div class="stat-icon-wrapper blue">
            <Phone :size="24" color="#0ea5e9" />
        </div>
        <div class="stat-info">
            <span class="label">AKTİF ÇAĞRILAR</span>
            <span class="value">1,234</span>
            <div class="stat-meta">
                <span class="change negative">
                    <TrendingDown :size="14" /> 3.1%
                </span>
                <span class="muted">vs geçen ay</span>
            </div>
        </div>
      </div>

      <!-- Success Rate (Moved here to fill width) -->
      <div class="stat-card">
         <div class="stat-icon-wrapper green">
            <Activity :size="24" color="#22c55e" />
        </div>
        <div class="stat-info">
            <span class="label">BAŞARI ORANI</span>
            <span class="value">94.2%</span>
            <div class="stat-meta">
                <span class="change positive">
                    <TrendingUp :size="14" /> 2.4%
                </span>
                <span class="muted">vs geçen ay</span>
            </div>
        </div>
      </div>
    </div>

    <!-- Charts Row -->
    <div class="charts-grid">
        <!-- Weekly Traffic (Line Chart) -->
        <div class="chart-card large">
            <div class="chart-header">
                <div>
                    <h3>Haftalık Trafik</h3>
                    <p>Son 7 günlük aktivite</p>
                </div>
                <select class="chart-select">
                    <option>Son 7 Gün</option>
                </select>
            </div>
            <div class="chart-container">
                <canvas ref="trafficChartEl"></canvas>
            </div>
        </div>

        <!-- System Performance (Donut) -->
        <div class="chart-card small">
            <div class="chart-header">
                <div>
                     <h3>Sistem Performansı</h3>
                     <p>Başarı oranları</p>
                </div>
            </div>
             <div class="chart-container donut-container">
                <canvas ref="performanceChartEl"></canvas>
            </div>
             <div class="chart-legend center">
                <div class="legend-item"><span class="dot green"></span>Başarılı</div>
                <div class="legend-item"><span class="dot purple"></span>Beklemede</div>
                <div class="legend-item"><span class="dot red"></span>Başarısız</div>
            </div>
        </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Chart, registerables } from 'chart.js'
import { Users, DollarSign, Phone, Activity, TrendingUp, TrendingDown, Bell, Settings } from 'lucide-vue-next'

Chart.register(...registerables)

const trafficChartEl = ref(null)
const performanceChartEl = ref(null)

onMounted(() => {
    // Traffic Chart
    if (trafficChartEl.value) {
        new Chart(trafficChartEl.value, {
            type: 'line',
            data: {
                labels: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
                datasets: [
                    {
                        label: 'Çağrılar',
                        data: [65, 78, 90, 81, 56, 55, 40],
                        borderColor: '#3b82f6', // Mobile Blue
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        tension: 0.4,
                        fill: true,
                        pointBackgroundColor: '#1e1e2e',
                        borderWidth: 2
                    },
                    {
                        label: 'Mesajlar',
                        data: [45, 52, 65, 59, 48, 42, 35],
                        borderColor: '#a855f7', // Purple
                        backgroundColor: 'transparent',
                        tension: 0.4,
                        borderDash: [5, 5],
                        pointBackgroundColor: '#1e1e2e',
                        borderWidth: 2
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                plugins: { 
                    legend: { display: false },
                    tooltip: {
                        enabled: true,
                        backgroundColor: '#1e1e2e',
                        titleColor: '#fff',
                        bodyColor: '#94a3b8',
                        borderColor: '#334155',
                        borderWidth: 1,
                        padding: 10,
                        displayColors: true,
                        usePointStyle: true,
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed.y !== null) {
                                    label += context.parsed.y;
                                }
                                return label;
                            }
                        }
                    }
                },
                scales: {
                    y: { 
                        beginAtZero: true, 
                        grid: { color: 'rgba(255,255,255,0.05)' },
                        ticks: { color: '#64748b' }
                    },
                    x: { 
                        grid: { display: false },
                        ticks: { color: '#64748b' }
                    }
                }
            }
        })
    }

    // Performance Chart
    if (performanceChartEl.value) {
        new Chart(performanceChartEl.value, {
            type: 'doughnut',
            data: {
                labels: ['Başarılı', 'Beklemede', 'Başarısız'],
                datasets: [{
                    data: [75, 15, 10],
                    backgroundColor: ['#22c55e', '#d8b4fe', '#ef4444'], // Green, Light Purple, Red
                    borderWidth: 0,
                    cutout: '70%'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } }
            }
        })
    }
})
</script>

<style scoped>
.classic-dashboard {
    width: 100%;
    min-width: 100%; /* Ensure it doesn't shrink */
    max-width: none !important; /* Force override any hidden limits */
    padding: 32px 40px; 
    background: var(--bg-main); 
    color: #fff;
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
}

.dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;
}

.page-title {
    font-size: 24px;
    font-weight: 700;
    margin: 0;
}

.subtitle {
    color: #64748b;
    font-size: 14px;
    margin-top: 4px;
}

.header-actions {
    display: flex;
    align-items: center;
    gap: 16px;
}

.icon-btn {
    background: transparent;
    border: 1px solid #334155;
    color: #94a3b8;
    width: 40px;
    height: 40px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
}

.icon-btn:hover {
    background: #1e293b;
    color: #fff;
}

.user-chip {
    display: flex;
    align-items: center;
    gap: 12px;
    background: #1e293b;
    padding: 8px 16px 8px 8px;
    border-radius: 12px;
    border: 1px solid #334155;
}

.avatar {
    width: 32px;
    height: 32px;
    background: #6366f1;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
}

.info {
    display: flex;
    flex-direction: column;
}

.name { font-size: 14px; font-weight: 600; }
.role { font-size: 11px; color: #94a3b8; }

.top-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 32px; 
    margin-bottom: 32px;
    margin-top: 10px;
    width: 100%;
}

.stat-card {
    flex: 1; /* Allow cards to grow if needed */
    min-width: 0; /* Prevent overflow issues in flex/grid */
}

@keyframes appear {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.stat-card {
    background: var(--bg-surface);
    border: 1px solid #1f1f23;
    border-radius: 16px;
    padding: 24px;
    display: flex;
    gap: 16px;
    align-items: center;
    animation: appear 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    opacity: 0; /* Init hidden */
    transform: translateY(20px);
    transition: transform 0.3s ease, box-shadow 0.3s ease; /* Add transition for hover */
    cursor: pointer;
}

.stat-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px -10px rgba(168, 85, 247, 0.15); /* Subtle purple glow */
    border-color: #334155;
    background: #141417;
}

/* Stagger delays */
.stat-card:nth-child(1) { animation-delay: 0.1s; }
.stat-card:nth-child(2) { animation-delay: 0.2s; }
.stat-card:nth-child(3) { animation-delay: 0.3s; }
.stat-card:nth-child(4) { animation-delay: 0.4s; }

.stat-icon-wrapper {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.stat-icon-wrapper.purple { background: rgba(168, 85, 247, 0.1); }
.stat-icon-wrapper.pink { background: rgba(236, 72, 153, 0.1); }
.stat-icon-wrapper.blue { background: rgba(14, 165, 233, 0.1); }
.stat-icon-wrapper.green { background: rgba(34, 197, 94, 0.1); }

.stat-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
    flex: 1;
}

.label {
    font-size: 11px;
    font-weight: 600;
    color: #94a3b8;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.value {
    font-size: 24px;
    font-weight: 700;
    color: #fff;
}

.stat-meta {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 4px;
}

.change {
    font-size: 12px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 2px;
}

.change.positive { color: #22c55e; }
.change.negative { color: #ef4444; }

.muted {
    color: #475569;
    font-size: 11px;
}

.charts-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 32px;
    width: 100%;
    margin-top: 10px;
}

.chart-card {
    background: var(--bg-surface);
    border: 1px solid #1f1f23;
    border-radius: 16px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    /* Entrance Animation */
    animation: appear 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    opacity: 0;
    transform: translateY(20px);
    animation-delay: 0.5s;
}

.chart-card.small { animation-delay: 0.6s; }

.chart-card.large { 
    flex: 2;
    min-width: 500px;
    min-height: 350px; 
}
.chart-card.small { 
    flex: 1;
    min-width: 300px;
    min-height: 350px; 
}

.chart-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 24px;
}

.chart-header h3 { font-size: 16px; font-weight: 600; margin: 0; }
.chart-header p { font-size: 12px; color: #64748b; margin-top: 4px; }

.chart-select {
    background: #18181b;
    border: 1px solid #27272a;
    color: #fff;
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 12px;
    outline: none;
}

.chart-container {
    flex: 1;
    position: relative;
    width: 100%;
}

.donut-container {
    display: flex;
    justify-content: center;
    align-items: center;
}

.chart-legend {
    display: flex;
    gap: 16px;
    margin-top: 16px;
    justify-content: center;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: #94a3b8;
}

.dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

.dot.blue { background: #3b82f6; }
.dot.purple { background: #a855f7; }
.dot.green { background: #22c55e; }
.dot.red { background: #ef4444; }

@media (max-width: 1400px) {
    .charts-grid { grid-template-columns: 3fr 2fr; }
}

@media (max-width: 1200px) {
    .top-stats { grid-template-columns: repeat(2, 1fr); }
    .charts-grid { grid-template-columns: 1fr; }
    .chart-card { min-height: 350px; }
}

@media (max-width: 768px) {
    .top-stats { grid-template-columns: 1fr; }
    .dashboard-header { flex-direction: column; align-items: flex-start; gap: 16px; }
}
</style>
