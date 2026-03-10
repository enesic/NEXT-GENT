<template>
  <div class="cards-management">
    <div class="page-header">
      <h1>Kart Yönetimi</h1>
      <p class="subtitle">Abonelik seviyelerini yönetin</p>
    </div>

    <div class="cards-grid">
      <div 
        v-for="card in cards" 
        :key="card.id" 
        class="card-item"
        :class="{ popular: card.is_popular }"
        :style="{ '--card-color': card.color_primary || '#6366f1' }"
      >
        <div class="card-badge" v-if="card.is_popular">En Popüler</div>
        
        <div class="card-header">
          <h3>{{ card.display_name }}</h3>
          <span class="tier-badge">Seviye {{ card.tier_level }}</span>
        </div>

        <div class="card-price">
          <span class="amount">₺{{ card.monthly_price.toLocaleString() }}</span>
          <span class="period">/ay</span>
        </div>

        <div class="card-features">
          <div class="feature-item" v-if="card.max_users">
            <Check :size="16" />
            <span>{{ card.max_users }} Kullanıcı</span>
          </div>
          <div class="feature-item" v-if="card.max_calls_per_month">
            <Check :size="16" />
            <span>{{ card.max_calls_per_month.toLocaleString() }} Çağrı/Ay</span>
          </div>
          <div class="feature-item" v-for="(value, key) in card.features" :key="key">
            <Check :size="16" />
            <span>{{ formatFeature(key, value) }}</span>
          </div>
        </div>

        <div class="card-actions">
          <button class="btn-edit" @click="editCard(card)">
            <Edit2 :size="16" />
            Düzenle
          </button>
          <button 
            class="btn-toggle" 
            :class="{ active: card.is_active }"
            @click="toggleCard(card)"
          >
            {{ card.is_active ? 'Aktif' : 'Pasif' }}
          </button>
        </div>
      </div>

      <!-- Add New Card -->
      <div class="card-item add-card" @click="showAddDialog = true">
        <Plus :size="48" />
        <span>Yeni Kart Ekle</span>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Kartlar yükleniyor...</p>
    </div>
  </div>

    <!-- ── Add / Edit Card Dialog ──────────────────────────────────────── -->
    <Teleport to="body">
      <div v-if="showAddDialog" class="modal-backdrop" @click.self="closeDialog">
        <div class="modal-box" @click.stop>
          <div class="modal-header">
            <h2>{{ selectedCard ? 'Kartı Düzenle' : 'Yeni Kart Ekle' }}</h2>
            <button class="modal-close" @click="closeDialog">✕</button>
          </div>
          <form @submit.prevent="saveCard" class="modal-form">
            <div class="form-group">
              <label>Görünüm Adı *</label>
              <input v-model="cardForm.display_name" type="text" placeholder="Örn: Profesyonel" required class="form-input" />
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Aylık Fiyat (₺) *</label>
                <input v-model.number="cardForm.monthly_price" type="number" min="0" step="0.01" placeholder="0.00" required class="form-input" />
              </div>
              <div class="form-group">
                <label>Seviye</label>
                <input v-model.number="cardForm.tier_level" type="number" min="1" max="10" placeholder="1" class="form-input" />
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Maks. Kullanıcı</label>
                <input v-model.number="cardForm.max_users" type="number" min="1" placeholder="5" class="form-input" />
              </div>
              <div class="form-group">
                <label>Maks. Çağrı/Ay</label>
                <input v-model.number="cardForm.max_calls_per_month" type="number" min="0" placeholder="1000" class="form-input" />
              </div>
            </div>
            <div class="form-group">
              <label>Renk (hex)</label>
              <div style="display:flex;gap:10px;align-items:center">
                <input v-model="cardForm.color_primary" type="color" class="color-picker" />
                <input v-model="cardForm.color_primary" type="text" placeholder="#6366f1" class="form-input" />
              </div>
            </div>
            <div class="form-group inline-row">
              <label class="toggle-label">
                <input v-model="cardForm.is_active" type="checkbox" class="toggle-input" />
                <span>Aktif</span>
              </label>
              <label class="toggle-label">
                <input v-model="cardForm.is_popular" type="checkbox" class="toggle-input" />
                <span>Popüler</span>
              </label>
            </div>
            <div class="modal-actions">
              <button type="button" class="btn-cancel" @click="closeDialog">İptal</button>
              <button type="submit" class="btn-save" :disabled="savingCard">
                {{ savingCard ? 'Kaydediliyor...' : (selectedCard ? 'Güncelle' : 'Oluştur') }}
              </button>
            </div>
            <p v-if="cardError" class="form-error">{{ cardError }}</p>
          </form>
        </div>
      </div>
    </Teleport>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Check, Edit2, Plus } from 'lucide-vue-next'
