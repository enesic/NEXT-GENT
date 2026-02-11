import { ref, onMounted, onUnmounted } from 'vue'
import { API_CONFIG } from '../config/api'
import { useAuthStore } from '../stores/auth'

/**
 * WebSocket Event Types
 */
export const WS_EVENTS = {
  // Data updates
  PULSE_UPDATE: 'pulse_update',
  STATS_UPDATE: 'stats_update',
  KPI_UPDATE: 'kpi_update',
  INSIGHT_UPDATE: 'insight_update',
  
  // Appointment events
  APPOINTMENT_CREATED: 'appointment_created',
  APPOINTMENT_UPDATED: 'appointment_updated',
  APPOINTMENT_CANCELLED: 'appointment_cancelled',
  APPOINTMENT_CONFIRMED: 'appointment_confirmed',
  
  // Call events
  CALL_STARTED: 'call_started',
  CALL_ENDED: 'call_ended',
  CALL_UPDATED: 'call_updated',
  
  // System events
  NOTIFICATION: 'notification',
  ALERT: 'alert',
  
  // Connection events
  PING: 'ping',
  PONG: 'pong'
}

/**
 * WebSocket Composable
 * Handles real-time connections with automatic reconnection
 */
export function useWebSocket() {
    const ws = ref(null)
    const isConnected = ref(false)
    const error = ref(null)
    const listeners = ref(new Map())
    const reconnectAttempts = ref(0)
    const maxReconnectDelay = 30000 // 30 seconds
    let reconnectTimeout = null

    // Get tenant ID from auth store
    const authStore = useAuthStore()

    const connect = () => {
        // Don't connect if no tenant ID
        if (!authStore.tenant_id) {
            console.warn('Cannot connect to WebSocket: No tenant ID')
            return
        }

        // Don't connect if already connected
        if (ws.value && ws.value.readyState === WebSocket.OPEN) {
            return
        }

        try {
            // Build WebSocket URL
            // Replace http/https with ws/wss
            let baseUrl = API_CONFIG.BASE_URL.replace(/^http/, 'ws')
            // Remove /api/v1 if it exists in base URL as usually WS endpoints are parallel or specific
            // In our case we defined it under /api/v1/ws so we append /ws
            // The FastAPI router prefix is /ws, and we included it in api router
            // So path is BASE_URL + /ws/{tenant_id}

            const wsUrl = `${baseUrl}/ws/${authStore.tenant_id}`

            console.log(`🔌 Connecting to WebSocket: ${wsUrl}`)
            ws.value = new WebSocket(wsUrl)

            ws.value.onopen = () => {
                console.log('✅ WebSocket Connected')
                isConnected.value = true
                error.value = null
                reconnectAttempts.value = 0
            }

            ws.value.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data)
                    
                    // Handle ping/pong
                    if (data.type === WS_EVENTS.PING) {
                        ws.value.send(JSON.stringify({ type: WS_EVENTS.PONG }))
                        return
                    }
                    
                    // Dispatch event to specific listeners
                    if (data.type && listeners.value.has(data.type)) {
                        listeners.value.get(data.type).forEach(callback => callback(data))
                    }
                    
                    // Dispatch to global wildcard listeners
                    if (listeners.value.has('*')) {
                        listeners.value.get('*').forEach(callback => callback(data))
                    }
                } catch (e) {
                    console.error('Error parsing WebSocket message:', e)
                }
            }

            ws.value.onclose = () => {
                console.log('❌ WebSocket Disconnected')
                isConnected.value = false
                handleReconnect()
            }

            ws.value.onerror = (e) => {
                console.error('⚠️ WebSocket Error:', e)
                error.value = e
            }

        } catch (e) {
            console.error('Failed to create WebSocket connection:', e)
            handleReconnect()
        }
    }

    const handleReconnect = () => {
        // Clear existing timeout
        if (reconnectTimeout) clearTimeout(reconnectTimeout)

        // Calculate delay with exponential backoff
        // 1s, 2s, 4s, 8s, 16s, 30s (capped)
        const delay = Math.min(
            1000 * Math.pow(2, reconnectAttempts.value),
            maxReconnectDelay
        )

        console.log(`Reconnecting in ${delay}ms (Attempt ${reconnectAttempts.value + 1})`)

        reconnectTimeout = setTimeout(() => {
            reconnectAttempts.value++
            connect()
        }, delay)
    }

    const disconnect = () => {
        if (reconnectTimeout) clearTimeout(reconnectTimeout)
        if (ws.value) {
            ws.value.close()
            ws.value = null
        }
    }

    const on = (eventType, callback) => {
        if (!listeners.value.has(eventType)) {
            listeners.value.set(eventType, [])
        }
        listeners.value.get(eventType).push(callback)
    }

    const off = (eventType, callback) => {
        if (listeners.value.has(eventType)) {
            const callbacks = listeners.value.get(eventType)
            const index = callbacks.indexOf(callback)
            if (index !== -1) {
                callbacks.splice(index, 1)
            }
        }
    }

    // Auto-connect on mount, disconnect on unmount
    onMounted(() => {
        connect()
    })

    onUnmounted(() => {
        disconnect()
    })

    return {
        isConnected,
        error,
        connect,
        disconnect,
        on,
        off
    }
}
