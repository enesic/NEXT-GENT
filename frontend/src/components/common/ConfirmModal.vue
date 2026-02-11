<template>
  <BaseModal
    v-model="isOpen"
    :title="title"
    size="small"
    :close-on-overlay="closeOnOverlay"
    :close-on-esc="closeOnEsc"
    @close="handleCancel"
  >
    <div class="confirm-modal-content">
      <div class="confirm-icon" :class="`confirm-icon-${variant}`">
        <component :is="getIcon()" :size="32" :stroke-width="2" />
      </div>
      <p class="confirm-message">{{ message }}</p>
    </div>

    <template #footer>
      <button
        class="btn btn-secondary"
        @click="handleCancel"
        type="button"
        ref="cancelButtonRef"
      >
        {{ cancelText }}
      </button>
      <button
        class="btn btn-primary"
        :class="`btn-${variant}`"
        @click="handleConfirm"
        type="button"
        :disabled="loading"
      >
        <span v-if="loading" class="btn-spinner"></span>
        <span>{{ confirmText }}</span>
      </button>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, computed } from 'vue'
import { AlertTriangle, Info, AlertCircle, CheckCircle } from 'lucide-vue-next'
import BaseModal from './BaseModal.vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: 'Confirm Action'
  },
  message: {
    type: String,
    required: true
  },
  confirmText: {
    type: String,
    default: 'Confirm'
  },
  cancelText: {
    type: String,
    default: 'Cancel'
  },
  variant: {
    type: String,
    default: 'info',
    validator: (value) => ['info', 'warning', 'danger', 'success'].includes(value)
  },
  closeOnOverlay: {
    type: Boolean,
    default: true
  },
  closeOnEsc: {
    type: Boolean,
    default: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'confirm', 'cancel'])

const cancelButtonRef = ref(null)

const isOpen = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const getIcon = () => {
  const icons = {
    info: Info,
    warning: AlertTriangle,
    danger: AlertCircle,
    success: CheckCircle
  }
  return icons[props.variant] || Info
}

const handleConfirm = () => {
  emit('confirm')
  if (!props.loading) {
    isOpen.value = false
  }
}

const handleCancel = () => {
  emit('cancel')
  isOpen.value = false
}
</script>

<style scoped>
.confirm-modal-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 20px 0;
}

.confirm-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
  position: relative;
}

.confirm-icon::before {
  content: '';
  position: absolute;
  inset: -8px;
  border-radius: 50%;
  opacity: 0.3;
  animation: pulse 2s ease-in-out infinite;
}

.confirm-icon-info {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.confirm-icon-info::before {
  background: rgba(59, 130, 246, 0.2);
}

.confirm-icon-warning {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.confirm-icon-warning::before {
  background: rgba(245, 158, 11, 0.2);
}

.confirm-icon-danger {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.confirm-icon-danger::before {
  background: rgba(239, 68, 68, 0.2);
}

.confirm-icon-success {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.confirm-icon-success::before {
  background: rgba(16, 185, 129, 0.2);
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.3;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.1;
  }
}

.confirm-message {
  font-size: 15px;
  color: #d1d5db;
  line-height: 1.6;
  margin: 0;
  max-width: 320px;
}

/* Buttons */
.btn {
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-width: 100px;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn:focus {
  outline: 2px solid rgba(99, 102, 241, 0.5);
  outline-offset: 2px;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #d1d5db;
}

.btn-secondary:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.08);
  color: white;
}

.btn-primary {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
}

.btn-info {
  background: linear-gradient(135deg, #3b82f6, #60a5fa);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn-info:hover:not(:disabled) {
  box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
}

.btn-warning {
  background: linear-gradient(135deg, #f59e0b, #fbbf24);
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}

.btn-warning:hover:not(:disabled) {
  box-shadow: 0 6px 16px rgba(245, 158, 11, 0.4);
}

.btn-danger {
  background: linear-gradient(135deg, #ef4444, #f87171);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.btn-danger:hover:not(:disabled) {
  box-shadow: 0 6px 16px rgba(239, 68, 68, 0.4);
}

.btn-success {
  background: linear-gradient(135deg, #10b981, #34d399);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.btn-success:hover:not(:disabled) {
  box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4);
}

.btn-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
