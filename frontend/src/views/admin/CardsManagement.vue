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
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Check, Edit2, Plus } from 'lucide-vue-next'
import api from '@/config/api'

const cards = ref([])
const loading = ref(true)
const showAddDialog = ref(false)
const selectedCard = ref(null)

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
  console.log('Edit card:', card)
  // Open edit dialog with card data
  showAddDialog.value = true
  selectedCard.value = card
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
}

.subtitle {
  color: var(--text-secondary);
  font-size: 14px;
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
}

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

@media (max-width: 768px) {
  .cards-management {
    padding: 16px;
  }

  .cards-grid {
    grid-template-columns: 1fr;
  }
}
</style>
