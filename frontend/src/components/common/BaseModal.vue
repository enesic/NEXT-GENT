<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="modelValue"
        class="modal-overlay"
        @click="handleOverlayClick"
        role="dialog"
        aria-modal="true"
        :aria-labelledby="titleId"
      >
        <div
          ref="modalRef"
          class="modal-container"
          :class="[`modal-${size}`, modalClass]"
          @click.stop
        >
          <!-- Header -->
          <div v-if="$slots.header || title" class="modal-header">
            <slot name="header">
              <h2 :id="titleId" class="modal-title">{{ title }}</h2>
            </slot>
            <button
              v-if="showClose"
              class="modal-close"
              @click="close"
              aria-label="Close modal"
              type="button"
            >
              <X :size="20" />
            </button>
          </div>

          <!-- Body -->
          <div class="modal-body" :class="bodyClass">
            <slot></slot>
          </div>

          <!-- Footer -->
          <div v-if="$slots.footer" class="modal-footer">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, computed } from 'vue'
import { X } from 'lucide-vue-next'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large', 'fullscreen'].includes(value)
  },
  closeOnOverlay: {
    type: Boolean,
    default: true
  },
  closeOnEsc: {
    type: Boolean,
    default: true
  },
  showClose: {
    type: Boolean,
    default: true
  },
  modalClass: {
    type: String,
    default: ''
  },
  bodyClass: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'close'])

const modalRef = ref(null)
const titleId = computed(() => `modal-title-${Math.random().toString(36).substr(2, 9)}`)

const close = () => {
  emit('update:modelValue', false)
  emit('close')
}

const handleOverlayClick = () => {
  if (props.closeOnOverlay) {
    close()
  }
}

const handleEscKey = (event) => {
  if (event.key === 'Escape' && props.closeOnEsc && props.modelValue) {
    close()
  }
}

// Focus trap
const focusableElements = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
let firstFocusableElement = null
let lastFocusableElement = null

const handleTabKey = (event) => {
  if (!props.modelValue) return

  const focusables = modalRef.value?.querySelectorAll(focusableElements)
  if (!focusables || focusables.length === 0) return

  firstFocusableElement = focusables[0]
  lastFocusableElement = focusables[focusables.length - 1]

  if (event.key === 'Tab') {
    if (event.shiftKey) {
      // Shift + Tab
      if (document.activeElement === firstFocusableElement) {
        lastFocusableElement.focus()
        event.preventDefault()
      }
    } else {
      // Tab
      if (document.activeElement === lastFocusableElement) {
        firstFocusableElement.focus()
        event.preventDefault()
      }
    }
  }
}

// Body scroll lock
const lockBodyScroll = () => {
  document.body.style.overflow = 'hidden'
}

const unlockBodyScroll = () => {
  document.body.style.overflow = ''
}

watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    lockBodyScroll()
    // Focus first element when modal opens
    setTimeout(() => {
      const focusables = modalRef.value?.querySelectorAll(focusableElements)
      if (focusables && focusables.length > 0) {
        focusables[0].focus()
      }
    }, 100)
  } else {
    unlockBodyScroll()
  }
})

onMounted(() => {
  document.addEventListener('keydown', handleEscKey)
  document.addEventListener('keydown', handleTabKey)
})

onBeforeUnmount(() => {
  document.removeEventListener('keydown', handleEscKey)
  document.removeEventListener('keydown', handleTabKey)
  unlockBodyScroll()
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  padding: 20px;
  overflow-y: auto;
}

.modal-container {
  background: rgba(17, 24, 39, 0.98);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5),
              0 0 0 1px rgba(255, 255, 255, 0.05);
  display: flex;
  flex-direction: column;
  max-height: calc(100vh - 40px);
  position: relative;
  will-change: transform, opacity;
}

/* Size variants */
.modal-small {
  width: 100%;
  max-width: 400px;
}

.modal-medium {
  width: 100%;
  max-width: 600px;
}

.modal-large {
  width: 100%;
  max-width: 900px;
}

.modal-fullscreen {
  width: calc(100vw - 40px);
  height: calc(100vh - 40px);
  max-width: none;
  max-height: none;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  flex-shrink: 0;
}

.modal-title {
  font-size: 20px;
  font-weight: 700;
  color: white;
  margin: 0;
  letter-spacing: -0.02em;
}

.modal-close {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: #9ca3af;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
  padding: 0;
}

.modal-close:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  transform: scale(1.05);
}

.modal-close:focus {
  outline: 2px solid rgba(99, 102, 241, 0.5);
  outline-offset: 2px;
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
  flex: 1;
  color: #d1d5db;
  line-height: 1.6;
}

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  flex-shrink: 0;
}

/* Modal Transitions */
.modal-enter-active {
  transition: opacity 0.3s ease;
}

.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-container {
  animation: modal-slide-up 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-leave-active .modal-container {
  animation: modal-slide-down 0.2s cubic-bezier(0.4, 0, 1, 1);
}

@keyframes modal-slide-up {
  from {
    transform: translateY(40px) scale(0.95);
    opacity: 0;
  }
  to {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
}

@keyframes modal-slide-down {
  from {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
  to {
    transform: translateY(40px) scale(0.95);
    opacity: 0;
  }
}

/* Mobile Responsive */
@media (max-width: 640px) {
  .modal-overlay {
    padding: 16px;
  }

  .modal-container {
    max-height: calc(100vh - 32px);
  }

  .modal-fullscreen {
    width: calc(100vw - 32px);
    height: calc(100vh - 32px);
  }

  .modal-header {
    padding: 20px;
  }

  .modal-body {
    padding: 20px;
  }

  .modal-footer {
    padding: 16px 20px;
  }

  .modal-title {
    font-size: 18px;
  }
}

/* Reduce motion for accessibility */
@media (prefers-reduced-motion: reduce) {
  .modal-enter-active,
  .modal-leave-active {
    transition-duration: 0.01ms !important;
  }

  .modal-enter-active .modal-container,
  .modal-leave-active .modal-container {
    animation: none !important;
  }
}

/* Custom scrollbar for modal body */
.modal-body::-webkit-scrollbar {
  width: 8px;
}

.modal-body::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.02);
  border-radius: 4px;
}

.modal-body::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.modal-body::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.15);
}
</style>
