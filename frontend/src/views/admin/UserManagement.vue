<template>
  <div class="user-management">
    <div class="page-header">
      <div>
        <h1>Kullanıcı Yönetimi</h1>
        <p class="subtitle">Sistem kullanıcılarını yönetin ve kullanıcı bilgilerini düzenleyin</p>
      </div>
      <button class="btn-primary" @click="showAddUserModal = true">
        <UserPlus :size="18" />
        Yeni Kullanıcı
      </button>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon users">
          <Users :size="24" />
        </div>
        <div>
          <p class="stat-label">Toplam Kullanıcı</p>
          <h3 class="stat-value">{{ totalUsers }}</h3>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon active">
          <UserCheck :size="24" />
        </div>
        <div>
          <p class="stat-label">Aktif Kullanıcı</p>
          <h3 class="stat-value">{{ activeUsers }}</h3>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon new">
          <UserPlus :size="24" />
        </div>
        <div>
          <p class="stat-label">Bu Ay Yeni</p>
          <h3 class="stat-value">{{ newUsersThisMonth }}</h3>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-bar glass-effect">
      <div class="search-box">
        <Search :size="18" />
        <input v-model="searchQuery" type="text" placeholder="Kullanıcı ara..." />
      </div>
      <div class="filter-group">
        <select v-model="filterSegment">
          <option value="">Tüm Segmentler</option>
          <option value="vip">VIP</option>
          <option value="premium">Premium</option>
          <option value="standard">Standard</option>
        </select>
        <select v-model="filterStatus">
          <option value="">Tüm Durumlar</option>
          <option value="active">Aktif</option>
          <option value="inactive">Pasif</option>
        </select>
      </div>
    </div>

    <!-- Users Table -->
    <div class="table-container glass-effect">
      <table class="users-table">
        <thead>
          <tr>
            <th>Kullanıcı ID</th>
            <th>Ad Soyad</th>
            <th>Email</th>
            <th>Telefon</th>
            <th>Segment</th>
            <th>Durum</th>
            <th>Kayıt Tarihi</th>
            <th>İşlemler</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in paginatedUsers" :key="user.id">
            <td>
              <span class="user-id">{{ user.customer_id }}</span>
            </td>
            <td>
              <div class="user-info">
                <div class="user-avatar">
                  {{ getInitials(user.first_name, user.last_name) }}
                </div>
                <span>{{ user.first_name }} {{ user.last_name }}</span>
              </div>
            </td>
            <td>
              <span class="masked-text">{{ user.email }}</span>
            </td>
            <td>
              <span class="masked-text">{{ user.phone }}</span>
            </td>
            <td>
              <span :class="['badge', `badge-${user.segment}`]">
                {{ getSegmentLabel(user.segment) }}
              </span>
            </td>
            <td>
              <span :class="['status-badge', user.status]">
                {{ user.status === 'active' ? 'Aktif' : 'Pasif' }}
              </span>
            </td>
            <td>{{ formatDate(user.created_at) }}</td>
            <td>
              <div class="action-buttons">
                <button class="action-btn edit" @click="editUser(user)" title="Düzenle">
                  <Edit :size="16" />
                </button>
                <button class="action-btn key" @click="changePIN(user)" title="PIN Değiştir">
                  <Key :size="16" />
                </button>
                <button class="action-btn delete" @click="confirmDelete(user)" title="Sil">
                  <Trash2 :size="16" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Empty State -->
      <div v-if="filteredUsers.length === 0" class="empty-state">
        <UserX :size="48" />
        <p>Kullanıcı bulunamadı</p>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="pagination">
      <button @click="currentPage--" :disabled="currentPage === 1" class="page-btn">
        <ChevronLeft :size="16" />
      </button>
      <span class="page-info">Sayfa {{ currentPage }} / {{ totalPages }}</span>
      <button @click="currentPage++" :disabled="currentPage === totalPages" class="page-btn">
        <ChevronRight :size="16" />
      </button>
    </div>

    <!-- Add/Edit User Modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showAddUserModal || editingUser" class="modal-overlay" @click="closeModals">
          <div class="modal-content glass-effect" @click.stop>
            <div class="modal-header">
              <h2>{{ editingUser ? 'Kullanıcıyı Düzenle' : 'Yeni Kullanıcı Ekle' }}</h2>
              <button class="close-btn" @click="closeModals">
                <X :size="20" />
              </button>
            </div>
            <form @submit.prevent="submitUser" class="user-form">
              <div class="form-row">
                <div class="form-group">
                  <label>Kullanıcı ID *</label>
                  <input v-model="userForm.customer_id" type="text" required :disabled="!!editingUser" />
                </div>
                <div class="form-group">
                  <label>PIN (4 haneli) *</label>
                  <input v-model="userForm.pin" type="text" maxlength="4" pattern="[0-9]{4}" required v-if="!editingUser" />
                  <span v-else class="form-note">PIN değiştirmek için ayrı butonu kullanın</span>
                </div>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label>Ad *</label>
                  <input v-model="userForm.first_name" type="text" required />
                </div>
                <div class="form-group">
                  <label>Soyad *</label>
                  <input v-model="userForm.last_name" type="text" required />
                </div>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label>Email *</label>
                  <input v-model="userForm.email" type="email" required />
                </div>
                <div class="form-group">
                  <label>Telefon *</label>
                  <input v-model="userForm.phone" type="tel" required />
                </div>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label>Segment *</label>
                  <select v-model="userForm.segment" required>
                    <option value="standard">Standard</option>
                    <option value="premium">Premium</option>
                    <option value="vip">VIP</option>
                  </select>
                </div>
                <div class="form-group" v-if="editingUser">
                  <label>Durum</label>
                  <select v-model="userForm.status">
                    <option value="active">Aktif</option>
                    <option value="inactive">Pasif</option>
                  </select>
                </div>
              </div>
              <div class="form-actions">
                <button type="button" class="btn-secondary" @click="closeModals">İptal</button>
                <button type="submit" class="btn-primary" :disabled="isSubmitting">
                  <Loader2 v-if="isSubmitting" :size="16" class="spin" />
                  {{ editingUser ? 'Güncelle' : 'Oluştur' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- PIN Change Modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="changingPINUser" class="modal-overlay" @click="changingPINUser = null">
          <div class="modal-content glass-effect" @click.stop>
            <div class="modal-header">
              <h2>PIN Değiştir</h2>
              <button class="close-btn" @click="changingPINUser = null">
                <X :size="20" />
              </button>
            </div>
            <form @submit.prevent="submitPINChange" class="pin-form">
              <p class="user-name">{{ changingPINUser?.first_name }} {{ changingPINUser?.last_name }}</p>
              <div class="form-group">
                <label>Yeni PIN (4 haneli) *</label>
                <input v-model="pinForm.new_pin" type="text" maxlength="4" pattern="[0-9]{4}" required autofocus />
              </div>
              <div class="form-group">
                <label>PIN Tekrar *</label>
                <input v-model="pinForm.confirm_pin" type="text" maxlength="4" pattern="[0-9]{4}" required />
              </div>
              <div class="form-actions">
                <button type="button" class="btn-secondary" @click="changingPINUser = null">İptal</button>
                <button type="submit" class="btn-primary" :disabled="isSubmitting">
                  <Loader2 v-if="isSubmitting" :size="16" class="spin" />
                  PIN Değiştir
                </button>
              </div>
            </form>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { 
  Users, UserCheck, UserPlus, UserX, Search, Edit, Trash2, Key, 
  ChevronLeft, ChevronRight, X, Loader2 
} from 'lucide-vue-next'
import { useAdminStore } from '@/stores/admin'
import api from '@/config/api'

const adminStore = useAdminStore()

// State
const users = ref([])
const searchQuery = ref('')
const filterSegment = ref('')
const filterStatus = ref('')
const currentPage = ref(1)
const pageSize = 20
const showAddUserModal = ref(false)
const editingUser = ref(null)
const changingPINUser = ref(null)
const isSubmitting = ref(false)

const userForm = ref({
  customer_id: '',
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  segment: 'standard',
  status: 'active',
  pin: ''
})

const pinForm = ref({
  new_pin: '',
  confirm_pin: ''
})

// Computed
const totalUsers = computed(() => users.value.length)
const activeUsers = computed(() => users.value.filter(u => u.status === 'active').length)
const newUsersThisMonth = computed(() => {
  const thisMonth = new Date().getMonth()
  return users.value.filter(u => new Date(u.created_at).getMonth() === thisMonth).length
})

const filteredUsers = computed(() => {
  return users.value.filter(user => {
    const matchesSearch = !searchQuery.value || 
      user.customer_id.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      `${user.first_name} ${user.last_name}`.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesSegment = !filterSegment.value || user.segment === filterSegment.value
    const matchesStatus = !filterStatus.value || user.status === filterStatus.value
    
    return matchesSearch && matchesSegment && matchesStatus
  })
})

const totalPages = computed(() => Math.ceil(filteredUsers.value.length / pageSize))

const paginatedUsers = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredUsers.value.slice(start, start + pageSize)
})

