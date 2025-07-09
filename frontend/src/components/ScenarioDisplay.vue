<template>
  <!-- Modern scenario display -->
  <div v-if="scenario && scenario.scenario" class="scenario-container">
    <!-- Header with gradient background -->
    <div class="scenario-header">
      <div class="header-content">
        <div class="title-section">
          <h2 class="scenario-title">
            <i class="pi pi-shield" style="margin-right: 0.5rem; color: var(--primary-color);"></i>
            Generated Scenario
          </h2>
          <p class="scenario-subtitle">Your cybersecurity tabletop exercise is ready</p>
        </div>
        <div class="meta-cards">
          <div class="meta-card cost-card">
            <i class="pi pi-dollar" style="color: #4caf50;"></i>
            <div class="meta-content">
              <span class="meta-label">Cost</span>
              <span class="meta-value">${{ scenario.estimated_cost.toFixed(4) }}</span>
            </div>
          </div>
          <div class="meta-card provider-card">
            <i class="pi pi-server" style="color: #2196f3;"></i>
            <div class="meta-content">
              <span class="meta-label">Provider</span>
              <span class="meta-value">{{ scenario.provider_used }}</span>
            </div>
          </div>
          <div class="meta-card id-card">
            <i class="pi pi-id-card" style="color: #ff9800;"></i>
            <div class="meta-content">
              <span class="meta-label">ID</span>
              <span class="meta-value">{{ scenario.id.substring(0, 8) }}...</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Scenario content -->
    <div class="scenario-content">
      <!-- Parsed sections display -->
      <div v-if="parsedSections.length > 0" class="sections-container">
        <div v-for="(section, index) in parsedSections" :key="index" class="section-card">
          <div class="section-header">
            <div class="section-title">
              <span class="section-number">{{ (index + 1).toString().padStart(2, '0') }}</span>
              <h3 class="section-title-text">{{ section.title }}</h3>
            </div>
            <Button 
              @click="rerollSection(section.title)" 
              icon="pi pi-refresh" 
              size="small"
              text
              rounded
              class="reroll-button"
              v-tooltip="'Regenerate this section'"
              :loading="rerollingSection === section.title"
              :disabled="rerollingSection === section.title"
            />
          </div>
          <div class="section-content" v-html="renderMarkdown(section.content)"></div>
        </div>
      </div>
      
      <!-- Fallback to raw text if no sections found -->
      <div v-else class="raw-content-card">
        <div class="raw-content-header">
          <h3 class="raw-content-title">
            <i class="pi pi-file-text" style="margin-right: 0.5rem;"></i>
            Scenario Content
          </h3>
        </div>
        <div class="raw-content-body">
          <div class="markdown-content" v-html="renderMarkdown(scenario.scenario)"></div>
        </div>
      </div>
    </div>
    
    <!-- Action buttons -->
    <div class="action-bar">
      <div class="action-buttons">
        <Button 
          @click="$emit('regenerate')" 
          label="Regenerate" 
          icon="pi pi-refresh" 
          class="primary-action"
        />
        <Button 
          @click="copyToClipboard" 
          label="Copy" 
          icon="pi pi-copy" 
          severity="secondary"
          class="secondary-action"
        />
        <Button 
          @click="exportScenario" 
          label="Export" 
          icon="pi pi-download" 
          severity="secondary"
          class="secondary-action"
        />
      </div>
    </div>
    
    <Toast />
  </div>
  
  <!-- Fallback when scenario exists but no content -->
  <div v-else-if="scenario" class="error-container">
    <div class="error-card">
      <i class="pi pi-exclamation-triangle" style="font-size: 2rem; color: #ff9800; margin-bottom: 1rem;"></i>
      <h3>Scenario Received but No Content</h3>
      <pre class="error-content">{{ JSON.stringify(scenario, null, 2) }}</pre>
    </div>
  </div>
  
  <!-- Fallback when no scenario -->
  <div v-else class="empty-container">
    <div class="empty-card">
      <i class="pi pi-file-edit" style="font-size: 3rem; color: var(--text-color-secondary); margin-bottom: 1rem;"></i>
      <h3>No Scenario Available</h3>
      <p>Generate a scenario to see it displayed here.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useToast } from 'primevue/usetoast'
import Button from 'primevue/button'
import Chip from 'primevue/chip'
import Toast from 'primevue/toast'
import { marked } from 'marked'
import axios from 'axios'

const props = defineProps({
  scenario: Object,
  formData: Object
})

const emit = defineEmits(['regenerate', 'reroll-section'])
const toast = useToast()

const rerollingSection = ref(null)
const sections = ref([])

// Configure marked for security
marked.setOptions({
  breaks: true,
  gfm: true
})

// Debug logging
console.log('ScenarioDisplay received props:', props.scenario)
console.log('Scenario object keys:', props.scenario ? Object.keys(props.scenario) : 'No scenario')
console.log('Scenario.scenario value:', props.scenario?.scenario)
console.log('Component should render:', !!props.scenario)

