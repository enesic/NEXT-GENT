import { useModalStore } from '../stores/modal'

/**
 * Composable for programmatic modal management
 */
export function useModal() {
  const modalStore = useModalStore()

  /**
   * Open a confirmation modal
   * @param {Object} options - Modal options
   * @returns {Promise<boolean>} - Resolves to true if confirmed, rejects if cancelled
   */
  const confirm = async (options = {}) => {
    const {
      title = 'Confirm Action',
      message = 'Are you sure you want to proceed?',
      confirmText = 'Confirm',
      cancelText = 'Cancel',
      variant = 'info'
    } = options

    const { promise } = modalStore.openModal({
      type: 'confirm',
      title,
      message,
      confirmText,
      cancelText,
      variant
    })

    try {
      return await promise
    } catch (error) {
      return false
    }
  }

  /**
   * Open a custom modal with a component
   * @param {Object} component - Vue component to render
   * @param {Object} props - Props to pass to the component
   * @param {Object} options - Additional modal options
   * @returns {Object} - Object with modal id and promise
   */
  const openCustomModal = (component, props = {}, options = {}) => {
    return modalStore.openModal({
      type: 'custom',
      component,
      props,
      ...options
    })
  }

  /**
   * Open an alert modal (info variant confirm with only OK button)
   * @param {Object} options - Modal options
   * @returns {Promise<boolean>}
   */
  const alert = async (options = {}) => {
    const {
      title = 'Information',
      message = '',
      confirmText = 'OK',
      variant = 'info'
    } = options

    const { promise } = modalStore.openModal({
      type: 'confirm',
      title,
      message,
      confirmText,
      cancelText: '',
      variant,
      closeOnOverlay: true,
      closeOnEsc: true
    })

    try {
      return await promise
    } catch (error) {
      return false
    }
  }

  /**
   * Open a success modal
   * @param {string} message - Success message
   * @param {string} title - Modal title
   * @returns {Promise<boolean>}
   */
  const success = async (message, title = 'Success') => {
    return await alert({
      title,
      message,
      variant: 'success'
    })
  }

  /**
   * Open an error modal
   * @param {string} message - Error message
   * @param {string} title - Modal title
   * @returns {Promise<boolean>}
   */
  const error = async (message, title = 'Error') => {
    return await alert({
      title,
      message,
      variant: 'danger'
    })
  }

  /**
   * Open a warning modal
   * @param {string} message - Warning message
   * @param {string} title - Modal title
   * @returns {Promise<boolean>}
   */
  const warning = async (message, title = 'Warning') => {
    return await alert({
      title,
      message,
      variant: 'warning'
    })
  }

  /**
   * Close a specific modal
   * @param {number} id - Modal id
   * @param {*} result - Result to resolve with
   */
  const closeModal = (id, result = null) => {
    modalStore.closeModal(id, result)
  }

  /**
   * Close all open modals
   */
  const closeAllModals = () => {
    modalStore.closeAllModals()
  }

  return {
    // Methods
    confirm,
    alert,
    success,
    error,
    warning,
    openCustomModal,
    closeModal,
    closeAllModals,
    
    // Store access
    modals: modalStore.modals
  }
}
