<template>
  <div class="threat-model-upload">
    <div class="threat-model-header cyber-card">
      <div class="header-content">
        <div class="title-section">
          <h2>
            <i class="pi pi-shield" style="margin-right: 0.5rem; color: var(--primary-color);"></i>
            AI-Powered Threat Modeling
          </h2>
          <p>Generate comprehensive threat models using advanced AI analysis</p>
        </div>
        <div class="header-actions">
          <Button 
            icon="pi pi-question-circle" 
            label="Tutorial"
            @click="showTutorial = true"
            severity="secondary"
            outlined
          />
        </div>
      </div>
    </div>
    
    <!-- Threat Model Form -->
    <div class="threat-model-form cyber-card">
      <div class="form-header">
        <h3>
          <i class="pi pi-shield" style="margin-right: 0.5rem; color: var(--primary-color);"></i>
          Threat Modeling Analysis
        </h3>
        <p>Describe your system or select an uploaded diagram for AI-powered threat modeling</p>
      </div>
      
      <div class="form-grid">
        <div class="field">
          <label for="content">System Description</label>
          <Textarea 
            id="content" 
            v-model="form.content" 
            placeholder="Describe the system, architecture, or components you want to analyze for threats..."
            rows="6"
            class="form-textarea"
          />
        </div>
        
        <div class="field">
          <label for="framework">Framework</label>
          <Dropdown
            id="framework"
            v-model="form.framework"
            :options="frameworkOptions"
            optionLabel="label"
            optionValue="value"
            placeholder="Select framework"
            class="form-dropdown"
          />
        </div>
        
        <div class="field">
          <label for="file">Uploaded File (Optional)</label>
          <Dropdown
            id="file"
            v-model="form.file_id"
            :options="fileOptions"
            optionLabel="label"
            optionValue="value"
            placeholder="Select uploaded file (optional)"
            class="form-dropdown"
            :disabled="!files.length"
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
            class="form-dropdown"
          />
        </div>
      </div>
      
      <div class="form-actions">
        <div class="generation-mode">
          <label class="mode-toggle">
            <input 
              type="checkbox" 
              v-model="useAsyncMode"
              class="mode-checkbox"
            />
            <span class="mode-label">
              <i class="pi" :class="useAsyncMode ? 'pi-clock' : 'pi-bolt'"></i>
              {{ useAsyncMode ? 'Async Mode' : 'Sync Mode' }}
            </span>
          </label>
          <span class="mode-description">
            {{ useAsyncMode ? 'Generate in background with progress tracking' : 'Generate immediately and wait for result' }}
          </span>
        </div>
        
        <div class="action-buttons">
          <Button 
            @click="generateThreatModel" 
            :loading="generating" 
            :label="useAsyncMode ? 'Create Async Job' : 'Generate Threat Model'"
            :icon="useAsyncMode ? 'pi-clock' : 'pi-shield'"
            :disabled="generating || !isFormValid"
            class="generate-button"
          />
          <Button 
            @click="compareCosts"
            label="Compare Costs"
            icon="pi pi-dollar"
            class="compare-costs-btn"
            severity="secondary"
          />
        </div>
        
        <div class="form-status">
          <div class="status-indicator" :class="{ valid: isFormValid }">
            <i :class="isFormValid ? 'pi pi-check-circle' : 'pi pi-exclamation-circle'"></i>
            <span>{{ isFormValid ? 'Form is ready' : 'Please provide system description' }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- File Upload Section -->
    <div class="file-upload-section cyber-card">
      <h3>Upload Diagram Files</h3>
      <form @submit.prevent="handleUpload">
        <div class="drop-area" @dragover.prevent @drop.prevent="onDrop" @click="fileInput.click()">
          <input type="file" ref="fileInput" @change="onFileChange" :accept="acceptTypes" multiple style="display:none;" />
          <span v-if="!selectedFiles.length">Drag & drop files here or click to select</span>
          <ul v-else>
            <li v-for="file in selectedFiles" :key="file.name + file.size">
              {{ file.name }} ({{ formatSize(file.size) }})
              <span v-if="uploadProgress[file.name] !== undefined">
                <ProgressBar :value="uploadProgress[file.name]" style="width:100px; margin-left:1rem;" />
              </span>
            </li>
          </ul>
        </div>
        <Button type="submit" label="Upload" :disabled="!selectedFiles.length || uploading" class="upload-btn" icon="pi pi-upload" />
        <span v-if="error" class="error">{{ error }}</span>
      </form>
      
      <div v-if="files.length > 0" class="bulk-actions">
        <Button label="Delete Selected" icon="pi pi-trash" severity="danger" class="bulk-delete-btn" :disabled="!selectedToDelete.length" @click="bulkDelete" />
      </div>
      
      <ul v-if="files.length > 0" class="file-list">
        <li v-for="file in files" :key="file.file_id" class="file-item">
          <input type="checkbox" v-model="selectedToDelete" :value="file.file_id" />
          <span>{{ file.filename }} ({{ file.file_type.toUpperCase() }}, {{ formatSize(file.size) }})</span>
          <Button icon="pi pi-trash" severity="danger" @click="deleteFile(file.file_id)" class="delete-btn" />
        </li>
      </ul>
      <div v-else-if="!uploading" style="color:#a7f6ff; opacity:0.7;">No files uploaded yet.</div>
    </div>
    
    <!-- Threat Model Results -->
    <div v-if="currentThreatModel" class="threat-model-results cyber-card">
      <ThreatModelDisplay 
        :threatModel="currentThreatModel"
        :formData="form"
        @regenerate="regenerate"
      />
    </div>

    <!-- Job Monitor -->
    <div class="job-monitor-section cyber-card">
      <JobMonitor @view-result="handleJobResult" />
    </div>

    <!-- Cost Comparison Dialog -->
    <CostComparison
      v-model:visible="showCostDialog"
      :estimates="costEstimates"
      :loading="loadingCosts"
      :selectedProvider="form.llm_provider"
      @select-provider="selectProvider"
    />

    <!-- Tutorial Modal -->
    <ThreatModelTutorial 
      :showTutorial="showTutorial"
      @close="showTutorial = false"
      @start-modeling="handleStartModeling"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import Button from 'primevue/button'
import ProgressSpinner from 'primevue/progressspinner'
import ProgressBar from 'primevue/progressbar'
import Dropdown from 'primevue/dropdown'
import Textarea from 'primevue/textarea'
import { useToast } from 'primevue/usetoast'
import CostComparison from './CostComparison.vue'
import ThreatModelDisplay from './ThreatModelDisplay.vue'
import JobMonitor from './JobMonitor.vue'
import ThreatModelTutorial from './ThreatModelTutorial.vue'

const toast = useToast()

const form = ref({
  content: '',
  framework: 'STRIDE',
  file_id: null,
  llm_provider: null
})

const files = ref([])
const selectedFiles = ref([])
const uploadProgress = ref({})
const selectedToDelete = ref([])
const uploading = ref(false)
const error = ref(null)
const fileInput = ref(null)
const acceptTypes = '.drawio,.png,.jpg,.svg,.xml'

const loadingProviders = ref(true)
const availableProviders = ref([])
const generating = ref(false)
const currentThreatModel = ref(null)
const showCostDialog = ref(false)
const costEstimates = ref([])
const loadingCosts = ref(false)

// Async generation mode
const useAsyncMode = ref(false)

// Tutorial state
const showTutorial = ref(false)

const frameworkOptions = [
  { label: 'STRIDE', value: 'STRIDE' },
  { label: 'LINDDUN', value: 'LINDDUN' },
  { label: 'PASTA', value: 'PASTA' },
  { label: 'Attack Trees', value: 'ATTACK_TREES' }
]

const isFormValid = computed(() => {
  return form.value.content.trim().length > 0
})

const fileOptions = computed(() => {
  return files.value.map(file => ({
    label: `${file.filename} (${file.file_type.toUpperCase()})`,
    value: file.file_id
  }))
})

async function fetchFiles() {
  try {
    const response = await axios.get('/api/threat-model/files')
    files.value = response.data
  } catch (error) {
    console.error('Failed to fetch files:', error)
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to load uploaded files',
      life: 3000
    })
  }
}

