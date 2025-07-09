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
          :formData="currentFormData"
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
const currentFormData = ref(null)
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
  currentFormData.value = formData
  
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
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

#app {
  min-height: 100vh;
  padding: 2rem;
  font-family: 'Inter', sans-serif;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Header styling */
.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 3rem;
  padding: 2rem;
  background: var(--surface-card);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--surface-border);
}

.title-section {
  flex: 1;
  position: relative;
}

h1 {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: 3.5rem;
  margin: 0 0 0.5rem 0;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-600) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  position: relative;
}

/* Professional SVG icons instead of emojis */
h1::before {
  content: '';
  width: 48px;
  height: 48px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%236366f1' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 2L2 7l10 5 10-5-10-5z'/%3E%3Cpath d='M2 17l10 5 10-5'/%3E%3Cpath d='M2 12l10 5 10-5'/%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  display: inline-block;
  margin-right: 1rem;
  animation: iconFloat 3s ease-in-out infinite;
  filter: drop-shadow(0 0 10px rgba(99, 102, 241, 0.4));
}

h1::after {
  content: '';
  width: 40px;
  height: 40px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%236366f1' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='3' y='3' width='18' height='18' rx='2' ry='2'/%3E%3Ccircle cx='9' cy='9' r='2'/%3E%3Cpath d='m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21'/%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  display: inline-block;
  margin-left: 1rem;
  animation: iconPulse 2.5s ease-in-out infinite;
  filter: drop-shadow(0 0 15px rgba(99, 102, 241, 0.5));
}

@keyframes iconFloat {
  0%, 100% {
    transform: translateY(0px) scale(1);
    filter: drop-shadow(0 0 10px rgba(99, 102, 241, 0.4));
  }
  50% {
    transform: translateY(-5px) scale(1.1);
    filter: drop-shadow(0 0 20px rgba(99, 102, 241, 0.6));
  }
}

@keyframes iconPulse {
  0%, 100% {
    transform: scale(1);
    filter: drop-shadow(0 0 15px rgba(99, 102, 241, 0.5));
  }
  50% {
    transform: scale(1.2);
    filter: drop-shadow(0 0 25px rgba(99, 102, 241, 0.7));
  }
}

/* Professional floating elements */
.title-section::before {
  content: '';
  position: absolute;
  width: 24px;
  height: 24px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%236366f1' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'/%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  top: -30px;
  left: -40px;
  animation: float 4s ease-in-out infinite;
  opacity: 0.7;
  filter: drop-shadow(0 0 8px rgba(99, 102, 241, 0.3));
}

.title-section::after {
  content: '';
  position: absolute;
  width: 24px;
  height: 24px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%236366f1' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolygon points='13 2 3 14 12 14 11 22 21 10 12 10 13 2'/%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  top: 30px;
  right: -40px;
  animation: float 4s ease-in-out infinite;
  animation-delay: 2s;
  opacity: 0.7;
  filter: drop-shadow(0 0 8px rgba(99, 102, 241, 0.3));
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
    opacity: 0.7;
  }
  50% {
    transform: translateY(-10px) rotate(5deg);
    opacity: 1;
  }
}

.subtitle {
  font-family: 'Inter', sans-serif;
  font-weight: 400;
  font-size: 1.125rem;
  color: var(--text-color-secondary);
  margin: 0;
  opacity: 0.9;
}

.theme-toggle {
  margin-top: 0.5rem;
}

