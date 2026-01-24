<template>
  <Transition name="dialog">
    <div v-if="isVisible" class="session-expired-overlay" @click="handleClose">
      <div class="session-expired-dialog" @click.stop>
        <!-- Icon -->
        <div class="dialog-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
        </div>
        
        <!-- Content -->
        <h2 class="dialog-title">Session Expired</h2>
        <p class="dialog-message">
          Your session has expired for security reasons. Please log in again to continue.
        </p>
        
        <!-- Countdown -->
        <div class="dialog-countdown">
          Redirecting in <span class="countdown-number">{{ countdown }}</span> seconds...
        </div>
        
        <!-- Actions -->
        <div class="dialog-actions">
          <button @click="handleGoToLogin" class="btn-primary">
            Go to Login
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isVisible = ref(false)
const countdown = ref(3)
let countdownInterval = null

const show = () => {
  isVisible.value = true
  startCountdown()
}

const hide = () => {
  isVisible.value = false
  stopCountdown()
}

const startCountdown = () => {
  countdown.value = 3
  countdownInterval = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      stopCountdown()
      handleGoToLogin()
    }
  }, 1000)
}

const stopCountdown = () => {
  if (countdownInterval) {
    clearInterval(countdownInterval)
    countdownInterval = null
  }
}

const handleGoToLogin = () => {
  hide()
  router.push('/login')
}

const handleClose = () => {
  // Prevent closing by clicking overlay - user must click button
  // hide()
}

// Expose show method for parent components
defineExpose({
  show,
  hide
})

onUnmounted(() => {
  stopCountdown()
})
</script>

<style scoped>
.session-expired-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  padding: 20px;
}

.session-expired-dialog {
  background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
  border: 1px solid rgba(139, 92, 246, 0.3);
  border-radius: 24px;
  padding: 40px;
  max-width: 480px;
  width: 100%;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5),
              0 0 0 1px rgba(139, 92, 246, 0.1),
              0 0 60px rgba(139, 92, 246, 0.2);
  text-align: center;
  animation: dialog-appear 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.dialog-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 10px 30px rgba(139, 92, 246, 0.4);
  animation: icon-pulse 2s ease-in-out infinite;
}

.dialog-title {
  font-size: 28px;
  font-weight: 700;
  color: white;
  margin: 0 0 16px;
  letter-spacing: -0.5px;
}

.dialog-message {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
  margin: 0 0 24px;
}

.dialog-countdown {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 32px;
  font-weight: 500;
}

.countdown-number {
  display: inline-block;
  min-width: 20px;
  color: #8b5cf6;
  font-weight: 700;
  font-size: 18px;
}

.dialog-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn-primary {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  border: none;
  padding: 14px 32px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(139, 92, 246, 0.6);
}

.btn-primary:active {
  transform: translateY(0);
}

/* Animations */
@keyframes dialog-appear {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes icon-pulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 10px 30px rgba(139, 92, 246, 0.4);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 15px 40px rgba(139, 92, 246, 0.6);
  }
}

/* Transition */
.dialog-enter-active,
.dialog-leave-active {
  transition: opacity 0.3s ease;
}

.dialog-enter-from,
.dialog-leave-to {
  opacity: 0;
}

.dialog-enter-active .session-expired-dialog,
.dialog-leave-active .session-expired-dialog {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.dialog-enter-from .session-expired-dialog,
.dialog-leave-to .session-expired-dialog {
  transform: scale(0.9) translateY(-20px);
}
</style>
