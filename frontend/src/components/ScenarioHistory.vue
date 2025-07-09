<template>
  <div class="scenario-history cyber-card" style="margin-bottom: 2rem;">
    <Panel header="Scenario History" :toggleable="true" v-model:collapsed="collapsed" class="history-panel">
      <DataTable :value="history" :loading="loading" class="p-datatable-sm">
        <Column field="company_name" header="Company" />
        <Column field="industry" header="Industry" />
        <Column field="created_at" header="Date" :body="formatDate" />
        <Column field="preview" header="Preview" :body="previewBody" />
        <Column header="Actions" :body="actionBody" style="width: 120px;" />
      </DataTable>
      <Toast />
      <ConfirmDialog />
    </Panel>
  </div>
</template>

<script setup>
import { ref, onMounted, h } from 'vue'
import axios from 'axios'
import Panel from 'primevue/panel'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Toast from 'primevue/toast'
import { useToast } from 'primevue/usetoast'
import ConfirmDialog from 'primevue/confirmdialog'
import { useConfirm } from 'primevue/useconfirm'

const history = ref([])
const loading = ref(false)
const collapsed = ref(true)
const toast = useToast()
const confirm = useConfirm()

const emit = defineEmits(['load-scenario'])

onMounted(fetchHistory)

async function fetchHistory() {
  loading.value = true
  try {
    const res = await axios.get('/api/scenarios/history')
    history.value = res.data
  } finally {
    loading.value = false
  }
}

function formatDate(row) {
  return new Date(row.created_at).toLocaleString()
}

function previewBody(row) {
  return row.preview
}

function actionBody(row) {
  return [
    h(Button, {
      icon: 'pi pi-eye',
      size: 'small',
      text: true,
      rounded: true,
      class: 'p-button-text p-button-info',
      title: 'View',
      onClick: () => viewScenario(row)
    }),
    h(Button, {
      icon: 'pi pi-trash',
      size: 'small',
      text: true,
      rounded: true,
      class: 'p-button-text p-button-danger',
      title: 'Delete',
      style: 'margin-left: 0.5rem;',
      onClick: () => confirmDelete(row)
    })
  ]
}

async function viewScenario(item) {
  // Fetch full scenario details from backend (simulate for now)
  // In real app, backend should return full scenario and form_data
  // For now, just emit with what we have
  const res = await axios.get('/api/scenarios/history')
  const full = res.data.find(s => s.id === item.id)
  if (full) {
    emit('load-scenario', { scenario: full, formData: full.form_data })
  } else {
    toast.add({ severity: 'error', summary: 'Not found', detail: 'Scenario not found', life: 2000 })
  }
}

function confirmDelete(item) {
  confirm.require({
    message: 'Are you sure you want to delete this scenario?',
    header: 'Delete Confirmation',
    icon: 'pi pi-exclamation-triangle',
    accept: () => deleteScenario(item.id)
  })
}

async function deleteScenario(id) {
  try {
    await axios.delete(`/api/scenarios/history/${id}`)
    toast.add({ severity: 'success', summary: 'Deleted', detail: 'Scenario deleted', life: 2000 })
    await fetchHistory()
  } catch (err) {
    toast.add({ severity: 'error', summary: 'Delete failed', detail: err.response?.data?.detail || 'Failed to delete', life: 3000 })
  }
}
</script>

<style scoped>
.history-panel {
  margin-bottom: 2rem;
}
</style> 