<template>
  <div class="visual-threat-modeler">
    <div class="toolbar">
      <div class="toolbar-section">
        <h3>Visual Threat Modeling</h3>
        <p>Create interactive system diagrams and map threats visually</p>
      </div>
      
      <div class="toolbar-actions">
        <Button 
          icon="pi pi-plus" 
          label="Add Component"
          @click="showComponentDialog = true"
          severity="primary"
        />
        <Button 
          icon="pi pi-shield" 
          label="Map Threats"
          @click="mapThreats"
          :disabled="!hasComponents"
          severity="secondary"
        />
        <Button 
          icon="pi pi-download" 
          label="Export Diagram"
          @click="exportDiagram"
          :disabled="!hasComponents"
          severity="secondary"
        />
        <Button 
          icon="pi pi-save" 
          label="Save"
          @click="saveDiagram"
          :disabled="!hasComponents"
          severity="success"
        />
      </div>
    </div>

    <div class="canvas-container">
      <div class="canvas" 
           ref="canvas"
           @drop="handleDrop"
           @dragover="handleDragOver"
           @click="deselectAll">
        
        <!-- System Components -->
        <div v-for="component in components" 
             :key="component.id"
             :class="['component', component.type, { selected: selectedComponent?.id === component.id }]"
             :style="{ left: component.x + 'px', top: component.y + 'px' }"
             @click.stop="selectComponent(component)"
             @mousedown="startDrag(component, $event)"
             draggable="true">
          
          <div class="component-header">
            <i :class="getComponentIcon(component.type)"></i>
            <span class="component-name">{{ component.name }}</span>
            <Button 
              icon="pi pi-times" 
              @click.stop="removeComponent(component.id)"
              severity="danger"
              text
              size="small"
            />
          </div>
          
          <div class="component-content">
            <div class="component-type">{{ component.type }}</div>
            <div class="component-description">{{ component.description }}</div>
          </div>

          <!-- Threat Indicators -->
          <div v-if="component.threats && component.threats.length > 0" class="threat-indicators">
            <div v-for="threat in component.threats" 
                 :key="threat.id"
                 :class="['threat-indicator', threat.severity]"
                 :title="threat.description">
              <i class="pi pi-exclamation-triangle"></i>
            </div>
          </div>
        </div>

        <!-- Connections -->
        <svg class="connections" :width="canvasWidth" :height="canvasHeight">
          <defs>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" 
                    refX="9" refY="3.5" orient="auto">
              <polygon points="0 0, 10 3.5, 0 7" fill="#666" />
            </marker>
          </defs>
          <line v-for="connection in connections" 
                :key="connection.id"
                :x1="connection.from.x" 
                :y1="connection.from.y"
                :x2="connection.to.x" 
                :y2="connection.to.y"
                stroke="#666" 
                stroke-width="2"
                marker-end="url(#arrowhead)" />
        </svg>
      </div>
    </div>

    <!-- Component Library Sidebar -->
    <div class="component-library">
      <h4>Component Library</h4>
      <div class="component-categories">
        <div class="category">
          <h5>External</h5>
          <div class="component-templates">
            <div class="component-template external" 
                 draggable="true"
                 @dragstart="handleDragStart($event, 'external', 'Internet')">
              <i class="pi pi-globe"></i>
              <span>Internet</span>
            </div>
            <div class="component-template external" 
                 draggable="true"
                 @dragstart="handleDragStart($event, 'external', 'User')">
              <i class="pi pi-user"></i>
              <span>User</span>
            </div>
          </div>
        </div>

        <div class="category">
          <h5>Frontend</h5>
          <div class="component-templates">
            <div class="component-template frontend" 
                 draggable="true"
                 @dragstart="handleDragStart($event, 'frontend', 'Web App')">
              <i class="pi pi-desktop"></i>
              <span>Web App</span>
            </div>
            <div class="component-template frontend" 
                 draggable="true"
                 @dragstart="handleDragStart($event, 'frontend', 'Mobile App')">
              <i class="pi pi-mobile"></i>
              <span>Mobile App</span>
            </div>
          </div>
        </div>

        <div class="category">
          <h5>Backend</h5>
          <div class="component-templates">
            <div class="component-template backend" 
                 draggable="true"
                 @dragstart="handleDragStart($event, 'backend', 'API Server')">
              <i class="pi pi-server"></i>
              <span>API Server</span>
            </div>
            <div class="component-template backend" 
                 draggable="true"
                 @dragstart="handleDragStart($event, 'backend', 'Database')">
              <i class="pi pi-database"></i>
              <span>Database</span>
            </div>
          </div>
        </div>

        <div class="category">
          <h5>Security</h5>
          <div class="component-templates">
            <div class="component-template security" 
                 draggable="true"
                 @dragstart="handleDragStart($event, 'security', 'Firewall')">
              <i class="pi pi-shield"></i>
              <span>Firewall</span>
            </div>
            <div class="component-template security" 
                 draggable="true"
                 @dragstart="handleDragStart($event, 'security', 'Load Balancer')">
              <i class="pi pi-sitemap"></i>
              <span>Load Balancer</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Component Dialog -->
    <Dialog v-model:visible="showComponentDialog" 
            header="Add Component" 
            :style="{ width: '500px' }"
            :modal="true">
      <div class="component-form">
        <div class="form-group">
          <label>Component Name</label>
          <InputText v-model="newComponent.name" placeholder="Enter component name" />
        </div>
        
        <div class="form-group">
          <label>Component Type</label>
          <Dropdown v-model="newComponent.type" 
                   :options="componentTypes" 
                   optionLabel="label"
                   optionValue="value"
                   placeholder="Select component type" />
        </div>
        
        <div class="form-group">
          <label>Description</label>
          <Textarea v-model="newComponent.description" 
                   placeholder="Describe the component's purpose and functionality"
                   rows="3" />
        </div>
      </div>
      
      <template #footer>
        <Button label="Cancel" @click="showComponentDialog = false" severity="secondary" />
        <Button label="Add Component" @click="addComponent" severity="primary" />
      </template>
    </Dialog>

    <!-- Threat Mapping Dialog -->
    <Dialog v-model:visible="showThreatDialog" 
            header="Map Threats to Components" 
            :style="{ width: '800px' }"
            :modal="true">
      <div class="threat-mapping">
        <div v-for="component in components" :key="component.id" class="component-threats">
          <h5>{{ component.name }}</h5>
          <div class="threat-list">
            <div v-for="threat in availableThreats" :key="threat.id" class="threat-item">
              <Checkbox v-model="component.threats" 
                       :value="threat" 
                       :binary="false" />
              <span class="threat-name">{{ threat.name }}</span>
              <span :class="['threat-severity', threat.severity]">{{ threat.severity }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <Button label="Cancel" @click="showThreatDialog = false" severity="secondary" />
        <Button label="Apply Threats" @click="applyThreats" severity="primary" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Dropdown from 'primevue/dropdown'
import Textarea from 'primevue/textarea'
import Checkbox from 'primevue/checkbox'
import { useToast } from 'primevue/usetoast'

const toast = useToast()

// Canvas state
const canvas = ref(null)
const canvasWidth = ref(1200)
const canvasHeight = ref(800)

// Components and connections
const components = ref([])
const connections = ref([])
const selectedComponent = ref(null)

// Dialogs
const showComponentDialog = ref(false)
const showThreatDialog = ref(false)

// New component form
const newComponent = ref({
  name: '',
  type: '',
  description: '',
  x: 0,
  y: 0
})

// Component types
const componentTypes = [
  { label: 'External', value: 'external' },
  { label: 'Frontend', value: 'frontend' },
  { label: 'Backend', value: 'backend' },
  { label: 'Database', value: 'database' },
  { label: 'Security', value: 'security' },
  { label: 'Infrastructure', value: 'infrastructure' }
]

// Available threats (STRIDE framework)
const availableThreats = ref([
  { id: 1, name: 'Spoofing', severity: 'high', description: 'Authentication/identity threats' },
  { id: 2, name: 'Tampering', severity: 'high', description: 'Data integrity threats' },
  { id: 3, name: 'Repudiation', severity: 'medium', description: 'Non-repudiation threats' },
  { id: 4, name: 'Information Disclosure', severity: 'high', description: 'Confidentiality threats' },
  { id: 5, name: 'Denial of Service', severity: 'medium', description: 'Availability threats' },
  { id: 6, name: 'Elevation of Privilege', severity: 'high', description: 'Authorization threats' }
])

// Computed properties
const hasComponents = computed(() => components.value.length > 0)

// Component methods
const getComponentIcon = (type) => {
  const icons = {
    external: 'pi pi-globe',
    frontend: 'pi pi-desktop',
    backend: 'pi pi-server',
    database: 'pi pi-database',
    security: 'pi pi-shield',
    infrastructure: 'pi pi-sitemap'
  }
  return icons[type] || 'pi pi-cube'
}

const addComponent = () => {
  if (!newComponent.value.name || !newComponent.value.type) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Please fill in all required fields',
      life: 3000
    })
    return
  }

  const component = {
    id: Date.now(),
    name: newComponent.value.name,
    type: newComponent.value.type,
    description: newComponent.value.description,
    x: Math.random() * (canvasWidth.value - 200),
    y: Math.random() * (canvasHeight.value - 100),
    threats: []
  }

  components.value.push(component)
  
  // Reset form
  newComponent.value = {
    name: '',
    type: '',
    description: '',
    x: 0,
    y: 0
  }
  
  showComponentDialog.value = false
  
  toast.add({
    severity: 'success',
    summary: 'Success',
    detail: 'Component added successfully',
    life: 3000
  })
}

