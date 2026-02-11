<template>
  <div class="error-boundary">
    <slot v-if="!error"></slot>
    <div v-else class="error-boundary-fallback">
      <slot name="fallback" :error="error" :retry="retry">
        <ErrorState
          variant="error"
          :title="fallbackTitle"
          :message="fallbackMessage"
          action-text="Try Again"
          @action="retry"
        >
          <template v-if="showErrorDetails && error">
            <details class="error-details">
              <summary>Error Details</summary>
              <pre class="error-stack">{{ error.message }}</pre>
              <pre v-if="error.stack" class="error-stack">{{ error.stack }}</pre>
            </details>
          </template>
        </ErrorState>
      </slot>
    </div>
  </div>
</template>

<script setup>
import { ref, onErrorCaptured, provide } from 'vue'
import ErrorState from './ErrorState.vue'

const props = defineProps({
  fallbackTitle: {
    type: String,
    default: 'Something went wrong'
  },
  fallbackMessage: {
    type: String,
    default: 'An unexpected error occurred. Please try again or contact support if the problem persists.'
  },
  onError: {
    type: Function,
    default: null
  },
  showErrorDetails: {
    type: Boolean,
    default: false
  },
  logErrors: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['error', 'retry'])

const error = ref(null)
const errorInfo = ref(null)
const retryKey = ref(0)

// Capture errors from child components
onErrorCaptured((err, instance, info) => {
  error.value = err
  errorInfo.value = info

  // Log error if enabled
  if (props.logErrors) {
    console.error('ErrorBoundary caught an error:', err)
    console.error('Component:', instance)
    console.error('Error info:', info)
  }

  // Call custom error handler if provided
  if (props.onError) {
    props.onError(err, instance, info)
  }

  // Emit error event
  emit('error', { error: err, instance, info })

  // Prevent error from propagating further
  return false
})

// Retry function to reset error state
const retry = () => {
  error.value = null
  errorInfo.value = null
  retryKey.value++
  emit('retry')
}

// Provide retry function to descendants
provide('errorBoundaryRetry', retry)
</script>

<style scoped>
.error-boundary {
  width: 100%;
  height: 100%;
}

.error-boundary-fallback {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error-details {
  margin-top: 20px;
  text-align: left;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 16px;
  max-width: 600px;
  width: 100%;
}

.error-details summary {
  cursor: pointer;
  font-weight: 600;
  color: #d1d5db;
  margin-bottom: 12px;
  user-select: none;
}

.error-details summary:hover {
  color: white;
}

.error-stack {
  margin: 8px 0 0 0;
  padding: 12px;
  background: rgba(0, 0, 0, 0.4);
  border-radius: 6px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  color: #ef4444;
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
  line-height: 1.5;
}

/* Custom scrollbar for error details */
.error-stack::-webkit-scrollbar {
  height: 8px;
}

.error-stack::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

.error-stack::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.error-stack::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.15);
}
</style>
