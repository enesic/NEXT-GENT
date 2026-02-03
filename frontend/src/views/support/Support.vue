<template>
  <div class="support-page">
    <!-- Background Effects -->
    <div class="bg-gradient"></div>
    <div class="bg-overlay"></div>

    <div class="support-container">
      <!-- Header Section -->
      <div class="page-header">
        <div class="icon-wrapper">
          <Headphones :size="32" :stroke-width="2" />
        </div>
        <h1 class="page-title">Destek Merkezi</h1>
        <p class="page-subtitle">7/24 profesyonel destek ekibimiz, sizin için burada. Sorularınız için hızlı çözümler sunuyoruz.</p>
      </div>

      <!-- Support Stats -->
      <div class="stats-grid">
        <div class="stat-card glass-effect">
          <div class="stat-icon">
            <Clock :size="24" />
          </div>
          <div class="stat-content">
            <span class="stat-value">&lt; 2 saat</span>
            <span class="stat-label">Ortalama Yanıt Süresi</span>
          </div>
        </div>

        <div class="stat-card glass-effect">
          <div class="stat-icon">
            <Users :size="24" />
          </div>
          <div class="stat-content">
            <span class="stat-value">98%</span>
            <span class="stat-label">Müşteri Memnuniyeti</span>
          </div>
        </div>

        <div class="stat-card glass-effect">
          <div class="stat-icon">
            <Zap :size="24" />
          </div>
          <div class="stat-content">
            <span class="stat-value">7/24</span>
            <span class="stat-label">Kesintisiz Destek</span>
          </div>
        </div>
      </div>

      <!-- Support Sections -->
      <div class="sections-grid">
        <div
          v-for="(section, index) in sections"
          :key="index"
          class="section-card glass-effect"
        >
          <div class="section-icon">
            <component :is="section.icon" :size="28" :stroke-width="2" />
          </div>
          <h3>{{ section.title }}</h3>
          <p>{{ section.desc }}</p>
          <ul class="feature-list" v-if="section.features">
            <li v-for="(feature, idx) in section.features" :key="idx">
              <CheckCircle2 :size="16" />
              {{ feature }}
            </li>
          </ul>
        </div>
      </div>

      <!-- FAQ Section -->
      <div class="faq-section glass-effect">
        <h2 class="section-title">
          <HelpCircle :size="24" />
          Sıkça Sorulan Sorular
        </h2>
        
        <div class="faq-items">
          <div
            v-for="(faq, index) in faqs"
            :key="index"
            class="faq-item"
            :class="{ active: activeFaq === index }"
            @click="toggleFaq(index)"
          >
            <div class="faq-question">
              <span>{{ faq.question }}</span>
              <ChevronDown :size="20" class="chevron" />
            </div>
            <Transition name="expand">
              <div v-if="activeFaq === index" class="faq-answer">
                {{ faq.answer }}
              </div>
            </Transition>
          </div>
        </div>
      </div>

      <!-- Contact CTA -->
      <div class="contact-cta glass-effect">
        <div class="cta-content">
          <div class="cta-icon">
            <MessageCircle :size="32" />
          </div>
          <div class="cta-text">
            <h3>Hala yardıma mı ihtiyacınız var?</h3>
            <p>Destek ekibimizle doğrudan iletişime geçin, size yardımcı olmaktan mutluluk duyarız.</p>
          </div>
        </div>
        <router-link to="/iletisim" class="btn-contact">
          <Send :size="18" />
          İletişime Geç
        </router-link>
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
import {
  Headphones,
  Clock,
  Users,
  Zap,
  CheckCircle2,
  HelpCircle,
  ChevronDown,
  MessageCircle,
  Send,
  ArrowLeft,
  Shield,
  Bell,
  RefreshCw
} from 'lucide-vue-next'

const activeFaq = ref(null)

const sections = [
  {
    icon: Shield,
    title: 'Destek Kanalları',
    desc: 'E-posta, canlı sohbet ve telefon ile çoklu kanal desteği',
    features: [
      '7/24 öncelikli yanıt',
      'Uzman destek ekibi',
      'Çoklu dil desteği'
    ]
  },
  {
    icon: Bell,
    title: 'Kritik Durumlar',
    desc: 'Acil durumlar için hızlı müdahale ve çözüm',
    features: [
      'Otomatik alarm sistemi',
      'Anında bildirimler',
      'IP kısıtlama kontrolü'
    ]
  },
  {
    icon: RefreshCw,
    title: 'Güncellemeler',
    desc: 'Sistem güncellemeleri ve bakım bilgilendirmeleri',
    features: [
      'Sürüm notları',
      'Bakım pencereleri',
      'Yeni özellik duyuruları'
    ]
  }
]

