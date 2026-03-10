<template>
  <div class="executions-page">
    <div class="page-header">
      <div class="back-row">
        <button class="btn-back" @click="router.back()">
          <ArrowLeft :size="16" />
          Geri
        </button>
      </div>
      <h1>Akış Çalıştırma Geçmişi</h1>
      <p class="subtitle">Flow ID: <code>{{ flowId }}</code></p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Geçmiş yükleniyor...</p>
    </div>

    <!-- Executions Table -->
    <div v-else-if="executions.length > 0" class="content-card">
      <table class="exec-table">
        <thead>
          <tr>
            <th>Çalıştırma ID</th>
            <th>Başlangıç</th>
            <th>Süre</th>
            <th>Durum</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="exec in executions" :key="exec.id">
            <td><code>{{ exec.id }}</code></td>
            <td>{{ formatDate(exec.started_at) }}</td>
            <td>{{ exec.duration_ms ? `${exec.duration_ms}ms` : '-' }}</td>
            <td>
              <span class="status-badge" :class="exec.status === 'success' ? 'success' : 'failed'">
                {{ exec.status === 'success' ? 'Başarılı' : 'Başarısız' }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <Activity :size="48" />
      <h3>Henüz çalıştırma kaydı yok</h3>
      <p>Bu akış henüz hiç çalıştırılmamış veya geçmiş kaydı bulunamadı.</p>
      <button class="btn-back" @click="router.back()">Ana Sayfaya Dön</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Activity } from 'lucide-vue-next'
import api from '@/config/api'

const route  = useRoute()
const router = useRouter()

const flowId    = route.params.flowId
const executions = ref([])
const loading    = ref(true)

const formatDate = (iso) => {
  if (!iso) return '-'
  return new Date(iso).toLocaleString('tr-TR')
}

onMounted(async () => {
  try {
    const res = await api.get(`/flow/${flowId}/executions`)
    executions.value = Array.isArray(res.data) ? res.data : (res.data?.items || [])
  } catch (e) {
    console.error('Executions yüklenemedi:', e)
    executions.value = []
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.executions-page {
  padding: 24px;
  width: 100%;
  box-sizing: border-box;
}

.page-header { margin-bottom: 28px; }

.back-row { margin-bottom: 16px; }

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: var(--surface-hover);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-back:hover { color: var(--text-primary); border-color: var(--border-hover); }

.page-header h1 { font-size: 28px; font-weight: 700; color: var(--text-primary); margin: 0 0 8px 0; }
.subtitle { font-size: 14px; color: var(--text-secondary); }
.subtitle code { background: var(--surface-hover); padding: 2px 6px; border-radius: 4px; font-size: 12px; }

.content-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  overflow: hidden;
}

.exec-table {
  width: 100%;
  border-collapse: collapse;
}
.exec-table th, .exec-table td {
  padding: 14px 20px;
  text-align: left;
  font-size: 14px;
}
.exec-table th {
  background: var(--surface-hover);
  color: var(--text-secondary);
  font-weight: 600;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid var(--border-subtle);
}
.exec-table td { color: var(--text-primary); border-bottom: 1px solid var(--border-subtle); }
.exec-table tr:last-child td { border-bottom: none; }
.exec-table tr:hover td { background: var(--surface-hover); }
.exec-table code { background: var(--surface-hover); padding: 2px 6px; border-radius: 4px; font-size: 12px; }

.status-badge {
  padding: 4px 10px;
  border-radius: 99px;
  font-size: 12px;
  font-weight: 600;
}
.status-badge.success { background: rgba(16,185,129,0.1); color: #10b981; }
.status-badge.failed  { background: rgba(239,68,68,0.1);  color: #ef4444; }

.loading-state, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 64px 24px;
  text-align: center;
  color: var(--text-secondary);
}

.empty-state svg { opacity: 0.4; }
.empty-state h3 { font-size: 18px; font-weight: 600; color: var(--text-primary); margin: 0; }
.empty-state p  { font-size: 14px; max-width: 400px; margin: 0; }

.spinner {
  width: 36px; height: 36px;
  border: 3px solid var(--border-subtle);
  border-top-color: var(--indigo-primary, #6366f1);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
