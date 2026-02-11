<template>
  <div class="sector-layout" :data-sector="currentSector">
    <slot />
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { applyTheme } from '../config/sector-themes'

const route = useRoute()

const currentSector = computed(() => {
  return route.meta?.sector || 'default'
})

// Apply theme based on current sector
onMounted(() => {
  applyTheme(currentSector.value)
})

watch(currentSector, (newSector) => {
  applyTheme(newSector)
}, { immediate: true })
</script>

<style scoped>
.sector-layout {
  width: 100%;
  min-height: 100vh;
  transition: all 0.3s ease;
}
</style>
