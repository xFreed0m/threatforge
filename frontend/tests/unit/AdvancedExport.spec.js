import { mount } from '@vue/test-utils'
import { describe, it, expect, beforeEach } from 'vitest'
import AdvancedExport from '@/components/AdvancedExport.vue'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import Checkbox from 'primevue/checkbox'
import Dropdown from 'primevue/dropdown'
import MultiSelect from 'primevue/multiselect'
import InputText from 'primevue/inputtext'
import Calendar from 'primevue/calendar'

// Mock PrimeVue components
vi.mock('primevue/dialog', () => ({
  default: {
    name: 'Dialog',
    template: '<div><slot /></div>',
    props: ['visible', 'header', 'style', 'modal']
  }
}))

vi.mock('primevue/button', () => ({
  default: {
    name: 'Button',
    template: '<button><slot /></button>',
    props: ['label', 'loading', 'severity', 'icon', 'iconPos']
  }
}))

describe('AdvancedExport', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(AdvancedExport, {
      props: {
        visible: true,
        threatModel: {
          id: 'test-123',
          threat_model: 'Test threat model content',
          framework: 'STRIDE',
          provider_used: 'openai',
          estimated_cost: 0.05
        }
      },
      global: {
        components: {
          Dialog,
          Button,
          Checkbox,
          Dropdown,
          MultiSelect,
          InputText,
          Calendar
        }
      }
    })
  })

  it('renders the advanced export dialog', () => {
    expect(wrapper.find('.advanced-export').exists()).toBe(true)
    expect(wrapper.find('.export-content').exists()).toBe(true)
  })

  it('displays export type selection cards', () => {
    const exportTypes = wrapper.findAll('.export-type-card')
    expect(exportTypes.length).toBe(4)
    
    const typeLabels = exportTypes.map(card => card.find('h5').text())
    expect(typeLabels).toContain('PDF Report')
    expect(typeLabels).toContain('Executive Summary')
    expect(typeLabels).toContain('Technical Report')
    expect(typeLabels).toContain('Compliance Report')
  })

  it('allows selecting export type', async () => {
    const pdfCard = wrapper.findAll('.export-type-card')[0]
    await pdfCard.trigger('click')
    
    expect(wrapper.vm.selectedType).toBe('pdf')
    expect(pdfCard.classes()).toContain('selected')
  })

  it('shows configuration options for selected export type', async () => {
    // Select executive summary
    wrapper.vm.selectedType = 'executive'
    await wrapper.vm.$nextTick()
    
    // Should show executive summary specific options
    expect(wrapper.find('.config-group label').text()).toBe('Summary Level')
  })

  it('displays report configuration checkboxes', () => {
    const checkboxes = wrapper.findAll('.checkbox-item')
    expect(checkboxes.length).toBeGreaterThan(0)
    
    const checkboxLabels = checkboxes.map(cb => cb.find('span').text())
    expect(checkboxLabels).toContain('System Overview')
    expect(checkboxLabels).toContain('Threat Analysis')
    expect(checkboxLabels).toContain('Risk Assessment')
    expect(checkboxLabels).toContain('Mitigation Strategies')
  })

  it('allows configuring report sections', async () => {
    const overviewCheckbox = wrapper.find('.checkbox-item input[type="checkbox"]')
    await overviewCheckbox.setChecked(false)
    
    expect(wrapper.vm.config.includeOverview).toBe(false)
  })

  it('shows executive summary options when executive type is selected', async () => {
    wrapper.vm.selectedType = 'executive'
    await wrapper.vm.$nextTick()
    
    const summaryLevel = wrapper.find('.config-group label')
    expect(summaryLevel.text()).toBe('Summary Level')
  })

  it('shows compliance framework options when compliance type is selected', async () => {
    wrapper.vm.selectedType = 'compliance'
    await wrapper.vm.$nextTick()
    
    const frameworkLabel = wrapper.find('.config-group label')
    expect(frameworkLabel.text()).toBe('Framework')
  })

  it('displays report metadata form', () => {
    const metadataSection = wrapper.find('.export-section h4')
    expect(metadataSection.text()).toBe('Report Metadata')
    
    const formGroups = wrapper.findAll('.config-group')
    expect(formGroups.length).toBeGreaterThan(0)
  })

  it('allows editing report metadata', async () => {
    const titleInput = wrapper.find('input[placeholder="Enter report title"]')
    await titleInput.setValue('Custom Report Title')
    
    expect(wrapper.vm.metadata.title).toBe('Custom Report Title')
  })

  it('shows report preview based on configuration', () => {
    const previewSection = wrapper.find('.preview-sections')
    expect(previewSection.exists()).toBe(true)
    
    // Should show sections based on config
    const sections = wrapper.findAll('.preview-section')
    expect(sections.length).toBeGreaterThan(0)
  })

  it('updates preview when configuration changes', async () => {
    // Initially overview should be shown
    let sections = wrapper.findAll('.preview-section')
    const initialCount = sections.length
    
    // Disable overview
    wrapper.vm.config.includeOverview = false
    await wrapper.vm.$nextTick()
    
    sections = wrapper.findAll('.preview-section')
    expect(sections.length).toBeLessThan(initialCount)
  })

  it('generates PDF report when generate button is clicked', async () => {
    // Mock the generate function
    const mockGenerate = vi.fn()
    wrapper.vm.generateReport = mockGenerate
    
    const generateButton = wrapper.find('Button[label="Generate Report"]')
    await generateButton.trigger('click')
    
    expect(mockGenerate).toHaveBeenCalled()
  })

  it('shows loading state during report generation', async () => {
    wrapper.vm.generating = true
    await wrapper.vm.$nextTick()
    
    const generateButton = wrapper.find('Button[label="Generate Report"]')
    expect(generateButton.props('loading')).toBe(true)
  })

  it('generates correct PDF report structure', () => {
    const report = wrapper.vm.generatePDFReport()
    
    expect(report.type).toBe('pdf')
    expect(report.content).toHaveProperty('title')
    expect(report.content).toHaveProperty('sections')
    expect(report.content).toHaveProperty('config')
  })

  it('generates correct executive summary structure', () => {
    wrapper.vm.selectedType = 'executive'
    const report = wrapper.vm.generateExecutiveSummary()
    
    expect(report.type).toBe('executive')
    expect(report.content).toHaveProperty('title')
    expect(report.content).toHaveProperty('level')
    expect(report.content).toHaveProperty('focusAreas')
    expect(report.content).toHaveProperty('summary')
  })

  it('generates correct technical report structure', () => {
    wrapper.vm.selectedType = 'technical'
    const report = wrapper.vm.generateTechnicalReport()
    
    expect(report.type).toBe('technical')
    expect(report.content).toHaveProperty('title')
    expect(report.content).toHaveProperty('sections')
    expect(report.content).toHaveProperty('config')
  })

  it('generates correct compliance report structure', () => {
    wrapper.vm.selectedType = 'compliance'
    const report = wrapper.vm.generateComplianceReport()
    
    expect(report.type).toBe('compliance')
    expect(report.content).toHaveProperty('title')
    expect(report.content).toHaveProperty('framework')
    expect(report.content).toHaveProperty('includeControls')
    expect(report.content).toHaveProperty('sections')
  })

  it('includes correct sections based on configuration', () => {
    wrapper.vm.config.includeOverview = true
    wrapper.vm.config.includeThreats = true
    wrapper.vm.config.includeRisks = false
    wrapper.vm.config.includeMitigations = true
    
    const sections = wrapper.vm.getReportSections()
    
    expect(sections.length).toBe(3)
    expect(sections.some(s => s.title === 'System Overview')).toBe(true)
    expect(sections.some(s => s.title === 'Threat Analysis')).toBe(true)
    expect(sections.some(s => s.title === 'Risk Assessment')).toBe(false)
    expect(sections.some(s => s.title === 'Mitigation Strategies')).toBe(true)
  })

  it('generates technical sections correctly', () => {
    const sections = wrapper.vm.getTechnicalSections()
    
    expect(sections.length).toBe(4)
    expect(sections[0].title).toBe('Technical Architecture')
    expect(sections[1].title).toBe('Threat Modeling Methodology')
    expect(sections[2].title).toBe('Detailed Threat Analysis')
    expect(sections[3].title).toBe('Technical Mitigations')
  })

  it('generates compliance sections correctly', () => {
    wrapper.vm.complianceConfig.framework = 'iso27001'
    const sections = wrapper.vm.getComplianceSections()
    
    expect(sections.length).toBe(4)
    expect(sections[0].title).toBe('Compliance Framework')
    expect(sections[1].title).toBe('Control Mapping')
    expect(sections[2].title).toBe('Gap Analysis')
    expect(sections[3].title).toBe('Remediation Plan')
  })

  it('generates executive content with correct structure', () => {
    const content = wrapper.vm.generateExecutiveContent()
    
    expect(content).toHaveProperty('summary')
    expect(content).toHaveProperty('keyRisks')
    expect(content).toHaveProperty('recommendations')
    expect(content).toHaveProperty('timeline')
    expect(content).toHaveProperty('budget')
  })

  it('formats dates correctly', () => {
    const date = new Date('2024-01-01')
    const formatted = wrapper.vm.formatDate(date)
    
    expect(formatted).toBe('1/1/2024') // or locale-specific format
  })

  it('handles null dates gracefully', () => {
    const formatted = wrapper.vm.formatDate(null)
    expect(formatted).toBe('Not specified')
  })

  it('gets correct export type labels', () => {
    const labels = {
      pdf: 'PDF Report',
      executive: 'Executive Summary',
      technical: 'Technical Report',
      compliance: 'Compliance Report'
    }
    
    Object.entries(labels).forEach(([type, expectedLabel]) => {
      const label = wrapper.vm.getExportTypeLabel(type)
      expect(label).toBe(expectedLabel)
    })
  })

  it('downloads report file when export is triggered', async () => {
    // Mock browser APIs
    const mockBlob = { type: 'application/json' }
    const mockUrl = 'blob:test-url'
    global.Blob = vi.fn().mockReturnValue(mockBlob)
    global.URL.createObjectURL = vi.fn().mockReturnValue(mockUrl)
    global.URL.revokeObjectURL = vi.fn()
    
    const mockAnchor = {
      href: '',
      download: '',
      click: vi.fn()
    }
    global.document.createElement = vi.fn().mockReturnValue(mockAnchor)
    
    // Trigger download
    await wrapper.vm.downloadReport('test content', 'test-report.json')
    
    expect(global.URL.createObjectURL).toHaveBeenCalled()
    expect(mockAnchor.click).toHaveBeenCalled()
    expect(global.URL.revokeObjectURL).toHaveBeenCalledWith(mockUrl)
  })

  it('closes dialog when cancel button is clicked', async () => {
    const cancelButton = wrapper.find('Button[label="Cancel"]')
    await cancelButton.trigger('click')
    
    expect(wrapper.emitted('close')).toBeTruthy()
  })

  it('emits close event when closeDialog is called', async () => {
    await wrapper.vm.closeDialog()
    
    expect(wrapper.emitted('close')).toBeTruthy()
  })
}) 