import { mount, flushPromises } from '@vue/test-utils'
import ScenarioForm from '@/components/ScenarioForm.vue'
import PrimeVue from 'primevue/config'
import MultiSelect from 'primevue/multiselect'
import Chips from 'primevue/chips'
import Dropdown from 'primevue/dropdown'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import ToastService from 'primevue/toastservice'
import axios from 'axios'

vi.mock('axios')

describe('ScenarioForm.vue', () => {
  function factory(props = {}) {
    return mount(ScenarioForm, {
      global: {
        plugins: [PrimeVue, ToastService],
        components: { MultiSelect, Chips, Dropdown, Button, InputText, InputNumber }
      },
      props
    })
  }

  it('renders all required fields', () => {
    const wrapper = factory()
    expect(wrapper.find('input#company').exists()).toBe(true)
    expect(wrapper.find('input#industry').exists()).toBe(true)
    expect(wrapper.findComponent(MultiSelect).exists()).toBe(true)
    expect(wrapper.findComponent(Chips).exists()).toBe(true)
    expect(wrapper.findComponent(Dropdown).exists()).toBe(true)
    expect(wrapper.findComponent(InputNumber).exists()).toBe(true)
  })

  it('validates required fields', async () => {
    const wrapper = factory()
    await wrapper.find('button.generate-button').trigger('click')
    expect(wrapper.emitted('scenario-generated')).toBeFalsy()
    await wrapper.find('input#company').setValue('Acme')
    await wrapper.find('input#industry').setValue('Finance')
    await wrapper.find('button.generate-button').trigger('click')
    expect(wrapper.emitted('scenario-generated')).toBeTruthy()
  })

  it('template selection updates form fields', async () => {
    const wrapper = factory()
    await flushPromises()
    const dropdown = wrapper.findComponent(Dropdown)
    expect(dropdown.exists()).toBe(true)
    // Simulate template selection
    wrapper.vm.selectedTemplate = 'ransomware_healthcare'
    await wrapper.vm.onTemplateChange({ value: 'ransomware_healthcare' })
    await flushPromises()
    expect(wrapper.vm.form.industry).toBe('Healthcare')
    expect(wrapper.vm.form.threat_actor).toBe('ransomware')
  })

  it('emits scenario-generated with correct data', async () => {
    const wrapper = factory()
    await wrapper.find('input#company').setValue('Acme')
    await wrapper.find('input#industry').setValue('Finance')
    await wrapper.find('button.generate-button').trigger('click')
    const emitted = wrapper.emitted('scenario-generated')
    expect(emitted).toBeTruthy()
    expect(emitted[0][0].company_name).toBe('Acme')
    expect(emitted[0][0].industry).toBe('Finance')
  })

  it('shows loading state when generating', async () => {
    const wrapper = factory({ generating: true })
    expect(wrapper.find('button.generate-button').attributes('disabled')).toBeDefined()
  })
}) 