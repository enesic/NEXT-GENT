<template>
  <div class="luxury-chart glass-panel">
    <div class="chart-header">
      <h3 class="chart-title">{{ title }}</h3>
      <div v-if="period" class="chart-period">{{ period }}</div>
    </div>
    
    <div class="chart-container">
      <apexchart
        :type="type"
        :height="height"
        :options="chartOptions"
        :series="series"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: 'area' // area, bar, or heatmap
  },
  series: {
    type: Array,
    required: true
  },
  categories: {
    type: Array,
    default: () => []
  },
  height: {
    type: Number,
    default: 300
  },
  details: {
    type: Object,
    default: () => ({})
  },
  color: {
    type: String,
    default: '#6366f1' // Indigo primary
  },
  period: String
})

const isLight = computed(() => document.body.classList.contains('light-mode'))

const chartOptions = computed(() => {
  const mode = isLight.value ? 'light' : 'dark'
  
  return {
    chart: {
      type: props.type,
      background: 'transparent',
      toolbar: { show: false },
      sparkline: { enabled: false },
      animations: {
        enabled: true,
        easing: 'easeinout',
        speed: 800
      }
    },
    colors: [props.color, '#8b5cf6', '#ec4899'],
    stroke: {
      curve: 'smooth',
      width: 3,
      lineCap: 'round'
    },
    fill: {
      type: 'gradient',
      gradient: {
        shade: mode,
        type: 'vertical',
        shadeIntensity: 0.5,
        gradientToColors: ['#8b5cf6'],
        inverseColors: true,
        opacityFrom: 0.6,
        opacityTo: 0.1,
        stops: [0, 100]
      }
    },
    grid: {
      show: false,
      padding: {
        top: 0,
        right: 0,
        bottom: 0,
        left: 10
      }
    },
    xaxis: {
      categories: props.categories,
      axisBorder: { show: false },
      axisTicks: { show: false },
      labels: {
        style: {
          colors: isLight.value ? '#64748b' : '#94a3b8',
          fontSize: '11px',
          fontFamily: 'Inter, sans-serif'
        }
      },
      tooltip: { enabled: false }
    },
    yaxis: {
      show: true,
      labels: {
        style: {
          colors: isLight.value ? '#64748b' : '#94a3b8',
          fontSize: '11px',
          fontFamily: 'Inter, sans-serif'
        },
        formatter: (val) => {
           if (val >= 1000) return (val / 1000).toFixed(1) + 'k'
           return val
        }
      }
    },
    theme: {
      mode: mode
    },
    tooltip: {
      theme: mode,
      style: {
        fontSize: '12px',
        fontFamily: 'Inter, sans-serif'
      },
      x: { show: true },
      y: {
        formatter: (val) => val
      },
      marker: { show: false }
    },
    dataLabels: { enabled: false },
    legend: { show: false },
    ...props.details
  }
})
</script>

<style scoped>
.luxury-chart {
  padding: 20px;
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  gap: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
}

.luxury-chart:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 20px rgba(99, 102, 241, 0.15); /* Soft glow on hover */
  border-color: rgba(99, 102, 241, 0.3);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.chart-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.chart-period {
  font-size: 12px;
  color: var(--text-muted);
  font-weight: 500;
}

.chart-container {
  min-height: 300px;
}
</style>
