<script setup>
import { version } from '../package.json'
</script>

<template>
  <main class="min-h-screen py-12 px-4 sm:px-6 lg:px-8 flex flex-col items-center justify-center bg-gray-50">
    <h1>DDI Tool</h1>
    <div class="mt-10 pt-4 border-t border-gray-100 text-center text-xs text-gray-400">
      Medizinische Entscheidungsunterstützung | DDI-Tool Prototyp v{{ version }} by V3ctor2
    </div>
  </main>
</template>