<template>
  <div ref="chartContainer" class="interactive-chart" :class="{ 'chart-visible': isVisible }">
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
  },
  animateOnView: {
    type: Boolean,
    default: true
  },
  staggerDelay: {
    type: Number,
    default: 50 // milliseconds between each data point animation
  }
})

const chartCanvas = ref(null)
const chartContainer = ref(null)
const isVisible = ref(false)
const hasAnimated = ref(false)
let chartInstance = null
let intersectionObserver = null

// Enhanced animation configuration with stagger
const getAnimationConfig = () => {
  const baseConfig = {
    duration: 1500,
    easing: 'easeOutQuart'
  }

  // Progressive reveal animation with stagger
  if (props.type === 'bar' || props.type === 'line') {
    return {
      ...baseConfig,
      delay: (context) => {
        let delay = 0
        if (context.type === 'data' && context.mode === 'default') {
          delay = context.dataIndex * props.staggerDelay
        }
        return delay
      },
      onProgress: (animation) => {
        // Use requestAnimationFrame for smooth animation
        if (animation.currentStep < animation.numSteps) {
          window.requestAnimationFrame(() => {
            if (chartInstance) {
              chartInstance.update('none')
            }
          })
        }
      }
    }
  }

  return baseConfig
}

const defaultOptions = {
  responsive: true,
  maintainAspectRatio: false,
  animation: false, // Will be set dynamically
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
          const name = context.label || ''
          const value = context.parsed?.y ?? context.parsed ?? context.raw
          if (value != null && !isNaN(Number(value))) {
            return `${name}: ${new Intl.NumberFormat('tr-TR').format(Number(value))}`
          }
          return name
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

  // Determine if animation should be enabled
  const shouldAnimate = props.animateOnView ? (isVisible.value && !hasAnimated.value) : true

  const mergedOptions = {
    ...defaultOptions,
    ...props.options,
    animation: shouldAnimate ? getAnimationConfig() : false,
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

  if (shouldAnimate) {
    hasAnimated.value = true
  }
}

// Setup Intersection Observer for viewport detection
const setupIntersectionObserver = () => {
  if (!props.animateOnView || !chartContainer.value) return

  const options = {
    root: null,
    rootMargin: '50px', // Trigger slightly before element is visible
    threshold: 0.1 // 10% of element must be visible
  }

  intersectionObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting && !hasAnimated.value) {
        isVisible.value = true
        // Reinitialize chart with animation
        if (chartInstance) {
          chartInstance.destroy()
        }
        initChart()
      }
    })
  }, options)

  intersectionObserver.observe(chartContainer.value)
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
  if (props.animateOnView) {
    setupIntersectionObserver()
    // Initialize chart without animation first if not visible
    if (!isVisible.value) {
      initChart()
    }
  } else {
    initChart()
  }
})

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy()
  }
  if (intersectionObserver) {
    intersectionObserver.disconnect()
  }
})
</script>

<style scoped>
.interactive-chart {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 200px;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}

.interactive-chart.chart-visible {
  opacity: 1;
  transform: translateY(0);
}

/* Respect prefers-reduced-motion */
@media (prefers-reduced-motion: reduce) {
  .interactive-chart {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
</style>
