<template>
  <div class="landing-contact">
    <div class="contact-container">
      <div class="contact-card glass-effect">
        <div class="contact-content">
          <h2>Bize Ulaşın</h2>
          <p>Potansiyelinizi birlikte keşfedelim.</p>
          <div class="action-buttons">
            <a href="mailto:iletisim@nextgent.com" class="action-btn primary">
              <Mail :size="20" />
              E-posta Gönder
            </a>
            <a href="tel:+902125550000" class="action-btn secondary">
              <Phone :size="20" />
              Bizi Arayın
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Mail, Phone } from 'lucide-vue-next'
</script>

<style scoped>
.landing-contact {
  padding: 40px 24px 80px;
  background-color: #030712;
}

.contact-container {
  max-width: 800px;
  margin: 0 auto;
}

.contact-card {
  padding: 48px;
  border-radius: 24px;
  background: linear-gradient(135deg, rgba(79, 70, 229, 0.1), rgba(124, 58, 237, 0.1));
  border: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;
}

.contact-content h2 {
  font-size: 32px;
  font-weight: 700;
  color: white;
  margin-bottom: 12px;
}

.contact-content p {
  color: #cbd5e1;
  font-size: 18px;
  margin-bottom: 32px;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;
  border-radius: 99px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
}

.action-btn.primary {
  background: white;
  color: #4f46e5;
}

.action-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(255, 255, 255, 0.2);
}

.action-btn.secondary {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.action-btn.secondary:hover {
  background: rgba(255, 255, 255, 0.2);
}
</style>
