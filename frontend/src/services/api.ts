
function fetchPatients(patients: any) {
    fetch('http://localhost:8000/patients')
    .then(response => response.json())
    .then(data => {
        console.log('Fetched patients:', data)
        patients.value = data.patients
        return data.patients
    })
    .catch(error => {
        console.error('Error fetching patients:', error)
    })
}

export { fetchPatients }