import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

/**
 * Loading Store
 * Manages global loading state for HTTP requests
 * Handles concurrent requests properly
 */
export const useLoadingStore = defineStore('loading', () => {
    // State
    const requestCount = ref(0)

    // Getters
    const isLoading = computed(() => requestCount.value > 0)

    // Actions
    const startLoading = () => {
        requestCount.value++
    }

    const stopLoading = () => {
        if (requestCount.value > 0) {
            requestCount.value--
        }
    }

    const resetLoading = () => {
        requestCount.value = 0
    }

    return {
        // State
        requestCount,

        // Getters
        isLoading,

        // Actions
        startLoading,
        stopLoading,
        resetLoading,
    }
})