// Methods
async function loadUsers() {
  try {
    const response = await api.get('/admin/users', {
      headers: {
        Authorization: `Bearer ${adminStore.accessToken}`
      }
    })
    users.value = response.data.users
  } catch (error) {
    console.error('Failed to load users:', error)
  }
}

function getInitials(firstName, lastName) {
  return `${firstName?.charAt(0) || ''}${lastName?.charAt(0) || ''}`.toUpperCase()
}

function getSegmentLabel(segment) {
  const labels = {
    vip: 'VIP',
    premium: 'Premium',
    standard: 'Standard'
  }
  return labels[segment] || segment
}

function formatDate(dateString) {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('tr-TR')
}

function editUser(user) {
  editingUser.value = user
  userForm.value = {
    customer_id: user.customer_id,
    first_name: user.first_name,
    last_name: user.last_name,
    email: user.email,
    phone: user.phone,
    segment: user.segment,
    status: user.status
  }
}

function changePIN(user) {
  changingPINUser.value = user
  pinForm.value = { new_pin: '', confirm_pin: '' }
}

function closeModals() {
  showAddUserModal.value = false
  editingUser.value = null
  userForm.value = {
    customer_id: '',
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    segment: 'standard',
    status: 'active',
    pin: ''
  }
}

async function submitUser() {
  isSubmitting.value = true
  
  try {
    if (editingUser.value) {
      // Update user
      await api.patch(`/admin/users/${editingUser.value.id}`, userForm.value, {
        headers: {
          Authorization: `Bearer ${adminStore.accessToken}`
        }
      })
      alert('Kullanıcı başarıyla güncellendi')
    } else {
      // Create user
      await api.post('/admin/users', userForm.value, {
        headers: {
          Authorization: `Bearer ${adminStore.accessToken}`
        }
      })
      alert('Kullanıcı başarıyla oluşturuldu')
    }
    
    closeModals()
    await loadUsers()
  } catch (error) {
    alert(error.response?.data?.detail || 'İşlem başarısız')
  } finally {
    isSubmitting.value = false
  }
}