async function handleUpload() {
  if (!selectedFiles.value.length) return
  
  uploading.value = true
  error.value = null
  
  try {
    for (const file of selectedFiles.value) {
      const formData = new FormData()
      formData.append('file', file)
      
      uploadProgress.value[file.name] = 0
      
      await axios.post('/api/threat-model/upload', formData, {
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            uploadProgress.value[file.name] = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            )
          }
        }
      })
    }
    
    await fetchFiles()
    selectedFiles.value = []
    uploadProgress.value = {}
    
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'Files uploaded successfully',
      life: 3000
    })
  } catch (error) {
    console.error('Upload failed:', error)
    error.value = error.response?.data?.detail || 'Upload failed'
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: error.value,
      life: 3000
    })
  } finally {
    uploading.value = false
  }
}

function onFileChange(event) {
  selectedFiles.value = Array.from(event.target.files)
}

function onDrop(event) {
  event.preventDefault()
  selectedFiles.value = Array.from(event.dataTransfer.files)
}

function formatSize(bytes) {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

async function deleteFile(fileId) {
  try {
    await axios.delete(`/api/threat-model/files/${fileId}`)
    await fetchFiles()
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'File deleted successfully',
      life: 3000
    })
  } catch (error) {
    console.error('Delete failed:', error)
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to delete file',
      life: 3000
    })
  }
}

