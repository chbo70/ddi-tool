
function fetchPatients(patients: any) {
    fetch('http://localhost:8000/api/patients')
    .then(response => response.json())
    .then(data => {
        patients.value = data.patients
        return data.patients
    })
    .catch(error => {
        console.error('Error fetching patients:', error)
    })
}

async function fetchPatientDrugs(patientId: number, prescribedDrugs: any) {
    try {
        const response = await fetch(`http://localhost:8000/api/prefetch/${patientId}`)
        const data = await response.json()
        prescribedDrugs.value = data.patient_drugs
        return data.prescribedDrugs
    } catch (error) {
        console.error(`Error fetching drugs for patient ${patientId}:`, error)
    }

}

async function fetchDrugInteractions(drugName: string) {
    try {
        const response = await fetch("http://localhost:8000/api/interaction", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                drug: drugName
            })
        });
        const data = await response.json()
        return data.interactions
    }
    catch (error) {
        console.error(`Error fetching interactions for drug ${drugName}:`, error)
    }
}

async function addDrugToPatient(patientId: number, drugName: string, isInteraction: boolean, interaction: string) {
    const response = await fetch(`http://localhost:8000/api/patients/${patientId}/drugs`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            drug_name: drugName,
            is_interaction: isInteraction,
            interaction: interaction
        })
    });
    return response.json();
}

export { fetchPatients, fetchPatientDrugs, fetchDrugInteractions, addDrugToPatient }