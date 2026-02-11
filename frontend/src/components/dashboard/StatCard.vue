<template>
  <div 
    ref="cardRef"
    class="stat-card" 
    @click="handleClick"
    :class="{ clickable: clickable }"
  >
    <div class="stat-icon-wrapper" :style="{ background: gradient }">
      <component :is="icon" :size="24" :stroke-width="2" />
    </div>
    <div class="stat-content">
      <p class="stat-label">{{ label }}</p>
      <h3 ref="valueRef" class="stat-value">{{ formattedValue }}</h3>
      <div v-if="change" class="stat-change" :class="changeType">
        <component :is="changeType === 'positive' ? TrendingUp : TrendingDown" :size="16" />
        <span>{{ change }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { TrendingUp, TrendingDown } from 'lucide-vue-next'
import gsap from 'gsap'
import { useRipple } from '../../composables/useRipple'

const props = defineProps({
  icon: {
    type: Object,
    required: true
  },
  label: {
    type: String,
    required: true
  },
  value: {
    type: [Number, String],
    required: true
  },
  change: {
    type: String,
    default: null
  },
  changeType: {
    type: String,
    default: 'positive',
    validator: (value) => ['positive', 'negative', 'neutral'].includes(value)
  },
  gradient: {
    type: String,
    default: 'linear-gradient(135deg, #6366f1, #8b5cf6)'
  },
  clickable: {
    type: Boolean,
    default: true
  },
  animated: {
    type: Boolean,
    default: true
  },
  format: {
    type: String,
    default: 'number', // 'number', 'currency', 'percentage'
    validator: (value) => ['number', 'currency', 'percentage'].includes(value)
  }
})

const emit = defineEmits(['click'])

const displayValue = ref(0)
const cardRef = ref(null)
const valueRef = ref(null)
const previousValue = ref(0)
const valueColor = ref('#ffffff')

// Add ripple effect
useRipple(cardRef, {
  color: 'rgba(255, 255, 255, 0.25)',
  duration: 0.6
})

// Format value based on prop
const formattedValue = computed(() => {
  const val = displayValue.value
  
  if (typeof val !== 'number') {
    return val
  }
  
  switch (props.format) {
    case 'currency':
      return new Intl.NumberFormat('tr-TR', {
        style: 'currency',
        currency: 'TRY',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(val)
    case 'percentage':
      return `${val.toFixed(1)}%`
    default:
      return new Intl.NumberFormat('tr-TR').format(val)
  }
})

const handleClick = () => {
  if (props.clickable) {
    emit('click')
  }
}

// Animate value changes with color transitions
const animateValue = (from, to, options = {}) => {
  const {
    duration = 1.5,
    ease = 'power2.out',
    showParticles = false
  } = options

  // Calculate percentage change
  const percentChange = from > 0 ? ((to - from) / from) * 100 : 100
  const isSignificantChange = Math.abs(percentChange) > 10

  // Color transition based on change direction
  const targetColor = to > from ? '#10b981' : to < from ? '#ef4444' : '#ffffff'
  
  // Animate color
  gsap.to(valueRef.value, {
    color: targetColor,
    duration: 0.3,
    ease: 'power2.inOut',
    onComplete: () => {
      // Fade back to white
      gsap.to(valueRef.value, {
        color: '#ffffff',
        duration: 0.5,
        delay: 0.3
      })
    }
  })

  // Odometer-style animation with easing
  const tempValue = { value: from }
  gsap.to(tempValue, {
    value: to,
    duration,
    ease,
    onUpdate: () => {
      displayValue.value = tempValue.value
    },
    onComplete: () => {
      displayValue.value = to
    }
  })

  // Add particle effect for significant changes
  if (isSignificantChange && showParticles && valueRef.value) {
    createParticleEffect(valueRef.value, to > from)
  }

  // Slight bounce effect on the value
  if (valueRef.value) {
    gsap.fromTo(valueRef.value, 
      { scale: 1 },
      { 
        scale: 1.1, 
        duration: 0.2, 
        ease: 'power2.out',
        yoyo: true,
        repeat: 1
      }
    )
  }

  previousValue.value = to
}

// Create particle effect for significant changes
const createParticleEffect = (element, isPositive) => {
  const rect = element.getBoundingClientRect()
  const particleCount = 6
  
  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement('div')
    particle.className = 'stat-particle'
    particle.style.cssText = `
      position: fixed;
      left: ${rect.left + rect.width / 2}px;
      top: ${rect.top + rect.height / 2}px;
      width: 4px;
      height: 4px;
      border-radius: 50%;
      background: ${isPositive ? '#10b981' : '#ef4444'};
      pointer-events: none;
      z-index: 1000;
    `
    document.body.appendChild(particle)
    
    const angle = (Math.PI * 2 * i) / particleCount
    const distance = 30 + Math.random() * 20
    
    gsap.to(particle, {
      x: Math.cos(angle) * distance,
      y: Math.sin(angle) * distance - 20,
      opacity: 0,
      duration: 0.8,
      ease: 'power2.out',
      onComplete: () => {
        document.body.removeChild(particle)
      }
    })
  }
}

// Watch for value changes
watch(() => props.value, (newValue) => {
  if (props.animated && typeof newValue === 'number') {
    const from = displayValue.value
    animateValue(from, newValue, { showParticles: true })
  } else {
    displayValue.value = newValue
  }
})

onMounted(() => {
  if (props.animated && typeof props.value === 'number') {
    animateValue(0, props.value, { showParticles: false })
  } else {
    displayValue.value = props.value
  }
})
</script>

<style scoped>
.stat-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), transparent);
  opacity: 0;
  transition: opacity 0.3s;
}

.stat-card.clickable {
  cursor: pointer;
}

.stat-card.clickable:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.15);
}

.stat-card.clickable:hover::before {
  opacity: 1;
}

.stat-card.clickable:active {
  transform: translateY(-2px);
}

.stat-icon-wrapper {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.stat-content {
  flex: 1;
  min-width: 0;
}

.stat-label {
  font-size: 13px;
  font-weight: 500;
  color: #9ca3af;
  margin: 0 0 8px 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: white;
  margin: 0 0 8px 0;
  letter-spacing: -0.02em;
  transition: color 0.3s ease;
  will-change: transform, color;
}

.stat-change {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
}

.stat-change.positive {
  color: #10b981;
}

.stat-change.negative {
  color: #ef4444;
}

.stat-change.neutral {
  color: #9ca3af;
}

@media (max-width: 768px) {
  .stat-card {
    padding: 20px;
    gap: 16px;
  }

  .stat-icon-wrapper {
    width: 48px;
    height: 48px;
  }

  .stat-value {
    font-size: 24px;
  }
}
</style>
