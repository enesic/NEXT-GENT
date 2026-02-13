<template>
  <div class="helpdesk-container">
    <!-- Chat Button (Floating) -->
    <button 
      v-if="!isOpen"
      class="chat-button"
      @click="openChat"
      :class="{ 'pulse': hasUnreadMessages }"
    >
      <MessageCircle :size="24" :stroke-width="2" />
      <span v-if="hasUnreadMessages" class="badge">{{ unreadCount }}</span>
    </button>

    <!-- Chat Window -->
    <Transition name="slide-up">
      <div v-if="isOpen" class="chat-window">
        <!-- Header -->
        <div class="chat-header">
          <div class="header-info">
            <div class="ai-avatar">
              <Sparkles :size="20" :stroke-width="2" />
            </div>
            <div>
              <h3>AI Yardım Merkezi</h3>
              <p class="status-text">
                <span class="status-dot"></span>
                {{ isTyping ? 'Yazıyor...' : 'Çevrimiçi' }}
              </p>
            </div>
          </div>
          <button class="close-btn" @click="closeChat">
            <X :size="20" :stroke-width="2" />
          </button>
        </div>

        <!-- Messages -->
        <div class="chat-messages" ref="messagesContainer">
          <div 
            v-for="(message, index) in messages" 
            :key="index"
            :class="['message', message.role]"
          >
            <div v-if="message.role === 'assistant'" class="message-avatar">
              <Sparkles :size="16" :stroke-width="2" />
            </div>
            <div class="message-content">
              <div class="message-text" v-html="formatMessage(message.content)"></div>
              <div class="message-time">{{ formatTime(message.timestamp) }}</div>
            </div>
            <div v-if="message.role === 'user'" class="message-avatar user">
              <User :size="16" :stroke-width="2" />
            </div>
          </div>
          
          <!-- Typing Indicator -->
          <div v-if="isTyping" class="message assistant">
            <div class="message-avatar">
              <Sparkles :size="16" :stroke-width="2" />
            </div>
            <div class="message-content">
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>

        <!-- Input -->
        <div class="chat-input">
          <input
            v-model="inputMessage"
            @keyup.enter="sendMessage"
            :disabled="isTyping"
            placeholder="Mesajınızı yazın..."
            class="message-input"
          />
          <button 
            @click="sendMessage" 
            :disabled="!inputMessage.trim() || isTyping"
            class="send-btn"
          >
            <Send :size="20" :stroke-width="2" />
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted, onUnmounted } from 'vue'
import { MessageCircle, Sparkles, X, User, Send } from 'lucide-vue-next'
import { inject } from 'vue'
import { useWebSocket } from '../composables/useWebSocket'

import axios from 'axios'

// Create clean axios instance for public helpdesk endpoint
const helpdeskApi = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  headers: {
    'Content-Type': 'application/json'
  }
})

// State
const isOpen = ref(false)
const messages = ref([
  {
    role: 'assistant',
    content: 'Merhaba! 👋 Ben NextGent AI Yardım Merkezi. Size nasıl yardımcı olabilirim?',
    timestamp: new Date()
  }
])
const inputMessage = ref('')
const isTyping = ref(false)
const hasUnreadMessages = ref(false)
const unreadCount = ref(0)
const messagesContainer = ref(null)

// WebSocket for real-time notifications (optional, can work without)
let wsOn = null
let wsIsConnected = ref(false)

// Try to initialize WebSocket if available
try {
  const ws = useWebSocket()
  wsOn = ws.on
  wsIsConnected = ws.isConnected
} catch (e) {
  console.log('WebSocket not available, helpdesk will work without real-time notifications')
}