const removeComponent = (id) => {
  components.value = components.value.filter(c => c.id !== id)
  connections.value = connections.value.filter(c => c.fromId !== id && c.toId !== id)
  
  if (selectedComponent.value?.id === id) {
    selectedComponent.value = null
  }
}

const selectComponent = (component) => {
  selectedComponent.value = component
}

const deselectAll = () => {
  selectedComponent.value = null
}

// Drag and drop
const handleDragStart = (event, type, name) => {
  event.dataTransfer.setData('application/json', JSON.stringify({ type, name }))
}

const handleDragOver = (event) => {
  event.preventDefault()
}

const handleDrop = (event) => {
  event.preventDefault()
  const data = JSON.parse(event.dataTransfer.getData('application/json'))
  
  const rect = canvas.value.getBoundingClientRect()
  const x = event.clientX - rect.left
  const y = event.clientY - rect.top
  
  const component = {
    id: Date.now(),
    name: data.name,
    type: data.type,
    description: `Automatically added ${data.name} component`,
    x: x - 100,
    y: y - 50,
    threats: []
  }
  
  components.value.push(component)
}

// Drag component
const startDrag = (component, event) => {
  // Implementation for dragging components
}

// Threat mapping
const mapThreats = () => {
  showThreatDialog.value = true
}

