<template>
  <div class="visual-threat-modeler">
    <!-- Error Boundary -->
    <div v-if="error" class="error-boundary">
      <div class="error-content">
        <i class="pi pi-exclamation-triangle"></i>
        <h4>Something went wrong</h4>
        <p>{{ error }}</p>
        <Button @click="clearError" label="Dismiss" severity="secondary" />
      </div>
    </div>

    <div class="toolbar">
      <div class="toolbar-section">
        <h3>Visual Threat Modeling</h3>
        <p>Create interactive system diagrams and map threats visually</p>
        <div class="toolbar-stats">
          <span class="stat">
            <i class="pi pi-cube"></i>
            {{ components.length }} Components
          </span>
          <span class="stat">
            <i class="pi pi-shield"></i>
            {{ totalThreats }} Threats
          </span>
          <span class="stat">
            <i class="pi pi-link"></i>
            {{ connections.length }} Connections
          </span>
        </div>
      </div>
      
      <div class="toolbar-actions">
        <Button 
          icon="pi pi-plus" 
          label="Add Component"
          @click="showComponentDialog = true"
          severity="primary"
          :loading="addingComponent"
        />
        <Button 
          icon="pi pi-shield" 
          label="Map Threats"
          @click="mapThreats"
          :disabled="!hasComponents || mappingThreats"
          :loading="mappingThreats"
          severity="secondary"
        />
        <Button 
          icon="pi pi-download" 
          label="Export Diagram"
          @click="exportDiagram"
          :disabled="!hasComponents || exporting"
          :loading="exporting"
          severity="secondary"
        />
        <Button 
          icon="pi pi-save" 
          label="Save"
          @click="saveDiagram"
          :disabled="!hasComponents || saving"
          :loading="saving"
          severity="success"
        />
        <Button 
          icon="pi pi-undo" 
          label="Undo"
          @click="undo"
          :disabled="!canUndo"
          severity="secondary"
          text
        />
        <Button 
          icon="pi pi-redo" 
          label="Redo"
          @click="redo"
          :disabled="!canRedo"
          severity="secondary"
          text
        />
      </div>
    </div>

    <div class="canvas-container">
      <!-- Canvas Controls -->
      <div class="canvas-controls">
        <Button 
          icon="pi pi-search-plus" 
          @click="zoomIn"
          severity="secondary"
          text
          size="small"
        />
        <Button 
          icon="pi pi-search-minus" 
          @click="zoomOut"
          severity="secondary"
          text
          size="small"
        />
        <Button 
          icon="pi pi-refresh" 
          @click="resetZoom"
          severity="secondary"
          text
          size="small"
        />
        <span class="zoom-level">{{ Math.round(zoom * 100) }}%</span>
      </div>

      <div class="canvas" 
           ref="canvas"
           @drop="handleDrop"
           @dragover="handleDragOver"
           @dragenter="handleDragEnter"
           @dragleave="handleDragLeave"
           @click="deselectAll"
           :class="{ 'drag-over': isDragOver }">
        
        <!-- System Components -->
        <div v-for="component in visibleComponents" 
             :key="component.id"
             :class="['component', component.type, { selected: selectedComponent?.id === component.id }]"
             :style="{ 
               left: (component.x * zoom) + 'px', 
               top: (component.y * zoom) + 'px',
               transform: `scale(${zoom})`
             }"
             @click.stop="selectComponent(component)"
             @mousedown="startDrag(component, $event)"
                             @contextmenu="handleContextMenu(component, $event)"
             draggable="true">
          
          <div class="component-header">
            <i :class="getComponentIcon(component.type)"></i>
            <span class="component-name">{{ component.name }}</span>
            <div class="component-actions">
              <Button 
                icon="pi pi-cog" 
                @click.stop="editComponent(component)"
                severity="secondary"
                text
                size="small"
              />
              <Button 
                icon="pi pi-times" 
                @click.stop="removeComponent(component.id)"
                severity="danger"
                text
                size="small"
              />
            </div>
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
                 :title="`${threat.name}: ${threat.description}`"
                 @click.stop="showThreatDetails(threat)">
              <i class="pi pi-exclamation-triangle"></i>
              <span class="threat-count" v-if="component.threats.length > 1">{{ component.threats.length }}</span>
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
            <marker id="arrowhead-selected" markerWidth="12" markerHeight="8" 
                    refX="10" refY="4" orient="auto">
              <polygon points="0 0, 12 4, 0 8" fill="#007bff" />
            </marker>
          </defs>
          <line v-for="connection in connections" 
                :key="connection.id"
                :x1="connection.from.x * zoom" 
                :y1="connection.from.y * zoom"
                :x2="connection.to.x * zoom" 
                :y2="connection.to.y * zoom"
                :stroke="selectedConnection?.id === connection.id ? '#007bff' : '#666'"
                :stroke-width="selectedConnection?.id === connection.id ? '3' : '2'"
                :marker-end="selectedConnection?.id === connection.id ? 'url(#arrowhead-selected)' : 'url(#arrowhead)'"
                @click="selectConnection(connection)" />
        </svg>

        <!-- Grid (optional) -->
        <div v-if="showGrid" class="grid-overlay"></div>
      </div>
    </div>

    <!-- Component Library Sidebar -->
    <div class="component-library">
      <div class="library-header">
        <h4>Component Library</h4>
        <Button 
          icon="pi pi-cog" 
          @click="showLibrarySettings = true"
          severity="secondary"
          text
          size="small"
        />
      </div>
      
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
            <div class="component-template external" 
                 draggable="true"
                 @dragstart="handleDragStart($event, 'external', 'Third Party')">
              <i class="pi pi-building"></i>
              <span>Third Party</span>
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
            <div class="component-template frontend" 
                 draggable="true"
                 @dragstart="handleDragStart($event, 'frontend', 'SPA')">
              <i class="pi pi-window-maximize"></i>
              <span>SPA</span>
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
            <div class="component-template backend" 
                 draggable="true"
                 @dragstart="handleDragStart($event, 'backend', 'Cache')">
              <i class="pi pi-bolt"></i>
              <span>Cache</span>
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
            <div class="component-template security" 
                 draggable="true"
                 @dragstart="handleDragStart($event, 'security', 'WAF')">
              <i class="pi pi-shield-check"></i>
              <span>WAF</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Component Dialog -->
    <Dialog :visible="showComponentDialog" 
            @update:visible="showComponentDialog = $event"
            header="Add Component" 
            :style="{ width: '500px' }"
            :modal="true"
            :closable="!addingComponent">
      <div class="component-form">
        <div class="form-group">
          <label>Component Name *</label>
          <InputText 
            v-model="newComponent.name" 
            placeholder="Enter component name"
            :class="{ 'p-invalid': validationErrors.name }"
            @input="validateComponent"
          />
          <small v-if="validationErrors.name" class="p-error">{{ validationErrors.name }}</small>
        </div>
        
        <div class="form-group">
          <label>Component Type *</label>
          <Dropdown 
            v-model="newComponent.type" 
            :options="componentTypes" 
            optionLabel="label"
            optionValue="value"
            placeholder="Select component type"
            :class="{ 'p-invalid': validationErrors.type }"
            @change="validateComponent"
          />
          <small v-if="validationErrors.type" class="p-error">{{ validationErrors.type }}</small>
        </div>
        
        <div class="form-group">
          <label>Description</label>
          <Textarea 
            v-model="newComponent.description" 
            placeholder="Describe the component's purpose and functionality"
            rows="3"
            maxlength="500"
          />
          <small class="form-help">{{ newComponent.description.length }}/500 characters</small>
        </div>
      </div>
      
      <template #footer>
        <Button 
          label="Cancel" 
          @click="showComponentDialog = false" 
          severity="secondary"
          :disabled="addingComponent"
        />
        <Button 
          label="Add Component" 
          @click="addComponent" 
          severity="primary"
          :loading="addingComponent"
          :disabled="!isComponentValid"
        />
      </template>
    </Dialog>

    <!-- Threat Mapping Dialog -->
    <Dialog :visible="showThreatDialog" 
            @update:visible="showThreatDialog = $event"
            header="Map Threats to Components" 
            :style="{ width: '900px' }"
            :modal="true"
            :closable="!mappingThreats">
      <div class="threat-mapping">
        <div class="mapping-header">
          <p>Select threats to map to each component. Threats will be visually indicated on the diagram.</p>
          <div class="mapping-actions">
            <Button 
              label="Select All High Risk"
              @click="selectAllHighRisk"
              severity="warning"
              size="small"
            />
            <Button 
              label="Clear All"
              @click="clearAllThreats"
              severity="secondary"
              size="small"
            />
          </div>
        </div>
        
        <div v-for="component in components" :key="component.id" class="component-threats">
          <h5>{{ component.name }}</h5>
          <div class="threat-list">
            <div v-for="threat in availableThreats" :key="threat.id" class="threat-item">
              <Checkbox 
                v-model="component.threats" 
                :value="threat" 
                :binary="false"
                :disabled="mappingThreats"
              />
              <span class="threat-name">{{ threat.name }}</span>
              <span :class="['threat-severity', threat.severity]">{{ threat.severity }}</span>
              <span class="threat-description">{{ threat.description }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <Button 
          label="Cancel" 
          @click="showThreatDialog = false" 
          severity="secondary"
          :disabled="mappingThreats"
        />
        <Button 
          label="Apply Threats" 
          @click="applyThreats" 
          severity="primary"
          :loading="mappingThreats"
        />
      </template>
    </Dialog>

    <!-- Context Menu -->
    <div v-if="showContextMenu" 
         class="context-menu"
         :style="{ left: contextMenuPosition.x + 'px', top: contextMenuPosition.y + 'px' }"
         @click.stop>
      <div class="context-menu-item" @click="editSelectedComponent">
        <i class="pi pi-pencil"></i>
        <span>Edit</span>
      </div>
      <div class="context-menu-item" @click="duplicateSelectedComponent">
        <i class="pi pi-copy"></i>
        <span>Duplicate</span>
      </div>
      <div class="context-menu-item danger" @click="removeSelectedComponent">
        <i class="pi pi-trash"></i>
        <span>Delete</span>
      </div>
    </div>

    <!-- Threat Details Dialog -->
    <Dialog :visible="showThreatDetailsDialog" 
            @update:visible="showThreatDetailsDialog = $event"
            header="Threat Details" 
            :style="{ width: '600px' }"
            :modal="true">
      <div v-if="selectedThreat" class="threat-details">
        <h4>{{ selectedThreat.name }}</h4>
        <div class="threat-meta">
          <span :class="['threat-severity', selectedThreat.severity]">{{ selectedThreat.severity }}</span>
          <span class="threat-category">{{ selectedThreat.category }}</span>
        </div>
        <p class="threat-description">{{ selectedThreat.description }}</p>
        <div class="threat-mitigation">
          <h5>Mitigation Strategies:</h5>
          <ul>
            <li v-for="mitigation in selectedThreat.mitigations" :key="mitigation">{{ mitigation }}</li>
          </ul>
        </div>
      </div>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch, onUnmounted } from 'vue'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Dropdown from 'primevue/dropdown'
