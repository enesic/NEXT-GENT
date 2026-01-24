<template>
  <Teleport to="body">
    <Transition name="panel-fade">
      <div v-if="isOpen" class="ai-call-panel-overlay">
        <div 
          ref="panelRef" 
          class="ai-call-panel glass-effect"
          @click.stop
        >
          <!-- Header -->
          <div class="panel-header">
            <div class="header-left">
              <div class="status-indicator" ref="pulseRef">
                <div class="pulse-ring"></div>
                <Phone :size="16" :stroke-width="2.5" />
              </div>
              <div class="header-info">
                <h3 class="panel-title">AI Canlı Bağlantı</h3>
                <span class="call-duration">{{ callDuration }}</span>
              </div>
            </div>
            <button class="close-btn" @click="closePanel">
              <X :size="20" :stroke-width="2" />
            </button>
          </div>

          <!-- Customer Recognition Card -->
          <div class="customer-card" ref="customerCardRef">
            <div class="customer-header">
              <div class="customer-avatar">{{ customerInitials }}</div>
              <div class="customer-info">
                <h4 class="customer-name">{{ customer.name }}</h4>
                <span class="customer-segment" :class="customer.segmentClass">
                  <Crown :size="14" :stroke-width="2.5" />
                  {{ customer.segment }}
                </span>
              </div>
            </div>
            
            <div class="customer-history">
              <div class="history-header">
                <History :size="14" :stroke-width="2" />
                <span>Geçmiş Randevular</span>
              </div>
              <div class="history-list">
                <div 
                  v-for="(note, index) in customer.history" 
                  :key="index"
                  class="history-item"
                >
                  <span class="history-date">{{ note.date }}</span>
                  <span class="history-note">{{ note.note }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Live Transcript -->
          <div class="transcript-section">
            <div class="transcript-header">
              <MessageSquare :size="16" :stroke-width="2" />
              <span>Live Transcript</span>
              <span class="live-badge">
                <span class="live-dot"></span>
                CANLI
              </span>
            </div>
            
            <div class="transcript-messages" ref="transcriptRef">
              <div 
                v-for="message in transcript" 
                :key="message.id"
                :class="['message', message.type]"
              >
                <div class="message-content">
                  <span class="message-text" v-html="highlightText(message.text)"></span>
                  <span class="message-time">{{ message.time }}</span>
                </div>
              </div>
              
              <div v-if="isTyping" class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="action-buttons">
            <button class="glass-button action-btn approve-btn">
              <CheckCircle2 :size="18" :stroke-width="2" />
              <span>Randevuyu Onayla</span>
            </button>
            <button class="glass-button action-btn transfer-btn">
              <PhoneForwarded :size="18" :stroke-width="2" />
              <span>Operatöre Aktar</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Floating Trigger Button -->
    <button 
      v-if="!isOpen"
      class="call-trigger-btn"
      @click="openPanel"
      ref="triggerRef"
    >
      <Phone :size="24" :stroke-width="2.5" />
      <span class="trigger-badge">1</span>
    </button>
  </Teleport>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { gsap } from 'gsap'
import { 
  Phone, 
  X, 
  Crown, 
  History, 
  MessageSquare, 
  CheckCircle2, 
  PhoneForwarded 
} from 'lucide-vue-next'
import { useWebSocket } from '../composables/useWebSocket'

const isOpen = ref(false)
const panelRef = ref(null)
const customerCardRef = ref(null)
const transcriptRef = ref(null)
const pulseRef = ref(null)
const triggerRef = ref(null)

// Call state
const callDuration = ref('00:42')
const isTyping = ref(false)

// Highlighter logic
const highlightText = (text) => {
    if (!text) return ''
    
    // Terms: Medical, Legal, Real Estate
    const terms = [
      'Randevu', 'Muayene', 'Kardiyoloji', 'İlaç', 
      'Dava', 'Duruşma', 'Mahkeme', 'Dosya', 
      'Portföy', 'Daire', 'Tapu', 'Sunum', 'Emlak'
    ]
    
    let highlighted = text
    terms.forEach(term => {
        const regex = new RegExp(`(${term})`, 'gi')
        highlighted = highlighted.replace(regex, '<span class="term-highlight">$1</span>')
    })
    
    return highlighted
}

// Customer data
const customer = ref({
  name: 'Ayşe Yılmaz',
  segment: 'VIP Platinum',
  segmentClass: 'vip-platinum',
  history: [
    { date: '15 Ocak', note: 'Kontrol muayenesi - Başarılı' },
    { date: '8 Ocak', note: 'Tedavi planı güncellendi' },
    { date: '2 Ocak', note: 'İlk konsültasyon tamamlandı' }
  ]
})

const customerInitials = computed(() => {
  return customer.value.name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
})

// Transcript messages
const transcript = ref([
  { id: 1, type: 'ai', text: 'Merhaba, NextGent AI asistanı. Size nasıl yardımcı olabilirim?', time: '00:12' },
  { id: 2, type: 'customer', text: 'Merhaba, yarın için randevu almak istiyorum.', time: '00:18' },
  { id: 3, type: 'ai', text: 'Tabii ki! Hangi saat aralığı sizin için uygun?', time: '00:25' },
  { id: 4, type: 'customer', text: 'Öğleden sonra müsait miyim acaba?', time: '00:32' },
  { id: 5, type: 'ai', text: '14:30 ve 16:00 saatleri müsait. Hangisini tercih edersiniz?', time: '00:38' }
])

// Auto-scroll transcript
watch(() => transcript.value.length, async () => {
  await nextTick()
  if (transcriptRef.value) {
    gsap.to(transcriptRef.value, {
      scrollTop: transcriptRef.value.scrollHeight,
      duration: 0.5,
      ease: 'power2.out'
    })
  }
})

// Simulate typing
const simulateTyping = () => {
  isTyping.value = true
  setTimeout(() => {
    isTyping.value = false
    transcript.value.push({
      id: transcript.value.length + 1,
      type: 'ai',
      text: 'Randevunuz 23 Ocak, 14:30 için kaydedildi. Başka bir konuda yardımcı olabilir miyim?',
      time: '00:45'
    })
  }, 2000)
}

const openPanel = () => {
  isOpen.value = true
  
  nextTick(() => {
    // Panel entrance animation with GSAP
    gsap.from(panelRef.value, {
      duration: 0.6,
      scale: 0.85,
      opacity: 0,
      y: 50,
      ease: 'power3.out'
    })

    // Indigo glow effect
    gsap.to(panelRef.value, {
      duration: 1.5,
      boxShadow: '0 0 60px rgba(99, 102, 241, 0.8), 0 8px 32px rgba(0, 0, 0, 0.4)',
      repeat: 2,
      yoyo: true,
      ease: 'sine.inOut'
    })

    // Customer card quick load (50ms delay)
    gsap.from(customerCardRef.value, {
      duration: 0.4,
      opacity: 0,
      y: 20,
      delay: 0.05,
      ease: 'power2.out'
    })

    // Pulse animation for active call indicator
    gsap.to(pulseRef.value, {
      duration: 1.5,
      scale: 1.1,
      opacity: 0.8,
      repeat: -1,
      yoyo: true,
      ease: 'sine.inOut'
    })

    // Simulate typing after 3 seconds
    setTimeout(simulateTyping, 3000)
  })
}

const closePanel = () => {
  gsap.to(panelRef.value, {
    duration: 0.3,
    scale: 0.9,
    opacity: 0,
    y: 20,
    ease: 'power2.in',
    onComplete: () => {
      isOpen.value = false
    }
  })
}

onMounted(() => {
  // Trigger button pulse animation
  if (triggerRef.value) {
    gsap.to(triggerRef.value, {
      duration: 2,
      boxShadow: '0 0 30px rgba(99, 102, 241, 0.6)',
      repeat: -1,
      yoyo: true,
      ease: 'sine.inOut'
    })
  }

  // WebSocket Integration
  const { on, off } = useWebSocket()
  
  const handleNewCall = (data) => {
    console.log('📞 Incoming Call Detected:', data)
    
    // Update customer data if provided
    if (data.customer) {
      customer.value = { ...customer.value, ...data.customer }
    }
    
    // Reset call state
    transcript.value = []
    
    // Open the panel with "Wow" effect
    openPanel()
  }

  const handleTranscript = (data) => {
    // data: { role: 'ai' | 'customer', text: '...', is_final: boolean }
    const text = data.text
    
    // Regex based Terminology Highlighting
    // Terms: Medical, Legal, Real Estate
    const terms = [
      'Randevu', 'Muayene', 'Kardiyoloji', 'İlaç', // Medical
      'Dava', 'Duruşma', 'Mahkeme', 'Dosya', // Legal
      'Portföy', 'Daire', 'Tapu', 'Sunum', 'Emlak' // Real Estate
    ]
    
    // Simple wrapping for highlighting (frontend usually needs v-html for this but simplified here for demo logic)
    // Actually, we'll store clean text and handle highlighting in template if possible, 
    // or just assume text is displayed as is. 
    // To enable highlighting we need safe HTML rendering.
    
    // For now, let's just push the message
    
    // Check if we should update the last message (streaming) or add new
    const lastMsg = transcript.value[transcript.value.length - 1]
    
    if (lastMsg && lastMsg.type === (data.role === 'assistant' ? 'ai' : 'customer') && !lastMsg.isFinal) {
        lastMsg.text = text
        lastMsg.isFinal = data.is_final
    } else {
        transcript.value.push({
            id: Date.now(),
            type: data.role === 'assistant' ? 'ai' : 'customer',
            text: text,
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            isFinal: data.is_final
        })
    }
  }

  const handleActionSignal = (data) => {
    // data: { action: 'CONFIRMATION', details: '...' }
    if (data.action === 'CONFIRMATION') {
        // Trigger Green Flash Effect on action buttons
        gsap.to('.approve-btn', {
            backgroundColor: '#22c55e',
            color: '#fff',
            duration: 0.5,
            yoyo: true,
            repeat: 3,
            onComplete: () => {
                gsap.to('.approve-btn', { clearProps: 'all' })
            }
        })
        
        // Add system message to transcript
        transcript.value.push({
            id: Date.now(),
            type: 'system',
            text: '✅ Teyit Alındı: Randevu Onaylandı',
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        })
    }
  }
  
  on('NEW_CALL', handleNewCall)
  on('TRANSCRIPT', handleTranscript)
  on('ACTION_SIGNAL', handleActionSignal)
  
  // Cleanup listener on unmount
  onUnmounted(() => {
    off('NEW_CALL', handleNewCall)
    off('TRANSCRIPT', handleTranscript)
    off('ACTION_SIGNAL', handleActionSignal)
  })
})
</script>

<style scoped>
.ai-call-panel-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 9999;
  pointer-events: none;
}

