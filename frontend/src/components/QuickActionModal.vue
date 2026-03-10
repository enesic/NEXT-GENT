<template>
  <Transition name="modal-fade">
    <div v-if="visible" class="modal-overlay" @click.self="close">
      <div class="modal-container" :style="{ '--accent': resolvedAccent }">
        <!-- Header -->
        <div class="modal-header">
          <div class="modal-title-group">
            <div class="modal-icon">
              <component :is="iconComponent" :size="20" :stroke-width="2" />
            </div>
            <h2>{{ tLoc(resolvedTitle) }}</h2>
          </div>
          <button class="close-btn" @click="close">
            <X :size="20" :stroke-width="2" />
          </button>
        </div>

        <!-- Form Content -->
        <div class="modal-body">
          <div v-for="(field, index) in resolvedFields" :key="index" class="form-group">
            <label>{{ tLoc(field.label) }}</label>
            <input
              v-if="field.type === 'text' || field.type === 'email' || field.type === 'tel' || field.type === 'number'"
              v-model="formData[field.key]"
              :type="field.type"
              :placeholder="tLoc(field.placeholder)"
              class="form-input"
            />
            <textarea
              v-else-if="field.type === 'textarea'"
              v-model="formData[field.key]"
              :placeholder="tLoc(field.placeholder)"
              class="form-textarea"
              rows="3"
            ></textarea>
            <select
              v-else-if="field.type === 'select'"
              v-model="formData[field.key]"
              class="form-select"
            >
              <option value="" disabled>{{ tLoc(field.placeholder) }}</option>
              <option v-for="opt in field.options" :key="opt.value" :value="opt.value">
                {{ tLoc(opt.label) }}
              </option>
            </select>
            <input
              v-else-if="field.type === 'date' || field.type === 'datetime-local'"
              v-model="formData[field.key]"
              :type="field.type"
              class="form-input"
            />
          </div>
        </div>

        <!-- Footer -->
        <div class="modal-footer">
          <button class="btn-cancel" @click="close">{{ t('cancel') }}</button>
          <button class="btn-submit" @click="handleSubmit" :disabled="submitting">
            <span v-if="submitting" class="spinner-small"></span>
            {{ submitting ? t('processing') : tLoc(resolvedSubmitLabel) }}
          </button>
        </div>

        <!-- Success State -->
        <Transition name="success-fade">
          <div v-if="showSuccess" class="success-overlay">
            <div class="success-icon">✓</div>
            <p>{{ tLoc(resolvedSuccessMessage) }}</p>
          </div>
        </Transition>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { X, CalendarPlus, UserPlus, FileText, Activity, ShoppingCart, Package, Truck, Tag } from 'lucide-vue-next'
import { useSectorStore } from '../stores/sector'

const props = defineProps({
  // v-model support
  modelValue: { type: Boolean, default: false },
  // action object (used by PortalDashboard)
  action: { type: Object, default: null },
  // fallback individual props
  title: { type: String, default: 'İşlem' },
  icon: { type: String, default: 'CalendarPlus' },
  fields: { type: Array, default: () => [] },
  submitLabel: { type: String, default: 'Kaydet' },
  successMessage: { type: String, default: 'İşlem başarıyla kaydedildi!' },
  accentColor: { type: String, default: '' }
})

const emit = defineEmits(['update:modelValue', 'submit'])

const sectorStore = useSectorStore()
const t = (key) => sectorStore.t(key)
const tLoc = (obj) => sectorStore.tLoc(obj)

// Resolve values from action prop (priority) or individual props
const resolvedTitle = computed(() => props.action?.label || props.title)
const resolvedIcon = computed(() => props.action?.icon || props.icon)
const resolvedFields = computed(() => props.action?.fields || props.fields)
const resolvedSubmitLabel = computed(() => props.action?.submitLabel || props.submitLabel)
const resolvedSuccessMessage = computed(() => props.action?.successMessage || props.successMessage)
const resolvedAccent = computed(() => props.accentColor || sectorStore.theme?.primary || '#6366f1')

// Visibility: support both v-model and visible prop
const visible = computed(() => props.modelValue)

const formData = reactive({})
const submitting = ref(false)
const showSuccess = ref(false)

const iconMap = {
  CalendarPlus, UserPlus, FileText, Activity, ShoppingCart, Package, Truck, Tag, X
}
const iconComponent = computed(() => iconMap[resolvedIcon.value] || CalendarPlus)

// Initialize/reset form data when fields change
watch(resolvedFields, (newFields) => {
  // Clear old keys
  Object.keys(formData).forEach(k => delete formData[k])
  // Init new keys
  newFields.forEach(field => {
    formData[field.key] = field.default || ''
  })
}, { immediate: true })

const close = () => {
  showSuccess.value = false
  emit('update:modelValue', false)
}

const handleSubmit = async () => {
  submitting.value = true
  await new Promise(resolve => setTimeout(resolve, 800))
  submitting.value = false
  showSuccess.value = true
  emit('submit', { ...formData })
  setTimeout(() => {
    Object.keys(formData).forEach(key => { formData[key] = '' })
    close()
  }, 1500)
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-container {
  width: 480px;
  max-width: 90vw;
  max-height: 85vh;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.2), 0 0 0 1px var(--border-subtle) inset;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-subtle);
}

.modal-title-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.modal-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: color-mix(in srgb, var(--accent) 15%, transparent);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
}

.modal-header h2 {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.close-btn {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: #a1a1aa;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.15);
  color: #f4f4f5;
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  letter-spacing: 0.02em;
}

.form-input,
.form-textarea,
.form-select {
  width: 100%;
  padding: 12px 14px;
  background: var(--bg-main);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  color: var(--text-primary);
  font-size: 14px;
  outline: none;
  transition: all 0.2s;
  box-sizing: border-box;
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  border-color: var(--accent);
  background: rgba(255, 255, 255, 0.06);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 15%, transparent);
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: #52525b;
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.form-select option {
  background: #18181b;
  color: #f4f4f5;
}

.modal-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding: 16px 24px;
  border-top: 1px solid var(--border-subtle);
}

.btn-cancel {
  padding: 10px 20px;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  color: #a1a1aa;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #f4f4f5;
}

.btn-submit {
  padding: 10px 24px;
  background: var(--accent);
  border: none;
  border-radius: 10px;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 16px color-mix(in srgb, var(--accent) 40%, transparent);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Success Overlay */
.success-overlay {
  position: absolute;
  inset: 0;
  background: var(--bg-surface);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  z-index: 10;
}

.success-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: 700;
  box-shadow: 0 0 24px rgba(16, 185, 129, 0.3);
}

.success-overlay p {
  font-size: 16px;
  font-weight: 500;
  color: var(--text-primary);
}

/* Transitions */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-fade-enter-active .modal-container,
.modal-fade-leave-active .modal-container {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-fade-enter-from {
  opacity: 0;
}

.modal-fade-enter-from .modal-container {
  transform: translateY(20px) scale(0.96);
}

.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-leave-to .modal-container {
  transform: translateY(20px) scale(0.96);
}

.success-fade-enter-active,
.success-fade-leave-active {
  transition: all 0.3s;
}

.success-fade-enter-from,
.success-fade-leave-to {
  opacity: 0;
  transform: scale(0.9);
}
</style>
