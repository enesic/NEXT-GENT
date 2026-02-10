<template>
  <div class="landing-container">
    <nav class="landing-nav">
      <div class="logo">
        <div class="logo-icon"></div>
        <span class="logo-text">NextGent</span>
      </div>
      <div class="nav-links">
        <a href="#features">Özellikler</a>
        <a href="#security">Güvenlik</a>
        <a href="#sectors">Sektörler</a>
        <a href="#pricing">Fiyatlandırma</a>
        <a href="#support" class="nav-link">Destek</a>
        <a href="#contact" class="nav-link">İletişim</a>
        <button class="login-btn" @click="$router.push('/login')">Giriş Yap</button>
      </div>
    </nav>

    <header class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          Yeni Nesil <br />
          <span class="gradient-text">AI Operasyon Sistemi</span>
        </h1>
        <p class="hero-subtitle">
          Telefon – WhatsApp – CRM – Otomasyon → Hepsi 7/24 çalışan tek sistemde.
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

    <!-- Sectors Section -->
    <section id="sectors" class="sectors-section">
      <div class="section-header">
        <h2>Sektörel Çözümler</h2>
        <p>Her sektörün ihtiyacına özel, özelleştirilmiş AI asistanları.</p>
      </div>
      <div class="sectors-grid">
        <div class="sector-card medical">
          <div class="sector-icon"><Activity /></div>
          <h3>Sağlık & Klinik</h3>
          <p>Randevu optimizasyonu, hasta takibi ve 7/24 danışmanlık.</p>
        </div>
        <div class="sector-card legal">
          <div class="sector-icon"><Scale /></div>
          <h3>Hukuk & Danışmanlık</h3>
          <p>Müvekkil bilgilendirme, dosya durumu sorgulama ve ön görüşme.</p>
        </div>
        <div class="sector-card property">
          <div class="sector-icon"><Building2 /></div>
          <h3>Gayrimenkul</h3>
          <p>Portföy sunumu, müşteri profilleme ve randevu planlama.</p>
        </div>
      </div>
    </section>

    <!-- Security & KVKK Section -->
    <section id="security" class="security-section">
      <div class="section-header">
        <h2>Güvenlik, Gizlilik ve KVKK</h2>
        <p>KVKK uyumlu, şifreli ve geçici bellek mimarisi ile tasarlanmış.</p>
      </div>
      <div class="security-grid">
        <div class="security-card">
          <h3>Veri Güvenliği</h3>
          <ul>
            <li><span class="bullet">•</span> Şifreli veri aktarımı</li>
            <li><span class="bullet">•</span> IP koruması</li>
            <li><span class="bullet">•</span> Güvenlik duvarı</li>
          </ul>
        </div>
        <div class="security-card">
          <h3>KVKK Uyumlu Saklama</h3>
          <ul>
            <li><span class="bullet">•</span> Veriler geçici hafızada işlenir</li>
            <li><span class="bullet">•</span> Gereksiz veriler otomatik silinir</li>
            <li><span class="bullet">•</span> Veri talep edildiğinde indirilebilir veya tamamen temizlenebilir</li>
          </ul>
        </div>
        <div class="security-card">
          <h3>Mesajların Kalıcı Olmaması</h3>
          <ul>
            <li><span class="bullet">•</span> Model hiçbir konuşmayı kaydetmez</li>
            <li><span class="bullet">•</span> Anlık işlem → anında silme mantığı</li>
          </ul>
        </div>
        <div class="security-card">
          <h3>Token Güvenliği</h3>
          <ul>
            <li><span class="bullet">•</span> İzole token oturumları</li>
            <li><span class="bullet">•</span> Güvenlik loglaması</li>
            <li><span class="bullet">•</span> Yetkisiz erişim engeli</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- Demo Section -->
    <section id="demo" class="demo-section">
      <div class="demo-grid">
        <div class="demo-content">
          <h2>Demo Alın</h2>
          <p class="demo-description">
            Canlı ortamda NextGent deneyimini izleyin. Telefon, WhatsApp ve otomasyon
            akışlarını tek ekrandan görün.
          </p>
          <div class="demo-buttons">
            <a href="mailto:sales@nextgent.co?subject=Demo%20Talebi" class="demo-btn primary">
              Demo Planla
            </a>
            <a href="#teknik-gereksinimler" class="demo-btn secondary">
              Teknik Detay İste
            </a>
          </div>
          <p class="demo-note">
            Demo sırasında verilen bilgiler kayıt altına alınmaz ve kalıcı olarak saklanmaz.
          </p>
        </div>
        <div class="demo-card">
          <h3>Ne Göreceksiniz?</h3>
          <ul class="demo-list">
            <li>• AI telefon operatörü canlı arama senaryosu</li>
            <li>• WhatsApp AI diyalog örnekleri</li>
            <li>• Sekreter onay akışları</li>
            <li>• Otomatik randevu motoru</li>
            <li>• Anlık raporlama paneli</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- Reporting Section -->
    <section class="reporting-section">
      <div class="section-header">
        <h2>Akıllı Otomatik Raporlama Sistemi</h2>
        <p>Günlük konuşmalardan satış dönüşümlerine kadar tüm veriler tek panelde.</p>
      </div>
      <div class="reporting-grid">
        <div class="report-card">
          <h3>Günlük konuşma raporu</h3>
          <p>Her gün tüm kanalların özetini tek ekranda görün.</p>
        </div>
        <div class="report-card">
          <h3>Kaç kişi yazdı?</h3>
          <p>Günlük ve haftalık benzersiz kişi takibi.</p>
        </div>
        <div class="report-card">
          <h3>Kaçı randevu oluşturdu?</h3>
          <p>Otomatik randevu dönüşüm oranlarını izleyin.</p>
        </div>
        <div class="report-card">
          <h3>Kaçı satışa dönüştü?</h3>
          <p>Satışa giden yolculuğu uçtan uca görün.</p>
        </div>
        <div class="report-card">
          <h3>Hangi saatlerde yoğunluk var?</h3>
          <p>Heatmap tarzı yoğunluk görselleştirme.</p>
        </div>
      </div>
    </section>

    <!-- Personas Section -->
    <section class="personas-section">
      <div class="section-header">
        <h2>Persona Analizi ile Gerçek Müşteri Segmentasyonu</h2>
        <p>Farklı persona setleriyle her müşteriye bağlamına uygun deneyim sunun.</p>
      </div>
      <div class="personas-grid">
        <div class="persona-card">
          <h3>Selamcı Persona</h3>
          <p>Hızlı selamlama, bilgi toplama ve yönlendirme odaklı.</p>
        </div>
        <div class="persona-card">
          <h3>Randevu Persona</h3>
          <p>Randevu talebini alır, uygun saatleri sunar, sekretere onaya iletir.</p>
        </div>
        <div class="persona-card">
          <h3>Satın Alma Persona</h3>
          <p>Ürün/hizmet sorularını yanıtlar, satışa yönlendirir, ikna dilini kullanır.</p>
        </div>
        <div class="persona-card">
          <h3>Endişeli Persona</h3>
          <p>Güven verici ton, risk ve gizlilik endişelerini yatıştırır.</p>
        </div>
        <div class="persona-card">
          <h3>VIP Persona</h3>
          <p>Premium dil, hızlı dönüş, öncelikli yönlendirme ve takip.</p>
        </div>
      </div>
    </section>

    <!-- Case Studies Section -->
    <section class="case-studies-section">
      <div class="section-header">
        <h2>Gerçekçi Sektör Case Study'leri</h2>
        <p>Farklı sektörlerde ölçülebilir sonuçlar.</p>
      </div>
      <div class="case-studies-grid">
        <div class="case-card">
          <h3>Estetik Kliniği Case Study</h3>
          <ul class="case-metrics">
            <li><Check :size="16" class="check-icon" /> %73 daha hızlı yanıt</li>
            <li><Check :size="16" class="check-icon" /> %22 daha fazla randevu</li>
            <li><Check :size="16" class="check-icon" /> %41 daha düşük operasyon yükü</li>
          </ul>
        </div>
        <div class="case-card">
          <h3>E-Ticaret Case Study</h3>
          <ul class="case-metrics">
            <li><Check :size="16" class="check-icon" /> 5 kat daha fazla müşteri cevabı</li>
            <li><Check :size="16" class="check-icon" /> %60 daha düşük yoğunluk</li>
            <li><Check :size="16" class="check-icon" /> 2 kat daha yüksek WhatsApp dönüşümü</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section class="how-it-works-section">
      <div class="section-header">
        <h2>Nasıl Çalışır?</h2>
        <p>4 adımda uçtan uca otomasyon ve güvenli onay akışı.</p>
      </div>
      <div class="steps-grid">
        <div class="step-card">
          <div class="step-icon">
            <Activity :size="32" />
          </div>
          <h3>Müşteri → AI</h3>
          <p>Müşteri talebi kanaldan gelir, AI karşılar.</p>
        </div>
        <div class="step-card">
          <div class="step-icon">
            <Cpu :size="32" />
          </div>
          <h3>AI → Sekreter onayı</h3>
          <p>AI taslak oluşturur, sekreter onayına iletir.</p>
        </div>
        <div class="step-card">
          <div class="step-icon">
            <Check :size="32" />
          </div>
          <h3>Onay → CRM'e işlenir</h3>
          <p>Onaylanan kayıt otomatik CRM ve randevu sistemine işler.</p>
        </div>
        <div class="step-card">
          <div class="step-icon">
            <MessageSquare :size="32" />
          </div>
          <h3>Bildirim → Müşteriye gider</h3>
          <p>Sonuç müşteriye bildirilir, geri bildirim kaydedilir.</p>
        </div>
      </div>
    </section>

    <!-- Pricing Section -->
    <section id="pricing" class="pricing-section">
      <div class="section-header">
        <h2>Planlama ve Fiyatlandırma</h2>
        <p>İşletmenizin büyüklüğüne uygun esnek paketler.</p>
      </div>
      <div class="pricing-grid">
        <div class="pricing-card">
          <h3>Başlangıç</h3>
          <div class="price">₺2.999<span>/ay</span></div>
          <ul class="features-list">
            <li><Check :size="16" /> 1 AI Asistan</li>
            <li><Check :size="16" /> 1.000 Dakika Konuşma</li>
            <li><Check :size="16" /> Temel Raporlama</li>
            <li><Check :size="16" /> E-posta Desteği</li>
          </ul>
          <a href="mailto:sales@nextgent.com?subject=Başlangıç Paketi Talebi" class="pricing-btn outline">İletişime Geçin</a>
        </div>
        <div class="pricing-card featured">
          <div class="badge">En Popüler</div>
          <h3>Profesyonel</h3>
          <div class="price">₺5.999<span>/ay</span></div>
          <ul class="features-list">
            <li><Check :size="16" /> 3 AI Asistan</li>
            <li><Check :size="16" /> 5.000 Dakika Konuşma</li>
            <li><Check :size="16" /> Gelişmiş Analitik</li>
            <li><Check :size="16" /> CRM Entegrasyonu</li>
            <li><Check :size="16" /> Öncelikli Destek</li>
          </ul>
          <a href="mailto:sales@nextgent.com?subject=Profesyonel Paket Talebi" class="pricing-btn primary">İletişime Geçin</a>
        </div>
        <div class="pricing-card">
          <h3>Enterprise</h3>
          <div class="price">Özel<span>/teklif</span></div>
          <ul class="features-list">
            <li><Check :size="16" /> Sınırsız Asistan</li>
            <li><Check :size="16" /> Özel Entegrasyonlar</li>
            <li><Check :size="16" /> Dedicated Server</li>
            <li><Check :size="16" /> 7/24 Canlı Destek</li>
          </ul>
          <a href="mailto:sales@nextgent.com?subject=Enterprise Paket Talebi" class="pricing-btn outline">İletişime Geç</a>
        </div>
      </div>
    </section>



    <!-- Support Section -->
    <section id="support" class="spacing-section">
      <LandingSupport />
    </section>

    <!-- Contact Section -->
    <section id="contact">
      <LandingContact />
    </section>

    <footer class="landing-footer">
      <div class="footer-content">
        <div class="footer-section">
          <div class="footer-logo">NextGent</div>
          <p class="footer-description">Yeni nesil AI operasyon sistemi ile işletmenizi geleceğe taşıyın.</p>
        </div>
        
        <div class="footer-section">
          <h4>Ürün</h4>
          <a href="#features">Özellikler</a>
          <a href="#security">Güvenlik</a>
          <a href="#pricing">Fiyatlandırma</a>
          <router-link to="/teknik-gereksinimler">Teknik Gereksinimler</router-link>
        </div>
        
        <div class="footer-section">
          <h4>Şirket</h4>
          <a href="#support">Destek</a>
          <a href="#contact">İletişim</a>
          <router-link to="/kvkk">KVKK</router-link>
          <router-link to="/gizlilik-politikasi">Gizlilik Politikası</router-link>
        </div>
        
        <div class="footer-section">
          <h4>İletişim</h4>
          <a href="mailto:info@nextgent.com">info@nextgent.com</a>
          <a href="mailto:sales@nextgent.com">sales@nextgent.com</a>
          <a href="tel:+905XXXXXXXXX">+90 (5XX) XXX XX XX</a>
        </div>
      </div>
      <div class="footer-bottom">
        <p class="copyright">© 2026 NextGent Technology. Tüm hakları saklıdır.</p>
      </div>
    </footer>

    <!-- AI Helpdesk Chatbot -->
    <HelpdeskChatbot />
  </div>
