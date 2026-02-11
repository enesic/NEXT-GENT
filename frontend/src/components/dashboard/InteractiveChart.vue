<template>
  <div class="interactive-chart">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import {
  Chart,
  LineController,
  BarController,
  DoughnutController,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'

// Register Chart.js components
Chart.register(
  LineController,
  BarController,
  DoughnutController,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const props = defineProps({
  type: {
    type: String,
    required: true,
    validator: (value) => ['line', 'bar', 'doughnut'].includes(value)
  },
  data: {
    type: Object,
    required: true
  },
  options: {
    type: Object,
    default: () => ({})
  },
  gradient: {
    type: Boolean,
    default: true
  },
  gradientColors: {
    type: Array,
    default: () => ['rgba(99, 102, 241, 0.8)', 'rgba(139, 92, 246, 0.2)']
  }
})

const chartCanvas = ref(null)
let chartInstance = null

const defaultOptions = {
  responsive: true,
  maintainAspectRatio: false,
  animation: {
    duration: 1500,
    easing: 'easeInOutQuart'
  },
  interaction: {
    mode: 'nearest',
    intersect: false
  },
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      backgroundColor: 'rgba(17, 24, 39, 0.95)',
      titleColor: '#ffffff',
      bodyColor: '#d1d5db',
      borderColor: 'rgba(255, 255, 255, 0.1)',
      borderWidth: 1,
      padding: 12,
      cornerRadius: 8,
      displayColors: true,
      callbacks: {
        label: function(context) {
          let label = context.dataset.label || ''
          if (label) {
            label += ': '
          }
          if (context.parsed.y !== null) {
            label += new Intl.NumberFormat('tr-TR').format(context.parsed.y)
          }
          return label
        }
      }
    }
  },
  scales: {}
}

// Line/Bar specific defaults
if (props.type === 'line' || props.type === 'bar') {
  defaultOptions.scales = {
    x: {
      grid: {
        display: false,
        drawBorder: false
      },
      ticks: {
        color: '#9ca3af',
        font: {
          size: 11
        }
      }
    },
    y: {
      grid: {
        color: 'rgba(255, 255, 255, 0.05)',
        drawBorder: false
      },
      ticks: {
        color: '#9ca3af',
        font: {
          size: 11
        },
        callback: function(value) {
          return new Intl.NumberFormat('tr-TR', { notation: 'compact' }).format(value)
        }
      }
    }
  }
}

const createGradient = (ctx) => {
  const gradient = ctx.createLinearGradient(0, 0, 0, 400)
  gradient.addColorStop(0, props.gradientColors[0])
  gradient.addColorStop(1, props.gradientColors[1])
  return gradient
}

const initChart = () => {
  if (!chartCanvas.value) return

  const ctx = chartCanvas.value.getContext('2d')
  
  // Apply gradient to datasets if enabled
  const chartData = { ...props.data }
  if (props.gradient && chartData.datasets) {
    chartData.datasets = chartData.datasets.map((dataset, index) => {
      if (props.type === 'line') {
        return {
          ...dataset,
          backgroundColor: createGradient(ctx),
          borderColor: props.gradientColors[0],
          borderWidth: 2,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: props.gradientColors[0],
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6
        }
      } else if (props.type === 'bar') {
        return {
          ...dataset,
          backgroundColor: createGradient(ctx),
          borderRadius: 8,
          borderSkipped: false
        }
      }
      return dataset
    })
  }

  const mergedOptions = {
    ...defaultOptions,
    ...props.options,
    plugins: {
      ...defaultOptions.plugins,
      ...(props.options.plugins || {})
    },
    scales: {
      ...defaultOptions.scales,
      ...(props.options.scales || {})
    }
  }

  chartInstance = new Chart(ctx, {
    type: props.type,
    data: chartData,
    options: mergedOptions
  })
}

const updateChart = () => {
  if (chartInstance) {
    chartInstance.destroy()
  }
  initChart()
}

watch(() => props.data, updateChart, { deep: true })
watch(() => props.options, updateChart, { deep: true })

onMounted(() => {
  initChart()
})

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy()
  }
})
</script>

<style scoped>
.interactive-chart {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 200px;
}
</style>
