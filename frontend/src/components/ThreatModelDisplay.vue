<template>
  <div class="threat-model-display">
    <div v-if="threatModel && threatModel.threat_model" class="threat-model-container">
      <!-- Header with gradient background -->
      <div class="threat-model-header">
        <div class="header-content">
          <div class="title-section">
            <h2 class="threat-model-title">
              <i class="pi pi-shield" style="margin-right: 0.5rem; color: var(--primary-color);"></i>
              Generated Threat Model
            </h2>
            <p class="threat-model-subtitle">Your cybersecurity threat analysis is ready</p>
          </div>
          <div class="meta-cards">
            <div class="meta-card cost-card">
              <i class="pi pi-dollar" style="color: #4caf50;"></i>
              <div class="meta-content">
                <span class="meta-label">Cost</span>
                <span class="meta-value">${{ threatModel.estimated_cost.toFixed(4) }}</span>
              </div>
            </div>
            <div class="meta-card provider-card">
              <i class="pi pi-server" style="color: #2196f3;"></i>
              <div class="meta-content">
                <span class="meta-label">Provider</span>
                <span class="meta-value">{{ threatModel.provider_used }}</span>
              </div>
            </div>
            <div class="meta-card framework-card">
              <i class="pi pi-sitemap" style="color: #ff9800;"></i>
              <div class="meta-content">
                <span class="meta-label">Framework</span>
                <span class="meta-value">{{ threatModel.framework }}</span>
              </div>
            </div>
            <div class="meta-card id-card">
              <i class="pi pi-id-card" style="color: #9c27b0;"></i>
              <div class="meta-content">
                <span class="meta-label">ID</span>
                <span class="meta-value">{{ threatModel.id.substring(0, 8) }}...</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Threat model content -->
      <div class="threat-model-content">
        <div class="content-card">
          <div class="content-header">
            <h3 class="content-title">
              <i class="pi pi-file-text" style="margin-right: 0.5rem;"></i>
              Threat Analysis Results
            </h3>
          </div>
          <div class="content-body">
            <div class="markdown-content" v-html="renderMarkdown(threatModel.threat_model)"></div>
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
          <SplitButton
            :model="exportItems"
            label="Export"
            icon="pi pi-download"
            severity="secondary"
            class="secondary-action cyber-splitbutton"
            @click="exportThreatModel('pdf')"
          />
        </div>
      </div>
      
      <Toast />
    </div>
    
    <!-- Fallback when no threat model -->
    <div v-else class="empty-container">
      <div class="empty-card">
        <i class="pi pi-shield" style="font-size: 3rem; color: var(--text-color-secondary); margin-bottom: 1rem;"></i>
        <h3>No Threat Model Available</h3>
        <p>Generate a threat model to see it displayed here.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useToast } from 'primevue/usetoast'
import Button from 'primevue/button'
import Toast from 'primevue/toast'
import { marked } from 'marked'
import SplitButton from 'primevue/splitbutton'

const props = defineProps({
  threatModel: Object,
  formData: Object
})

const emit = defineEmits(['regenerate'])
const toast = useToast()

// Configure marked for security
marked.setOptions({
  breaks: true,
  gfm: true
})

