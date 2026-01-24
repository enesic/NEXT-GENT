<template>
  <header class="topbar">
    <div class="topbar-left">
      <h1 class="page-title">{{ pageTitle }}</h1>
      <div class="search-bar">
        <Search :size="18" :stroke-width="2" class="search-icon" />
        <input 
          type="text" 
          class="search-input" 
          placeholder="Ara... (⌘K)"
          :value="searchQuery"
          @input="$emit('update:searchQuery', $event.target.value)"
        />
      </div>
    </div>

    <div class="topbar-center">
      <RoleSwitcher 
        :currentRole="currentRole"
        @toggle="$emit('toggleRole')"
      />
    </div>

    <div class="topbar-right">
      <button class="icon-button">
        <Bell :size="20" :stroke-width="2" />
        <span class="notification-badge"></span>
      </button>
      <button class="icon-button">
        <Settings :size="20" :stroke-width="2" />
      </button>
    </div>
  </header>
</template>

<script setup>
import { Search, Bell, Settings } from 'lucide-vue-next'
import RoleSwitcher from './RoleSwitcher.vue'

defineProps({
  pageTitle: {
    type: String,
    default: 'Dashboard'
  },
  searchQuery: {
    type: String,
    default: ''
  },
  currentRole: {
    type: String,
    required: true
  }
})

defineEmits(['update:searchQuery', 'toggleRole'])
</script>

<style scoped>
.topbar {
  height: 72px;
  background: var(--obsidian-black);
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  position: relative;
  z-index: 5;
  animation: slideInDown var(--transition-slow) ease-out;
}

.topbar::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    var(--indigo-glow) 50%, 
    transparent 100%);
  pointer-events: none;
}

.topbar-left {
  display: flex;
  align-items: center;
  gap: 24px;
}

.topbar-center {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  letter-spacing: var(--letter-spacing-tight);
  line-height: var(--line-height-tight);
}

.search-bar {
  position: relative;
  width: 320px;
}

.search-input {
  width: 100%;
  height: 40px;
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 0 16px 0 44px;
  color: var(--text-primary);
  font-size: 14px;
  font-family: var(--font-family);
  letter-spacing: var(--letter-spacing-normal);
  transition: all var(--transition-fast);
}

.search-input:focus {
  outline: none;
  border-color: var(--indigo-primary);
  box-shadow: 0 0 0 3px var(--indigo-glow),
              0 0 24px var(--indigo-glow-strong);
}

.search-input::placeholder {
  color: var(--text-muted);
}

.search-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  pointer-events: none;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.icon-button {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  cursor: pointer;
  transition: all var(--transition-fast);
  position: relative;
  color: var(--text-secondary);
}

.icon-button:hover {
  background: var(--surface-hover);
  border-color: var(--border-hover);
  transform: translateY(-1px);
  color: var(--text-primary);
}

.notification-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 8px;
  height: 8px;
  background: #ef4444;
  border-radius: 50%;
  border: 2px solid var(--obsidian-black);
  box-shadow: 0 0 12px #ef4444;
}
</style>
