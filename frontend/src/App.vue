<template>
  <PageLoadingBar />
  <router-view v-slot="{ Component, route }">
    <transition :name="getTransitionName(route)" mode="out-in">
      <component :is="Component" :key="route.path" />
    </transition>
  </router-view>
  <ToastNotification />
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import ToastNotification from './components/common/ToastNotification.vue'
import PageLoadingBar from './components/common/PageLoadingBar.vue'

const router = useRouter()

// Determine transition type based on route hierarchy and meta
const getTransitionName = (route) => {
  // Use custom transition from route meta if specified
  if (route.meta?.transition) {
    return route.meta.transition
  }

  // Determine direction based on route path depth
  const fromPath = router.currentRoute.value.path
  const toPath = route.path
  
  // No transition for same path (shouldn't happen but just in case)
  if (fromPath === toPath) {
    return 'fade'
  }

  // Admin routes use slide-up
  if (toPath.startsWith('/admin')) {
    return 'slide-up'
  }

  // Dashboard sector-to-sector transitions (nested: /dashboard/sectors/...)
  if (toPath.includes('/dashboard/sectors/') && fromPath.includes('/dashboard/sectors/')) {
    return 'fade'
  }

  // Default to fade-slide for most transitions
  const fromDepth = fromPath.split('/').length
  const toDepth = toPath.split('/').length
  
  if (toDepth > fromDepth) {
    return 'slide-left' // Going deeper
  } else if (toDepth < fromDepth) {
    return 'slide-right' // Going back
  }
  
  return 'fade'
}
</script>

<style>
/* Global Resets if needed, though clean-css handles most */
html, body, #app {
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
  background: var(--bg-main);
}

body {
  overflow-y: auto; /* Allow vertical scroll for landing/login pages */
}

#app {
  overflow: visible; /* Let child components manage their own overflow */
}

/* Page Transition Animations */
/* Fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Slide Left (going deeper) */
.slide-left-enter-active,
.slide-left-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-left-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.slide-left-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* Slide Right (going back) */
.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-right-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.slide-right-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

/* Slide Up (for modals, admin panels) */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}

/* Respect prefers-reduced-motion */
@media (prefers-reduced-motion: reduce) {
  .fade-enter-active,
  .fade-leave-active,
  .slide-left-enter-active,
  .slide-left-leave-active,
  .slide-right-enter-active,
  .slide-right-leave-active,
  .slide-up-enter-active,
  .slide-up-leave-active {
    transition: none;
  }

  .fade-enter-from,
  .fade-leave-to,
  .slide-left-enter-from,
  .slide-left-leave-to,
  .slide-right-enter-from,
  .slide-right-leave-to,
  .slide-up-enter-from,
  .slide-up-leave-to {
    opacity: 1;
    transform: none;
  }
}
</style>
