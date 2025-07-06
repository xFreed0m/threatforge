<template>
  <div style="margin: 100px;">
    <Dropdown
      v-model="selected"
      :options="['Option 1', 'Option 2', 'Option 3']"
      appendTo="body"
      placeholder="Select an option"
      style="width: 200px"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Dropdown from 'primevue/dropdown'

const selected = ref(null)
</script> 