import Textarea from 'primevue/textarea'
import Checkbox from 'primevue/checkbox'
import Calendar from 'primevue/calendar'
import { useToast } from 'primevue/usetoast'

const toast = useToast()

// Error handling
const error = ref(null)

// Canvas state
const canvas = ref(null)
const canvasWidth = ref(1200)
const canvasHeight = ref(800)
const zoom = ref(1)
const showGrid = ref(false)
const isDragOver = ref(false)

// Components and connections
const components = ref([])
const connections = ref([])
const selectedComponent = ref(null)
const selectedConnection = ref(null)

// Dialogs
const showComponentDialog = ref(false)
const showThreatDialog = ref(false)
const showThreatDetailsDialog = ref(false)
const showLibrarySettings = ref(false)

// Loading states
const addingComponent = ref(false)
const mappingThreats = ref(false)
const exporting = ref(false)
const saving = ref(false)

// Context menu
const showContextMenu = ref(false)
const contextMenuPosition = ref({ x: 0, y: 0 })
const selectedThreat = ref(null)

// New component form
const newComponent = ref({
  name: '',
  type: '',
  description: '',
  x: 0,
  y: 0
})

// Validation
const validationErrors = ref({})
const isComponentValid = computed(() => {
  return newComponent.value.name.trim() && 
         newComponent.value.type && 
         !validationErrors.value.name && 
         !validationErrors.value.type
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
  { 
    id: 1, 
    name: 'Spoofing', 
    severity: 'high', 
    category: 'Authentication',
    description: 'Authentication/identity threats',
    mitigations: [
      'Implement strong authentication mechanisms',
      'Use multi-factor authentication',
      'Validate user identity before granting access'
    ]
  },
  { 
    id: 2, 
    name: 'Tampering', 
    severity: 'high', 
    category: 'Integrity',
    description: 'Data integrity threats',
    mitigations: [
      'Implement data validation and sanitization',
      'Use digital signatures for critical data',
      'Implement checksums and hashing'
    ]
  },
  { 
    id: 3, 
    name: 'Repudiation', 
    severity: 'medium', 
    category: 'Non-repudiation',
    description: 'Non-repudiation threats',
    mitigations: [
      'Implement comprehensive audit logging',
      'Use digital signatures for transactions',
      'Store logs in tamper-evident storage'
    ]
  },
  { 
    id: 4, 
    name: 'Information Disclosure', 
    severity: 'high', 
    category: 'Confidentiality',
    description: 'Confidentiality threats',
    mitigations: [
      'Implement data encryption at rest and in transit',
      'Use access controls and authorization',
      'Implement data classification and handling'
    ]
  },
  { 
    id: 5, 
    name: 'Denial of Service', 
    severity: 'medium', 
    category: 'Availability',
    description: 'Availability threats',
    mitigations: [
      'Implement rate limiting and throttling',
      'Use load balancing and redundancy',
      'Monitor system resources and performance'
    ]
  },
  { 
    id: 6, 
    name: 'Elevation of Privilege', 
    severity: 'high', 
    category: 'Authorization',
    description: 'Authorization threats',
    mitigations: [
      'Implement principle of least privilege',
      'Use role-based access control (RBAC)',
      'Regular access reviews and audits'
    ]
  }
])