import api from '@/config/api'

const cards = ref([])
const loading = ref(true)
const showAddDialog = ref(false)
const selectedCard = ref(null)
const savingCard = ref(false)
const cardError = ref(null)

const cardForm = ref({
  display_name: '',
  monthly_price: 0,
  tier_level: 1,
  max_users: 5,
  max_calls_per_month: 1000,
  color_primary: '#6366f1',
  is_active: true,
  is_popular: false
})

const resetForm = () => {
  cardForm.value = {
    display_name: '',
    monthly_price: 0,
    tier_level: 1,
    max_users: 5,
    max_calls_per_month: 1000,
    color_primary: '#6366f1',
    is_active: true,
    is_popular: false
  }
  cardError.value = null
  selectedCard.value = null
}

const closeDialog = () => {
  showAddDialog.value = false
  resetForm()
}

const loadCards = async () => {
  try {
    loading.value = true
    const response = await api.get('/admin/cards')
    cards.value = response.data
  } catch (error) {
    console.error('Kartlar yüklenemedi:', error)
  } finally {
    loading.value = false
  }
}

const formatFeature = (key, value) => {
  const featureNames = {
    'ai_features': 'AI Özellikleri',
    'priority_support': 'Öncelikli Destek',
    'custom_branding': 'Özel Marka',
    'api_access': 'API Erişimi',
    'webhook_integrations': 'Webhook Entegrasyonları',
    'advanced_analytics': 'Gelişmiş Analitik'
  }
  
  if (typeof value === 'boolean') {
    return featureNames[key] || key
  }
  return `${featureNames[key] || key}: ${value}`
}

const editCard = (card) => {
  selectedCard.value = card
  cardForm.value = {
    display_name:        card.display_name        || '',
    monthly_price:       card.monthly_price        ?? 0,
    tier_level:          card.tier_level           ?? 1,
    max_users:           card.max_users            ?? 5,
    max_calls_per_month: card.max_calls_per_month  ?? 1000,
    color_primary:       card.color_primary        || '#6366f1',
    is_active:           card.is_active            ?? true,
    is_popular:          card.is_popular           ?? false,
  }
  cardError.value = null
  showAddDialog.value = true
}

const saveCard = async () => {
  savingCard.value = true
  cardError.value = null
  try {
    if (selectedCard.value) {
      // Update existing card
      const res = await api.put(`/admin/cards/${selectedCard.value.id}`, cardForm.value)
      const idx = cards.value.findIndex(c => c.id === selectedCard.value.id)
      if (idx !== -1) cards.value[idx] = { ...cards.value[idx], ...res.data }
    } else {
      // Create new card
      const res = await api.post('/admin/cards', cardForm.value)
      cards.value.push(res.data)
    }
    closeDialog()
  } catch (e) {
    console.error('Kart kaydedilemedi:', e)
    cardError.value = e?.response?.data?.detail || 'Kayıt sırasında hata oluştu.'
  } finally {
    savingCard.value = false
  }
}

const toggleCard = async (card) => {
  try {
    // Call API to toggle card active status
    await api.patch(`/admin/cards/${card.id}/toggle`, {
      is_active: !card.is_active
    })
    
    // Update local state
    card.is_active = !card.is_active
    
    console.log(`Card ${card.name} is now ${card.is_active ? 'active' : 'inactive'}`)
  } catch (error) {
    console.error('Kart durumu değiştirilemedi:', error)
    // Revert on error
    card.is_active = !card.is_active
  }
}

onMounted(() => {
  loadCards()
})
</script>

<style scoped>
.cards-management {
  padding: 24px;
  width: 100%;
  box-sizing: border-box;
}