const applyThreats = () => {
  showThreatDialog.value = false
  toast.add({
    severity: 'success',
    summary: 'Success',
    detail: 'Threats mapped to components',
    life: 3000
  })
}

// Export and save
const exportDiagram = () => {
  const diagramData = {
    components: components.value,
    connections: connections.value,
    metadata: {
      created: new Date().toISOString(),
      version: '1.0'
    }
  }
  
  const blob = new Blob([JSON.stringify(diagramData, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'threat-model-diagram.json'
  a.click()
  URL.revokeObjectURL(url)
  
  toast.add({
    severity: 'success',
    summary: 'Success',
    detail: 'Diagram exported successfully',
    life: 3000
  })
}

const saveDiagram = () => {
  // Save to local storage or backend
  localStorage.setItem('threatModelDiagram', JSON.stringify({
    components: components.value,
    connections: connections.value
  }))
  
  toast.add({
    severity: 'success',
    summary: 'Success',
    detail: 'Diagram saved successfully',
    life: 3000
  })
}

// Load saved diagram
onMounted(() => {
  const saved = localStorage.getItem('threatModelDiagram')
  if (saved) {
    const data = JSON.parse(saved)
    components.value = data.components || []
    connections.value = data.connections || []
  }
})
</script>

<style scoped>
.visual-threat-modeler {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--surface-ground);
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: var(--surface-card);
  border-bottom: 1px solid var(--surface-border);
}

.toolbar-section h3 {
  margin: 0 0 0.25rem 0;
  color: var(--text-color);
}

.toolbar-section p {
  margin: 0;
  color: var(--text-color-secondary);
  font-size: 0.9rem;
}

.toolbar-actions {
  display: flex;
  gap: 0.5rem;
}

.canvas-container {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.canvas {
  width: 100%;
  height: 100%;
  position: relative;
  background: var(--surface-ground);
  cursor: crosshair;
}

.component {
  position: absolute;
  width: 200px;
  background: var(--surface-card);
  border: 2px solid var(--surface-border);
  border-radius: 8px;
  padding: 1rem;
  cursor: move;
  transition: all 0.3s ease;
  z-index: 10;
}

.component:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.component.selected {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px var(--primary-200);
}

.component.external {
  border-left: 4px solid var(--orange-500);
}

.component.frontend {
  border-left: 4px solid var(--blue-500);
}

.component.backend {
  border-left: 4px solid var(--green-500);
}

.component.database {
  border-left: 4px solid var(--purple-500);
}

.component.security {
  border-left: 4px solid var(--red-500);
}

.component.infrastructure {
  border-left: 4px solid var(--gray-500);
}

.component-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.component-header i {
  color: var(--primary-color);
  font-size: 1.2rem;
}

.component-name {
  font-weight: 600;
  color: var(--text-color);
  flex: 1;
}

.component-content {
  font-size: 0.9rem;
}

.component-type {
  color: var(--text-color-secondary);
  font-size: 0.8rem;
  text-transform: uppercase;
  margin-bottom: 0.25rem;
}

.component-description {
  color: var(--text-color-secondary);
  line-height: 1.4;
}

.threat-indicators {
  position: absolute;
  top: -8px;
  right: -8px;
  display: flex;
  gap: 2px;
}

.threat-indicator {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
}

.threat-indicator.high {
  background: var(--red-500);
  color: white;
}

.threat-indicator.medium {
  background: var(--orange-500);
  color: white;
}

.threat-indicator.low {
  background: var(--green-500);
  color: white;
}

.connections {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: none;
  z-index: 5;
}

.component-library {
  width: 250px;
  background: var(--surface-card);
  border-left: 1px solid var(--surface-border);
  padding: 1rem;
  overflow-y: auto;
}

.component-library h4 {
  margin: 0 0 1rem 0;
  color: var(--text-color);
}

.component-categories {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.category h5 {
  margin: 0 0 0.5rem 0;
  color: var(--text-color);
  font-size: 0.9rem;
}

.component-templates {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.component-template {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border: 1px solid var(--surface-border);
  border-radius: 4px;
  cursor: grab;
  transition: all 0.2s ease;
  font-size: 0.9rem;
}

.component-template:hover {
  background: var(--surface-hover);
  border-color: var(--primary-color);
}

.component-template:active {
  cursor: grabbing;
}

.component-template.external {
  border-left: 3px solid var(--orange-500);
}

.component-template.frontend {
  border-left: 3px solid var(--blue-500);
}

.component-template.backend {
  border-left: 3px solid var(--green-500);
}

.component-template.security {
  border-left: 3px solid var(--red-500);
}

.component-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: var(--text-color);
}

.threat-mapping {
  max-height: 400px;
  overflow-y: auto;
}

.component-threats {
  margin-bottom: 1.5rem;
  padding: 1rem;
  border: 1px solid var(--surface-border);
  border-radius: 8px;
}

.component-threats h5 {
  margin: 0 0 1rem 0;
  color: var(--text-color);
}

.threat-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.threat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  background: var(--surface-section);
  border-radius: 4px;
}

.threat-name {
  flex: 1;
  color: var(--text-color);
}

.threat-severity {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.threat-severity.high {
  background: var(--red-100);
  color: var(--red-700);
}

.threat-severity.medium {
  background: var(--orange-100);
  color: var(--orange-700);
}

.threat-severity.low {
  background: var(--green-100);
  color: var(--green-700);
}

@media (max-width: 768px) {
  .toolbar {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .toolbar-actions {
    justify-content: center;
  }
  
  .component-library {
    width: 100%;
    border-left: none;
    border-top: 1px solid var(--surface-border);
  }
}
</style> 