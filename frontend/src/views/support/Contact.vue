<template>
  <div class="contact-page">
    <!-- Background Effects -->
    <div class="bg-gradient"></div>
    <div class="bg-overlay"></div>

    <div class="contact-container">
      <!-- Header Section -->
      <div class="page-header">
        <div class="icon-wrapper">
          <Mail :size="32" :stroke-width="2" />
        </div>
        <h1 class="page-title">İletişime Geç</h1>
        <p class="page-subtitle">Size nasıl yardımcı olabiliriz? Mesajınızı bırakın, en kısa sürede size dönüş yapalım.</p>
      </div>

      <!-- Contact Methods Grid -->
      <div class="contact-methods">
        <div class="method-card glass-effect">
          <div class="method-icon">
            <Phone :size="24" />
          </div>
          <h3>Telefon</h3>
          <p>+90 (212) 555 0000</p>
          <span class="availability">Hafta içi 09:00 - 18:00</span>
        </div>

        <div class="method-card glass-effect">
          <div class="method-icon">
            <Mail :size="24" />
          </div>
          <h3>E-posta</h3>
          <p>destek@nextgent.com</p>
          <span class="availability">7/24 Destek</span>
        </div>

        <div class="method-card glass-effect">
          <div class="method-icon">
            <MessageCircle :size="24" />
          </div>
          <h3>Canlı Destek</h3>
          <p>Anında yardım alın</p>
          <span class="availability">Çevrimiçi</span>
        </div>
      </div>

      <!-- Contact Form -->
      <div class="contact-card glass-effect">
        <h2 class="form-title">
          <Send :size="20" />
          Mesaj Gönderin
        </h2>
        
        <Transition name="success-fade">
          <div v-if="showSuccess" class="success-banner">
            <CheckCircle :size="18" />
            <span>Mesajınız başarıyla gönderildi! En kısa sürede size dönüş yapacağız.</span>
          </div>
        </Transition>

        <form @submit.prevent="handleSubmit" class="contact-form">
          <div class="form-row">
            <div class="form-group">
              <label for="name">
                <User :size="16" />
                Ad Soyad
              </label>
              <input
                id="name"
                v-model="form.name"
                type="text"
                required
                placeholder="Adınız ve soyadınız"
                :disabled="isSubmitting"
              />
            </div>

            <div class="form-group">
              <label for="email">
                <Mail :size="16" />
                E-posta
              </label>
              <input
                id="email"
                v-model="form.email"
                type="email"
                required
                placeholder="ornek@email.com"
                :disabled="isSubmitting"
              />
            </div>
          </div>

          <div class="form-group">
            <label for="subject">
              <FileText :size="16" />
              Konu
            </label>
            <input
              id="subject"
              v-model="form.subject"
              type="text"
              required
              placeholder="Mesajınızın konusu"
              :disabled="isSubmitting"
            />
          </div>

          <div class="form-group">
            <label for="message">
              <MessageSquare :size="16" />
              Mesajınız
            </label>
            <textarea
              id="message"
              v-model="form.message"
              rows="6"
              required
              placeholder="Mesajınızı detaylı bir şekilde yazın..."
              :disabled="isSubmitting"
            ></textarea>
            <div class="char-count">{{ form.message.length }} / 1000</div>
          </div>

          <button type="submit" class="submit-btn" :disabled="isSubmitting">
            <span v-if="!isSubmitting">
              <Send :size="18" />
              Gönder
            </span>
            <span v-else class="loading-spinner">
              <Loader2 :size="18" class="spin" />
              Gönderiliyor...
            </span>
          </button>
        </form>
      </div>

      <!-- Back Link -->
      <div class="back-link">
        <router-link to="/" class="btn-back">
          <ArrowLeft :size="18" />
          Ana Sayfaya Dön
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Mail, Phone, MessageCircle, Send, User, FileText, MessageSquare, CheckCircle, ArrowLeft, Loader2 } from 'lucide-vue-next'

