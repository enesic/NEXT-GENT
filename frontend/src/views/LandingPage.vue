<template>
  <div class="landing-container">
    <nav class="landing-nav">
      <div class="logo">
        <div class="logo-icon"></div>
        <span class="logo-text">NextGent</span>
      </div>
      <div class="nav-links">
        <a href="#features">Çözümler</a>
        <a href="#sectors">Sektörler</a>
        <a href="#about">Hakkımızda</a>
        <button class="login-btn" @click="$router.push('/login')">Giriş Yap</button>
      </div>
    </nav>

    <header class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          Yapay Zeka ile <br />
          <span class="gradient-text">Geleceği Yönetin</span>
        </h1>
        <p class="hero-subtitle">
          NextGent, işletmenizin operasyonel zekasını artırır. 
          Sesli asistanlar, öngörücü analitik ve entegre yönetim paneli ile tanışın.
        </p>
        <div class="cta-group">
          <button class="primary-btn" @click="$router.push('/login')">
            Hemen Başlayın
            <ArrowRight class="icon" />
          </button>
          <button class="secondary-btn">Demoyu İzle</button>
        </div>
      </div>
      <div class="hero-visual">
        <div class="orbital-ring option-1"></div>
        <div class="orbital-ring option-2"></div>
        <div class="floating-card">
          <div class="card-icon"><Activity /></div>
          <div class="card-text">
            <span>Canlı Performans</span>
            <strong>%98.4 Verimlilik</strong>
          </div>
        </div>
        <div class="floating-card glass-2">
            <div class="card-icon"><MessageSquare /></div>
            <div class="card-text">
              <span>AI Asistan</span>
              <strong>Aktif</strong>
            </div>
          </div>
      </div>
    </header>

    <section id="features" class="features-section">
      <div class="section-header">
        <h2>Gücümüz Teknolojimizden Gelir</h2>
        <p>KVKK uyumlu, %100 güvenli ve ölçeklenebilir altyapı.</p>
      </div>
      <div class="features-grid">
        <div class="feature-card">
          <ShieldCheck class="feature-icon" />
          <h3>KVKK ve GDPR Uyumlu</h3>
          <p>Verileriniz en yüksek güvenlik standartlarında şifrelenir ve korunur. Yasal mevzuatlara tam uyum.</p>
        </div>
        <div class="feature-card">
          <Zap class="feature-icon" />
          <h3>Gerçek Zamanlı Analitik</h3>
          <p>İşletmenizin nabzını anlık tutun. Veriye dayalı kararlar alarak büyümenizi hızlandırın.</p>
        </div>
        <div class="feature-card">
          <Cpu class="feature-icon" />
          <h3>Otonom AI Asistan</h3>
          <p>Müşterilerinizle 7/24 ilgilenen, randevu alan ve sorun çözen akıllı asistanlar.</p>
        </div>
      </div>
    </section>

    <footer class="landing-footer">
      <div class="footer-content">
        <div class="footer-logo">NextGent</div>
        <p class="copyright">© 2026 NextGent Technology. All rights reserved.</p>
      </div>
    </footer>

    <!-- AI Helpdesk Chatbot -->
    <HelpdeskChatbot />
  </div>
</template>

<script setup>
import { ArrowRight, ShieldCheck, Zap, Cpu, Activity, MessageSquare } from 'lucide-vue-next'
import { onMounted } from 'vue'
import gsap from 'gsap'
import HelpdeskChatbot from '../components/HelpdeskChatbot.vue'

onMounted(() => {
  // Intro Animation
  gsap.from('.hero-title', {
    y: 50,
    opacity: 0,
    duration: 1,
    ease: 'power3.out'
  })

  gsap.from('.hero-subtitle', {
    y: 30,
    opacity: 0,
    duration: 1,
    delay: 0.3,
    ease: 'power3.out'
  })

  gsap.from('.cta-group', {
    y: 20,
    opacity: 0,
    duration: 1,
    delay: 0.5,
    ease: 'power3.out'
  })

  gsap.from('.orbital-ring', {
    scale: 0,
    opacity: 0,
    duration: 1.5,
    stagger: 0.2,
    ease: 'elastic.out(1, 0.5)',
    delay: 0.2
  })
})
</script>

<style scoped>
.landing-container {
  min-height: 100vh;
  width: 100%;
  background-color: #030712; /* Obsidian Black */
  color: #ffffff;
  font-family: 'Inter', sans-serif;
  overflow-x: hidden;
  position: relative;
}