async function submitPINChange() {
  if (pinForm.value.new_pin !== pinForm.value.confirm_pin) {
    alert('PIN\'ler eşleşmiyor')
    return
  }
  
  isSubmitting.value = true
  
  try {
    await api.post(`/admin/users/${changingPINUser.value.id}/change-pin`, pinForm.value, {
      headers: {
        Authorization: `Bearer ${adminStore.accessToken}`
      }
    })
    alert('PIN başarıyla değiştirildi')
    changingPINUser.value = null
  } catch (error) {
    alert(error.response?.data?.detail || 'PIN değiştirme başarısız')
  } finally {
    isSubmitting.value = false
  }
}

async function confirmDelete(user) {
  if (!confirm(`${user.first_name} ${user.last_name} kullanıcısını silmek istediğinizden emin misiniz? Bu işlem geri alınamaz.`)) {
    return
  }
  
  try {
    await api.delete(`/admin/users/${user.id}`, {
      headers: {
        Authorization: `Bearer ${adminStore.accessToken}`
      }
    })
    alert('Kullanıcı başarıyla silindi')
    await loadUsers()
  } catch (error) {
    alert(error.response?.data?.detail || 'Kullanıcı silme başarısız')
  }
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
.user-management {
  padding: 32px;
  max-width: 1600px;
  margin: 0 auto;
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

.btn-primary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4);
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon.users {
  background: rgba(99, 102, 241, 0.1);
  color: #6366f1;
}

.stat-icon.active {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.stat-icon.new {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
}

.stat-label {
  color: var(--text-secondary);
  font-size: 13px;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
}

/* Filters */
.filters-bar {
  display: flex;
  gap: 16px;
  padding: 16px;
  border-radius: 12px;
  margin-bottom: 24px;
}

.search-box {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
}

.search-box input {
  flex: 1;
  background: transparent;
  border: none;
  color: var(--text-primary);
  font-size: 14px;
  outline: none;
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

/* Table */
.table-container {
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 24px;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table thead {
  background: rgba(255, 255, 255, 0.03);
}

.users-table th {
  text-align: left;
  padding: 16px;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.025em;
  border-bottom: 1px solid var(--border-subtle);
}

.users-table td {
  padding: 16px;
  border-bottom: 1px solid var(--border-subtle);
  font-size: 14px;
}

.users-table tbody tr {
  transition: background 0.2s;
}

.users-table tbody tr:hover {
  background: rgba(255, 255, 255, 0.02);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 12px;
  font-weight: 600;
}

.user-id {
  font-family: 'Courier New', monospace;
  font-size: 13px;
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.05);
  padding: 4px 8px;
  border-radius: 6px;
}

.masked-text {
  color: var(--text-secondary);
  font-size: 13px;
}

.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
}

.badge-vip {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
}

.badge-premium {
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
}

.badge-standard {
  background: rgba(107, 114, 128, 0.1);
  color: #9ca3af;
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.active {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.status-badge.inactive {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.action-btn {
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
  transition: all 0.2s;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.action-btn.edit:hover {
  border-color: #6366f1;
  color: #6366f1;
}

.action-btn.key:hover {
  border-color: #f59e0b;
  color: #f59e0b;
}

.action-btn.delete:hover {
  border-color: #ef4444;
  color: #ef4444;
}

.empty-state {
  padding: 64px;
  text-align: center;
  color: var(--text-secondary);
}

/* Pagination */
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
  max-width: 600px;
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

.user-form,
.pin-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
}

.form-group input,
.form-group select {
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  color: var(--text-primary);
  font-size: 14px;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #6366f1;
}

.form-note {
  font-size: 13px;
  color: var(--text-muted);
  font-style: italic;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 8px;
}

.btn-secondary {
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.pin-form .user-name {
  font-size: 16px;
  font-weight: 600;
  text-align: center;
  padding: 12px;
  background: rgba(99, 102, 241, 0.1);
  border-radius: 10px;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
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
