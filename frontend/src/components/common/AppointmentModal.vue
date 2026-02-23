<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div v-if="modelValue" class="modal-overlay" @click.self="close">
        <Transition name="modal-slide">
          <div v-if="modelValue" class="modal-box" role="dialog" aria-modal="true" aria-labelledby="modal-title">
            <!-- Header -->
            <div class="modal-header">
              <div class="modal-title-row">
                <div class="modal-icon">
                  <CalendarPlus :size="20" :stroke-width="2" />
                </div>
                <h2 id="modal-title">Yeni Randevu Oluştur</h2>
              </div>
              <button class="close-btn" @click="close" aria-label="Kapat">
                <X :size="20" :stroke-width="2" />
              </button>
            </div>

            <!-- Form -->
            <form @submit.prevent="submit" class="modal-form">
              <!-- Service Type -->
              <div class="form-group">
                <label class="form-label">
                  <Tag :size="14" />
                  Hizmet Türü
                </label>
                <select v-model="form.service" class="form-select" required>
                  <option value="" disabled>Hizmet seçin...</option>
                  <option v-for="s in serviceOptions" :key="s" :value="s">{{ s }}</option>
                </select>
              </div>

              <!-- Date & Time Row -->
              <div class="form-row">
                <div class="form-group">
                  <label class="form-label">
                    <Calendar :size="14" />
                    Tarih
                  </label>
                  <input
                    v-model="form.date"
                    type="date"
                    class="form-input"
                    :min="today"
                    required
                  />
                </div>
                <div class="form-group">
                  <label class="form-label">
                    <Clock :size="14" />
                    Saat
                  </label>
                  <input
                    v-model="form.time"
                    type="time"
                    class="form-input"
                    required
                  />
                </div>
              </div>

              <!-- Notes -->
              <div class="form-group">
                <label class="form-label">
                  <FileText :size="14" />
                  Notlar <span class="optional">(isteğe bağlı)</span>
                </label>
                <textarea
                  v-model="form.notes"
                  class="form-textarea"
                  rows="3"
                  placeholder="Randevu hakkında notlar ekleyin..."
                ></textarea>
              </div>

              <!-- Status Message -->
              <Transition name="status-fade">
                <div v-if="statusMsg" :class="['status-msg', statusType]">
                  <CheckCircle v-if="statusType === 'success'" :size="16" />
                  <AlertCircle v-else :size="16" />
                  {{ statusMsg }}
                </div>
              </Transition>

              <!-- Actions -->
              <div class="modal-actions">
                <button type="button" class="btn-cancel" @click="close">
                  İptal
                </button>
                <button type="submit" class="btn-submit" :disabled="submitting">
                  <Loader2 v-if="submitting" :size="16" class="spin" />
                  <CalendarPlus v-else :size="16" />
                  {{ submitting ? 'Kaydediliyor...' : 'Randevu Oluştur' }}
                </button>
              </div>
            </form>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, inject } from 'vue'
import { CalendarPlus, X, Calendar, Clock, Tag, FileText, Loader2, CheckCircle, AlertCircle } from 'lucide-vue-next'
import { useSectorStore } from '@/stores/sector'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  serviceOptions: {
    type: Array,
    default: () => [
      'Genel Danışma',
      'Kontrol Randevusu',
      'Uzman Görüşmesi',
      'Cilt Bakımı',
      'Saç Kesim',
      'Masaj Terapisi',
      'Manikür & Pedikür',
      'Kalıcı Makyaj',
      'Diğer'
    ]
  }
})

const emit = defineEmits(['update:modelValue', 'created'])
const axios = inject('axios')
const sectorStore = useSectorStore()

const form = ref({
  service: '',
  date: '',
  time: '',
  notes: ''
})

const submitting = ref(false)
const statusMsg = ref('')
const statusType = ref('success')

const today = computed(() => new Date().toISOString().split('T')[0])

const close = () => {
  if (submitting.value) return
  emit('update:modelValue', false)
  // Reset form after close
  setTimeout(() => {
    form.value = { service: '', date: '', time: '', notes: '' }
    statusMsg.value = ''
  }, 300)
}