const form = ref({
  name: '',
  email: '',
  subject: '',
  message: ''
})

const isSubmitting = ref(false)
const showSuccess = ref(false)

const handleSubmit = async () => {
  if (form.value.message.length > 1000) {
    alert('Mesaj çok uzun. Maksimum 1000 karakter olabilir.')
    return
  }

  isSubmitting.value = true

  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 1500))

  console.log('Form submitted:', form.value)
  
  showSuccess.value = true
  form.value = { name: '', email: '', subject: '', message: '' }
  isSubmitting.value = false

  // Hide success message after 5 seconds
  setTimeout(() => {
    showSuccess.value = false
  }, 5000)
}
</script>

<style scoped>
.contact-page {
  position: relative;
  min-height: 100vh;
  background: #030712;
  padding: 100px 24px 60px;
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
    rgba(99, 102, 241, 0.08) 0%,
    rgba(139, 92, 246, 0.05) 25%,
    transparent 50%
  );
  animation: rotate 40s linear infinite;
  pointer-events: none;
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
    rgba(6, 182, 212, 0.06) 0%,
    transparent 50%
  );
  pointer-events: none;
}

.contact-container {
  position: relative;
  z-index: 10;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  padding: 0 24px;
}

/* Header */
.page-header {
  text-align: center;
  margin-bottom: 64px;
}

.icon-wrapper {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 0 40px rgba(99, 102, 241, 0.3);
}

.page-title {
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 16px;
  background: linear-gradient(135deg, #818cf8, #c084fc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-subtitle {
  font-size: 18px;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Contact Methods Grid */
.contact-methods {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 48px;
}

.method-card {
  padding: 32px 24px;
  border-radius: 16px;
  text-align: center;
  transition: all 0.3s;
}

.method-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(99, 102, 241, 0.15);
}

.method-icon {
  width: 56px;
  height: 56px;
  margin: 0 auto 20px;
  background: rgba(99, 102, 241, 0.15);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #818cf8;
}

.method-card h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.method-card p {
  color: var(--text-secondary);
  font-size: 15px;
  margin-bottom: 12px;
}

.availability {
  display: inline-block;
  padding: 6px 12px;
  background: rgba(34, 197, 94, 0.1);
  border: 1px solid rgba(34, 197, 94, 0.2);
  border-radius: 20px;
  color: #22c55e;
  font-size: 12px;
  font-weight: 600;
}

/* Contact Form Card */
.contact-card {
  padding: 48px 40px;
  border-radius: 24px;
  margin-bottom: 48px;
}

.form-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 32px;
}

/* Success Banner */
.success-banner {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  background: rgba(34, 197, 94, 0.1);
  border: 1px solid rgba(34, 197, 94, 0.3);
  border-radius: 12px;
  color: #22c55e;
  font-size: 14px;
  margin-bottom: 32px;
}

.success-fade-enter-active, .success-fade-leave-active {
  transition: all 0.3s ease;
}

.success-fade-enter-from, .success-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Form */
.contact-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  position: relative;
}

.form-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 600;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 14px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: var(--text-primary);
  font-size: 15px;
  font-family: 'Inter', sans-serif;
  transition: all 0.2s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.08);
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.form-group input:disabled,
.form-group textarea:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.form-group textarea {
  resize: vertical;
  min-height: 140px;
}

.char-count {
  position: absolute;
  bottom: -24px;
  right: 0;
  font-size: 12px;
  color: var(--text-muted);
}

/* Submit Button */
.submit-btn {
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

.submit-btn span {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(99, 102, 241, 0.4);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
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

/* Back Link */
.back-link {
  text-align: center;
}

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 99px;
  color: white;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-back:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

/* Responsive */
@media (max-width: 768px) {
  .contact-page {
    padding: 80px 16px 40px;
  }

  .page-title {
    font-size: 36px;
  }

  .page-subtitle {
    font-size: 16px;
  }

  .contact-methods {
    grid-template-columns: 1fr;
  }

  .contact-card {
    padding: 32px 24px;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
