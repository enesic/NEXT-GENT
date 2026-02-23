<template>
  <div class="settings-layout">
    <div class="header">
      <div class="title-group">
        <h2>{{ sectorStore.t('settings') }}</h2>
        <p class="subtitle">Hesap ve uygulama tercihlerini yönetin</p>
      </div>
      <button class="save-btn">Tümünü Kaydet</button>
    </div>

    <div class="settings-grid">
      <!-- Profile Section -->
      <div class="settings-card" :style="{ animationDelay: '0.1s' }">
        <div class="card-header">
          <User :size="20" />
          <h3>Profil Ayarları</h3>
        </div>
        <div class="card-body">
          <div class="input-group">
            <label>Ad Soyad</label>
            <input type="text" value="Ahmet Yılmaz" placeholder="Adınızı girin" />
          </div>
          <div class="input-group">
            <label>Email Adresi</label>
            <input type="email" value="info@nextgent.co" disabled />
          </div>
          <div class="input-group">
            <label>Telefon</label>
            <input type="tel" value="+90 555 123 4567" />
          </div>
        </div>
      </div>

      <!-- Theme Section -->
      <div class="settings-card" :style="{ animationDelay: '0.2s' }">
        <div class="card-header">
          <Palette :size="20" />
          <h3>Görünüm Ayarları</h3>
        </div>
        <div class="card-body">
          <div class="toggle-group">
            <div class="toggle-info">
              <label>Koyu Mod</label>
              <p>Göz yorgunluğunu azaltan karanlık arayüz</p>
            </div>
            <div class="toggle active"></div>
          </div>
          <div class="toggle-group">
            <div class="toggle-info">
              <label>Yüksek Karşıtlık</label>
              <p>Daha belirgin metin ve bileşenler</p>
            </div>
            <div class="toggle"></div>
          </div>
          <div class="toggle-group">
            <div class="toggle-info">
              <label>Kompakt Görünüm</label>
              <p>Daha fazla veriyi tek ekranda görün</p>
            </div>
            <div class="toggle"></div>
          </div>
        </div>
      </div>

      <!-- Notifications -->
      <div class="settings-card" :style="{ animationDelay: '0.3s' }">
        <div class="card-header">
          <Bell :size="20" />
          <h3>Bildirim Ayarları</h3>
        </div>
        <div class="card-body">
          <div class="toggle-group">
            <div class="toggle-info">
              <label>Email Bildirimleri</label>
              <p>Önemli güncellemeleri e-posta ile al</p>
            </div>
            <div class="toggle active"></div>
          </div>
          <div class="toggle-group">
            <div class="toggle-info">
              <label>SMS Bildirimleri</label>
              <p>Randevu hatırlatmalarını SMS ile al</p>
            </div>
            <div class="toggle active"></div>
          </div>
        </div>
      </div>

      <!-- Security -->
      <div class="settings-card" :style="{ animationDelay: '0.4s' }">
        <div class="card-header">
          <ShieldCheck :size="20" />
          <h3>Güvenlik Ayarları</h3>
        </div>
        <div class="card-body">
          <div class="action-row">
            <div class="action-info">
              <label>İki Faktörlü Doğrulama</label>
              <p>Ekstra güvenlik katmanı ekleyin</p>
            </div>
            <button class="outline-btn">Etkinleştir</button>
          </div>
          <div class="action-row">
            <div class="action-info">
              <label>Şifre Güncelleme</label>
              <p>Son güncelleme: 3 ay önce</p>
            </div>
            <button class="outline-btn">Değiştir</button>
          </div>
          <div class="action-row">
            <div class="action-info">
              <label>Hesap Kurtarma</label>
              <p>Yedek e-posta ve telefon ayarları</p>
            </div>
            <button class="outline-btn">Yapılandır</button>
          </div>
        </div>
      </div>

      <!-- Privacy & Data -->
      <div class="settings-card" :style="{ animationDelay: '0.5s' }">
        <div class="card-header">
          <Eye :size="20" />
          <h3>Gizlilik ve Veri</h3>
        </div>
        <div class="card-body">
          <div class="toggle-group">
            <div class="toggle-info">
              <label>Veri Kişiselleştirme</label>
              <p>Deneyiminizi iyileştirmek için verileri kullan</p>
            </div>
            <div class="toggle active"></div>
          </div>
          <div class="action-row">
            <div class="action-info">
              <label>Verilerimi İndir</label>
              <p>Tüm kişisel verilerinizin bir kopyasını alın</p>
            </div>
            <button class="outline-btn">İndir</button>
          </div>
        </div>
      </div>

      <!-- Storage Management -->
      <div class="settings-card" :style="{ animationDelay: '0.6s' }">
        <div class="card-header">
          <HardDrive :size="20" />
          <h3>Depolama Yönetimi</h3>
        </div>
        <div class="card-body">
          <div class="storage-usage">
            <div class="usage-stats">
              <span>6.5 GB / 10 GB Kullanıldı</span>
              <span class="usage-pct">%65</span>
            </div>
            <div class="usage-bar">
              <div class="bar-fill" style="width: 65%"></div>
            </div>
            <p class="usage-hint">En çok yer kaplayan: PDF Belgeler (%42)</p>
          </div>
          <button class="outline-btn full-width">Plânı Yükselt</button>
        </div>
      </div>

      <!-- Connected Apps -->
      <div class="settings-card" :style="{ animationDelay: '0.7s' }">
        <div class="card-header">
          <Link :size="20" />
          <h3>Bağlı Uygulamalar</h3>
        </div>
        <div class="card-body">
          <div class="app-item">
            <div class="app-icon google">G</div>
            <div class="app-text">
                <label>Google Drive</label>
                <p>Dosyaları otomatik yedekle</p>
            </div>
            <span class="status-badge connected">Bağlı</span>
          </div>
          <div class="app-item">
            <div class="app-icon slack">S</div>
            <div class="app-text">
                <label>Slack</label>
                <p>Bildirimleri kanala gönder</p>
            </div>
            <button class="link-btn">Bağla</button>
          </div>
        </div>
      </div>

      <!-- Billing Overview -->
      <div class="settings-card" :style="{ animationDelay: '0.8s' }">
        <div class="card-header">
          <CreditCard :size="20" />
          <h3>Ödeme ve Faturalandırma</h3>
        </div>
        <div class="card-body">
          <div class="billing-card-preview">
            <div class="card-brand">VISA</div>
            <div class="card-number">**** **** **** 4242</div>
            <div class="card-exp">12/26</div>
          </div>
          <div class="action-row">
            <div class="action-info">
                <label>Mevcut Paket</label>
                <p>Kurumsal Pro Plus</p>
            </div>
            <span class="price-tag">49$/Ay</span>
          </div>
        </div>
      </div>

      <!-- Localization -->
      <div class="settings-card" :style="{ animationDelay: '0.9s' }">
        <div class="card-header">
          <Globe :size="20" />
          <h3>Dil ve Bölge</h3>
        </div>
        <div class="card-body">
          <div class="input-group">
            <label>Arayüz Dili</label>
            <select class="premium-select">
              <option value="tr">Türkçe</option>
              <option value="en">English</option>
              <option value="de">Deutsch</option>
            </select>
          </div>
          <div class="input-group">
            <label>Saat Dilimi</label>
            <select class="premium-select">
              <option value="europe/istanbul">İstanbul (GMT+3)</option>
              <option value="europe/london">London (GMT+0)</option>
              <option value="america/new_york">New York (GMT-5)</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Advanced -->
      <div class="settings-card" :style="{ animationDelay: '0.6s' }">
        <div class="card-header">
          <Cpu :size="20" />
          <h3>Gelişmiş Ayarlar</h3>
        </div>
        <div class="card-body">
          <div class="toggle-group">
            <div class="toggle-info">
              <label>Beta Özellikler</label>
              <p>Yeni özellikleri herkesten önce deneyin</p>
            </div>
            <div class="toggle"></div>
          </div>
          <div class="toggle-group">
            <div class="toggle-info">
              <label>Analitik Paylaşımı</label>
              <p>Hata raporlarını otomatik olarak gönder</p>
            </div>
            <div class="toggle active"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { User, Palette, Bell, ShieldCheck, Globe, Cpu, Eye, HardDrive, Link, CreditCard } from 'lucide-vue-next'
