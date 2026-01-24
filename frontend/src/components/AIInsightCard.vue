<template>
  <div class="ai-insight-card glass-panel" :class="type">
    <div class="insight-icon-wrapper">
      <div class="insight-icon">
        <Sparkles v-if="type === 'opportunity'" :size="20" />
        <AlertTriangle v-else-if="type === 'warning'" :size="20" />
        <TrendingUp v-else :size="20" />
      </div>
      <div class="pulse-ring"></div>
    </div>
    
    <div class="insight-content">
      <h4 class="insight-title">{{ title }}</h4>
      <p class="insight-message">{{ message }}</p>
      
      <button v-if="action" class="insight-action-btn">
        {{ action }}
        <ArrowRight :size="14" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { Sparkles, AlertTriangle, TrendingUp, ArrowRight } from 'lucide-vue-next'

defineProps({
  type: {
    type: String,
    required: true, 
    validator: (val) => ['opportunity', 'warning', 'success'].includes(val)
  },
  title: {
    type: String,
    required: true
  },
  message: {
    type: String,
    required: true
  },
  action: {
    type: String,
    default: null
  }
})
</script>

<style scoped>
.ai-insight-card {
  display: flex;
  gap: 16px;
  padding: 20px;
  border-radius: var(--radius-lg);
  border-left: 3px solid transparent; /* Colored border on left */
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.ai-insight-card:hover {
  transform: translateY(-2px);
}

/* Types */
.ai-insight-card.opportunity {
  border-left-color: #8b5cf6; /* Violet */
  background: linear-gradient(to right, rgba(139, 92, 246, 0.05), rgba(255, 255, 255, 0.02));
}

.ai-insight-card.warning {
  border-left-color: #f59e0b; /* Amber */
  background: linear-gradient(to right, rgba(245, 158, 11, 0.05), rgba(255, 255, 255, 0.02));
}

.ai-insight-card.success {
  border-left-color: #10b981; /* Emerald */
  background: linear-gradient(to right, rgba(16, 185, 129, 0.05), rgba(255, 255, 255, 0.02));
}

/* Icon */
.insight-icon-wrapper {
  position: relative;
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.insight-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
  color: white;
}

.opportunity .insight-icon { background: linear-gradient(135deg, #8b5cf6, #6366f1); box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3); }
.warning .insight-icon { background: linear-gradient(135deg, #f59e0b, #d97706); box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3); }
.success .insight-icon { background: linear-gradient(135deg, #10b981, #059669); box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); }

/* Pulse Animation */
.pulse-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  border-radius: 12px;
  border: 1px solid currentColor;
  opacity: 0;
  z-index: 1;
}

.opportunity .pulse-ring { border-color: #8b5cf6; animation: pulse 2s infinite; }
.warning .pulse-ring { border-color: #f59e0b; animation: pulse 2s infinite; }
.success .pulse-ring { border-color: #10b981; animation: pulse 2s infinite; }

@keyframes pulse {
  0% { transform: translate(-50%, -50%) scale(0.8); opacity: 0.5; }
  100% { transform: translate(-50%, -50%) scale(1.5); opacity: 0; }
}

/* Content */
.insight-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.insight-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.insight-message {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
}

/* Action Button */
.insight-action-btn {
  margin-top: 8px;
  width: fit-content;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  background: none;
  border: none;
  padding: 0;
  transition: gap 0.2s ease;
}

.opportunity .insight-action-btn { color: #8b5cf6; }
.warning .insight-action-btn { color: #f59e0b; }
.success .insight-action-btn { color: #10b981; }

.insight-action-btn:hover {
  gap: 10px;
  text-decoration: underline;
}
</style>
