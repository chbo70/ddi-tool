# Features
## Targetgroup
- Doctors (with a list of patients)

## App Flow
1. Already Logged in 
2. Has Patient List with their Profile
3. Patient List contains Information about (Base Infromation, Disease, Current Medication (if the data is available we could add dosis))
4. Can add new Presiciption
5. Modal opens with search bar and already prescribed medication (already prefiltered)
6. Enter a drug and either there is an interaction or not
7. Add it to the precribed drugs

## Backend

- Database with transformed dataset of drugs from csv
- API Interface: Search Drugs, Add Patient, Delete Patient, Add Drug to Patient

## Frontend

- Simple UI Inputs
- List of patients on root path - Button to view medication
- Medication view lists all prescribed medication of patient 
- Add new medication -> opens search bar and  




## Future Implementations

- Default drug search of two different drugs
- Add more information to the drugs, enabling dosis interaction
- Allow multiple concurrent drug adding
- Prefilter drugs with the associated category of the drug
- Recommendation of alternative drugs of the category, in case of a negative interaction