// Undo/Redo functionality
const history = ref([])
const historyIndex = ref(-1)
const maxHistorySize = 50

// Computed properties
const hasComponents = computed(() => components.value.length > 0)
const canUndo = computed(() => historyIndex.value > 0)
const canRedo = computed(() => historyIndex.value < history.value.length - 1)
const totalThreats = computed(() => {
  return components.value.reduce((total, component) => {
    return total + (component.threats?.length || 0)
  }, 0)
})

// Visible components (for performance optimization)
const visibleComponents = computed(() => {
  // In a real implementation, this would filter components based on viewport
  return components.value
})

// Methods
const clearError = () => {
  error.value = null
}

const handleError = (err, context = 'Operation') => {
  console.error(`${context} error:`, err)
  error.value = `${context} failed: ${err.message || err}`
  toast.add({
    severity: 'error',
    summary: 'Error',
    detail: error.value,
    life: 5000
  })
}

const validateComponent = () => {
  validationErrors.value = {}
  
  if (!newComponent.value.name.trim()) {
    validationErrors.value.name = 'Component name is required'
  } else if (newComponent.value.name.length > 50) {
    validationErrors.value.name = 'Component name must be less than 50 characters'
  }
  
  if (!newComponent.value.type) {
    validationErrors.value.type = 'Component type is required'
  }
}

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

