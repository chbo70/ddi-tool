<script setup>
import SearchBar from './SearchBar.vue'
import { fetchPatientDrugs, fetchDrugInteractions, addDrugToPatient } from '../services/api.ts'
import { ref, watch, onMounted } from 'vue'
import { BeakerIcon, ExclamationTriangleIcon, CheckCircleIcon } from '@heroicons/vue/24/outline'
import PrescribedDrugsList from './PrescribedDrugsList.vue'

const props = defineProps({
    patient: {
        type: Object,
        required: true
    }
})

defineEmits(['back'])

const prescribedDrugs = ref([])
const searchQuery = ref('')
const interactionResults = ref([])
const isLoading = ref(false)
const isSearching = ref(false)
const isSaving = ref(false)

const checkInteractions = async (newDrug) => {
    if (!newDrug) {
        interactionResults.value = []
        return
    }

    isSearching.value = true

    try {
        const interactions = await fetchDrugInteractions(newDrug)
        interactionResults.value = interactions
    } catch (error) {
        console.error("Fehler bei der Interaktionsprüfung:", error)
    } finally {
        isSearching.value = false
    }
}

const handleAddDrug = async () => {
    if (!searchQuery.value) return
    isSaving.value = true

    try {
        const hasInteraction = interactionResults.value.length > 0
        const interactionText = hasInteraction
            ? interactionResults.value.map(r => `${r.drug1} + ${r.drug2}: ${r.interaction}`).join(" | ")
            : null;

        await addDrugToPatient(props.patient.id, searchQuery.value, hasInteraction, interactionText)

        searchQuery.value = ''
        interactionResults.value = []

        fetchPatientDrugs(props.patient.id, prescribedDrugs)
    } catch (error) {
        console.error("Fehler beim Hinzufügen des Medikaments:", error)
    } finally {
        isSaving.value = false
    }
}

let searchTimeout
watch(searchQuery, (newValue) => {
    clearTimeout(searchTimeout)
    searchTimeout = setTimeout(() => {
        checkInteractions(newValue)
    }, 500)
})

onMounted(() => {
    fetchPatientDrugs(props.patient.id, prescribedDrugs)
})
</script>

<template>
    <div class="w-full">
        <button @click="$emit('back')"
            class="mb-6 flex items-center text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18">
                </path>
            </svg>
            Zurück zur Übersicht
        </button>

        <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-8 flex justify-between items-center">
            <div>
                <h2 class="text-2xl font-bold text-gray-900">{{ props.patient.name }}</h2>
                <p class="text-sm text-gray-500 mt-1">Geburtsdatum: {{ props.patient.dob }}</p>
            </div>
            <div class="bg-blue-50 text-blue-700 px-4 py-2 rounded-lg text-sm font-medium">
                {{ prescribedDrugs.length }} aktive Medikamente
            </div>
        </div>

        <SearchBar v-model="searchQuery" placeholder="Medikamentenname eingeben..." class="mb-6" />

        <div v-if="searchQuery && !isSearching" class="mb-8">

            <div v-if="interactionResults.length > 0" class="p-5 bg-red-50 border border-red-200 rounded-xl">
                <div class="flex items-center mb-3">
                    <ExclamationTriangleIcon class="w-6 h-6 text-red-600 mr-2" />
                    <h4 class="text-red-800 font-bold text-lg">Interaktion erkannt!</h4>
                </div>
                <ul class="space-y-2">
                    <li v-for="(result, index) in interactionResults" :key="index"
                        class="text-sm text-red-700 bg-white bg-opacity-50 p-3 rounded-lg border border-red-100">
                        <span class="font-bold capitalize">{{ result.drug1 }}</span> + <span
                            class="font-bold capitalize">{{ result.drug2 }}</span>:
                        <span class="ml-1">{{ result.interaction }}</span>
                    </li>
                </ul>
            </div>

            <div v-if="searchQuery && !isSearching" class="mb-8">

                <div class="mt-4 flex justify-end">
                    <button @click="handleAddDrug" :disabled="isSaving" :class="[
                        'px-4 py-2 rounded-lg font-medium text-white transition-colors flex items-center shadow-sm',
                        interactionResults.length > 0
                            ? 'bg-red-600 hover:bg-red-700'
                            : 'bg-green-600 hover:bg-green-700', 
                        isSaving ? 'opacity-50 cursor-not-allowed' : ''
                    ]">
                        <span v-if="isSaving">Wird gespeichert...</span>
                        <span v-else-if="interactionResults.length > 0">Trotz Warnung verschreiben</span>
                        <span v-else>Medikament verschreiben</span>
                    </button>
                </div>
            </div>

            <div v-else class="p-4 bg-green-50 border border-green-200 rounded-xl flex items-center">
                <CheckCircleIcon class="w-5 h-5 text-green-600 mr-2" />
                <span class="text-green-700 text-sm font-medium">Keine bekannten Interaktionen mit der aktuellen
                    Medikation gefunden. Sicher zu verschreiben.</span>
            </div>
        </div>

        <PrescribedDrugsList 
            :drugs="prescribedDrugs" 
            :isLoading="isLoading" 
        />
    </div>
</template>