</template>

<script setup>
import { ArrowRight, ShieldCheck, Zap, Cpu, Activity, MessageSquare, Scale, Building2, Check } from 'lucide-vue-next'
import { onMounted } from 'vue'
import gsap from 'gsap'
import HelpdeskChatbot from '../components/HelpdeskChatbot.vue'
import LandingSupport from '../components/landing/LandingSupport.vue'
import LandingContact from '../components/landing/LandingContact.vue'

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

.nav-links a,
.nav-links .nav-link {
  color: #9ca3af;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.2s;
}

.nav-links a:hover,
.nav-links .nav-link:hover {
  color: #ffffff;
}

.login-btn {
  padding: 10px 24px;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  border: none;
  border-radius: 99px;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(79, 70, 229, 0.5);
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
  
  .nav-links a,
  .nav-links .nav-link {
    display: none;
  }
  
  .nav-links .login-btn {
    display: block; /* Keep login button visible on mobile */
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
  margin-top: 8px;
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

/* Pricing Button Link Styles */
a.pricing-btn {
  display: inline-block;
  text-decoration: none;
  text-align: center;
  padding: 14px 28px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

a.pricing-btn.primary {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: white;
  border: none;
}

a.pricing-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -5px rgba(124, 58, 237, 0.5);
}

a.pricing-btn.outline {
  background: transparent;
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

a.pricing-btn.outline:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
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

.spacing-section {
  margin-bottom: 80px; /* Added separation between Support and Contact */
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

/* Footer Link Styling */
.landing-footer a {
  color: #9ca3af;
  text-decoration: none;
  transition: color 0.2s ease;
  display: block;
  margin-bottom: 8px;
}

.landing-footer a:hover {
  color: #ffffff;
}

.footer-section h4 {
  color: #ffffff;
  margin-bottom: 16px;
}

/* Sectors */
.sectors-section {
  padding: 100px 48px;
  background: #030712;
}

.sectors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 32px;
  max-width: 1200px;
  margin: 0 auto;
}

.sector-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 32px;
  border-radius: 24px;
  text-align: center;
  transition: transform 0.3s;
}

.sector-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.05);
}

