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

// Production hosts that typically don't support WebSocket (Vercel, static hosting)
const WS_DISABLED_HOSTS = ['nextgent.co', 'vercel.app']

/**
 * WebSocket Composable
 * Handles real-time connections with automatic reconnection.
 * Disabled on production hosts without WebSocket support to prevent console spam.
 */
export function useWebSocket() {
    const ws = ref(null)
    const isConnected = ref(false)
    const error = ref(null)
    const listeners = ref(new Map())
    const reconnectAttempts = ref(0)
    const maxReconnectAttempts = 2
    const maxReconnectDelay = 5000
    let reconnectTimeout = null

    const authStore = useAuthStore()

    const isWsDisabled = () => {
        const host = typeof window !== 'undefined' ? window.location.hostname : ''
        const disabled = WS_DISABLED_HOSTS.some(h => host.includes(h))
        const hasDedicatedWs = !!import.meta.env.VITE_WS_URL
        return disabled && !hasDedicatedWs
    }

    const connect = () => {
        if (isWsDisabled()) return
        if (!authStore.tenant_id) return
        if (ws.value && ws.value.readyState === WebSocket.OPEN) return
        if (reconnectAttempts.value >= maxReconnectAttempts) return

        try {
            // Build WebSocket URL
            let wsUrl
            
            // Check if we have a dedicated WebSocket URL (HYBRID deployment)
            const wsBaseUrl = import.meta.env.VITE_WS_URL
            
            if (wsBaseUrl) {
                // Production HYBRID: Separate WebSocket service
                // wss://nextgent-ws.railway.app + /ws/{tenant_id}
                wsUrl = `${wsBaseUrl}/ws/${authStore.tenant_id}`
            } else if (API_CONFIG.BASE_URL.startsWith('http://') || API_CONFIG.BASE_URL.startsWith('https://')) {
                // Fallback: Convert REST API URL to WebSocket
                // https://backend.railway.app/api/v1 -> wss://backend.railway.app/api/v1/ws/{tenant_id}
                const baseUrl = API_CONFIG.BASE_URL.replace(/^http/, 'ws')
                wsUrl = `${baseUrl}/ws/${authStore.tenant_id}`
            } else {
                // Development: Local development setup
                // /api/v1 -> ws://localhost:8001/api/v1/ws/{tenant_id}
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
                const host = window.location.hostname
                const port = import.meta.env.DEV ? '8001' : window.location.port
                const portSuffix = port ? `:${port}` : ''
                wsUrl = `${protocol}//${host}${portSuffix}${API_CONFIG.BASE_URL}/ws/${authStore.tenant_id}`
            }

            if (import.meta.env.DEV) console.log(`🔌 Connecting to WebSocket: ${wsUrl}`)
            ws.value = new WebSocket(wsUrl)

            ws.value.onopen = () => {
                if (import.meta.env.DEV) console.log('✅ WebSocket Connected')
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
                isConnected.value = false
                handleReconnect()
            }

            ws.value.onerror = (e) => {
                error.value = e
            }

        } catch (e) {
            console.error('Failed to create WebSocket connection:', e)
            handleReconnect()
        }
    }

    const handleReconnect = () => {
        if (reconnectAttempts.value >= maxReconnectAttempts) return
        if (reconnectTimeout) clearTimeout(reconnectTimeout)

        const delay = Math.min(1000 * Math.pow(2, reconnectAttempts.value), maxReconnectDelay)

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
