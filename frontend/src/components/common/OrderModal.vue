<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div v-if="modelValue" class="modal-overlay" @click.self="close">
        <Transition name="modal-slide">
          <div v-if="modelValue" class="modal-box" role="dialog" aria-modal="true" aria-labelledby="order-modal-title">
            <div class="modal-header">
              <div class="modal-title-row">
                <div class="modal-icon">
                  <Package :size="20" :stroke-width="2" />
                </div>
                <h2 id="order-modal-title">Yeni Sipariş Oluştur</h2>
              </div>
              <button class="close-btn" @click="close" aria-label="Kapat">
                <X :size="20" :stroke-width="2" />
              </button>
            </div>

            <form @submit.prevent="submit" class="modal-form">
              <div class="form-group">
                <label class="form-label">
                  <User :size="14" />
                  Müşteri Adı
                </label>
                <input v-model="form.customerName" type="text" class="form-input" placeholder="Müşteri adı girin" required />
              </div>

              <div class="form-group">
                <label class="form-label">
                  <Package :size="14" />
                  Ürün
                </label>
                <select v-model="form.product" class="form-select" required>
                  <option value="" disabled>Ürün seçin...</option>
                  <option v-for="p in productOptions" :key="p" :value="p">{{ p }}</option>
                </select>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label class="form-label">
                    <ShoppingCart :size="14" />
                    Adet
                  </label>
                  <input v-model.number="form.quantity" type="number" class="form-input" min="1" required />
                </div>
                <div class="form-group">
                  <label class="form-label">
                    <DollarSign :size="14" />
                    Tutar (₺)
                  </label>
                  <input v-model.number="form.amount" type="number" class="form-input" min="0" step="0.01" placeholder="0.00" />
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">
                  <FileText :size="14" />
                  Not <span class="optional">(isteğe bağlı)</span>
                </label>
                <textarea v-model="form.notes" class="form-textarea" rows="2" placeholder="Sipariş notu..."></textarea>
              </div>

              <Transition name="status-fade">
                <div v-if="statusMsg" :class="['status-msg', statusType]">
                  <CheckCircle v-if="statusType === 'success'" :size="16" />
                  <AlertCircle v-else :size="16" />
                  {{ statusMsg }}
                </div>
              </Transition>

              <div class="modal-actions">
                <button type="button" class="btn-cancel" @click="close">İptal</button>
                <button type="submit" class="btn-submit" :disabled="submitting">
                  <Loader2 v-if="submitting" :size="16" class="spin" />
                  <Package v-else :size="16" />
                  {{ submitting ? 'Kaydediliyor...' : 'Sipariş Oluştur' }}
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
import { ref } from 'vue'
import { Package, X, User, ShoppingCart, DollarSign, FileText, Loader2, CheckCircle, AlertCircle } from 'lucide-vue-next'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  productOptions: {
    type: Array,
    default: () => [
      'Premium Kulaklık',
      'Akıllı Saat',
      'Kablosuz Mouse',
      'Mekanik Klavye',
      'USB Hub',
      'Webcam',
      'Diğer'
    ]
  }
})

const emit = defineEmits(['update:modelValue', 'created'])

const form = ref({
  customerName: '',
  product: '',
  quantity: 1,
  amount: '',
  notes: ''
})

const submitting = ref(false)
const statusMsg = ref('')
const statusType = ref('success')

const close = () => {
  if (submitting.value) return
  emit('update:modelValue', false)
  setTimeout(() => {
    form.value = { customerName: '', product: '', quantity: 1, amount: '', notes: '' }
    statusMsg.value = ''
  }, 300)
}

const submit = async () => {
  if (submitting.value) return
  submitting.value = true
  statusMsg.value = ''

  try {
    // Simulate API call - replace with actual endpoint when backend ready
    await new Promise(resolve => setTimeout(resolve, 800))
    statusType.value = 'success'
    statusMsg.value = 'Sipariş başarıyla oluşturuldu!'
    emit('created')
    setTimeout(() => close(), 1500)
  } catch (e) {
    statusType.value = 'error'
    statusMsg.value = 'Sipariş oluşturulurken hata oluştu.'
    console.error(e)
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
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 20px;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(139, 92, 246, 0.1);
  overflow: hidden;
}

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
  background: linear-gradient(135deg, #8b5cf6, #a78bfa);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 0 16px rgba(139, 92, 246, 0.4);
}

.modal-header h2 {
  font-size: 18px;
  font-weight: 700;
  color: #fff;
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

.optional { font-weight: 400; color: #52525b; }

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

.form-select option { background: #1a1a2e; color: white; }

.form-textarea { resize: vertical; min-height: 60px; }

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2);
  background: rgba(255, 255, 255, 0.06);
}

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
  background: linear-gradient(135deg, #8b5cf6, #a78bfa);
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
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(139, 92, 246, 0.4);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spin { animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.25s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }

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

.status-fade-enter-active, .status-fade-leave-active { transition: all 0.2s ease; }
.status-fade-enter-from, .status-fade-leave-to { opacity: 0; transform: translateY(-4px); }
</style>
