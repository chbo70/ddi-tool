<script setup>
defineProps({
  doctorName: {
    type: String,
    required: true
  }
})
</script>

<template>
  <header class="w-full bg-white shadow-sm px-6 py-4 flex justify-between items-center border-b border-gray-200">
    <h1 class="text-xl font-bold text-blue-600">DDI Tool</h1>
    
    <div class="text-sm font-medium text-gray-600 flex items-center">
      <div class="mr-3 bg-blue-100 text-blue-700 h-8 w-8 rounded-full flex items-center justify-center font-bold">
        Dr.
      </div>
      Eingeloggt als: {{ doctorName }}
    </div>
  </header>
</template>