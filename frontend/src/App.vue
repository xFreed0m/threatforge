<template>
  <div id="app">
    <h1>🔥 ThreatForge</h1>
    <p>AI-powered cybersecurity tabletop exercise generator</p>
    <p>API Status: {{ apiStatus }}</p>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'App',
  setup() {
    const apiStatus = ref('Checking...')
    
    onMounted(async () => {
      try {
        const response = await axios.get('/api/health')
        apiStatus.value = '✅ Connected'
      } catch (error) {
        apiStatus.value = '❌ Disconnected'
      }
    })
    
    return { apiStatus }
  }
}
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  text-align: center;
  margin-top: 50px;
}
</style>
