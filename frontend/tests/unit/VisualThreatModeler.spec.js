import { mount } from '@vue/test-utils'
import { describe, it, expect, beforeEach } from 'vitest'
import VisualThreatModeler from '@/components/VisualThreatModeler.vue'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Dropdown from 'primevue/dropdown'
import Textarea from 'primevue/textarea'
import Checkbox from 'primevue/checkbox'
import Calendar from 'primevue/calendar'

// Mock PrimeVue components
vi.mock('primevue/button', () => ({
  default: {
    name: 'Button',
    template: '<button><slot /></button>',
    props: ['icon', 'label', 'severity', 'size', 'loading', 'disabled', 'text']
  }
}))

vi.mock('primevue/dialog', () => ({
  default: {
    name: 'Dialog',
    template: '<div><slot /></div>',
    props: ['visible', 'header', 'style', 'modal']
  }
}))

describe('VisualThreatModeler', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(VisualThreatModeler, {
      global: {
        components: {
          Button,
          Dialog,
          InputText,
          Dropdown,
          Textarea,
          Checkbox,
          Calendar
        }
      }
    })
  })

  it('renders the visual threat modeler interface', () => {
    expect(wrapper.find('.visual-threat-modeler').exists()).toBe(true)
    expect(wrapper.find('.toolbar').exists()).toBe(true)
    expect(wrapper.find('.canvas-container').exists()).toBe(true)
    expect(wrapper.find('.component-library').exists()).toBe(true)
  })

  it('displays toolbar with action buttons', () => {
    const toolbar = wrapper.find('.toolbar')
    expect(toolbar.find('.toolbar-section h3').text()).toBe('Visual Threat Modeling')
    expect(toolbar.find('.toolbar-actions').exists()).toBe(true)
  })

  it('shows component library with categories', () => {
    const library = wrapper.find('.component-library')
    expect(library.find('h4').text()).toBe('Component Library')
    
    const categories = library.findAll('.category')
    expect(categories.length).toBeGreaterThan(0)
    
    // Check for expected categories
    const categoryTitles = categories.map(cat => cat.find('h5').text())
    expect(categoryTitles).toContain('External')
    expect(categoryTitles).toContain('Frontend')
    expect(categoryTitles).toContain('Backend')
    expect(categoryTitles).toContain('Security')
  })

  it('displays component templates in library', () => {
    const templates = wrapper.findAll('.component-template')
    expect(templates.length).toBeGreaterThan(0)
    
    // Check for common component types
    const templateTexts = templates.map(t => t.text())
    expect(templateTexts.some(text => text.includes('Internet'))).toBe(true)
    expect(templateTexts.some(text => text.includes('Web App'))).toBe(true)
    expect(templateTexts.some(text => text.includes('API Server'))).toBe(true)
    expect(templateTexts.some(text => text.includes('Database'))).toBe(true)
  })

  it('has draggable component templates', () => {
    const templates = wrapper.findAll('.component-template')
    templates.forEach(template => {
      expect(template.attributes('draggable')).toBe('true')
    })
  })

  it('shows empty canvas initially', () => {
    const canvas = wrapper.find('.canvas')
    expect(canvas.exists()).toBe(true)
    
    // Initially no components should be present
    const components = wrapper.findAll('.component')
    expect(components.length).toBe(0)
  })

  it('displays add component dialog when button is clicked', async () => {
    const addButton = wrapper.find('.toolbar-actions Button[label="Add Component"]')
    await addButton.trigger('click')
    
    expect(wrapper.vm.showComponentDialog).toBe(true)
  })

  it('can add components through dialog', async () => {
    // Open dialog
    wrapper.vm.showComponentDialog = true
    await wrapper.vm.$nextTick()
    
    // Fill form
    wrapper.vm.newComponent = {
      name: 'Test Component',
      type: 'frontend',
      description: 'Test description',
      x: 100,
      y: 100
    }
    
    // Add component
    await wrapper.vm.addComponent()
    
    expect(wrapper.vm.components.length).toBe(1)
    expect(wrapper.vm.components[0].name).toBe('Test Component')
    expect(wrapper.vm.showComponentDialog).toBe(false)
  })

  it('validates component form before adding', async () => {
    // Open dialog
    wrapper.vm.showComponentDialog = true
    await wrapper.vm.$nextTick()
    
    // Try to add without required fields
    wrapper.vm.newComponent = {
      name: '',
      type: '',
      description: '',
      x: 0,
      y: 0
    }
    
    await wrapper.vm.addComponent()
    
    // Component should not be added
    expect(wrapper.vm.components.length).toBe(0)
  })

  it('can remove components', async () => {
    // Add a component
    wrapper.vm.components = [{
      id: 1,
      name: 'Test Component',
      type: 'frontend',
      description: 'Test',
      x: 100,
      y: 100,
      threats: []
    }]
    
    // Remove component
    await wrapper.vm.removeComponent(1)
    
    expect(wrapper.vm.components.length).toBe(0)
  })

  it('can select components', async () => {
    // Add a component
    const component = {
      id: 1,
      name: 'Test Component',
      type: 'frontend',
      description: 'Test',
      x: 100,
      y: 100,
      threats: []
    }
    wrapper.vm.components = [component]
    
    // Select component
    await wrapper.vm.selectComponent(component)
    
    expect(wrapper.vm.selectedComponent).toBe(component)
  })

  it('can deselect components by clicking canvas', async () => {
    // Select a component first
    wrapper.vm.selectedComponent = { id: 1, name: 'Test' }
    
    // Click canvas to deselect
    await wrapper.vm.deselectAll()
    
    expect(wrapper.vm.selectedComponent).toBe(null)
  })

  it('shows threat mapping dialog when button is clicked', async () => {
    // Add a component first
    wrapper.vm.components = [{
      id: 1,
      name: 'Test Component',
      type: 'frontend',
      description: 'Test',
      x: 100,
      y: 100,
      threats: []
    }]
    
    const mapButton = wrapper.find('.toolbar-actions Button[label="Map Threats"]')
    await mapButton.trigger('click')
    
    expect(wrapper.vm.showThreatDialog).toBe(true)
  })

  it('can export diagram data', async () => {
    // Add components
    wrapper.vm.components = [
      {
        id: 1,
        name: 'Component 1',
        type: 'frontend',
        description: 'Test',
        x: 100,
        y: 100,
        threats: []
      },
      {
        id: 2,
        name: 'Component 2',
        type: 'backend',
        description: 'Test',
        x: 300,
        y: 100,
        threats: []
      }
    ]
    
    // Mock URL.createObjectURL and document.createElement
    const mockUrl = 'blob:test-url'
    const mockBlob = { type: 'application/json' }
    global.URL.createObjectURL = vi.fn().mockReturnValue(mockUrl)
    global.URL.revokeObjectURL = vi.fn()
    
    const mockAnchor = {
      href: '',
      download: '',
      click: vi.fn()
    }
    global.document.createElement = vi.fn().mockReturnValue(mockAnchor)
    
    // Export diagram
    await wrapper.vm.exportDiagram()
    
    expect(global.URL.createObjectURL).toHaveBeenCalled()
    expect(mockAnchor.click).toHaveBeenCalled()
    expect(global.URL.revokeObjectURL).toHaveBeenCalledWith(mockUrl)
  })

  it('can save diagram to local storage', async () => {
    // Mock localStorage
    const mockSetItem = vi.fn()
    global.localStorage = {
      setItem: mockSetItem
    }
    
    // Add components
    wrapper.vm.components = [{
      id: 1,
      name: 'Test Component',
      type: 'frontend',
      description: 'Test',
      x: 100,
      y: 100,
      threats: []
    }]
    
    // Save diagram
    await wrapper.vm.saveDiagram()
    
    expect(mockSetItem).toHaveBeenCalledWith(
      'threatModelDiagram',
      expect.stringContaining('Test Component')
    )
  })

  it('loads saved diagram from local storage on mount', async () => {
    const savedData = {
      components: [{
        id: 1,
        name: 'Saved Component',
        type: 'frontend',
        description: 'Saved',
        x: 100,
        y: 100,
        threats: []
      }],
      connections: []
    }
    
    // Mock localStorage
    global.localStorage = {
      getItem: vi.fn().mockReturnValue(JSON.stringify(savedData))
    }
    
    // Create new wrapper to trigger onMounted
    const newWrapper = mount(VisualThreatModeler, {
      global: {
        components: {
          Button,
          Dialog,
          InputText,
          Dropdown,
          Textarea,
          Checkbox,
          Calendar
        }
      }
    })
    
    await newWrapper.vm.$nextTick()
    
    expect(newWrapper.vm.components.length).toBe(1)
    expect(newWrapper.vm.components[0].name).toBe('Saved Component')
  })

  it('handles drag and drop events', async () => {
    const canvas = wrapper.find('.canvas')
    
    // Test drag over
    await canvas.trigger('dragover')
    expect(canvas.exists()).toBe(true)
    
    // Test drop with mock data
    const mockEvent = {
      preventDefault: vi.fn(),
      dataTransfer: {
        getData: vi.fn().mockReturnValue(JSON.stringify({
          type: 'frontend',
          name: 'Web App'
        }))
      },
      clientX: 200,
      clientY: 200
    }
    
    // Mock getBoundingClientRect
    canvas.element.getBoundingClientRect = vi.fn().mockReturnValue({
      left: 0,
      top: 0
    })
    
    await wrapper.vm.handleDrop(mockEvent)
    
    expect(wrapper.vm.components.length).toBe(1)
    expect(wrapper.vm.components[0].name).toBe('Web App')
  })

  it('generates correct component icons', () => {
    const iconTests = [
      { type: 'external', expected: 'pi pi-globe' },
      { type: 'frontend', expected: 'pi pi-desktop' },
      { type: 'backend', expected: 'pi pi-server' },
      { type: 'database', expected: 'pi pi-database' },
      { type: 'security', expected: 'pi pi-shield' },
      { type: 'infrastructure', expected: 'pi pi-sitemap' }
    ]
    
    iconTests.forEach(test => {
      const icon = wrapper.vm.getComponentIcon(test.type)
      expect(icon).toBe(test.expected)
    })
  })

  it('handles unknown component types gracefully', () => {
    const icon = wrapper.vm.getComponentIcon('unknown_type')
    expect(icon).toBe('pi pi-cube') // Default icon
  })
}) 