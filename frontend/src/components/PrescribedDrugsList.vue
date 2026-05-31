<script setup>
import { ref } from 'vue'
import { BeakerIcon, ChevronDownIcon, ExclamationTriangleIcon } from '@heroicons/vue/24/outline'

defineProps({
    drugs: {
        type: Array,
        required: true
    },
    isLoading: {
        type: Boolean,
        default: false
    }
})

const expandedId = ref(null)

const toggleExpand = (id) => {
    expandedId.value = expandedId.value === id ? null : id
}
</script>

<template>
    <div class="w-full">
        <h3 class="text-lg font-bold text-gray-900 mb-4">Aktuelle Medikation</h3>

        <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
            <div v-if="isLoading" class="p-8 text-center text-gray-500">
                Lade Medikamente...
            </div>

            <ul v-else class="divide-y divide-gray-100">
                <li v-if="drugs.length === 0" class="p-6 text-center text-gray-500">
                    Keine Medikamente verschrieben.
                </li>

                <li v-for="drug in drugs" :key="drug.id" class="flex flex-col">

                    <div @click="toggleExpand(drug.id)"
                        class="p-4 flex justify-between items-center hover:bg-gray-50 cursor-pointer transition-colors">
                        <div class="flex items-center">
                            <div
                                class="h-8 w-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center mr-3">
                                <BeakerIcon class="h-4 w-4" />
                            </div>
                            <span class="font-medium text-gray-900 capitalize">{{ drug.drug_name }}</span>
                        </div>

                        <div class="flex items-center">
                            <span v-if="drug.is_interaction"
                                class="mr-4 text-xs font-medium px-2 py-1 bg-red-100 text-red-700 rounded-md">
                                Warnungen vorhanden
                            </span>
                            <ChevronDownIcon class="h-5 w-5 text-gray-400 transition-transform duration-200"
                                :class="{ 'rotate-180': expandedId === drug.id }" />
                        </div>
                    </div>

                    <div v-show="expandedId === drug.id" class="bg-gray-50 px-4 pb-4 border-t border-gray-100">
                        <div v-if="drug.is_interaction"
                            class="p-4 bg-red-50 border border-red-100 rounded-lg flex items-start mt-4">
                            <ExclamationTriangleIcon class="w-5 h-5 text-red-600 mr-2 flex-shrink-0 mt-0.5" />
                            <div>
                                <p class="text-sm font-bold text-red-800">Interaktionen</p>
                                <ul class="text-sm text-red-700 mt-1 space-y-2">
                                    <li v-for="(interaction, index) in drug.interaction.split('|')" :key="index"
                                        class="flex items-start">
                                        <span class="mr-2">•</span>
                                        <span>{{ interaction.trim() }}</span>
                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div v-else class="mt-4 text-sm text-gray-500 p-2">
                            Keine Interaktionen bei der Verschreibung gefunden.
                        </div>
                    </div>

                </li>
            </ul>
        </div>
    </div>
</template>