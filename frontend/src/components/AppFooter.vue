<script setup>
defineProps({
  version: {
    type: String,
    required: true
  }
})
</script>

<template>
  <footer class="mt-12 pt-6 w-full border-t border-gray-200 text-center text-xs text-gray-400">
    Medizinische Entscheidungsunterstützung | DDI-Tool Prototyp v{{ version }} von V3ctor2
  </footer>
</template>