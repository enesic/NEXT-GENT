<template>
  <div class="documents-layout">
    <div class="header">
      <h2>{{ sectorStore.t('documents') }}</h2>
      <button class="upload-btn">
        <Upload :size="16" />
        Yeni Belge Yükle
      </button>
    </div>

    <div class="file-grid">
      <div v-for="file in files" :key="file.id" class="file-card">
        <div class="file-icon" :class="file.type">
          <FileText v-if="file.type === 'pdf'" :size="32" />
          <Image v-else-if="file.type === 'img'" :size="32" />
          <File v-else :size="32" />
        </div>
        <div class="file-info">
          <h3>{{ file.name }}</h3>
          <p>{{ file.date }} • {{ file.size }}</p>
        </div>
        <button class="menu-btn">
          <MoreVertical :size="16" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Upload, FileText, Image, File, MoreVertical } from 'lucide-vue-next'
import { useSectorStore } from '../stores/sector'

const sectorStore = useSectorStore()

const files = ref([
  { id: 1, name: 'Sözleşme Taslağı.pdf', type: 'pdf', date: 'Bugün', size: '2.4 MB' },
  { id: 2, name: 'Müşteri Raporu Q3.docx', type: 'doc', date: 'Dün', size: '1.1 MB' },
  { id: 3, name: 'Görsel Materyaller.zip', type: 'zip', date: '2 gün önce', size: '15 MB' },
  { id: 4, name: 'Fatura #1023.pdf', type: 'pdf', date: 'Geçen Hafta', size: '0.5 MB' },
])
</script>

<style scoped>
.documents-layout {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.upload-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--current-accent);
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

.file-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.file-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  position: relative;
  transition: all var(--transition-fast);
}

.file-card:hover {
  transform: translateY(-2px);
  border-color: var(--border-hover);
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.file-icon {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: var(--surface-hover);
  color: var(--text-secondary);
}

.file-icon.pdf { color: #f43f5e; background: rgba(244, 63, 94, 0.1); }
.file-icon.img { color: #3b82f6; background: rgba(59, 130, 246, 0.1); }

.file-info {
  text-align: center;
}

.file-info h3 {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 4px;
  word-break: break-word;
}

.file-info p {
  font-size: 12px;
  color: var(--text-muted);
}

.menu-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
}
</style>
