<template>
  <div class="portal-page">
    <div class="page-header">
      <h1 :style="{ color: colors.primary }">{{ tLoc(pageTitle) }}</h1>
      <p class="subtitle">{{ tLoc(pageSubtitle) }}</p>
    </div>

    <!-- Stats Row -->
    <div class="stats-row" v-if="!loading">
      <div
        class="stat-card"
        v-for="stat in sectorStats"
        :key="stat.label"
        :style="{ borderTopColor: colors.primary }"
      >
        <span class="stat-label">{{ tLoc(stat.label) }}</span>
        <span class="stat-value" :style="{ color: colors.primary }">{{ stat.value }}</span>
        <span class="stat-change" :class="stat.change > 0 ? 'up' : 'down'">
          {{ stat.change > 0 ? '+' : '' }}{{ stat.change }}%
        </span>
      </div>
    </div>
    <div class="stats-row" v-else>
      <div class="stat-card skeleton" v-for="i in 4" :key="i"></div>
    </div>

    <!-- Main List -->
    <div class="content-card">
      <div class="card-header-row">
        <h3>{{ tLoc(listTitle) }}</h3>
        <button class="btn-refresh" @click="fetchData" :disabled="loading">
          <RefreshCw :size="14" :class="{ spinning: loading }" />
          {{ tLoc({ tr: 'Yenile', en: 'Refresh', de: 'Aktualisieren' }) }}
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="list-loading">
        <div class="skeleton-row" v-for="i in 5" :key="i"></div>
      </div>

      <!-- Empty State -->
      <div v-else-if="items.length === 0" class="empty-state">
        <component :is="sectorStore.getIcon(pageIcon)" :size="48" :style="{ color: colors.primary, opacity: 0.5 }" />
        <p>{{ tLoc({ tr: 'Henüz kayıt bulunamadı.', en: 'No records found yet.', de: 'Noch keine Einträge gefunden.' }) }}</p>
      </div>

      <!-- Error State -->
      <div v-else-if="fetchError" class="error-state">
        <AlertCircle :size="32" color="#ef4444" />
        <p>{{ tLoc({ tr: 'Veriler yüklenemedi.', en: 'Failed to load data.', de: 'Daten konnten nicht geladen werden.' }) }}</p>
        <button @click="fetchData">{{ tLoc({ tr: 'Tekrar Dene', en: 'Try Again', de: 'Erneut versuchen' }) }}</button>
      </div>

      <!-- Data List -->
      <div v-else class="generic-list">
        <div v-for="(item, i) in items" :key="i" class="list-row">
          <div class="row-icon" :style="{ background: glowColor, color: colors.primary }">
            <component :is="sectorStore.getIcon(pageIcon)" :size="20" />
          </div>
          <div class="row-content">
            <strong>{{ item.title || item.name || item.subject || 'Kayıt' }}</strong>
            <span>{{ item.desc || item.description || item.summary || '' }}</span>
          </div>
          <div class="row-badge" :class="statusClass(item.status)">
            {{ tLoc(statusLabel(item.status)) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch, onMounted } from 'vue'
import { RefreshCw, AlertCircle } from 'lucide-vue-next'
import { useSectorStore } from '../../stores/sector'
import api from '@/config/api'

const sectorStore = useSectorStore()

const tLoc = sectorStore.tLoc

const colors = computed(() => sectorStore.theme || {
  primary: '#0ea5e9',
  secondary: '#0f766e',
  accent: '#38bdf8',
})

const glowColor = computed(() => (colors.value.primary || '#0ea5e9') + '1A')

// ── Sector Config ──────────────────────────────────────────────────────────
const sectorConfigs = {
  medical:       { title: { tr: 'Tıbbi Raporlar', en: 'Medical Reports', de: 'Medizinische Berichte' }, subtitle: { tr: 'Lab ve Görüntüleme Sonuçları', en: 'Lab & Imaging Results', de: 'Labor- & Bildgebungsberichte' }, icon: 'FileText', listTitle: { tr: 'Son Tıbbi Kayıtlar', en: 'Recent Medical Records', de: 'Letzte med. Aufzeichnungen' }, endpoint: '/portal/interactions' },
  legal:         { title: { tr: 'Dava Dosyaları', en: 'Case Files', de: 'Fallakten' }, subtitle: { tr: 'Aktif ve Arşivlenmiş Dosyalar', en: 'Active & Archived Cases', de: 'Aktive & archivierte Fälle' }, icon: 'Briefcase', listTitle: { tr: 'Aktif Davalar', en: 'Active Cases', de: 'Aktive Fälle' }, endpoint: '/portal/interactions' },
  real_estate:   { title: { tr: 'Portföy Yönetimi', en: 'Portfolio Mgmt', de: 'Portfolio-Mgmt' }, subtitle: { tr: 'İlan ve Müşteri Kayıtları', en: 'Listings & Clients', de: 'Inserate & Kunden' }, icon: 'Home', listTitle: { tr: 'Son Portföy Hareketleri', en: 'Recent Portfolio Moves', de: 'Letzte Portfolio-Änderungen' }, endpoint: '/portal/interactions' },
  technology:    { title: { tr: 'Sistem Durumu', en: 'System Status', de: 'Systemstatus' }, subtitle: { tr: 'Server Hizmet Raporları', en: 'Server Service Reports', de: 'Server-Serviceberichte' }, icon: 'Server', listTitle: { tr: 'Son Olaylar', en: 'Recent Events', de: 'Letzte Ereignisse' }, endpoint: '/portal/interactions' },
  finance:       { title: { tr: 'Bütçe Raporları', en: 'Budget Reports', de: 'Budgetberichte' }, subtitle: { tr: 'Aylık Gelir/Gider Tabloları', en: 'Monthly Income/Expenses', de: 'Monatl. Einn./Ausg.' }, icon: 'PieChart', listTitle: { tr: 'Son Finansal İşlemler', en: 'Recent Financial Tx', de: 'Letzte Finanztransaktionen' }, endpoint: '/portal/interactions' },
  education:     { title: { tr: 'Ders Programı', en: 'Class Schedule', de: 'Stundenplan' }, subtitle: { tr: 'Haftalık Ders Çizelgesi', en: 'Weekly Class Layout', de: 'Wöchentliche Kursübersicht' }, icon: 'Calendar', listTitle: { tr: 'Aktif Dersler', en: 'Active Classes', de: 'Aktive Klassen' }, endpoint: '/portal/interactions' },
  automotive:    { title: { tr: 'Servis Kayıtları', en: 'Service Records', de: 'Serviceprotokolle' }, subtitle: { tr: 'Araç Servis Takibi', en: 'Vehicle Tracking', de: 'Fahrzeugverfolgung' }, icon: 'Activity', listTitle: { tr: 'Aktif Servis İşlemleri', en: 'Active Services', de: 'Aktive Dienste' }, endpoint: '/portal/interactions' },
  beauty:        { title: { tr: 'Hizmet Kayıtları', en: 'Service Records', de: 'Serviceprotokolle' }, subtitle: { tr: 'Randevu ve Hizmet Takibi', en: 'Appts & Services', de: 'Termine & Dienstl.' }, icon: 'Sparkles', listTitle: { tr: 'Son Randevular', en: 'Recent Appointments', de: 'Letzte Termine' }, endpoint: '/portal/interactions' },
  hospitality:   { title: { tr: 'Rezervasyon Yönetimi', en: 'Reservation Mgmt', de: 'Reservierungs-Mgmt' }, subtitle: { tr: 'Oda ve Misafir Takibi', en: 'Rooms & Guests', de: 'Zimmer & Gäste' }, icon: 'Home', listTitle: { tr: 'Aktif Rezervasyonlar', en: 'Active Reservations', de: 'Aktive Reservierungen' }, endpoint: '/portal/interactions' },
  manufacturing: { title: { tr: 'Üretim Takibi', en: 'Prod Tracking', de: 'Prod-Verfolgung' }, subtitle: { tr: 'Sipariş ve Stok Durumu', en: 'Orders & Inventory', de: 'Bestellungen & Inventar' }, icon: 'Activity', listTitle: { tr: 'Güncel Üretim Emirleri', en: 'Current Work Orders', de: 'Aktuelle Arbeitsaufträge' }, endpoint: '/portal/interactions' },
  retail:        { title: { tr: 'Satış Kayıtları', en: 'Sales Records', de: 'Verkaufsaufz.' }, subtitle: { tr: 'Günlük Satış ve Stok', en: 'Daily Sales & Inv', de: 'Tägl. Verkäufe & Bestand' }, icon: 'TrendingUp', listTitle: { tr: 'Son Satışlar', en: 'Recent Sales', de: 'Letzte Verkäufe' }, endpoint: '/portal/interactions' },
  ecommerce:     { title: { tr: 'Sipariş Yönetimi', en: 'Order Mgmt', de: 'Bestell-Mgmt' }, subtitle: { tr: 'Sipariş ve Kargo Takibi', en: 'Orders & Shipping', de: 'Bestellungen & Versand' }, icon: 'TrendingUp', listTitle: { tr: 'Son Siparişler', en: 'Recent Orders', de: 'Letzte Bestellungen' }, endpoint: '/portal/interactions' },
}

const pageConfig = computed(() => {
  const id = sectorStore.currentSectorId || 'medical'
  return sectorConfigs[id] || sectorConfigs.medical
})

const pageTitle    = computed(() => pageConfig.value.title)
const pageSubtitle = computed(() => pageConfig.value.subtitle)
const pageIcon     = computed(() => pageConfig.value.icon)
const listTitle    = computed(() => pageConfig.value.listTitle)
const endpoint     = computed(() => pageConfig.value.endpoint)

// Sector stats from the theme config
const sectorStats = computed(() => sectorStore.stats || [])

// ── Data ───────────────────────────────────────────────────────────────────
const items      = ref([])
const loading    = ref(false)
const fetchError = ref(false)

const fetchData = async () => {
  loading.value    = true
  fetchError.value = false
  try {
    const res = await api.get(endpoint.value, { params: { limit: 20 } })
    // Normalize various list response shapes
    const raw = Array.isArray(res.data)
      ? res.data
      : (res.data?.items || res.data?.data || res.data?.results || [])
    items.value = raw
  } catch (e) {
    console.error('SectorSpecific fetch error:', e)
    fetchError.value = true
    items.value = []
  } finally {
    loading.value = false
  }
}

// ── Status Helpers ─────────────────────────────────────────────────────────
const STATUS_MAP = {
  CONFIRMED: { label: { tr: 'Onaylandı', en: 'Confirmed', de: 'Bestätigt' },  cls: 'status-confirmed' },
  PENDING:   { label: { tr: 'Beklemede', en: 'Pending', de: 'Ausstehend' },  cls: 'status-pending'   },
  CANCELLED: { label: { tr: 'İptal', en: 'Cancelled', de: 'Abgebrochen' },      cls: 'status-cancelled' },
  COMPLETED: { label: { tr: 'Tamamlandı', en: 'Completed', de: 'Abgeschlossen' }, cls: 'status-completed' },
  ACTIVE:    { label: { tr: 'Aktif', en: 'Active', de: 'Aktiv' },      cls: 'status-confirmed' },
  INACTIVE:  { label: { tr: 'Pasif', en: 'Inactive', de: 'Inaktiv' },      cls: 'status-cancelled' },
}

const statusLabel = (s) => STATUS_MAP[s?.toUpperCase()]?.label || s || '-'
const statusClass = (s) => STATUS_MAP[s?.toUpperCase()]?.cls  || 'status-pending'

// Re-fetch when sector changes
watch(() => sectorStore.currentSectorId, () => fetchData())

onMounted(() => fetchData())
</script>

<style scoped>
.portal-page {
  width: 100%;
  padding: 24px;
  box-sizing: border-box;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 4px;
}

.subtitle {
  color: var(--text-secondary);
  font-size: 14px;
}

/* Stats Row */
.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-top: 3px solid transparent;
  border-radius: 12px;
  padding: 18px 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  transition: transform 0.2s;
}