const saveToHistory = () => {
  const state = {
    components: JSON.parse(JSON.stringify(components.value)),
    connections: JSON.parse(JSON.stringify(connections.value))
  }
  
  // Remove any future history if we're not at the end
  if (historyIndex.value < history.value.length - 1) {
    history.value = history.value.slice(0, historyIndex.value + 1)
  }
  
  history.value.push(state)
  historyIndex.value++
  
  // Limit history size
  if (history.value.length > maxHistorySize) {
    history.value.shift()
    historyIndex.value--
  }
}

const undo = () => {
  if (canUndo.value) {
    historyIndex.value--
    const state = history.value[historyIndex.value]
    components.value = JSON.parse(JSON.stringify(state.components))
    connections.value = JSON.parse(JSON.stringify(state.connections))
  }
}

const redo = () => {
  if (canRedo.value) {
    historyIndex.value++
    const state = history.value[historyIndex.value]
    components.value = JSON.parse(JSON.stringify(state.components))
    connections.value = JSON.parse(JSON.stringify(state.connections))
  }
}

const addComponent = async () => {
  if (!isComponentValid.value) {
    toast.add({
      severity: 'error',
      summary: 'Validation Error',
      detail: 'Please fix validation errors',
      life: 3000
    })
    return
  }
  
  addingComponent.value = true
  
  try {
    const component = {
      id: Date.now() + Math.random(),
      name: newComponent.value.name.trim(),
      type: newComponent.value.type,
      description: newComponent.value.description.trim(),
      x: Math.random() * (canvasWidth.value - 200),
      y: Math.random() * (canvasHeight.value - 100),
      threats: []
    }
    
    components.value.push(component)
    saveToHistory()
    
    // Reset form
    newComponent.value = {
      name: '',
      type: '',
      description: '',
      x: 0,
      y: 0
    }
    validationErrors.value = {}
    
    showComponentDialog.value = false
    
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'Component added successfully',
      life: 3000
    })
  } catch (err) {
    handleError(err, 'Adding component')
  } finally {
    addingComponent.value = false
  }
}

