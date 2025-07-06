<template>
  <div class="scenario-form">
    <div class="form-header">
      <h2 class="form-title">
        <i class="pi pi-magic" style="margin-right: 0.5rem; color: var(--primary-color);"></i>
        Generate Scenario
      </h2>
      <p class="form-subtitle">Configure your cybersecurity tabletop exercise parameters</p>
    </div>
    
    <div style="position: relative;">
      <div v-if="dropdownOpen" class="dropdown-overlay" @click="closeDropdown"></div>
      <div class="form-grid">
        <div class="field">
          <label for="company">Company Name</label>
          <InputText 
            id="company" 
            v-model="form.company_name" 
            placeholder="Enter company name"
            class="form-input"
          />
        </div>
        
        <div class="field">
          <label for="industry">Industry</label>
          <InputText 
            id="industry" 
            v-model="form.industry" 
            placeholder="e.g., Healthcare, Finance, Technology"
            class="form-input"
          />
        </div>
        
        <div class="field dropdown-spacing">
          <label for="size">Company Size</label>
          <Dropdown
            id="size"
            v-model="form.company_size"
            :options="sizeOptions"
            appendTo="body"
            placeholder="Select company size"
            class="form-dropdown"
          />
        </div>
        
        <div class="field dropdown-spacing">
          <label for="threat">Threat Actor</label>
          <Dropdown
            id="threat"
            v-model="form.threat_actor"
            :options="threatOptions"
            appendTo="body"
            placeholder="Select threat actor type"
            class="form-dropdown"
          />
        </div>
        
        <div class="field dropdown-spacing">
          <label for="provider">AI Provider</label>
          <Dropdown
            id="provider"
            v-model="form.llm_provider"
            :options="availableProviders"
            :loading="loadingProviders"
            appendTo="body"
            placeholder="Select AI Provider"
            class="form-dropdown"
          />
        </div>
        
        <div class="field">
          <label for="duration">Duration (hours)</label>
          <InputNumber 
            id="duration" 
            v-model="form.duration_hours" 
            :min="1" 
            :max="8" 
            :show-buttons="true"
            class="form-input"
          />
        </div>
      </div>
      <div class="form-actions">
        <Button 
          @click="generateScenario" 
          :loading="props.generating" 
          label="Generate Scenario"
          icon="pi pi-sparkles"
          :disabled="props.generating || !isFormValid"
          class="generate-button"
        />
        
        <div class="form-status">
          <div class="status-indicator" :class="{ valid: isFormValid }">
            <i :class="isFormValid ? 'pi pi-check-circle' : 'pi pi-exclamation-circle'"></i>
            <span>{{ isFormValid ? 'Form is ready' : 'Please fill all required fields' }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Dropdown from 'primevue/dropdown'
import Button from 'primevue/button'

const emit = defineEmits(['scenario-generated'])

const props = defineProps({
  generating: {
    type: Boolean,
    default: false
  }
})

const loadingProviders = ref(true)
const availableProviders = ref([])

const form = ref({
  company_name: '',
  industry: '',
  company_size: 'medium',
  threat_actor: 'ransomware',
  scenario_type: 'ransomware',
  duration_hours: 2,
  technologies: [],
  participants: ['Security Team', 'IT Team'],
  llm_provider: null
})

const sizeOptions = ['small', 'medium', 'large', 'enterprise']
const threatOptions = ['apt', 'ransomware', 'insider', 'hacktivist', 'cybercriminal']

const dropdownOpen = ref(false)
const openDropdownRef = ref(null)
const companyDropdown = ref(null)
const threatDropdown = ref(null)
const providerDropdown = ref(null)
const openDropdownType = ref(null)

const isFormValid = computed(() => {
  const valid = form.value.company_name.trim() && 
                form.value.industry.trim() && 
                form.value.company_size && 
                form.value.threat_actor
  console.log('Form validation:', {
    company_name: form.value.company_name.trim(),
    industry: form.value.industry.trim(),
    company_size: form.value.company_size,
    threat_actor: form.value.threat_actor,
    isValid: valid
  })
  return valid
})

onMounted(async () => {
  try {
    const response = await axios.get('/api/scenarios/providers')
    availableProviders.value = response.data.providers
    if (availableProviders.value.length > 0) {
      form.value.llm_provider = availableProviders.value[0]
    }
  } catch (error) {
    console.error('Failed to load providers:', error)
  } finally {
    loadingProviders.value = false
  }
})

const generateScenario = async () => {
  if (!isFormValid.value) return
  emit('scenario-generated', form.value)
}

function onDropdownShow(type) {
  dropdownOpen.value = true
  openDropdownType.value = type
  if (type === 'company') openDropdownRef.value = companyDropdown
  else if (type === 'threat') openDropdownRef.value = threatDropdown
  else if (type === 'provider') openDropdownRef.value = providerDropdown
}
function onDropdownHide() {
  dropdownOpen.value = false
  openDropdownType.value = null
  openDropdownRef.value = null
}
function closeDropdown() {
  if (openDropdownRef.value && openDropdownRef.value.value) {
    openDropdownRef.value.value.hide()
  }
}
</script>

<style scoped>
.scenario-form {
  padding: 2rem;
  background: var(--surface-card);
  border-radius: 16px;
  border: 1px solid var(--surface-border);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
  transition: all 0.3s ease;
  position: relative;
  z-index: 1;
  isolation: isolate;
}

.scenario-form:hover {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}

.form-header {
  margin-bottom: 2rem;
  text-align: center;
}

.form-title {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: 1.75rem;
  margin: 0 0 0.5rem 0;
  color: var(--text-color);
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-subtitle {
  font-family: 'Inter', sans-serif;
  font-size: 1rem;
  color: var(--text-color-secondary);
  margin: 0;
  opacity: 0.9;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  position: relative;
  z-index: 1;
}

.field:focus-within {
  z-index: 1000;
}

label {
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 0.875rem;
  color: var(--text-color);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-input,
.form-dropdown {
  font-family: 'Inter', sans-serif;
  border-radius: 8px;
  border: 2px solid var(--surface-border);
  transition: all 0.3s ease;
  background: var(--surface-ground);
  color: var(--text-color);
}

.form-input:focus,
.form-dropdown:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(var(--primary-color-rgb), 0.1);
  outline: none;
}

.form-input:hover,
.form-dropdown:hover {
  border-color: var(--primary-color);
}

/* Fix dropdown z-index - more aggressive approach */
:deep(.p-dropdown-panel) {
  z-index: 99999 !important;
  position: fixed !important;
  transform: none !important;
}

:deep(.p-dropdown-panel .p-dropdown-list) {
  z-index: 99999 !important;
}

:deep(.p-dropdown-panel .p-dropdown-item) {
  z-index: 99999 !important;
  position: relative !important;
}

.form-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
  position: relative;
  z-index: 1;
  margin-top: 2rem;
}

.generate-button {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-600) 100%);
  border: none;
  padding: 1rem 2rem;
  font-size: 1.125rem;
  font-weight: 600;
  border-radius: 12px;
  min-width: 200px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(var(--primary-color-rgb), 0.3);
}

