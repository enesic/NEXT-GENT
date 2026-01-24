<template>
  <div class="card" :style="{ animationDelay: `${index * 50}ms` }">
    <div class="card-header">
      <div class="card-icon">
        <component :is="icon" :size="24" :stroke-width="2" />
      </div>
    </div>
    <h3 class="card-title">{{ title }}</h3>
    <p class="card-description">{{ description }}</p>
    <div class="card-footer">
      <span class="card-stat">
        Durum: <span class="card-stat-value">{{ status }}</span>
      </span>
      <span class="card-stat">
        <span class="card-stat-value">{{ progress }}%</span>
      </span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  icon: {
    type: Object,
    required: true
  },
  status: {
    type: String,
    default: 'Aktif'
  },
  progress: {
    type: Number,
    default: 0
  },
  index: {
    type: Number,
    default: 0
  }
})
</script>

<style scoped>
.card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 24px;
  transition: all var(--transition-base);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  animation: fadeIn var(--transition-slow) ease-out backwards;
}

.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent, 
    var(--indigo-primary), 
    transparent);
  opacity: 0;
  transition: opacity var(--transition-base);
}

.card:hover {
  background: var(--surface-hover);
  border-color: var(--border-hover);
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4),
              0 0 0 1px var(--border-hover),
              0 0 48px var(--indigo-glow);
}

.card:hover::before {
  opacity: 1;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.card-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, var(--indigo-primary), #8b5cf6);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 24px var(--indigo-glow);
  color: white;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  letter-spacing: var(--letter-spacing-tight);
  margin-bottom: 8px;
  line-height: var(--line-height-tight);
}

.card-description {
  font-size: 14px;
  color: var(--text-secondary);
  letter-spacing: var(--letter-spacing-normal);
  line-height: var(--line-height-relaxed);
}

.card-footer {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-stat {
  font-size: 12px;
  color: var(--text-muted);
  letter-spacing: var(--letter-spacing-normal);
}

.card-stat-value {
  color: var(--text-primary);
  font-weight: 600;
  margin-left: 4px;
}
</style>
