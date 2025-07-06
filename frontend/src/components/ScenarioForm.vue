<template>
  <div class="scenario-form">
    <h2>Generate Scenario</h2>
    
    <div class="form-grid">
      <div class="field">
        <label for="company">Company Name</label>
        <InputText 
          id="company" 
          v-model="form.company_name" 
          placeholder="Enter company name"
        />
      </div>
      
      <div class="field">
        <label for="industry">Industry</label>
        <InputText 
          id="industry" 
          v-model="form.industry" 
          placeholder="e.g., Healthcare, Finance, Technology"
        />
      </div>
      
      <div class="field">
        <label for="size">Company Size</label>
        <Dropdown 
          id="size" 
          v-model="form.company_size" 
          :options="sizeOptions" 
          placeholder="Select company size"
        />
      </div>
      
      <div class="field">
        <label for="threat">Threat Actor</label>
        <Dropdown 
          id="threat" 
          v-model="form.threat_actor" 
          :options="threatOptions" 
          placeholder="Select threat actor type"
        />
      </div>
      
      <div class="field">
        <label for="provider">AI Provider</label>
        <Dropdown 
          id="provider" 
          v-model="form.llm_provider" 
          :options="availableProviders"
          :loading="loadingProviders"
          placeholder="Select AI Provider"
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
        />
      </div>
    </div>
    
    <Button 
      @click="generateScenario" 
      :loading="props.generating" 
      label="Generate Scenario"
      icon="pi pi-sparkles"
      :disabled="props.generating"
      class="generate-button"
    />
    
    <!-- Debug info -->
    <div style="margin-top: 1rem; font-size: 0.8rem; color: var(--text-color-secondary);">
      Form valid: {{ isFormValid }} | Generating: {{ props.generating }}
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
</script>

<style scoped>
.scenario-form {
  padding: 2rem;
  background: var(--surface-card);
  border-radius: 10px;
  border: 1px solid var(--surface-border);
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 2rem;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-weight: bold;
  color: var(--text-color-secondary);
}

.generate-button {
  width: 100%;
  padding: 1rem;
  font-size: 1.1rem;
  margin-top: 1rem;
}
</style>


