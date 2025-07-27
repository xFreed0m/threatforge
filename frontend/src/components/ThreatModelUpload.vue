<template>
  <div class="threat-model-upload">
    <h2>Generate Threat Model</h2>
    
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
        <Button 
          @click="generateThreatModel" 
          :loading="generating" 
          label="Generate Threat Model"
          icon="pi pi-shield"
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
    
    <!-- Cost Comparison Dialog -->
    <CostComparison
      v-model:visible="showCostDialog"
      :estimates="costEstimates"
      :loading="loadingCosts"
      :selectedProvider="form.llm_provider"
      @select-provider="selectProvider"
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

function formatSize(size) {
  if (size > 1024 * 1024) return (size / (1024 * 1024)).toFixed(2) + ' MB'
  if (size > 1024) return (size / 1024).toFixed(1) + ' KB'
  return size + ' B'
}

async function fetchFiles() {
  const res = await axios.get('/api/threat-model/files')
  files.value = res.data
}

function onFileChange(e) {
  error.value = null
  const filesArr = Array.from(e.target.files)
  selectedFiles.value = filesArr.filter(validateFile)
}

function onDrop(e) {
  error.value = null
  const filesArr = Array.from(e.dataTransfer.files)
  selectedFiles.value = filesArr.filter(validateFile)
}

function validateFile(file) {
  const allowed = ['drawio', 'png', 'jpg', 'svg', 'xml']
  const ext = file.name.split('.').pop().toLowerCase()
  if (!allowed.includes(ext)) {
    error.value = 'Unsupported file type.'
    return false
  }
  if (file.size > 10 * 1024 * 1024) {
    error.value = 'File too large (max 10MB).'
    return false
  }
  return true
}

async function handleUpload() {
  if (!selectedFiles.value.length) return
  error.value = null
  uploading.value = true
  uploadProgress.value = {}
  try {
    await Promise.all(selectedFiles.value.map(file => uploadSingleFile(file)))
    selectedFiles.value = []
    await fetchFiles()
    toast.add({ severity: 'success', summary: 'Upload Complete', detail: 'Files uploaded successfully', life: 2000 })
  } catch (e) {
    error.value = e.response?.data?.detail || 'Upload failed.'
    toast.add({ severity: 'error', summary: 'Upload Failed', detail: error.value, life: 3000 })
  } finally {
    uploading.value = false
  }
}

async function uploadSingleFile(file) {
  return new Promise((resolve, reject) => {
    const formData = new FormData()
    formData.append('file', file)
    const xhr = new XMLHttpRequest()
    xhr.open('POST', '/api/threat-model/upload')
    xhr.upload.onprogress = (e) => {
      if (e.lengthComputable) {
        uploadProgress.value[file.name] = Math.round((e.loaded / e.total) * 100)
      }
    }
    xhr.onload = () => {
      uploadProgress.value[file.name] = 100
      resolve()
    }
    xhr.onerror = () => {
      error.value = 'Upload failed.'
      reject()
    }
    xhr.send(formData)
  })
}

async function bulkDelete() {
  await Promise.all(selectedToDelete.value.map(id => deleteFile(id, true)))
  selectedToDelete.value = []
  await fetchFiles()
  toast.add({ severity: 'success', summary: 'Files Deleted', detail: 'Selected files deleted successfully', life: 2000 })
}

async function deleteFile(file_id, silent) {
  await axios.delete(`/api/threat-model/files/${file_id}`)
  if (!silent) {
    await fetchFiles()
    toast.add({ severity: 'success', summary: 'File Deleted', detail: 'File deleted successfully', life: 2000 })
  }
}

async function generateThreatModel() {
  if (!isFormValid.value) return
  generating.value = true
  currentThreatModel.value = null
  try {
    const response = await axios.post('/api/threat-model/generate', form.value)
    currentThreatModel.value = response.data
    toast.add({ severity: 'success', summary: 'Threat Model Generated', detail: 'Analysis completed successfully', life: 3000 })
  } catch (err) {
    toast.add({ severity: 'error', summary: 'Generation Failed', detail: err.response?.data?.detail || 'Failed to generate threat model', life: 3000 })
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

.compare-costs-btn {
  margin-left: 1rem;
}
</style> 