import { useSectorStore } from '../stores/sector'
const sectorStore = useSectorStore()
</script>

<style scoped>
.settings-layout {
  display: flex;
  flex-direction: column;
  gap: 32px;
  color: var(--text-primary);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.title-group h2 {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 4px;
}

.subtitle {
  color: var(--text-secondary);
  font-size: 14px;
}

.save-btn {
  background: var(--current-accent);
  color: white;
  border: none;
  padding: 0 24px;
  height: 44px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 12px var(--current-glow);
}

.save-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px var(--current-glow-strong);
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.settings-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  padding: 0;
  overflow: hidden;
  transition: all 0.3s;
  animation: appear 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
}

.settings-card:hover {
  border-color: var(--current-accent);
  box-shadow: 0 12px 24px -12px var(--current-glow-strong);
}

.card-header {
  padding: 20px 24px;
  background: rgba(255, 255, 255, 0.02);
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--current-accent);
}

.card-header h3 {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: var(--text-primary);
}

.card-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-group label {
  font-size: 12px;
  color: var(--text-muted);
}

.input-group input {
  background: #030303;
  border: 1px solid var(--border-subtle);
  padding: 12px 16px;
  border-radius: 10px;
  color: var(--text-primary);
  transition: all 0.3s;
}

.input-group input:focus {
  outline: none;
  border-color: var(--current-accent);
  box-shadow: 0 0 0 2px var(--current-glow);
}

