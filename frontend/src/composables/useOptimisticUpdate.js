import { ref } from 'vue'
import { useNotificationStore } from '../stores/notification'

/**
 * Optimistic Update Composable
 * Performs optimistic UI updates with automatic rollback on error
 * 
 * @returns {Object} Methods for performing optimistic updates
 */
export function useOptimisticUpdate() {
  const notificationStore = useNotificationStore()
  const pendingUpdates = ref(new Map())
  
  /**
   * Perform an optimistic update
   * 
   * @param {String} key - Unique key for this update
   * @param {Function} optimisticFn - Function to update local state immediately
   * @param {Function} apiFn - Async function to call API
   * @param {Function} rollbackFn - Function to rollback if API fails
   * @param {Object} options - Configuration options
   * @param {Boolean} options.showSuccess - Show success notification (default: true)
   * @param {Boolean} options.showError - Show error notification (default: true)
   * @param {String} options.successMessage - Success message (default: 'Update successful')
   * @param {String} options.errorMessage - Error message (default: 'Update failed')
   * @returns {Promise} Promise that resolves with API result
   */
  const performUpdate = async (key, optimisticFn, apiFn, rollbackFn, options = {}) => {
    const {
      showSuccess = true,
      showError = true,
      successMessage = 'Güncelleme başarılı',
      errorMessage = 'Güncelleme başarısız'
    } = options
    
    // Mark as pending
    pendingUpdates.value.set(key, true)
    
    try {
      // Apply optimistic update immediately
      optimisticFn()
      
      // Call API
      const result = await apiFn()
      
      // Show success notification
      if (showSuccess) {
        notificationStore.success(successMessage)
      }
      
      return result
    } catch (error) {
      // Rollback on error
      rollbackFn()
      
      // Show error notification
      if (showError) {
        const errorMsg = error.response?.data?.message || error.message || errorMessage
        notificationStore.error(errorMsg)
      }
      
      // Re-throw error for caller to handle if needed
      throw error
    } finally {
      // Remove pending status
      pendingUpdates.value.delete(key)
    }
  }
  
  /**
   * Check if an update is currently pending
   * 
   * @param {String} key - Update key to check
   * @returns {Boolean} True if update is pending
   */
  const isPending = (key) => {
    return pendingUpdates.value.has(key)
  }
  
  /**
   * Check if any updates are pending
   * 
   * @returns {Boolean} True if any updates are pending
   */
  const hasPending = () => {
    return pendingUpdates.value.size > 0
  }
  
  /**
   * Get all pending update keys
   * 
   * @returns {Array} Array of pending update keys
   */
  const getPendingKeys = () => {
    return Array.from(pendingUpdates.value.keys())
  }
  
  /**
   * Clear all pending updates (use with caution)
   */
  const clearPending = () => {
    pendingUpdates.value.clear()
  }
  
  /**
   * Perform multiple optimistic updates in parallel
   * 
   * @param {Array} updates - Array of update configurations
   * @returns {Promise} Promise that resolves when all updates complete
   */
  const performBatch = async (updates) => {
    const promises = updates.map(update => 
      performUpdate(
        update.key,
        update.optimisticFn,
        update.apiFn,
        update.rollbackFn,
        update.options
      ).catch(err => ({ error: err, key: update.key }))
    )
    
    const results = await Promise.allSettled(promises)
    
    // Check for errors
    const errors = results
      .filter(r => r.status === 'rejected' || r.value?.error)
      .map(r => r.reason || r.value.error)
    
    if (errors.length > 0) {
      throw new Error(`${errors.length} updates failed`)
    }
    
    return results.map(r => r.value)
  }
  
  return {
    performUpdate,
    isPending,
    hasPending,
    getPendingKeys,
    clearPending,
    performBatch,
    pendingUpdates
  }
}

/**
 * Example usage:
 * 
 * const { performUpdate, isPending } = useOptimisticUpdate()
 * const appointments = ref([...])
 * 
 * const cancelAppointment = async (appointmentId) => {
 *   const appointment = appointments.value.find(a => a.id === appointmentId)
 *   const originalStatus = appointment.status
 *   
 *   await performUpdate(
 *     `cancel-${appointmentId}`,
 *     // Optimistic update
 *     () => {
 *       appointment.status = 'CANCELLED'
 *     },
 *     // API call
 *     () => appointmentService.cancel(appointmentId),
 *     // Rollback
 *     () => {
 *       appointment.status = originalStatus
 *     },
 *     {
 *       successMessage: 'Randevu iptal edildi',
 *       errorMessage: 'Randevu iptal edilemedi'
 *     }
 *   )
 * }
 */
