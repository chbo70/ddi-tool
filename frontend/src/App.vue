<script setup>
import { ref, computed } from 'vue'
import { version } from '../package.json'
import AppHeader from './components/AppHeader.vue'
import PatientSearch from './components/PatientSearch.vue'
import PatientList from './components/PatientList.vue'
import AppFooter from './components/AppFooter.vue'

const searchQuery = ref('')
const patients = ref([
  { id: 1, name: 'Max Mustermann', dob: '12.04.1985', drugCount: 3 },
  { id: 2, name: 'Erika Musterfrau', dob: '05.11.1992', drugCount: 1 },
  { id: 3, name: 'Johannes Schmidt', dob: '23.08.1964', drugCount: 2 },
  { id: 4, name: 'Anna Weber', dob: '17.02.1978', drugCount: 4 }
])

const filteredPatients = computed(() => {
  if (!searchQuery.value) return patients.value
  return patients.value.filter(p => 
    p.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})
</script>

<template>
  <div class="min-h-screen bg-gray-50 font-sans">
    
    <AppHeader doctorName="Dr. med. Müller" />

    <main class="max-w-3xl mx-auto pt-12 pb-20 px-4 sm:px-6 lg:px-8 flex flex-col items-center">
      
      <div class="text-center mb-8 w-full">
        <h2 class="text-2xl font-bold text-gray-900">Patientenübersicht</h2>
        <p class="text-sm text-gray-500 mt-2">Wählen Sie einen Patienten aus, um die Medikation zu verwalten.</p>
      </div>

      <div class="w-full mb-8">
        <PatientSearch v-model="searchQuery" />
      </div>

      <PatientList :patients="filteredPatients" />

      <AppFooter :version="version" />
      
    </main>
  </div>
</template>