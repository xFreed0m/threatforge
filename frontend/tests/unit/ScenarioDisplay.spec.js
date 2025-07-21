import { mount, flushPromises } from '@vue/test-utils'
import ScenarioDisplay from '@/components/ScenarioDisplay.vue'
import PrimeVue from 'primevue/config'
import Button from 'primevue/button'
import ToastService from 'primevue/toastservice'
import SplitButton from 'primevue/splitbutton'
import axios from 'axios'

vi.mock('axios')

describe('ScenarioDisplay.vue', () => {
  const scenario = {
    id: 'abc123',
    scenario: '## Section One\nContent one\n## Section Two\nContent two',
    estimated_cost: 0.0123,
    provider_used: 'openai',
    formData: { company_name: 'Acme', industry: 'Finance' }
  }
  function factory(props = {}) {
    return mount(ScenarioDisplay, {
      global: {
        plugins: [PrimeVue, ToastService],
        components: { Button, SplitButton }
      },
      props: { scenario, ...props }
    })
  }

  it('parses and displays scenario sections', () => {
    const wrapper = factory()
    expect(wrapper.findAll('.section-card').length).toBe(2)
    expect(wrapper.text()).toContain('Section One')
    expect(wrapper.text()).toContain('Section Two')
  })

  it('calls rerollSection on reroll button click', async () => {
    axios.post.mockResolvedValue({ data: { new_content: 'new content' } })
    const wrapper = factory()
    await wrapper.findAll('.reroll-button')[0].trigger('click')
    await flushPromises()
    expect(wrapper.text()).toContain('new content')
  })

  it('shows loading state during reroll', async () => {
    axios.post.mockImplementation(() => new Promise(resolve => setTimeout(() => resolve({ data: { new_content: 'new content' } }), 100)))
    const wrapper = factory()
    wrapper.vm.rerollSection('Section One')
    await flushPromises()
    expect(wrapper.vm.rerollingSection).toBe('Section One')
  })

  it('exports scenario as text, markdown, json, pdf', async () => {
    const wrapper = factory()
    const spy = vi.spyOn(document, 'createElement')
    wrapper.vm.exportScenario('txt')
    wrapper.vm.exportScenario('md')
    wrapper.vm.exportScenario('json')
    wrapper.vm.exportScenario('pdf')
    expect(spy).toHaveBeenCalled()
    spy.mockRestore()
  })
}) 