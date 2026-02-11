<template>
  <div
    class="skeleton"
    :class="[
      `skeleton-${shape}`,
      { 'skeleton-wave': wave }
    ]"
    :style="skeletonStyle"
    :aria-busy="true"
    :aria-label="ariaLabel || 'Loading content'"
  ></div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  shape: {
    type: String,
    default: 'rectangle',
    validator: (value) => ['rectangle', 'circle', 'text'].includes(value)
  },
  width: {
    type: [String, Number],
    default: '100%'
  },
  height: {
    type: [String, Number],
    default: '20px'
  },
  wave: {
    type: Boolean,
    default: true
  },
  ariaLabel: {
    type: String,
    default: ''
  }
})

const skeletonStyle = computed(() => {
  const style = {}
  
  if (props.width) {
    style.width = typeof props.width === 'number' ? `${props.width}px` : props.width
  }
  
  if (props.height) {
    style.height = typeof props.height === 'number' ? `${props.height}px` : props.height
  }
  
  return style
})
</script>

<style scoped>
.skeleton {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  position: relative;
  overflow: hidden;
  display: inline-block;
}

.skeleton-rectangle {
  border-radius: 8px;
}

.skeleton-circle {
  border-radius: 50%;
}

.skeleton-text {
  border-radius: 4px;
  height: 1em;
  transform: scale(1, 0.8);
}

.skeleton-wave::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.08),
    transparent
  );
  animation: wave 1.5s ease-in-out infinite;
}

@keyframes wave {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

/* Alternative pulse animation if wave is disabled */
.skeleton:not(.skeleton-wave) {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Reduce motion for accessibility */
@media (prefers-reduced-motion: reduce) {
  .skeleton-wave::before {
    animation: none;
  }
  
  .skeleton {
    animation: none;
  }
}
</style>
