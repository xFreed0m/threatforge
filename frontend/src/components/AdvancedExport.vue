<template>
  <div class="advanced-export">
    <Dialog v-model:visible="visible" 
            header="Advanced Export Options" 
            :style="{ width: '800px' }"
            :modal="true">
      
      <div class="export-content">
        <!-- Export Type Selection -->
        <div class="export-section">
          <h4>Export Type</h4>
          <div class="export-types">
            <div class="export-type-card" 
                 :class="{ selected: selectedType === 'pdf' }"
                 @click="selectedType = 'pdf'">
              <i class="pi pi-file-pdf"></i>
              <h5>PDF Report</h5>
              <p>Professional PDF report with executive summary</p>
            </div>
            
            <div class="export-type-card" 
                 :class="{ selected: selectedType === 'executive' }"
                 @click="selectedType = 'executive'">
              <i class="pi pi-chart-line"></i>
              <h5>Executive Summary</h5>
              <p>High-level summary for stakeholders</p>
            </div>
            
            <div class="export-type-card" 
                 :class="{ selected: selectedType === 'technical' }"
                 @click="selectedType = 'technical'">
              <i class="pi pi-cog"></i>
              <h5>Technical Report</h5>
              <p>Detailed technical analysis for security teams</p>
            </div>
            
            <div class="export-type-card" 
                 :class="{ selected: selectedType === 'compliance' }"
                 @click="selectedType = 'compliance'">
              <i class="pi pi-check-circle"></i>
              <h5>Compliance Report</h5>
              <p>Compliance-focused report with controls mapping</p>
            </div>
          </div>
        </div>

        <!-- Report Configuration -->
        <div class="export-section">
          <h4>Report Configuration</h4>
          
          <div class="config-grid">
            <div class="config-group">
              <label>Include Sections</label>
              <div class="checkbox-group">
                <div class="checkbox-item">
                  <Checkbox v-model="config.includeOverview" :binary="true" />
                  <span>System Overview</span>
                </div>
                <div class="checkbox-item">
                  <Checkbox v-model="config.includeThreats" :binary="true" />
                  <span>Threat Analysis</span>
                </div>
                <div class="checkbox-item">
                  <Checkbox v-model="config.includeRisks" :binary="true" />
                  <span>Risk Assessment</span>
                </div>
                <div class="checkbox-item">
                  <Checkbox v-model="config.includeMitigations" :binary="true" />
                  <span>Mitigation Strategies</span>
                </div>
                <div class="checkbox-item">
                  <Checkbox v-model="config.includeRecommendations" :binary="true" />
                  <span>Security Recommendations</span>
                </div>
                <div class="checkbox-item">
                  <Checkbox v-model="config.includeDiagrams" :binary="true" />
                  <span>System Diagrams</span>
                </div>
              </div>
            </div>

            <div class="config-group">
              <label>Report Options</label>
              <div class="checkbox-group">
                <div class="checkbox-item">
                  <Checkbox v-model="config.includeCharts" :binary="true" />
                  <span>Include Charts & Graphs</span>
                </div>
                <div class="checkbox-item">
                  <Checkbox v-model="config.includeAppendices" :binary="true" />
                  <span>Include Appendices</span>
                </div>
                <div class="checkbox-item">
                  <Checkbox v-model="config.includeGlossary" :binary="true" />
                  <span>Include Glossary</span>
                </div>
                <div class="checkbox-item">
                  <Checkbox v-model="config.includeReferences" :binary="true" />
                  <span>Include References</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Executive Summary Configuration -->
        <div v-if="selectedType === 'executive'" class="export-section">
          <h4>Executive Summary Options</h4>
          
          <div class="config-grid">
            <div class="config-group">
              <label>Summary Level</label>
              <Dropdown v-model="executiveConfig.level" 
                       :options="summaryLevels" 
                       optionLabel="label"
                       optionValue="value"
                       placeholder="Select summary level" />
            </div>
            
            <div class="config-group">
              <label>Focus Areas</label>
              <MultiSelect v-model="executiveConfig.focusAreas" 
                          :options="focusAreas" 
                          optionLabel="label"
                          optionValue="value"
                          placeholder="Select focus areas" />
            </div>
          </div>
        </div>

        <!-- Compliance Configuration -->
        <div v-if="selectedType === 'compliance'" class="export-section">
          <h4>Compliance Framework</h4>
          
          <div class="config-grid">
            <div class="config-group">
              <label>Framework</label>
              <Dropdown v-model="complianceConfig.framework" 
                       :options="complianceFrameworks" 
                       optionLabel="label"
                       optionValue="value"
                       placeholder="Select compliance framework" />
            </div>
            
            <div class="config-group">
              <label>Include Controls Mapping</label>
              <Checkbox v-model="complianceConfig.includeControls" :binary="true" />
            </div>
          </div>
        </div>

        <!-- Report Metadata -->
        <div class="export-section">
          <h4>Report Metadata</h4>
          
          <div class="config-grid">
            <div class="config-group">
              <label>Report Title</label>
              <InputText v-model="metadata.title" placeholder="Enter report title" />
            </div>
            
            <div class="config-group">
              <label>Author</label>
              <InputText v-model="metadata.author" placeholder="Enter author name" />
            </div>
            
            <div class="config-group">
              <label>Organization</label>
              <InputText v-model="metadata.organization" placeholder="Enter organization" />
            </div>
            
            <div class="config-group">
              <label>Report Date</label>
              <Calendar v-model="metadata.date" showIcon />
            </div>
          </div>
        </div>

        <!-- Preview -->
        <div class="export-section">
          <h4>Report Preview</h4>
          <div class="preview-container">
            <div class="preview-content">
              <h3>{{ metadata.title || 'Threat Model Report' }}</h3>
              <p class="preview-meta">
                <strong>Author:</strong> {{ metadata.author || 'Not specified' }} | 
                <strong>Date:</strong> {{ formatDate(metadata.date) }} | 
                <strong>Type:</strong> {{ getExportTypeLabel(selectedType) }}
              </p>
              
              <div class="preview-sections">
                <div v-if="config.includeOverview" class="preview-section">
                  <h4>System Overview</h4>
                  <p>Brief description of the analyzed system and its components...</p>
                </div>
                
                <div v-if="config.includeThreats" class="preview-section">
                  <h4>Threat Analysis</h4>
                  <p>Detailed analysis of identified threats using {{ threatModel?.framework || 'STRIDE' }} framework...</p>
                </div>
                
                <div v-if="config.includeRisks" class="preview-section">
                  <h4>Risk Assessment</h4>
                  <p>Risk evaluation and prioritization of identified threats...</p>
                </div>
                
                <div v-if="config.includeMitigations" class="preview-section">
                  <h4>Mitigation Strategies</h4>
                  <p>Recommended controls and countermeasures for identified threats...</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <Button label="Cancel" @click="closeDialog" severity="secondary" />
        <Button label="Generate Report" 
                @click="generateReport" 
                :loading="generating"
                severity="primary" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import Checkbox from 'primevue/checkbox'
