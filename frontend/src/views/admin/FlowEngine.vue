<template>
  <div class="flow-engine">
    <div class="page-header">
      <div>
        <h1>Flow Engine</h1>
        <p class="subtitle">Otomasyon akışlarını yönetin</p>
      </div>
      <button class="btn-primary" @click="showCreateDialog = true">
        <Plus :size="20" />
        Yeni Akış Oluştur
      </button>
    </div>

    <!-- Flows List -->
    <div class="flows-grid">
      <div 
        v-for="flow in flows" 
        :key="flow.id" 
        class="flow-card"
        :class="{ active: flow.is_active }"
      >
        <div class="flow-header">
          <div class="flow-info">
            <h3>{{ flow.name }}</h3>
            <span class="flow-category" v-if="flow.category">{{ flow.category }}</span>
          </div>
          <div class="flow-status">
            <span class="status-badge" :class="{ active: flow.is_active }">
              {{ flow.is_active ? 'Aktif' : 'Pasif' }}
            </span>
          </div>
        </div>

        <p class="flow-description" v-if="flow.description">{{ flow.description }}</p>

        <!-- Stats -->
        <div class="flow-stats">
          <div class="stat">
            <span class="stat-label">Toplam</span>
            <span class="stat-value">{{ flow.total_executions }}</span>
          </div>
          <div class="stat success">
            <span class="stat-label">Başarılı</span>
            <span class="stat-value">{{ flow.successful_executions }}</span>
          </div>
          <div class="stat failed">
            <span class="stat-label">Başarısız</span>
            <span class="stat-value">{{ flow.failed_executions }}</span>
          </div>
          <div class="stat">
            <span class="stat-label">Başarı Oranı</span>
            <span class="stat-value">{{ flow.success_rate.toFixed(1) }}%</span>
          </div>
        </div>

        <!-- Tags -->
        <div class="flow-tags" v-if="flow.tags && flow.tags.length">
          <span v-for="tag in flow.tags" :key="tag" class="tag">{{ tag }}</span>
        </div>

        <!-- Actions -->
        <div class="flow-actions">
          <button class="btn-action" @click="executeFlow(flow)" :disabled="!flow.is_active">
            <Play :size="16" />
            Çalıştır
          </button>
          <button class="btn-action" @click="editFlow(flow)">
            <Edit2 :size="16" />
            Düzenle
          </button>
          <button class="btn-action" @click="viewExecutions(flow)">
            <Activity :size="16" />
            Geçmiş
          </button>
          <button class="btn-action danger" @click="deleteFlow(flow)">
            <Trash2 :size="16" />
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="!loading && flows.length === 0" class="empty-state">
      <Zap :size="64" />
      <h3>Henüz akış oluşturulmamış</h3>
      <p>Otomasyon akışları oluşturarak iş süreçlerinizi otomatikleştirin</p>
      <button class="btn-primary" @click="showCreateDialog = true">
        <Plus :size="20" />
        İlk Akışı Oluştur
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Akışlar yükleniyor...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Play, Edit2, Activity, Trash2, Zap } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import api from '@/config/api'

const router = useRouter()

const flows = ref([])
const loading = ref(true)
const showCreateDialog = ref(false)
const showEditDialog = ref(false)
const selectedFlow = ref(null)

const loadFlows = async () => {
  try {
    loading.value = true
    const response = await api.get('/flow')
    flows.value = response.data
  } catch (error) {
    console.error('Akışlar yüklenemedi:', error)
  } finally {
    loading.value = false
  }
}

const executeFlow = async (flow) => {
  try {
    await api.post(`/flow/${flow.id}/execute`)
    // Show success notification
    console.log('Flow çalıştırıldı:', flow.name)
  } catch (error) {
    console.error('Flow çalıştırılamadı:', error)
  }
}

const editFlow = (flow) => {
  console.log('Edit flow:', flow)
  // Open edit dialog with flow data
  selectedFlow.value = flow
  showEditDialog.value = true
}

const viewExecutions = (flow) => {
  console.log('View executions:', flow)
  // Navigate to flow execution history page
  router.push({ name: 'FlowExecutions', params: { flowId: flow.id } })
}

const deleteFlow = async (flow) => {
  if (!confirm(`"${flow.name}" akışını silmek istediğinizden emin misiniz?`)) {
    return
  }

  try {
    await api.delete(`/flow/${flow.id}`)
    flows.value = flows.value.filter(f => f.id !== flow.id)
  } catch (error) {
    console.error('Flow silinemedi:', error)
  }
}

onMounted(() => {
  loadFlows()
})
</script>

<style scoped>
.flow-engine {
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
  color: var(--text-primary);
  margin-bottom: 8px;
  letter-spacing: var(--letter-spacing-tight);
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
  background: var(--indigo-primary);
  border: none;
  border-radius: var(--radius-md);
  color: white;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all var(--transition-base);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px var(--indigo-glow-strong);
}

.flows-grid {
  display: grid;
  gap: 24px;
}

.flow-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 24px;
  transition: all var(--transition-base);
}

.flow-card:hover {
  border-color: var(--border-hover);
  background: var(--surface-hover);
}

.flow-card.active {
  border-color: rgba(99, 102, 241, 0.3);
}

.flow-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.flow-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.flow-info h3 {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
}

.flow-category {
  background: var(--surface-hover);
  color: var(--text-secondary);
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.status-badge.active {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.flow-description {
  color: var(--text-secondary);
  font-size: 14px;
  margin-bottom: 16px;
  line-height: 1.6;
}

.flow-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
  padding: 16px;
  background: var(--surface-hover);
  border-radius: var(--radius-md);
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
}

.stat.success .stat-value {
  color: #10b981;
}

.stat.failed .stat-value {
  color: #ef4444;
}

.flow-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.tag {
  background: var(--surface-hover);
  color: var(--text-secondary);
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 12px;
}

.flow-actions {
  display: flex;
  gap: 8px;
  padding-top: 16px;
  border-top: 1px solid var(--border-subtle);
}

.btn-action {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: var(--surface-hover);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-base);
}

.btn-action:hover:not(:disabled) {
  background: var(--surface-elevated);
  border-color: var(--border-hover);
}

.btn-action:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-action.danger {
  color: #ef4444;
}

.btn-action.danger:hover {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.3);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px;
  gap: 16px;
  text-align: center;
}

.empty-state svg {
  color: var(--text-secondary);
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
}

.empty-state p {
  color: var(--text-secondary);
  max-width: 400px;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px;
  gap: 16px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-subtle);
  border-top-color: var(--indigo-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .flow-engine {
    padding: 16px;
  }

  .page-header {
    flex-direction: column;
    gap: 16px;
  }

  .btn-primary {
    width: 100%;
    justify-content: center;
  }

  .flow-actions {
    flex-wrap: wrap;
  }

  .btn-action {
    flex: 1;
    min-width: 100px;
  }
}
</style>
