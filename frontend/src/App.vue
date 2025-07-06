<template>
  <div id="app">
    <div class="container">
      <div class="header">
        <div class="title-section">
          <h1>🔥 ThreatForge</h1>
          <p class="subtitle">AI-powered cybersecurity tabletop exercise generator</p>
        </div>
        <div class="theme-toggle">
          <Button 
            @click="toggleTheme" 
            :icon="isDark ? 'pi pi-sun' : 'pi pi-moon'"
            rounded
            text
            severity="secondary"
            aria-label="Toggle theme"
            v-tooltip="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
          />
        </div>
      </div>
      
      <ScenarioForm 
        @scenario-generated="handleGenerate" 
        :generating="generating"
      />

      <ProgressSpinner 
        v-if="generating" 
        style="width: 50px; height: 50px; margin: 2rem auto; display: block;"
      />
      
      <div v-if="error" class="error">
        <i class="pi pi-exclamation-triangle"></i> 
        <span>{{ error }}</span>
      </div>
      
      <div v-if="currentScenario">
        <ScenarioDisplay 
          :scenario="currentScenario"
          @regenerate="regenerate"
        />
      </div>
      
      <div v-else-if="!generating && !error">
        <p>No scenario generated yet.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Button from 'primevue/button'
import ProgressSpinner from 'primevue/progressspinner'
import ScenarioForm from './components/ScenarioForm.vue'
import ScenarioDisplay from './components/ScenarioDisplay.vue'

console.log('App.vue: Starting script setup')
console.log('App.vue: ScenarioForm component imported:', ScenarioForm)

const currentScenario = ref(null)
const error = ref(null)
const isDark = ref(true)
const generating = ref(false)

onMounted(() => {
  console.log('App.vue: onMounted called')
  
  // Check system preference or saved preference
  const savedTheme = localStorage.getItem('theme') || 'dark'
  isDark.value = savedTheme === 'dark'
  updateTheme()
  
  console.log('App.vue: onMounted completed')
})

const toggleTheme = () => {
  isDark.value = !isDark.value
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
  updateTheme()
}

const updateTheme = () => {
  const element = document.documentElement
  if (isDark.value) {
    element.classList.add('dark-mode')
    element.classList.remove('light-mode')
  } else {
    element.classList.add('light-mode')
    element.classList.remove('dark-mode')
  }
}

const handleGenerate = async (formData) => {
  console.log('App.vue: Generating scenario with data:', formData)
  error.value = null
  generating.value = true
  currentScenario.value = null
  
  try {
    const response = await axios.post('/api/scenarios/generate', formData)
    console.log('App.vue: API response received successfully')
    currentScenario.value = response.data
  } catch (err) {
    console.error('App.vue: API error:', err)
    error.value = err.response?.data?.detail || 'Failed to generate scenario'
  } finally {
    generating.value = false
  }
}

const regenerate = () => {
  currentScenario.value = null
  error.value = null
}
</script>

<style>


#app {
  min-height: 100vh;
  padding: 2rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  text-align: center;
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.subtitle {
  text-align: center;
  color: #888;
  margin-bottom: 3rem;
}

.error {
  background: #f44336;
  color: white;
  padding: 1rem;
  border-radius: 5px;
  margin: 1rem 0;
}

:root.dark-mode {
  --surface-ground: #0d0d0d;
  --surface-card: #1e1e1e;
  --surface-border: #383838;
  --text-color: #ffffff;
  --text-color-secondary: #888888;
}

:root.light-mode {
  --surface-ground: #f8f9fa;
  --surface-card: #ffffff;
  --surface-border: #dee2e6;
  --text-color: #212529;
  --text-color-secondary: #6c757d;
}

body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: var(--surface-ground);
  color: var(--text-color);
  transition: background-color 0.3s, color 0.3s;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 3rem;
}

.theme-toggle {
  margin-top: 1rem;
}

h1 {
  font-size: 3rem;
  margin-bottom: 0.5rem;
  margin-top: 0;
}

.subtitle {
  color: var(--text-color-secondary);
  margin: 0;
}

.error {
  background: #f44336;
  color: white;
  padding: 1rem;
  border-radius: 5px;
  margin: 1rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

</style>

