import { mount } from '@vue/test-utils'
import CostComparison from '@/components/CostComparison.vue'
import PrimeVue from 'primevue/config'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import ProgressSpinner from 'primevue/progressspinner'

// Mock PrimeVue Dialog to always render slot content
vi.mock('primevue/dialog', () => ({
  default: {
    name: 'Dialog',
    template: '<div><slot /></div>'
  }
}))

describe('CostComparison.vue', () => {
  const estimates = [
    { provider: 'openai', estimated_cost: 0.01 },
    { provider: 'anthropic', estimated_cost: 0.02 },
    { provider: 'other', estimated_cost: 0.03 }
  ]
  function factory(props = {}) {
    return mount(CostComparison, {
      global: {
        plugins: [PrimeVue],
        components: { Dialog, Button, ProgressSpinner }
      },
      props: {
        estimates: [
          { provider: 'openai', estimated_cost: 0.01 },
          { provider: 'anthropic', estimated_cost: 0.02 },
        ],
        loading: false,
        visible: true,
        selectedProvider: 'openai',
        ...props,
      },
    })
  }

  it('displays cost estimates and formatting', () => {
    const wrapper = factory()
    expect(wrapper.text()).toContain('openai')
    expect(wrapper.text()).toContain('$0.0100')
    expect(wrapper.text()).toContain('anthropic')
    expect(wrapper.text()).toContain('$0.0200')
  })

  it('emits select-provider event when Select is clicked', async () => {
    const wrapper = factory({ visible: true, loading: false })
    // Directly call the select method to simulate provider selection
    wrapper.vm.select('openai')
    await wrapper.vm.$nextTick()
    expect(wrapper.emitted('select-provider')).toBeTruthy()
    expect(wrapper.emitted('select-provider')[0][0]).toBe('openai')
  })

  it('shows loading state', () => {
    const wrapper = factory({ loading: true })
    expect(wrapper.text()).toContain('Estimating costs')
  })
}) 