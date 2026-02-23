<template>
  <div class="admin-login">
    <!-- Background Effects -->
    <div class="bg-gradient"></div>
    <div class="bg-overlay"></div>

    <!-- Login Card -->
    <div class="login-container">
      <div class="login-card glass-effect">
        <!-- Logo/Header -->
        <div class="login-header">
          <div class="logo-container">
            <div class="logo-icon">
              <img src="/logo.svg" alt="NextGent Logo" class="admin-logo-image" style="width: 60px; height: 60px;" />
            </div>
            <h1>NextGent Admin</h1>
          </div>
          <p class="subtitle">Sistem Yönetimi Paneli</p>
        </div>

        <!-- Error Message -->
        <Transition name="fade">
          <div v-if="errorMessage" class="error-banner">
            <AlertCircle :size="16" />
            <span>{{ errorMessage }}</span>
          </div>
        </Transition>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="username">
              <User :size="16" />
              Kullanıcı Adı
            </label>
            <input
              id="username"
              v-model="username"
              type="text"
              placeholder="admin"
              autocomplete="username"
              required
              :disabled="isLoading"
            />
          </div>

          <div class="form-group">
            <label for="password">
              <Lock :size="16" />
              Şifre
            </label>
            <div class="password-input">
              <input
                id="password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="••••••••"
                autocomplete="current-password"
                required
                :disabled="isLoading"
              />
              <button
                type="button"
                class="toggle-password"
                @click="showPassword = !showPassword"
                :disabled="isLoading"
              >
                <Eye v-if="!showPassword" :size="18" />
                <EyeOff v-else :size="18" />
              </button>
            </div>
          </div>

          <button type="submit" class="login-btn" :disabled="isLoading">
            <span v-if="!isLoading">Giriş Yap</span>
            <span v-else class="loading-spinner">
              <Loader2 :size="20" class="spin" />
              Giriş yapılıyor...
            </span>
          </button>
        </form>

        <!-- Footer -->
        <div class="login-footer">
          <div class="security-badge">
            <LockKeyhole :size="14" />
            <span>Güvenli Bağlantı</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAdminStore } from '@/stores/admin'
import { Shield, User, Lock, Eye, EyeOff, Loader2, AlertCircle, LockKeyhole } from 'lucide-vue-next'

const router = useRouter()
const adminStore = useAdminStore()

const username = ref('')
const password = ref('')
const showPassword = ref(false)
const isLoading = ref(false)
const errorMessage = ref('')

async function handleLogin() {
  if (!username.value || !password.value) {
    errorMessage.value = 'Lütfen tüm alanları doldurun'
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  try {
    await adminStore.login(username.value, password.value)
    router.push('/admin/dashboard')
  } catch (error) {
    const message = error.response?.data?.detail || 'Giriş başarısız. Lütfen bilgilerinizi kontrol edin.'
    errorMessage.value = message
    
    // Clear error after 5 seconds
    setTimeout(() => {
      errorMessage.value = ''
    }, 5000)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.admin-login {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #030712;
  overflow: hidden;
}

/* Background Effects */
.bg-gradient {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(
    circle at 50% 50%,
    rgba(99, 102, 241, 0.15) 0%,
    rgba(139, 92, 246, 0.1) 25%,
    transparent 50%
  );
  animation: rotate 30s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.bg-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(
    circle at 20% 80%,
    rgba(6, 182, 212, 0.1) 0%,
    transparent 50%
  ),
  radial-gradient(
    circle at 80% 20%,
    rgba(168, 85, 247, 0.1) 0%,
    transparent 50%
  );
}

/* Login Container */
.login-container {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 440px;
  padding: 24px;
}

.login-card {
  padding: 48px 40px;
  border-radius: 24px;
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Header */
.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
}

.logo-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 0 40px rgba(99, 102, 241, 0.4);
}

.admin-logo-image {
  width: 50px;
  height: 50px;
  object-fit: contain;
  filter: brightness(0) invert(1);
}

.login-header h1 {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.subtitle {
  color: var(--text-secondary);
  font-size: 15px;
}

/* Error Banner */
.error-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 12px;
  color: #ef4444;
  font-size: 14px;
  margin-bottom: 24px;
}

.fade-enter-active, .fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Form */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.form-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 600;
}

.form-group input {
  width: 100%;
  padding: 14px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: var(--text-primary);
  font-size: 15px;
  transition: all 0.2s;
}

.form-group input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.08);
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.form-group input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.password-input {
  position: relative;
}

.password-input input {
  padding-right: 48px;
}

.toggle-password {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
}

.toggle-password:hover {
  color: var(--text-secondary);
}

.toggle-password:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Login Button */
.login-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 8px;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4);
}

.login-btn:active:not(:disabled) {
  transform: translateY(0);
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Footer */
.login-footer {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: center;
}

.security-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--text-muted);
  font-size: 13px;
}

/* Responsive */
@media (max-width: 480px) {
  .login-container {
    padding: 16px;
  }

  .login-card {
    padding: 32px 24px;
  }

  .login-header h1 {
    font-size: 26px;
  }

  .logo-icon {
    width: 64px;
    height: 64px;
  }
}
</style>
