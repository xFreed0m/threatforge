<template>
  <div class="threat-model-tutorial" v-if="showTutorial">
    <div class="tutorial-overlay" @click="closeTutorial"></div>
    
    <div class="tutorial-modal">
      <div class="tutorial-header">
        <h2>
          <i class="pi pi-graduation-cap" style="margin-right: 0.5rem; color: var(--primary-color);"></i>
          Threat Modeling Tutorial
        </h2>
        <Button 
          icon="pi pi-times" 
          @click="closeTutorial"
          class="close-btn"
          severity="secondary"
          text
        />
      </div>

      <div class="tutorial-content">
        <div class="tutorial-progress">
          <ProgressBar :value="progressPercentage" :showValue="true" />
          <span class="progress-text">Step {{ currentStep }} of {{ totalSteps }}</span>
        </div>

        <div class="tutorial-step" v-if="currentStep === 1">
          <h3>Welcome to Threat Modeling! 🛡️</h3>
          <p>This tutorial will guide you through creating your first threat model using ThreatForge's AI-powered analysis.</p>
          
          <div class="step-content">
            <h4>What is Threat Modeling?</h4>
            <p>Threat modeling is a systematic approach to identifying, quantifying, and addressing security risks in your software systems.</p>
            
            <div class="benefits-grid">
              <div class="benefit-card">
                <i class="pi pi-shield"></i>
                <h5>Identify Threats</h5>
                <p>Find potential security vulnerabilities in your system</p>
              </div>
              <div class="benefit-card">
                <i class="pi pi-chart-line"></i>
                <h5>Assess Risks</h5>
                <p>Evaluate the likelihood and impact of threats</p>
              </div>
              <div class="benefit-card">
                <i class="pi pi-cog"></i>
                <h5>Plan Mitigations</h5>
                <p>Develop strategies to reduce security risks</p>
              </div>
            </div>
          </div>
        </div>

        <div class="tutorial-step" v-if="currentStep === 2">
          <h3>Step 1: Describe Your System 📝</h3>
          <p>Start by providing a comprehensive description of the system you want to analyze.</p>
          
          <div class="step-content">
            <h4>What to Include:</h4>
            <ul class="tutorial-list">
              <li><strong>System Purpose:</strong> What does your system do?</li>
              <li><strong>User Types:</strong> Who uses the system?</li>
              <li><strong>Key Features:</strong> What are the main functions?</li>
              <li><strong>Technologies:</strong> What technologies does it use?</li>
              <li><strong>Data Types:</strong> What kind of data does it handle?</li>
            </ul>

            <div class="example-box">
              <h5>Example System Description:</h5>
              <pre><code>Our web application is a customer portal that allows users to:
- Register and authenticate using email/password
- View and update their profile information
- Upload and download documents (PDF, images)
- Make payments using credit cards
- Access support tickets and chat with agents

