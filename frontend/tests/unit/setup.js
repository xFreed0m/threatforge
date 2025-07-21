// Polyfill window.matchMedia for jsdom
if (!window.matchMedia) {
  window.matchMedia = function (query) {
    return {
      matches: false,
      media: query,
      onchange: null,
      addListener: function () {},
      removeListener: function () {},
      addEventListener: function () {},
      removeEventListener: function () {},
      dispatchEvent: function () { return false; },
    };
  };
}

// Mock URL.createObjectURL for jsdom
global.URL.createObjectURL = global.URL.createObjectURL || (() => 'mock-url')

// Mock URL.revokeObjectURL in the test environment for jsdom.
global.URL.revokeObjectURL = global.URL.revokeObjectURL || (() => {})

// Register PrimeVue plugins/directives globally for tests
import { config } from '@vue/test-utils'
import PrimeVue from 'primevue/config'
import Tooltip from 'primevue/tooltip'

config.global.plugins = [PrimeVue]
config.global.directives = { tooltip: Tooltip } 