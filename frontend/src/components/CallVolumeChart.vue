<template>
  <div class="chart-container">
    <div class="chart-header">
      <h3 class="chart-title">
        <Phone :size="18" :stroke-width="2" class="title-icon" />
        Çağrı Yoğunluğu
      </h3>
    </div>
    
    <div class="chart-wrapper">
      <apexchart
        type="area"
        height="280"
        :options="chartOptions"
        :series="series"
      />
    </div>

    <div class="ai-insight">
      <Sparkles :size="14" :stroke-width="2" class="insight-icon" />
      <p class="insight-text">{{ aiInsight }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Phone, Sparkles } from 'lucide-vue-next'

const aiInsight = ref('Öğleden sonra çağrı yoğunluğu zirve yaptı, verimlilik %20 arttı')

const series = ref([{
  name: 'Çağrı Sayısı',
  data: [12, 18, 25, 32, 28, 45, 52, 48, 38, 42, 35, 28]
}])

const chartOptions = ref({
  chart: {
    type: 'area',
    height: 280,
    toolbar: {
      show: false
    },
    background: 'transparent',
    animations: {
      enabled: true,
      easing: 'easeinout',
      speed: 800,
      animateGradually: {
        enabled: true,
        delay: 150
      }
    },
    sparkline: {
      enabled: false
    }
  },
  colors: ['#6366f1'],
  stroke: {
    curve: 'smooth',
    width: 3,
    colors: ['#6366f1']
  },
  fill: {
    type: 'gradient',
    gradient: {
      shade: 'dark',
      type: 'vertical',
      shadeIntensity: 0.5,
      gradientToColors: ['#8b5cf6'],
      inverseColors: false,
      opacityFrom: 0.8,
      opacityTo: 0.1,
      stops: [0, 100]
    }
  },
  dataLabels: {
    enabled: false
  },
  grid: {
    show: false, // Grid kaldırıldı
    padding: {
      left: 0,
      right: 0,
      top: 0,
      bottom: 0
    }
  },
  xaxis: {
    categories: ['00:00', '02:00', '04:00', '06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00'],
    labels: {
      style: {
        colors: '#52525b',
        fontSize: '11px',
        fontFamily: 'Inter, sans-serif',
        fontWeight: 500
      }
    },
    axisBorder: {
      show: false
    },
    axisTicks: {
      show: false
    },
    crosshairs: {
      show: false
    }
  },
  yaxis: {
    labels: {
      style: {
        colors: '#52525b',
        fontSize: '11px',
        fontFamily: 'Inter, sans-serif',
        fontWeight: 500
      },
      formatter: (value) => Math.round(value)
    },
    axisBorder: {
      show: false
    },
    axisTicks: {
      show: false
    }
  },
  tooltip: {
    theme: 'dark',
    style: {
      fontSize: '12px',
      fontFamily: 'Inter, sans-serif'
    },
    x: {
      show: true
    },
    y: {
      formatter: (value) => `${value} çağrı`,
      title: {
        formatter: () => ''
      }
    },
    marker: {
      show: true
    }
  },
  legend: {
    show: false
  }
})
</script>

<style scoped>
.chart-container {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 24px;
  transition: all var(--transition-base);
}

.chart-container:hover {
  border-color: var(--border-hover);
  box-shadow: 0 0 32px var(--indigo-glow);
}

.chart-header {
  margin-bottom: 16px;
}

.chart-title {
  font-size: 18px;
  font-weight: 600;
  letter-spacing: var(--letter-spacing-tight);
  display: flex;
  align-items: center;
  gap: 8px;
}

.title-icon {
  color: var(--indigo-primary);
}

.chart-wrapper {
  margin: 0 -12px;
}

.ai-insight {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
  padding: 12px 16px;
  background: rgba(99, 102, 241, 0.08);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: var(--radius-md);
}

.insight-icon {
  color: var(--indigo-primary);
  flex-shrink: 0;
}

.insight-text {
  font-size: 13px;
  font-style: italic;
  letter-spacing: var(--letter-spacing-normal);
  line-height: var(--line-height-relaxed);
  color: var(--text-secondary);
  font-weight: 500;
}
</style>
