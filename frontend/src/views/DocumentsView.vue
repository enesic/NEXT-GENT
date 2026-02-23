<template>
  <div class="documents-layout">
    <div class="header">
      <div class="title-group">
        <h2>{{ sectorStore.t('documents') }}</h2>
        <p class="subtitle">{{ files.length }} belge bulundu</p>
      </div>
      <div class="header-actions">
        <div class="search-bar">
          <Search :size="18" />
          <input v-model="searchQuery" placeholder="Belge ara..." />
        </div>
        <button class="upload-btn" @click="triggerFileUpload" :disabled="uploading">
          <Upload :size="16" />
          {{ uploading ? 'Yükleniyor...' : 'Yeni Belge' }}
        </button>
      </div>
    </div>

    <!-- Categories & Folders -->
    <div class="filter-strip">
      <div class="categories-bar">
        <button 
          v-for="cat in categories" 
          :key="cat.id"
          :class="['cat-btn', { active: activeCategory === cat.id }]"
          @click="activeCategory = cat.id"
        >
          {{ cat.label }}
        </button>
      </div>
      <div class="folder-crumbs">
          <span class="crumb active">Root</span>
          <ChevronRight :size="14" />
          <span class="crumb">Projeler</span>
      </div>
    </div>

    <input 
      id="fileInput" 
      type="file" 
      style="display: none" 
      @change="handleFileUpload"
      :disabled="uploading"
    />

    <!-- Error message -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="loading-message">
      Belgeler yükleniyor...
    </div>

    <!-- Empty state -->
    <div v-else-if="filteredFiles.length === 0" class="empty-state">
      <div class="empty-icon-wrap">
        <FileText :size="48" />
      </div>
      <p>Belge bulunamadı</p>
      <button v-if="searchQuery || activeCategory !== 'all'" class="clear-btn" @click="clearFilters">
        Filtreleri Temizle
      </button>
    </div>

    <!-- File grid -->
    <div v-else class="file-grid">
      <div 
        v-for="(file, index) in filteredFiles" 
        :key="file.id" 
        class="file-card"
        :style="{ animationDelay: `${index * 0.03}s` }"
      >
        <div class="file-tag" v-if="file.tag" :class="file.tag.id">
            {{ file.tag.label }}
        </div>
        <div class="file-icon" :class="file.type">
          <FileText v-if="file.type === 'pdf'" :size="32" />
          <Image v-else-if="file.type === 'img'" :size="32" />
          <FileCode v-else-if="file.type === 'doc'" :size="32" />
          <FileArchive v-else-if="file.type === 'zip'" :size="32" />
          <File v-else :size="32" />
        </div>
        <div class="file-info">
          <h3>{{ file.name }}</h3>
          <div class="file-meta">
            <span>{{ file.date }}</span>
            <span class="dot"></span>
            <span>{{ file.size }}</span>
          </div>
          <div class="file-owner" v-if="file.owner">
              <User :size="12" />
              {{ file.owner }}
          </div>
        </div>
        <button class="menu-btn" @click="deleteDocument(file.id)" title="Sil">
          <Trash2 :size="16" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue'
import { Upload, FileText, Image, File, Search, Trash2, Download, FileCode, FileArchive, ChevronRight, User, Folder } from 'lucide-vue-next'
import { useSectorStore } from '../stores/sector'

const sectorStore = useSectorStore()
const axios = inject('axios')

const files = ref([])
const loading = ref(false)
const uploading = ref(false)
const error = ref(null)
const searchQuery = ref('')
const activeCategory = ref('all')

const categories = [
  { id: 'all', label: 'Tümü' },
  { id: 'pdf', label: 'PDF' },
  { id: 'img', label: 'Görseller' },
  { id: 'doc', label: 'Dokümanlar' },
  { id: 'zip', label: 'Arşivler' }
]

const filteredFiles = computed(() => {
  return files.value.filter(f => {
    const matchesSearch = f.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCategory = activeCategory.value === 'all' || f.type === activeCategory.value
    return matchesSearch && matchesCategory
  })
})

const clearFilters = () => {
  searchQuery.value = ''
  activeCategory.value = 'all'
}

