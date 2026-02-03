<template>
  <div class="settings-layout">
    <div class="header">
      <h2>{{ sectorStore.t('settings') }}</h2>
      <button class="save-btn">Kaydet</button>
    </div>

    <div class="settings-grid">
      <!-- Profile Section -->
      <div class="settings-card">
        <h3>Profil Ayarları</h3>
        <div class="input-group">
          <label>Ad Soyad</label>
          <input type="text" value="Ahmet Yılmaz" />
        </div>
        <div class="input-group">
          <label>Email</label>
          <input type="email" value="medical@nextgent.com" disabled />
        </div>
      </div>

      <!-- Theme Section -->
      <div class="settings-card">
        <h3>Görünüm Ayarları</h3>
        <div class="toggle-group">
          <label>Koyu Mod</label>
          <div class="toggle active"></div>
        </div>
        <div class="toggle-group">
          <label>Yüksek Karşıtlık</label>
          <div class="toggle"></div>
        </div>
      </div>

      <!-- Notifications -->
      <div class="settings-card">
        <h3>Bildirim Ayarları</h3>
        <div class="toggle-group">
          <label>Email Bildirimleri</label>
          <div class="toggle active"></div>
        </div>
        <div class="toggle-group">
          <label>SMS Bildirimleri</label>
          <div class="toggle active"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useSectorStore } from '../stores/sector'
const sectorStore = useSectorStore()
</script>

<style scoped>
.settings-layout {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.save-btn {
  background: var(--current-accent);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.settings-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.settings-card h3 {
  font-size: 16px;
  font-weight: 600;
  border-bottom: 1px solid var(--border-subtle);
  padding-bottom: 8px;
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
  background: var(--surface-hover);
  border: 1px solid var(--border-subtle);
  padding: 10px;
  border-radius: 8px;
  color: var(--text-primary);
}

.toggle-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.toggle {
  width: 40px;
  height: 20px;
  background: var(--surface-hover);
  border-radius: 99px;
  position: relative;
  cursor: pointer;
}

.toggle::after {
  content: '';
  position: absolute;
  left: 2px;
  top: 2px;
  width: 16px;
  height: 16px;
  background: var(--text-muted);
  border-radius: 50%;
  transition: all 0.2s;
}

.toggle.active {
  background: var(--current-accent);
}

.toggle.active::after {
  transform: translateX(20px);
  background: white;
}
</style>