.stat-card:hover { transform: translateY(-2px); }

.stat-card.skeleton {
  min-height: 90px;
  animation: pulse 1.5s ease-in-out infinite;
  background: var(--surface-hover);
  border-top-color: transparent !important;
}

@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

.stat-label { font-size: 12px; color: var(--text-secondary); }
.stat-value { font-size: 26px; font-weight: 700; }
.stat-change { font-size: 12px; font-weight: 600; }
.stat-change.up   { color: #10b981; }
.stat-change.down { color: #ef4444; }

/* Content Card */
.content-card {
  background: var(--surface-elevated);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
}

.card-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.card-header-row h3 { font-size: 16px; font-weight: 600; }

.btn-refresh {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: var(--surface-hover);
  border: 1px solid var(--border-subtle);
  border-radius: 6px;
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-refresh:hover:not(:disabled) {
  color: var(--text-primary);
  border-color: var(--border-hover);
}

.btn-refresh:disabled { opacity: 0.5; cursor: not-allowed; }

.spinning { animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Skeleton rows */
.list-loading { display: flex; flex-direction: column; gap: 8px; }
.skeleton-row {
  height: 60px;
  border-radius: 8px;
  background: var(--surface-hover);
  animation: pulse 1.5s ease-in-out infinite;
}

/* Empty / Error */
.empty-state, .error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 48px 24px;
  color: var(--text-secondary);
  font-size: 14px;
}

.error-state button {
  padding: 8px 20px;
  background: rgba(239,68,68,0.1);
  border: 1px solid rgba(239,68,68,0.3);
  border-radius: 6px;
  color: #ef4444;
  font-weight: 600;
  cursor: pointer;
}

/* List */
.generic-list { display: flex; flex-direction: column; }

.list-row {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 8px;
  border-bottom: 1px solid var(--border-subtle);
  transition: background 0.15s;
}

.list-row:last-child { border-bottom: none; }
.list-row:hover { background: var(--surface-hover); border-radius: 8px; }

.row-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.row-content { flex: 1; display: flex; flex-direction: column; gap: 2px; }
.row-content strong { font-size: 14px; color: var(--text-primary); }
.row-content span   { font-size: 12px; color: var(--text-secondary); }

/* Status Badges */
.row-badge {
  padding: 4px 10px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
}

.status-confirmed { background: rgba(16,185,129,0.12); color: #10b981; }
.status-pending   { background: rgba(245,158,11,0.12);  color: #f59e0b; }
.status-cancelled { background: rgba(239,68,68,0.12);   color: #ef4444; }
.status-completed { background: rgba(59,130,246,0.12);  color: #3b82f6; }

@media (max-width: 768px) {
  .stats-row { grid-template-columns: repeat(2, 1fr); }
}
</style>