const removeComponent = (id) => {
  try {
    components.value = components.value.filter(c => c.id !== id)
    connections.value = connections.value.filter(c => c.fromId !== id && c.toId !== id)
    
    if (selectedComponent.value?.id === id) {
      selectedComponent.value = null
    }
    
    saveToHistory()
    
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'Component removed successfully',
      life: 3000
    })
  } catch (err) {
    handleError(err, 'Removing component')
  }
}

const selectComponent = (component) => {
  selectedComponent.value = component
  selectedConnection.value = null
}

const deselectAll = () => {
  selectedComponent.value = null
  selectedConnection.value = null
  showContextMenu.value = false
}

const selectConnection = (connection) => {
  selectedConnection.value = connection
  selectedComponent.value = null
}

// Drag and drop
const handleDragStart = (event, type, name) => {
  try {
    event.dataTransfer.setData('application/json', JSON.stringify({ type, name }))
    event.dataTransfer.effectAllowed = 'copy'
  } catch (err) {
    handleError(err, 'Drag start')
  }
}

const handleDragOver = (event) => {
  event.preventDefault()
  event.dataTransfer.dropEffect = 'copy'
}

const handleDragEnter = (event) => {
  event.preventDefault()
  isDragOver.value = true
}

const handleDragLeave = (event) => {
  if (!event.currentTarget.contains(event.relatedTarget)) {
    isDragOver.value = false
  }
}

const handleDrop = (event) => {
  event.preventDefault()
  isDragOver.value = false
  
  try {
    const data = JSON.parse(event.dataTransfer.getData('application/json'))
    
    const rect = canvas.value.getBoundingClientRect()
    const x = (event.clientX - rect.left) / zoom.value
    const y = (event.clientY - rect.top) / zoom.value
    
    const component = {
      id: Date.now() + Math.random(),
      name: data.name,
      type: data.type,
      description: `Automatically added ${data.name} component`,
      x: Math.max(0, Math.min(x - 100, canvasWidth.value - 200)),
      y: Math.max(0, Math.min(y - 50, canvasHeight.value - 100)),
      threats: []
    }
    
    components.value.push(component)
    saveToHistory()
    
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: `${data.name} component added`,
      life: 2000
    })
  } catch (err) {
    handleError(err, 'Drop operation')
  }
}

// Drag component
const startDrag = (component, event) => {
  // Implementation for dragging components
  // This would be implemented with mouse event handlers
}

// Zoom controls
const zoomIn = () => {
  zoom.value = Math.min(zoom.value * 1.2, 3)
}

