import { onMounted, onUnmounted } from 'vue'
import { useWebSocket, WS_EVENTS } from './useWebSocket'
import { useAnalyticsStore } from '../stores/analytics'
import { useNotificationStore } from '../stores/notification'

/**
 * Real-time Dashboard Composable
 * Handles WebSocket events for dashboard real-time updates
 * 
 * @param {Object} options - Configuration options
 * @param {Boolean} options.showNotifications - Show toast notifications for events (default: true)
 * @param {Boolean} options.autoRefresh - Auto-refresh data on events (default: true)
 * @returns {Object} WebSocket connection state
 */
export function useRealtimeDashboard(options = {}) {
  const {
    showNotifications = true,
    autoRefresh = true
  } = options
  
  const ws = useWebSocket()
  const analyticsStore = useAnalyticsStore()
  const notificationStore = useNotificationStore()
  
  /**
   * Handle pulse data updates
   */
  const handlePulseUpdate = (data) => {
    if (data.payload) {
      analyticsStore.pulse = data.payload
    }
  }
  
  /**
   * Handle stats updates
   */
  const handleStatsUpdate = (data) => {
    if (data.payload) {
      analyticsStore.stats = data.payload
    }
  }
  
  /**
   * Handle KPI updates
   */
  const handleKPIUpdate = (data) => {
    if (data.payload) {
      analyticsStore.kpis = data.payload
    }
  }
  
  /**
   * Handle insight updates
   */
  const handleInsightUpdate = (data) => {
    if (data.payload) {
      analyticsStore.insights = data.payload
    }
  }
  
  /**
   * Handle appointment created event
   */
  const handleAppointmentCreated = (data) => {
    if (showNotifications) {
      notificationStore.success('Yeni randevu oluşturuldu!')
    }
    
    // Refresh relevant data
    if (autoRefresh) {
      analyticsStore.fetchPulse(true)
      analyticsStore.fetchKPIs(true)
    }
  }
  
  /**
   * Handle appointment updated event
   */
  const handleAppointmentUpdated = (data) => {
    if (autoRefresh) {
      analyticsStore.fetchPulse(true)
    }
  }
  
  /**
   * Handle appointment cancelled event
   */
  const handleAppointmentCancelled = (data) => {
    if (showNotifications && data.payload?.customer) {
      notificationStore.warning(`Randevu iptal edildi: ${data.payload.customer}`)
    }
    
    if (autoRefresh) {
      analyticsStore.fetchPulse(true)
      analyticsStore.fetchKPIs(true)
    }
  }
  
  /**
   * Handle appointment confirmed event
   */
  const handleAppointmentConfirmed = (data) => {
    if (showNotifications && data.payload?.customer) {
      notificationStore.success(`Randevu onaylandı: ${data.payload.customer}`)
    }
    
    if (autoRefresh) {
      analyticsStore.fetchPulse(true)
    }
  }
  
  /**
   * Handle call started event
   */
  const handleCallStarted = (data) => {
    // Update active calls count
    if (analyticsStore.pulse) {
      analyticsStore.pulse.activeCalls = (analyticsStore.pulse.activeCalls || 0) + 1
    }
  }
  
  /**
   * Handle call ended event
   */
  const handleCallEnded = (data) => {
    // Update active calls count
    if (analyticsStore.pulse && analyticsStore.pulse.activeCalls > 0) {
      analyticsStore.pulse.activeCalls--
    }
    
    // Optionally refresh data for completed calls
    if (autoRefresh && data.payload?.status === 'completed') {
      analyticsStore.fetchPulse(true)
    }
  }
  
  /**
   * Handle call updated event
   */
  const handleCallUpdated = (data) => {
    // Refresh pulse data if call status changed
    if (autoRefresh && data.payload?.statusChanged) {
      analyticsStore.fetchPulse(true)
    }
  }
  
  /**
   * Handle notification event
   */
  const handleNotification = (data) => {
    if (showNotifications && data.payload) {
      const { type = 'info', title, message } = data.payload
      
      switch (type) {
        case 'success':
          notificationStore.success(message, title)
          break
        case 'error':
          notificationStore.error(message, title)
          break
        case 'warning':
          notificationStore.warning(message, title)
          break
        default:
          notificationStore.info(message, title)
      }
    }
  }
  
  /**
   * Handle alert event
   */
  const handleAlert = (data) => {
    if (showNotifications && data.payload) {
      const { message, title = 'Uyarı' } = data.payload
      notificationStore.warning(message, title)
    }
  }
  
  // Register event handlers on mount
  onMounted(() => {
    ws.on(WS_EVENTS.PULSE_UPDATE, handlePulseUpdate)
    ws.on(WS_EVENTS.STATS_UPDATE, handleStatsUpdate)
    ws.on(WS_EVENTS.KPI_UPDATE, handleKPIUpdate)
    ws.on(WS_EVENTS.INSIGHT_UPDATE, handleInsightUpdate)
    ws.on(WS_EVENTS.APPOINTMENT_CREATED, handleAppointmentCreated)
    ws.on(WS_EVENTS.APPOINTMENT_UPDATED, handleAppointmentUpdated)
    ws.on(WS_EVENTS.APPOINTMENT_CANCELLED, handleAppointmentCancelled)
    ws.on(WS_EVENTS.APPOINTMENT_CONFIRMED, handleAppointmentConfirmed)
    ws.on(WS_EVENTS.CALL_STARTED, handleCallStarted)
    ws.on(WS_EVENTS.CALL_ENDED, handleCallEnded)
    ws.on(WS_EVENTS.CALL_UPDATED, handleCallUpdated)
    ws.on(WS_EVENTS.NOTIFICATION, handleNotification)
    ws.on(WS_EVENTS.ALERT, handleAlert)
  })
  
  // Unregister event handlers on unmount
  onUnmounted(() => {
    ws.off(WS_EVENTS.PULSE_UPDATE, handlePulseUpdate)
    ws.off(WS_EVENTS.STATS_UPDATE, handleStatsUpdate)
    ws.off(WS_EVENTS.KPI_UPDATE, handleKPIUpdate)
    ws.off(WS_EVENTS.INSIGHT_UPDATE, handleInsightUpdate)
    ws.off(WS_EVENTS.APPOINTMENT_CREATED, handleAppointmentCreated)
    ws.off(WS_EVENTS.APPOINTMENT_UPDATED, handleAppointmentUpdated)
    ws.off(WS_EVENTS.APPOINTMENT_CANCELLED, handleAppointmentCancelled)
    ws.off(WS_EVENTS.APPOINTMENT_CONFIRMED, handleAppointmentConfirmed)
    ws.off(WS_EVENTS.CALL_STARTED, handleCallStarted)
    ws.off(WS_EVENTS.CALL_ENDED, handleCallEnded)
    ws.off(WS_EVENTS.CALL_UPDATED, handleCallUpdated)
    ws.off(WS_EVENTS.NOTIFICATION, handleNotification)
    ws.off(WS_EVENTS.ALERT, handleAlert)
  })
  
  return {
    isConnected: ws.isConnected,
    error: ws.error,
    connect: ws.connect,
    disconnect: ws.disconnect
  }
}