The system uses:
- React frontend with Node.js backend
- PostgreSQL database for user data
- AWS S3 for file storage
- Stripe for payment processing
- Redis for session management</code></pre>
            </div>
          </div>
        </div>

        <div class="tutorial-step" v-if="currentStep === 3">
          <h3>Step 2: Choose a Framework 🎯</h3>
          <p>Select the threat modeling framework that best fits your system.</p>
          
          <div class="step-content">
            <div class="framework-cards">
              <div class="framework-card" :class="{ selected: selectedFramework === 'STRIDE' }" @click="selectFramework('STRIDE')">
                <h4>STRIDE</h4>
                <p>Microsoft's framework for general security threats</p>
                <ul>
                  <li>Spoofing</li>
                  <li>Tampering</li>
                  <li>Repudiation</li>
                  <li>Information Disclosure</li>
                  <li>Denial of Service</li>
                  <li>Elevation of Privilege</li>
                </ul>
                <span class="best-for">Best for: Software applications</span>
              </div>

              <div class="framework-card" :class="{ selected: selectedFramework === 'LINDDUN' }" @click="selectFramework('LINDDUN')">
                <h4>LINDDUN</h4>
                <p>Privacy-focused threat modeling</p>
                <ul>
                  <li>Linkability</li>
                  <li>Identifiability</li>
                  <li>Non-repudiation</li>
                  <li>Detectability</li>
                  <li>Disclosure</li>
                  <li>Unawareness</li>
                  <li>Non-compliance</li>
                </ul>
                <span class="best-for">Best for: Systems with personal data</span>
              </div>

              <div class="framework-card" :class="{ selected: selectedFramework === 'PASTA' }" @click="selectFramework('PASTA')">
                <h4>PASTA</h4>
                <p>Process for Attack Simulation and Threat Analysis</p>
                <ul>
                  <li>Business context</li>
                  <li>Attack vectors</li>
                  <li>Threat intelligence</li>
                  <li>Risk assessment</li>
                  <li>Attack simulation</li>
                </ul>
                <span class="best-for">Best for: Enterprise systems</span>
              </div>

              <div class="framework-card" :class="{ selected: selectedFramework === 'ATTACK_TREES' }" @click="selectFramework('ATTACK_TREES')">
                <h4>Attack Trees</h4>
                <p>Hierarchical representation of attack scenarios</p>
                <ul>
                  <li>Specific attack paths</li>
                  <li>Detailed analysis</li>
                  <li>Attack scenario mapping</li>
                  <li>Countermeasure planning</li>
                </ul>
                <span class="best-for">Best for: Critical systems</span>
              </div>
            </div>
          </div>
        </div>

        <div class="tutorial-step" v-if="currentStep === 4">
          <h3>Step 3: Upload Diagrams (Optional) 📊</h3>
          <p>Upload system architecture diagrams to enhance the analysis.</p>
          
          <div class="step-content">
            <h4>Supported File Types:</h4>
            <div class="file-types">
              <span class="file-type">DRAWIO</span>
              <span class="file-type">PNG</span>
              <span class="file-type">JPG</span>
              <span class="file-type">SVG</span>
              <span class="file-type">XML</span>
            </div>

            <h4>Tips for Effective Diagrams:</h4>
            <ul class="tutorial-list">
              <li>Include data flow between components</li>
              <li>Show external interfaces and APIs</li>
              <li>Highlight sensitive data storage</li>
              <li>Include authentication and authorization points</li>
              <li>Keep diagrams clear and readable</li>
            </ul>

            <div class="example-box">
              <h5>Diagram Best Practices:</h5>
              <div class="diagram-tips">
                <div class="tip">
                  <i class="pi pi-check-circle"></i>
                  <span>Show system boundaries clearly</span>
                </div>
                <div class="tip">
                  <i class="pi pi-check-circle"></i>
                  <span>Include data classification</span>
                </div>
                <div class="tip">
                  <i class="pi pi-check-circle"></i>
                  <span>Mark security controls</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="tutorial-step" v-if="currentStep === 5">
          <h3>Step 4: Choose Processing Mode ⚡</h3>
          <p>Select between synchronous and asynchronous processing.</p>
          
          <div class="step-content">
            <div class="mode-comparison">
              <div class="mode-card">
                <h4><i class="pi pi-bolt"></i> Sync Mode</h4>
                <p>Generate results immediately</p>
                <ul>
                  <li>✅ Instant results</li>
                  <li>✅ Simple systems</li>
                  <li>✅ Quick analysis</li>
                  <li>❌ Limited to simple systems</li>
                </ul>
                <span class="best-for">Best for: Simple applications</span>
              </div>

              <div class="mode-card">
                <h4><i class="pi pi-clock"></i> Async Mode</h4>
                <p>Background processing with progress tracking</p>
                <ul>
                  <li>✅ Complex systems</li>
                  <li>✅ Progress tracking</li>
                  <li>✅ Can cancel jobs</li>
                  <li>❌ Takes longer</li>
                </ul>
                <span class="best-for">Best for: Complex systems</span>
              </div>
            </div>
          </div>
        </div>

        <div class="tutorial-step" v-if="currentStep === 6">
          <h3>Step 5: Generate and Review 🎉</h3>
          <p>Generate your threat model and review the results.</p>
          
          <div class="step-content">
            <h4>What You'll Get:</h4>
            <div class="results-preview">
              <div class="result-section">
                <h5><i class="pi pi-list"></i> System Overview</h5>
                <p>Summary of your analyzed system</p>
              </div>
              <div class="result-section">
                <h5><i class="pi pi-shield"></i> Threat Analysis</h5>
                <p>Detailed threats using your chosen framework</p>
              </div>
              <div class="result-section">
                <h5><i class="pi pi-chart-bar"></i> Risk Assessment</h5>
                <p>Threat ratings (High/Medium/Low)</p>
              </div>
              <div class="result-section">
                <h5><i class="pi pi-cog"></i> Mitigation Strategies</h5>
                <p>Recommended security controls</p>
              </div>
            </div>

            <div class="next-steps">
              <h4>Next Steps:</h4>
              <ol class="tutorial-list">
                <li>Review the generated threats</li>
                <li>Prioritize high-risk threats</li>
                <li>Implement recommended mitigations</li>
                <li>Update threat model as system evolves</li>
                <li>Conduct regular security assessments</li>
              </ol>
            </div>
          </div>
        </div>
      </div>

      <div class="tutorial-footer">
        <Button 
          v-if="currentStep > 1"
          @click="previousStep"
          label="Previous"
          icon="pi pi-chevron-left"
          severity="secondary"
        />
        <Button 
          v-if="currentStep < totalSteps"
          @click="nextStep"
          label="Next"
          icon="pi pi-chevron-right"
          iconPos="right"
        />
        <Button 
          v-if="currentStep === totalSteps"
          @click="startThreatModeling"
          label="Start Threat Modeling"
          icon="pi pi-play"
          iconPos="right"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Button from 'primevue/button'