const faqs = [
  {
    question: 'Destek saatleri nedir?',
    answer: '7/24 kesintisiz destek sağlıyoruz. Hafta içi mesai saatleri içinde daha hızlı yanıt sürelerine sahipsiniz.'
  },
  {
    question: 'Kritik bir sorun yaşarsam ne yapmalıyım?',
    answer: 'Kritik sorunlar için öncelikli destek hattımızı arayabilir veya acil destek formunu kullanabilirsiniz. Ekibimiz 15 dakika içinde size ulaşacaktır.'
  },
  {
    question: 'Sistem güncellemeleri hakkında nasıl bilgi alabilirim?',
    answer: 'Tüm sistem güncellemeleri portal üzerinden duyurulur. Ayrıca e-posta ve SMS ile bildirim alabilirsiniz.'
  },
  {
    question: 'Teknik dokümantasyona nereden ulaşabilirim?',
    answer: 'Tüm teknik dokümantasyon ve API referansları portal içindeki dokümantasyon bölümünde mevcuttur.'
  }
]

const toggleFaq = (index) => {
  activeFaq.value = activeFaq.value === index ? null : index
}
</script>

<style scoped>
.support-page {
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
  right: -50%;
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
    circle at 80% 20%,
    rgba(168, 85, 247, 0.06) 0%,
    transparent 50%
  );
  pointer-events: none;
}

.support-container {
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
  max-width: 650px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 64px;
}

.stat-card {
  padding: 28px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(99, 102, 241, 0.15);
}

.stat-icon {
  width: 56px;
  height: 56px;
  background: rgba(99, 102, 241, 0.15);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #818cf8;
  flex-shrink: 0;
}

.stat-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary);
}

/* Sections Grid */
.sections-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 28px;
  margin-bottom: 64px;
}

.section-card {
  padding: 36px 32px;
  border-radius: 20px;
  transition: all 0.3s;
}

.section-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 40px rgba(99, 102, 241, 0.12);
}

.section-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(139, 92, 246, 0.15));
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #818cf8;
  margin-bottom: 24px;
}

.section-card h3 {
  font-size: 22px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.section-card p {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 20px;
  font-size: 15px;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.feature-list li {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--text-secondary);
  font-size: 14px;
}

.feature-list li svg {
  color: #22c55e;
  flex-shrink: 0;
}

/* FAQ Section */
.faq-section {
  padding: 48px 40px;
  border-radius: 24px;
  margin-bottom: 48px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 28px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 32px;
}

.faq-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.faq-item {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s;
  cursor: pointer;
}

.faq-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(129, 140, 248, 0.3);
}

.faq-item.active {
  border-color: rgba(129, 140, 248, 0.4);
}

.faq-question {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  font-weight: 600;
  color: var(--text-primary);
  user-select: none;
}

.chevron {
  color: var(--text-muted);
  transition: transform 0.3s;
  flex-shrink: 0;
}

.faq-item.active .chevron {
  transform: rotate(180deg);
}

.faq-answer {
  padding: 0 24px 20px;
  color: var(--text-secondary);
  line-height: 1.7;
}

.expand-enter-active, .expand-leave-active {
  transition: all 0.3s ease;
}

.expand-enter-from, .expand-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Contact CTA */
.contact-cta {
  padding: 40px;
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
  border: 1px solid rgba(99, 102, 241, 0.2);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 32px;
  margin-bottom: 48px;
}

.cta-content {
  display: flex;
  align-items: center;
  gap: 24px;
  flex: 1;
}

.cta-icon {
  width: 64px;
  height: 64px;
  background: rgba(99, 102, 241, 0.2);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #818cf8;
  flex-shrink: 0;
}

.cta-text h3 {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.cta-text p {
  color: var(--text-secondary);
  line-height: 1.6;
}

.btn-contact {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 16px 32px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 99px;
  color: white;
  text-decoration: none;
  font-weight: 600;
  font-size: 16px;
  transition: all 0.3s;
  white-space: nowrap;
}

.btn-contact:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(99, 102, 241, 0.4);
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
  .support-page {
    padding: 80px 16px 40px;
  }

  .page-title {
    font-size: 36px;
  }

  .page-subtitle {
    font-size: 16px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .sections-grid {
    grid-template-columns: 1fr;
  }

  .faq-section {
    padding: 32px 24px;
  }

  .contact-cta {
    flex-direction: column;
    text-align: center;
    padding: 32px 24px;
  }

  .cta-content {
    flex-direction: column;
    text-align: center;
  }

  .btn-contact {
    width: 100%;
    justify-content: center;
  }
}
</style>