// Fetch documents from API
const fetchDocuments = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await axios.get('/documents')
    
    // If API returns empty, use rich dummy data for demonstration
    if (!response.data || response.data.length === 0) {
      files.value = [
        { id: 1, name: '2023_Yillik_Vergi_Beyannamesi.pdf', type: 'pdf', date: '15.01.2024', size: '2.4 MB', tag: { id: 'urgent', label: 'Acil' }, owner: 'Mali Müşavir' },
        { id: 2, name: 'Klinik_Analiz_Raporu_Ocak.img', type: 'img', date: '02.02.2024', size: '4.1 MB', tag: { id: 'new', label: 'Yeni' }, owner: 'Dr. Ahmet' },
        { id: 3, name: 'Hizmet_Kullanim_Kilavuzu_v2.doc', type: 'doc', date: '20.12.2023', size: '1.2 MB', owner: 'Sistem' },
        { id: 4, name: 'Sektor_Analiz_Sunumu.pdf', type: 'pdf', date: '10.02.2024', size: '8.5 MB', tag: { id: 'shared', label: 'Paylaşıldı' }, owner: 'Analiz Ekibi' },
        { id: 5, name: 'Sistem_Yedekleme_Loglari.zip', type: 'zip', date: '09.02.2024', size: '124 MB', owner: 'Admin' },
        { id: 6, name: 'Musteri_Memnuniyet_Anketi_Sonuclari.pdf', type: 'pdf', date: '05.02.2024', size: '1.8 MB', owner: 'Destek' },
        { id: 7, name: 'Yeni_Donem_Butce_Plani.doc', type: 'doc', date: '01.02.2024', size: '3.2 MB', tag: { id: 'urgent', label: 'Kritik' }, owner: 'Finans' },
        { id: 8, name: 'Ofis_Yerlesim_Plani_Mimari.img', type: 'img', date: '25.01.2024', size: '12.4 MB', owner: 'Projeler' },
        { id: 9, name: 'Hukuki_Danismanlik_Sozlesmesi.pdf', type: 'pdf', date: '12.01.2024', size: '4.5 MB', tag: { id: 'signed', label: 'İmzalandı' }, owner: 'Hukuk' },
        { id: 10, name: 'Proje_Gelistirme_Yol_Haritasi.doc', type: 'doc', date: '08.02.2024', size: '2.1 MB', owner: 'PMO' },
        { id: 11, name: 'Eski_Arsiv_Kayitlari_2022.zip', type: 'zip', date: '15.12.2022', size: '450 MB', owner: 'Arşiv' },
        { id: 12, name: 'Sektor_Trend_Raporu_Q4.pdf', type: 'pdf', date: '30.12.2023', size: '5.2 MB', owner: 'Strateji' },
        { id: 13, name: 'Kullanici_Deneyimi_Feedback.img', type: 'img', date: '12.02.2024', size: '2.8 MB', tag: { id: 'new', label: 'Yeni' }, owner: 'UX Design' },
        { id: 14, name: 'API_Dokumantasyonu_v3.pdf', type: 'pdf', date: '11.02.2024', size: '6.2 MB', owner: 'Dev Team' },
        { id: 15, name: 'Girisim_Sermayesi_Sunumu.pdf', type: 'pdf', date: '10.02.2024', size: '14.1 MB', tag: { id: 'shared', label: 'Yatırımcı' }, owner: 'CEO' },
        { id: 16, name: 'Marketing_Asset_Library.zip', type: 'zip', date: '09.02.2024', size: '89 MB', owner: 'Pazarlama' },
        { id: 17, name: 'Personel_Egitim_Portali_Syllabus.doc', type: 'doc', date: '08.02.2024', size: '1.5 MB', owner: 'HR' },
        { id: 18, name: 'Sunucu_Performans_Grafikleri.img', type: 'img', date: '07.02.2024', size: '5.5 MB', owner: 'SRE' },
        { id: 19, name: 'Musteri_Sikayetleri_Raporu.pdf', type: 'pdf', date: '06.02.2024', size: '3.1 MB', tag: { id: 'urgent', label: 'Acil' }, owner: 'QM' },
        { id: 20, name: 'Yeni_Urun_Tanitim_Videosu_Script.doc', type: 'doc', date: '05.02.2024', size: '0.8 MB', owner: 'İçerik' }
      ]
    } else {
      files.value = response.data.map(doc => ({
        id: doc.id,
        name: doc.filename,
        type: getFileTypeFromMime(doc.file_type),
        date: formatDate(doc.created_at),
        size: formatFileSize(doc.size),
        file_url: doc.file_url,
        mime_type: doc.file_type
      }))
    }
  } catch (err) {
    console.error('Error fetching documents:', err)
    error.value = 'Belgeler yüklenirken bir hata oluştu'
  } finally {
    loading.value = false
  }
}

// Handle file upload
const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  uploading.value = true
  error.value = null

  try {
    const formData = new FormData()
    formData.append('file', file)

    const response = await axios.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    // Refresh the documents list
    await fetchDocuments()
    
    // Reset file input
    event.target.value = ''
  } catch (err) {
    console.error('Error uploading file:', err)
    error.value = err.response?.data?.detail || 'Dosya yüklenirken bir hata oluştu'
  } finally {
    uploading.value = false
  }
}

// Handle file deletion
const deleteDocument = async (documentId) => {
  if (!confirm('Bu belgeyi silmek istediğinizden emin misiniz?')) {
    return
  }

  try {
    await axios.delete(`/documents/${documentId}`)
    await fetchDocuments()
  } catch (err) {
    console.error('Error deleting document:', err)
    error.value = 'Belge silinirken bir hata oluştu'
  }
}

