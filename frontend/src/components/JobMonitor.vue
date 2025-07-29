<template>
  <div class="job-monitor">
    <div class="job-monitor-header">
      <h3>
        <i class="pi pi-clock" style="margin-right: 0.5rem; color: var(--primary-color);"></i>
        Job Monitor
      </h3>
      <p>Track the progress of your threat model generation jobs</p>
    </div>

    <!-- Active Jobs -->
    <div v-if="activeJobs.length > 0" class="active-jobs-section">
      <h4>Active Jobs</h4>
      <div class="job-list">
        <div v-for="job in activeJobs" :key="job.job_id" class="job-card">
          <div class="job-header">
            <div class="job-info">
              <span class="job-id">Job #{{ job.job_id.slice(-8) }}</span>
              <span class="job-status" :class="job.status">{{ job.status }}</span>
            </div>
            <div class="job-actions">
              <Button 
                v-if="job.status === 'pending' || job.status === 'processing'"
                icon="pi pi-times" 
                severity="danger" 
                size="small"
                @click="cancelJob(job.job_id)"
                :loading="cancellingJob === job.job_id"
              />
            </div>
          </div>
          
          <div class="job-progress">
            <ProgressBar :value="job.progress" :showValue="true" />
            <span class="progress-text">{{ job.progress }}% complete</span>
          </div>
          
          <div class="job-message">{{ job.message }}</div>
          
          <div class="job-meta">
            <span class="created-at">Created: {{ formatDate(job.created_at) }}</span>
            <span v-if="job.estimated_completion" class="estimated-completion">
              Estimated completion: {{ formatDate(job.estimated_completion) }}
            </span>
          </div>
          
          <!-- Job Result -->
          <div v-if="job.status === 'completed' && job.result" class="job-result">
            <div class="result-header">
              <h5>Generated Threat Model</h5>
              <Button 
                icon="pi pi-eye" 
                label="View" 
                size="small"
                @click="viewResult(job.result)"
              />
            </div>
            <div class="result-meta">
              <span class="provider">Provider: {{ job.result.provider_used }}</span>
              <span class="framework">Framework: {{ job.result.framework }}</span>
              <span class="cost">Cost: ${{ job.result.estimated_cost.toFixed(4) }}</span>
            </div>
          </div>
          
          <!-- Job Error -->
          <div v-if="job.status === 'failed' && job.error" class="job-error">
            <div class="error-header">
              <i class="pi pi-exclamation-triangle" style="color: #f44336;"></i>
              <span>Job Failed</span>
            </div>
            <div class="error-message">{{ job.error }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Completed Jobs -->
    <div v-if="completedJobs.length > 0" class="completed-jobs-section">
      <h4>Recent Completed Jobs</h4>
      <div class="job-list">
        <div v-for="job in completedJobs.slice(0, 5)" :key="job.job_id" class="job-card completed">
          <div class="job-header">
            <div class="job-info">
              <span class="job-id">Job #{{ job.job_id.slice(-8) }}</span>
              <span class="job-status completed">{{ job.status }}</span>
            </div>
            <div class="job-actions">
              <Button 
                v-if="job.result"
                icon="pi pi-eye" 
                label="View" 
                size="small"
                @click="viewResult(job.result)"
              />
            </div>
          </div>
          
          <div class="job-message">{{ job.message }}</div>
          
          <div class="job-meta">
            <span class="completed-at">Completed: {{ formatDate(job.updated_at) }}</span>
            <span v-if="job.result" class="result-info">
              {{ job.result.provider_used }} • {{ job.result.framework }} • ${{ job.result.estimated_cost.toFixed(4) }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="!activeJobs.length && !completedJobs.length" class="empty-state">
      <i class="pi pi-clock" style="font-size: 3rem; color: var(--text-color-secondary); margin-bottom: 1rem;"></i>
      <h4>No Jobs Found</h4>
      <p>Start generating threat models to see them here.</p>
    </div>

    <!-- Refresh Button -->
    <div class="refresh-section">
      <Button 
        icon="pi pi-refresh" 
        label="Refresh" 
        @click="refreshJobs"
        :loading="refreshing"
        severity="secondary"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import axios from 'axios'
import Button from 'primevue/button'
import ProgressBar from 'primevue/progressbar'
import { useToast } from 'primevue/usetoast'

const props = defineEmits(['view-result'])

const toast = useToast()

const jobs = ref([])
const refreshing = ref(false)
const cancellingJob = ref(null)
const refreshInterval = ref(null)

const activeJobs = computed(() => {
  return jobs.value.filter(job => 
    job.status === 'pending' || job.status === 'processing'
  ).sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
})

const completedJobs = computed(() => {
  return jobs.value.filter(job => 
    job.status === 'completed' || job.status === 'failed' || job.status === 'cancelled'
  ).sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at))
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString()
}

const refreshJobs = async () => {
  refreshing.value = true
  try {
    const response = await axios.get('/api/threat-model/jobs')
    jobs.value = response.data
  } catch (error) {
    console.error('Failed to refresh jobs:', error)
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to refresh jobs',
      life: 3000
    })
  } finally {
    refreshing.value = false
  }
}

