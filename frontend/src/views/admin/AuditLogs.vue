<template>
  <div class="audit-logs">
    <div class="page-header">
      <div>
        <h1>Audit Logları</h1>
        <p class="subtitle">Sistem aktivitelerini izleyin (KVKK uyumlu)</p>
      </div>
      <button class="btn-export" @click="exportLogs">
        <Download :size="18" />
        Export CSV
      </button>
    </div>

    <!-- Filters -->
    <div class="filters-bar glass-effect">
      <div class="filter-group">
        <select v-model="filterAction">
          <option value="">Tüm İşlemler</option>
          <option value="CREATE">Oluşturma</option>
          <option value="UPDATE">Güncelleme</option>
          <option value="DELETE">Silme</option>
          <option value="LOGIN">Giriş</option>
          <option value="LOGOUT">Çıkış</option>
          <option value="PASSWORD_CHANGE">Şifre Değişikliği</option>
          <option value="ANONYMIZE">Anonimleştirme</option>
        </select>
        <select v-model="filterResource">
          <option value="">Tüm Kaynaklar</option>
          <option value="customer">Müşteri</option>
          <option value="admin_user">Admin Kullanıcı</option>
          <option value="call">Çağrı</option>
        </select>
      </div>
      <button class="btn-refresh" @click="loadLogs" :disabled="isLoading">
        <RefreshCw :size="18" :class="{ spin: isLoading }" />
      </button>
    </div>

    <!-- Logs Table -->
    <div class="table-container glass-effect">
      <table class="logs-table">
        <thead>
          <tr>
            <th>Zaman</th>
            <th>İşlem</th>
            <th>Kaynak</th>
            <th>Admin</th>
            <th>IP Adresi</th>
            <th>Detaylar</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in logs" :key="log.id">
            <td>
              <div class="timestamp">
                <Clock :size="14" />
                {{ formatDateTime(log.created_at) }}
              </div>
            </td>
            <td>
              <span :class="['action-badge', getActionClass(log.action_type)]">
                <component :is="getActionIcon(log.action_type)" :size="14" />
                {{ log.action_type }}
              </span>
            </td>
            <td>
              <span class="resource-type">{{ log.resource_type }}</span>
            </td>
            <td>
              <span class="admin-id">{{ log.admin_user_id || 'System' }}</span>
            </td>
            <td>
              <span class="ip-address">{{ log.ip_address || '-' }}</span>
            </td>
            <td>
              <button class="details-btn" @click="showDetails(log)">
                <Info :size="14" />
                Detay
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Empty State -->
      <div v-if="logs.length === 0 && !isLoading" class="empty-state">
        <FileText :size="48" />
        <p>Log kaydı bulunamadı</p>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="loading-state">
        <Loader2 :size="32" class="spin" />
        <p>Loglar yükleniyor...</p>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="pagination">
      <button @click="currentPage--" :disabled="currentPage === 1 || isLoading" class="page-btn">
        <ChevronLeft :size="16" />
      </button>
      <span class="page-info">Sayfa {{ currentPage }} / {{ totalPages }}</span>
      <button @click="currentPage++" :disabled="currentPage === totalPages || isLoading" class="page-btn">
        <ChevronRight :size="16" />
      </button>
    </div>

    <!-- Details Modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="selectedLog" class="modal-overlay" @click="selectedLog = null">
          <div class="modal-content glass-effect" @click.stop>
            <div class="modal-header">
              <h2>Log Detayları</h2>
              <button class="close-btn" @click="selectedLog = null">
                <X :size="20" />
              </button>
            </div>
            <div class="log-details">
              <div class="detail-row">
                <label>ID:</label>
                <code>{{ selectedLog.id }}</code>
              </div>
              <div class="detail-row">
                <label>İşlem:</label>
                <span>{{ selectedLog.action_type }}</span>
              </div>
              <div class="detail-row">
                <label>Kaynak Tipi:</label>
                <span>{{ selectedLog.resource_type }}</span>
              </div>
              <div class="detail-row">
                <label>Admin ID:</label>
                <span>{{ selectedLog.admin_user_id || 'System' }}</span>
              </div>
              <div class="detail-row">
                <label>IP Adresi:</label>
                <span>{{ selectedLog.ip_address || '-' }}</span>
              </div>
              <div class="detail-row">
                <label>User Agent:</label>
                <span class="user-agent">{{ selectedLog.user_agent || '-' }}</span>
              </div>
              <div class="detail-row">
                <label>Zaman:</label>
                <span>{{ formatDateTime(selectedLog.created_at) }}</span>
              </div>
              <div v-if="selectedLog.changes" class="changes-section">
                <label>Değişiklikler (KVKK Uyumlu - Maskelenmiş):</label>
                <pre>{{ JSON.stringify(selectedLog.changes, null, 2) }}</pre>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { 
  Download, RefreshCw, Clock, Info, FileText, Loader2, ChevronLeft, ChevronRight, X,
  Plus, Edit, Trash, LogIn, LogOut, Key, UserX
} from 'lucide-vue-next'
import { useAdminStore } from '@/stores/admin'
import api from '@/config/api'

const adminStore = useAdminStore()

// State
const logs = ref([])
const filterAction = ref('')
const filterResource = ref('')
const currentPage = ref(1)
const pageSize = 50
const totalPages = ref(1)
const isLoading = ref(false)
const selectedLog = ref(null)

