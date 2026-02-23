<template>
  <div class="sector-dashboard-router">
    <Suspense>
      <component
        :is="activeSectorComponent"
        :key="sectorStore.currentSectorId || 'default'"
        @navigate="$emit('navigate', $event)"
      />
      <template #fallback>
        <div class="dashboard-loading">
          <div class="loading-spinner"></div>
          <p>Dashboard yükleniyor...</p>
        </div>
      </template>
    </Suspense>
  </div>
</template>

<script setup>
import { computed, defineAsyncComponent } from 'vue'
import { useSectorStore } from '../../stores/sector'

const createAsyncDashboard = (loader) =>
  defineAsyncComponent({
    loader,
    delay: 200,
    timeout: 15000
  })

// Sektör dashboard bileşenleri (lazy) — defineAsyncComponent ile Promise doğru işlenir
const MedicalDashboard = createAsyncDashboard(() => import('../../views/sectors/medical/MedicalDashboard.vue'))
const LegalDashboard = createAsyncDashboard(() => import('../../views/sectors/legal/LegalDashboard.vue'))
const BeautyDashboard = createAsyncDashboard(() => import('../../views/sectors/beauty/BeautyDashboard.vue'))
const HospitalityDashboard = createAsyncDashboard(() => import('../../views/sectors/hospitality/HospitalityDashboard.vue'))
const RealEstateDashboard = createAsyncDashboard(() => import('../../views/sectors/real_estate/RealEstateDashboard.vue'))
const ManufacturingDashboard = createAsyncDashboard(() => import('../../views/sectors/manufacturing/ManufacturingDashboard.vue'))
const EducationDashboard = createAsyncDashboard(() => import('../../views/sectors/education/EducationDashboard.vue'))
const FinanceDashboard = createAsyncDashboard(() => import('../../views/sectors/finance/FinanceDashboard.vue'))
const AutomotiveDashboard = createAsyncDashboard(() => import('../../views/sectors/automotive/AutomotiveDashboard.vue'))
const RetailDashboard = createAsyncDashboard(() => import('../../views/sectors/retail/RetailDashboard.vue'))
const PortalDashboard = createAsyncDashboard(() => import('../../views/portal/PortalDashboard.vue'))
const DashboardContent = createAsyncDashboard(() => import('./DashboardContent.vue'))

const sectorStore = useSectorStore()

const sectorComponentMap = {
  medical: MedicalDashboard,
  legal: LegalDashboard,
  beauty: BeautyDashboard,
  hospitality: HospitalityDashboard,
  real_estate: RealEstateDashboard,
  manufacturing: ManufacturingDashboard,
  education: EducationDashboard,
  finance: FinanceDashboard,
  automotive: AutomotiveDashboard,
  retail: RetailDashboard,
  ecommerce: DashboardContent
}

defineEmits(['navigate'])

const activeSectorComponent = computed(() => {
  const sectorId = sectorStore.currentSectorId
  return sectorComponentMap[sectorId] || PortalDashboard
})
</script>

<style scoped>
.sector-dashboard-router {
  width: 100%;
  min-height: 100%;
}

.dashboard-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 16px;
  color: var(--text-secondary);
}

.dashboard-loading p {
  font-size: 14px;
  font-weight: 500;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-subtle);
  border-top-color: var(--current-accent);
  border-radius: 50%;
  animation: sector-spin 0.8s linear infinite;
}

@keyframes sector-spin {
  to { transform: rotate(360deg); }
}
</style>