const zoomOut = () => {
  zoom.value = Math.max(zoom.value / 1.2, 0.1)
}

const resetZoom = () => {
  zoom.value = 1
}

// Context menu
const handleContextMenu = (component, event) => {
  event.preventDefault()
  contextMenuPosition.value = { x: event.clientX, y: event.clientY }
  selectedComponent.value = component
  showContextMenu.value = true
}

const editSelectedComponent = () => {
  if (selectedComponent.value) {
    newComponent.value = { ...selectedComponent.value }
    showComponentDialog.value = true
  }
  showContextMenu.value = false
}

const duplicateSelectedComponent = () => {
  if (selectedComponent.value) {
    const duplicate = {
      ...selectedComponent.value,
      id: Date.now() + Math.random(),
      x: selectedComponent.value.x + 20,
      y: selectedComponent.value.y + 20
    }
    components.value.push(duplicate)
    saveToHistory()
  }
  showContextMenu.value = false
}

const removeSelectedComponent = () => {
  if (selectedComponent.value) {
    removeComponent(selectedComponent.value.id)
  }
  showContextMenu.value = false
}

// Threat mapping
const mapThreats = () => {
  showThreatDialog.value = true
}

const selectAllHighRisk = () => {
  const highRiskThreats = availableThreats.value.filter(t => t.severity === 'high')
  components.value.forEach(component => {
    component.threats = [...highRiskThreats]
  })
}

const clearAllThreats = () => {
  components.value.forEach(component => {
    component.threats = []
  })
}

const applyThreats = async () => {
  mappingThreats.value = true
  
  try {
    // Simulate processing time
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    showThreatDialog.value = false
    
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'Threats mapped to components',
      life: 3000
    })
  } catch (err) {
    handleError(err, 'Mapping threats')
  } finally {
    mappingThreats.value = false
  }
}

const showThreatDetails = (threat) => {
  selectedThreat.value = threat
  showThreatDetailsDialog.value = true
}

// Export and save
const exportDiagram = async () => {
  exporting.value = true
  
  try {
    const diagramData = {
      components: components.value,
      connections: connections.value,
      metadata: {
        created: new Date().toISOString(),
        version: '1.0',
        totalComponents: components.value.length,
        totalThreats: totalThreats.value,
        totalConnections: connections.value.length
      }
    }
    
    const blob = new Blob([JSON.stringify(diagramData, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `threat-model-diagram-${Date.now()}.json`
    a.click()
    URL.revokeObjectURL(url)
    
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'Diagram exported successfully',
      life: 3000
    })
  } catch (err) {
    handleError(err, 'Exporting diagram')
  } finally {
    exporting.value = false
  }
}

const saveDiagram = async () => {
  saving.value = true
  
  try {
    // Save to local storage
    localStorage.setItem('threatModelDiagram', JSON.stringify({
      components: components.value,
      connections: connections.value,
      lastSaved: new Date().toISOString()
    }))
    
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'Diagram saved successfully',
      life: 3000
    })
  } catch (err) {
    handleError(err, 'Saving diagram')
  } finally {
    saving.value = false
  }
}

// Load saved diagram
onMounted(() => {
  try {
    const saved = localStorage.getItem('threatModelDiagram')
    if (saved) {
      const data = JSON.parse(saved)
      components.value = data.components || []
      connections.value = data.connections || []
      
      // Initialize history
      if (components.value.length > 0 || connections.value.length > 0) {
        saveToHistory()
      }
    }
  } catch (err) {
    handleError(err, 'Loading saved diagram')
  }
})

// Close context menu when clicking outside
onMounted(() => {
  document.addEventListener('click', () => {
    showContextMenu.value = false
  })
})

onUnmounted(() => {
  document.removeEventListener('click', () => {
    showContextMenu.value = false
  })
})

// Watch for changes and save to history
watch([components, connections], () => {
  // Don't save to history during initial load
  if (history.value.length > 0) {
    saveToHistory()
  }
}, { deep: true })
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

.toolbar-stats {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: var(--text-color-secondary);
}

