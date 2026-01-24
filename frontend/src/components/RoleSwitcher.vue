<template>
  <div class="role-switcher">
    <span :class="['role-label', { active: currentRole === 'secretary' }]">
      Secretary
    </span>
    <button 
      class="toggle-switch"
      @click="$emit('toggle')"
      :aria-label="`Switch to ${currentRole === 'admin' ? 'secretary' : 'admin'} mode`"
    >
      <div class="toggle-track">
        <div 
          class="toggle-thumb"
          :class="{ 'admin-mode': currentRole === 'admin' }"
        >
          <component 
            :is="currentRole === 'admin' ? ShieldCheck : UserCircle" 
            :size="14" 
            :stroke-width="2.5"
          />
        </div>
      </div>
    </button>
    <span :class="['role-label', { active: currentRole === 'admin' }]">
      Admin
    </span>
  </div>
</template>

<script setup>
import { ShieldCheck, UserCircle } from 'lucide-vue-next'

defineProps({
  currentRole: {
    type: String,
    required: true,
    validator: (value) => ['admin', 'secretary'].includes(value)
  }
})

defineEmits(['toggle'])
</script>

<style scoped>
.role-switcher {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 12px;
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
}

.role-label {
  font-size: 13px;
  font-weight: 500;
  letter-spacing: var(--letter-spacing-normal);
  color: var(--text-muted);
  transition: color var(--transition-fast);
  user-select: none;
}

.role-label.active {
  color: var(--text-primary);
  font-weight: 600;
}

.toggle-switch {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
}

.toggle-track {
  width: 52px;
  height: 28px;
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: 14px;
  position: relative;
  transition: all var(--transition-base);
}

.toggle-switch:hover .toggle-track {
  border-color: var(--border-hover);
  box-shadow: 0 0 16px var(--indigo-glow);
}

.toggle-thumb {
  position: absolute;
  left: 2px;
  top: 2px;
  width: 22px;
  height: 22px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  transition: all var(--transition-base);
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.4),
              0 0 16px var(--indigo-glow);
}

.toggle-thumb.admin-mode {
  transform: translateX(24px);
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.6),
              0 0 20px var(--indigo-glow-strong);
}

.toggle-switch:active .toggle-thumb {
  transform: scale(0.95);
}

.toggle-switch:active .toggle-thumb.admin-mode {
  transform: translateX(24px) scale(0.95);
}
</style>
