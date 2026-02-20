<template>
  <div class="login-container">
    <div class="background-effects">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
    </div>

    <!-- Login Card -->
    <div v-if="!isInitializing" class="login-card" ref="loginCard">
      <div class="brand-header">
        <div class="logo-icon">
          <img src="/logo.svg" alt="NextGent Logo" class="brand-logo-image" style="width: 48px; height: 48px;" />
        </div>
        <h1 class="brand-name">NextGent</h1>
      </div>
      
      <div class="card-content">
        <h2 class="welcome-text">Hoş Geldiniz</h2>
        <p class="subtitle">Akıllı çalışma alanınıza giriş yapın</p>
        
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="input-group">
            <div class="input-icon">
              <CreditCard :size="20" :stroke-width="2" />
            </div>
            <input
              type="text"
              v-model="form.customer_id"
              placeholder="Müşteri ID (Örn: MED-001234)"
              class="input-field"
              required
              @input="form.customer_id = form.customer_id.toUpperCase()"
            />
          </div>
          
          <div class="input-group">
            <div class="input-icon">
              <Lock :size="20" :stroke-width="2" />
            </div>
            <input
              type="password"
              v-model="form.pin"
              placeholder="PIN (Varsayılan: 1234)"
              class="input-field"
              required
              maxlength="6"
            />
          </div>
          
          <button type="submit" class="btn-login" :disabled="isLoading">
            <span v-if="!isLoading">Giriş Yap</span>
            <div v-else class="spinner"></div>
          </button>
        </form>
      </div>
    </div>

    <!-- Cinematic Loader Overlay -->
    <div v-if="isInitializing" class="cinematic-loader" ref="resultLoader">
      <div class="loader-content">
        <div class="check-icon-wrapper">
          <Check :size="48" :stroke-width="3" />
        </div>
        <div class="loader-text">
          <h3>Kimlik Doğrulandı</h3>
          <p>Arayüz Hazırlanıyor...</p>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useNotificationStore } from '../stores/notification'
import { useSectorStore } from '../stores/sector'
import { Activity, CreditCard, Lock, Check } from 'lucide-vue-next'
import gsap from 'gsap'
import { inject } from 'vue'

const router = useRouter()
const authStore = useAuthStore()
const notificationStore = useNotificationStore()
const sectorStore = useSectorStore()
const axios = inject('axios')

const resultLoader = ref(null)
const loginCard = ref(null)

const form = ref({
  customer_id: '',
  pin: ''
})

const isLoading = ref(false)
const isInitializing = ref(false)

const handleLogin = async () => {
  isLoading.value = true
  
  try {
    // Call backend login API with customer ID + PIN
    const response = await axios.post('/auth/login', {
      customer_id: form.value.customer_id,
      pin: form.value.pin
    })
    
    // Set auth data from API response
    // Backend returns: { token, user, tenant_id, sector, tenant_name, customer_id }
    authStore.setToken(response.data.token)
    authStore.setUser(response.data.user)         // API returns 'user', not 'customer'
    authStore.setTenant(response.data.tenant_id)  // tenant_id is at top level
    
    // Set sector directly from API response (no need to parse tenant_config)
    sectorStore.setSector(response.data.sector || 'beauty')
    
    // Success - proceed to dashboard
    proceedToDashboard()
    
  } catch (error) {
    isLoading.value = false
    
    // Check if it's an authentication error (wrong ID or PIN)
    if (error.response && error.response.status === 401) {
      // SHAKE ANIMATION for wrong credentials
      gsap.to(loginCard.value, {
        x: -10,
        duration: 0.1,
        yoyo: true,
        repeat: 5,
        ease: 'power1.inOut',
        onComplete: () => {
          gsap.set(loginCard.value, { x: 0 })
        }
      })
      // Show error notification
      notificationStore.error('Geçersiz Müşteri ID veya PIN. Lütfen tekrar deneyin.', 'Giriş Başarısız')
      return
    }
    
    // For other errors (network, server down, etc), show error message
    console.error('❌ Giriş başarısız:', error)
    
    let errorMessage = 'Giriş başarısız. '
    
    if (error.response) {
      // Backend returned an error response
      console.log('Error Data:', error.response.data)
      errorMessage += `Sunucu Hatası (${error.response.status}): ${error.response.data.detail || JSON.stringify(error.response.data)}`
    } else if (error.request) {
      // Request made but no response
      errorMessage += 'Sunucuya ulaşılamıyor. Lütfen internet bağlantınızı ve backend servisini kontrol edin.'
    } else {
      // Setup error
      errorMessage += error.message
    }
    
    notificationStore.error(errorMessage, 'Giriş Hatası')
  }
}