import Dropdown from 'primevue/dropdown'
import MultiSelect from 'primevue/multiselect'
import InputText from 'primevue/inputtext'
import Calendar from 'primevue/calendar'
import { useToast } from 'primevue/usetoast'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  threatModel: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close'])

const toast = useToast()

// Export type
const selectedType = ref('pdf')

// Configuration
const config = ref({
  includeOverview: true,
  includeThreats: true,
  includeRisks: true,
  includeMitigations: true,
  includeRecommendations: true,
  includeDiagrams: true,
  includeCharts: true,
  includeAppendices: false,
  includeGlossary: false,
  includeReferences: false
})

// Executive summary configuration
const executiveConfig = ref({
  level: 'summary',
  focusAreas: []
})

const summaryLevels = [
  { label: 'Executive Summary', value: 'summary' },
  { label: 'Detailed Summary', value: 'detailed' },
  { label: 'Technical Summary', value: 'technical' }
]

const focusAreas = [
  { label: 'High-Risk Threats', value: 'high-risk' },
  { label: 'Compliance Issues', value: 'compliance' },
  { label: 'Cost Implications', value: 'cost' },
  { label: 'Timeline for Mitigation', value: 'timeline' },
  { label: 'Resource Requirements', value: 'resources' }
]

// Compliance configuration
const complianceConfig = ref({
  framework: '',
  includeControls: true
})

