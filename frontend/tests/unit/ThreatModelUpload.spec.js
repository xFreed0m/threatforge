import { mount, flushPromises } from '@vue/test-utils'
import ThreatModelUpload from '@/components/ThreatModelUpload.vue'
import axios from 'axios'

jest.mock('axios')

describe('ThreatModelUpload.vue', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('validates file type and size', async () => {
    const wrapper = mount(ThreatModelUpload)
    const input = wrapper.find('input[type="file"]')
    // Invalid type
    await input.setValue({
      target: { files: [new File(['abc'], 'test.exe', { type: 'application/octet-stream', size: 100 })] }
    })
    expect(wrapper.text()).toContain('Unsupported file type')
    // Too large
    await input.setValue({
      target: { files: [new File(['a'.repeat(11 * 1024 * 1024)], 'big.png', { type: 'image/png', size: 11 * 1024 * 1024 })] }
    })
    expect(wrapper.text()).toContain('File too large')
  })

  it('uploads a file and refreshes list', async () => {
    axios.get.mockResolvedValueOnce({ data: [] }) // initial fetch
    axios.post.mockResolvedValueOnce({})
    axios.get.mockResolvedValueOnce({ data: [{ file_id: '1', filename: 'diagram.drawio', file_type: 'drawio', size: 1234 }] })
    const wrapper = mount(ThreatModelUpload)
    await flushPromises()
    // Set a valid file
    const file = new File(['abc'], 'diagram.drawio', { type: 'application/octet-stream', size: 1234 })
    wrapper.vm.selectedFiles = [file]
    await wrapper.vm.handleUpload()
    expect(axios.post).toHaveBeenCalled()
    await flushPromises()
    expect(wrapper.text()).toContain('diagram.drawio')
  })

  it('deletes a file and refreshes list', async () => {
    axios.get.mockResolvedValueOnce({ data: [{ file_id: '1', filename: 'diagram.svg', file_type: 'svg', size: 1234 }] })
    axios.delete.mockResolvedValueOnce({})
    axios.get.mockResolvedValueOnce({ data: [] })
    const wrapper = mount(ThreatModelUpload)
    await flushPromises()
    await wrapper.vm.deleteFile('1')
    expect(axios.delete).toHaveBeenCalledWith('/api/threat-model/files/1')
    await flushPromises()
    expect(wrapper.text()).not.toContain('diagram.svg')
  })

  it('supports drag and drop', async () => {
    const wrapper = mount(ThreatModelUpload)
    const dropArea = wrapper.find('.drop-area')
    const file = new File(['abc'], 'diagram.drawio', { type: 'application/octet-stream', size: 1234 })
    
    await dropArea.trigger('drop', {
      dataTransfer: {
        files: [file]
      }
    })
    
    expect(wrapper.vm.selectedFiles).toHaveLength(1)
    expect(wrapper.vm.selectedFiles[0].name).toBe('diagram.drawio')
  })

  it('supports multi-file upload', async () => {
    const wrapper = mount(ThreatModelUpload)
    const input = wrapper.find('input[type="file"]')
    const file1 = new File(['abc'], 'diagram1.drawio', { type: 'application/octet-stream', size: 1234 })
    const file2 = new File(['def'], 'diagram2.drawio', { type: 'application/octet-stream', size: 5678 })
    
    await input.setValue({
      target: { files: [file1, file2] }
    })
    
    expect(wrapper.vm.selectedFiles).toHaveLength(2)
    expect(wrapper.vm.selectedFiles[0].name).toBe('diagram1.drawio')
    expect(wrapper.vm.selectedFiles[1].name).toBe('diagram2.drawio')
  })

  it('shows upload progress', async () => {
    const wrapper = mount(ThreatModelUpload)
    const file = new File(['abc'], 'diagram.drawio', { type: 'application/octet-stream', size: 1234 })
    wrapper.vm.selectedFiles = [file]
    
    // Mock XMLHttpRequest for progress tracking
    const mockXHR = {
      open: jest.fn(),
      send: jest.fn(),
      upload: {
        onprogress: null
      },
      onload: null,
      onerror: null
    }
    global.XMLHttpRequest = jest.fn(() => mockXHR)
    
    wrapper.vm.handleUpload()
    
    // Simulate progress
    mockXHR.upload.onprogress({ loaded: 50, total: 100 })
    expect(wrapper.vm.uploadProgress['diagram.drawio']).toBe(50)
  })

  it('supports bulk delete', async () => {
    axios.get.mockResolvedValueOnce({ 
      data: [
        { file_id: '1', filename: 'diagram1.drawio', file_type: 'drawio', size: 1234 },
        { file_id: '2', filename: 'diagram2.drawio', file_type: 'drawio', size: 5678 }
      ] 
    })
    axios.delete.mockResolvedValueOnce({})
    axios.get.mockResolvedValueOnce({ data: [] })
    
    const wrapper = mount(ThreatModelUpload)
    await flushPromises()
    
    wrapper.vm.selectedToDelete = ['1', '2']
    await wrapper.vm.bulkDelete()
    
    expect(axios.delete).toHaveBeenCalledTimes(2)
    await flushPromises()
    expect(wrapper.text()).not.toContain('diagram1.drawio')
    expect(wrapper.text()).not.toContain('diagram2.drawio')
  })

  // New tests for AI-powered threat model generation
  it('loads providers on mount', async () => {
    axios.get.mockResolvedValueOnce({ data: [] }) // files
    axios.get.mockResolvedValueOnce({ data: { providers: ['openai', 'anthropic'] } }) // providers
    
    const wrapper = mount(ThreatModelUpload)
    await flushPromises()
    
    expect(wrapper.vm.availableProviders).toEqual(['openai', 'anthropic'])
    expect(wrapper.vm.form.llm_provider).toBe('openai')
  })

  it('generates threat model successfully', async () => {
    axios.get.mockResolvedValueOnce({ data: [] }) // files
    axios.get.mockResolvedValueOnce({ data: { providers: ['openai'] } }) // providers
    axios.post.mockResolvedValueOnce({
      data: {
        id: '123',
        threat_model: 'Generated threat model content',
        estimated_cost: 0.05,
        provider_used: 'openai',
        framework: 'STRIDE',
        content_analyzed: 'Test content'
      }
    })
    
    const wrapper = mount(ThreatModelUpload)
    await flushPromises()
    
    wrapper.vm.form.content = 'Test system description'
    wrapper.vm.form.framework = 'STRIDE'
    wrapper.vm.form.llm_provider = 'openai'
    
    await wrapper.vm.generateThreatModel()
    
    expect(axios.post).toHaveBeenCalledWith('/api/threat-model/generate', {
      content: 'Test system description',
      framework: 'STRIDE',
      file_id: null,
      llm_provider: 'openai'
    })
    
    expect(wrapper.vm.currentThreatModel).toBeTruthy()
    expect(wrapper.vm.currentThreatModel.threat_model).toBe('Generated threat model content')
  })

  it('validates form before generation', async () => {
    axios.get.mockResolvedValueOnce({ data: [] }) // files
    axios.get.mockResolvedValueOnce({ data: { providers: ['openai'] } }) // providers
    
    const wrapper = mount(ThreatModelUpload)
    await flushPromises()
    
    // Initially form should be invalid (no content)
    expect(wrapper.vm.isFormValid).toBe(false)
    
    // Add content and form should be valid
    wrapper.vm.form.content = 'Test content'
    expect(wrapper.vm.isFormValid).toBe(true)
  })

  it('handles generation errors', async () => {
    axios.get.mockResolvedValueOnce({ data: [] }) // files
    axios.get.mockResolvedValueOnce({ data: { providers: ['openai'] } }) // providers
    axios.post.mockRejectedValueOnce(new Error('Generation failed'))
    
    const wrapper = mount(ThreatModelUpload)
    await flushPromises()
    
    wrapper.vm.form.content = 'Test content'
    wrapper.vm.form.llm_provider = 'openai'
    
    await wrapper.vm.generateThreatModel()
    
    expect(wrapper.vm.generating).toBe(false)
    // Should show error toast (would need to mock toast)
  })

  it('compares costs successfully', async () => {
    axios.get.mockResolvedValueOnce({ data: [] }) // files
    axios.get.mockResolvedValueOnce({ data: { providers: ['openai', 'anthropic'] } }) // providers
    axios.post.mockResolvedValueOnce({
      data: [
        { provider: 'openai', estimated_cost: 0.05 },
        { provider: 'anthropic', estimated_cost: 0.03 }
      ]
    })
    
    const wrapper = mount(ThreatModelUpload)
    await flushPromises()
    
    wrapper.vm.form.content = 'Test content'
    wrapper.vm.form.llm_provider = 'openai'
    
    await wrapper.vm.compareCosts()
    
    expect(axios.post).toHaveBeenCalledWith('/api/threat-model/estimate-cost', {
      content: 'Test content',
      framework: 'STRIDE',
      file_id: null,
      llm_provider: 'openai'
    })
    
    expect(wrapper.vm.costEstimates).toHaveLength(2)
    expect(wrapper.vm.showCostDialog).toBe(true)
  })
}) 