.page-header {
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
  letter-spacing: var(--letter-spacing-tight);
  animation: appear 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.subtitle {
  color: var(--text-secondary);
  font-size: 14px;
  animation: appear 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  animation-delay: 0.1s;
  opacity: 0;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.card-item {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 32px;
  position: relative;
  transition: all var(--transition-base);
  animation: appear 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
}

.card-item:nth-child(1) { animation-delay: 0.2s; }
.card-item:nth-child(2) { animation-delay: 0.3s; }
.card-item:nth-child(3) { animation-delay: 0.4s; }
.card-item:nth-child(4) { animation-delay: 0.5s; }
.card-item:nth-child(5) { animation-delay: 0.6s; }

.card-item:hover {
  border-color: var(--border-hover);
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
}

.card-item.popular {
  border-color: var(--card-color);
  box-shadow: 0 0 24px rgba(99, 102, 241, 0.2);
}

.card-badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--card-color);
  color: white;
  padding: 4px 16px;
  border-radius: 99px;
  font-size: 12px;
  font-weight: 600;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-header h3 {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
}

.tier-badge {
  background: var(--surface-hover);
  color: var(--text-secondary);
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.card-price {
  margin-bottom: 24px;
}

.card-price .amount {
  font-size: 48px;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: var(--letter-spacing-tight);
}

.card-price .period {
  font-size: 16px;
  color: var(--text-secondary);
  margin-left: 4px;
}

.card-features {
  margin-bottom: 24px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  color: var(--text-secondary);
  font-size: 14px;
}

.feature-item svg {
  color: var(--card-color);
  flex-shrink: 0;
}

.card-actions {
  display: flex;
  gap: 12px;
  padding-top: 24px;
  border-top: 1px solid var(--border-subtle);
}

.btn-edit,
.btn-toggle {
  flex: 1;
  padding: 12px;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all var(--transition-base);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-edit {
  background: var(--surface-hover);
  border: 1px solid var(--border-subtle);
  color: var(--text-primary);
}

.btn-edit:hover {
  background: var(--surface-elevated);
  border-color: var(--border-hover);
}

.btn-toggle {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.btn-toggle.active {
  background: rgba(16, 185, 129, 0.1);
  border-color: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.add-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  cursor: pointer;
  border-style: dashed;
  min-height: 400px;
}

.add-card:hover {
  border-color: var(--indigo-primary);
  background: var(--indigo-glow);
}

.add-card svg {
  color: var(--text-secondary);
}

.add-card span {
  color: var(--text-secondary);
  font-weight: 600;
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

@media (max-width: 768px) {
  .cards-management {
    padding: 16px;
  }

  .cards-grid {
    grid-template-columns: 1fr;
  }
}

/* ── Modal Styles ──────────────────────────────────────────────────── */
.modal-backdrop {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.65);
  backdrop-filter: blur(4px);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000; padding: 16px;
}

.modal-box {
  background: var(--surface-elevated, #1a1a2e);
  border: 1px solid var(--border-subtle, rgba(255,255,255,0.1));
  border-radius: 16px; padding: 32px;
  width: 100%; max-width: 520px;
  box-shadow: 0 24px 60px rgba(0,0,0,0.5);
  animation: slideUp 0.25s cubic-bezier(0.16,1,0.3,1);
  max-height: 90vh; overflow-y: auto;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}

.modal-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 24px;
}
.modal-header h2 { font-size: 20px; font-weight: 700; color: var(--text-primary); margin: 0; }

.modal-close {
  width: 32px; height: 32px; border-radius: 8px;
  background: var(--surface-hover, rgba(255,255,255,0.05));
  border: 1px solid var(--border-subtle); color: var(--text-secondary);
  font-size: 16px; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.2s;
}
.modal-close:hover { background: rgba(239,68,68,0.1); color: #ef4444; }

.modal-form { display: flex; flex-direction: column; gap: 16px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label { font-size: 13px; font-weight: 600; color: var(--text-secondary); }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }

.form-group.inline-row { flex-direction: row; gap: 24px; }
.toggle-label { display: flex; align-items: center; gap: 8px; cursor: pointer; font-size: 14px; color: var(--text-primary); }
.toggle-input { width: 16px; height: 16px; accent-color: var(--indigo-primary, #6366f1); cursor: pointer; }

.color-picker { width: 44px; height: 38px; border-radius: 8px; border: 1px solid var(--border-subtle); cursor: pointer; padding: 2px; background: transparent; }

.form-input {
  background: var(--surface-hover, rgba(255,255,255,0.05));
  border: 1px solid var(--border-subtle); border-radius: 8px;
  padding: 10px 14px; color: var(--text-primary); font-size: 14px;
  transition: border-color 0.2s; width: 100%; box-sizing: border-box;
}
.form-input:focus { outline: none; border-color: var(--indigo-primary, #6366f1); }

.modal-actions { display: flex; gap: 12px; padding-top: 4px; }
.btn-cancel {
  flex: 1; padding: 10px 20px;
  background: var(--surface-hover); border: 1px solid var(--border-subtle);
  border-radius: 8px; color: var(--text-primary); font-weight: 600; font-size: 14px; cursor: pointer; transition: all 0.2s;
}
.btn-save {
  flex: 1; padding: 10px 20px;
  background: var(--indigo-primary, #6366f1); border: none;
  border-radius: 8px; color: white; font-weight: 600; font-size: 14px; cursor: pointer; transition: all 0.2s;
}
.btn-save:hover:not(:disabled) { opacity: 0.9; transform: translateY(-1px); }
.btn-save:disabled { opacity: 0.5; cursor: not-allowed; }
.form-error { color: #ef4444; font-size: 13px; margin: 0; }
</style>
