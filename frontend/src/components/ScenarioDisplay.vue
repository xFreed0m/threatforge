<template>
  <!-- Simple scenario display -->
  <div v-if="scenario && scenario.scenario" style="background: #e8f5e8; padding: 1rem; margin: 1rem 0; border: 1px solid #4caf50;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
      <h3>Generated Scenario</h3>
      <div style="display: flex; gap: 1rem;">
        <Chip :label="`Cost: $${scenario.estimated_cost.toFixed(4)}`" icon="pi pi-dollar" />
        <Chip :label="`Provider: ${scenario.provider_used}`" icon="pi pi-server" />
      </div>
    </div>
    <p><strong>ID:</strong> {{ scenario.id }}</p>
    
    <!-- Parsed sections display -->
    <div v-if="parsedSections.length > 0" style="margin: 1rem 0;">
      <div v-for="(section, index) in parsedSections" :key="index" style="background: white; padding: 1rem; margin-bottom: 1rem; border: 1px solid #ddd; border-radius: 4px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
          <h4 style="margin: 0; color: #2196f3;">{{ section.title }}</h4>
          <Button 
            @click="rerollSection(section.title)" 
            icon="pi pi-refresh" 
            size="small"
            text
            rounded
            v-tooltip="'Regenerate this section'"
          />
        </div>
        <div style="white-space: pre-wrap; word-wrap: break-word; line-height: 1.6;">{{ section.content }}</div>
      </div>
    </div>
    
    <!-- Fallback to raw text if no sections found -->
    <div v-else style="background: white; padding: 1rem; margin: 1rem 0; border: 1px solid #ddd; border-radius: 4px; max-height: 400px; overflow-y: auto;">
      <h4>Scenario Content (Raw):</h4>
      <pre style="white-space: pre-wrap;">{{ scenario.scenario }}</pre>
    </div>
    
    <div style="display: flex; gap: 1rem; margin-top: 1rem;">
      <Button @click="$emit('regenerate')" label="Regenerate" icon="pi pi-refresh" />
      <Button @click="copyToClipboard" label="Copy" icon="pi pi-copy" severity="secondary" />
      <Button @click="exportScenario" label="Export" icon="pi pi-download" severity="secondary" />
    </div>
    <Toast />
  </div>
  
  <!-- Fallback when scenario exists but no content -->
  <div v-else-if="scenario" style="background: #fff3cd; padding: 1rem; margin: 1rem 0; border: 1px solid #ffc107;">
    <h3>Debug: Scenario Received but No Content</h3>
    <pre>{{ JSON.stringify(scenario, null, 2) }}</pre>
  </div>
  
  <!-- Fallback when no scenario -->
  <div v-else style="background: #f8d7da; padding: 1rem; margin: 1rem 0; border: 1px solid #dc3545;">
    <h3>No Scenario Available</h3>
    <p>Generate a scenario to see it displayed here.</p>
  </div>
</template>

<script setup>
import { computed, watch } from 'vue'
import { useToast } from 'primevue/usetoast'
import Button from 'primevue/button'
import Chip from 'primevue/chip'
import Toast from 'primevue/toast'

const props = defineProps({
  scenario: Object
})

const emit = defineEmits(['regenerate', 'reroll-section'])
const toast = useToast()

// Debug logging
console.log('ScenarioDisplay received props:', props.scenario)
console.log('Scenario object keys:', props.scenario ? Object.keys(props.scenario) : 'No scenario')
console.log('Scenario.scenario value:', props.scenario?.scenario)
console.log('Component should render:', !!props.scenario)

// Watch for prop changes
watch(() => props.scenario, (newScenario, oldScenario) => {
  console.log('ScenarioDisplay prop changed:', {
    old: oldScenario,
    new: newScenario,
    oldKeys: oldScenario ? Object.keys(oldScenario) : null,
    newKeys: newScenario ? Object.keys(newScenario) : null
  })
}, { immediate: true, deep: true })

const parsedSections = computed(() => {
  try {
    if (!props.scenario || !props.scenario.scenario) {
      console.log('parsedSections: No scenario or scenario.scenario')
      return []
    }
    
    const text = props.scenario.scenario
    console.log('parsedSections: Processing text:', text.substring(0, 100) + '...')
    
    const sections = []
    const lines = text.split('\n')
    let currentSection = null
    
    for (const line of lines) {
      // Match markdown headers: ##, ###, ####, etc. followed by text
      // OR ALL CAPS headers (with or without colons)
      if (line.match(/^#{2,}\s+/) || line.match(/^[A-Z][A-Z\s]+:?$/)) {
        if (currentSection) {
          sections.push(currentSection)
        }
        const title = line.replace(/^#{2,}\s+/, '').replace(/:$/, '').trim()
        currentSection = {
          title: title,
          content: ''
        }
      } else if (currentSection) {
        currentSection.content += line + '\n'
      }
    }
    
    if (currentSection) {
      sections.push(currentSection)
    }
    
    console.log('parsedSections: Found sections:', sections.length)
    return sections
  } catch (error) {
    console.error('Error in parsedSections:', error)
    return []
  }
})

const rerollSection = (sectionTitle) => {
  toast.add({
    severity: 'info',
    summary: 'Re-roll Coming Soon',
    detail: `Re-rolling "${sectionTitle}" will be implemented next!`,
    life: 3000
  })
}

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(props.scenario.scenario)
    toast.add({
      severity: 'success',
      summary: 'Copied!',
      detail: 'Scenario copied to clipboard',
      life: 2000
    })
  } catch (err) {
    console.error('Failed to copy to clipboard:', err)
    toast.add({
      severity: 'error',
      summary: 'Failed to copy',
      detail: 'Please try again or use the export feature',
      life: 3000
    })
  }
}

const exportScenario = () => {
  try {
    const blob = new Blob([props.scenario.scenario], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `threatforge-scenario-${props.scenario.id}.txt`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    
    toast.add({
      severity: 'success',
      summary: 'Exported!',
      detail: 'Scenario downloaded successfully',
      life: 2000
    })
  } catch (err) {
    console.error('Failed to export scenario:', err)
    toast.add({
      severity: 'error',
      summary: 'Export Failed',
      detail: 'Please try again',
      life: 3000
    })
  }
}
</script>

<style scoped>
/* No styles for now to keep it simple */
</style>