// Watch for prop changes
watch(() => props.scenario, (newScenario, oldScenario) => {
  console.log('ScenarioDisplay prop changed:', {
    old: oldScenario,
    new: newScenario,
    oldKeys: oldScenario ? Object.keys(oldScenario) : null,
    newKeys: newScenario ? Object.keys(newScenario) : null
  })
  // Re-parse sections when scenario changes
  sections.value = parseSections(newScenario?.scenario)
}, { immediate: true })

function parseSections(text) {
  if (!text) return []
  const sections = []
  const lines = text.split('\n')
  let currentSection = null
  for (const line of lines) {
    if (line.match(/^#{2,}\s+/) || line.match(/^[A-Z][A-Z\s]+:?$/)) {
      if (currentSection) sections.push(currentSection)
      const title = line.replace(/^#{2,}\s+/, '').replace(/:$/, '').trim()
      currentSection = { title, content: '' }
    } else if (currentSection) {
      currentSection.content += line + '\n'
    }
  }
  if (currentSection) sections.push(currentSection)
  return sections
}

const parsedSections = computed(() => sections.value)

// Function to render markdown content
const renderMarkdown = (content) => {
  try {
    return marked(content)
  } catch (error) {
    console.error('Error rendering markdown:', error)
    return content
  }
}

async function rerollSection(sectionTitle) {
  if (rerollingSection.value) return
  const sectionIdx = sections.value.findIndex(s => s.title === sectionTitle)
  if (sectionIdx === -1) return
  rerollingSection.value = sectionTitle
  try {
    const response = await axios.post('/api/scenarios/reroll', {
      original_scenario: props.scenario.scenario,
      section_title: sectionTitle,
      section_content: sections.value[sectionIdx].content,
      context: props.formData,
      llm_provider: props.scenario.provider_used
    })
    if (response.data && response.data.new_content) {
      sections.value[sectionIdx] = {
        ...sections.value[sectionIdx],
        content: response.data.new_content
      }
      toast.add({
        severity: 'success',
        summary: 'Section Regenerated',
        detail: `"${sectionTitle}" updated!`,
        life: 2000
      })
    } else {
      throw new Error('No new content returned')
    }
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: 'Re-roll Failed',
      detail: err.response?.data?.detail || err.message || 'Failed to regenerate section',
      life: 3000
    })
  } finally {
    rerollingSection.value = null
  }
}

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(props.scenario.scenario)
    toast.add({
      severity: 'success',
      summary: 'Copied!',
      detail: 'Scenario copied to clipboard',
      life: 2000
    })
  } catch (err) {
    console.error('Failed to copy to clipboard:', err)
    toast.add({
      severity: 'error',
      summary: 'Failed to copy',
      detail: 'Please try again or use the export feature',
      life: 3000
    })
  }
}

const exportScenario = () => {
  try {
    const blob = new Blob([props.scenario.scenario], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `threatforge-scenario-${props.scenario.id}.txt`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    
    toast.add({
      severity: 'success',
      summary: 'Exported!',
      detail: 'Scenario downloaded successfully',
      life: 2000
    })
  } catch (err) {
    console.error('Failed to export scenario:', err)
    toast.add({
      severity: 'error',
      summary: 'Export Failed',
      detail: 'Please try again',
      life: 3000
    })
  }
}
</script>

<style scoped>
/* Import Google Fonts for better typography */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* Main container */
.scenario-container {
  background: var(--surface-card);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin: 2rem 0;
  border: 1px solid var(--surface-border);
  transition: all 0.3s ease;
}

.scenario-container:hover {
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

/* Header with gradient */
.scenario-header {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-600) 100%);
  padding: 2rem;
  color: white;
  position: relative;
  overflow: hidden;
}

.scenario-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="75" cy="75" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="50" cy="10" r="0.5" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
  opacity: 0.3;
}

.header-content {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 2rem;
}

.title-section {
  flex: 1;
}

.scenario-title {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: 2rem;
  margin: 0 0 0.5rem 0;
  color: white;
  display: flex;
  align-items: center;
}

.scenario-subtitle {
  font-family: 'Inter', sans-serif;
  font-weight: 400;
  font-size: 1rem;
  margin: 0;
  color: rgba(255, 255, 255, 0.9);
  opacity: 0.9;
}

/* Meta cards */
.meta-cards {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.meta-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 1rem;
  min-width: 120px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.meta-card:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
}

.meta-card i {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  display: block;
}

.meta-content {
  display: flex;
  flex-direction: column;
}

.meta-label {
  font-family: 'Inter', sans-serif;
  font-size: 0.75rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.8);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.meta-value {
  font-family: 'Inter', sans-serif;
  font-size: 1rem;
  font-weight: 600;
  color: white;
}

/* Content area */
.scenario-content {
  padding: 2rem;
  background: var(--surface-ground);
}

/* Sections container */
.sections-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Section cards */
.section-card {
  background: var(--surface-card);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid var(--surface-border);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.section-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(180deg, var(--primary-color) 0%, var(--primary-600) 100%);
}

.section-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.section-number {
  background: var(--primary-color);
  color: white;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 600;
  font-size: 0.875rem;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  min-width: 2.5rem;
  text-align: center;
}

