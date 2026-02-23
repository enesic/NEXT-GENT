<template>
  <div class="sector-dashboard-router">
    <component
      :is="activeSectorComponent"
      :key="sectorStore.currentSectorId || 'default'"
      @navigate="$emit('navigate', $event)"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useSectorStore } from '../../stores/sector'

// Sync import — [object Promise] hatasını önler, Vite chunk'lara ayırır
import MedicalDashboard from '../../views/sectors/medical/MedicalDashboard.vue'
import LegalDashboard from '../../views/sectors/legal/LegalDashboard.vue'
import BeautyDashboard from '../../views/sectors/beauty/BeautyDashboard.vue'
import HospitalityDashboard from '../../views/sectors/hospitality/HospitalityDashboard.vue'
import RealEstateDashboard from '../../views/sectors/real_estate/RealEstateDashboard.vue'
import ManufacturingDashboard from '../../views/sectors/manufacturing/ManufacturingDashboard.vue'
import EducationDashboard from '../../views/sectors/education/EducationDashboard.vue'
import FinanceDashboard from '../../views/sectors/finance/FinanceDashboard.vue'
import AutomotiveDashboard from '../../views/sectors/automotive/AutomotiveDashboard.vue'
import RetailDashboard from '../../views/sectors/retail/RetailDashboard.vue'
import PortalDashboard from '../../views/portal/PortalDashboard.vue'
import DashboardContent from './DashboardContent.vue'

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
