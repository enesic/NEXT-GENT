<template>
  <Teleport to="body">
    <div v-if="isLoading" class="page-loading-bar" :style="{ width: `${progress}%` }">
      <div class="loading-bar-glow"></div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const isLoading = ref(false)
const progress = ref(0)
let progressInterval = null

const router = useRouter()

/**
 * Start the loading progress
 */
const start = () => {
  isLoading.value = true
  progress.value = 0
  
  // Clear any existing interval
  if (progressInterval) {
    clearInterval(progressInterval)
  }

  // Simulate progress with decreasing increment rate
  progressInterval = setInterval(() => {
    if (progress.value < 90) {
      // Progress faster at the beginning, slower as it approaches 90%
      const increment = (90 - progress.value) * 0.1
      progress.value = Math.min(progress.value + increment, 90)
    }
  }, 100)
}

/**
 * Complete the loading progress
 */
const finish = () => {
  // Quickly move to 100%
  progress.value = 100

  // Clear interval
  if (progressInterval) {
    clearInterval(progressInterval)
    progressInterval = null
  }

  // Hide the bar after animation completes
  setTimeout(() => {
    isLoading.value = false
    progress.value = 0
  }, 400)
}

/**
 * Fail the loading progress (show red briefly, then hide)
 */
const fail = () => {
  // Clear interval
  if (progressInterval) {
    clearInterval(progressInterval)
    progressInterval = null
  }

  // Keep current progress, just hide after a moment
  setTimeout(() => {
    isLoading.value = false
    progress.value = 0
  }, 500)
}

// Setup router hooks
onMounted(() => {
  // Start loading before each route change
  router.beforeEach((to, from, next) => {
    start()
    next()
  })

  // Finish loading after route change completes
  router.afterEach(() => {
    finish()
  })

  // Handle navigation errors
  router.onError(() => {
    fail()
  })
})
</script>

<style scoped>
.page-loading-bar {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  background: linear-gradient(90deg, #6366f1, #8b5cf6, #a855f7);
  z-index: 10000;
  transition: width 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  will-change: width;
}

.loading-bar-glow {
  position: absolute;
  top: 0;
  right: 0;
  width: 100px;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4));
  animation: glow 1.5s ease-in-out infinite;
}

@keyframes glow {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

/* Respect prefers-reduced-motion */
@media (prefers-reduced-motion: reduce) {
  .page-loading-bar {
    transition: none;
  }

  .loading-bar-glow {
    animation: none;
    display: none;
  }
}
</style>
