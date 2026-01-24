<template>
  <div class="chart-container">
    <div class="chart-header">
      <h3 class="chart-title">
        <TrendingUp :size="18" :stroke-width="2" class="title-icon" />
        Randevu Dönüşüm Oranı
      </h3>
    </div>
    
    <div class="chart-wrapper">
      <apexchart
        type="line"
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
import { TrendingUp, Sparkles } from 'lucide-vue-next'

const aiInsight = ref('Dönüşüm oranı hedefin %15 üzerinde, bugün verimlilik zirve yaptı')

const series = ref([{
  name: 'Dönüşüm %',
  data: [65, 68, 72, 70, 75, 78, 82, 85, 88, 90, 92, 95]
}])

const chartOptions = ref({
  chart: {
    type: 'line',
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
    dropShadow: {
      enabled: true,
      color: '#6366f1',
      top: 0,
      left: 0,
      blur: 12,
      opacity: 0.5
    }
  },
  colors: ['#6366f1'],
  stroke: {
    curve: 'smooth',
    width: 4,
    colors: ['#6366f1'],
    lineCap: 'round'
  },
  markers: {
    size: 6,
    colors: ['#6366f1'],
    strokeColors: '#030303',
    strokeWidth: 2,
    hover: {
      size: 8,
      sizeOffset: 2
    },
    discrete: []
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
    categories: ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz', 'Tem', 'Ağu', 'Eyl', 'Eki', 'Kas', 'Ara'],
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
    min: 60,
    max: 100,
    labels: {
      style: {
        colors: '#52525b',
        fontSize: '11px',
        fontFamily: 'Inter, sans-serif',
        fontWeight: 500
      },
      formatter: (value) => `${Math.round(value)}%`
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
      formatter: (value) => `${value}%`,
      title: {
        formatter: () => 'Dönüşüm: '
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