async function bulkDelete() {
  if (!selectedToDelete.value.length) return
  
  try {
    for (const fileId of selectedToDelete.value) {
      await axios.delete(`/api/threat-model/files/${fileId}`)
    }
    await fetchFiles()
    selectedToDelete.value = []
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'Files deleted successfully',
      life: 3000
    })
  } catch (error) {
    console.error('Bulk delete failed:', error)
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to delete some files',
      life: 3000
    })
  }
}

async function generateThreatModel() {
  if (!isFormValid.value) return
  
  generating.value = true
  error.value = null
  
  try {
    if (useAsyncMode.value) {
      // Use async generation
      const response = await axios.post('/api/threat-model/generate-async', {
        content: form.value.content,
        framework: form.value.framework,
        file_id: form.value.file_id,
        llm_provider: form.value.llm_provider
      })
      
      toast.add({
        severity: 'success',
        summary: 'Job Created',
        detail: `Async job created with ID: ${response.data.job_id.slice(-8)}`,
        life: 5000
      })
    } else {
      // Use sync generation
      const response = await axios.post('/api/threat-model/generate', {
        content: form.value.content,
        framework: form.value.framework,
        file_id: form.value.file_id,
        llm_provider: form.value.llm_provider
      })
      
      currentThreatModel.value = response.data
      
      toast.add({
        severity: 'success',
        summary: 'Success',
        detail: 'Threat model generated successfully',
        life: 3000
      })
    }
  } catch (error) {
    console.error('Generation failed:', error)
    error.value = error.response?.data?.detail || 'Generation failed'
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: error.value,
      life: 3000
    })
  } finally {
    generating.value = false
  }
}

async function compareCosts() {
  loadingCosts.value = true
  showCostDialog.value = true
  try {
    const res = await axios.post('/api/threat-model/estimate-cost', form.value)
    costEstimates.value = res.data
  } catch (err) {
    toast.add({ severity: 'error', summary: 'Cost estimation failed', detail: err.response?.data?.detail || 'Failed to estimate costs', life: 3000 })
    showCostDialog.value = false
  } finally {
    loadingCosts.value = false
  }
}

function selectProvider(provider) {
  form.value.llm_provider = provider
  toast.add({ severity: 'info', summary: 'Provider selected', detail: `Selected: ${provider}`, life: 2000 })
}

function regenerate() {
  currentThreatModel.value = null
}

function handleJobResult(result) {
  currentThreatModel.value = result
  toast.add({
    severity: 'success',
    summary: 'Result Loaded',
    detail: 'Threat model result loaded from job',
    life: 3000
  })
}

function handleStartModeling() {
  // Pre-fill form with example content when user completes tutorial
  form.value.content = `Our web application is a customer portal that allows users to:
- Register and authenticate using email/password
- View and update their profile information
- Upload and download documents (PDF, images)
- Make payments using credit cards
- Access support tickets and chat with agents

The system uses:
- React frontend with Node.js backend
- PostgreSQL database for user data
- AWS S3 for file storage
- Stripe for payment processing
- Redis for session management`
  
  toast.add({
    severity: 'info',
    summary: 'Tutorial Complete',
    detail: 'Example content loaded. You can modify it or start generating your threat model!',
    life: 5000
  })
}