const complianceFrameworks = [
  { label: 'ISO 27001', value: 'iso27001' },
  { label: 'SOC 2', value: 'soc2' },
  { label: 'NIST Cybersecurity Framework', value: 'nist' },
  { label: 'GDPR', value: 'gdpr' },
  { label: 'HIPAA', value: 'hipaa' },
  { label: 'PCI DSS', value: 'pci' }
]

// Metadata
const metadata = ref({
  title: 'Threat Model Analysis Report',
  author: '',
  organization: '',
  date: new Date()
})

// Generation state
const generating = ref(false)

// Methods
const closeDialog = () => {
  emit('close')
}

const formatDate = (date) => {
  if (!date) return 'Not specified'
  return new Date(date).toLocaleDateString()
}

const getExportTypeLabel = (type) => {
  const labels = {
    pdf: 'PDF Report',
    executive: 'Executive Summary',
    technical: 'Technical Report',
    compliance: 'Compliance Report'
  }
  return labels[type] || type
}

const generateReport = async () => {
  generating.value = true
  
  try {
    // Simulate report generation
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Generate report based on type
    let reportContent = ''
    let fileName = ''
    
    switch (selectedType.value) {
      case 'pdf':
        reportContent = generatePDFReport()
        fileName = `threat-model-report-${Date.now()}.pdf`
        break
      case 'executive':
        reportContent = generateExecutiveSummary()
        fileName = `executive-summary-${Date.now()}.pdf`
        break
      case 'technical':
        reportContent = generateTechnicalReport()
        fileName = `technical-report-${Date.now()}.pdf`
        break
      case 'compliance':
        reportContent = generateComplianceReport()
        fileName = `compliance-report-${Date.now()}.pdf`
        break
    }
    
    // Download the report
    downloadReport(reportContent, fileName)
    
    toast.add({
      severity: 'success',
      summary: 'Report Generated',
      detail: `${getExportTypeLabel(selectedType.value)} generated successfully`,
      life: 3000
    })
    
    closeDialog()
  } catch (error) {
    console.error('Error generating report:', error)
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to generate report',
      life: 3000
    })
  } finally {
    generating.value = false
  }
}

const generatePDFReport = () => {
  // This would integrate with a PDF generation library like jsPDF
  return {
    type: 'pdf',
    content: {
      title: metadata.value.title,
      author: metadata.value.author,
      date: metadata.value.date,
      sections: getReportSections(),
      config: config.value
    }
  }
}

const generateExecutiveSummary = () => {
  return {
    type: 'executive',
    content: {
      title: `${metadata.value.title} - Executive Summary`,
      author: metadata.value.author,
      date: metadata.value.date,
      level: executiveConfig.value.level,
      focusAreas: executiveConfig.value.focusAreas,
      summary: generateExecutiveContent()
    }
  }
}

const generateTechnicalReport = () => {
  return {
    type: 'technical',
    content: {
      title: `${metadata.value.title} - Technical Analysis`,
      author: metadata.value.author,
      date: metadata.value.date,
      sections: getTechnicalSections(),
      config: config.value
    }
  }
}

const generateComplianceReport = () => {
  return {
    type: 'compliance',
    content: {
      title: `${metadata.value.title} - Compliance Analysis`,
      author: metadata.value.author,
      date: metadata.value.date,
      framework: complianceConfig.value.framework,
      includeControls: complianceConfig.value.includeControls,
      sections: getComplianceSections()
    }
  }
}

