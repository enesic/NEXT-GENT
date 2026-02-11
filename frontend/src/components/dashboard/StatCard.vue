<template>
  <div 
    class="stat-card" 
    @click="handleClick"
    :class="{ clickable: clickable }"
  >
    <div class="stat-icon-wrapper" :style="{ background: gradient }">
      <component :is="icon" :size="24" :stroke-width="2" />
    </div>
    <div class="stat-content">
      <p class="stat-label">{{ label }}</p>
      <h3 class="stat-value">{{ displayValue }}</h3>
      <div v-if="change" class="stat-change" :class="changeType">
        <component :is="changeType === 'positive' ? TrendingUp : TrendingDown" :size="16" />
        <span>{{ change }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { TrendingUp, TrendingDown } from 'lucide-vue-next'
import gsap from 'gsap'

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
  }
})

const emit = defineEmits(['click'])

const displayValue = ref(0)

const handleClick = () => {
  if (props.clickable) {
    emit('click')
  }
}

onMounted(() => {
  if (props.animated && typeof props.value === 'number') {
    gsap.to(displayValue, {
      value: props.value,
      duration: 1.5,
      ease: 'power2.out',
      onUpdate: () => {
        displayValue.value = Math.round(displayValue.value)
      }
    })
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
