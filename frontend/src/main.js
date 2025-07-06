import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice'
import 'primeicons/primeicons.css'
import App from './App.vue'

console.log('main.js: Creating Vue app')
console.log('main.js: App component:', App)

const app = createApp(App)

console.log('main.js: Setting up PrimeVue')
app.use(PrimeVue, {
    theme: {
        name: 'aura-light-green',
        darkModeSelector: 'system',
        cssLayer: false
    }
})

app.use(ToastService)

console.log('main.js: Mounting app to #app')
app.mount('#app')
console.log('main.js: App mounted successfully')