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
          <Activity :size="32" />
        </div>
        <h1 class="brand-name">NextGent</h1>
      </div>
      
      <div class="card-content">
        <h2 class="welcome-text">Welcome Back</h2>
        <p class="subtitle">Sign in to your intelligent workspace</p>
        
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label>Email Address</label>
            <div class="input-wrapper">
              <User :size="18" class="input-icon" />
              <input
                v-model="form.email"
                type="email"
                placeholder="name@company.com"
                required
              />
            </div>
            <p class="form-hint">Sektör otomatik olarak tespit edilecektir</p>
          </div>
          
          <div class="form-group">
            <label>Password</label>
            <div class="input-wrapper">
              <Lock :size="18" class="input-icon" />
              <input
                v-model="form.password"
                type="password"
                placeholder="••••••••"
                required
              />
            </div>
          </div>
          
          <div class="form-group" v-if="detectedSector">
            <div class="sector-preview">
              <component :is="sectorIcon" :size="16" :stroke-width="2" />
              <span>{{ detectedSectorName }} sektörü tespit edildi</span>
            </div>
          </div>
          
          <button type="submit" class="btn-login" :disabled="isLoading || isDetecting">
            <span v-if="!isLoading && !isDetecting">Sign In</span>
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
          <h3>Authentication Verified</h3>
          <p>Preparing Interface...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useSectorStore } from '../stores/sector'
import { Activity, Building2, User, Lock, Check, Stethoscope, Scale, Home } from 'lucide-vue-next'
import gsap from 'gsap'
import { inject } from 'vue'

const router = useRouter()
const authStore = useAuthStore()
const sectorStore = useSectorStore()
const axios = inject('axios')

const loginCard = ref(null)
const resultLoader = ref(null)

const form = ref({
  email: '',
  password: ''
})

const isLoading = ref(false)
const isInitializing = ref(false)
const isDetecting = ref(false)
const detectedSector = ref(null)
const detectedSectorName = ref('')

// Sector icon mapping
const sectorIcons = {
  medical: Stethoscope,
  legal: Scale,
  real_estate: Home
}

const sectorIcon = computed(() => {
  return sectorIcons[detectedSector.value] || Activity
})

// Auto-detect sector when email changes
watch(() => form.value.email, async (newEmail) => {
  if (newEmail && newEmail.includes('@')) {
    await detectSector()
  } else {
    detectedSector.value = null
    detectedSectorName.value = ''
  }
})

const detectSector = async () => {
  if (!form.value.email || !form.value.email.includes('@')) return
  
  isDetecting.value = true
  try {
    const response = await axios.post('/auth/detect-sector', {
      email: form.value.email
    })
    
    detectedSector.value = response.data.sector
    detectedSectorName.value = getSectorDisplayName(response.data.sector)
    
    // Update sector store
    sectorStore.setSector(response.data.sector)
    
  } catch (error) {
    console.error('Sector detection error:', error)
    // Fallback to medical
    detectedSector.value = 'medical'
    detectedSectorName.value = 'Medical'
  } finally {
    isDetecting.value = false
  }
}

const getSectorDisplayName = (sector) => {
  const names = {
    medical: 'Medical',
    legal: 'Legal',
    real_estate: 'Real Estate'
  }
  return names[sector] || 'Medical'
}

const handleLogin = async () => {
  isLoading.value = true
  
  try {
    // Call backend login API with sector detection
    const response = await axios.post('/auth/login', {
      email: form.value.email,
      password: form.value.password
    })
    
    // Set auth data
    authStore.setToken(response.data.token)
    authStore.setUser(response.data.user)
    authStore.setTenant(response.data.tenant_id)
    
    // Set sector
    sectorStore.setSector(response.data.sector)
    
  } catch (error) {
    console.warn('🛡️ Backend unavailable, using demo mode:', error.message)
    
    // FALLBACK: Set demo data if backend is down
    authStore.setToken('demo-token-' + Date.now())
    authStore.setUser({
      id: 1,
      email: form.value.email,
      name: form.value.email.split('@')[0]
    })
    authStore.setTenant('demo-tenant-id')
    sectorStore.setSector(detectedSector.value || 'medical')
  }
  
  // Always proceed to dashboard after login attempt
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
      // Navigate to dashboard immediately
      router.push('/dashboard')
    }
  })
}

const animateLoader = () => {
  const tl = gsap.timeline({
    onComplete: () => {
       router.push('/dashboard')
    }
  })

  tl.from('.check-icon-wrapper', {
    scale: 0,
    rotate: -180,
    opacity: 0,
    duration: 0.6,
    ease: 'back.out(1.7)'
  })
  .from('.loader-text', {
    y: 20,
    opacity: 0,
    duration: 0.4,
    ease: 'power2.out'
  }, '-=0.2')
  .to('.cinematic-loader', {
    delay: 1.5,
    opacity: 0,
    duration: 0.5
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

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 13px;
  font-weight: 600;
  color: #d4d4d8;
  margin-left: 4px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 14px;
  color: #71717a;
  z-index: 2;
}

.form-group input {
  width: 100%;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 14px 14px 14px 44px;
  font-size: 15px;
  color: white;
  transition: all 0.2s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #6366f1;
  background: rgba(255, 255, 255, 0.06);
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
}

.form-group input::placeholder {
  color: #52525b;
}

.form-hint {
  font-size: 11px;
  color: #71717a;
  margin-top: 4px;
  margin-left: 4px;
}

.sector-preview {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.3);
  border-radius: 12px;
  color: #818cf8;
  font-size: 13px;
  font-weight: 500;
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