.sector-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 24px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.sector-card.medical .sector-icon { background: linear-gradient(135deg, #ef4444, #f87171); box-shadow: 0 10px 30px -10px rgba(239, 68, 68, 0.5); }
.sector-card.legal .sector-icon { background: linear-gradient(135deg, #3b82f6, #60a5fa); box-shadow: 0 10px 30px -10px rgba(59, 130, 246, 0.5); }
.sector-card.property .sector-icon { background: linear-gradient(135deg, #10b981, #34d399); box-shadow: 0 10px 30px -10px rgba(16, 185, 129, 0.5); }

.sector-card h3 { font-size: 20px; font-weight: 700; margin-bottom: 12px; }
.sector-card p { color: #9ca3af; font-size: 15px; }

/* Pricing */
.pricing-section {
  padding: 100px 48px;
  background: #0f172a;
}

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 32px;
  max-width: 1200px;
  margin: 0 auto;
}

.pricing-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 40px;
  border-radius: 24px;
  position: relative;
  display: flex;
  flex-direction: column;
}

.pricing-card.featured {
  background: rgba(79, 70, 229, 0.1);
  border-color: #4f46e5;
  transform: scale(1.05);
}

.badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: #4f46e5;
  color: white;
  padding: 4px 12px;
  border-radius: 99px;
  font-size: 12px;
  font-weight: 600;
}

.price {
  font-size: 48px;
  font-weight: 800;
  margin: 24px 0;
  color: white;
}

.price span { font-size: 16px; color: #9ca3af; font-weight: 500; }

.features-list {
  list-style: none;
  padding: 0;
  margin: 0 0 32px;
  flex: 1;
}

.features-list li {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  color: #d1d5db;
  font-size: 15px;
}

.pricing-btn {
  width: 100%;
  padding: 16px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.pricing-btn.primary {
  background: #4f46e5;
  color: white;
  border: none;
}

.pricing-btn.outline {
  background: transparent;
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.pricing-btn:hover { transform: translateY(-2px); }
.pricing-btn.primary:hover { box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.5); }
.pricing-btn.outline:hover { background: rgba(255, 255, 255, 0.05); }

@media (max-width: 768px) {
  .pricing-card.featured { transform: scale(1); }
   .sectors-section, .pricing-section { padding: 60px 24px; }
}

/* Security Section */
.security-section {
  padding: 100px 48px;
  background: #0f172a;
}

.security-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.security-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 32px;
  transition: all 0.3s ease;
}

.security-card:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(99, 102, 241, 0.3);
  transform: translateY(-4px);
}

.security-card h3 {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #818cf8;
}

.security-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.security-card li {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
  color: #d1d5db;
  line-height: 1.6;
}

.security-card .bullet {
  color: #818cf8;
  font-weight: bold;
  flex-shrink: 0;
}

/* Demo Section */
.demo-section {
  padding: 100px 48px;
  background: #030712;
}

.demo-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  max-width: 1200px;
  margin: 0 auto;
  align-items: center;
}

@media (max-width: 768px) {
  .demo-grid {
    grid-template-columns: 1fr;
    gap: 32px;
  }
}

.demo-content h2 {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 24px;
  background: linear-gradient(135deg, #818cf8, #c084fc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.demo-description {
  color: #9ca3af;
  line-height: 1.6;
  margin-bottom: 32px;
}

.demo-buttons {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.demo-btn {
  padding: 14px 28px;
  border-radius: 99px;
  font-weight: 600;
  font-size: 15px;
  text-decoration: none;
  transition: all 0.2s;
  display: inline-block;
}

.demo-btn.primary {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: white;
  border: none;
}

.demo-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -5px rgba(124, 58, 237, 0.5);
}

.demo-btn.secondary {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
}

.demo-btn.secondary:hover {
  background: rgba(255, 255, 255, 0.05);
}

.demo-note {
  font-size: 13px;
  color: #6b7280;
}

.demo-card {
  background: rgba(17, 24, 39, 0.8);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 32px;
}

.demo-card h3 {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #818cf8;
}

.demo-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.demo-list li {
  color: #d1d5db;
  margin-bottom: 12px;
  line-height: 1.6;
}

/* Reporting Section */
.reporting-section {
  padding: 100px 48px;
  background: #0f172a;
}

.reporting-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.report-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 32px;
  transition: all 0.3s ease;
}

.report-card:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(129, 140, 248, 0.3);
  transform: translateY(-4px);
}

.report-card h3 {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #818cf8;
}

.report-card p {
  color: #9ca3af;
  line-height: 1.6;
}

/* Personas Section */
.personas-section {
  padding: 100px 48px;
  background: #030712;
}

.personas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.persona-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 32px;
  transition: all 0.3s ease;
}

.persona-card:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(168, 85, 247, 0.3);
  transform: translateY(-4px);
}

