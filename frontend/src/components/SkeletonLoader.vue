<template>
  <div 
    class="skeleton-loader" 
    :style="{ 
      width: width, 
      height: height, 
      borderRadius: borderRadius 
    }"
  >
    <div class="shimmer"></div>
  </div>
</template>

<script setup>
defineProps({
  width: {
    type: String,
    default: '100%'
  },
  height: {
    type: String,
    default: '20px'
  },
  borderRadius: {
    type: String,
    default: '8px'
  }
})
</script>

<style scoped>
.skeleton-loader {
  background-color: rgba(255, 255, 255, 0.05); /* Obsidian Black base */
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.shimmer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.05) 50%,
    transparent 100%
  );
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}
</style>
