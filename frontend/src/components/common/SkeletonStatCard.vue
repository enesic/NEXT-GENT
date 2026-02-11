<template>
  <div class="stat-card-skeleton" aria-busy="true" aria-label="Loading statistics">
    <SkeletonLoader shape="circle" :width="56" :height="56" />
    <div class="skeleton-content">
      <SkeletonLoader shape="text" width="60%" height="13px" />
      <SkeletonLoader shape="text" width="80%" height="28px" class="skeleton-value" />
      <SkeletonLoader shape="text" width="40%" height="13px" />
    </div>
  </div>
</template>

<script setup>
import SkeletonLoader from './SkeletonLoader.vue'
</script>

<style scoped>
.stat-card-skeleton {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  min-height: 120px;
}

.skeleton-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.skeleton-value {
  margin: 4px 0;
}

@media (max-width: 768px) {
  .stat-card-skeleton {
    padding: 20px;
    gap: 16px;
  }
}
</style>
