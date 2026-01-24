<template>
  <Transition name="loading-bar">
    <div v-if="loadingStore.isLoading" class="loading-bar-container">
      <div class="loading-bar">
        <div class="loading-bar-progress"></div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { useLoadingStore } from '../stores/loading'

const loadingStore = useLoadingStore()
</script>

<style scoped>
.loading-bar-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 9999;
  height: 3px;
  background: transparent;
}

.loading-bar {
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: linear-gradient(
    90deg,
    rgba(99, 102, 241, 0.1) 0%,
    rgba(139, 92, 246, 0.1) 100%
  );
}

.loading-bar-progress {
  height: 100%;
  background: linear-gradient(
    90deg,
    #6366f1 0%,
    #8b5cf6 50%,
    #ec4899 100%
  );
  background-size: 200% 100%;
  animation: loading-slide 1.5s cubic-bezier(0.4, 0, 0.2, 1) infinite,
             loading-glow 2s ease-in-out infinite;
  box-shadow: 0 0 10px rgba(99, 102, 241, 0.5),
              0 0 20px rgba(139, 92, 246, 0.3);
  transform-origin: left;
}

@keyframes loading-slide {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

@keyframes loading-glow {
  0%, 100% {
    opacity: 0.8;
    box-shadow: 0 0 10px rgba(99, 102, 241, 0.5),
                0 0 20px rgba(139, 92, 246, 0.3);
  }
  50% {
    opacity: 1;
    box-shadow: 0 0 15px rgba(99, 102, 241, 0.8),
                0 0 30px rgba(139, 92, 246, 0.5),
                0 0 40px rgba(236, 72, 153, 0.3);
  }
}

/* Transition animations */
.loading-bar-enter-active,
.loading-bar-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.loading-bar-enter-from {
  opacity: 0;
  transform: translateY(-100%);
}

.loading-bar-leave-to {
  opacity: 0;
}
</style>
