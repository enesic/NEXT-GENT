import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useNotificationStore = defineStore('notification', () => {
    // State
    const notifications = ref([])
    let notificationIdCounter = 1

    // Getters
    const unreadCount = computed(() => {
        return notifications.value.filter(n => !n.read).length
    })

    const unreadNotifications = computed(() => {
        return notifications.value.filter(n => !n.read)
    })

    const readNotifications = computed(() => {
        return notifications.value.filter(n => n.read)
    })

    const notificationsByType = computed(() => (type) => {
        return notifications.value.filter(n => n.type === type)
    })

    // Actions
    const addNotification = (notification) => {
        const newNotification = {
            id: notificationIdCounter++,
            title: notification.title || 'Bildirim',
            message: notification.message || '',
            type: notification.type || 'info', // info, success, warning, error
            read: false,
            timestamp: new Date(),
            ...notification
        }

        notifications.value.unshift(newNotification)

        // Auto-remove after 30 seconds for non-error notifications
        if (notification.type !== 'error' && notification.autoRemove !== false) {
            setTimeout(() => {
                removeNotification(newNotification.id)
            }, 30000)
        }

        return newNotification.id
    }

    const removeNotification = (id) => {
        const index = notifications.value.findIndex(n => n.id === id)
        if (index !== -1) {
            notifications.value.splice(index, 1)
        }
    }

    const markAsRead = (id) => {
        const notification = notifications.value.find(n => n.id === id)
        if (notification) {
            notification.read = true
        }
    }

    const markAllAsRead = () => {
        notifications.value.forEach(n => {
            n.read = true
        })
    }

    const clearAll = () => {
        notifications.value = []
    }

    const clearRead = () => {
        notifications.value = notifications.value.filter(n => !n.read)
    }

    // Helper methods for common notification types
    const success = (message, title = 'Başarılı') => {
        return addNotification({
            type: 'success',
            title,
            message
        })
    }

    const error = (message, title = 'Hata') => {
        return addNotification({
            type: 'error',
            title,
            message,
            autoRemove: false // Errors should not auto-remove
        })
    }

    const warning = (message, title = 'Uyarı') => {
        return addNotification({
            type: 'warning',
            title,
            message
        })
    }

    const info = (message, title = 'Bilgi') => {
        return addNotification({
            type: 'info',
            title,
            message
        })
    }

    return {
        // State
        notifications,

        // Getters
        unreadCount,
        unreadNotifications,
        readNotifications,
        notificationsByType,

        // Actions
        addNotification,
        removeNotification,
        markAsRead,
        markAllAsRead,
        clearAll,
        clearRead,

        // Helper methods
        success,
        error,
        warning,
        info
    }
})