const proceedToDashboard = () => {
  isLoading.value = false
  
  // Start cinematic exit animation
  gsap.to(loginCard.value, {
    scale: 0.95,
    opacity: 0,
    y: 20,
    duration: 0.5,
    ease: 'power2.in',
    onComplete: () => {
      isInitializing.value = true
      
      // Animate loader entry
      nextTick(() => {
        gsap.from(resultLoader.value, {
          opacity: 0,
          scale: 0.9,
          duration: 0.5
        })
      })

      // Wait a bit before navigating so user sees the success message
      setTimeout(() => {
        router.push('/dashboard')
      }, 800)
    }
  })
}

onMounted(() => {
  // Intro Animation
  gsap.from(loginCard.value, {
    y: 30,
    opacity: 0,
    duration: 0.8,
    ease: 'power3.out',
    delay: 0.2
  })
})
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #09090b; /* Obsidian Black */
  position: relative;
  overflow: hidden;
  font-family: 'Inter', sans-serif;
  padding: 24px;
}

.background-effects {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
}

.orb-1 {
  width: 400px;
  height: 400px;
  background: #4f46e5;
  top: -100px;
  left: -100px;
  animation: float 10s ease-in-out infinite;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: #7c3aed;
  bottom: -50px;
  right: -50px;
  animation: float 12s ease-in-out infinite reverse;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(30px, 50px); }
}

.login-card {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 420px;
  background: rgba(24, 24, 27, 0.7);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  gap: 32px;
  margin: 0 auto;
}

/* Responsive Design */
@media (max-width: 768px) {
  .login-card {
    padding: 32px 24px;
    max-width: 100%;
  }
  
  .welcome-text {
    font-size: 24px;
  }
  
  .brand-name {
    font-size: 20px;
  }
}

.brand-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 0 20px rgba(79, 70, 229, 0.4);
  padding: 8px;
}

.brand-logo-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  filter: brightness(0) invert(1);
}

.brand-name {
  font-size: 24px;
  font-weight: 700;
  color: white;
  letter-spacing: -0.02em;
}

.welcome-text {
  font-size: 28px;
  font-weight: 700;
  color: white;
  margin-bottom: 8px;
}

.subtitle {
  color: #a1a1aa;
  font-size: 14px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-top: 32px;
}

.input-group {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}

.input-icon {
  position: absolute;
  left: 14px;
  color: #71717a;
  z-index: 2;
  pointer-events: none;
}

.input-field {
  width: 100%;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 14px 14px 14px 44px;
  font-size: 15px;
  color: white;
  transition: all 0.2s ease;
}

.input-field:focus {
  outline: none;
  border-color: #6366f1;
  background: rgba(255, 255, 255, 0.06);
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
}

.input-field::placeholder {
  color: #52525b;
}

.btn-login {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: white;
  border: none;
  padding: 16px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
  margin-top: 8px; /* Added spacing */
}

.btn-login:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(79, 70, 229, 0.5);
}

.btn-login:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

/* Spinner */
.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Cinematic Loader */
.cinematic-loader {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 20;
}

.loader-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

.check-icon-wrapper {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #10b981;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 0 40px rgba(16, 185, 129, 0.5);
}

.loader-text {
  text-align: center;
  color: white;
}

.loader-text h3 {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 8px;
}

.loader-text p {
  color: #a1a1aa;
}
</style>
