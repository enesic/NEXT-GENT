<template>
  <div class="landing-support">
    <div class="support-container">
      <div class="section-header">
        <h2>7/24 Uzman Destek</h2>
        <p>İhtiyaç duyduğunuz her an yanınızdayız.</p>
      </div>

      <div class="support-channels">
        <div class="channel-card glass-effect">
          <Clock :size="32" class="icon" />
          <div class="content">
            <h3>7/24 Canlı Destek</h3>
            <p>Anında yanıt</p>
          </div>
        </div>

        <div class="channel-card glass-effect">
          <Mail :size="32" class="icon" />
          <div class="content">
            <h3>E-posta Desteği</h3>
            <p>destek@nextgent.com</p>
          </div>
        </div>

        <div class="channel-card glass-effect">
          <Phone :size="32" class="icon" />
          <div class="content">
            <h3>Telefon</h3>
            <p>+90 (212) 555 0000</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Clock, Mail, Phone } from 'lucide-vue-next'
</script>

<style scoped>

.landing-support {
  padding: 100px 24px; /* Increased top/bottom padding */
  background-color: #030712;
  color: #fff;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.support-container {
  max-width: 1200px; /* Increased max-width */
  margin: 0 auto;
  text-align: center;
}

.section-header h2 {
  font-size: 36px; /* Larger title */
  font-weight: 700;
  margin-bottom: 12px;
  color: white;
}

.section-header p {
  color: #94a3b8;
  margin-bottom: 60px; /* More space below header */
  font-size: 18px;
}

.support-channels {
  display: flex;
  justify-content: center;
  gap: 32px; /* Increased gap */
  flex-wrap: wrap;
}

.channel-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 32px 48px; /* Larger padding for bigger boxes */
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  min-width: 300px; /* Wider minimum width */
  transition: all 0.3s;
}

.channel-card:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateY(-4px);
}

.icon {
  color: #6366f1;
}

.content h3 {
  font-size: 20px; /* Larger text */
  font-weight: 600;
  color: white;
  margin: 0;
}

.content p {
  font-size: 16px; /* Larger text */
  color: #94a3b8;
  margin: 4px 0 0 0;
}
</style>
