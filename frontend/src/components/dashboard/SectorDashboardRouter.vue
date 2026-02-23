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

// Sektör dashboard bileşenleri (lazy)
const MedicalDashboard = () => import('../../views/sectors/medical/MedicalDashboard.vue')
const LegalDashboard = () => import('../../views/sectors/legal/LegalDashboard.vue')
const BeautyDashboard = () => import('../../views/sectors/beauty/BeautyDashboard.vue')
const HospitalityDashboard = () => import('../../views/sectors/hospitality/HospitalityDashboard.vue')
const RealEstateDashboard = () => import('../../views/sectors/real_estate/RealEstateDashboard.vue')
const ManufacturingDashboard = () => import('../../views/sectors/manufacturing/ManufacturingDashboard.vue')
const EducationDashboard = () => import('../../views/sectors/education/EducationDashboard.vue')
const FinanceDashboard = () => import('../../views/sectors/finance/FinanceDashboard.vue')
const AutomotiveDashboard = () => import('../../views/sectors/automotive/AutomotiveDashboard.vue')
const RetailDashboard = () => import('../../views/sectors/retail/RetailDashboard.vue')
const PortalDashboard = () => import('../../views/portal/PortalDashboard.vue')
const DashboardContent = () => import('./DashboardContent.vue')

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
</style>