.generate-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(var(--primary-color-rgb), 0.4);
}

.generate-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.form-status {
  display: flex;
  justify-content: center;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-family: 'Inter', sans-serif;
  font-size: 0.875rem;
  font-weight: 500;
  background: var(--surface-section);
  border: 1px solid var(--surface-border);
  color: var(--text-color-secondary);
  transition: all 0.3s ease;
}

.status-indicator.valid {
  background: rgba(76, 175, 80, 0.1);
  border-color: rgba(76, 175, 80, 0.3);
  color: #4caf50;
}

.status-indicator i {
  font-size: 1rem;
}

/* Responsive design */
@media (max-width: 768px) {
  .scenario-form {
    padding: 1.5rem;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .form-title {
    font-size: 1.5rem;
  }
  
  .generate-button {
    width: 100%;
    min-width: auto;
  }
}

/* Dark mode adjustments */
:root.dark-mode .form-input,
:root.dark-mode .form-dropdown {
  background: var(--surface-ground);
  color: var(--text-color);
}

:root.dark-mode .status-indicator {
  background: var(--surface-section);
  border-color: var(--surface-border);
}

/* Additional safety for dropdown positioning */
:deep(.p-dropdown-panel) {
  pointer-events: auto !important;
  position: fixed !important;
  z-index: 999999 !important;
}

/* Force dropdown to be on top */
:deep(.p-dropdown:focus-within .p-dropdown-panel) {
  z-index: 999999 !important;
  position: fixed !important;
}

/* Add more spacing between form sections */
.form-section {
  margin-bottom: 3rem;
  position: relative;
  z-index: 1;
}

/* GLOBAL: Force PrimeVue dropdown panel to fixed and high z-index */
:global(.p-dropdown-panel) {
  position: fixed !important;
  z-index: 2147483647 !important;
  left: var(--p-dropdown-left, auto) !important;
  top: var(--p-dropdown-top, auto) !important;
  width: auto !important;
  min-width: 180px !important;
  max-width: 100vw !important;
  max-height: 60vh !important;
  overflow-y: auto !important;
}

.dropdown-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.85);
  z-index: 2147483646;
  transition: background 0.2s;
}

.dropdown-overlay-local {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.85);
  z-index: 10;
  border-radius: 6px;
  transition: background 0.2s;
}

.dropdown-spacing {
  margin-bottom: 3.5rem !important;
}
</style>


