<template>
  <div class="skeleton-table" aria-busy="true" aria-label="Loading list">
    <div
      v-for="i in rows"
      :key="i"
      class="skeleton-row"
    >
      <SkeletonLoader v-if="showAvatar" shape="circle" :width="40" :height="40" />
      <div class="skeleton-row-content">
        <SkeletonLoader shape="text" :width="`${getRandomWidth(60, 80)}%`" height="14px" />
        <SkeletonLoader shape="text" :width="`${getRandomWidth(40, 60)}%`" height="12px" class="skeleton-subtitle" />
      </div>
      <SkeletonLoader v-if="showAction" shape="rectangle" width="80px" height="32px" />
    </div>
  </div>
</template>

<script setup>
import SkeletonLoader from './SkeletonLoader.vue'

const props = defineProps({
  rows: {
    type: Number,
    default: 3
  },
  showAvatar: {
    type: Boolean,
    default: true
  },
  showAction: {
    type: Boolean,
    default: false
  }
})

const getRandomWidth = (min, max) => {
  return Math.floor(Math.random() * (max - min + 1)) + min
}
</script>

<style scoped>
.skeleton-table {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.skeleton-row {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.skeleton-row-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.skeleton-subtitle {
  margin-top: 4px;
}

@media (max-width: 768px) {
  .skeleton-row {
    padding: 14px;
  }
}
</style>