/* Error styling */
.error {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 12px;
  margin: 2rem 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 500;
  box-shadow: 0 4px 20px rgba(255, 107, 107, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.error i {
  font-size: 1.25rem;
}

/* Dark mode variables */
:root.dark-mode {
  --surface-ground: #0d0d0d;
  --surface-card: #1e1e1e;
  --surface-section: #2a2a2a;
  --surface-border: #383838;
  --text-color: #ffffff;
  --text-color-secondary: #a0a0a0;
  --primary-color: #6366f1;
  --primary-600: #4f46e5;
  --primary-color-rgb: 99, 102, 241;
}

/* Light mode variables */
:root.light-mode {
  --surface-ground: #f8f9fa;
  --surface-card: #ffffff;
  --surface-section: #f1f3f4;
  --surface-border: #e1e5e9;
  --text-color: #1a1a1a;
  --text-color-secondary: #6b7280;
  --primary-color: #6366f1;
  --primary-600: #4f46e5;
  --primary-color-rgb: 99, 102, 241;
}

/* Body styling */
body {
  margin: 0;
  font-family: 'Inter', sans-serif;
  background: var(--surface-ground);
  color: var(--text-color);
  transition: background-color 0.3s ease, color 0.3s ease;
  line-height: 1.6;
  position: relative;
  overflow-x: hidden;
}

/* Cool animated backgrounds */
body::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background: 
    linear-gradient(45deg, transparent 30%, rgba(99, 102, 241, 0.1) 50%, transparent 70%),
    linear-gradient(-45deg, transparent 30%, rgba(168, 85, 247, 0.1) 50%, transparent 70%),
    radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(236, 72, 153, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(34, 197, 94, 0.1) 0%, transparent 50%);
  animation: backgroundShift 15s ease-in-out infinite;
}

/* Dark mode background - more cyberpunk */
:root.dark-mode body::before {
  background: 
    linear-gradient(45deg, transparent 30%, rgba(99, 102, 241, 0.2) 50%, transparent 70%),
    linear-gradient(-45deg, transparent 30%, rgba(168, 85, 247, 0.2) 50%, transparent 70%),
    radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.25) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(236, 72, 153, 0.25) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(34, 197, 94, 0.15) 0%, transparent 50%);
}

@keyframes backgroundShift {
  0%, 100% {
    transform: scale(1) rotate(0deg);
    opacity: 0.8;
  }
  25% {
    transform: scale(1.2) rotate(1deg);
    opacity: 1;
  }
  50% {
    transform: scale(0.9) rotate(-1deg);
    opacity: 0.6;
  }
  75% {
    transform: scale(1.1) rotate(0.5deg);
    opacity: 0.9;
  }
}

/* Add floating particles */
body::after {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background-image: 
    radial-gradient(circle at 25% 25%, rgba(99, 102, 241, 0.3) 1px, transparent 1px),
    radial-gradient(circle at 75% 75%, rgba(168, 85, 247, 0.3) 1px, transparent 1px),
    radial-gradient(circle at 50% 10%, rgba(34, 197, 94, 0.2) 1px, transparent 1px),
    radial-gradient(circle at 10% 50%, rgba(236, 72, 153, 0.2) 1px, transparent 1px);
  background-size: 60px 60px, 80px 80px, 40px 40px, 70px 70px;
  animation: particleFloat 25s linear infinite;
  opacity: 0.4;
}

:root.dark-mode body::after {
  background-image: 
    radial-gradient(circle at 25% 25%, rgba(99, 102, 241, 0.4) 1px, transparent 1px),
    radial-gradient(circle at 75% 75%, rgba(168, 85, 247, 0.4) 1px, transparent 1px),
    radial-gradient(circle at 50% 10%, rgba(34, 197, 94, 0.3) 1px, transparent 1px),
    radial-gradient(circle at 10% 50%, rgba(236, 72, 153, 0.3) 1px, transparent 1px);
  opacity: 0.6;
}

@keyframes particleFloat {
  0% {
    transform: translateY(0px) translateX(0px) rotate(0deg);
  }
  33% {
    transform: translateY(-30px) translateX(20px) rotate(1deg);
  }
  66% {
    transform: translateY(-60px) translateX(-10px) rotate(-1deg);
  }
  100% {
    transform: translateY(-90px) translateX(30px) rotate(0deg);
  }
}

/* Add circuit pattern overlay */
#app::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background-image: 
    linear-gradient(90deg, transparent 98%, rgba(99, 102, 241, 0.1) 100%),
    linear-gradient(0deg, transparent 98%, rgba(168, 85, 247, 0.1) 100%);
  background-size: 50px 50px;
  animation: circuitPulse 8s ease-in-out infinite;
  opacity: 0.3;
}

:root.dark-mode #app::before {
  background-image: 
    linear-gradient(90deg, transparent 98%, rgba(99, 102, 241, 0.2) 100%),
    linear-gradient(0deg, transparent 98%, rgba(168, 85, 247, 0.2) 100%);
  opacity: 0.5;
}

@keyframes circuitPulse {
  0%, 100% {
    opacity: 0.3;
  }
  50% {
    opacity: 0.6;
  }
}

/* Responsive design */
@media (max-width: 768px) {
  #app {
    padding: 1rem;
  }
  
  .header {
    flex-direction: column;
    gap: 1.5rem;
    text-align: center;
  }
  
  h1 {
    font-size: 2.5rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }
}

/* Smooth transitions */
* {
  transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: var(--surface-ground);
}

::-webkit-scrollbar-thumb {
  background: var(--surface-border);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--text-color-secondary);
}
</style>

