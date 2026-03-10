<template>
  <div class="portal-page">
    <div class="page-header">
      <h1 :style="{ color: colors.primary }">{{ t('satisfaction_title') }}</h1>
      <p class="subtitle">{{ t('satisfaction_subtitle') }}</p>
    </div>

    <div class="content-card">
       <div class="satisfaction-content">
            <div class="score-card" :style="{ background: getGlowColor('primary') }">
                <h3>Genel Memnuniyet</h3>
                <div class="score" :style="{ color: colors.primary }">4.8/5.0</div>
                <div class="stars">
                    <component :is="sectorStore.getIcon('Star')" v-for="i in 5" :key="i" :size="20" :fill="i <= 4 ? colors.primary : 'none'" :color="colors.primary" />
                </div>
            </div>

            <div class="feedback-list">
                 <h3>{{ t('recent_feedbacks') }}</h3>
                 <div v-for="i in 3" :key="i" class="feedback-item">
                    <div class="feedback-icon" :style="{ background: getGlowColor('primary'), color: colors.primary }">
                        <component :is="sectorStore.getIcon('MessageCircle')" :size="18" />
                    </div>
                    <div class="feedback-text">
                        <strong>Hizmet Kalitesi</strong>
                        <p>"Çok hızlı ve ilgili bir hizmet aldım, teşekkürler."</p>
                    </div>
                    <span class="feedback-date">2 gün önce</span>
                 </div>
            </div>

            <button class="action-btn-primary" :style="{ background: colors.primary }" @click="showModal = true">
                {{ t('send_new_feedback') }}
            </button>
       </div>
    </div>

    <!-- Feedback Modal -->
    <Teleport to="body">
      <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
        <div class="modal-container" :style="{ '--modal-accent': colors.primary }">
          <div class="modal-header">
            <h3>{{ t('new_feedback_title') }}</h3>
            <button class="close-btn" @click="showModal = false">
              <X :size="20" />
            </button>
          </div>
          
          <div class="modal-body">
            <div class="rating-section">
              <label>{{ t('rate_service') }}</label>
              <div class="rating-stars">
                <button 
                  v-for="i in 5" 
                  :key="i" 
                  @click="form.score = i"
                  class="star-btn"
                >
                  <Star 
                    :size="32" 
                    :fill="i <= form.score ? colors.primary : 'none'" 
                    :color="i <= form.score ? colors.primary : '#94a3b8'" 
                  />
                </button>
              </div>
            </div>

            <div class="form-group">
              <label>{{ t('your_thoughts') }}</label>
              <textarea 
                v-model="form.feedback" 
                :placeholder="t('feedback_placeholder')"
                rows="4"
              ></textarea>
            </div>
          </div>

          <div class="modal-footer">
            <button class="cancel-btn" @click="showModal = false">{{ t('cancel') }}</button>
            <button 
              class="submit-btn" 
              :disabled="!form.score || isSubmitting"
              :style="{ background: colors.primary }"
              @click="submitFeedback"
            >
              <span v-if="isSubmitting">{{ t('sending') }}</span>
              <span v-else>{{ t('send') }}</span>
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, inject } from 'vue'
import { Star, X } from 'lucide-vue-next'
import { useSectorStore } from '../../stores/sector'
import { useNotificationStore } from '../../stores/notification'

const axios = inject('axios')
const sectorStore = useSectorStore()
const notificationStore = useNotificationStore()

const showModal = ref(false)
const isSubmitting = ref(false)
const form = ref({
    score: 5,
    feedback: ''
})

const colors = computed(() => sectorStore.theme || {
    primary: '#0ea5e9',
    secondary: '#0f766e',
    text: '#0f172a',
    background: '#f0f9ff'
})

const getColor = (name) => (sectorStore.theme || {})[name] || colors.value.primary
const getGlowColor = (name) => getColor(name) + '1A'

const t = (key) => sectorStore.t(key)