const getReportSections = () => {
  const sections = []
  
  if (config.value.includeOverview) {
    sections.push({
      title: 'System Overview',
      content: 'Detailed description of the analyzed system...'
    })
  }
  
  if (config.value.includeThreats) {
    sections.push({
      title: 'Threat Analysis',
      content: 'Comprehensive threat analysis using STRIDE framework...'
    })
  }
  
  if (config.value.includeRisks) {
    sections.push({
      title: 'Risk Assessment',
      content: 'Risk evaluation and prioritization...'
    })
  }
  
  if (config.value.includeMitigations) {
    sections.push({
      title: 'Mitigation Strategies',
      content: 'Recommended controls and countermeasures...'
    })
  }
  
  return sections
}

const getTechnicalSections = () => {
  return [
    { title: 'Technical Architecture', content: 'Detailed technical analysis...' },
    { title: 'Threat Modeling Methodology', content: 'Framework and approach used...' },
    { title: 'Detailed Threat Analysis', content: 'In-depth threat examination...' },
    { title: 'Technical Mitigations', content: 'Technical control recommendations...' }
  ]
}

const getComplianceSections = () => {
  return [
    { title: 'Compliance Framework', content: `${complianceConfig.value.framework} analysis...` },
    { title: 'Control Mapping', content: 'Mapping threats to compliance controls...' },
    { title: 'Gap Analysis', content: 'Compliance gaps and recommendations...' },
    { title: 'Remediation Plan', content: 'Plan to address compliance gaps...' }
  ]
}

const generateExecutiveContent = () => {
  return {
    summary: 'High-level summary of key findings...',
    keyRisks: ['Risk 1', 'Risk 2', 'Risk 3'],
    recommendations: ['Recommendation 1', 'Recommendation 2'],
    timeline: '3-6 months for implementation',
    budget: '$50,000 - $100,000'
  }
}

const downloadReport = (reportContent, fileName) => {
  // For now, we'll create a JSON file as a placeholder
  // In a real implementation, this would generate actual PDF/Word documents
  const blob = new Blob([JSON.stringify(reportContent, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = fileName
  a.click()
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
.advanced-export {
  /* Component styles */
}

.export-content {
  max-height: 70vh;
  overflow-y: auto;
}

.export-section {
  margin-bottom: 2rem;
}

.export-section h4 {
  margin: 0 0 1rem 0;
  color: var(--text-color);
  font-size: 1.1rem;
}

.export-types {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.export-type-card {
  border: 2px solid var(--surface-border);
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.export-type-card:hover {
  border-color: var(--primary-color);
  transform: translateY(-2px);
}

.export-type-card.selected {
  border-color: var(--primary-color);
  background: var(--primary-50);
}

.export-type-card i {
  font-size: 2rem;
  color: var(--primary-color);
  margin-bottom: 0.5rem;
}

.export-type-card h5 {
  margin: 0.5rem 0;
  color: var(--text-color);
}

.export-type-card p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--text-color-secondary);
}

.config-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.config-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.config-group label {
  font-weight: 600;
  color: var(--text-color);
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.checkbox-item span {
  color: var(--text-color);
  font-size: 0.9rem;
}

.preview-container {
  border: 1px solid var(--surface-border);
  border-radius: 8px;
  padding: 1rem;
  background: var(--surface-section);
  max-height: 300px;
  overflow-y: auto;
}

.preview-content h3 {
  margin: 0 0 0.5rem 0;
  color: var(--text-color);
}

.preview-meta {
  font-size: 0.9rem;
  color: var(--text-color-secondary);
  margin-bottom: 1rem;
}

.preview-sections {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.preview-section h4 {
  margin: 0 0 0.5rem 0;
  color: var(--text-color);
  font-size: 1rem;
}

.preview-section p {
  margin: 0;
  color: var(--text-color-secondary);
  font-size: 0.9rem;
  line-height: 1.4;
}

@media (max-width: 768px) {
  .export-types {
    grid-template-columns: 1fr;
  }
  
  .config-grid {
    grid-template-columns: 1fr;
  }
}
</style> 