import ProgressBar from 'primevue/progressbar'

const props = defineProps({
  showTutorial: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'start-modeling'])

const currentStep = ref(1)
const totalSteps = 6
const selectedFramework = ref('STRIDE')

const progressPercentage = computed(() => {
  return (currentStep.value / totalSteps) * 100
})

const nextStep = () => {
  if (currentStep.value < totalSteps) {
    currentStep.value++
  }
}

const previousStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

const selectFramework = (framework) => {
  selectedFramework.value = framework
}

const closeTutorial = () => {
  emit('close')
}

const startThreatModeling = () => {
  emit('start-modeling')
  closeTutorial()
}
</script>

<style scoped>
.threat-model-tutorial {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tutorial-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
}

.tutorial-modal {
  position: relative;
  background: var(--surface-card);
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  max-width: 800px;
  width: 90%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.tutorial-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid var(--surface-border);
  background: var(--surface-section);
}

.tutorial-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--text-color);
  display: flex;
  align-items: center;
}

.tutorial-content {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
}

.tutorial-progress {
  margin-bottom: 2rem;
}

.progress-text {
  font-size: 0.9rem;
  color: var(--text-color-secondary);
  margin-top: 0.5rem;
  display: block;
}

.tutorial-step h3 {
  margin: 0 0 1rem 0;
  color: var(--text-color);
  font-size: 1.3rem;
}

.tutorial-step p {
  color: var(--text-color-secondary);
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.step-content h4 {
  margin: 1.5rem 0 1rem 0;
  color: var(--text-color);
  font-size: 1.1rem;
}

.tutorial-list {
  list-style: none;
  padding: 0;
  margin: 1rem 0;
}

.tutorial-list li {
  padding: 0.5rem 0;
  color: var(--text-color-secondary);
  line-height: 1.5;
}

.tutorial-list li::before {
  content: "•";
  color: var(--primary-color);
  font-weight: bold;
  margin-right: 0.5rem;
}

.benefits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin: 1.5rem 0;
}