.input-group input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: var(--surface-hover);
}

.input-group select {
  background: #030303;
  border: 1px solid var(--border-subtle);
  padding: 12px 16px;
  border-radius: 10px;
  color: var(--text-primary);
  transition: all 0.3s;
  cursor: pointer;
}

.input-group select:focus {
  outline: none;
  border-color: var(--current-accent);
  box-shadow: 0 0 0 2px var(--current-glow);
}

.premium-select option {
  background: var(--surface-elevated);
  padding: 10px;
}

.toggle-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.toggle-info label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 2px;
}

.toggle-info p {
  font-size: 12px;
  color: var(--text-muted);
}

.toggle {
  width: 44px;
  height: 24px;
  background: #030303;
  border: 1px solid var(--border-subtle);
  border-radius: 99px;
  position: relative;
  cursor: pointer;
  transition: all 0.3s;
}

.toggle::after {
  content: '';
  position: absolute;
  left: 3px;
  top: 3px;
  width: 16px;
  height: 16px;
  background: var(--text-muted);
  border-radius: 50%;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.toggle.active {
  background: var(--current-accent);
  border-color: var(--current-accent);
}

.toggle.active::after {
  transform: translateX(18px);
  background: white;
}

.action-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.action-info label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 2px;
}

.action-info p {
  font-size: 12px;
  color: var(--text-muted);
}

.outline-btn {
  background: transparent;
  border: 1px solid var(--border-subtle);
  color: var(--text-primary);
  padding: 8px 16px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.outline-btn:hover {
  border-color: var(--current-accent);
  color: var(--current-accent);
  background: var(--current-glow);
}

.outline-btn.full-width {
    width: 100%;
}

/* Storage Usage */
.storage-usage {
    margin-bottom: 8px;
}

.usage-stats {
    display: flex;
    justify-content: space-between;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 10px;
}

.usage-pct {
    color: var(--current-accent);
}

.usage-bar {
    height: 8px;
    background: #030303;
    border-radius: 4px;
    margin-bottom: 8px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    background: var(--current-accent);
    box-shadow: 0 0 10px var(--current-glow);
}

.usage-hint {
    font-size: 11px;
    color: var(--text-muted);
}

/* App Item */
.app-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 12px;
    background: #030303;
    border-radius: 12px;
    border: 1px solid var(--border-subtle);
}

.app-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 18px;
}

.app-icon.google { background: #4285F4; color: white; }
.app-icon.slack { background: #4A154B; color: white; }

.app-text {
    flex: 1;
}

.app-text label {
    display: block;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 2px;
}

.app-text p {
    font-size: 11px;
    color: var(--text-muted);
}

.status-badge.connected {
    font-size: 10px;
    font-weight: 700;
    color: #22c55e;
    background: rgba(34, 197, 94, 0.1);
    padding: 4px 8px;
    border-radius: 6px;
}

.link-btn {
    background: transparent;
    border: none;
    color: var(--current-accent);
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
}

/* Billing Card */
.billing-card-preview {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 12px;
}

.card-brand {
    font-weight: 800;
    font-style: italic;
    font-size: 18px;
    color: white;
}

.card-number {
    font-family: monospace;
    font-size: 18px;
    letter-spacing: 2px;
    color: white;
    opacity: 0.9;
}

.card-exp {
    font-size: 12px;
    color: white;
    opacity: 0.6;
}

.price-tag {
    font-size: 16px;
    font-weight: 700;
    color: var(--current-accent);
}

@keyframes appear {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