// Function to render markdown content
const renderMarkdown = (content) => {
  try {
    return marked(content)
  } catch (error) {
    console.error('Error rendering markdown:', error)
    return content
  }
}

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(props.threatModel.threat_model)
    toast.add({
      severity: 'success',
      summary: 'Copied!',
      detail: 'Threat model copied to clipboard',
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

const exportItems = [
  { label: 'Text File (.txt)', icon: 'pi pi-file', command: () => exportThreatModel('txt') },
  { label: 'Markdown (.md)', icon: 'pi pi-file-edit', command: () => exportThreatModel('md') },
  { label: 'JSON (.json)', icon: 'pi pi-code', command: () => exportThreatModel('json') },
  { label: 'PDF (.pdf)', icon: 'pi pi-file-pdf', command: () => exportThreatModel('pdf') }
]

function exportThreatModel(format) {
  if (!props.threatModel) return
  if (format === 'txt') {
    const blob = new Blob([props.threatModel.threat_model], { type: 'text/plain' })
    saveBlob(blob, `threatforge-threatmodel-${props.threatModel.id}.txt`)
    toast.add({ severity: 'success', summary: 'Exported!', detail: 'Exported as Text File', life: 2000 })
  } else if (format === 'md') {
    const md = buildMarkdown()
    const blob = new Blob([md], { type: 'text/markdown' })
    saveBlob(blob, `threatforge-threatmodel-${props.threatModel.id}.md`)
    toast.add({ severity: 'success', summary: 'Exported!', detail: 'Exported as Markdown', life: 2000 })
  } else if (format === 'json') {
    const data = {
      ...props.threatModel,
      formData: props.formData
    }
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    saveBlob(blob, `threatforge-threatmodel-${props.threatModel.id}.json`)
    toast.add({ severity: 'success', summary: 'Exported!', detail: 'Exported as JSON', life: 2000 })
  } else if (format === 'pdf') {
    exportPDF()
    toast.add({ severity: 'success', summary: 'Exported!', detail: 'Exported as PDF', life: 2000 })
  }
}

function saveBlob(blob, filename) {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

function buildMarkdown() {
  let md = `# ThreatForge Threat Model\n\n`;
  md += `**Framework:** ${props.threatModel.framework}\n`;
  md += `**Date:** ${new Date().toLocaleString()}\n`;
  md += `**Cost:** $${props.threatModel.estimated_cost?.toFixed(4) || ''}\n`;
  md += `**Provider:** ${props.threatModel.provider_used || ''}\n`;
  md += `**ID:** ${props.threatModel.id || ''}\n`;
  md += `**Content Analyzed:** ${props.threatModel.content_analyzed || ''}\n`;
  md += `\n---\n`;
  md += props.threatModel.threat_model;
  return md;
}

function exportPDF() {
  // Use window.print() for now with print-specific CSS
  window.print()
}
</script>

<style scoped>
/* Import Google Fonts for better typography */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* Main container */
.threat-model-container {
  background: var(--surface-card);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin: 2rem 0;
  border: 1px solid var(--surface-border);
  transition: all 0.3s ease;
}

.threat-model-container:hover {
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

/* Header with gradient */
.threat-model-header {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-600) 100%);
  padding: 2rem;
  color: white;
  position: relative;
  overflow: hidden;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 2rem;
}

.title-section {
  flex: 1;
  min-width: 300px;
}

.threat-model-title {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: 2rem;
  margin: 0 0 0.5rem 0;
  display: flex;
  align-items: center;
}

.threat-model-subtitle {
  font-family: 'Inter', sans-serif;
  font-size: 1.1rem;
  margin: 0;
  opacity: 0.9;
}

.meta-cards {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.meta-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.meta-content {
  display: flex;
  flex-direction: column;
}

.meta-label {
  font-size: 0.75rem;
  opacity: 0.8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.meta-value {
  font-weight: 600;
  font-size: 1rem;
}

/* Content section */
.threat-model-content {
  padding: 2rem;
}

.content-card {
  background: var(--surface-ground);
  border-radius: 12px;
  border: 1px solid var(--surface-border);
  overflow: hidden;
}

.content-header {
  background: var(--surface-section);
  padding: 1.5rem 2rem;
  border-bottom: 1px solid var(--surface-border);
}

.content-title {
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 1.25rem;
  margin: 0;
  color: var(--text-color);
  display: flex;
  align-items: center;
}

.content-body {
  padding: 2rem;
}

.markdown-content {
  font-family: 'Inter', sans-serif;
  line-height: 1.7;
  color: var(--text-color);
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4 {
  color: var(--text-color);
  margin-top: 2rem;
  margin-bottom: 1rem;
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

.markdown-content p {
  margin-bottom: 1rem;
}

.markdown-content ul,
.markdown-content ol {
  margin-bottom: 1rem;
  padding-left: 2rem;
}

.markdown-content li {
  margin-bottom: 0.5rem;
}

.markdown-content strong {
  color: var(--primary-color);
  font-weight: 600;
}

.markdown-content code {
  background: var(--surface-section);
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.9em;
}

.markdown-content pre {
  background: var(--surface-section);
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
  margin: 1rem 0;
}

.markdown-content pre code {
  background: none;
  padding: 0;
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

.primary-action,
.secondary-action {
  min-width: 120px;
}

/* Empty state */
.empty-container {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-card {
  background: var(--surface-card);
  border-radius: 16px;
  padding: 3rem;
  border: 1px solid var(--surface-border);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.empty-card h3 {
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 1.5rem;
  margin: 1rem 0 0.5rem 0;
  color: var(--text-color);
}

.empty-card p {
  font-family: 'Inter', sans-serif;
  color: var(--text-color-secondary);
  margin: 0;
}

/* Responsive design */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    text-align: center;
  }
  
  .meta-cards {
    justify-content: center;
  }
  
  .meta-card {
    min-width: 120px;
  }
  
  .action-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .primary-action,
  .secondary-action {
    width: 100%;
    max-width: 200px;
  }
}

/* Cyberpunk split button styling */
.cyber-splitbutton .p-splitbutton {
  background: linear-gradient(90deg, #6f00ff 0%, #00fff7 100%) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 8px !important;
  font-family: 'Orbitron', 'Rajdhani', 'Segoe UI', Arial, sans-serif !important;
  font-weight: 700 !important;
  font-size: 1.1rem !important;
  box-shadow: 0 0 12px #6f00ff88, 0 0 2px #00fff7 !important;
  transition: background 0.2s, box-shadow 0.2s, color 0.2s, transform 0.15s !important;
  cursor: pointer !important;
  outline: none !important;
}

.cyber-splitbutton .p-splitbutton:hover {
  background: linear-gradient(90deg, #00fff7 0%, #6f00ff 100%) !important;
  color: #fff !important;
  box-shadow: 0 0 24px #00fff7cc, 0 0 8px #6f00ffcc !important;
}
</style> 