.benefit-card {
  background: var(--surface-section);
  border: 1px solid var(--surface-border);
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
}

.benefit-card i {
  font-size: 2rem;
  color: var(--primary-color);
  margin-bottom: 0.5rem;
}

.benefit-card h5 {
  margin: 0.5rem 0;
  color: var(--text-color);
}

.benefit-card p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--text-color-secondary);
}

.example-box {
  background: var(--surface-ground);
  border: 1px solid var(--surface-border);
  border-radius: 8px;
  padding: 1rem;
  margin: 1rem 0;
}

.example-box h5 {
  margin: 0 0 0.5rem 0;
  color: var(--text-color);
}

.example-box pre {
  background: var(--surface-card);
  border: 1px solid var(--surface-border);
  border-radius: 4px;
  padding: 1rem;
  overflow-x: auto;
  font-size: 0.85rem;
  line-height: 1.4;
}

.framework-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin: 1rem 0;
}

.framework-card {
  background: var(--surface-section);
  border: 2px solid var(--surface-border);
  border-radius: 8px;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.framework-card:hover {
  border-color: var(--primary-color);
  transform: translateY(-2px);
}

.framework-card.selected {
  border-color: var(--primary-color);
  background: var(--primary-50);
}

.framework-card h4 {
  margin: 0 0 0.5rem 0;
  color: var(--text-color);
}

.framework-card p {
  margin: 0 0 1rem 0;
  color: var(--text-color-secondary);
  font-size: 0.9rem;
}

.framework-card ul {
  list-style: none;
  padding: 0;
  margin: 0 0 1rem 0;
}

.framework-card li {
  padding: 0.25rem 0;
  font-size: 0.85rem;
  color: var(--text-color-secondary);
}

.best-for {
  font-size: 0.8rem;
  color: var(--primary-color);
  font-weight: 600;
}

.file-types {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin: 1rem 0;
}

.file-type {
  background: var(--primary-color);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.diagram-tips {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.tip {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-color-secondary);
}

.tip i {
  color: var(--green-500);
}

.mode-comparison {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin: 1rem 0;
}

.mode-card {
  background: var(--surface-section);
  border: 1px solid var(--surface-border);
  border-radius: 8px;
  padding: 1rem;
}

.mode-card h4 {
  margin: 0 0 0.5rem 0;
  color: var(--text-color);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.mode-card p {
  margin: 0 0 1rem 0;
  color: var(--text-color-secondary);
}

.mode-card ul {
  list-style: none;
  padding: 0;
  margin: 0 0 1rem 0;
}

.mode-card li {
  padding: 0.25rem 0;
  font-size: 0.9rem;
  color: var(--text-color-secondary);
}

.results-preview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin: 1rem 0;
}

.result-section {
  background: var(--surface-section);
  border: 1px solid var(--surface-border);
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
}

.result-section h5 {
  margin: 0 0 0.5rem 0;
  color: var(--text-color);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.result-section p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--text-color-secondary);
}

.next-steps {
  background: var(--surface-ground);
  border: 1px solid var(--surface-border);
  border-radius: 8px;
  padding: 1rem;
  margin: 1rem 0;
}

.next-steps ol {
  margin: 0;
  padding-left: 1.5rem;
}

.next-steps li {
  padding: 0.25rem 0;
  color: var(--text-color-secondary);
}

.tutorial-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-top: 1px solid var(--surface-border);
  background: var(--surface-section);
}

@media (max-width: 768px) {
  .tutorial-modal {
    width: 95%;
    max-height: 95vh;
  }
  
  .tutorial-content {
    padding: 1rem;
  }
  
  .framework-cards {
    grid-template-columns: 1fr;
  }
  
  .mode-comparison {
    grid-template-columns: 1fr;
  }
  
  .benefits-grid {
    grid-template-columns: 1fr;
  }
  
  .results-preview {
    grid-template-columns: 1fr;
  }
}
</style> 