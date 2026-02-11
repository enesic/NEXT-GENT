<template>
  <div class="activity-feed">
    <div class="feed-header">
      <h3 class="feed-title">{{ title }}</h3>
      <button v-if="showViewAll" class="btn-link" @click="$emit('view-all')">
        Tümünü Gör
      </button>
    </div>
    <div class="feed-list">
      <TransitionGroup name="list">
        <div 
          v-for="item in items" 
          :key="item.id"
          class="feed-item"
          @click="handleItemClick(item)"
        >
          <div class="item-icon" :style="{ background: item.iconGradient || defaultGradient }">
            <component :is="item.icon" :size="16" :stroke-width="2" />
          </div>
          <div class="item-content">
            <p class="item-title">{{ item.title }}</p>
            <p class="item-subtitle">{{ item.subtitle }}</p>
          </div>
          <div v-if="item.badge" class="item-badge" :class="item.badgeType">
            {{ item.badge }}
          </div>
          <div class="item-time">
            <Clock :size="14" />
            <span>{{ item.time }}</span>
          </div>
        </div>
      </TransitionGroup>
      <div v-if="items.length === 0" class="empty-state">
        <component :is="emptyIcon" :size="48" :stroke-width="1.5" />
        <p>{{ emptyMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Clock, Inbox } from 'lucide-vue-next'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  items: {
    type: Array,
    default: () => []
  },
  showViewAll: {
    type: Boolean,
    default: true
  },
  emptyMessage: {
    type: String,
    default: 'Henüz aktivite bulunmuyor'
  },
  emptyIcon: {
    type: Object,
    default: () => Inbox
  },
  defaultGradient: {
    type: String,
    default: 'linear-gradient(135deg, #6366f1, #8b5cf6)'
  }
})

const emit = defineEmits(['view-all', 'item-click'])

const handleItemClick = (item) => {
  emit('item-click', item)
}
</script>

<style scoped>
.activity-feed {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 24px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.feed-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.feed-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: white;
}

.btn-link {
  background: none;
  border: none;
  color: var(--sector-accent, #818cf8);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  padding: 6px 12px;
  border-radius: 8px;
}

.btn-link:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--sector-icon, #6366f1);
}

.feed-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.feed-item {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.feed-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  transform: translateX(4px);
}

.item-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.item-content {
  flex: 1;
  min-width: 0;
}

.item-title {
  font-size: 14px;
  font-weight: 600;
  color: white;
  margin: 0 0 4px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-subtitle {
  font-size: 12px;
  color: #9ca3af;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-badge {
  padding: 4px 10px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 600;
  flex-shrink: 0;
}

.item-badge.success {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.item-badge.warning {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.item-badge.error {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.item-badge.info {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.item-time {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: #6b7280;
  flex-shrink: 0;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
  color: #6b7280;
  text-align: center;
}

.empty-state p {
  margin-top: 12px;
  font-size: 13px;
}

/* List Transition */
.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease;
}

.list-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}

.list-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

/* Scrollbar */
.feed-list::-webkit-scrollbar {
  width: 6px;
}

.feed-list::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.02);
  border-radius: 3px;
}

.feed-list::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.feed-list::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.15);
}

@media (max-width: 768px) {
  .activity-feed {
    padding: 20px;
  }

  .feed-item {
    padding: 14px;
  }

  .item-icon {
    width: 32px;
    height: 32px;
  }
}
</style>