// Computed
const formatTime = (date) => {
  return new Date(date).toLocaleTimeString('tr-TR', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

const formatMessage = (text) => {
  // Simple markdown-like formatting
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>')
}

// Methods
const openChat = () => {
  isOpen.value = true
  hasUnreadMessages.value = false
  unreadCount.value = 0
  scrollToBottom()
}

const closeChat = () => {
  isOpen.value = false
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const sendMessage = async () => {
  if (!inputMessage.value.trim() || isTyping.value) return

  const userMessage = {
    role: 'user',
    content: inputMessage.value,
    timestamp: new Date()
  }

  messages.value.push(userMessage)
  const currentMessage = inputMessage.value
  inputMessage.value = ''
  isTyping.value = true

  await scrollToBottom()

  try {
    // Send to backend AI helpdesk endpoint
    const response = await helpdeskApi.post('/helpdesk/chat', {
      message: currentMessage,
      context: {
        page: 'landing',
        timestamp: new Date().toISOString()
      }
    })

    // Add AI response
    setTimeout(() => {
      messages.value.push({
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date()
      })
      isTyping.value = false
      scrollToBottom()
    }, 500)

  } catch (error) {
    console.error('Helpdesk error:', error)
    messages.value.push({
      role: 'assistant',
      content: 'Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin veya bizimle iletişime geçin: info@nextgent.co',
      timestamp: new Date()
    })
    isTyping.value = false
    scrollToBottom()
  }
}

// Listen for notifications
onMounted(() => {
  // Listen for helpdesk notifications via WebSocket (if available)
  if (wsOn && wsIsConnected.value) {
    wsOn('HELPDESK_NOTIFICATION', (data) => {
      if (!isOpen.value) {
        hasUnreadMessages.value = true
        unreadCount.value++
      }
    })
  }
})

onUnmounted(() => {
  // Cleanup if needed
})
</script>

<style scoped>
.helpdesk-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 1000;
}

/* Chat Button */
.chat-button {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.chat-button:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(99, 102, 241, 0.5);
}

.chat-button.pulse {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4);
  }
  50% {
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.8), 0 0 0 8px rgba(99, 102, 241, 0.2);
  }
}

.badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: #ef4444;
  color: white;
  font-size: 12px;
  font-weight: 700;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #030303;
}

/* Chat Window */
.chat-window {
  width: 400px;
  height: 600px;
  background: rgba(24, 24, 27, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  overflow: hidden;
}

/* Header */
.chat-header {
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(255, 255, 255, 0.03);
}

.header-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.ai-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 0 16px rgba(99, 102, 241, 0.4);
}

.header-info h3 {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: white;
}

.status-text {
  font-size: 12px;
  color: #a1a1aa;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
  display: inline-block;
  animation: pulse-dot 2s infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.close-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: transparent;
  border: none;
  color: #a1a1aa;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

/* Messages */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(99, 102, 241, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6366f1;
  flex-shrink: 0;
}

.message-avatar.user {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.message-content {
  max-width: 70%;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.message.user .message-content {
  align-items: flex-end;
}

.message-text {
  padding: 12px 16px;
  border-radius: 16px;
  font-size: 14px;
  line-height: 1.5;
  word-wrap: break-word;
}

.message.assistant .message-text {
  background: rgba(255, 255, 255, 0.05);
  color: white;
  border-bottom-left-radius: 4px;
}

.message.user .message-text {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  border-bottom-right-radius: 4px;
}

.message-time {
  font-size: 11px;
  color: #71717a;
  padding: 0 4px;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  border-bottom-left-radius: 4px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #6366f1;
  animation: typing 1.4s infinite;
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
    transform: translateY(-10px);
    opacity: 1;
  }
}

/* Input */
.chat-input {
  padding: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  gap: 12px;
  background: rgba(255, 255, 255, 0.03);
}

.message-input {
  flex: 1;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 12px 16px;
  color: white;
  font-size: 14px;
  outline: none;
  transition: all 0.2s;
}

.message-input:focus {
  border-color: #6366f1;
  background: rgba(255, 255, 255, 0.08);
}

.message-input::placeholder {
  color: #71717a;
}

.send-btn {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(99, 102, 241, 0.4);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Transitions */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}

/* Responsive */
@media (max-width: 768px) {
  .chat-window {
    width: calc(100vw - 32px);
    height: calc(100vh - 100px);
    max-width: 400px;
    max-height: 600px;
  }
  
  .helpdesk-container {
    bottom: 16px;
    right: 16px;
  }
  
  .chat-button {
    width: 56px;
    height: 56px;
  }
}
</style>