.ai-call-panel {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 420px;
  max-height: 700px;
  border-radius: var(--radius-lg);
  overflow: hidden;
  pointer-events: all;
  display: flex;
  flex-direction: column;
}

/* Panel Fade Transition */
.panel-fade-enter-active,
.panel-fade-leave-active {
  transition: opacity 0.3s ease;
}

.panel-fade-enter-from,
.panel-fade-leave-to {
  opacity: 0;
}

/* Header */
.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-indicator {
  position: relative;
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 0 20px rgba(34, 197, 94, 0.5);
}

.pulse-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid #22c55e;
  animation: pulse-ring 2s ease-out infinite;
}

@keyframes pulse-ring {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(1.5);
    opacity: 0;
  }
}

.header-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.panel-title {
  font-size: 16px;
  font-weight: 600;
  letter-spacing: var(--letter-spacing-tight);
}

.call-duration {
  font-size: 12px;
  color: var(--text-muted);
  font-weight: 500;
}

.close-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--text-primary);
}

/* Customer Card */
.customer-card {
  padding: 16px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.customer-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.customer-avatar {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, var(--indigo-primary), #8b5cf6);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  color: white;
  box-shadow: 0 0 20px var(--indigo-glow);
}

.customer-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.customer-name {
  font-size: 16px;
  font-weight: 600;
  letter-spacing: var(--letter-spacing-tight);
}

.customer-segment {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  width: fit-content;
}

.customer-segment.vip-platinum {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  color: #000;
  box-shadow: 0 0 16px rgba(251, 191, 36, 0.4);
}

.customer-history {
  margin-top: 12px;
}

.history-header {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.history-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: var(--radius-sm);
  border-left: 2px solid var(--indigo-primary);
}

.history-date {
  font-size: 11px;
  font-weight: 600;
  color: var(--indigo-primary);
}

.history-note {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.4;
}

/* Transcript Section */
.transcript-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.transcript-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 13px;
  font-weight: 600;
}