.section-title-text {
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 1.25rem;
  margin: 0;
  color: var(--text-color);
}

.reroll-button {
  opacity: 0.7;
  transition: all 0.3s ease;
}

.reroll-button:hover {
  opacity: 1;
  transform: rotate(180deg);
}

.section-content {
  font-family: 'Inter', sans-serif;
  font-size: 1rem;
  line-height: 1.7;
  color: var(--text-color);
  white-space: pre-wrap;
  word-wrap: break-word;
}

/* Markdown content styling */
.markdown-content {
  font-family: 'Inter', sans-serif;
  line-height: 1.7;
  color: var(--text-color);
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  margin: 1.5rem 0 1rem 0;
  color: var(--text-color);
}

.markdown-content h1 {
  font-size: 1.75rem;
  border-bottom: 2px solid var(--primary-color);
  padding-bottom: 0.5rem;
}

.markdown-content h2 {
  font-size: 1.5rem;
  color: var(--primary-color);
}

.markdown-content h3 {
  font-size: 1.25rem;
}

.markdown-content h4 {
  font-size: 1.125rem;
}

.markdown-content p {
  margin: 1rem 0;
  line-height: 1.7;
}

.markdown-content ul,
.markdown-content ol {
  margin: 1rem 0;
  padding-left: 2rem;
}

.markdown-content li {
  margin: 0.5rem 0;
  line-height: 1.6;
}

.markdown-content strong,
.markdown-content b {
  font-weight: 600;
  color: var(--text-color);
}

.markdown-content em,
.markdown-content i {
  font-style: italic;
  color: var(--text-color-secondary);
}

.markdown-content code {
  background: var(--surface-section);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875rem;
  color: var(--primary-color);
  border: 1px solid var(--surface-border);
}

.markdown-content pre {
  background: var(--surface-section);
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
  border: 1px solid var(--surface-border);
  margin: 1rem 0;
}

.markdown-content pre code {
  background: none;
  padding: 0;
  border: none;
  color: var(--text-color);
}

.markdown-content blockquote {
  border-left: 4px solid var(--primary-color);
  padding-left: 1rem;
  margin: 1rem 0;
  font-style: italic;
  color: var(--text-color-secondary);
  background: var(--surface-section);
  padding: 1rem;
  border-radius: 0 8px 8px 0;
}

.markdown-content hr {
  border: none;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--primary-color), transparent);
  margin: 2rem 0;
}

.markdown-content table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  background: var(--surface-card);
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--surface-border);
}

.markdown-content th,
.markdown-content td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid var(--surface-border);
}

.markdown-content th {
  background: var(--surface-section);
  font-weight: 600;
  color: var(--text-color);
}

.markdown-content tr:hover {
  background: var(--surface-ground);
}

/* Raw content card */
.raw-content-card {
  background: var(--surface-card);
  border-radius: 12px;
  border: 1px solid var(--surface-border);
  overflow: hidden;
}

.raw-content-header {
  background: var(--surface-section);
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--surface-border);
}

.raw-content-title {
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 1.125rem;
  margin: 0;
  color: var(--text-color);
  display: flex;
  align-items: center;
}

.raw-content-body {
  padding: 1.5rem;
  max-height: 400px;
  overflow-y: auto;
}

.raw-content-text {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875rem;
  line-height: 1.6;
  color: var(--text-color);
  white-space: pre-wrap;
  margin: 0;
}

/* Action bar */
.action-bar {
  background: var(--surface-section);
  padding: 1.5rem 2rem;
  border-top: 1px solid var(--surface-border);
}

.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.primary-action {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-600) 100%);
  border: none;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.primary-action:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(var(--primary-color-rgb), 0.3);
}

.secondary-action {
  font-weight: 500;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.secondary-action:hover {
  transform: translateY(-2px);
}

/* Error and empty states */
.error-container,
.empty-container {
  display: flex;
  justify-content: center;
  padding: 3rem 2rem;
}

.error-card,
.empty-card {
  background: var(--surface-card);
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  border: 1px solid var(--surface-border);
  max-width: 500px;
  width: 100%;
}

.error-card h3,
.empty-card h3 {
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 1.25rem;
  margin: 0 0 1rem 0;
  color: var(--text-color);
}

.empty-card p {
  font-family: 'Inter', sans-serif;
  font-size: 1rem;
  color: var(--text-color-secondary);
  margin: 0;
}

.error-content {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875rem;
  background: var(--surface-ground);
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
  text-align: left;
  overflow-x: auto;
  color: var(--text-color);
}

/* Responsive design */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .meta-cards {
    justify-content: center;
  }
  
  .meta-card {
    min-width: 100px;
  }
  
  .scenario-title {
    font-size: 1.5rem;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}

/* Dark mode specific adjustments */
:root.dark-mode .scenario-container {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

:root.dark-mode .section-card {
  background: var(--surface-card);
  border-color: var(--surface-border);
}

:root.dark-mode .section-content {
  color: var(--text-color);
}

:root.dark-mode .raw-content-text {
  color: var(--text-color);
}

:root.dark-mode .error-content {
  background: var(--surface-ground);
  color: var(--text-color);
}
</style>