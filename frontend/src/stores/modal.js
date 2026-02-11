import { defineStore } from 'pinia'
import { ref, markRaw } from 'vue'

export const useModalStore = defineStore('modal', () => {
    // State
    const modals = ref([])
    let modalIdCounter = 1

    // Actions
    const openModal = (options) => {
        const modal = {
            id: modalIdCounter++,
            type: options.type || 'custom',
            component: options.component ? markRaw(options.component) : null,
            props: options.props || {},
            title: options.title || '',
            message: options.message || '',
            confirmText: options.confirmText || 'Confirm',
            cancelText: options.cancelText || 'Cancel',
            variant: options.variant || 'info',
            size: options.size || 'medium',
            closeOnOverlay: options.closeOnOverlay !== false,
            closeOnEsc: options.closeOnEsc !== false,
            resolve: null,
            reject: null
        }

        // Create a promise for confirm modals
        const promise = new Promise((resolve, reject) => {
            modal.resolve = resolve
            modal.reject = reject
        })

        modals.value.push(modal)

        return {
            id: modal.id,
            promise
        }
    }

    const closeModal = (id, result = null) => {
        const index = modals.value.findIndex(m => m.id === id)
        if (index !== -1) {
            const modal = modals.value[index]
            if (result !== null && modal.resolve) {
                modal.resolve(result)
            } else if (modal.reject) {
                modal.reject(new Error('Modal cancelled'))
            }
            modals.value.splice(index, 1)
        }
    }

    const closeAllModals = () => {
        modals.value.forEach(modal => {
            if (modal.reject) {
                modal.reject(new Error('All modals closed'))
            }
        })
        modals.value = []
    }

    const confirmModal = (id) => {
        const modal = modals.value.find(m => m.id === id)
        if (modal && modal.resolve) {
            modal.resolve(true)
            closeModal(id)
        }
    }

    const cancelModal = (id) => {
        const modal = modals.value.find(m => m.id === id)
        if (modal) {
            if (modal.reject) {
                modal.reject(new Error('Modal cancelled'))
            }
            closeModal(id)
        }
    }

    return {
        // State
        modals,

        // Actions
        openModal,
        closeModal,
        closeAllModals,
        confirmModal,
        cancelModal
    }
})
