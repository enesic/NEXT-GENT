<template>
  <div class="legal-page">
    <div class="legal-container">
      <h1 class="page-title">KVKK Bilgilendirmesi</h1>
      
      <div class="sections-grid">
        <div v-for="(section, index) in sections" :key="index" class="section-card">
          <h2>{{ section.title }}</h2>
          <p>{{ section.desc }}</p>
        </div>
      </div>

      <div class="back-link">
        <router-link to="/" class="btn-back">← Ana Sayfaya Dön</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
const sections = [
  { 
    title: 'Geçici Bellek Mimarısi', 
    desc: 'NextGent, KVKK uyumlu geçici bellek yapısı kullanır. Kullanıcı verileri kalıcı olarak saklanmaz.' 
  },
  { 
    title: 'Silme ve İndirme Hakları', 
    desc: 'Veri sahipleri talepleri halinde verilerini indirebilir veya tamamen sildirebilir.' 
  },
  { 
    title: 'Güvenlik Tedbirleri', 
    desc: 'Şifreli aktarım, IP koruması, güvenlik duvarı ve erişim logları uygulanır.' 
  },
  { 
    title: 'Saklama Politikası', 
    desc: 'Gereksiz veriler otomatik silinir, yalnızca operasyonel süre boyunca tutulur.' 
  },
]
</script>

<style scoped>
.legal-page {
  min-height: 100vh;
  background: #030712;
  padding: 100px 24px 60px;
}

.legal-container {
  max-width: 900px;
  margin: 0 auto;
}

.page-title {
  font-size: 40px;
  font-weight: 700;
  margin-bottom: 48px;
  text-align: center;
  background: linear-gradient(135deg, #818cf8, #c084fc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.sections-grid {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 48px;
}

.section-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 32px;
  transition: all 0.3s ease;
}

.section-card:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(129, 140, 248, 0.3);
  transform: translateY(-2px);
}

.section-card h2 {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #818cf8;
}

.section-card p {
  color: #9ca3af;
  line-height: 1.6;
  font-size: 16px;
}

.back-link {
  text-align: center;
  margin-top: 48px;
}

.btn-back {
  display: inline-block;
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

@media (max-width: 768px) {
  .page-title {
    font-size: 32px;
  }
  
  .section-card {
    padding: 24px;
  }
  
  .section-card h2 {
    font-size: 20px;
  }
}
</style>