const submit = async () => {
  if (submitting.value) return
  submitting.value = true
  statusMsg.value = ''

  try {
    const startTime = new Date(`${form.value.date}T${form.value.time}:00`).toISOString()
    const payload = {
      title: form.value.service,
      service: form.value.service,
      start_time: startTime,
      notes: form.value.notes,
      sector: sectorStore.currentSectorId || 'beauty',
      status: 'pending'
    }

    // Try portal endpoint first, fallback to interactions
    try {
      await axios.post('/portal/appointments', payload)
    } catch {
      await axios.post('/interactions', {
        ...payload,
        type: form.value.service,
        client_name: 'Müşteri'
      })
    }

    statusType.value = 'success'
    statusMsg.value = 'Randevunuz başarıyla oluşturuldu!'
    emit('created')

    // Auto close after success
    setTimeout(() => {
      close()
    }, 1500)
  } catch (e) {
    statusType.value = 'error'
    statusMsg.value = 'Randevu oluşturulurken bir hata oluştu. Lütfen tekrar deneyin.'
    console.error('Appointment create error:', e)
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 16px;
}

.modal-box {
  background: #0d0d14;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(255,255,255,0.06);
  overflow: hidden;
}

/* Header */
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 24px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.modal-title-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.modal-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--current-accent, #6366f1), #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 0 16px var(--current-glow, rgba(99, 102, 241, 0.3));
}

.modal-header h2 {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary, #fff);
  margin: 0;
}

.close-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: #6b7280;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

/* Form */
.modal-form {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-label {
  font-size: 13px;
  font-weight: 600;
  color: #9ca3af;
  display: flex;
  align-items: center;
  gap: 6px;
}

.optional {
  font-weight: 400;
  color: #52525b;
}

.form-input,
.form-select,
.form-textarea {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 10px 14px;
  color: white;
  font-size: 14px;
  transition: all 0.2s;
  outline: none;
  font-family: inherit;
  width: 100%;
}

.form-select {
  cursor: pointer;
  appearance: none;
  -webkit-appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='none' viewBox='0 0 24 24' stroke='%236b7280'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 36px;
}

.form-select option {
  background: #1a1a2e;
  color: white;
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  border-color: var(--current-accent, #6366f1);
  box-shadow: 0 0 0 3px var(--current-glow, rgba(99, 102, 241, 0.15));
  background: rgba(255, 255, 255, 0.06);
}

/* Date/time native picker color fix */
input[type="date"]::-webkit-calendar-picker-indicator,
input[type="time"]::-webkit-calendar-picker-indicator {
  filter: invert(0.6);
  cursor: pointer;
}

/* Status */
.status-msg {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 500;
}

.status-msg.success {
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.25);
  color: #34d399;
}

.status-msg.error {
  background: rgba(239, 68, 68, 0.12);
  border: 1px solid rgba(239, 68, 68, 0.25);
  color: #f87171;
}

/* Actions */
.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding-top: 4px;
}

.btn-cancel {
  padding: 10px 20px;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  color: #9ca3af;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel:hover {
  background: rgba(255, 255, 255, 0.05);
  color: white;
}

.btn-submit {
  padding: 10px 24px;
  background: linear-gradient(135deg, var(--current-accent, #6366f1), #8b5cf6);
  border: none;
  border-radius: 10px;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
  box-shadow: 0 4px 12px var(--current-glow, rgba(99, 102, 241, 0.3));
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px var(--current-glow, rgba(99, 102, 241, 0.4));
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Transitions */
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.25s ease;
}
.modal-fade-enter-from, .modal-fade-leave-to {
  opacity: 0;
}

.modal-slide-enter-active, .modal-slide-leave-active {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.modal-slide-enter-from {
  opacity: 0;
  transform: scale(0.92) translateY(20px);
}
.modal-slide-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(10px);
}

.status-fade-enter-active, .status-fade-leave-active {
  transition: all 0.2s ease;
}
.status-fade-enter-from, .status-fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