.persona-card h3 {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #c084fc;
}

.persona-card p {
  color: #9ca3af;
  line-height: 1.6;
}

/* Case Studies Section */
.case-studies-section {
  padding: 100px 48px;
  background: #0f172a;
}

.case-studies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 32px;
  max-width: 1200px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .case-studies-grid {
    grid-template-columns: 1fr;
  }
}

.case-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 40px;
  transition: all 0.3s ease;
}

.case-card:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(129, 140, 248, 0.3);
  transform: translateY(-4px);
}

.case-card h3 {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 24px;
  color: #818cf8;
}

.case-metrics {
  list-style: none;
  padding: 0;
  margin: 0;
}

.case-metrics li {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  color: #d1d5db;
  font-size: 16px;
}

.check-icon {
  color: #10b981;
  flex-shrink: 0;
}

/* How It Works Section */
.how-it-works-section {
  padding: 100px 48px;
  background: #030712;
}

.steps-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.step-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 32px;
  text-align: center;
  transition: all 0.3s ease;
}

.step-card:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(168, 85, 247, 0.3);
  transform: translateY(-4px);
}

.step-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 20px;
  background: rgba(99, 102, 241, 0.1);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #818cf8;
}

.step-card h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 12px;
  color: white;
}

.step-card p {
  color: #9ca3af;
  font-size: 14px;
  line-height: 1.6;
}