const cancelJob = async (jobId) => {
  cancellingJob.value = jobId
  try {
    await axios.delete(`/api/threat-model/jobs/${jobId}`)
    toast.add({
      severity: 'success',
      summary: 'Job Cancelled',
      detail: 'Job has been cancelled successfully',
      life: 3000
    })
    await refreshJobs()
  } catch (error) {
    console.error('Failed to cancel job:', error)
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to cancel job',
      life: 3000
    })
  } finally {
    cancellingJob.value = null
  }
}

const viewResult = (result) => {
  emit('view-result', result)
}

const startAutoRefresh = () => {
  refreshInterval.value = setInterval(refreshJobs, 5000) // Refresh every 5 seconds
}

const stopAutoRefresh = () => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
    refreshInterval.value = null
  }
}

onMounted(async () => {
  await refreshJobs()
  startAutoRefresh()
})

onUnmounted(() => {
  stopAutoRefresh()
})
</script>

<style scoped>
.job-monitor {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 0;
}

.job-monitor-header {
  text-align: center;
  margin-bottom: 2rem;
}

.job-monitor-header h3 {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: 1.5rem;
  margin: 0 0 0.5rem 0;
  color: var(--text-color);
  display: flex;
  align-items: center;
  justify-content: center;
}

.job-monitor-header p {
  font-family: 'Inter', sans-serif;
  font-size: 1rem;
  color: var(--text-color-secondary);
  margin: 0;
  opacity: 0.9;
}

.active-jobs-section,
.completed-jobs-section {
  margin-bottom: 2rem;
}

.active-jobs-section h4,
.completed-jobs-section h4 {
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 1.2rem;
  margin: 0 0 1rem 0;
  color: var(--text-color);
}

.job-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.job-card {
  background: var(--surface-card);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid var(--surface-border);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.job-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.job-card.completed {
  opacity: 0.8;
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.job-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.job-id {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.9rem;
  color: var(--text-color-secondary);
  background: var(--surface-ground);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.job-status {
  font-size: 0.8rem;
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.job-status.pending {
  background: #fff3cd;
  color: #856404;
}

.job-status.processing {
  background: #cce5ff;
  color: #004085;
}

.job-status.completed {
  background: #d4edda;
  color: #155724;
}

.job-status.failed {
  background: #f8d7da;
  color: #721c24;
}

.job-status.cancelled {
  background: #e2e3e5;
  color: #383d41;
}

.job-progress {
  margin-bottom: 1rem;
}

.progress-text {
  font-size: 0.9rem;
  color: var(--text-color-secondary);
  margin-top: 0.5rem;
  display: block;
}

.job-message {
  font-size: 0.95rem;
  color: var(--text-color);
  margin-bottom: 1rem;
  line-height: 1.4;
}

.job-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
  color: var(--text-color-secondary);
  margin-bottom: 1rem;
}

.job-result {
  background: var(--surface-ground);
  border-radius: 8px;
  padding: 1rem;
  margin-top: 1rem;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.result-header h5 {
  margin: 0;
  font-size: 1rem;
  color: var(--text-color);
}

.result-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.8rem;
  color: var(--text-color-secondary);
}

.job-error {
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 8px;
  padding: 1rem;
  margin-top: 1rem;
}

.error-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #721c24;
  margin-bottom: 0.5rem;
}

.error-message {
  font-size: 0.9rem;
  color: #721c24;
  line-height: 1.4;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--text-color-secondary);
}

.empty-state h4 {
  margin: 1rem 0 0.5rem 0;
  color: var(--text-color);
}

.empty-state p {
  margin: 0;
  opacity: 0.8;
}

.refresh-section {
  text-align: center;
  margin-top: 2rem;
}

@media (max-width: 768px) {
  .job-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .result-meta {
    flex-direction: column;
    gap: 0.25rem;
  }
}
</style> 