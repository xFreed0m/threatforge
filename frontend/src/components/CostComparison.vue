<template>
  <Dialog v-model:visible="visible" modal header="Compare Provider Costs" :closable="true" :style="{ width: '420px' }">
    <div v-if="loading" class="cost-loading">
      <ProgressSpinner style="width: 40px; height: 40px;" />
      <span>Estimating costs...</span>
    </div>
    <div v-else>
      <div class="cost-table">
        <div class="cost-row cost-header">
          <span>Provider</span>
          <span>Estimated Cost</span>
          <span></span>
        </div>
        <div v-for="(item, idx) in sortedEstimates" :key="item.provider" class="cost-row" :class="costClass(item, idx)">
          <span>{{ item.provider }}</span>
          <span>{{ formatCost(item.estimated_cost) }} <span v-if="idx !== 0" class="cost-diff">({{ percentDiff(item.estimated_cost) }})</span></span>
          <Button label="Select" size="small" @click="select(item.provider)" :disabled="selectedProvider === item.provider" />
        </div>
      </div>
      <div class="token-estimate" v-if="tokenEstimate">
        <i class="pi pi-chart-bar" style="margin-right: 0.5rem;"></i>
        Estimated tokens: <b>{{ tokenEstimate }}</b>
      </div>
    </div>
  </Dialog>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import ProgressSpinner from 'primevue/progressspinner'

const props = defineProps({
  visible: Boolean,
  estimates: Array,
  loading: Boolean,
  selectedProvider: String,
  tokenEstimate: [String, Number]
})
const emit = defineEmits(['update:visible', 'select-provider'])

const sortedEstimates = computed(() => {
  if (!props.estimates) return []
  return [...props.estimates].sort((a, b) => a.estimated_cost - b.estimated_cost)
})

function formatCost(cost) {
  return `$${cost.toFixed(4)}`
}

function percentDiff(cost) {
  const cheapest = sortedEstimates.value[0]?.estimated_cost || 0
  if (!cheapest || cost === cheapest) return ''
  const diff = ((cost - cheapest) / cheapest) * 100
  return `${diff > 0 ? '+' : ''}${diff.toFixed(1)}%`
}

function costClass(item, idx) {
  if (idx === 0) return 'cost-cheapest'
  if (idx === sortedEstimates.value.length - 1) return 'cost-expensive'
  return 'cost-medium'
}

function select(provider) {
  emit('select-provider', provider)
  emit('update:visible', false)
}
</script>

<style scoped>
.cost-table {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}
.cost-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  font-size: 1.05rem;
}
.cost-header {
  font-weight: 600;
  background: var(--surface-section);
  color: var(--text-color-secondary);
}
.cost-cheapest {
  background: #e8f5e9;
  color: #388e3c;
}
.cost-medium {
  background: #fffde7;
  color: #fbc02d;
}
.cost-expensive {
  background: #ffebee;
  color: #d32f2f;
}
.cost-diff {
  font-size: 0.95em;
  margin-left: 0.5em;
  opacity: 0.7;
}
.token-estimate {
  margin-top: 1rem;
  color: var(--primary-color);
  font-size: 1.1rem;
  display: flex;
  align-items: center;
}
.cost-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem 0;
}
</style> 