.toolbar-stats i {
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

.canvas-controls {
  position: absolute;
  top: 1rem;
  left: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--surface-card);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  z-index: 10;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.zoom-level {
  font-size: 0.8rem;
  color: var(--text-color-secondary);
}

.canvas {
  width: 100%;
  height: 100%;
  position: relative;
  background: var(--surface-ground);
  cursor: crosshair;
  transform-origin: 0 0; /* Ensure zoom is centered */
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
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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

.component-actions {
  display: flex;
  gap: 0.25rem;
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
  cursor: pointer;
  position: relative;
}

.threat-indicator:hover {
  background: var(--surface-hover);
}

.threat-indicator.selected {
  border: 2px solid var(--primary-color);
  box-shadow: 0 0 0 2px var(--primary-200);
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

.threat-count {
  position: absolute;
  top: -5px;
  right: -5px;
  background: var(--red-500);
  color: white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: bold;
  border: 2px solid var(--surface-card);
}

.connections {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: none;
  z-index: 5;
}

.grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(to right, var(--surface-border) 1px, transparent 1px),
    linear-gradient(to bottom, var(--surface-border) 1px, transparent 1px);
  background-size: 100px 100px;
  opacity: 0.1;
  z-index: -1;
}

.component-library {
  width: 250px;
  background: var(--surface-card);
  border-left: 1px solid var(--surface-border);
  padding: 1rem;
  overflow-y: auto;
}

.library-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.library-header h4 {
  margin: 0;
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

.form-group .p-inputtext {
  border-radius: 6px;
}

.form-group .p-inputtext:focus {
  box-shadow: 0 0 0 2px var(--primary-200), 0 0 0 4px var(--primary-200);
}

.form-group .p-inputtext.p-invalid {
  border-color: var(--red-500);
}

.form-group .p-inputtext.p-invalid:focus {
  box-shadow: 0 0 0 2px var(--red-500), 0 0 0 4px var(--red-200);
}

.form-help {
  font-size: 0.75rem;
  color: var(--text-color-secondary);
  margin-top: -0.5rem;
}

.threat-mapping {
  max-height: 400px;
  overflow-y: auto;
}

.mapping-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--surface-border);
}

.mapping-header p {
  margin: 0;
  color: var(--text-color-secondary);
  font-size: 0.9rem;
}

.mapping-actions {
  display: flex;
  gap: 0.5rem;
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

.threat-item:hover {
  background: var(--surface-hover);
}

.threat-item.selected {
  background: var(--surface-hover);
  border: 1px solid var(--primary-color);
  box-shadow: 0 0 0 2px var(--primary-200);
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

.threat-description {
  font-size: 0.8rem;
  color: var(--text-color-secondary);
  margin-left: 0.5rem;
}

.threat-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.threat-details h4 {
  margin: 0 0 0.5rem 0;
  color: var(--text-color);
}

.threat-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: var(--text-color-secondary);
}

.threat-mitigation ul {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0 0 0;
}

.threat-mitigation li {
  font-size: 0.85rem;
  color: var(--text-color-secondary);
  margin-bottom: 0.25rem;
}

.context-menu {
  position: fixed;
  background: var(--surface-card);
  border: 1px solid var(--surface-border);
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  padding: 0.5rem 0;
  min-width: 150px;
}

.context-menu-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
  font-size: 0.9rem;
  color: var(--text-color);
}

.context-menu-item:hover {
  background: var(--surface-hover);
}

.context-menu-item.danger {
  color: var(--red-500);
}

.context-menu-item.danger:hover {
  background: var(--red-100);
}

.error-boundary {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: var(--surface-ground);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.error-content {
  text-align: center;
  padding: 2rem;
  background: var(--surface-card);
  border: 1px solid var(--red-500);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.error-content i {
  font-size: 3rem;
  color: var(--red-500);
  margin-bottom: 1rem;
}

.error-content h4 {
  margin-bottom: 0.5rem;
}

.error-content p {
  margin-bottom: 1.5rem;
  color: var(--text-color-secondary);
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

  .canvas-controls {
    left: 50%;
    transform: translateX(-50%);
    top: 0.5rem;
  }
}
</style> 