const submitFeedback = async () => {
    isSubmitting.value = true
    try {
        const tenant = sessionStorage.getItem('tenant_slug') || 'medical'
        const response = await axios.post('/satisfaction', {
            tenant: tenant,
            score: form.score,
            feedback: form.feedback
        })
        
        notificationStore.success(
            t('feedback_success'),
            t('feedback_success_title')
        )
        
        showModal.value = false
        form.value = { score: 5, feedback: '' }
    } catch (err) {
        console.error('Feedback error:', err)
        const errorMsg = err.response?.data?.message || err.response?.data?.error || err.message
        notificationStore.error(
            `${t('feedback_error')}: ${errorMsg}`,
            t('system_error')
        )
    } finally {
        isSubmitting.value = false
    }
}
</script>

<style scoped>
.portal-page {
    width: 100%;
    margin: 0;
    padding: 24px;
}

.page-header {
    margin-bottom: 32px;
}

.page-header h1 {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 4px;
}

.subtitle {
    color: var(--text-secondary);
    font-size: 14px;
}

.content-card {
    background: var(--surface-elevated);
    border-radius: 12px;
    padding: 32px;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
}

.satisfaction-content {
    display: flex;
    flex-direction: column;
    gap: 32px;
    align-items: center;
}

.score-card {
    padding: 32px;
    border-radius: 16px;
    text-align: center;
    width: 100%;
    max-width: 400px;
}

.score-card h3 {
    margin-bottom: 16px;
    font-weight: 600;
    color: var(--text-primary);
}

.score {
    font-size: 48px;
    font-weight: 800;
    margin-bottom: 16px;
}

.stars {
    display: flex;
    justify-content: center;
    gap: 8px;
}

.feedback-list {
    width: 100%;
}

.feedback-list h3 {
    margin-bottom: 16px;
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
}

.feedback-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px;
    border-bottom: 1px solid var(--border-subtle);
}

.feedback-icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.feedback-text {
    flex: 1;
}

.feedback-text strong {
    display: block;
    font-size: 14px;
    color: var(--text-primary);
}

.feedback-text p {
    font-size: 13px;
    color: var(--text-secondary);
    margin-top: 4px;
}

.feedback-date {
    font-size: 12px;
    color: var(--text-muted);
}

.action-btn-primary {
    padding: 12px 24px;
    border-radius: 8px;
    color: white;
    font-weight: 600;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
}

.action-btn-primary:hover {
    opacity: 0.9;
    transform: translateY(-1px);
}

/* Modal Styles */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
}

.modal-container {
    background: var(--bg-surface, #0f172a);
    width: 90%;
    max-width: 500px;
    border-radius: 16px;
    border: 1px solid var(--modal-accent, rgba(255, 255, 255, 0.1));
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5),
                0 0 0 1px var(--modal-accent, transparent) inset;
    overflow: hidden;
}

.modal-header {
    padding: 20px 24px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.modal-header h3 {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
}

.close-btn {
    background: transparent;
    border: none;
    color: #94a3b8;
    cursor: pointer;
    transition: color 0.2s;
}

.close-btn:hover {
    color: white;
}

.modal-body {
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.rating-section {
    text-align: center;
}

.rating-section label {
    display: block;
    margin-bottom: 12px;
    font-size: 14px;
    color: #94a3b8;
}

.rating-stars {
    display: flex;
    justify-content: center;
    gap: 12px;
}

.star-btn {
    background: transparent;
    border: none;
    cursor: pointer;
    transition: transform 0.2s;
}

.star-btn:hover {
    transform: scale(1.2);
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-size: 14px;
    color: #94a3b8;
}

.form-group textarea {
    width: 100%;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 12px;
    color: white;
    font-size: 14px;
    resize: none;
}

.form-group textarea:focus {
    outline: none;
    border-color: var(--modal-accent, #6366f1);
    box-shadow: 0 0 0 3px color-mix(in srgb, var(--modal-accent, #6366f1) 15%, transparent);
}

.modal-footer {
    padding: 20px 24px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    justify-content: flex-end;
    gap: 12px;
}

.cancel-btn {
    padding: 10px 20px;
    border-radius: 8px;
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: white;
    font-size: 14px;
    cursor: pointer;
}

.submit-btn {
    padding: 10px 24px;
    border-radius: 8px;
    color: white;
    font-weight: 600;
    border: none;
    cursor: pointer;
}

.submit-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
</style>
