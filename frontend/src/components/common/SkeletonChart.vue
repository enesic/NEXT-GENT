<template>
  <div class="skeleton-chart" :class="`skeleton-chart-${type}`" aria-busy="true" aria-label="Loading chart">
    <!-- Line/Bar Chart -->
    <template v-if="type === 'line' || type === 'bar'">
      <div class="chart-bars">
        <div
          v-for="i in barCount"
          :key="i"
          class="chart-bar"
          :style="{ height: `${getRandomHeight()}%` }"
        >
          <SkeletonLoader shape="rectangle" width="100%" height="100%" />
        </div>
      </div>
      <div class="chart-axis">
        <SkeletonLoader
          v-for="i in barCount"
          :key="i"
          shape="text"
          width="40px"
          height="10px"
        />
      </div>
    </template>

    <!-- Doughnut/Pie Chart -->
    <template v-else-if="type === 'doughnut' || type === 'pie'">
      <div class="chart-doughnut">
        <SkeletonLoader shape="circle" :width="200" :height="200" />
      </div>
      <div class="chart-legend">
        <div v-for="i in 4" :key="i" class="legend-item">
          <SkeletonLoader shape="circle" :width="12" :height="12" />
          <SkeletonLoader shape="text" width="80px" height="12px" />
          <SkeletonLoader shape="text" width="40px" height="12px" />
        </div>
      </div>
    </template>

    <!-- Default/Generic -->
    <template v-else>
      <SkeletonLoader shape="rectangle" width="100%" height="100%" />
    </template>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import SkeletonLoader from './SkeletonLoader.vue'

const props = defineProps({
  type: {
    type: String,
    default: 'line',
    validator: (value) => ['line', 'bar', 'doughnut', 'pie', 'generic'].includes(value)
  },
  barCount: {
    type: Number,
    default: 7
  }
})

// Generate random heights for bars to look more realistic
const heights = ref([])
const getRandomHeight = () => {
  if (heights.value.length < props.barCount) {
    heights.value.push(Math.floor(Math.random() * 60) + 40)
  }
  return heights.value[heights.value.length - 1]
}
</script>

<style scoped>
.skeleton-chart {
  width: 100%;
  height: 100%;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  gap: 12px;
}

/* Line/Bar Chart Skeleton */
.skeleton-chart-line,
.skeleton-chart-bar {
  padding: 20px;
}

.chart-bars {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 8px;
  height: 100%;
  min-height: 200px;
}

.chart-bar {
  flex: 1;
  min-width: 20px;
  max-width: 80px;
  position: relative;
  transition: height 0.3s ease;
}

.chart-axis {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  padding-top: 8px;
}

/* Doughnut/Pie Chart Skeleton */
.skeleton-chart-doughnut,
.skeleton-chart-pie {
  align-items: center;
  justify-content: center;
}

.chart-doughnut {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 20px 0;
}

.chart-legend {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 0 20px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* Generic Chart Skeleton */
.skeleton-chart-generic {
  padding: 20px;
}

@media (max-width: 768px) {
  .skeleton-chart {
    min-height: 180px;
  }

  .chart-bars {
    min-height: 180px;
  }

  .chart-doughnut {
    margin: 10px 0;
  }

  .chart-legend {
    padding: 0 10px;
  }
}
</style>