// Helper functions
const getFileTypeFromMime = (mimeType) => {
  if (mimeType.includes('pdf')) return 'pdf'
  if (mimeType.includes('image')) return 'img'
  if (mimeType.includes('word') || mimeType.includes('document')) return 'doc'
  if (mimeType.includes('zip') || mimeType.includes('compressed')) return 'zip'
  return 'file'
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return 'Bugün'
  if (diffDays === 1) return 'Dün'
  if (diffDays < 7) return `${diffDays} gün önce`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} hafta önce`
  return date.toLocaleDateString('tr-TR')
}

// Trigger file input click
const triggerFileUpload = () => {
  document.getElementById('fileInput').click()
}

// Load documents on mount
onMounted(() => {
  fetchDocuments()
})
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
  align-items: flex-start;
  margin-bottom: 32px;
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

.header-actions {
  display: flex;
  gap: 16px;
  align-items: center;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  padding: 0 16px;
  width: 300px;
  height: 44px;
  transition: all 0.3s;
}

.search-bar:focus-within {
  border-color: var(--current-accent);
  box-shadow: 0 0 0 2px var(--current-glow);
}

.search-bar input {
  background: transparent;
  border: none;
  color: var(--text-primary);
  font-size: 14px;
  width: 100%;
}

.search-bar input:focus {
  outline: none;
}

.upload-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--current-accent);
  color: white;
  border: none;
  padding: 0 20px;
  height: 44px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 12px var(--current-glow);
}

.upload-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px var(--current-glow-strong);
}

/* Categories Bar */
.filter-strip {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.categories-bar {
  display: flex;
  gap: 8px;
}

.folder-crumbs {
    display: flex;
    align-items: center;
    gap: 8px;
    background: var(--surface-elevated);
    padding: 8px 16px;
    border-radius: 12px;
    border: 1px solid var(--border-subtle);
    font-size: 13px;
    color: var(--text-muted);
}

.folder-crumbs .crumb.active {
    color: var(--current-accent);
    font-weight: 600;
}

.cat-btn {
  padding: 8px 16px;
  border-radius: 10px;
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.cat-btn:hover {
  border-color: var(--border-hover);
  color: var(--text-primary);
}

.cat-btn.active {
  background: var(--current-accent);
  color: white;
  border-color: var(--current-accent);
}

.upload-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  padding: 12px 16px;
  background: rgba(244, 63, 94, 0.1);
  border: 1px solid #f43f5e;
  border-radius: 8px;
  color: #f43f5e;
  font-size: 14px;
}

.loading-message {
  padding: 24px;
  text-align: center;
  color: var(--text-secondary);
  font-size: 14px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 24px;
  gap: 16px;
  color: var(--text-muted);
}

.empty-icon-wrap {
  width: 100px;
  height: 100px;
  background: var(--surface-elevated);
  border-radius: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
}

.clear-btn {
  background: transparent;
  border: 1px solid var(--border-subtle);
  color: var(--current-accent);
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}

.file-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.file-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: relative;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  animation: appear 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
}

.file-tag {
    position: absolute;
    top: 16px;
    left: 16px;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    z-index: 2;
}

.file-tag.urgent { background: rgba(239, 68, 68, 0.1); color: #ef4444; }
.file-tag.new { background: rgba(34, 197, 94, 0.1); color: #22c55e; }
.file-tag.shared { background: rgba(59, 130, 246, 0.1); color: #3b82f6; }
.file-tag.signed { background: rgba(168, 85, 247, 0.1); color: #a855f7; }

.file-card:hover {
  transform: translateY(-8px);
  border-color: var(--current-accent);
  box-shadow: 0 12px 24px -12px var(--current-glow-strong);
}

.file-icon {
  width: 100%;
  height: 140px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
  background: #030303;
  color: var(--text-secondary);
  transition: all 0.3s;
}

.file-card:hover .file-icon {
  background: var(--surface-hover);
}

.file-icon.pdf { color: #f43f5e; background: rgba(244, 63, 94, 0.1); }
.file-icon.img { color: #3b82f6; background: rgba(59, 130, 246, 0.1); }

.file-info {
  text-align: left;
}

.file-info h3 {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: var(--text-muted);
    margin-bottom: 12px;
}

.file-meta .dot {
    width: 3px;
    height: 3px;
    background: var(--border-subtle);
    border-radius: 50%;
}

.file-owner {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: var(--text-secondary);
    background: #030303;
    padding: 6px 10px;
    border-radius: 8px;
    width: fit-content;
}

.menu-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  color: var(--text-muted);
  cursor: pointer;
  padding: 8px;
  border-radius: 10px;
  transition: all 0.2s;
  opacity: 0;
}

.file-card:hover .menu-btn {
  opacity: 1;
}

.menu-btn:hover {
  background: rgba(244, 63, 94, 0.1);
  color: #f43f5e;
  border-color: #f43f5e;
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
