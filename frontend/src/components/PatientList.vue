<script setup>
defineProps({
  patients: {
    type: Array,
    required: true
  }
})
</script>

<template>
  <div class="w-full bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
    <ul class="divide-y divide-gray-100">
      
      <li v-if="patients.length === 0" class="p-6 text-center text-gray-500">
        Keine Patienten gefunden.
      </li>
      
      <li 
        v-for="patient in patients" 
        :key="patient.id"
        class="p-4 hover:bg-blue-50 cursor-pointer flex justify-between items-center"
        @click="$emit('select-patient', patient)"
      >
        <div class="flex flex-col">
          <span class="font-medium text-gray-900">{{ patient.name }}</span>
          <span class="text-xs text-gray-500 mt-1">Geb: {{ patient.dob }}</span>
        </div>
        
        <div class="flex items-center">
           <span class="px-2 py-1 text-xs rounded-full font-medium bg-yellow-100 text-yellow-700">
             {{ patient.drugCounter }} Medikamente
           </span>
           <svg class="h-5 w-5 text-gray-400 ml-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
             <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
           </svg>
        </div>
      </li>
      
    </ul>
  </div>
</template>