// Methods
async function loadLogs() {
  isLoading.value = true
  
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize
    }
    
    if (filterAction.value) params.action_type = filterAction.value
    if (filterResource.value) params.resource_type = filterResource.value
    
    const response = await api.get('/admin/logs', {
      params,
      headers: {
        Authorization: `Bearer ${adminStore.accessToken}`
      }
    })
    
    logs.value = response.data.logs
    totalPages.value = Math.ceil(response.data.total / pageSize)
  } catch (error) {
    console.error('Failed to load logs:', error)
    alert('Loglar yüklenemedi')
  } finally {
    isLoading.value = false
  }
}

function formatDateTime(dateString) {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('tr-TR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

function getActionClass(action) {
  const classes = {
    CREATE: 'create',
    UPDATE: 'update',
    DELETE: 'delete',
    LOGIN: 'login',
    LOGOUT: 'logout',
    PASSWORD_CHANGE: 'password',
    ANONYMIZE: 'anonymize'
  }
  return classes[action] || 'default'
}

function getActionIcon(action) {
  const icons = {
    CREATE: Plus,
    UPDATE: Edit,
    DELETE: Trash,
    LOGIN: LogIn,
    LOGOUT: LogOut,
    PASSWORD_CHANGE: Key,
    ANONYMIZE: UserX
  }
  return icons[action] || Info
}

function showDetails(log) {
  selectedLog.value = log
}

function exportLogs() {
  // Convert logs to CSV
  const headers = ['Zaman', 'İşlem', 'Kaynak', 'Admin ID', 'IP Adresi']
  const rows = logs.value.map(log => [
    formatDateTime(log.created_at),
    log.action_type,
    log.resource_type,
    log.admin_user_id || 'System',
    log.ip_address || '-'
  ])
  
  const csv = [
    headers.join(','),
    ...rows.map(row => row.join(','))
  ].join('\n')
  
  // Download
  const blob = new Blob([csv], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `audit_logs_${new Date().toISOString()}.csv`
  a.click()
  URL.revokeObjectURL(url)
}

// Watch filters
watch([filterAction, filterResource], () => {
  currentPage.value = 1
  loadLogs()
})

watch(currentPage, () => {
  loadLogs()
})

onMounted(() => {
  loadLogs()
})
</script>

<style scoped>
.audit-logs {
  padding: 24px;
  width: 100%;
  box-sizing: border-box;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 8px;
}

.subtitle {
  color: var(--text-secondary);
  font-size: 14px;
}

.btn-export {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 12px;
  color: #10b981;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-export:hover {
  background: rgba(16, 185, 129, 0.2);
  transform: translateY(-2px);
}

.filters-bar {
  display: flex;
  justify-content: space-between;
  padding: 16px;
  border-radius: 12px;
  margin-bottom: 24px;
}

.filter-group {
  display: flex;
  gap: 12px;
}

.filter-group select {
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  color: var(--text-primary);
  font-size: 14px;
  cursor: pointer;
}

.btn-refresh {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}

.btn-refresh:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1);
}

.btn-refresh:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.table-container {
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 24px;
  min-height: 400px;
  position: relative;
}

.logs-table {
  width: 100%;
  border-collapse: collapse;
}

.logs-table thead {
  background: rgba(255, 255, 255, 0.03);
}

.logs-table th {
  text-align: left;
  padding: 16px;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.025em;
  border-bottom: 1px solid var(--border-subtle);
}

.logs-table td {
  padding: 16px;
  border-bottom: 1px solid var(--border-subtle);
  font-size: 14px;
}

.logs-table tbody tr {
  transition: background 0.2s;
}

.logs-table tbody tr:hover {
  background: rgba(255, 255, 255, 0.02);
}

.timestamp {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
  font-size: 13px;
}

.action-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
}

.action-badge.create {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.action-badge.update {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

.action-badge.delete {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.action-badge.login {
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
}

.action-badge.logout {
  background: rgba(107, 114, 128, 0.1);
  color: #9ca3af;
}

.action-badge.password {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
}

.action-badge.anonymize {
  background: rgba(168, 85, 247, 0.1);
  color: #a855f7;
}

.resource-type {
  font-family: 'Courier New', monospace;
  font-size: 13px;
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.05);
  padding: 4px 8px;
  border-radius: 6px;
}

.admin-id,
.ip-address {
  font-size: 13px;
  color: var(--text-secondary);
}

.details-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.3);
  border-radius: 8px;
  color: #6366f1;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.details-btn:hover {
  background: rgba(99, 102, 241, 0.2);
}

.empty-state,
.loading-state {
  padding: 80px;
  text-align: center;
  color: var(--text-secondary);
}

.empty-state p,
.loading-state p {
  margin-top: 16px;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.page-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1);
}

.page-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  color: var(--text-secondary);
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  padding: 24px;
}

.modal-content {
  width: 100%;
  max-width: 700px;
  border-radius: 16px;
  padding: 32px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.modal-header h2 {
  font-size: 24px;
  font-weight: 700;
}

.close-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  color: var(--text-secondary);
  cursor: pointer;
}

.log-details {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.detail-row label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
}

.detail-row code,
.detail-row span {
  font-size: 14px;
  color: var(--text-primary);
}

.detail-row code {
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
  font-family: 'Courier New', monospace;
}

.user-agent {
  word-break: break-all;
  font-size: 12px;
  color: var(--text-secondary);
}

.changes-section {
  margin-top: 8px;
}

.changes-section label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  margin-bottom: 8px;
}

.changes-section pre {
  padding: 16px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  font-size: 12px;
  color: var(--text-secondary);
  overflow-x: auto;
  max-height: 300px;
  font-family: 'Courier New', monospace;
}

/* Modal Transition */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-content,
.modal-leave-active .modal-content {
  transition: transform 0.3s;
}

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
  transform: scale(0.9);
}
</style>