/* Responsive adjustments for new sections */
@media (max-width: 768px) {
  .security-section,
  .demo-section,
  .reporting-section,
  .personas-section,
  .case-studies-section,
  .how-it-works-section {
    padding: 60px 24px;
  }
  
  .security-grid,
  .reporting-grid,
  .personas-grid,
  .steps-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}

/* Footer Styles */
.landing-footer {
  background: #000000;
  padding: 80px 48px 40px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 14px;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1.5fr;
  gap: 64px;
  margin-bottom: 64px;
}

.footer-logo {
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(135deg, #fff, #94a3b8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 16px;
}

.footer-description {
  color: #94a3b8;
  line-height: 1.6;
  max-width: 300px;
}

.footer-section h4 {
  color: white;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 24px;
}

.footer-section a {
  display: block;
  color: #94a3b8;
  text-decoration: none;
  margin-bottom: 12px;
  transition: color 0.2s;
}

.footer-section a:hover {
  color: #6366f1;
}

.footer-bottom {
  max-width: 1200px;
  margin: 0 auto;
  padding-top: 32px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  text-align: center;
  color: #64748b;
}

@media (max-width: 1024px) {
  .footer-content {
    grid-template-columns: 1fr 1fr;
    gap: 48px;
  }
}

@media (max-width: 768px) {
  .landing-footer {
    padding: 60px 24px 32px;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
    gap: 40px;
    text-align: center;
  }
  
  .footer-description {
    margin: 0 auto;
  }
}

</style>