.landing-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 48px;
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 100;
  background: rgba(3, 7, 18, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  border-radius: 8px;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 32px;
}

.nav-links a {
  color: #9ca3af;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.2s;
}

.nav-links a:hover {
  color: #ffffff;
}

.login-btn {
  padding: 8px 20px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 99px;
  color: white;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.login-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* Hero Section */
.hero-section {
  padding: 180px 48px 100px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1400px;
  margin: 0 auto;
  gap: 48px;
  flex-wrap: wrap;
  width: 100%;
  box-sizing: border-box;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .hero-section {
    flex-direction: column;
    text-align: center;
    padding: 140px 24px 80px;
  }
  
  .hero-content {
    max-width: 100%;
  }
  
  .hero-visual {
    width: 100%;
    max-width: 500px;
    margin: 0 auto;
  }
  
  .hero-title {
    font-size: 48px;
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 120px 16px 60px;
  }
  
  .hero-title {
    font-size: 36px;
  }
  
  .hero-subtitle {
    font-size: 16px;
  }
  
  .cta-group {
    flex-direction: column;
    width: 100%;
  }
  
  .primary-btn,
  .secondary-btn {
    width: 100%;
  }
  
  .landing-nav {
    padding: 16px 24px;
  }
  
  .nav-links {
    gap: 16px;
  }
  
  .nav-links a {
    display: none;
  }
  
  .features-section {
    padding: 60px 24px;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }
}

.hero-content {
  max-width: 600px;
}

.hero-title {
  font-size: 64px;
  line-height: 1.1;
  font-weight: 800;
  margin-bottom: 24px;
  letter-spacing: -0.03em;
}

.gradient-text {
  background: linear-gradient(135deg, #818cf8, #c084fc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 18px;
  line-height: 1.6;
  color: #9ca3af;
  margin-bottom: 40px;
}

.cta-group {
  display: flex;
  gap: 16px;
}

.primary-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 32px;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  border: none;
  border-radius: 99px;
  color: white;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -5px rgba(124, 58, 237, 0.5);
}

.secondary-btn {
  padding: 16px 32px;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 99px;
  color: white;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.2s;
}

.secondary-btn:hover {
  background: rgba(255, 255, 255, 0.05);
}

/* Hero Visual */
.hero-visual {
  position: relative;
  width: 500px;
  height: 500px;
  flex-shrink: 0;
}

@media (max-width: 1024px) {
  .hero-visual {
    width: 100%;
    max-width: 500px;
    height: 400px;
  }
}

@media (max-width: 768px) {
  .hero-visual {
    height: 300px;
  }
  
  .orbital-ring.option-1 {
    width: 200px;
    height: 200px;
  }
  
  .orbital-ring.option-2 {
    width: 350px;
    height: 350px;
  }
}

.orbital-ring {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.1);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.option-1 {
  width: 300px;
  height: 300px;
  border-color: rgba(99, 102, 241, 0.3);
  box-shadow: 0 0 50px rgba(99, 102, 241, 0.1);
}

.option-2 {
  width: 500px;
  height: 500px;
  border-style: dashed;
}

.floating-card {
  position: absolute;
  background: rgba(17, 24, 39, 0.8);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 16px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.floating-card:nth-child(3) {
  top: 100px;
  left: 0;
  animation: float 6s ease-in-out infinite;
}

.floating-card:nth-child(4) {
  bottom: 100px;
  right: 0;
  animation: float 6s ease-in-out infinite reverse;
}

.card-icon {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #a855f7;
}

.card-text span {
  display: block;
  font-size: 12px;
  color: #9ca3af;
}

.card-text strong {
  display: block;
  font-size: 14px;
  color: white;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

/* Features */
.features-section {
  padding: 100px 48px;
  background: #0f172a;
}

.section-header {
  text-align: center;
  margin-bottom: 64px;
}

.section-header h2 {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 16px;
}

.section-header p {
  color: #9ca3af;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 32px;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 32px;
  border-radius: 24px;
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.05);
}

.feature-icon {
  width: 40px;
  height: 40px;
  color: #818cf8;
  margin-bottom: 24px;
}

.feature-card h3 {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 12px;
}

.feature-card p {
  color: #9ca3af;
  line-height: 1.6;
}

/* Footer */
.landing-footer {
  padding: 64px 48px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
}

.footer-logo {
  font-weight: 700;
  font-size: 18px;
}

.copyright {
  color: #6b7280;
  font-size: 14px;
}
</style>
