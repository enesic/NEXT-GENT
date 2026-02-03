<template>
  <div class="documents-layout">
    <div class="header">
      <h2>{{ sectorStore.t('documents') }}</h2>
      <div>
        <input 
          id="fileInput" 
          type="file" 
          style="display: none" 
          @change="handleFileUpload"
          :disabled="uploading"
        />
        <button class="upload-btn" @click="triggerFileUpload" :disabled="uploading">
          <Upload :size="16" />
          {{ uploading ? 'Yükleniyor...' : 'Yeni Belge Yükle' }}
        </button>
      </div>
    </div>

    <!-- Error message -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="loading-message">
      Belgeler yükleniyor...
    </div>

    <!-- Empty state -->
    <div v-else-if="files.length === 0" class="empty-state">
      <FileText :size="48" />
      <p>Henüz belge yüklenmemiş</p>
    </div>

    <!-- File grid -->
    <div v-else class="file-grid">
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
        <button class="menu-btn" @click="deleteDocument(file.id)" title="Sil">
          <Trash2 :size="16" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Upload, FileText, Image, File, MoreVertical, Download, Trash2 } from 'lucide-vue-next'
import { useSectorStore } from '../stores/sector'
import { axios } from '../plugins/axios'

const sectorStore = useSectorStore()

const files = ref([])
const loading = ref(false)
const uploading = ref(false)
const error = ref(null)

// Fetch documents from API
const fetchDocuments = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await axios.get('/documents')
    files.value = response.data.map(doc => ({
      id: doc.id,
      name: doc.filename,
      type: getFileTypeFromMime(doc.file_type),
      date: formatDate(doc.created_at),
      size: formatFileSize(doc.size),
      file_url: doc.file_url,
      mime_type: doc.file_type
    }))
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
  transition: opacity 0.2s;
}

.upload-btn:hover:not(:disabled) {
  opacity: 0.9;
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
  padding: 48px 24px;
  gap: 16px;
  color: var(--text-muted);
}

.empty-state svg {
  opacity: 0.5;
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
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s;
}

.menu-btn:hover {
  background: rgba(244, 63, 94, 0.1);
  color: #f43f5e;
}
</style>