.live-badge {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  background: rgba(239, 68, 68, 0.15);
  border-radius: 8px;
  font-size: 10px;
  font-weight: 700;
  color: #ef4444;
}

.live-dot {
  width: 6px;
  height: 6px;
  background: #ef4444;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

.transcript-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  display: flex;
  animation: messageSlide 0.3s ease-out;
}

@keyframes messageSlide {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.ai {
  justify-content: flex-start;
}

.message.customer {
  justify-content: flex-end;
}

.message-content {
  max-width: 75%;
  padding: 10px 14px;
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.message.ai .message-content {
  background: rgba(99, 102, 241, 0.15);
  border: 1px solid rgba(99, 102, 241, 0.3);
}

.message.customer .message-content {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.message-text {
  font-size: 13px;
  line-height: 1.5;
  letter-spacing: var(--letter-spacing-normal);
}

.message-time {
  font-size: 10px;
  color: var(--text-muted);
  align-self: flex-end;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 10px 14px;
  background: rgba(99, 102, 241, 0.15);
  border: 1px solid rgba(99, 102, 241, 0.3);
  border-radius: var(--radius-md);
  width: fit-content;
}

.typing-indicator span {
  width: 6px;
  height: 6px;
  background: var(--indigo-primary);
  border-radius: 50%;
  animation: typing 1.4s ease-in-out infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.7;
  }
  30% {
    transform: translateY(-8px);
    opacity: 1;
  }
}

/* Action Buttons */
.action-buttons {
  padding: 16px 20px;
  display: flex;
  gap: 12px;
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  border-radius: var(--radius-md);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: var(--letter-spacing-normal);
  cursor: pointer;
  font-family: var(--font-family);
  color: var(--text-primary);
}

/* Floating Trigger Button */
.call-trigger-btn {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, var(--indigo-primary), #8b5cf6);
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  cursor: pointer;
  box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4);
  transition: all var(--transition-base);
  z-index: 9998;
}

.call-trigger-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 12px 32px rgba(99, 102, 241, 0.6);
}

.trigger-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 20px;
  height: 20px;
  background: #ef4444;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  border: 2px solid var(--obsidian-black);
  box-shadow: 0 0 12px #ef4444;
}

:deep(.term-highlight) {
  background: rgba(251, 191, 36, 0.2);
  color: #fbbf24;
  font-weight: 700;
  padding: 0 4px;
  border-radius: 4px;
  border: 1px solid rgba(251, 191, 36, 0.3);
}
</style>