onMounted(async () => {
  await fetchFiles()
  
  try {
    const response = await axios.get('/api/threat-model/providers')
    availableProviders.value = response.data.providers
    if (availableProviders.value.length > 0) {
      form.value.llm_provider = availableProviders.value[0]
    }
  } catch (error) {
    console.error('Failed to load providers:', error)
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to load AI providers',
      life: 3000
    })
  } finally {
    loadingProviders.value = false
  }
})
</script>

<style scoped>
.threat-model-upload {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 0;
}

.threat-model-header {
  margin-bottom: 2rem;
  padding: 2rem;
  background: var(--surface-card);
  border-radius: 16px;
  border: 1px solid var(--surface-border);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}

.title-section h2 {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: 1.8rem;
  margin: 0;
  color: var(--text-color);
  display: flex;
  align-items: center;
}

.title-section p {
  font-family: 'Inter', sans-serif;
  font-size: 1rem;
  color: var(--text-color-secondary);
  margin: 0;
  opacity: 0.9;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.threat-model-form, .file-upload-section, .threat-model-results {
  padding: 2rem;
  background: var(--surface-card);
  border-radius: 16px;
  border: 1px solid var(--surface-border);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
  transition: all 0.3s ease;
}

.form-header {
  margin-bottom: 2rem;
  text-align: center;
}

.form-header h3 {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: 1.5rem;
  margin: 0 0 0.5rem 0;
  color: var(--text-color);
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-header p {
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
}

label {
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 0.875rem;
  color: var(--text-color);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-textarea, .form-dropdown {
  font-family: 'Inter', sans-serif;
  border-radius: 8px;
  border: 2px solid var(--surface-border);
  transition: all 0.3s ease;
  background: var(--surface-ground);
  color: var(--text-color);
}

.form-textarea:focus, .form-dropdown:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(var(--primary-color-rgb), 0.1);
  outline: none;
}

.form-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
  margin-top: 2rem;
}

.generation-mode {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  padding: 1rem;
  border-radius: 12px;
  background: var(--surface-section);
  border: 1px solid var(--surface-border);
  width: 100%;
  max-width: 400px;
}

.mode-toggle {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.mode-toggle:hover {
  background: var(--surface-hover);
}

.mode-checkbox {
  display: none;
}

.mode-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: var(--text-color);
  font-size: 0.9rem;
}

.mode-label i {
  font-size: 1rem;
  color: var(--primary-color);
}

.mode-description {
  font-size: 0.8rem;
  color: var(--text-color-secondary);
  text-align: center;
  line-height: 1.4;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
  justify-content: center;
}

.generate-button {
  min-width: 200px;
}

.compare-costs-btn {
  min-width: 150px;
}

.form-status {
  margin-top: 1rem;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  background: var(--surface-section);
  border: 1px solid var(--surface-border);
  color: var(--text-color-secondary);
  font-size: 0.9rem;
}

.status-indicator.valid {
  background: var(--green-50);
  border-color: var(--green-200);
  color: var(--green-700);
}

.status-indicator i {
  font-size: 1rem;
}

.job-monitor-section {
  margin-top: 2rem;
}

.drop-area {
  border: 2px dashed #6f00ff;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  color: #a7f6ff;
  background: #23244a;
  margin-bottom: 1rem;
  cursor: pointer;
  transition: border-color 0.2s;
}

.drop-area:hover {
  border-color: #00fff7;
}

.upload-btn {
  margin-left: 1rem;
}

.bulk-actions {
  margin-bottom: 0.5rem;
}

.bulk-delete-btn {
  margin-bottom: 0.5rem;
}

.file-list {
  list-style: none;
  padding: 0;
}

.file-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  background: #23244a;
  border-radius: 6px;
  padding: 0.5rem 1rem;
}

.delete-btn {
  margin-left: 1rem;
}

.error {
  color: #ff4d4f;
  margin-left: 1rem;
}
</style> 