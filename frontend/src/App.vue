<script setup>
import { ref, computed } from 'vue'
import { version } from '../package.json'
import AppHeader from './components/AppHeader.vue'
import SearchBar from './components/SearchBar.vue'
import PatientList from './components/PatientList.vue'
import PatientDrugList from './components/PatientDrugList.vue'
import AppFooter from './components/AppFooter.vue'
import { fetchPatients } from './services/api.ts'

const searchQuery = ref('')
const patients = ref([])
fetchPatients(patients)
const selectedPatient = ref(null)

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

    <main class="max-w-4xl mx-auto pt-12 pb-20 px-4 sm:px-6 lg:px-8 flex flex-col items-center">
      <div v-if="!selectedPatient" class="w-full">
        <div class="text-center mb-8 w-full">
          <h2 class="text-2xl font-bold text-gray-900">Patientenübersicht</h2>
          <p class="text-sm text-gray-500 mt-2">Wählen Sie einen Patienten aus, um die Medikation zu verwalten.</p>
        </div>

        <div class="w-full mb-8">
          <SearchBar v-model="searchQuery" placeholder="Patientenname eingeben..." />
        </div>

        <PatientList :patients="filteredPatients" @select-patient="selectedPatient = $event" />
      </div>

      <div v-else class="w-full">
        <PatientDrugList :patient="selectedPatient" @back="selectedPatient = null" />
      </div>

      <AppFooter :version="version" />

    </main>
  </div>
</template>